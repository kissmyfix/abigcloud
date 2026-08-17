#!/usr/bin/env python3
"""Parse Tennessee Parcel Details Reports into one machine-readable file.

Reads the PDFs in state_of_tennessee/tn_property_assessments/ from word
coordinates (pdftotext -bbox-layout)
rather than flowed text. The reports lay commercial buildings out side by side in
two columns, so flowed text interleaves them; coordinates keep them apart.

Regenerate with:  python3 files/bin/parse-assessment.py
"""

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from xml.etree import ElementTree as ET

NS = "{http://www.w3.org/1999/xhtml}"
ROOT = Path(__file__).resolve().parent.parent.parent
HERE = ROOT / "state_of_tennessee" / "tn_property_assessments"
OUT = HERE / "derived" / "sumner-assessments.json"

# The report is a four-column grid. A commercial building panel occupies two
# adjacent columns, so a building starting at x=7 owns [7,405) and one starting
# at x=405 owns [405, page width).
PANEL_SPLIT = 405.0

SECTION_TITLES = {
    "Value Information",
    "Subdivision Data",
    "Additional Information",
    "General Information",
    "Outbuildings & Yard Items",
    "Sale Information",
    "Land Information",
}

# Inside a building panel these end a table as surely as a section title does.
BUILDING_STOPS = SECTION_TITLES | {
    "Commercial Features", "Building Sketch", "Interior/Exterior Areas",
    "Type Units", "Square",
}

BUILDING_LABELS = [
    "Improvement Type", "Actual Year Built", "Quality", "Business Living Area",
    "Foundation", "Floor System", "Roof Framing", "Roof Cover/Deck",
    "Cabinet/Millwork", "Floor Finish", "Interior Finish", "Paint/Decor",
    "Bath Tiles", "Electrical", "Shape", "Structural Frame", "Heat and AC",
    "Plumbing Fixtures",
]

LINE_TOL = 2.0      # words within this many points of each other share a line
FIELD_GAP = 11.2    # vertical distance from a label to its value
ROW_GAP = 14.0      # a new table row starts when the gap exceeds this
HEADER_GAP = 4.0    # column headers can sit only ~6pt apart
LABEL_GAP = 30.0    # 'Calculated Acres: 512.54' nearly touches the next label


# ---------------------------------------------------------------- extraction

class Word:
    __slots__ = ("page", "y", "x0", "x1", "text")

    def __init__(self, page, y, x0, x1, text):
        self.page, self.y, self.x0, self.x1, self.text = page, y, x0, x1, text

    def __repr__(self):
        return f"<{self.text!r} p{self.page} y{self.y:.1f} x{self.x0:.1f}>"


def read_words(pdf):
    xml = subprocess.run(
        ["pdftotext", "-bbox-layout", str(pdf), "-"],
        capture_output=True, text=True, check=True,
    ).stdout
    root = ET.fromstring(xml)
    pages, words = [], []
    for pi, page in enumerate(root.iter(NS + "page"), 1):
        pages.append(float(page.get("width")))
        for w in page.iter(NS + "word"):
            if not (w.text or "").strip():
                continue
            words.append(Word(pi, float(w.get("yMin")), float(w.get("xMin")),
                              float(w.get("xMax")), w.text))
    words.sort(key=lambda w: (w.page, w.y, w.x0))
    return words, pages


def rows(words, tol=LINE_TOL):
    """Group words into horizontal bands. Returns [(page, y, [words])]."""
    out = []
    for w in sorted(words, key=lambda w: (w.page, w.y, w.x0)):
        if out and out[-1][0] == w.page and abs(w.y - out[-1][1]) <= tol:
            out[-1][2].append(w)
        else:
            out.append((w.page, w.y, [w]))
    return [(p, y, sorted(ws, key=lambda w: w.x0)) for p, y, ws in out]


def phrases(ws, gap=8.0):
    """Split a row's words into runs separated by more than `gap` points."""
    out = []
    for w in ws:
        if out and w.x0 - out[-1][-1].x1 <= gap:
            out[-1].append(w)
        else:
            out.append([w])
    return out


