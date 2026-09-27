"""Generate a demo C:\\Dashboard-style folder tree with realistic workbooks.

    python scripts/make_sample.py [target_root] [--seed-history]

The VPS input sheet mirrors the layout of the real template (merged header
bands, rotated section labels, benchmark / reference / target columns,
coast-down table, remarks and sign-off block). Values are illustrative.
"""
import datetime as dt
import json
import random
import shutil
import sys
from pathlib import Path

from openpyxl import Workbook
from openpyxl.comments import Comment
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.worksheet.datavalidation import DataValidation

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

DARK = "404040"
BLUE = "2F75B5"
BLUE_LT = "DDEBF7"
BLUE_MID = "BDD7EE"
ORANGE = "FFC000"
YELLOW = "FFFF00"
GREY = "F2F2F2"

thin = Side(style="thin", color="7F7F7F")
med = Side(style="medium", color="1F3864")
BOX = Border(left=thin, right=thin, top=thin, bottom=thin)


def fill(c):
    return PatternFill("solid", fgColor=c)


def style_range(ws, rng, fill_color=None, font=None, align=None, border=BOX):
    for row in ws[rng]:
        for cell in row:
            if fill_color:
                cell.fill = fill(fill_color)
            if font:
                cell.font = font
            if align:
                cell.alignment = align
            if border:
                cell.border = border


def put(ws, rng, value, fill_color=None, bold=False, color="000000", size=9, h="center", v="center",
        wrap=True, rotate=0, italic=False):
    first = rng.split(":")[0]
    if ":" in rng:
        ws.merge_cells(rng)
    ws[first] = value
    style_range(ws, rng if ":" in rng else f"{rng}:{rng}", fill_color,
                Font(name="Arial", size=size, bold=bold, color=color, italic=italic),
                Alignment(horizontal=h, vertical=v, wrap_text=wrap, text_rotation=rotate))


SKIP = object()
GROUPS = {"B": ("D", "F"), "R": ("G", "I"), "T": ("J", "L")}


def row3(ws, r, label, b, ref, tgt, label_bold=False, tgt_fill=BLUE_LT, h=None):
    put(ws, f"B{r}:C{r}", label, bold=label_bold, h="left")
    put(ws, f"D{r}:F{r}", b)
    put(ws, f"G{r}:I{r}", ref, fill_color=BLUE_LT)
    if tgt is not SKIP:
        put(ws, f"J{r}:L{r}", tgt, fill_color=tgt_fill)
    if h:
        ws.row_dimensions[r].height = h


def section(ws, r1, r2, title):
    put(ws, f"A{r1}:A{r2}", title, fill_color=BLUE, bold=True, color="FFFFFF", size=9, rotate=90)


