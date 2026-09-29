"""Convert an .xlsx workbook into a JSON render model for the web grid.

The model keeps everything needed to draw the sheet the way Excel does:
column widths, row heights, merged ranges, fills (incl. theme colours and
tints), fonts, borders, alignment / text rotation, rich text, images,
comments and list-type data validations (rendered as dropdowns).
"""
from __future__ import annotations

import base64
import colorsys
import datetime as dt
import html
import re
import threading
import zipfile
from collections import OrderedDict

from lxml import etree
from openpyxl import load_workbook
from openpyxl.cell.rich_text import CellRichText, TextBlock
from openpyxl.styles.colors import COLOR_INDEX
from openpyxl.styles.numbers import is_date_format
from openpyxl.utils import get_column_letter, range_boundaries
from openpyxl.utils.datetime import from_excel

MAX_ROWS = 2500
MAX_COLS = 120
DEFAULT_COL_WIDTH = 8.43  # Excel characters
DEFAULT_ROW_HEIGHT = 15.0  # points

_A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
# Office 2013+ default theme, in Excel's theme-index order.
DEFAULT_THEME = [
    "FFFFFF", "000000", "E7E6E6", "44546A", "4472C4", "ED7D31",
    "A5A5A5", "FFC000", "5B9BD5", "70AD47", "0563C1", "954F72",
]


# --------------------------------------------------------------------------
# Colours
# --------------------------------------------------------------------------
def parse_theme(xml_bytes) -> list[str]:
    if not xml_bytes:
        return list(DEFAULT_THEME)
    try:
        root = etree.fromstring(xml_bytes)
        scheme = root.find(f".//{_A}clrScheme")
        found = {}
        for child in scheme:
            name = etree.QName(child).localname
            if not len(child):
                continue
            el = child[0]
            kind = etree.QName(el).localname
            if kind == "srgbClr":
                found[name] = el.get("val")
            elif kind == "sysClr":
                found[name] = el.get("lastClr") or ("000000" if "Text" in el.get("val", "") else "FFFFFF")
        order = ["lt1", "dk1", "lt2", "dk2", "accent1", "accent2", "accent3",
                 "accent4", "accent5", "accent6", "hlink", "folHlink"]
        return [found.get(k, DEFAULT_THEME[i]).upper() for i, k in enumerate(order)]
    except Exception:  # malformed theme -> fall back silently
        return list(DEFAULT_THEME)


def apply_tint(hex6: str, tint: float) -> str:
    if not tint:
        return hex6
    r, g, b = (int(hex6[i:i + 2], 16) / 255 for i in (0, 2, 4))
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    l = l * (1 + tint) if tint < 0 else l * (1 - tint) + tint
    r, g, b = colorsys.hls_to_rgb(h, max(0, min(1, l)), s)
    return "".join(f"{round(x * 255):02X}" for x in (r, g, b))


def resolve_color(color, theme: list[str]) -> str | None:
    """openpyxl Color -> '#RRGGBB' or None."""
    if color is None:
        return None
    try:
        ctype = color.type
        tint = color.tint or 0
        if ctype == "rgb":
            val = color.rgb
            if not isinstance(val, str) or len(val) < 6:
                return None
            return "#" + apply_tint(val[-6:].upper(), tint)
        if ctype == "theme":
            idx = color.theme
            if idx is None or idx >= len(theme):
                return None
            return "#" + apply_tint(theme[idx], tint)
        if ctype == "indexed":
            idx = color.indexed
            if idx == 64:
                return "#000000"
            if idx == 65:
                return "#FFFFFF"
            if idx is not None and 0 <= idx < len(COLOR_INDEX):
                return "#" + apply_tint(COLOR_INDEX[idx][-6:], tint)
    except Exception:
        pass
    return None