def text_of(ws):
    return " ".join(w.text for w in ws).strip()


def left_rows(rws, page=1):
    """Rows restricted to the left panel, by default page 1 only.

    The left panel's key/value sections share y bands with the building panel on
    the right, so rows have to be clipped before anything is read off them.
    """
    out = []
    for p, y, ws in rws:
        if page is not None and p != page:
            continue
        inside = [w for w in ws if w.x0 < PANEL_SPLIT]
        if inside:
            out.append((p, y, inside))
    return out


def find_row(rws, text, page=None):
    for p, y, ws in rws:
        if page and p != page:
            continue
        if text_of(ws) == text:
            return (p, y, ws)
    return None


# ------------------------------------------------------------------- tables

def columns_from_header(header_rows):
    """Header words -> column spans. Stacked headers ('Square' over 'Feet')
    merge when their x ranges overlap."""
    cols = []
    for _, _, ws in header_rows:
        for ph in phrases(ws, gap=HEADER_GAP):
            span = [ph[0].x0, ph[-1].x1, text_of(ph)]
            for c in cols:
                if span[0] <= c[1] and c[0] <= span[1]:      # overlaps -> stacked
                    c[0], c[1] = min(c[0], span[0]), max(c[1], span[1])
                    c[2] = f"{c[2]} {span[2]}"
                    break
            else:
                cols.append(span)
    cols.sort()
    return cols


def assign(word, cols):
    """Column whose header span the word overlaps most.

    Overlap rather than a left-edge cut, because columns are aligned
    inconsistently: money and areas are right aligned and can start well left of
    their header, while type descriptions run well past theirs.
    """
    best, best_ov = None, -1.0
    for i, (x0, x1, _) in enumerate(cols):
        ov = min(word.x1, x1) - max(word.x0, x0)
        if ov > best_ov:
            best, best_ov = i, ov
    if best_ov > 0:
        return best
    # No overlap: the word is text that ran past its narrow header ("MFG" in
    # "44 - LIGHT MFG"). It belongs to the column it starts inside of, not to
    # whichever header centre happens to be nearest.
    starts = [i for i, (x0, _, _) in enumerate(cols) if word.x0 >= x0 - 1]
    return starts[-1] if starts else 0


def read_table(rws, header_rows, body_rows):
    """Body rows -> list of cell dicts, merging wrapped continuation lines."""
    cols = columns_from_header(header_rows)
    out, last_y, last_page = [], None, None
    for p, y, ws in body_rows:
        cont = (out and p == last_page and last_y is not None
                and y - last_y <= ROW_GAP)
        if not cont:
            out.append([[] for _ in cols])
        for w in ws:
            out[-1][assign(w, cols)].append(w.text)
        last_y, last_page = y, p
    names = [c[2] for c in cols]
    return [
        {n: (" ".join(cell).strip() or None) for n, cell in zip(names, row)}
        for row in out
    ]


def table_sections(rws, header_text, stop):
    """Every occurrence of a repeating table header, with the rows beneath it.

    Tables continue across pages and the header reprints on each one.
    """
    found = []
    for i, (p, y, ws) in enumerate(rws):
        if text_of(ws) != header_text:
            continue
        body = []
        for p2, y2, ws2 in rws[i + 1:]:
            if p2 != p:
                break
            t = text_of(ws2)
            if t in stop or t.startswith("Commercial Building #"):
                break
            body.append((p2, y2, ws2))
        found.append(((p, y, ws), body))
    return found


# ------------------------------------------------------------------- values

MONEY = re.compile(r"^\$-?[\d,]+(?:\.\d+)?$")


def money(raw):
    if raw is None:
        return {"raw": None, "usd": None}
    s = raw.strip()
    if not MONEY.match(s):
        return {"raw": s, "usd": None}
    return {"raw": s, "usd": int(round(float(s.replace("$", "").replace(",", ""))))}


def number(raw):
    if raw is None:
        return None
    s = raw.replace(",", "").strip()
    try:
        f = float(s)
    except ValueError:
        return None
    return int(f) if f.is_integer() else f


