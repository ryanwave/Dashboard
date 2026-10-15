"""Write cell edits back into an .xlsx by patching the sheet XML in place.

Unlike re-saving through openpyxl, this keeps everything else in the file
untouched: logos, signatures, charts, macros, conditional formats, etc.
Only the edited <c> elements (plus calc settings) are rewritten.
"""
from __future__ import annotations

import datetime as dt
import html
import io
import posixpath
import re
import xml.etree.ElementTree as ET
import zipfile

from openpyxl.formula.translate import Translator
from openpyxl.utils import get_column_letter, range_boundaries
from openpyxl.utils.datetime import to_excel

NS = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
REL_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PKG_REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
CT_NS = "http://schemas.openxmlformats.org/package/2006/content-types"
XML_SPACE = "{http://www.w3.org/XML/1998/namespace}space"


def q(tag: str) -> str:
    return f"{{{NS}}}{tag}"


_ILLEGAL = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")
_REF = re.compile(r"([A-Z]+)(\d+)")


class EditError(ValueError):
    pass


class Formula(str):
    """Marker type: text that should be written as a formula."""


def col_index(letters: str) -> int:
    n = 0
    for ch in letters:
        n = n * 26 + (ord(ch) - 64)
    return n


# --------------------------------------------------------------------------
# Text -> typed value, mirroring how Excel interprets typed input
# --------------------------------------------------------------------------
_NUM = re.compile(r"^[+-]?(\d{1,3}(,\d{3})+|\d+)?(\.\d+)?([eE][+-]?\d+)?$")
_DATE_PATTERNS = ["%d-%m-%Y", "%d/%m/%Y", "%Y-%m-%d", "%d-%m-%y", "%d/%m/%y", "%d-%b-%Y", "%d %b %Y"]


def parse_number(text: str):
    t = text.strip()
    if not t or not _NUM.match(t) or t in ("+", "-", "."):
        return None
    try:
        num = float(t.replace(",", ""))
    except ValueError:
        return None
    return int(num) if num.is_integer() and "." not in t and "e" not in t.lower() and abs(num) < 1e15 else num


def coerce(text, original, number_format: str | None):
    """Turn user text into the value to store, based on the original cell."""
    if text is None:
        return None
    text = str(text)
    if text.strip() == "":
        return None
    if text.startswith("="):
        return Formula(text)
    if isinstance(original, str) or (number_format == "@"):
        return text
    stripped = text.strip()
    if isinstance(original, (dt.date, dt.datetime)):
        for pat in _DATE_PATTERNS:
            try:
                return dt.datetime.strptime(stripped, pat)
            except ValueError:
                pass
    if stripped.endswith("%"):
        num = parse_number(stripped[:-1])
        if num is not None:
            return num / 100
    if stripped.startswith("0") and len(stripped) > 1 and stripped[1].isdigit():
        return text  # keep leading zeros like an ID
    num = parse_number(stripped)
    if num is not None:
        return num
    if stripped.upper() in ("TRUE", "FALSE") and isinstance(original, bool):
        return stripped.upper() == "TRUE"
    return text


# --------------------------------------------------------------------------
# Package helpers
#
# Only Python's standard library is used here (no lxml): some corporate PCs
# block compiled add-on DLLs. Reading uses xml.etree; writing edits the XML
# *text* of the affected cells only, so every other byte of the file — and
# every namespace prefix Excel relies on — stays exactly as it was.
# --------------------------------------------------------------------------
def _xml(data: bytes):
    return ET.fromstring(data)


def _sheet_paths(zf: zipfile.ZipFile) -> dict:
    wb = _xml(zf.read("xl/workbook.xml"))
    rels = _xml(zf.read("xl/_rels/workbook.xml.rels"))
    targets = {r.get("Id"): r.get("Target") for r in rels}
    out = {}
    sheets = wb.find(q("sheets"))
    if sheets is None:
        raise EditError("This workbook uses the 'Strict Open XML' format. Open it in Excel and "
                        "Save As → Excel Workbook (*.xlsx), then edit it here.")
    for sh in sheets:
        rid = sh.get(f"{{{REL_NS}}}id")
        target = targets.get(rid)
        if not target:
            continue
        path = target.lstrip("/") if target.startswith("/") else posixpath.normpath(posixpath.join("xl", target))
        out[sh.get("name")] = path
    return out


def _esc(text: str) -> str:
    text = _ILLEGAL.sub("", str(text))
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _decode(xml: bytes):
    if xml[:2] in (b"\xff\xfe", b"\xfe\xff"):
        return xml.decode("utf-16"), "utf-16"
    return xml.decode("utf-8-sig" if xml[:3] == b"\xef\xbb\xbf" else "utf-8"), "utf-8"


