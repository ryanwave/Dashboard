"""Folder tree, revision history and activity log.

Layout on disk (ROOT is e.g. C:\\Dashboard):

    ROOT/<Model>/<Milestone>/<Variant>/<document>.xlsx   <- live documents
    ROOT/.dochub/docs/<relative path>/revisions.json      <- revision log
    ROOT/.dochub/docs/<relative path>/r0003.xlsx          <- full snapshots
    ROOT/.dochub/docs/<relative path>/meta.json           <- status, etc.
    ROOT/.dochub/activity.jsonl                           <- global feed

Every revision stores who, when, a note, and the exact list of changed
cells (old -> new), so the change history is documented automatically.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
import shutil
import tempfile
import threading
from pathlib import Path

from openpyxl import load_workbook

from . import excel_reader, excel_writer

DOC_EXTS = (".xlsx", ".xlsm")
STATUSES = ["Draft", "In Review", "Approved", "Released"]
META_DIR = ".dochub"

_lock = threading.RLock()


class Conflict(Exception):
    def __init__(self, latest):
        super().__init__("Document was changed by someone else")
        self.latest = latest


class FileLocked(Exception):
    pass


def now_iso() -> str:
    return dt.datetime.now().astimezone().isoformat(timespec="seconds")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def _visible(name: str) -> bool:
    return not (name.startswith(".") or name.startswith("~$") or name.startswith("__"))


class Store:
    def __init__(self, root: str):
        self.root = Path(root).resolve()
        self.root.mkdir(parents=True, exist_ok=True)
        self.meta_root = self.root / META_DIR
        (self.meta_root / "docs").mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------------ paths
    def resolve(self, rel: str) -> Path:
        rel = (rel or "").replace("\\", "/").strip("/")
        p = (self.root / rel).resolve()
        if p != self.root and self.root not in p.parents:
            raise PermissionError("Path escapes the document root")
        if any(part.startswith(".") for part in Path(rel).parts):
            raise PermissionError("Hidden paths are not accessible")
        return p

    def rel(self, p: Path) -> str:
        return p.resolve().relative_to(self.root).as_posix()

    def doc_dir(self, rel: str) -> Path:
        d = self.meta_root / "docs" / rel
        d.mkdir(parents=True, exist_ok=True)
        return d

    # ------------------------------------------------------------------- tree
    def _subdirs(self, p: Path):
        try:
            return sorted((d for d in p.iterdir() if d.is_dir() and _visible(d.name)), key=lambda d: d.name.lower())
        except OSError:
            return []

    def _docs(self, p: Path):
        try:
            return sorted((f for f in p.iterdir() if f.is_file() and _visible(f.name)
                           and f.suffix.lower() in DOC_EXTS), key=lambda f: f.name.lower())
        except OSError:
            return []

    def doc_summary(self, f: Path) -> dict:
        rel = self.rel(f)
        st = f.stat()
        revs = self._read_revisions(rel)
        last = revs[-1] if revs else None
        meta = self._read_meta(rel)
        return {
            "name": f.stem,
            "file": f.name,
            "path": rel,
            "size": st.st_size,
            "modified": dt.datetime.fromtimestamp(st.st_mtime).astimezone().isoformat(timespec="seconds"),
            "rev": last["rev"] if last else 0,
            "revisions": len(revs),
            "lastUser": last["user"] if last else None,
            "lastNote": last.get("note") if last else None,
            "status": meta.get("status", "Draft"),
        }

    def tree(self) -> dict:
        models = []
        for m in self._subdirs(self.root):
            milestones = []
            for ms in self._subdirs(m):
                variants = []
                for v in self._subdirs(ms):
                    variants.append({"name": v.name, "documents": [self.doc_summary(f) for f in self._docs(v)]})
                milestones.append({"name": ms.name, "variants": variants})
            models.append({"name": m.name, "milestones": milestones})
        return {"root": str(self.root), "models": models, "statuses": STATUSES}

    def all_docs(self):
        for m in self._subdirs(self.root):
            for ms in self._subdirs(m):
                for v in self._subdirs(ms):
                    for f in self._docs(v):
                        yield f

    # --------------------------------------------------------------- metadata
    def _read_json(self, p: Path, default):
        try:
            with open(p, encoding="utf-8") as fh:
                return json.load(fh)
        except (OSError, ValueError):
            return default

    def _write_json(self, p: Path, data):
        p.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp = tempfile.mkstemp(dir=p.parent, suffix=".tmp")
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=1, ensure_ascii=False)
        os.replace(tmp, p)

    def _read_revisions(self, rel: str) -> list:
        return self._read_json(self.meta_root / "docs" / rel / "revisions.json", [])

    def _read_meta(self, rel: str) -> dict:
        return self._read_json(self.meta_root / "docs" / rel / "meta.json", {})

    def log_activity(self, entry: dict):
        with open(self.meta_root / "activity.jsonl", "a", encoding="utf-8") as fh:
            fh.write(json.dumps(entry, ensure_ascii=False) + "\n")

    def activity(self, limit=None) -> list:
        items = []
        try:
            with open(self.meta_root / "activity.jsonl", encoding="utf-8") as fh:
                for line in fh:
                    try:
                        items.append(json.loads(line))
                    except ValueError:
                        pass
        except OSError:
            pass
        items.reverse()
        return items[:limit] if limit else items

    # --------------------------------------------------------------- revisions
    def _snapshot(self, rel: str, rev: int, src: Path) -> str:
        name = f"r{rev:04d}{src.suffix.lower()}"
        shutil.copy2(src, self.doc_dir(rel) / name)
        return name

    def sync(self, rel: str) -> list:
        """Make sure the revision log reflects the file on disk.

        Creates the baseline revision the first time a document is seen and
        records a revision (with a cell diff) when the file was edited
        outside the app, e.g. directly in Excel.
        """
        with _lock:
            f = self.resolve(rel)
            revs = self._read_revisions(rel)
            st = f.stat()
            if revs:
                last = revs[-1]
                if last.get("mtime") == st.st_mtime and last.get("size") == st.st_size:
                    return revs
                digest = sha256(f)
                if digest == last.get("sha"):
                    last["mtime"], last["size"] = st.st_mtime, st.st_size
                    self._write_json(self.doc_dir(rel) / "revisions.json", revs)
                    return revs
                prev_snapshot = self.doc_dir(rel) / last["file"]
                try:
                    changes = diff_files(prev_snapshot, f)
                except Exception:
                    changes = []
                rev = last["rev"] + 1
                entry = {
                    "rev": rev, "user": "Outside DocHub", "time": now_iso(), "kind": "external",
                    "note": "File was modified outside DocHub (e.g. directly in Excel)",
                    "changes": changes, "file": self._snapshot(rel, rev, f),
                    "sha": digest, "mtime": st.st_mtime, "size": st.st_size,
                }
            else:
                entry = {
                    "rev": 0, "user": "System", "time": now_iso(), "kind": "import",
                    "note": "Document imported into DocHub", "changes": [],
                    "file": self._snapshot(rel, 0, f), "sha": sha256(f),
                    "mtime": st.st_mtime, "size": st.st_size,
                }
            revs.append(entry)
            self._write_json(self.doc_dir(rel) / "revisions.json", revs)
            if entry["kind"] == "external":
                self.log_activity({"time": entry["time"], "user": entry["user"], "path": rel,
                                   "action": "external", "rev": entry["rev"], "count": len(entry["changes"])})
            return revs

    def revisions(self, rel: str) -> list:
        return self.sync(rel)

    def revision_file(self, rel: str, rev: int) -> Path:
        for r in self._read_revisions(rel):
            if r["rev"] == rev:
                return self.doc_dir(rel) / r["file"]
        raise KeyError(f"Revision {rev} not found")

    # ----------------------------------------------------------------- reading
    def load(self, rel: str, rev: int | None = None) -> dict:
        revs = self.sync(rel)
        f = self.resolve(rel) if rev is None else self.revision_file(rel, rev)
        st = f.stat()
        model = excel_reader.read_workbook(str(f), cache_key=(str(f), st.st_mtime, st.st_size))
        latest = revs[-1]
        meta = self._read_meta(rel)
        return {
            **model,
            "path": rel,
            "name": Path(rel).stem,
            "file": Path(rel).name,
            "rev": latest["rev"],
            "viewingRev": rev,
            "lastUser": latest["user"],
            "lastTime": latest["time"],
            "status": meta.get("status", "Draft"),
            "revisions": len(revs),
        }

    # ----------------------------------------------------------------- writing
    def _typed_edits(self, f: Path, edits: dict):
        """Validate + coerce {sheet: {"r,c": text}} using the original cells."""
        wb = load_workbook(f, data_only=False)
        typed, changes = {}, {}
        try:
            for sheet, cells in (edits or {}).items():
                if sheet not in wb.sheetnames:
                    raise KeyError(f"Unknown sheet '{sheet}'")
                ws = wb[sheet]
                for key, text in cells.items():
                    r, c = (int(x) for x in key.split(","))
                    if r < 1 or c < 1:
                        continue
                    cell = ws._cells.get((r, c))
                    orig = cell.value if cell is not None else None
                    fmt = cell.number_format if cell is not None else "General"
                    old_text = excel_reader.edit_text(orig, fmt)
                    new_text = "" if text is None else str(text)
                    if new_text == old_text:
                        continue
                    typed.setdefault(sheet, {})[(r, c)] = excel_writer.coerce(new_text, orig, fmt)
                    changes.setdefault(sheet, []).append((r, c, old_text, new_text))
        finally:
            wb.close()
        flat = [{"sheet": s, "cell": f"{excel_reader.get_column_letter(c)}{r}", "r": r, "c": c,
                 "old": o, "new": n} for s, lst in changes.items() for (r, c, o, n) in lst]
        return typed, flat

    def render_with_edits(self, rel: str, edits: dict) -> bytes:
        f = self.resolve(rel)
        typed, _ = self._typed_edits(f, edits)
        return excel_writer.apply_edits(f.read_bytes(), typed)

    def save(self, rel: str, edits: dict, user: str, note: str, base_rev: int | None) -> dict:
        with _lock:
            revs = self.sync(rel)
            latest = revs[-1]
            if base_rev is not None and base_rev != latest["rev"]:
                raise Conflict(latest)
            f = self.resolve(rel)
            typed, changes = self._typed_edits(f, edits)
            if not changes:
                return {"saved": False, "rev": latest["rev"], "changes": []}
            data = excel_writer.apply_edits(f.read_bytes(), typed)
            tmp = f.with_name(f".{f.name}.dochub.tmp")
            tmp.write_bytes(data)
            try:
                os.replace(tmp, f)
            except PermissionError as exc:
                tmp.unlink(missing_ok=True)
                raise FileLocked("The Excel file is open/locked on the server. Close it in Excel and save again.") from exc
            st = f.stat()
            rev = latest["rev"] + 1
            entry = {
                "rev": rev, "user": user or "Unknown", "time": now_iso(), "kind": "edit",
                "note": (note or "").strip(), "changes": changes,
                "file": self._snapshot(rel, rev, f), "sha": sha256(f),
                "mtime": st.st_mtime, "size": st.st_size,
            }
            revs.append(entry)
            self._write_json(self.doc_dir(rel) / "revisions.json", revs)
            self.log_activity({"time": entry["time"], "user": entry["user"], "path": rel, "action": "edit",
                               "rev": rev, "count": len(changes), "note": entry["note"]})
            return {"saved": True, "rev": rev, "changes": changes}

    def restore(self, rel: str, rev: int, user: str) -> dict:
        with _lock:
            revs = self.sync(rel)
            src = self.revision_file(rel, rev)
            f = self.resolve(rel)
            changes = diff_files(f, src)
            tmp = f.with_name(f".{f.name}.dochub.tmp")
            shutil.copyfile(src, tmp)
            try:
                os.replace(tmp, f)
            except PermissionError as exc:
                tmp.unlink(missing_ok=True)
                raise FileLocked("The Excel file is open/locked on the server.") from exc
            st = f.stat()
            new_rev = revs[-1]["rev"] + 1
            entry = {
                "rev": new_rev, "user": user or "Unknown", "time": now_iso(), "kind": "restore",
                "note": f"Restored revision {rev}", "changes": changes,
                "file": self._snapshot(rel, new_rev, f), "sha": sha256(f),
                "mtime": st.st_mtime, "size": st.st_size,
            }
            revs.append(entry)
            self._write_json(self.doc_dir(rel) / "revisions.json", revs)
            self.log_activity({"time": entry["time"], "user": entry["user"], "path": rel, "action": "restore",
                               "rev": new_rev, "count": len(changes), "note": entry["note"]})
            return {"rev": new_rev}

    def set_status(self, rel: str, status: str, user: str):
        if status not in STATUSES:
            raise ValueError("Unknown status")
        self.resolve(rel)
        meta = self._read_meta(rel)
        old = meta.get("status", "Draft")
        if old == status:
            return
        meta["status"] = status
        self._write_json(self.doc_dir(rel) / "meta.json", meta)
        self.log_activity({"time": now_iso(), "user": user or "Unknown", "path": rel, "action": "status",
                           "note": f"{old} → {status}"})

    # --------------------------------------------------------------- folders
    def make_folder(self, parent: str, name: str, user: str) -> str:
        name = (name or "").strip()
        if not name or any(ch in name for ch in '<>:"/\\|?*') or name.startswith("."):
            raise ValueError("Invalid folder name")
        p = self.resolve(parent) / name
        depth = len(Path(self.rel(p)).parts)
        if depth > 3:
            raise ValueError("Folders are limited to Model / Milestone / Variant")
        p.mkdir(parents=False, exist_ok=True)
        self.log_activity({"time": now_iso(), "user": user or "Unknown", "path": self.rel(p), "action": "folder"})
        return self.rel(p)

    def add_document(self, folder: str, filename: str, data: bytes, user: str) -> str:
        filename = Path(filename).name
        if not filename.lower().endswith(DOC_EXTS):
            raise ValueError("Only .xlsx / .xlsm files are supported")
        d = self.resolve(folder)
        if len(Path(self.rel(d)).parts) != 3:
            raise ValueError("Documents must be placed inside a Variant folder")
        target = d / filename
        if target.exists():
            raise FileExistsError(f"'{filename}' already exists in this variant")
        load_workbook(io_bytes(data)).close()  # validate it is a real workbook
        target.write_bytes(data)
        rel = self.rel(target)
        self.log_activity({"time": now_iso(), "user": user or "Unknown", "path": rel, "action": "upload"})
        self.sync(rel)
        return rel

    def copy_document(self, rel: str, folder: str, new_name: str | None, user: str) -> str:
        src = self.resolve(rel)
        name = (new_name or src.stem).strip() + src.suffix
        return self.add_document(folder, name, src.read_bytes(), user)


def io_bytes(data: bytes):
    import io
    return io.BytesIO(data)


def diff_files(old: Path, new: Path) -> list:
    a = excel_reader.cell_values(str(old))
    b = excel_reader.cell_values(str(new))
    out = []
    for sheet in list(dict.fromkeys(list(a) + list(b))):
        va, vb = a.get(sheet, {}), b.get(sheet, {})
        keys = set(va) | set(vb)
        for key in sorted(keys, key=lambda k: tuple(int(x) for x in k.split(","))):
            if va.get(key, "") != vb.get(key, ""):
                r, c = (int(x) for x in key.split(","))
                out.append({"sheet": sheet, "cell": f"{excel_reader.get_column_letter(c)}{r}", "r": r, "c": c,
                            "old": va.get(key, ""), "new": vb.get(key, "")})
    return out
