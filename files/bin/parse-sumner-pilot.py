#!/usr/bin/env python3
"""Parse Sumner County PILOT filings (2015-2025) from the comptroller reports into JSON.

PDFs are parsed from word coordinates (pdftotext -bbox-layout) so that empty cells
stay empty instead of collapsing. The 2023-2025 .ods is read straight from its cells.

Blank and $0.00 are different facts and are kept different: null vs 0.
"""

import json
import re
import subprocess
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent.parent
DIR = ROOT / "state_of_tennessee" / "tn_comptroller_pilot_reports" / "sumner_county"

COUNTIES = {
    "Anderson", "Bedford", "Benton", "Bradley", "Blount", "Campbell", "Cannon",
    "Carroll", "Carter", "Cheatham", "Chester", "Claiborne", "Clay", "Cocke",
    "Coffee", "Crockett", "Cumberland", "Davidson", "Decatur", "DeKalb", "Dickson",
    "Dyer", "Fayette", "Fentress", "Franklin", "Gibson", "Giles", "Grainger",
    "Greene", "Grundy", "Hamblen", "Hamilton", "Hancock", "Hardeman", "Hardin",
    "Hawkins", "Haywood", "Henderson", "Henry", "Hickman", "Houston", "Humphreys",
    "Jackson", "Jefferson", "Johnson", "Knox", "Lake", "Lauderdale", "Lawrence",
    "Lewis", "Lincoln", "Loudon", "Macon", "Madison", "Marion", "Marshall", "Maury",
    "McMinn", "McNairy", "Meigs", "Monroe", "Montgomery", "Moore", "Morgan",
    "Obion", "Overton", "Perry", "Pickett", "Polk", "Putnam", "Rhea", "Roane",
    "Robertson", "Rutherford", "Scott", "Sequatchie", "Sevier", "Shelby", "Smith",
    "Stewart", "Sullivan", "Sumner", "Tipton", "Trousdale", "Unicoi", "Union",
    "Van Buren", "Warren", "Washington", "Wayne", "Weakley", "White", "Williamson",
    "Wilson",
}

# Left-to-right field order per report year. Years whose crop includes no header row
# use the documented schema for their era.
SCHEMAS = {
    # 2015 names no counties - only the numeric code. Sumner is 83.
    2015: ["filing_date", "county_type", "lessee", "contact_name",
           "parcel", "prop_code", "assessor_flag", "prop_letter", "est_value",
           "rent", "pilot_city", "pilot_county", "leasehold_tax", "lease_end"],
    2016: ["county", "county_code", "filing_date", "project_type", "lessee",
           "address", "city", "contact_name", "email", "parcel", "prop_code",
           "assessor_flag", "prop_letter", "est_value", "rent", "pilot_city",
           "pilot_county", "leasehold_tax", "lease_begin", "lease_end"],
    2017: ["county", "county_code", "project_type", "filing_date", "case_number",
           "lessee", "address", "city", "parcel", "prop_code", "contact_name",
           "contact_title", "email", "est_value", "rent", "pilot_city",
           "pilot_county", "leasehold_tax", "lease_begin", "lease_end"],
    2018: ["county", "project_type", "filing_date", "case_number", "lessee",
           "address", "city", "parcel", "prop_code", "contact_name",
           "contact_title", "email", "est_value", "rent", "pilot_city",
           "pilot_county", "leasehold_tax", "lease_begin", "lease_end"],
    2019: ["county", "project_type", "filing_date", "case_number", "lessee",
           "address", "city", "parcel", "prop_code", "contact_name",
           "contact_title", "email", "est_value", "rent", "pilot_city",
           "pilot_county", "leasehold_tax", "lease_begin", "lease_end"],
    2020: ["county", "project_type", "filing_date", "case_number", "lessee",
           "address", "city", "parcel", "prop_type", "prop_code", "contact_name",
           "contact_title", "email", "est_value", "rent", "pilot_city",
           "pilot_county", "leasehold_tax", "lease_begin", "lease_end"],
    2021: ["county", "project_type", "filing_date", "lessee", "address", "city",
           "parcel", "prop_type", "prop_code", "contact_name", "contact_title",
           "email", "est_value", "rent", "pilot_city", "pilot_county",
           "leasehold_tax", "lease_begin", "lease_end"],
    2022: ["county", "project_type", "filing_date", "lessee", "address", "city",
           "parcel", "prop_type", "prop_code", "contact_name", "contact_title",
           "email", "est_value", "rent", "pilot_city", "pilot_county",
           "leasehold_tax", "lease_begin", "lease_end"],
}

