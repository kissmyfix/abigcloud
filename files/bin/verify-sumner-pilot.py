#!/usr/bin/env python3
"""All-years totals for the Sumner County PILOT filings, computed twice.

Pass A reads sumner-pilot.json.

Pass B re-extracts from the source documents down a different path: the PDFs are
read as `pdftotext -layout` character grid (not word coordinates), the blocks are
found by line text (not geometry), and the .ods is read as raw cell text. It never
touches the JSON.

Totals that agree across both confirm the extraction; totals that disagree name the
year and column where the two paths read the documents differently.
"""

import json
import re
import subprocess
import zipfile
from collections import defaultdict
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent.parent
DIR = ROOT / "state_of_tennessee" / "tn_comptroller_pilot_reports" / "sumner_county"
COLS = ["est_value", "rent", "pilot_city", "pilot_county", "leasehold_tax"]
LABELS = {"est_value": "Est. value", "rent": "Rent", "pilot_city": "PILOT city",
          "pilot_county": "PILOT county", "leasehold_tax": "L/H tax"}

MONEY = re.compile(r"\$[\d,]+(?:\.\d\d)?")


def usd(s):
    return int(round(float(s.replace("$", "").replace(",", ""))))


# ---------------------------------------------------------------- pass A

def from_json():
    data = json.loads((DIR / "derived" / "sumner-pilot.json").read_text())
    tot = defaultdict(lambda: defaultdict(int))
    rows = defaultdict(int)
    values = defaultdict(list)
    for r in data:
        y = r["report_year"]
        rows[y] += 1
        for c in COLS:
            v = r["amounts"][c]["usd"]
            if v is not None:
                tot[y][c] += v
                values[y].append(v)
    return tot, rows, values


# ---------------------------------------------------------------- pass B

def pdf_block_lines(year):
    """Sumner's lines from the character-grid rendering, found by line text."""
    txt = subprocess.run(["pdftotext", "-layout", str(DIR / f"{year}-pilot-sumner.pdf"), "-"],
                         capture_output=True, text=True, check=True).stdout
    lines = txt.splitlines()
    if year == 2015:                       # no county names; Sumner is code 83
        return [l for l in lines if re.match(r"\s*\d{1,2}/\d{1,2}/\d{4}\s+83\s", l)]
    out, inblock = [], False
    county = re.compile(r"^\s*([A-Z][a-z]+(?: [A-Z][a-z]+)?)\s")
    for line in lines:
        m = county.match(line)
        name = m.group(1) if m else None
        if name == "Sumner":
            inblock = True
            out.append(line)
            continue
        if inblock:
            if name and name != "Sumner" and name not in ("Revised",):
                break
            if line.strip():
                out.append(line)
    return out


def ods_rows():
    T = "{urn:oasis:names:tc:opendocument:xmlns:table:1.0}"
    root = ET.fromstring(zipfile.ZipFile(
        DIR / "2023-2025-pilot-sumner.ods").read("content.xml"))
    year, out = None, []
    for r in root.iter(T + "table-row"):
        cells = []
        for c in r.findall(T + "table-cell"):
            rep = int(c.get(T + "number-columns-repeated", 1))
            cells += ["".join(c.itertext())] * (1 if rep > 100 else rep)
        if not any(c.strip() for c in cells):
            continue
        if re.fullmatch(r"20\d\d", cells[0].strip()):
            year = int(cells[0])
            continue
        if any(h in cells for h in ("LESSEE NAME", "Lessee")):
            continue
        if year:
            out.append((year, cells))
    return out


def from_sources():
    """Every money value in each year's Sumner block, by position in the row."""
    tot = defaultdict(lambda: defaultdict(int))
    rows = defaultdict(int)
    values = defaultdict(list)

    for year in range(2015, 2023):
        for line in pdf_block_lines(year):
            # count filing rows by their date, not by money: a filer can leave
            # every dollar column blank (Gallatin SLP's personal property does)
            if not re.search(r"\d{1,2}/\d{1,2}/\d{4}", line):
                continue
            rows[year] += 1
            values[year] += [usd(v) for v in MONEY.findall(line)]

    for year, cells in ods_rows():
        rows[year] += 1
        for i, c in zip(range(12, 17), COLS):
            if i < len(cells) and MONEY.fullmatch(cells[i].strip()):
                tot[year][c] += usd(cells[i])
                values[year].append(usd(cells[i]))
    return tot, rows, values


# ----------------------------------------------------------------

def money_fmt(n):
    return f"${n:,}" if n else "-"


def main():
    ta, ra, va = from_json()
    tb, rb, vb = from_sources()
    years = sorted(ra)

    w = 14
    print("\nSUMNER COUNTY PILOT FILINGS, 2015-2025")
    print("=" * (8 + 6 + w * 5))
    print(f"{'Year':<6}{'Rows':>5}  " + "".join(f"{LABELS[c]:>{w}}" for c in COLS))
    print("-" * (8 + 6 + w * 5))
    grand = defaultdict(int)
    for y in years:
        print(f"{y:<6}{ra[y]:>5}  " +
              "".join(f"{money_fmt(ta[y][c]):>{w}}" for c in COLS))
        for c in COLS:
            grand[c] += ta[y][c]
    print("-" * (8 + 6 + w * 5))
    print(f"{'ALL':<6}{sum(ra.values()):>5}  " +
          "".join(f"{money_fmt(grand[c]):>{w}}" for c in COLS))

    print("\n\nCROSS-CHECK  (json vs. an independent read of the sources)")
    print("=" * 62)
    ok = True
    for y in years:
        # row counts
        note = []
        if ra[y] != rb[y]:
            note.append(f"rows {ra[y]} vs {rb[y]}")
        # the multiset of money values, ignoring which column they landed in
        if sorted(va[y]) != sorted(vb[y]):
            only_a = sorted(set(va[y]) - set(vb[y]))
            only_b = sorted(set(vb[y]) - set(va[y]))
            note.append(f"values differ (json-only {only_a[:3]}, "
                        f"source-only {only_b[:3]})")
        # per-column totals, where pass B could resolve columns (the .ods years)
        if tb[y]:
            for c in COLS:
                if ta[y][c] != tb[y][c]:
                    note.append(f"{c}: {ta[y][c]:,} vs {tb[y][c]:,}")
        if note:
            ok = False
            print(f"  {y}  MISMATCH  " + "; ".join(note))
        else:
            scope = "values + columns" if tb[y] else "values"
            print(f"  {y}  ok        {ra[y]} rows, {len(va[y])} amounts ({scope})")
    print("=" * 62)
    print("ALL AGREE" if ok else "DISAGREEMENTS ABOVE - resolve before quoting")


if __name__ == "__main__":
    main()