def vps_sheet(wb, project, variant_label, seed=0):
    rnd = random.Random(seed)
    ws = wb.active
    ws.title = "VPS Input"
    ws.sheet_view.showGridLines = False
    ws.sheet_view.zoomScale = 100
    widths = {"A": 4.5, "B": 30, "C": 16, "D": 13, "E": 13, "F": 13, "G": 14, "H": 14, "I": 14,
              "J": 14, "K": 14, "L": 14}
    for k, w in widths.items():
        ws.column_dimensions[k].width = w

    # ---- Title band
    put(ws, "A1:L1", "ENGINEERING — VEHICLE PERFORMANCE", fill_color=DARK, bold=True, color="FFFFFF", size=13)
    ws.row_dimensions[1].height = 24
    put(ws, "A2:L2", "Vehicle Product Requirements & Vehicle Data", fill_color="595959", bold=True,
        color="FFFFFF", size=10)
    put(ws, "A3:L3", f"Engineering Inputs Signoff : Product Performance & FE Requirements for {project} Variants",
        fill_color=GREY, size=8, italic=True)
    put(ws, "A4:B4", "Project", fill_color=GREY, bold=True)
    put(ws, "C4:F4", f"{project} _ {variant_label}", bold=True, h="left")
    put(ws, "G4:H4", "Document No.", fill_color=GREY, bold=True)
    put(ws, "I4:L4", f"VPS-{project}-{seed:03d}", h="left")

    # ---- Column headers
    put(ws, "A5:C6", "Vehicle Data", fill_color=BLUE, bold=True, color="FFFFFF", size=10)
    put(ws, "D5:F5", "BENCHMARK", fill_color=BLUE, bold=True, color="FFFFFF")
    put(ws, "D6:F6", "Competitor LCV DC _ 2.2L", fill_color=BLUE, bold=True, color="FFFFFF")
    put(ws, "G5:I5", "Reference vehicle", fill_color=BLUE, bold=True, color="FFFFFF")
    put(ws, "G6:I6", "Previous gen _ DC _ FB _ 2WD _ 1.1T\n(VPS Signoff Dec 2025)", fill_color=BLUE_MID, bold=True)
    put(ws, "J5:L5", "Target Vehicle - 1", fill_color=ORANGE, bold=True)
    put(ws, "J6:L6", f"{project} _ {variant_label}\n( High )", fill_color=BLUE_MID, bold=True)
    ws.row_dimensions[6].height = 30

    r = 7
    vehicle = [
        ("Vehicle Category", "N1", "N1", "N1"),
        ("Vehicle Class based on AIS175", "Class 2", "Class 2", "Class 2"),
        ("Type of construction (Monocoque / Chassis)", "Chassis", "Chassis", "Chassis"),
        ("Steering Type", "Hydraulic Assisted Power Steering", "Hydraulic Assisted Power Steering",
         "Hydraulic Assisted Power Steering"),
        ("No. of Seats & No. of Doors", "D + 4 & 4 Doors", "D + 4 & 4 Doors", "D + 4 & 4 Doors"),
        ("L x W x H (mm)", "5350 x 1860 x 1834", "4859 x 1700 x 1855 (CMVR)", "5064 x 1710 x 1862"),
        ("Wheelbase (mm) & Wheel Track (mm)", "WB : 3300 | WT - Front : 1550 & Rear : 1460",
         "WB : 3014 | WT - Front : 1443 & Rear : 1335", "WB : 3150 | WT - Front : 1480 & Rear : 1480"),
        ("Drive ( 2WD / 4WD / AWD )", "2WD", "2WD", "2WD"),
        ("Frontal Area  (m²)", "—", 2.706, 2.818),
        ("Cd", "—", "—", 0.65),
    ]
    start = r
    for row in vehicle:
        row3(ws, r, *row)
        r += 1
    # Weight distribution sub-table
    put(ws, f"B{r}:C{r}", "Weight Distributions", fill_color=BLUE_MID, bold=True, h="left")
    for col, txt in zip("DEFGHIJKL", ["Kerb", "WLTP", "GVW", "Kerb ( as per CMVR )", "WLTP", "GVW ( as per CMVR )",
                                      "Kerb ( Estimated )", "WLTP", "GVW ( Estimated )"]):
        put(ws, f"{col}{r}", txt, fill_color=BLUE_MID, bold=True)
    r += 1
    weights = [("FAW (kg)", ["—", "—", 1240, 815, "—", 835, 989, 802, 1077]),
               ("RAW (kg)", ["—", "—", 1750, 835, "—", 1860, 836, 1421, 1909]),
               ("Overall  Weight (kg)", [1868, 2254, 2990, 1650, 2015, 2695, 1825, 2222, 2985])]
    for label, vals in weights:
        put(ws, f"B{r}:C{r}", label, h="left", bold=label.startswith("Overall"))
        for col, val in zip("DEFGHIJKL", vals):
            put(ws, f"{col}{r}", val, fill_color=BLUE_LT if col in "GHIJKL" else None, bold=label.startswith("Overall"))
        r += 1
    row3(ws, r, "Payload (kg)", 1122, 1045, 1160); r += 1
    row3(ws, r, "GCW (kg)", "Not Applicable", "Not Applicable", "Not Applicable"); r += 1
    section(ws, start, r - 1, "Vehicle")

    # ---- Powertrain
    start = r
    powertrain = [
        ("Engine", "2.2L _ Diesel", "2.5L _ 4 Cylinder", "2.5L _ 4 Cylinder _ Diesel _ CI _ Single Turbo"),
        ("Engine Max Power", "100 HP (74.8kW) @ 3750 RPM", "80 hp (59.7 kW) @ 3200 RPM", "80 hp (59.7 kW) @ 3200 RPM"),
        ("Engine Max Torque", "250 Nm (1000 - 2500) RPM", "220 Nm @ 1400 - 2200 RPM", "220 Nm @ 1400 - 2200 RPM"),
        ("Engine Start Stop Availability", "No", "No", "No"),
        ("Transmission Type", "5 Speed - MT", "5 Speed - MT", "5 Speed - MT"),
        ("Transmission Model", "—", "All Synchromesh", "5MT320"),
        ("Transmission Gear Ratio", "4.49 | 2.22 | 1.42 | 1.00 | 0.73 | Rev : 3.75",
         "4.000 | 2.090 | 1.380 | 1.000 | 0.789 | Rev : 3.550", "4.605 | 2.628 | 1.534 | 1.000 | 0.832 | Rev : 4.128"),
        ("Axle ratio", 4.1, 4.3, 4.3),
        ("Transfercase Ratio (Low)", "Not Applicable", "Not Applicable", "Not Applicable"),
    ]
    for row in powertrain:
        row3(ws, r, *row)
        r += 1
    section(ws, start, r - 1, "Powertrain")

    # ---- Wheels & brakes
    start = r
    wheels = [
        ("Tyre Make", "Brand A", "Brand B", "Brand A, Brand B, Brand C", None),
        ("Tyre Size & Rim Size", "215/75 R16 &  5.5J x 16", "235 / 75 R15 & 6J x 15", "235 / 75 R15 LT ( 8 PR ) & 6J x 15 (TBC)", None),
        ("Load Index & Speed Index", "—", "Load index : 105 ( Max Load : 925 kg )\nSpeed index : S ( 180 kmph )",
         "116 (1250 kg) | L (120kmph), N (140kmph), Q (160kmph)", 30),
        ("Tyre DRR (m)", "—", 0.354, "0.370 ± 2 %", None),
        ("Tyre CRR (N/kN) @ ISO28580 or AIS142", "—", "9.26 @ 80 Psi inflation pressure @786kg load",
         "8.5 N/kN(Max) @ 80 psi Tyre Pressure & 1063 kg Load", None),
        ("Brake Type & Residual Brake Drag Target : Front & Rear", "Front : Disc & Rear : Drum",
         "Front : Disc ( 5.0 Nm ) | Rear : Drum ( 1.0 Nm )", "Front : Disc ( 5.0 Nm ) | Rear : Drum ( 1.0 Nm )", 26),
    ]
    for label, b, ref, tgt, h in wheels:
        row3(ws, r, label, b, ref, tgt, h=h)
        r += 1
    section(ws, start, r - 1, "Wheels & Brakes")

    # ---- Coast down
    start = r
    coast = [
        ("Towing Capacity (kg)", "Not Applicable", "Not Applicable", "Not Applicable"),
        ("Coast Down Test Mass (kg) in AIS137", 2018, "—", "—"),
        ("Coast Down Test Mass (kg) in AIS175", 2255, 2015, 2222),
        ("Tyre Pressure - Front & Rear", "Unladen & Laden : Front : 38 | Rear : 76",
         "Unladen : Front - 28 psi & Rear - 28 psi\nLaden : Front - 28 psi & Rear - 36 psi",
         "Unladen : 37 psi / 37 psi & Laden : 37 psi / 65 psi"),
        ("Rolling Resistance: a (N)", "—", "Ref Coast Down Curve", "Ref Coast Down Curve"),
        ("Aerodynamic Resistance: b (N/kmph²)", "—", "Ref Coast Down Curve", "Ref Coast Down Curve"),
        ("Transmission Friction Power (kW)", "—", "0.61kW  @ 80  kmph", "0.60kW @ 80  kmph"),
        ("Rear Axle Friction Power (kW)", "—", "0.88kW @80 kmph", "0.88kW @ 80 Kmph"),
        ("Transfercase Friction Power (kW) @ 80kmph", "Not Applicable", "Not Applicable", "Not Applicable"),
    ]
    for row in coast:
        row3(ws, r, *row, h=28 if "\n" in str(row[2]) else None)
        r += 1
    # coast-down table header
    hdr = r
    put(ws, f"C{hdr}", "Speed\n(kmph)", fill_color=BLUE_MID, bold=True)
    heads = ["Coastdown Force (N)\nAIS 175\nMeasured", None, "DTL (kW)\nKerb\nMeasured",
             "Coastdown Force (N)\nAIS 175 Default\n± 3% Margin", "Coastdown Force (N)\nAIS 175\n± 3% Margin",
             "DTL (kW)\nKerb\n± 5% Margin",
             "Coastdown Force (N)\nAIS 175 Default\n± 3% Margin", "Coastdown Force (N)\nAIS 175\n± 3% Margin",
             "DTL (kW)\nKerb\n± 5% Margin"]
    put(ws, f"D{hdr}:E{hdr}", heads[0], fill_color=BLUE_MID, bold=True)
    for col, txt in zip("FGHIJKL", heads[2:]):
        put(ws, f"{col}{hdr}", txt, fill_color=BLUE_MID, bold=True)
    ws.row_dimensions[hdr].height = 48
    r += 1
    base = [272, 317, 378, 452, 542, 647, None]
    for i, speed in enumerate(range(20, 90, 10)):
        put(ws, f"C{r}", speed)
        f_bm = base[i]
        put(ws, f"D{r}:E{r}", f_bm if f_bm else "—")
        put(ws, f"F{r}", round(0.65 + i * 0.44, 2))
        ref_def = 309 + i * 25 + rnd.randint(0, 9)
        ref = round(ref_def * 1.08)
        put(ws, f"G{r}", ref_def, fill_color=BLUE_LT)
        put(ws, f"H{r}", ref, fill_color=BLUE_LT)
        # DTL (kW) = F(N) * v(km/h) / 3600
        ws[f"I{r}"] = f"=ROUND(H{r}*C{r}/3600,2)"
        style_range(ws, f"I{r}:I{r}", BLUE_LT, Font(name="Arial", size=9), Alignment(horizontal="center", vertical="center"))
        tgt_def = 335 + i * 28 + rnd.randint(0, 9)
        put(ws, f"J{r}", tgt_def, fill_color=BLUE_LT)
        put(ws, f"K{r}", round(tgt_def * 1.03), fill_color=BLUE_LT)
        ws[f"L{r}"] = f"=ROUND(K{r}*C{r}/3600,2)"
        style_range(ws, f"L{r}:L{r}", BLUE_LT, Font(name="Arial", size=9), Alignment(horizontal="center", vertical="center"))
        r += 1
    put(ws, f"B{hdr}:B{r - 1}", "Coast down force data\n(if coast down coefficients a & b values are not available)",
        size=8, h="left", v="center")
    section(ws, start, r - 1, "Coast down")

    # ---- Performance
    start = r
    row3(ws, r, "Performance Test weight (kg)", 2990, "2715 ( Taken from Reference vehicle GVW)", 2985); r += 1
    row3(ws, r, "Engine Operation Mode", "—", "—", SKIP); r += 1
    put(ws, f"B{r}:C{r}", "", h="left")
    put(ws, f"D{r}:F{r}", "")
    put(ws, f"G{r}:H{r}", "Actual", fill_color=BLUE_MID, bold=True)
    put(ws, f"I{r}", "Simulated", fill_color=BLUE_MID, bold=True)
    perf_top = r
    r += 1
    perf = [("Through Gear (Sec)", "0 — 60 kmph", "Normal : 10.17  ECO : 16.24", 11.5, 12.2),
            ("", "0 — 70 kmph", "Normal : 13.10  ECO : 43.42", 15.2, 15.8),
            ("In Gear (Sec)  GR : 2", "20 — 40 kmph", "Normal : 3.57  ECO : 3.54", 4.0, 4.0),
            ("In Gear (Sec)  GR : 3", "30 — 60 kmph", "Normal : 8.26  ECO : 23.04", 8.6, 8.7),
            ("In Gear (Sec)  GR : 4", "40 — 70 kmph", "Normal : 11.62  ECO : 37.11", 12.1, 12.8),
            ("In Gear (Sec)  GR : 5", "50 — 75 kmph", "Normal : 13.01  ECO : 49.65", 14.6, 16.4),
            ("Max Speed (kmph)", "", 79, 80.0, 80.0),
            ("Stop - Start Gradeability (deg) @ GVW : Forward", "", 16.9, 12.6, 12.6),
            ("Stop - Start Gradeability (deg) @ GVW : Reverse", "", 15.1, 9, "—")]
    for label, sub, b, act, sim in perf:
        if sub:
            put(ws, f"B{r}", label, h="left")
            put(ws, f"C{r}", sub)
        else:
            put(ws, f"B{r}:C{r}", label, h="left")
        put(ws, f"D{r}:F{r}", b)
        put(ws, f"G{r}:H{r}", act, fill_color=BLUE_LT)
        put(ws, f"I{r}", sim, fill_color=BLUE_LT)
        r += 1
    put(ws, f"J{perf_top - 1}:L{r - 1}", "Performance expected to be the same as per 80 HP / 220 Nm vehicle and variant",
        fill_color=YELLOW, bold=True)
    section(ws, start, r - 1, "Performance")

    # ---- FE / CO2
    start = r
    fe = [("Drive Cycle ( NEDC / WLTC / RWUP / etc. )", "NEDC", "NEDC (MIDC)", "WLTP"),
          ("Emission Norms ( BS 4 / BS 6 / BS 6.2 / E4 / E5 / E6 / etc. )", "BS6.2", "BS6.2", "BS 6.2 ( WLTC / BS 7 )"),
          ("Hot FE Test Weight (kg) with ESS", 2255, "1820 (Taken from Reference vehicle test mass)", ""),
          ("Hot FE  : CD Method (kmpl)", 13.7, 14.4, ""),
          ("Cold FE  : PA  Method (kmpl)", 13.83, 14.0, "15.2kmpl NEDC\n15.8 kmpl WLTP"),
          ("WLTP Cold CD FE (AIS 175 Test weight)", 13.97, "—", ""),
          ("Cold CO₂ :PA Method (g/km)", "—", 189.1, ""),
          ("Inertia Class (kg)", "PA 2040 with 1.3 Factor", "PA 1810 with 1.3 Factor", "—")]
    for label, b, ref, tgt in fe:
        row3(ws, r, label, b, ref, tgt, tgt_fill=YELLOW if label.startswith(("Drive", "Hot", "Cold", "WLTP")) else BLUE_LT,
             h=26 if "\n" in str(tgt) else None)
        r += 1
    section(ws, start, r - 1, "FE / CO2")

    # ---- Remarks
    remarks = [
        ("Remarks : Energy Management Team",
         "1. This target has been given for BC Gateway only.\n2. CDF & DTL vehicle spec values referred from reference "
         "vehicles as per VPS Signoff Dec 2025.\n3. CDF & DTL targets will be revised after SOR to VOB process completion.\n"
         "4. Benchmark data taken from Benchmarking report & validation trials.", 64),
        ("Remarks : Validation team",
         "Need following in VPS output sheet\n1. DTL loss required at both front wheel end & rear wheel end\n"
         "2. If modes will be there - Mode wise target at each gear is required (In gear & Thru Gear)\n"
         "3. Each gear max speed target along with First & reverse gear torque limitations", 58),
        ("Remarks : Vehicle Integration",
         "1. Reference vehicle Weight details added as per the Previous VPS output sheet\n"
         "2. Benchmark vehicle weight added as per the Benchmark report\n3. Vehicle width mentioned without mirror condition", 44),
        ("Remarks : VPS Team", "", 22),
        ("Remarks : PP Team", "", 22),
        ("Performance Improvement of Target Vehicle w.r.t Benchmark / Ref. Vehicle (%)", "", 26),
    ]
    for label, text, h in remarks:
        put(ws, f"A{r}:C{r}", label, bold=label.startswith("Remarks"), h="left", size=8)
        put(ws, f"D{r}:L{r}", text, h="left", v="top", size=8)
        ws.row_dimensions[r].height = h
        r += 1

    # ---- Sign-off
    put(ws, f"A{r}:L{r}", "Reviewed By", fill_color=GREY, bold=True)
    r += 1
    roles = [("A{0}:C{0}", "Lead\nVehicle Engineering"), ("D{0}:E{0}", "Lead\nVehicle Integration"),
             ("F{0}", "Lead\nTransmission"), ("G{0}", "Lead\nRear Axle / Tyres"), ("H{0}", "Lead\nBrake"),
             ("I{0}:J{0}", "Head\nEngine Delivery & Transmission"), ("K{0}", "PEH"),
             ("L{0}", "Head\nVehicle Integration & Energy Mgmt")]
    for rng, role in roles:
        put(ws, rng.format(r), "", h="center")
        put(ws, rng.format(r + 1), role, bold=False, size=8)
        put(ws, rng.format(r + 2), "Date:", size=8, h="left")
    ws.row_dimensions[r].height = 36
    ws.row_dimensions[r + 1].height = 30
    r += 3
    put(ws, f"A{r}:L{r}", "Vehicle Performance Simulation COE (Confidential)", fill_color=BLUE_MID, bold=True, size=8)

    # ---- Logo (images are preserved on save and shown in the web view)
    ws.add_image(_logo(), "A1")

    # ---- Dropdown fields & notes
    dv = DataValidation(type="list", formula1='"N1,N2,N3,M1,M2"', allow_blank=True)
    dv2 = DataValidation(type="list", formula1='"2WD,4WD,AWD"', allow_blank=True)
    dv3 = DataValidation(type="list", formula1='"Yes,No"', allow_blank=True)
    ws.add_data_validation(dv)
    ws.add_data_validation(dv2)
    ws.add_data_validation(dv3)
    dv.add("J7")
    dv2.add("J14")
    dv3.add("J25")
    ws["J7"].comment = Comment("Vehicle category as per CMVR / AIS-053.", "VPS Team")
    ws.freeze_panes = "D7"
    ws.print_title_rows = "5:6"
    return ws