MONEY_FIELDS = ("est_value", "rent", "pilot_city", "pilot_county", "leasehold_tax")
DATE_FIELDS = ("filing_date", "lease_begin", "lease_end")


def clean(s):
    """Strip soft hyphens, non-breaking spaces and collapse whitespace."""
    s = s.replace("­", "-").replace("–", "-").replace("—", "-")
    s = s.replace("\xa0", " ").replace("’", "'")
    return re.sub(r"\s+", " ", s).strip()


def money(raw):
    """'$1,854,800.00' -> 1854800 ; '' -> None ; '$0.00' -> 0."""
    if raw is None:
        return None
    t = clean(raw).replace("$", "").replace(",", "")
    if t in ("", "-", "NO INFO"):
        return None
    try:
        return int(round(float(t)))
    except ValueError:
        return None


def isodate(raw):
    """'9/23/2024' or '10/02/2020' -> '2024-09-23'. 'NO INFO'/'-' -> None."""
    if raw is None:
        return None
    t = clean(raw)
    m = re.fullmatch(r"(\d{1,2})/(\d{1,2})/(\d{2,4})", t)
    if not m:
        return None
    mo, d, y = (int(x) for x in m.groups())
    if y < 100:
        y += 2000 if y < 50 else 1900
    return f"{y:04d}-{mo:02d}-{d:02d}"


# --------------------------------------------------------------------------
# PDF: words -> cells -> rows -> columns
# --------------------------------------------------------------------------

def pdf_words(path):
    """[(page, x0, x1, ymid, text)] from pdftotext -bbox-layout."""
    xml = subprocess.run(
        ["pdftotext", "-bbox-layout", str(path), "-"],
        capture_output=True, text=True, check=True).stdout
    xml = xml.replace(' xmlns="http://www.w3.org/1999/xhtml"', "")
    root = ET.fromstring(xml)
    out = []
    for pno, page in enumerate(root.iter("page"), start=1):
        for w in page.iter("word"):
            txt = (w.text or "")
            if not txt.strip():
                continue
            out.append((pno, float(w.get("xMin")), float(w.get("xMax")),
                        (float(w.get("yMin")) + float(w.get("yMax"))) / 2, txt))
    return out


def group_rows(words, ytol=3.0):
    """Group words into visual rows by y proximity."""
    rows, cur, cury = [], [], None
    for w in sorted(words, key=lambda w: (w[0], w[3], w[1])):
        if cur and (w[0] != cur[0][0] or abs(w[3] - cury) > ytol):
            rows.append(sorted(cur, key=lambda w: w[1]))
            cur, cury = [], None
        cur.append(w)
        cury = w[3] if cury is None else (cury + w[3]) / 2
    if cur:
        rows.append(sorted(cur, key=lambda w: w[1]))
    return rows


def row_cells(row, gap=6.0):
    """Merge adjacent words into cells; a gap wider than `gap` starts a new cell."""
    cells = []
    for pno, x0, x1, y, txt in row:
        if cells and x0 - cells[-1][1] <= gap:
            cells[-1][1] = x1
            cells[-1][2] += " " + txt
        else:
            cells.append([x0, x1, txt])
    return [(c[0], c[1], clean(c[2])) for c in cells]


MONEY_RE = re.compile(r"^\$[\d,]+(\.\d\d)?$|^\$?0(\.00)?$")
DATE_RE = re.compile(r"^\d{1,2}/\d{1,2}/\d{2,4}$")