def _attr(attrs: str, name: str):
    m = re.search(r'(?:^|\s)' + re.escape(name) + r'\s*=\s*(["\'])(.*?)\1', attrs, re.S)
    return html.unescape(m.group(2)) if m else None


def _without_attr(attrs: str, name: str) -> str:
    return re.sub(r'\s+' + re.escape(name) + r'\s*=\s*(["\']).*?\1', "", attrs, flags=re.S)


def _in_ref(ref: str, r: int, c: int) -> bool:
    try:
        min_c, min_r, max_c, max_r = range_boundaries(ref)
    except Exception:
        return False
    return min_r <= r <= max_r and min_c <= c <= max_c


def _cell_xml(p: str, ref: str, style, value) -> str:
    s = f' s="{style}"' if style else ""
    if value is None:
        return f'<{p}c r="{ref}"{s}/>'
    if isinstance(value, Formula):
        return f'<{p}c r="{ref}"{s}><{p}f>{_esc(value[1:])}</{p}f></{p}c>'
    if isinstance(value, bool):
        return f'<{p}c r="{ref}"{s} t="b"><{p}v>{1 if value else 0}</{p}v></{p}c>'
    if isinstance(value, (int, float)):
        return f'<{p}c r="{ref}"{s}><{p}v>{repr(value) if isinstance(value, float) else value}</{p}v></{p}c>'
    if isinstance(value, (dt.datetime, dt.date)):
        return f'<{p}c r="{ref}"{s}><{p}v>{repr(float(to_excel(value)))}</{p}v></{p}c>'
    return (f'<{p}c r="{ref}"{s} t="inlineStr"><{p}is><{p}t xml:space="preserve">{_esc(value)}'
            f'</{p}t></{p}is></{p}c>')