def clean(s):
    """A lone hyphen is the report's way of printing an empty cell."""
    if s is None:
        return None
    s = s.strip()
    return None if s in ("", "-") else s


def value_right(rws, label, page=1):
    """Value printed to the right of a label on the same line."""
    for p, y, ws in rws:
        if p != page:
            continue
        ph = phrases(ws)
        for i, run in enumerate(ph):
            if text_of(run) == label and i + 1 < len(ph):
                return text_of(ph[i + 1])
    return None


def value_below(rws, label, page=1, labels=(), x_tol=2.0):
    """Value printed under a label, left aligned with it."""
    anchor = None
    for p, y, ws in rws:
        if p != page:
            continue
        for run in phrases(ws):
            if text_of(run) == label:
                anchor = (p, y, run[0].x0)
    if not anchor:
        return None
    p, y, x = anchor
    for p2, y2, ws2 in rws:
        if p2 != p or not (FIELD_GAP - 1.5 <= y2 - y <= FIELD_GAP + 1.5):
            continue
        for run in phrases(ws2):
            if abs(run[0].x0 - x) <= x_tol:
                t = text_of(run)
                return None if t in labels else t
    return None


# ------------------------------------------------------------------ sections

def parse_header(rws, pages):
    hdr = {"county": None, "tax_year": None, "reappraisal_year": None,
           "situs_address": None}
    for p, y, ws in rws:
        if p != 1 or y > 70:
            continue
        for run in phrases(ws, gap=40.0):
            t = text_of(run)
            m = re.match(r"^([A-Za-z ]+) \((\d+)\)$", t)
            if m:
                hdr["county"] = {"name": m.group(1).strip(), "code": m.group(2)}
            m = re.match(r"^Tax Year (\d{4}) \| Reappraisal (\d{4})$", t)
            if m:
                hdr["tax_year"] = int(m.group(1))
                hdr["reappraisal_year"] = int(m.group(2))
            # Situs address sits alone in the top right, above the parcel strip.
            if y < 25 and run[0].x0 > 560:
                hdr["situs_address"] = t

    # Owner blocks are two stacked address columns; take every phrase that is
    # left aligned with the heading.
    owners = {}
    for key, label in (("jan1", "Jan 1 Owner"), ("current", "Current Owner")):
        owners[key] = None
        anchor = None
        for p, y, ws in rws:
            if p != 1:
                continue
            for run in phrases(ws, gap=40.0):
                if text_of(run) == label:
                    anchor = (y, run[0].x0)
        if not anchor:
            continue
        ay, ax = anchor
        lines = []
        for p, y, ws in rws:
            if p != 1 or y <= ay or y > 75:
                continue
            for run in phrases(ws, gap=40.0):
                if abs(run[0].x0 - ax) <= 2.0:
                    lines.append(text_of(run))
        owners[key] = lines or None
    hdr["owners"] = owners

    parcel = {}
    for key, label in (("ctrl_map", "Ctrl Map:"), ("group", "Group:"),
                       ("parcel", "Parcel:"), ("pi", "PI:"), ("si", "SI:")):
        parcel[key] = clean(value_below(rws, label, page=1))
    hdr["parcel"] = parcel
    # Canonical form matches the parcel strings in the comptroller PILOT
    # filings ("111 00100 000"), so the two datasets join on it.
    hdr["parcel_id"] = " ".join(x for x in (
        parcel.get("ctrl_map"),
        (parcel.get("group") or "") + (parcel.get("parcel") or "").replace(".", ""),
        parcel.get("si"),
    ) if x)
    return hdr


def parse_value(rws):
    pct = value_right(rws, "Assessment Percentage:")
    return {
        "land_market": money(value_right(rws, "Land Market Value:")),
        "improvement": money(value_right(rws, "Improvement Value:")),
        "total_market_appraisal": money(value_right(rws, "Total Market Appraisal:")),
        "assessment_percentage": {
            "raw": pct,
            "pct": number(pct.rstrip("%")) if pct else None,
        },
        "assessment": money(value_right(rws, "Assessment:")),
    }