def _logo():
    import io
    from openpyxl.drawing.image import Image as XLImage
    from PIL import Image, ImageDraw, ImageFont
    img = Image.new("RGBA", (120, 30), (255, 255, 255, 255))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((1, 1, 118, 28), radius=5, fill=(196, 30, 58, 255))
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 15)
    except OSError:
        font = ImageFont.load_default()
    d.text((60, 15), "YOUR LOGO", fill="white", anchor="mm", font=font)
    buf = io.BytesIO()
    img.save(buf, "PNG")
    buf.seek(0)
    x = XLImage(buf)
    x.width, x.height = 120, 30
    return x


def dvp_workbook(project):
    wb = Workbook()
    ws = wb.active
    ws.title = "DVP Plan"
    ws.sheet_view.showGridLines = False
    heads = ["#", "Test", "Standard", "Samples", "Owner", "Planned Start", "Status", "Result"]
    widths = [5, 34, 16, 10, 18, 14, 14, 30]
    for i, (h, w) in enumerate(zip(heads, widths), start=1):
        c = ws.cell(row=2, column=i, value=h)
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = fill(BLUE)
        c.alignment = Alignment(horizontal="center", vertical="center")
        c.border = BOX
        ws.column_dimensions[chr(64 + i)].width = w
    ws.merge_cells("A1:H1")
    ws["A1"] = f"{project} — Design Verification Plan"
    ws["A1"].font = Font(bold=True, size=14, color="1F3864")
    ws.row_dimensions[1].height = 26
    tests = [("Coast down", "AIS-175"), ("Fuel economy (WLTC)", "AIS-175"), ("Gradeability", "IS 14272"),
             ("Acceleration 0-60", "Internal"), ("Max speed", "IS 10278"), ("Brake drag", "Internal"),
             ("Tyre rolling resistance", "ISO 28580"), ("Cooling performance", "Internal")]
    for i, (t, std) in enumerate(tests, start=3):
        row = [i - 2, t, std, 2, "", dt.date(2026, 10, 1) + dt.timedelta(days=7 * i), "Planned", ""]
        for j, v in enumerate(row, start=1):
            c = ws.cell(row=i, column=j, value=v)
            c.border = BOX
            c.alignment = Alignment(horizontal="left" if j in (2, 5, 8) else "center", vertical="center")
            if j == 6:
                c.number_format = "dd-mmm-yyyy"
    dv = DataValidation(type="list", formula1='"Planned,In Progress,Passed,Failed,On Hold"')
    ws.add_data_validation(dv)
    dv.add(f"G3:G{len(tests) + 2}")
    ws.freeze_panes = "A3"
    return wb