# --------------------------------------------------------------------------
# Number / date formatting (a pragmatic subset of Excel's rules)
# --------------------------------------------------------------------------
def _general(v) -> str:
    if isinstance(v, bool):
        return "TRUE" if v else "FALSE"
    if isinstance(v, int):
        return str(v)
    if isinstance(v, float):
        if v.is_integer() and abs(v) < 1e15:
            return str(int(v))
        s = f"{v:.10g}"
        if "e" in s:
            s = f"{v:.5E}"
        return s
    return str(v)


def _strip_literals(s: str) -> str:
    s = re.sub(r'"([^"]*)"', r"\1", s)
    s = re.sub(r"\\(.)", r"\1", s)
    s = re.sub(r"_.", " ", s)
    s = re.sub(r"\*.", "", s)
    return s


def format_number(v, fmt: str) -> str:
    if fmt in (None, "", "General", "@"):
        return _general(v)
    sections = fmt.split(";")
    sec = sections[0]
    negative = v < 0
    if negative and len(sections) > 1 and sections[1]:
        sec = sections[1]
        v = -v
    elif v == 0 and len(sections) > 2 and sections[2]:
        sec = sections[2]
    sec = re.sub(r"\[[^\]]*\]", "", sec)
    if sec.strip().lower() == "general":
        return _general(v)
    token = re.search(r"[#0?][#0?,]*(\.[#0?]+)?(E[+-]0+)?|\.[#0?]+", sec)
    if not token:
        return _strip_literals(sec) or _general(v)
    tok = token.group(0)
    pct = "%" in sec
    if pct:
        v = v * 100
    dec = len(re.sub(r"[^#0?]", "", tok.split(".", 1)[1])) if "." in tok else 0
    if "E" in tok:
        body = f"{v:.{dec}E}"
    else:
        grouping = "," in tok.split(".")[0]
        body = f"{v:{',' if grouping else ''}.{dec}f}"
    prefix = _strip_literals(sec[: token.start()])
    suffix = _strip_literals(sec[token.end():])
    return f"{prefix}{body}{suffix}"


_DATE_TOKENS = re.compile(r"yyyy|yy|mmmmm|mmmm|mmm|mm|m|dddd|ddd|dd|d|hh|h|ss|s|am/pm|a/p", re.I)


def format_date(v, fmt: str) -> str:
    fmt = re.sub(r"\[[^\]]*\]", "", fmt or "")
    fmt = _strip_literals(fmt.split(";")[0])
    if not re.search(r"[dmyhs]", fmt, re.I):
        fmt = "dd-mm-yyyy" if not isinstance(v, dt.time) else "hh:mm"
    if isinstance(v, dt.time):
        v = dt.datetime.combine(dt.date(1900, 1, 1), v)
    elif isinstance(v, dt.date) and not isinstance(v, dt.datetime):
        v = dt.datetime.combine(v, dt.time())
    has_ampm = bool(re.search(r"am/pm|a/p", fmt, re.I))
    tokens = list(_DATE_TOKENS.finditer(fmt))
    out, pos = [], 0
    for i, m in enumerate(tokens):
        out.append(fmt[pos:m.start()])
        t = m.group(0)
        tl = t.lower()
        prev = tokens[i - 1].group(0).lower() if i else ""
        nxt = tokens[i + 1].group(0).lower() if i + 1 < len(tokens) else ""
        is_minute = tl in ("m", "mm") and (prev.startswith("h") or nxt.startswith("s"))
        if tl == "yyyy":
            out.append(f"{v.year:04d}")
        elif tl == "yy":
            out.append(f"{v.year % 100:02d}")
        elif is_minute:
            out.append(f"{v.minute:02d}" if tl == "mm" else str(v.minute))
        elif tl == "mmmmm":
            out.append(v.strftime("%B")[0])
        elif tl == "mmmm":
            out.append(v.strftime("%B"))
        elif tl == "mmm":
            out.append(v.strftime("%b"))
        elif tl == "mm":
            out.append(f"{v.month:02d}")
        elif tl == "m":
            out.append(str(v.month))
        elif tl == "dddd":
            out.append(v.strftime("%A"))
        elif tl == "ddd":
            out.append(v.strftime("%a"))
        elif tl == "dd":
            out.append(f"{v.day:02d}")
        elif tl == "d":
            out.append(str(v.day))
        elif tl in ("hh", "h"):
            hour = v.hour % 12 or 12 if has_ampm else v.hour
            out.append(f"{hour:02d}" if tl == "hh" else str(hour))
        elif tl in ("ss", "s"):
            out.append(f"{v.second:02d}" if tl == "ss" else str(v.second))
        elif tl == "am/pm":
            out.append("AM" if v.hour < 12 else "PM")
        elif tl == "a/p":
            out.append("A" if v.hour < 12 else "P")
        pos = m.end()
    out.append(fmt[pos:])
    return "".join(out)