def parse_subdivision(rws):
    labels = ("Plat Book:", "Plat Page:", "Block:", "Lot:", "Additional Information")
    return {
        "name": clean(value_below(rws, "Subdivision:", labels=labels)),
        "plat_book": clean(value_below(rws, "Plat Book:", labels=labels)),
        "plat_page": clean(value_below(rws, "Plat Page:", labels=labels)),
        "block": clean(value_below(rws, "Block:", labels=labels)),
        "lot": clean(value_below(rws, "Lot:", labels=labels)),
    }


def parse_additional(rws):
    start = find_row(rws, "Additional Information", page=1)
    stop = find_row(rws, "General Information", page=1)
    if not start or not stop:
        return None
    lines = [text_of(ws) for p, y, ws in rws
             if p == 1 and start[1] < y < stop[1] and abs(ws[0].x0 - 7.0) <= 2.0]
    return " ".join(lines) or None


def parse_general(rws):
    start = find_row(rws, "General Information", page=1)
    if not start:
        return {}
    fields = {}
    for p, y, ws in rws:
        if p != 1 or y <= start[1] or y > start[1] + 90:
            continue
        for run in phrases(ws, gap=LABEL_GAP):
            t = text_of(run)
            if ":" not in t:
                continue
            k, _, v = t.partition(":")
            fields[k.strip()] = clean(v)
    g = lambda k: fields.get(k)
    return {
        "class": g("Class"),
        "city": g("City"),
        "city_number": g("City #"),
        "district": g("District"),
        "neighborhood": g("Neighborhood"),
        "special_service_district_1": g("Special Service District 1"),
        "special_service_district_2": g("Special Service District 2"),
        "number_of_buildings": number(g("Number of Buildings")),
        "number_of_mobile_homes": number(g("Number of Mobile Homes")),
        "zoning": g("Zoning"),
        "utilities": {
            "electricity": g("Utilities - Electricity"),
            "water_sewer": g("Utilities - Water/Sewer"),
            "gas": g("Utilities - Gas/Gas Type"),
        },
    }


def parse_land(rws, lft):
    land = {"deed_acres": None, "calculated_acres": None, "total_land_units": None,
            "codes": []}
    start = find_row(lft, "Land Information", page=1)
    if start:
        for p, y, ws in lft:
            if p != 1 or not (start[1] < y < start[1] + 20):
                continue
            for run in phrases(ws, gap=LABEL_GAP):
                t = text_of(run)
                k, _, v = t.partition(":")
                key = {"Deed Acres": "deed_acres",
                       "Calculated Acres": "calculated_acres",
                       "Total Land Units": "total_land_units"}.get(k.strip())
                if key:
                    land[key] = number(clean(v))
    for header, body in table_sections(left_rows(rws, page=None),
                                       "Land Code Soil Class Units", SECTION_TITLES):
        for r in read_table(rws, [header], body):
            land["codes"].append({
                "code": clean(r.get("Land Code")),
                "soil_class": clean(r.get("Soil Class")),
                "units": number(clean(r.get("Units"))),
            })
    return land


def parse_outbuildings(rws):
    out = []
    header = "Building # Type Description Area/Units"
    for h, body in table_sections(rws, header, SECTION_TITLES):
        for r in read_table(rws, [h], body):
            row = {
                "building": number(clean(r.get("Building #"))),
                "type": clean(r.get("Type")),
                "description": clean(r.get("Description")),
                "area_units": number(clean(r.get("Area/Units"))),
            }
            if any(v is not None for v in row.values()):
                out.append(row)
    return out


def parse_sales(rws):
    out = []
    header = ("Sale Date Price Book Page Vacant/Improved Type Instrument Qualification")
    for h, body in table_sections(rws, header, SECTION_TITLES):
        for r in read_table(rws, [h], body):
            date = clean(r.get("Sale Date"))
            if not date:
                continue
            m = re.match(r"^(\d{1,2})/(\d{1,2})/(\d{4})$", date)
            out.append({
                "date": f"{m.group(3)}-{int(m.group(1)):02d}-{int(m.group(2)):02d}" if m else None,
                "date_raw": date,
                "price": money(clean(r.get("Price"))),
                "book": clean(r.get("Book")),
                "page": clean(r.get("Page")),
                "vacant_improved": clean(r.get("Vacant/Improved")),
                "instrument": clean(r.get("Type Instrument")),
                "qualification": clean(r.get("Qualification")),
            })
    return out