def _patch_sheet(xml: bytes, edits: dict) -> bytes:
    """edits: {(row, col): value} -> patched sheet XML (bytes)."""
    text, enc = _decode(xml)
    m = re.search(r'<(?:([A-Za-z_][\w.\-]*):)?sheetData\b([^>]*?)(/?)>', text)
    if not m:
        raise EditError("The sheet has no cell data section and cannot be edited here.")
    p = m.group(1) + ":" if m.group(1) else ""
    if m.group(3) == "/":  # <sheetData/> — an empty sheet
        text = text[:m.start()] + f"<{p}sheetData{m.group(2)}></{p}sheetData>" + text[m.end():]
        m = re.search(r'<(?:[A-Za-z_][\w.\-]*:)?sheetData\b[^>]*>', text)
    body_start = m.end()
    body_end = text.index(f"</{p}sheetData>", body_start)
    body = text[body_start:body_end]

    pe = re.escape(p)
    row_re = re.compile(r'<' + pe + r'row\b([^>]*?)(/>|>(.*?)</' + pe + r'row>)', re.S)
    cell_re = re.compile(r'<' + pe + r'c\b([^>]*?)(/>|>(.*?)</' + pe + r'c>)', re.S)
    f_re = re.compile(r'<' + pe + r'f\b([^>]*?)(/>|>(.*?)</' + pe + r'f>)', re.S)

    # -- shared / array formulas -------------------------------------------
    groups, masters = {}, {}
    for cm in cell_re.finditer(body):
        inner = cm.group(3) or ""
        fm = f_re.search(inner)
        if not fm:
            continue
        ref = _attr(cm.group(1), "r") or ""
        rm = _REF.match(ref)
        if not rm:
            continue
        rc = (int(rm.group(2)), col_index(rm.group(1)))
        ft, si = _attr(fm.group(1), "t"), _attr(fm.group(1), "si")
        if ft == "shared" and si is not None:
            groups.setdefault(si, []).append((rc, ref))
            if fm.group(3):
                masters[si] = (rc, ref, html.unescape(fm.group(3)))
        elif ft == "array" and _attr(fm.group(1), "ref"):
            aref = _attr(fm.group(1), "ref")
            for (r, c) in edits:
                if (r, c) != rc and _in_ref(aref, r, c):
                    raise EditError(f"Cell {get_column_letter(c)}{r} is part of an array formula "
                                    f"({aref}) and can only be changed in Excel.")
    # Excel keeps a column of similar formulas as one "shared" formula whose
    # text lives only in the first (master) cell. If that cell is overwritten,
    # the other cells of the group get their own explicit formula.
    new_formula = {}
    for si, (mrc, mref, ftext) in masters.items():
        if mrc not in edits:
            continue
        for rc, ref in groups.get(si, []):
            if rc == mrc or rc in edits:
                continue
            try:
                new_formula[rc] = Translator("=" + ftext, origin=mref).translate_formula(ref)[1:]
            except Exception:
                new_formula[rc] = ftext

    # -- default styles for brand-new cells --------------------------------
    col_styles = {}
    for colm in re.finditer(r'<' + pe + r'col\b([^>]*?)/?>', text[:m.start()]):
        st, lo, hi = _attr(colm.group(1), "style"), _attr(colm.group(1), "min"), _attr(colm.group(1), "max")
        if st and lo and hi:
            for i in range(int(lo), min(int(hi), 16384) + 1):
                col_styles[i] = st

    by_row = {}
    for (r, c), v in edits.items():
        by_row.setdefault(r, {})[c] = v
    for (r, c) in new_formula:
        by_row.setdefault(r, {})

    def patch_row(rnum, attrs, inner):
        cell_edits = by_row.get(rnum, {})
        row_style = _attr(attrs, "s") if _attr(attrs, "customFormat") in ("1", "true") else None
        attrs = _without_attr(attrs, "spans")
        if _attr(attrs, "r") is None:
            attrs = f' r="{rnum}"' + attrs
        out, pos, implicit = [], 0, 0
        pending = sorted(cell_edits)

        def new_cells(upto):
            while pending and pending[0] < upto:
                c = pending.pop(0)
                if cell_edits[c] is not None:
                    out.append(_cell_xml(p, f"{get_column_letter(c)}{rnum}", row_style or col_styles.get(c), cell_edits[c]))

        for cm in cell_re.finditer(inner):
            cattrs = cm.group(1)
            ref = _attr(cattrs, "r")
            rm = _REF.match(ref or "")
            ci = col_index(rm.group(1)) if rm else implicit + 1
            implicit = ci
            out.append(inner[pos:cm.start()])
            pos = cm.end()
            new_cells(ci)
            cell = cm.group(0)
            if not rm:  # give implicit cells an explicit address before inserting others
                cell = f"<{p}c r=\"{get_column_letter(ci)}{rnum}\"" + cell[len(p) + 2:]
            if ci in cell_edits:
                if pending and pending[0] == ci:
                    pending.pop(0)
                cell = _cell_xml(p, f"{get_column_letter(ci)}{rnum}", _attr(cattrs, "s"), cell_edits[ci])
            elif (rnum, ci) in new_formula:
                cell = f_re.sub(lambda _: f"<{p}f>{_esc(new_formula[(rnum, ci)])}</{p}f>", cell, count=1)
            out.append(cell)
        rest = inner[pos:]
        ext = re.search(r'<' + pe + r'extLst\b', rest)
        if ext:
            out.append(rest[:ext.start()])
            new_cells(1 << 30)
            out.append(rest[ext.start():])
        else:
            new_cells(1 << 30)
            out.append(rest)
        return f"<{p}row{attrs}>" + "".join(out) + f"</{p}row>"

    out, pos, implicit = [], 0, 0
    todo = sorted(by_row)
    for rm in row_re.finditer(body):
        rattrs = rm.group(1)
        rnum = int(_attr(rattrs, "r") or implicit + 1)
        implicit = rnum
        while todo and todo[0] < rnum:  # rows that do not exist yet
            r = todo.pop(0)
            if any(v is not None for v in by_row[r].values()):
                out.append(body[pos:rm.start()])
                pos = rm.start()
                out.append(patch_row(r, f' r="{r}"', ""))
        if todo and todo[0] == rnum:
            todo.pop(0)
            out.append(body[pos:rm.start()])
            out.append(patch_row(rnum, rattrs, rm.group(3) or ""))
            pos = rm.end()
    out.append(body[pos:])
    for r in todo:
        if any(v is not None for v in by_row[r].values()):
            out.append(patch_row(r, f' r="{r}"', ""))
    return (text[:body_start] + "".join(out) + text[body_end:]).encode(enc)


_CALC_AFTER = ["oleSize", "customWorkbookViews", "pivotCaches", "smartTagPr", "smartTagTypes",
               "webPublishing", "fileRecoveryPr", "webPublishObjects", "extLst"]


def _patch_workbook(xml: bytes) -> bytes:
    """Ask Excel to recalculate all formulas when the file is next opened."""
    text, enc = _decode(xml)
    pm = re.search(r'<(?:([A-Za-z_][\w.\-]*):)?workbook\b', text)
    p = pm.group(1) + ":" if pm and pm.group(1) else ""
    pe = re.escape(p)
    cm = re.search(r'<' + pe + r'calcPr\b([^>]*?)(/?)>', text)
    if cm:
        attrs = cm.group(1)
        if re.search(r'\sfullCalcOnLoad\s*=', attrs):
            attrs = re.sub(r'(\sfullCalcOnLoad\s*=\s*)(["\']).*?\2', r'\1"1"', attrs)
        else:
            attrs += ' fullCalcOnLoad="1"'
        text = text[:cm.start()] + f"<{p}calcPr{attrs}{cm.group(2)}>" + text[cm.end():]
    else:
        insert = f'<{p}calcPr fullCalcOnLoad="1"/>'
        for tag in _CALC_AFTER:
            am = re.search(r'<' + pe + tag + r'\b', text)
            if am:
                text = text[:am.start()] + insert + text[am.start():]
                break
        else:
            end = text.rindex(f"</{p}workbook>")
            text = text[:end] + insert + text[end:]
    return text.encode(enc)