def display_value(v, fmt: str) -> str:
    if v is None:
        return ""
    if isinstance(v, CellRichText):
        return str(v)
    if isinstance(v, (dt.datetime, dt.date, dt.time)):
        return format_date(v, fmt)
    if isinstance(v, bool):
        return "TRUE" if v else "FALSE"
    if isinstance(v, (int, float)):
        try:
            return format_number(v, fmt)
        except Exception:
            return _general(v)
    return str(v)


def edit_text(v, fmt: str) -> str:
    """What the user sees in the edit box (like Excel's formula bar)."""
    if v is None:
        return ""
    if isinstance(v, (int, float)) and not isinstance(v, bool):
        if fmt and "%" in fmt:
            return _general(round(v * 100, 10)) + "%"
        return _general(v)
    return display_value(v, fmt)


# --------------------------------------------------------------------------
# Styles
# --------------------------------------------------------------------------
_BORDER = {
    "hair": "1px solid", "thin": "1px solid", "dotted": "1px dotted",
    "dashed": "1px dashed", "dashDot": "1px dashed", "dashDotDot": "1px dotted",
    "medium": "2px solid", "mediumDashed": "2px dashed",
    "mediumDashDot": "2px dashed", "mediumDashDotDot": "2px dashed",
    "slantDashDot": "2px dashed", "thick": "3px solid", "double": "3px double",
}


def _side_css(side, theme):
    if side is None or not side.style:
        return None
    color = resolve_color(side.color, theme) or "#000000"
    return f"{_BORDER.get(side.style, '1px solid')} {color}"


def _fill_color(fill, theme):
    try:
        if getattr(fill, "fill_type", None) in (None, "none"):
            if getattr(fill, "type", None) == "gradient" or fill.__class__.__name__ == "GradientFill":
                stops = getattr(fill, "stop", None) or []
                return resolve_color(stops[0].color, theme) if stops else None
            return None
        color = resolve_color(fill.fgColor, theme)
        if fill.fill_type == "solid":
            return color
        return color or resolve_color(fill.bgColor, theme)
    except Exception:
        return None


def _font_css(font, theme) -> dict:
    css = {}
    if font is None:
        return css
    if font.name and font.name != "Calibri":
        css["font-family"] = f"'{font.name}', Calibri, Carlito, sans-serif"
    if font.sz and float(font.sz) != 11:
        css["font-size"] = f"{float(font.sz):g}pt"
    if font.b:
        css["font-weight"] = "700"
    if font.i:
        css["font-style"] = "italic"
    deco = []
    if font.u and font.u != "none":
        deco.append("underline")
    if font.strike:
        deco.append("line-through")
    if deco:
        css["text-decoration"] = " ".join(deco)
    color = resolve_color(font.color, theme)
    if color and color.upper() != "#000000":
        css["color"] = color
    return css