# ----------------------------------------------------------------- buildings

def building_regions(rws, pages):
    """Each 'Commercial Building #: N' heading -> the box of page it owns."""
    # Two buildings can share a y band, so headings are matched phrase by phrase.
    heads = []
    for p, y, ws in rws:
        for run in phrases(ws, gap=40.0):
            m = re.match(r"^Commercial Building #: (\d+)$", text_of(run))
            if m:
                heads.append({"num": int(m.group(1)), "page": p, "y": y,
                              "x": run[0].x0})
    heads.sort(key=lambda h: (h["page"], h["y"], h["x"]))
    regions = []
    for i, h in enumerate(heads):
        width = pages[h["page"] - 1]
        x0, x1 = (7.0, PANEL_SPLIT) if h["x"] < PANEL_SPLIT else (PANEL_SPLIT, width)
        # Vertical extent: down to the next heading on this page that starts a new
        # band (not the one sitting beside it), or to the next section title.
        y1 = float("inf")
        for other in heads[i + 1:]:
            if other["page"] == h["page"] and other["y"] > h["y"] + 5:
                y1 = min(y1, other["y"] - 3)
                break
        for p, y, ws in rws:
            if p != h["page"] or y <= h["y"] + 5:
                continue
            hit = [run for run in phrases(ws, gap=40.0)
                   if text_of(run) in SECTION_TITLES and x0 - 1 <= run[0].x0 < x1]
            if hit:
                y1 = min(y1, y - 3)
                break
        # A building's tables can spill onto following pages. Those pages carry
        # no heading of their own, so claim pages until one opens a new building
        # or a full-width section.
        claimed = [h["page"]]
        for pg in range(h["page"] + 1, len(pages) + 1):
            if any(o["page"] == pg for o in heads):
                break
            if any(p == pg and any(text_of(run) in SECTION_TITLES and run[0].x0 < 20
                                   for run in phrases(ws, gap=40.0))
                   for p, y, ws in rws):
                break
            claimed.append(pg)
        regions.append({"num": h["num"], "page": h["page"], "pages": claimed,
                        "y0": h["y"], "y1": y1, "x0": x0, "x1": x1})
    return regions


def in_region(rws, reg, pad=1.0):
    out = []
    for p, y, ws in rws:
        if p not in reg["pages"]:
            continue
        if p == reg["page"] and not (reg["y0"] < y <= reg["y1"]):
            continue
        inside = [w for w in ws if reg["x0"] - pad <= w.x0 < reg["x1"]]
        if inside:
            out.append((p, y, inside))
    return out


def parse_building(rws, reg):
    local = in_region(rws, reg)
    labels = tuple(f"{lab}:" for lab in BUILDING_LABELS) + (
        "Building Sketch", "Interior/Exterior Areas", "Commercial Features")

    fields = {}
    for lab in BUILDING_LABELS:
        fields[lab] = clean(value_below(local, f"{lab}:", page=reg["page"], labels=labels))

    areas = []
    for h, body in table_sections(local, "Type Feet Exterior Wall", BUILDING_STOPS):
        # 'Square' prints on its own line above 'Feet'; both belong to one column.
        square = [r for r in local
                  if r[0] == h[0] and 0 < h[1] - r[1] <= FIELD_GAP + 1
                  and text_of(r[2]) == "Square"]
        for r in read_table(local, square + [h], body):
            row = {
                "type": clean(r.get("Type")),
                "square_feet": number(clean(r.get("Square Feet"))),
                "exterior_wall": clean(r.get("Exterior Wall")),
            }
            if any(v is not None for v in row.values()):
                areas.append(row)

    features = []
    for h, body in table_sections(local, "Type Units", BUILDING_STOPS):
        for r in read_table(local, [h], body):
            if clean(r.get("Type")):
                features.append({"type": clean(r.get("Type")),
                                 "units": clean(r.get("Units"))})

    return {
        "building": reg["num"],
        "improvement_type": fields["Improvement Type"],
        "actual_year_built": number(fields["Actual Year Built"]),
        "quality": fields["Quality"],
        "business_living_area": number(fields["Business Living Area"]),
        "foundation": fields["Foundation"],
        "floor_system": fields["Floor System"],
        "roof_framing": fields["Roof Framing"],
        "roof_cover_deck": fields["Roof Cover/Deck"],
        "cabinet_millwork": fields["Cabinet/Millwork"],
        "floor_finish": fields["Floor Finish"],
        "interior_finish": fields["Interior Finish"],
        "paint_decor": fields["Paint/Decor"],
        "bath_tiles": fields["Bath Tiles"],
        "electrical": fields["Electrical"],
        "shape": fields["Shape"],
        "structural_frame": fields["Structural Frame"],
        "heat_and_ac": fields["Heat and AC"],
        "plumbing_fixtures": number(fields["Plumbing Fixtures"]),
        "areas": areas,
        "features": features,
    }