def money_bands(rows, expect):
    """Cluster the money cells across the whole document into columns.

    Money cells are narrow and right-aligned, so their x-ranges cluster cleanly
    where long text fields would smear together.
    """
    spans = []
    for row in rows:
        for x0, x1, txt in row_cells(row):
            if MONEY_RE.match(txt):
                spans.append([x0, x1])
    spans.sort()
    bands = [spans[0][:]]
    for s in spans[1:]:
        if s[0] <= bands[-1][1]:
            bands[-1][1] = max(bands[-1][1], s[1])
        else:
            bands.append(s[:])
    # widen each band to the midpoint of the gap to its neighbours
    out = []
    for i, (a, b) in enumerate(bands):
        lo = a - 2 if i == 0 else (bands[i - 1][1] + a) / 2
        hi = b + 2 if i == len(bands) - 1 else (b + bands[i + 1][0]) / 2
        out.append((lo, hi))
    return out


def build_columns(block_rows, gap=6.0):
    """Cluster cell x-ranges across rows into shared column bands."""
    bands = []
    for row in block_rows:
        for x0, x1, _ in row_cells(row, gap):
            for b in bands:
                if x0 <= b[1] and x1 >= b[0]:      # overlaps -> same column
                    b[0], b[1] = min(b[0], x0), max(b[1], x1)
                    break
            else:
                bands.append([x0, x1])
    bands.sort()
    merged = [bands[0]]
    for b in bands[1:]:
        if b[0] <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], b[1])
        else:
            merged.append(b)
    return merged


def sumner_block(rows, year):
    """Rows between the 'Sumner' label and the next county label."""
    if year == 2015:
        # No county names in this report - select on the county code instead.
        hits = [r for r in rows if is_data_row(r)
                and any(t == "83" or t.startswith("83 ")
                        for _, _, t in row_cells(r))]
        if not hits:
            raise SystemExit("2015: no county-code-83 rows found")
        return hits, True

    start = end = None
    for i, row in enumerate(rows):
        cells = row_cells(row)
        if not cells:
            continue
        first = cells[0][2]
        if start is None and first == "Sumner":
            start = i
            continue
        if start is not None:
            if first in COUNTIES and first != "Sumner":
                end = i
                break
            if re.match(r"^(COUNTY|Revised)\b", first):
                end = i
                break
    if start is None:
        raise SystemExit(f"{year}: no Sumner block found")
    if end is None:
        raise SystemExit(f"{year}: Sumner block has no closing county (crop may cut it)")
    return [r for r in rows[start:end] if row_cells(r)], end is not None


# Header labels as word sequences, longest first so "PILOT COUNTY" is consumed
# before a bare "COUNTY" can match it.
HEADER_LABELS = [
    (("PAR", "ID", "OR", "ID#"), "parcel"),
    (("PAR", "ID", "#", "OR", "ASSESSOR'S", "ID#"), "parcel"),
    (("PROPERTY", "DESCRIPTION"), "parcel"),
    (("PROPERTY", "ADDRESS"), "address"),
    (("PROP", "TYPE", "CODE"), "prop_code"),
    (("DATE", "RECEIVED"), "filing_date"),
    (("FILING", "DATE"), "filing_date"),
    (("CONTACT", "TITLE"), "contact_title"),
    (("EMAIL", "ADDRESS"), "email"),
    (("E-MAIL", "ADDRESS"), "email"),
    (("EST", "VALUE"), "est_value"),
    (("EST.", "VALUE"), "est_value"),
    (("PILOT", "COUNTY"), "pilot_county"),
    (("PILOT", "CITY"), "pilot_city"),
    (("LEASE", "BEGIN"), "lease_begin"),
    (("LEASE", "END"), "lease_end"),
    (("PROP", "TYPE"), "prop_type"),
    (("PROP", "CODE"), "prop_code"),
    (("TYPE", "CODE"), "prop_code"),
    (("CTY", "CODE"), "county_code"),
    (("PROJ", "TYPE"), "project_type"),
    (("L/H", "TAX"), "leasehold_tax"),
    (("LH", "TAX"), "leasehold_tax"),
    (("PAR", "ID"), "parcel"),
    (("LESSEE", "NAME"), "lessee"),
    (("PILOT/CO",), "pilot_county"),
    (("PILOT/CI",), "pilot_city"),
    (("IDB/HED",), "project_type"),
    (("ASSESSOR",), "assessor_flag"),
    (("CASE",), "case_number"),
    (("CONTACT",), "contact_name"),
    (("LESSEE",), "lessee"),
    (("ADDRESS",), "address"),
    (("COUNTY",), "county"),
    (("CITY",), "city"),
    (("RENT",), "rent"),
    (("PROP.",), "prop_letter"),
]