def _align_css(al) -> tuple[dict, dict]:
    """Returns (td css, meta) where meta holds wrap/rotation/halign."""
    css, meta = {}, {"wrap": False, "h": None, "rot": 0}
    if al is None:
        return css, meta
    h = al.horizontal
    if h in ("center", "centerContinuous"):
        css["text-align"] = "center"
    elif h == "right":
        css["text-align"] = "right"
    elif h in ("justify", "distributed"):
        css["text-align"] = "justify"
    elif h == "left":
        css["text-align"] = "left"
    meta["h"] = h
    v = al.vertical
    css["vertical-align"] = {"top": "top", "center": "middle", "justify": "middle",
                             "distributed": "middle"}.get(v, "bottom")
    if al.wrap_text or h in ("justify", "distributed") or al.vertical in ("justify", "distributed"):
        meta["wrap"] = True
    if al.indent:
        css["padding-left"] = f"{int(al.indent) * 9 + 3}px"
    meta["rot"] = int(al.textRotation or 0)
    return css, meta


# --------------------------------------------------------------------------
# Rich text
# --------------------------------------------------------------------------
def rich_html(value: CellRichText, theme) -> str:
    parts = []
    for block in value:
        if isinstance(block, TextBlock):
            f = block.font
            css = {}
            if f is not None:
                if f.b:
                    css["font-weight"] = "700"
                if f.i:
                    css["font-style"] = "italic"
                if f.u and f.u != "none":
                    css["text-decoration"] = "underline"
                if f.strike:
                    css["text-decoration"] = "line-through"
                if f.sz:
                    css["font-size"] = f"{float(f.sz):g}pt"
                col = resolve_color(f.color, theme)
                if col:
                    css["color"] = col
                va = getattr(f, "vertAlign", None)
                tag = "sup" if va == "superscript" else "sub" if va == "subscript" else "span"
            else:
                tag = "span"
            style = ";".join(f"{k}:{v}" for k, v in css.items())
            parts.append(f'<{tag} style="{style}">{html.escape(block.text)}</{tag}>')
        else:
            parts.append(html.escape(str(block)))
    return "".join(parts)


# --------------------------------------------------------------------------
# Workbook -> model
# --------------------------------------------------------------------------
def col_width_px(width_chars: float) -> int:
    """Excel column width (as stored in the file) -> screen pixels at 100%.

    Excel's own formula with a 7px maximum digit width (Calibri 11 / Arial 10):
    pixels = trunc(((256 * width + trunc(128 / 7)) / 256) * 7)
    """
    if not width_chars:
        return 0
    return int(((256 * float(width_chars) + 18) / 256) * 7)


def row_height_px(points: float) -> int:
    return int(round(points * 96 / 72))


def _used_range(ws):
    """Rows/cols that actually matter: values, merges and images, plus any
    formatted-only cells close to them (whole-column formatting that runs
    thousands of rows past the data is ignored)."""
    val_r = val_c = 0
    sty_r = sty_c = 0
    for (r, c), cell in ws._cells.items():
        if cell.value is not None:
            if r > val_r:
                val_r = r
            if c > val_c:
                val_c = c
        elif cell.has_style and (r > sty_r or c > sty_c):
            fill = cell.fill
            b = cell.border
            if (fill is not None and fill.fill_type not in (None, "none")) or any(
                    getattr(getattr(b, s, None), "style", None) for s in ("left", "right", "top", "bottom")):
                sty_r, sty_c = max(sty_r, r), max(sty_c, c)
    for mr in ws.merged_cells.ranges:
        val_r, val_c = max(val_r, mr.max_row), max(val_c, mr.max_col)
    for img in getattr(ws, "_images", []):
        try:
            anc = img.anchor
            to = getattr(anc, "to", None) or anc._from
            val_r, val_c = max(val_r, to.row + 1), max(val_c, to.col + 1)
        except Exception:
            pass
    max_r = max(val_r, min(sty_r, val_r + 40))
    max_c = max(val_c, min(sty_c, val_c + 10))
    return max(1, max_r), max(1, max_c)