TREE = {
    "P115": {
        "M1 - Concept": ["DC_NFB_2WD_1.25T", "SC_FB_2WD_1.5T"],
        "M2 - Design Signoff": ["DC_NFB_2WD_1.25T", "DC_NFB_4WD_1.25T"],
    },
    "P149": {
        "M1 - Concept": ["DC_FB_2WD_1.1T"],
        "M3 - Validation": ["DC_FB_2WD_1.1T", "SC_FB_2WD_1.3T"],
    },
    "P201": {
        "M0 - Kickoff": ["Base_2WD"],
    },
}


def build(root: Path):
    seed = 1
    for model, milestones in TREE.items():
        for milestone, variants in milestones.items():
            for variant in variants:
                d = root / model / milestone / variant
                d.mkdir(parents=True, exist_ok=True)
                wb = Workbook()
                vps_sheet(wb, model, variant.replace("_", " _ "), seed)
                wb.save(d / f"VPS Input Sheet - {model} {variant}.xlsx")
                if seed % 2:
                    dvp_workbook(model).save(d / f"DVP Plan - {model}.xlsx")
                seed += 1


def store_formula_results(root: Path):
    """Write cached results for the demo formulas, like Excel does on save.

    openpyxl cannot compute formulas, so the (simple) ROUND(H*C/3600,2)
    formulas used in the coast-down table are evaluated here and the result
    is stored in each <c><v> element.
    """
    import io
    import re
    import zipfile
    from lxml import etree
    ns = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
    pat = re.compile(r"ROUND\(([A-Z]+)(\d+)\*([A-Z]+)(\d+)/3600,2\)")
    for f in root.rglob("VPS*.xlsx"):
        zin = zipfile.ZipFile(f)
        files = {i.filename: zin.read(i.filename) for i in zin.infolist()}
        infos = zin.infolist()
        zin.close()
        name = "xl/worksheets/sheet1.xml"
        tree = etree.fromstring(files[name])
        vals = {}
        for c in tree.iter(f"{ns}c"):
            v = c.find(f"{ns}v")
            if v is not None and v.text and c.get("t") in (None, "n"):
                vals[c.get("r")] = float(v.text)
        for c in tree.iter(f"{ns}c"):
            fe = c.find(f"{ns}f")
            if fe is None:
                continue
            m = pat.fullmatch(fe.text or "")
            if not m:
                continue
            a = vals.get(m.group(1) + m.group(2), 0)
            b = vals.get(m.group(3) + m.group(4), 0)
            v = c.find(f"{ns}v")
            if v is None:
                v = etree.SubElement(c, f"{ns}v")
            v.text = repr(round(a * b / 3600, 2))
        files[name] = etree.tostring(tree, xml_declaration=True, encoding="UTF-8", standalone=True)
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zout:
            for info in infos:
                zout.writestr(info, files[info.filename])
        f.write_bytes(buf.getvalue())