def match_header(row):
    """Match known labels against a header row's words -> [(x0, x1, field)]."""
    words = [(x0, x1, clean(t).upper().rstrip(":")) for _, x0, x1, _, t in row]
    used = [False] * len(words)
    found = []
    for label, field in HEADER_LABELS:
        n = len(label)
        for i in range(len(words) - n + 1):
            if any(used[i:i + n]):
                continue
            if tuple(w[2] for w in words[i:i + n]) == label:
                for j in range(i, i + n):
                    used[j] = True
                found.append((words[i][0], words[i + n - 1][1], field))
                break
    found.sort()
    return found


def find_header(rows):
    """First row that looks like the table header -> [(x0, x1, field)]."""
    for row in rows:
        found = match_header(row)
        if (sum(1 for f in found if f[2] in MONEY_FIELDS) >= 4
                and len(found) >= 12):
            return found
    return None


def is_data_row(row):
    """A filing line: has a date and at least one other cell."""
    cells = row_cells(row)
    return len(cells) > 3 and any(
        re.fullmatch(r"\d{1,2}/\d{1,2}/\d{2,4}", t) for _, _, t in cells)


def cluster_starts(data, xmax, tol=2.0, cells=False):
    """Cluster the x positions where text begins, left of `xmax`.

    Cell starts are strong evidence of a column (a real column is preceded by a
    wide gap). Word starts are the fallback for the case where two fields sit one
    space apart and merge into a single cell, hiding the second column's start.
    """
    if cells:
        xs = sorted(x0 for row in data for x0, x1, _ in row_cells(row, gap=5.0)
                    if x1 <= xmax)
    else:
        xs = sorted(w[1] for row in data for w in row if w[2] <= xmax)
    if not xs:
        return []
    groups = [[xs[0]]]
    for v in xs[1:]:
        if v - groups[-1][-1] <= tol:
            groups[-1].append(v)
        else:
            groups.append([v])
    return [(sum(g) / len(g), len(g)) for g in groups if len(g) >= 2]


def pick_starts(cell_cl, word_cl, nrows, labels, margin=12.0):
    """Locate each column's true left edge.

    Header labels are centred over their column, so a column's data starts to
    the left of its own label but never left of the previous label. That brackets
    the search; inside the bracket the real column start is the cluster backed by
    the most rows (interior words of a wide text field scatter, so they cluster
    weakly).
    """
    out = []
    for j, (hx, _) in enumerate(labels):
        lo = out[-1] if out else -1e9       # the previous column's real start
        def within(cl, minsup):
            c = [x for x, n in cl if lo < x <= hx + margin and n >= minsup]
            return min(c) if c else None
        pick = (within(cell_cl, nrows * 0.25)     # a gap-preceded column start
                or within(word_cl, nrows * 0.5)   # merged cell: fall back to words
                or within(cell_cl, 2)             # sparse column (county label)
                or within(word_cl, 2))
        out.append(pick if pick is not None else max(hx, lo + 1))
    return out