def _validations(ws, wb) -> dict:
    out = {}
    dv_list = getattr(getattr(ws, "data_validations", None), "dataValidation", []) or []
    for dv in dv_list:
        if dv.type != "list" or not dv.formula1:
            continue
        f = dv.formula1.strip()
        options = None
        if f.startswith('"') and f.endswith('"'):
            options = [o.strip() for o in f[1:-1].split(",")]
        else:
            try:
                ref = f.lstrip("=")
                if "!" in ref:
                    sheet_name, rng = ref.rsplit("!", 1)
                    src = wb[sheet_name.strip("'")]
                else:
                    src, rng = ws, ref
                rng = rng.replace("$", "")
                min_c, min_r, max_c, max_r = range_boundaries(rng)
                options = []
                for row in src.iter_rows(min_row=min_r, max_row=max_r, min_col=min_c, max_col=max_c):
                    for cell in row:
                        if cell.value not in (None, ""):
                            options.append(str(cell.value))
            except Exception:
                options = None
        if not options:
            continue
        for rng in dv.sqref.ranges:
            for r in range(rng.min_row, min(rng.max_row, MAX_ROWS) + 1):
                for c in range(rng.min_col, min(rng.max_col, MAX_COLS) + 1):
                    out[f"{r},{c}"] = options
    return out


def _images(ws) -> list:
    imgs = []
    for img in getattr(ws, "_images", []):
        try:
            data = img._data()
            fmt = (img.format or "png").lower()
            mime = "image/jpeg" if fmt in ("jpg", "jpeg") else f"image/{fmt}"
            anc = img.anchor
            frm = anc._from
            item = {
                "src": f"data:{mime};base64,{base64.b64encode(data).decode()}",
                "r": frm.row + 1, "c": frm.col + 1,
                "dx": round(frm.colOff / 9525), "dy": round(frm.rowOff / 9525),
            }
            to = getattr(anc, "to", None)
            ext = getattr(anc, "ext", None)
            if to is not None:
                item["to"] = {"r": to.row + 1, "c": to.col + 1,
                              "dx": round(to.colOff / 9525), "dy": round(to.rowOff / 9525)}
            elif ext is not None:
                item["w"] = round(ext.width / 9525)
                item["h"] = round(ext.height / 9525)
            else:
                item["w"], item["h"] = img.width, img.height
            imgs.append(item)
        except Exception:
            continue
    return imgs


