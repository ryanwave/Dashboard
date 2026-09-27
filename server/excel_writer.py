"""Write cell edits back into an .xlsx by patching the sheet XML in place.

Unlike re-saving through openpyxl, this keeps everything else in the file
untouched: logos, signatures, charts, macros, conditional formats, etc.
Only the edited <c> elements (plus calc settings) are rewritten.
"""
from __future__ import annotations

import datetime as dt
import io
import posixpath
import re
import zipfile

from lxml import etree
from openpyxl.utils import get_column_letter
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
# --------------------------------------------------------------------------
def _sheet_paths(zf: zipfile.ZipFile) -> dict:
    wb = etree.fromstring(zf.read("xl/workbook.xml"))
    rels = etree.fromstring(zf.read("xl/_rels/workbook.xml.rels"))
    targets = {r.get("Id"): r.get("Target") for r in rels}
    out = {}
    for sh in wb.find(q("sheets")):
        rid = sh.get(f"{{{REL_NS}}}id")
        target = targets.get(rid)
        if not target:
            continue
        path = target.lstrip("/") if target.startswith("/") else posixpath.normpath(posixpath.join("xl", target))
        out[sh.get("name")] = path
    return out


def _set_value(c, value):
    for child in list(c):
        if etree.QName(child).localname in ("f", "v", "is"):
            c.remove(child)
    c.attrib.pop("t", None)
    ext = [ch for ch in c if etree.QName(ch).localname == "extLst"]
    for e in ext:
        c.remove(e)
    if value is None:
        pass
    elif isinstance(value, Formula):
        f = etree.SubElement(c, q("f"))
        f.text = _ILLEGAL.sub("", value[1:])
    elif isinstance(value, bool):
        c.set("t", "b")
        etree.SubElement(c, q("v")).text = "1" if value else "0"
    elif isinstance(value, (int, float)):
        etree.SubElement(c, q("v")).text = repr(value) if isinstance(value, float) else str(value)
    elif isinstance(value, (dt.datetime, dt.date)):
        etree.SubElement(c, q("v")).text = repr(float(to_excel(value)))
    else:
        c.set("t", "inlineStr")
        is_ = etree.SubElement(c, q("is"))
        t = etree.SubElement(is_, q("t"))
        t.text = _ILLEGAL.sub("", str(value))
        t.set(XML_SPACE, "preserve")
    for e in ext:
        c.append(e)


def _patch_sheet(xml: bytes, edits: dict) -> bytes:
    """edits: {(row, col): value}"""
    root = etree.fromstring(xml)
    sheet_data = root.find(q("sheetData"))
    col_styles = {}
    cols = root.find(q("cols"))
    if cols is not None:
        for col in cols:
            if col.get("style"):
                for i in range(int(col.get("min")), int(col.get("max")) + 1):
                    col_styles[i] = col.get("style")

    rows = {}
    implicit = 0
    for row in sheet_data.findall(q("row")):
        idx = int(row.get("r")) if row.get("r") else implicit + 1
        row.set("r", str(idx))
        implicit = idx
        rows[idx] = row

    for (r, c), value in sorted(edits.items()):
        row = rows.get(r)
        if row is None:
            row = etree.Element(q("row"))
            row.set("r", str(r))
            later = [k for k in rows if k > r]
            if later:
                rows[min(later)].addprevious(row)
            else:
                sheet_data.append(row)
            rows[r] = row
        row.attrib.pop("spans", None)
        ref = f"{get_column_letter(c)}{r}"
        target, before = None, None
        implicit_c = 0
        for cell in row.findall(q("c")):
            if cell.get("r"):
                m = _REF.match(cell.get("r"))
                ci = col_index(m.group(1)) if m else implicit_c + 1
            else:
                ci = implicit_c + 1
                cell.set("r", f"{get_column_letter(ci)}{r}")
            implicit_c = ci
            if ci == c:
                target = cell
                break
            if ci > c:
                before = cell
                break
        if target is None:
            if value is None:
                continue
            target = etree.Element(q("c"))
            target.set("r", ref)
            style = row.get("s") if row.get("customFormat") in ("1", "true") else col_styles.get(c)
            if style:
                target.set("s", style)
            if before is not None:
                before.addprevious(target)
            else:
                ext = row.find(q("extLst"))
                if ext is not None:
                    ext.addprevious(target)
                else:
                    row.append(target)
        _set_value(target, value)
    return etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone=True)


_CALC_AFTER = ["oleSize", "customWorkbookViews", "pivotCaches", "smartTagPr", "smartTagTypes",
               "webPublishing", "fileRecoveryPr", "webPublishObjects", "extLst"]


def _patch_workbook(xml: bytes) -> bytes:
    root = etree.fromstring(xml)
    calc = root.find(q("calcPr"))
    if calc is None:
        calc = etree.Element(q("calcPr"))
        anchor = next((root.find(q(t)) for t in _CALC_AFTER if root.find(q(t)) is not None), None)
        if anchor is not None:
            anchor.addprevious(calc)
        else:
            root.append(calc)
    calc.set("fullCalcOnLoad", "1")
    return etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone=True)


def _drop_calc_chain(files: dict):
    files.pop("xl/calcChain.xml", None)
    ct = etree.fromstring(files["[Content_Types].xml"])
    for o in list(ct):
        if o.get("PartName") == "/xl/calcChain.xml":
            ct.remove(o)
    files["[Content_Types].xml"] = etree.tostring(ct, xml_declaration=True, encoding="UTF-8", standalone=True)
    rels = etree.fromstring(files["xl/_rels/workbook.xml.rels"])
    for r in list(rels):
        if (r.get("Type") or "").endswith("/calcChain"):
            rels.remove(r)
    files["xl/_rels/workbook.xml.rels"] = etree.tostring(rels, xml_declaration=True, encoding="UTF-8", standalone=True)


def apply_edits(src_bytes: bytes, edits: dict) -> bytes:
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