def align(detected, labels):
    """Assign every header label one detected column start, order preserving.

    Word-start clustering over-detects - a long text field produces peaks at its
    own interior words. Those extra starts get absorbed into the column they sit
    inside, which is what the monotonic constraint expresses.
    Returns [column index per label].
    """
    n, m = len(detected), len(labels)
    if m > n:
        return None
    INF = float("inf")
    f = [[INF] * (m + 1) for _ in range(n + 1)]
    back = [[None] * (m + 1) for _ in range(n + 1)]
    f[0][0] = 0.0
    for i in range(1, n + 1):
        f[i][0] = 0.0                     # leading columns before the first label
        back[i][0] = (i - 1, 0, False)
        for j in range(1, min(i, m) + 1):
            absorb = f[i - 1][j]          # column i-1 folds into the previous one
            match = f[i - 1][j - 1] + abs(detected[i - 1] - labels[j - 1][0])
            if match <= absorb:
                f[i][j], back[i][j] = match, (i - 1, j - 1, True)
            else:
                f[i][j], back[i][j] = absorb, (i - 1, j, False)
    if f[n][m] == INF:
        return None
    out, i, j = [None] * m, n, m
    while j > 0:
        pi, pj, matched = back[i][j]
        if matched:
            out[pj] = pi
        i, j = pi, pj
    return out


def header_boundaries(header, bands, data):
    """Header labels name and order the columns; the data says where they start.

    Header labels are centred over their column while values are left aligned,
    so the label span alone puts the boundary in the wrong place.
    """
    money_fields = [f for _, _, f in header if f in MONEY_FIELDS]
    left_labels = [(x0, f) for x0, x1, f in header
                   if f not in MONEY_FIELDS and not f.startswith("lease_")]
    lease_labels = [(x0, f) for x0, x1, f in header if f.startswith("lease_")]

    lefts = pick_starts(cluster_starts(data, bands[0][0], cells=True),
                        cluster_starts(data, bands[0][0]),
                        len(data), left_labels)
    cols = []
    for k, (_, f) in enumerate(left_labels):
        hi = lefts[k + 1] - 3 if k + 1 < len(lefts) else bands[0][0]
        cols.append([lefts[k] - 3, hi, f])

    for f, (lo, hi) in zip(money_fields, bands):
        cols.append([lo, hi, f])

    tail_rows = [r for r in ([w for w in row if w[1] >= bands[-1][1]]
                             for row in data) if r]
    if lease_labels:
        tails = pick_starts(cluster_starts(tail_rows, 1e9, tol=3.0, cells=True),
                            cluster_starts(tail_rows, 1e9, tol=3.0),
                            len(tail_rows), lease_labels)
        for k, (_, f) in enumerate(lease_labels):
            hi = tails[k + 1] - 3 if k + 1 < len(tails) else 1e6
            cols.append([tails[k] - 3, hi, f])

    have = {c[2] for c in cols}
    for _, _, f in header:
        if f not in have:
            cols.append([1e7, 1e7 + 1, f])   # column carries no data in this crop
    return [tuple(c) for c in cols]


# 2015 and 2021 carry no header row anywhere in the crop, so there is nothing to
# name the columns from. Their column starts (pt from the left edge) were read off
# the word coordinates and are recorded here; re-derive with:
#   pdftotext -bbox-layout <file> -
FALLBACK = {
    2015: {
        # county code and project type sit one space apart and merge; split later
        "left": [(47, "filing_date"), (88, "county_type"), (132, "lessee"),
                 (290, "contact_name"), (430, "parcel"), (535, "prop_code"),
                 (573, "assessor_flag"), (605, "prop_letter")],
        "money": ["est_value", "rent", "pilot_city", "pilot_county",
                  "leasehold_tax"],
        "lease": [(890, "lease_end")],
    },
    2021: {
        "left": [(14, "county"), (35, "project_type"), (50, "filing_date"),
                 (67, "lessee"), (151, "address"), (213, "city"),
                 (239, "parcel"), (276, "prop_type"), (294, "prop_code"),
                 (313, "contact_name"), (355, "contact_title"), (433, "email")],
        # the leasehold-tax column is empty throughout this report
        "money": ["est_value", "rent", "pilot_city", "pilot_county"],
        "lease": [(605, "lease_begin"), (628, "lease_end")],
    },
}