def sheet_model(ws, cached, wb, theme) -> dict:
    max_r, max_c = _used_range(ws)
    truncated = max_r > MAX_ROWS or max_c > MAX_COLS
    max_r, max_c = min(max_r, MAX_ROWS), min(max_c, MAX_COLS)

    fmt = ws.sheet_format
    # Default: defaultColWidth if stored, else baseColWidth (8) chars + 5px padding = 64px
    default_px = col_width_px(fmt.defaultColWidth) if fmt.defaultColWidth else int((fmt.baseColWidth or 8) * 7 + 5)
    default_h = fmt.defaultRowHeight or DEFAULT_ROW_HEIGHT

    col_widths = [default_px] * (max_c + 1)
    hidden_cols = set()
    for dim in ws.column_dimensions.values():
        lo, hi = dim.min or 0, dim.max or 0
        if not lo:
            continue
        for c in range(lo, min(hi, max_c) + 1):
            if dim.width:
                col_widths[c] = col_width_px(dim.width)
            if dim.hidden:
                hidden_cols.add(c)
    row_heights = [row_height_px(default_h)] * (max_r + 1)
    hidden_rows = set()
    for r, dim in ws.row_dimensions.items():
        if r > max_r:
            continue
        if dim.ht:
            row_heights[r] = row_height_px(dim.ht)
        if dim.hidden:
            hidden_rows.add(r)

    merges = []
    covered = {}
    for mr in ws.merged_cells.ranges:
        if mr.min_row > max_r or mr.min_col > max_c:
            continue
        m = {"r1": mr.min_row, "c1": mr.min_col, "r2": min(mr.max_row, max_r), "c2": min(mr.max_col, max_c)}
        merges.append(m)
        for r in range(m["r1"], m["r2"] + 1):
            for c in range(m["c1"], m["c2"] + 1):
                covered[(r, c)] = m

    def raw_border(r, c):
        cell = ws._cells.get((r, c))
        return cell.border if cell is not None and cell.has_style else None

    def side(r, c, name):
        b = raw_border(r, c)
        return _side_css(getattr(b, name, None), theme) if b else None

    style_index: "OrderedDict[str, int]" = OrderedDict()
    cells = {}
    grid_color_default = None

    for r in range(1, max_r + 1):
        for c in range(1, max_c + 1):
            m = covered.get((r, c))
            if m and (m["r1"], m["c1"]) != (r, c):
                continue
            cell = ws._cells.get((r, c))
            r2, c2 = (m["r2"], m["c2"]) if m else (r, c)
            css = {}
            meta = {"wrap": False, "h": None, "rot": 0}
            fill = None
            if cell is not None and cell.has_style:
                fill = _fill_color(cell.fill, theme)
                if fill:
                    css["background"] = fill
                css.update(_font_css(cell.font, theme))
                a_css, meta = _align_css(cell.alignment)
                css.update(a_css)
            # Normalised borders: each cell draws its right + bottom edge,
            # taking the neighbour's left/top into account (Excel shares edges).
            right = side(r, c2, "right") or (side(r, c2 + 1, "left") if c2 < max_c else None)
            bottom = side(r2, c, "bottom") or (side(r2 + 1, c, "top") if r2 < max_r else None)
            if right:
                css["border-right"] = right
            elif fill:
                css["border-right"] = f"1px solid {fill}"
            if bottom:
                css["border-bottom"] = bottom
            elif fill:
                css["border-bottom"] = f"1px solid {fill}"
            if c == 1 and side(r, c, "left"):
                css["border-left"] = side(r, c, "left")
            if r == 1 and side(r, c, "top"):
                css["border-top"] = side(r, c, "top")

            value = cell.value if cell is not None else None
            number_format = (cell.number_format if cell is not None else None) or "General"
            entry = {}
            formula = _formula_text(value)
            if formula is not None:
                entry["f"] = formula
                value = cached.get((r, c))
                if isinstance(value, (int, float)) and not isinstance(value, bool) and is_date_format(number_format):
                    try:
                        value = from_excel(value)
                    except Exception:
                        pass
            if value is not None:
                try:
                    entry["v"] = display_value(value, number_format)
                    entry["e"] = edit_text(value, number_format)
                    if isinstance(value, CellRichText):
                        entry["h"] = rich_html(value, theme)
                except Exception:
                    entry["v"] = entry["e"] = str(value)
                if isinstance(value, (int, float)) and not isinstance(value, bool):
                    entry["n"] = 1
                    if "text-align" not in css:
                        css["text-align"] = "right"
                elif isinstance(value, (dt.date, dt.datetime, dt.time)):
                    entry["n"] = 1
                    if "text-align" not in css:
                        css["text-align"] = "right"
                elif isinstance(value, bool) and "text-align" not in css:
                    css["text-align"] = "center"
            if cell is not None and cell.comment is not None:
                entry["note"] = cell.comment.text
            if meta["wrap"]:
                entry["w"] = 1
            if meta["rot"]:
                entry["rot"] = meta["rot"]
            if css:
                key = ";".join(f"{k}:{v}" for k, v in css.items())
                if key not in style_index:
                    style_index[key] = len(style_index)
                entry["s"] = style_index[key]
            if entry:
                cells[f"{r},{c}"] = entry

    view = ws.sheet_view
    freeze = None
    if ws.freeze_panes:
        try:
            fc, fr, _, _ = range_boundaries(ws.freeze_panes)
            freeze = {"r": fr - 1, "c": fc - 1}
        except Exception:
            freeze = None

    return {
        "name": ws.title,
        "state": ws.sheet_state,
        "maxRow": max_r,
        "maxCol": max_c,
        "truncated": truncated,
        "colWidths": col_widths,
        "rowHeights": row_heights,
        "customHeights": sorted(r for r, d in ws.row_dimensions.items()
                                if d.ht and d.customHeight and r <= max_r),
        "hiddenRows": sorted(hidden_rows),
        "hiddenCols": sorted(hidden_cols),
        "merges": merges,
        "cells": cells,
        "styles": list(style_index.keys()),
        "images": _images(ws),
        "validations": _validations(ws, wb),
        "gridLines": bool(view.showGridLines) if view.showGridLines is not None else True,
        "zoom": int(view.zoomScale or 100),
        "freeze": freeze,
        "tabColor": resolve_color(ws.sheet_properties.tabColor, theme) if ws.sheet_properties.tabColor else None,
        "colLetters": [""] + [get_column_letter(c) for c in range(1, max_c + 1)],
    }