def seed_history(root: Path):
    """Create a believable edit history so the dashboard isn't empty in a demo."""
    from server.storage import Store
    store = Store(str(root))
    users = ["Energy Mgmt", "Vehicle Integration", "Validation Team", "VPS Team", "Powertrain"]
    rnd = random.Random(7)
    docs = list(store.all_docs())
    edits_pool = [
        ("VPS Input", "15,10", ["2.83", "2.79", "2.81"]),
        ("VPS Input", "16,10", ["0.64", "0.66", "0.62"]),
        ("VPS Input", "20,11", ["1830", "1822", "1818"]),
        ("VPS Input", "21,10", ["1155", "1162", "1170"]),
        ("VPS Input", "35,10", ["0.368 ± 2 %", "0.372 ± 2 %"]),
        ("DVP Plan", "3,7", ["In Progress", "Passed"]),
        ("DVP Plan", "4,5", ["Energy Mgmt", "Validation Team"]),
        ("DVP Plan", "5,7", ["In Progress"]),
    ]
    notes = ["Updated target weights after supplier input", "Aligned Cd with latest CFD run",
             "Review comments incorporated", "Corrected tyre DRR per spec sheet", "Status update for weekly review",
             "Payload revised as per GVW change", ""]
    for f in docs:
        rel = store.rel(f)
        store.sync(rel)
        sheets = {"VPS Input"} if "VPS" in f.name else {"DVP Plan"}
        for _ in range(rnd.randint(1, 4)):
            edits = {}
            for sheet, key, values in rnd.sample(edits_pool, 3):
                if sheet in sheets:
                    edits.setdefault(sheet, {})[key] = rnd.choice(values)
            if edits:
                store.save(rel, edits, rnd.choice(users), rnd.choice(notes), None)
        if rnd.random() < 0.6:
            store.set_status(rel, rnd.choice(["In Review", "Approved", "Draft", "Released"]), rnd.choice(users))
    # spread timestamps over the last two weeks
    now = dt.datetime.now().astimezone()
    act = store.meta_root / "activity.jsonl"
    lines = [json.loads(line) for line in act.read_text(encoding="utf-8").splitlines() if line.strip()]
    n = len(lines)
    stamps = sorted(now - dt.timedelta(minutes=rnd.randint(30, 60 * 24 * 13)) for _ in range(n))
    remap = {}
    for line, ts in zip(lines, stamps):
        new = ts.isoformat(timespec="seconds")
        remap[(line["path"], line.get("rev"), line["action"])] = new
        line["time"] = new
    act.write_text("\n".join(json.dumps(x, ensure_ascii=False) for x in lines) + "\n", encoding="utf-8")
    for rj in (store.meta_root / "docs").rglob("revisions.json"):
        revs = json.loads(rj.read_text(encoding="utf-8"))
        rel = rj.parent.relative_to(store.meta_root / "docs").as_posix()
        first = None
        for r in revs:
            key = (rel, r["rev"], "edit")
            if key in remap:
                r["time"] = remap[key]
                first = first or remap[key]
        if first:
            revs[0]["time"] = (dt.datetime.fromisoformat(first) - dt.timedelta(days=1)).isoformat(timespec="seconds")
        rj.write_text(json.dumps(revs, indent=1, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    target = Path(args[0]) if args else ROOT / "sample_data" / "Dashboard"
    if target.exists():
        shutil.rmtree(target)
    build(target)
    store_formula_results(target)
    if "--seed-history" in sys.argv:
        seed_history(target)
    print(f"Sample documents written to {target}")