# --------------------------------------------------------------------- main

def parse_pdf(pdf):
    words, pages = read_words(pdf)
    rws = rows(words)
    lft = left_rows(rws)
    rec = parse_header(rws, pages)
    rec["value"] = parse_value(lft)
    rec["subdivision"] = parse_subdivision(lft)
    rec["additional_information"] = parse_additional(lft)
    rec["general"] = parse_general(lft)
    rec["land"] = parse_land(rws, lft)
    rec["buildings"] = [parse_building(rws, r) for r in building_regions(rws, pages)]
    rec["outbuildings"] = parse_outbuildings(rws)
    rec["sales"] = parse_sales(rws)
    rec["source"] = {
        "file": pdf.name,
        "pages": len(pages),
        "sha256": hashlib.sha256(pdf.read_bytes()).hexdigest(),
    }
    rec["flags"] = []
    return rec


# The county parcel viewer prints this line at the top of every report. Files
# without it are a different rendering of the same site and do not share this
# geometry — they are cross-check sources, not parse sources.
VIEWER_HEADER = "Tennessee Property Assessment Data - Parcel Details Report"


def is_viewer_report(pdf):
    t = subprocess.run(["pdftotext", "-layout", "-f", "1", "-l", "1", str(pdf), "-"],
                       capture_output=True, text=True, check=True).stdout
    return VIEWER_HEADER in t


def main():
    pdfs = sorted(HERE.glob("*.pdf"))
    records, seen = [], {}
    for pdf in pdfs:
        if not is_viewer_report(pdf):
            print(f"skipped {pdf.name}: not a parcel-viewer report (cross-check source)")
            continue
        rec = parse_pdf(pdf)
        key = rec["parcel_id"]
        if key in seen:
            # Same parcel already parsed from another file. Keep one record and
            # note the duplicate rather than double-counting it.
            other = seen[key]
            other["source"].setdefault("duplicate_files", []).append(rec["source"]["file"])
            same = json.dumps(strip_source(rec)) == json.dumps(strip_source(other))
            other["flags"].append(
                f"duplicate file {rec['source']['file']}: "
                + ("identical content" if same else "CONTENT DIFFERS — check")
            )
            continue
        seen[key] = rec
        records.append(rec)

    records.sort(key=lambda r: -(r["value"]["total_market_appraisal"]["usd"] or 0))
    OUT.write_text(json.dumps(records, indent=2) + "\n")
    print(f"{len(records)} parcels -> {OUT.relative_to(HERE)}")
    for r in records:
        print(f"  {r['parcel_id']:<20} {r['situs_address']:<22} "
              f"{r['value']['total_market_appraisal']['raw']:>14}  "
              f"{len(r['buildings'])} bldg  {len(r['outbuildings'])} outb  "
              f"{len(r['sales'])} sales")
        for f in r["flags"]:
            print(f"      flag: {f}")


def strip_source(rec):
    return {k: v for k, v in rec.items() if k not in ("source", "flags")}


if __name__ == "__main__":
    sys.exit(main())