def _formula_text(value):
    if isinstance(value, str):
        return value if value.startswith("=") and len(value) > 1 else None
    text = getattr(value, "text", None)  # ArrayFormula / DataTableFormula
    if isinstance(text, str):
        return text if text.startswith("=") else "=" + text
    if value.__class__.__name__ == "DataTableFormula":
        return "=TABLE()"
    return None


_SML = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
_REF = re.compile(r"([A-Z]+)(\d+)")


def formula_cache(path: str) -> dict:
    """{sheet: {(row, col): cached value}} for every formula cell."""
    from openpyxl.utils import column_index_from_string
    from .excel_writer import _sheet_paths

    out = {}
    with zipfile.ZipFile(path) as z:
        names = set(z.namelist())
        for sheet, part in _sheet_paths(z).items():
            if part not in names:
                continue
            vals = {}
            with z.open(part) as fh:
                for _, el in etree.iterparse(fh, tag=f"{_SML}c", resolve_entities=False, huge_tree=True):
                    if el.find(f"{_SML}f") is not None:
                        v = el.find(f"{_SML}v")
                        m = _REF.match(el.get("r") or "")
                        if v is not None and v.text is not None and m:
                            t = el.get("t")
                            if t == "b":
                                val = v.text == "1"
                            elif t in ("str", "e", "inlineStr", "s"):
                                val = v.text
                            else:
                                try:
                                    val = float(v.text)
                                    if val.is_integer() and abs(val) < 1e15:
                                        val = int(val)
                                except ValueError:
                                    val = v.text
                            vals[(int(m.group(2)), column_index_from_string(m.group(1)))] = val
                    el.clear()
            out[sheet] = vals
    return out


_cache: "OrderedDict[tuple, dict]" = OrderedDict()
_cache_lock = threading.Lock()


def read_workbook(path: str, cache_key=None) -> dict:
    """Return the render model for every sheet in the workbook at *path*."""
    if cache_key is not None:
        with _cache_lock:
            if cache_key in _cache:
                _cache.move_to_end(cache_key)
                return _cache[cache_key]
    # One parse of the workbook (styles + formulas); the results Excel last
    # calculated for formula cells are read straight from the sheet XML.
    wb = load_workbook(path, data_only=False, rich_text=True)
    try:
        cache = formula_cache(path)
    except Exception:
        cache = {}
    theme = parse_theme(getattr(wb, "loaded_theme", None))
    sheets = []
    for ws in wb.worksheets:
        sheets.append(sheet_model(ws, cache.get(ws.title, {}), wb, theme))
    active = wb.active.title if wb.active is not None else (sheets[0]["name"] if sheets else None)
    model = {"sheets": sheets, "active": active}
    if cache_key is not None:
        with _cache_lock:
            _cache[cache_key] = model
            while len(_cache) > 24:
                _cache.popitem(last=False)
    return model


def cell_values(path: str) -> dict:
    """{sheet: {"r,c": edit_text}} — used for diffs between revisions."""
    wb = load_workbook(path, data_only=False, read_only=True)
    out = {}
    try:
        for ws in wb.worksheets:
            vals = {}
            for row in ws.iter_rows():
                for cell in row:
                    if cell.value is None or not hasattr(cell, "column"):
                        continue
                    vals[f"{cell.row},{cell.column}"] = edit_text(cell.value, cell.number_format)
            out[ws.title] = vals
    finally:
        wb.close()
    return out
