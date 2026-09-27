from __future__ import annotations

import datetime as dt
import io
import os
from collections import Counter
from pathlib import Path
from urllib.parse import quote

from flask import Flask, jsonify, request, send_file, send_from_directory

from .storage import Conflict, FileLocked, Store

STATIC = Path(__file__).resolve().parent.parent / "static"

XLSX_MIME = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"


def create_app(root: str) -> Flask:
    app = Flask(__name__, static_folder=None)
    app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024
    store = Store(root)
    app.store = store

    def err(msg, code=400, **extra):
        return jsonify({"error": msg, **extra}), code

    @app.errorhandler(PermissionError)
    def _perm(e):
        return err(str(e), 403)

    @app.errorhandler(FileNotFoundError)
    def _nf(e):
        return err("Not found", 404)

    @app.errorhandler(FileExistsError)
    def _exists(e):
        return err(str(e), 409)

    @app.errorhandler(ValueError)
    def _val(e):
        return err(str(e), 400)

    @app.errorhandler(KeyError)
    def _key(e):
        return err(str(e).strip("'\""), 404)

    @app.errorhandler(FileLocked)
    def _locked(e):
        return err(str(e), 423)

    # -------------------------------------------------------------- static
    @app.get("/")
    def index():
        return send_from_directory(STATIC, "index.html")

    @app.get("/static/<path:name>")
    def static_files(name):
        resp = send_from_directory(STATIC, name)
        resp.headers["Cache-Control"] = "no-cache"
        return resp

    # ----------------------------------------------------------------- api
    @app.get("/api/tree")
    def tree():
        return jsonify(store.tree())

    @app.get("/api/stats")
    def stats():
        t = store.tree()
        docs = [d for m in t["models"] for ms in m["milestones"] for v in ms["variants"] for d in v["documents"]]
        activity = store.activity()
        today = dt.date.today()
        days = [today - dt.timedelta(days=i) for i in range(13, -1, -1)]
        per_day = Counter()
        cells_changed = 0
        users = Counter()
        for a in activity:
            try:
                d = dt.datetime.fromisoformat(a["time"]).date()
            except (KeyError, ValueError):
                continue
            if a.get("action") in ("edit", "restore", "external"):
                cells_changed += a.get("count", 0)
            if (today - d).days < 14:
                per_day[d] += 1
            if a.get("user") and a.get("user") not in ("System", "Outside DocHub"):
                users[a["user"]] += 1
        return jsonify({
            "models": len(t["models"]),
            "milestones": sum(len(m["milestones"]) for m in t["models"]),
            "variants": sum(len(ms["variants"]) for m in t["models"] for ms in m["milestones"]),
            "documents": len(docs),
            "revisions": sum(max(0, d["revisions"] - 1) for d in docs),
            "cellsChanged": cells_changed,
            "contributors": len(users),
            "topContributors": users.most_common(5),
            "byStatus": Counter(d["status"] for d in docs),
            "daily": [{"date": d.isoformat(), "count": per_day.get(d, 0)} for d in days],
            "activity": activity[:25],
            "recentDocs": sorted(docs, key=lambda d: d["modified"], reverse=True)[:6],
            "root": t["root"],
        })

    @app.get("/api/document")
    def document():
        path = request.args["path"]
        rev = request.args.get("rev", type=int)
        return jsonify(store.load(path, rev))

    @app.get("/api/history")
    def history():
        revs = store.revisions(request.args["path"])
        return jsonify([{k: v for k, v in r.items() if k not in ("sha", "mtime")} for r in reversed(revs)])

    @app.post("/api/save")
    def save():
        body = request.get_json(force=True)
        try:
            result = store.save(body["path"], body.get("edits") or {}, body.get("user"),
                                body.get("note"), body.get("baseRev"))
        except Conflict as c:
            return err(f"{c.latest['user']} saved revision {c.latest['rev']} while you were editing. "
                       "Reload to see their changes — your edits are kept in this browser.",
                       409, latest={k: c.latest.get(k) for k in ("rev", "user", "time", "note")})
        return jsonify(result)

    @app.post("/api/restore")
    def restore():
        body = request.get_json(force=True)
        return jsonify(store.restore(body["path"], int(body["rev"]), body.get("user")))

    @app.post("/api/status")
    def status():
        body = request.get_json(force=True)
        store.set_status(body["path"], body["status"], body.get("user"))
        return jsonify({"ok": True})

    def _download(data: bytes, filename: str):
        resp = send_file(io.BytesIO(data), mimetype=XLSX_MIME, as_attachment=True, download_name=filename)
        resp.headers["Content-Disposition"] = f"attachment; filename*=UTF-8''{quote(filename)}"
        return resp

    @app.get("/api/export")
    def export_get():
        path = request.args["path"]
        rev = request.args.get("rev", type=int)
        store.sync(path)
        f = store.resolve(path) if rev is None else store.revision_file(path, rev)
        stem = Path(path).stem + (f"_rev{rev}" if rev is not None else "")
        return _download(f.read_bytes(), stem + Path(path).suffix)

    @app.post("/api/export")
    def export_post():
        body = request.get_json(force=True)
        path = body["path"]
        data = store.render_with_edits(path, body.get("edits") or {})
        return _download(data, Path(path).stem + Path(path).suffix)

    @app.post("/api/folder")
    def folder():
        body = request.get_json(force=True)
        return jsonify({"path": store.make_folder(body.get("parent", ""), body["name"], body.get("user"))})

    @app.post("/api/upload")
    def upload():
        f = request.files.get("file")
        if f is None:
            return err("No file uploaded")
        rel = store.add_document(request.form["folder"], f.filename, f.read(), request.form.get("user"))
        return jsonify({"path": rel})

    @app.post("/api/copy")
    def copy():
        body = request.get_json(force=True)
        rel = store.copy_document(body["path"], body["folder"], body.get("name"), body.get("user"))
        return jsonify({"path": rel})

    return app


def default_root() -> str:
    env = os.environ.get("DOCHUB_ROOT")
    if env:
        return env
    if os.name == "nt":
        return r"C:\Dashboard"
    return str(Path(__file__).resolve().parent.parent / "sample_data" / "Dashboard")