def _drop_calc_chain(files: dict):
    files.pop("xl/calcChain.xml", None)
    ct, enc = _decode(files["[Content_Types].xml"])
    ct = re.sub(r'<(?:[\w.\-]+:)?Override\b[^>]*PartName\s*=\s*"/xl/calcChain\.xml"[^>]*/>', "", ct)
    files["[Content_Types].xml"] = ct.encode(enc)
    rels, enc = _decode(files["xl/_rels/workbook.xml.rels"])
    rels = re.sub(r'<(?:[\w.\-]+:)?Relationship\b[^>]*Type\s*=\s*"[^"]*/calcChain"[^>]*/>', "", rels)
    files["xl/_rels/workbook.xml.rels"] = rels.encode(enc)


_CP = "http://schemas.openxmlformats.org/package/2006/metadata/core-properties"
_DCT = "http://purl.org/dc/terms/"


def _patch_core(xml: bytes, user: str) -> bytes:
    """Record who/when in docProps/core.xml, as Excel does (File → Info)."""
    text, enc = _decode(xml)
    pm = re.search(r'xmlns:([\w.\-]+)\s*=\s*"' + re.escape(_CP) + '"', text)
    cp = pm.group(1) + ":" if pm else ""
    who = f"<{cp}lastModifiedBy>{_esc(user)}</{cp}lastModifiedBy>"
    lm = re.search(r'<' + re.escape(cp) + r'lastModifiedBy\b[^>]*?(/>|>.*?</' + re.escape(cp) + r'lastModifiedBy>)', text, re.S)
    if lm:
        text = text[:lm.start()] + who + text[lm.end():]
    else:
        end = re.search(r'</(?:[\w.\-]+:)?coreProperties>', text)
        if end:
            text = text[:end.start()] + who + text[end.start():]
    dm = re.search(r'xmlns:([\w.\-]+)\s*=\s*"' + re.escape(_DCT) + '"', text)
    if dm:
        d = re.escape(dm.group(1) + ":")
        now = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        text = re.sub(r'(<' + d + r'modified\b[^>]*>).*?(</' + d + r'modified>)', lambda x: x.group(1) + now + x.group(2), text, count=1, flags=re.S)
    return text.encode(enc)


def read_core(zf: zipfile.ZipFile) -> dict:
    """lastModifiedBy / modified / creator from docProps/core.xml (may be empty)."""
    try:
        root = _xml(zf.read("docProps/core.xml"))
    except Exception:
        return {}

    def text(ns, tag):
        el = root.find(f"{{{ns}}}{tag}")
        return (el.text or "").strip() if el is not None and el.text else ""
    return {"lastModifiedBy": text(_CP, "lastModifiedBy"), "modified": text(_DCT, "modified"),
            "creator": text("http://purl.org/dc/elements/1.1/", "creator")}


def apply_edits(src_bytes: bytes, edits: dict, user: str | None = None) -> bytes:
    """edits: {sheet_name: {(row, col): typed value}} -> new xlsx bytes."""
    zin = zipfile.ZipFile(io.BytesIO(src_bytes))
    infos = zin.infolist()
    files = {i.filename: zin.read(i.filename) for i in infos}
    sheet_paths = _sheet_paths(zin)
    changed = False
    for sheet, cell_edits in edits.items():
        if not cell_edits:
            continue
        path = sheet_paths.get(sheet)
        if path is None or path not in files:
            raise KeyError(f"Sheet '{sheet}' not found in workbook")
        files[path] = _patch_sheet(files[path], cell_edits)
        changed = True
    if changed:
        files["xl/workbook.xml"] = _patch_workbook(files["xl/workbook.xml"])
        if "xl/calcChain.xml" in files:
            _drop_calc_chain(files)
        if user and "docProps/core.xml" in files:
            try:
                files["docProps/core.xml"] = _patch_core(files["docProps/core.xml"], user)
            except Exception:
                pass
    out = io.BytesIO()
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zout:
        for info in infos:
            if info.filename not in files:
                continue
            zi = zipfile.ZipInfo(info.filename, date_time=info.date_time)
            zi.compress_type = info.compress_type
            zi.external_attr = info.external_attr
            zout.writestr(zi, files[info.filename])
    return out.getvalue()