def pinned_columns(year, bands):
    spec = FALLBACK[year]
    cols = []
    left = spec["left"]
    for i, (x, f) in enumerate(left):
        hi = left[i + 1][0] - 3 if i + 1 < len(left) else bands[0][0]
        cols.append((x - 3, hi, f))
    for f, (lo, hi) in zip(spec["money"], bands):
        cols.append((lo, hi, f))
    lease = spec["lease"]
    for i, (x, f) in enumerate(lease):
        hi = lease[i + 1][0] - 3 if i + 1 < len(lease) else 1e6
        cols.append((x - 3, hi, f))
    return cols


def fallback_columns(data, fields, bands):
    """No header anywhere in the crop (2015, 2021): recover the left-hand
    columns from where words consistently start, and pin money to the bands."""
    left_fields = [f for f in fields if f not in MONEY_FIELDS
                   and not f.startswith("lease_")]
    lease_fields = [f for f in fields if f.startswith("lease_")]
    money_present = [f for f in fields if f in MONEY_FIELDS]

    money_lo, money_hi = bands[0][0], bands[-1][1]
    starts, tails = [], []
    for row in data:
        for x0, x1, txt in row_cells(row):
            if x1 <= money_lo:
                starts.append(x0)
            elif x0 >= money_hi and DATE_RE.fullmatch(txt):
                tails.append(x0)

    def peaks(vals, want, tol=4.0):
        vals = sorted(vals)
        groups = [[vals[0]]]
        for v in vals[1:]:
            (groups[-1] if v - groups[-1][-1] <= tol else groups.append([v]) or groups[-1]).append(v)
        groups = [g for g in groups if len(g) >= max(2, len(data) * 0.03)]
        groups.sort(key=len, reverse=True)
        keep = sorted(groups[:want], key=lambda g: g[0])
        return [sum(g) / len(g) for g in keep]

    lstarts = peaks(starts, len(left_fields))
    if len(lstarts) != len(left_fields):
        print(f"  ! fallback: {len(lstarts)} left columns vs {len(left_fields)} fields")
    cols = []
    for i, f in enumerate(left_fields[:len(lstarts)]):
        lo = lstarts[i] - 3
        hi = (lstarts[i + 1] - 3) if i + 1 < len(lstarts) else money_lo
        cols.append((lo, hi, f))
    for f, (lo, hi) in zip(money_present, bands):
        cols.append((lo, hi, f))
    tstarts = peaks(tails, len(lease_fields)) if tails else []
    for i, f in enumerate(lease_fields[-len(tstarts):] if tstarts else []):
        lo = tstarts[i] - 3
        hi = (tstarts[i + 1] - 3) if i + 1 < len(tstarts) else 1e6
        cols.append((lo, hi, f))
    for f in fields:
        if not any(c[2] == f for c in cols):
            cols.append((1e7, 1e7 + 1, f))     # column absent from this report
    return cols


ANCHORS = [
    ("project_type", lambda t: t in ("IDB", "HED")),
    ("prop_type", lambda t: t in ("Real", "Personal")),
    ("prop_code", lambda t: re.fullmatch(r"(ID|HE)-?\d{1,2}", t) is not None),
    ("email", lambda t: "@" in t),
    ("case_number", lambda t: re.fullmatch(r"IDB\d+", t) is not None),
    ("county", lambda t: t in COUNTIES),
    ("county_code", lambda t: re.fullmatch(r"0?\d{2,3}", t) is not None),
    ("assessor_flag", lambda t: t in ("Y", "N")),
    ("prop_letter", lambda t: re.fullmatch(r"[A-H]", t) is not None),
    ("filing_date", lambda t: DATE_RE.fullmatch(t) is not None),
]


def assign_by_anchor(cells, fields):
    """Assign left-hand cells to fields: unambiguous ones by content, the rest
    in reading order. Used for 2015 and 2021, which carry no header row."""
    slots = {f: "" for f in fields}
    taken = [False] * len(cells)
    for field, test in ANCHORS:
        if field not in fields or slots[field]:
            continue
        for i, (_, _, t) in enumerate(cells):
            if not taken[i] and test(t):
                slots[field] = t
                taken[i] = True
                break
    rest_fields = [f for f in fields if not slots[f]]
    rest_cells = [cells[i][2] for i in range(len(cells)) if not taken[i]]
    if len(rest_cells) > len(rest_fields) and "parcel" in rest_fields:
        # over-split cell, almost always the parcel id ("112 109  P 000")
        k = rest_fields.index("parcel")
        extra = len(rest_cells) - len(rest_fields)
        rest_cells[k:k + extra + 1] = [" ".join(rest_cells[k:k + extra + 1])]
    for f, v in zip(rest_fields, rest_cells):
        slots[f] = v
    return slots


def parse_pdf(path, year):
    rows = group_rows(pdf_words(path))
    block, complete = sumner_block(rows, year)
    data = [r for r in rows if is_data_row(r)]
    bands = money_bands(data, 5)
    header = find_header(rows)
    fields = SCHEMAS[year]

    cols = (header_boundaries(header, bands, data) if header
            else pinned_columns(year, bands))

    records = []
    for row in block:
        slots = {f: "" for _, _, f in cols}
        # Assign word by word, not cell by cell: two fields often sit close
        # enough to merge into one visual cell (case number + lessee, for one).
        for _, x0, x1, _, txt in row:
            cx = (x0 + x1) / 2
            field = min(cols, key=lambda c: 0 if c[0] <= cx <= c[1]
                        else min(abs(cx - c[0]), abs(cx - c[1])))[2]
            slots[field] = (slots[field] + " " + clean(txt)).strip()
        slots["_locator"] = f"p{row[0][0]}:y{row[0][3]:.0f}"
        slots["_block_complete"] = complete
        records.append(slots)
    return records


# --------------------------------------------------------------------------
# ODS (2023-2025): three stacked tables in one sheet
# --------------------------------------------------------------------------

T = "{urn:oasis:names:tc:opendocument:xmlns:table:1.0}"
O = "{urn:oasis:names:tc:opendocument:xmlns:office:1.0}"

ODS_FIELDS = ["county", "project_type", "filing_date", "lessee", "address", "city",
              "parcel", "prop_type", "prop_code", "contact_name", "contact_title",
              "email", "est_value", "rent", "pilot_city", "pilot_county",
              "leasehold_tax", "lease_begin", "lease_end"]


def parse_ods(path):
    root = ET.fromstring(zipfile.ZipFile(path).read("content.xml"))
    rows = []
    for r in root.iter(T + "table-row"):
        cells = []
        for c in r.findall(T + "table-cell"):
            rep = int(c.get(T + "number-columns-repeated", 1))
            rep = 1 if rep > 100 else rep
            # keep the stored numeric value too - it cross-checks the display string
            cells += [(clean("".join(c.itertext())), c.get(O + "value"))] * rep
        rows.append(cells)

    records, year, rowno = [], None, 0
    for cells in rows:
        rowno += 1
        texts = [t for t, _ in cells]
        joined = "".join(texts).strip()
        if not joined:
            continue
        if re.fullmatch(r"20\d\d", texts[0]):          # year banner
            year = int(texts[0])
            continue
        if any(h in texts for h in ("LESSEE NAME", "Lessee")):   # header row
            continue
        if year is None:
            continue
        rec = {}
        for i, f in enumerate(ODS_FIELDS):
            rec[f] = texts[i] if i < len(texts) else ""
        rec["county"] = "Sumner"
        rec["_year"] = year
        rec["_locator"] = f"Sheet1!row{rowno}"
        rec["_block_complete"] = True
        rec["_stored"] = {ODS_FIELDS[i]: cells[i][1]
                          for i in range(min(len(cells), len(ODS_FIELDS)))
                          if cells[i][1] is not None}
        records.append(rec)
    return records


# --------------------------------------------------------------------------

def split_county_code(raw):
    """Peel the county code off a cell it merged into.

    2015 runs the code straight into the project type ("83 IDB"); 2016 runs it
    into the filing date ("83 9/28/2016").
    """
    m = re.match(r"^(\d{2,3})\s+(.*)$", clean(raw.get("county_type", "")))
    if m:
        raw["county_code"], raw["project_type"] = m.group(1), m.group(2)
    m = re.match(r"^(\d{2,3})\s+(\d{1,2}/\d{1,2}/\d{2,4})$",
                 clean(raw.get("filing_date", "")))
    if m:
        raw["county_code"], raw["filing_date"] = m.group(1), m.group(2)
    return raw


def finalize(raw, year, source):
    """Type the values, keeping every original string alongside."""
    raw = split_county_code(raw)
    rec = {
        "report_year": year,
        "county": "Sumner",
        "project_type": raw.get("project_type") or None,
        "filing_date": isodate(raw.get("filing_date")),
        "case_number": raw.get("case_number") or None,
        "lessee": raw.get("lessee") or None,
        "property": {
            "address": raw.get("address") or None,
            "city": raw.get("city") or None,
            "parcel": raw.get("parcel") or None,
            "code": raw.get("prop_code") or None,
        },
        "contact": {
            "name": raw.get("contact_name") or None,
            "title": raw.get("contact_title") or None,
            "email": raw.get("email") or None,
        },
        "amounts": {},
        "lease": {
            "begin": isodate(raw.get("lease_begin")),
            "end": isodate(raw.get("lease_end")),
        },
        "source": {
            "file": source,
            "locator": raw.get("_locator"),
            "block_complete": raw.get("_block_complete", True),
        },
    }

    ptype = clean(raw.get("prop_type", "")).lower()
    if ptype in ("real", "personal"):
        rec["property"]["type"] = ptype
        rec["property"]["type_source"] = "column"
    else:
        parcel = raw.get("parcel") or ""
        rec["property"]["type"] = "personal" if re.search(r"\bP\s*\d*\b", parcel) else "real"
        rec["property"]["type_source"] = "inferred_from_parcel_suffix"

    for f in MONEY_FIELDS:
        rawv = raw.get(f, "")
        rec["amounts"][f] = {"raw": rawv, "usd": money(rawv)}

    # cross-check money against the ODS stored numeric values
    stored = raw.get("_stored") or {}
    mismatch = [f for f in MONEY_FIELDS
                if f in stored and money(raw.get(f, "")) != int(round(float(stored[f])))]
    rec["flags"] = ["money_display_vs_stored_mismatch:" + ",".join(mismatch)] if mismatch else []

    for k in ("lease_begin", "lease_end", "filing_date"):
        if clean(raw.get(k, "")) == "NO INFO":
            rec["flags"].append(f"{k}_no_info")
    return rec


def main():
    out = []
    for year in range(2015, 2023):
        src = f"{year}-pilot-sumner.pdf"
        print(f"parsing {src}")
        for raw in parse_pdf(DIR / src, year):
            out.append(finalize(raw, year, src))

    src = "2023-2025-pilot-sumner.pdf.ods"
    print(f"parsing {src}")
    for raw in parse_ods(DIR / src):
        out.append(finalize(raw, raw["_year"], src))

    out.sort(key=lambda r: (r["report_year"], r["lessee"] or "",
                            r["property"]["parcel"] or ""))
    dest = DIR / "derived" / "sumner-pilot.json"
    dest.write_text(json.dumps(out, indent=2) + "\n")
    print(f"\n{len(out)} records -> {dest}")
    from collections import Counter
    for y, n in sorted(Counter(r["report_year"] for r in out).items()):
        print(f"  {y}: {n}")


if __name__ == "__main__":
    main()
