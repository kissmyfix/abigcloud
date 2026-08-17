#!/usr/bin/env python3
"""Check sumner-assessments.json against the source PDFs three independent ways.

None of the passes import the parser or share its code path:

  A  flowed text     pdftotext -layout, read by line shape, not by coordinate
  B  raw stream      pdftotext -raw, every money string and date as a multiset
  C  internal maths  the report's own arithmetic must close

Then a fourth condition: an all-parcels roll-up, recounted from the raw text.

Run with:  python3 files/bin/verify-assessments.py
"""

import collections
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
HERE = ROOT / "state_of_tennessee" / "tn_property_assessments"
DATA = HERE / "derived" / "sumner-assessments.json"


def text(pdf, mode):
    return subprocess.run(["pdftotext", mode, str(pdf), "-"],
                          capture_output=True, text=True, check=True).stdout


def bag(items=()):
    return collections.Counter(items)


def diff(name, got, want):
    """Returns (ok, message)."""
    if got == want:
        return True, f"{name}: {sum(want.values()) if isinstance(want, collections.Counter) else want}"
    if isinstance(want, collections.Counter):
        missing = want - got
        extra = got - want
        bits = []
        if missing:
            bits.append(f"in PDF not JSON {dict(missing)}")
        if extra:
            bits.append(f"in JSON not PDF {dict(extra)}")
        return False, f"{name}: " + "; ".join(bits)
    return False, f"{name}: PDF {want!r} vs JSON {got!r}"


# ----------------------------------------------------------------- pass A

VALUE_LINE = re.compile(r"^(Land Market Value|Improvement Value|Total Market Appraisal|"
                        r"Assessment Percentage|Assessment):\s+(\S+)", re.M)
SALE_LINE = re.compile(
    r"^\s*(\d{1,2}/\d{1,2}/\d{4})\s+(\$[\d,]+)\s+(\S+)\s+(\d+)\s+([VI] - \w+)", re.M)


def pass_a(pdf, rec):
    """Read the flowed text by line shape and compare the headline facts."""
    t = text(pdf, "-layout")
    checks = []

    vals = dict(VALUE_LINE.findall(t))
    for key, label in (("land_market", "Land Market Value"),
                       ("improvement", "Improvement Value"),
                       ("total_market_appraisal", "Total Market Appraisal"),
                       ("assessment", "Assessment")):
        checks.append(diff(label, rec["value"][key]["raw"], vals.get(label)))
    checks.append(diff("Assessment Percentage",
                       rec["value"]["assessment_percentage"]["raw"],
                       vals.get("Assessment Percentage")))

    m = re.search(r"Tax Year (\d{4}) \| Reappraisal (\d{4})", t)
    checks.append(diff("Tax year", rec["tax_year"], int(m.group(1))))
    checks.append(diff("Reappraisal", rec["reappraisal_year"], int(m.group(2))))

    m = re.search(r"Calculated Acres:\s+([\d.]+)", t)
    checks.append(diff("Calculated acres", rec["land"]["calculated_acres"],
                       float(m.group(1))))

    m = re.search(r"Number of Buildings:\s*(\d+)", t)
    checks.append(diff("Declared buildings", rec["general"]["number_of_buildings"],
                       int(m.group(1))))

    nums = sorted(int(n) for n in re.findall(r"Commercial Building #: (\d+)", t))
    checks.append(diff("Building numbers", sorted(b["building"] for b in rec["buildings"]),
                       nums))

    # Sale rows are full width, so the flowed text renders them faithfully.
    sales = SALE_LINE.findall(t)
    checks.append(diff("Sale rows", len(rec["sales"]), len(sales)))
    checks.append(diff(
        "Sale date/price pairs",
        bag((s["date_raw"], s["price"]["raw"]) for s in rec["sales"]),
        bag((d, p) for d, p, _b, _pg, _vi in sales)))
    checks.append(diff(
        "Sale book/page pairs",
        bag((s["book"], s["page"]) for s in rec["sales"]),
        bag((b, pg) for _d, _p, b, pg, _vi in sales)))
    return checks


# ----------------------------------------------------------------- pass B

def pass_b(pdf, rec):
    """Multisets off the raw stream: nothing dropped, duplicated or invented."""
    t = text(pdf, "-raw")
    checks = []

    pdf_money = bag(re.findall(r"\$[\d,]+(?:\.\d{2})?", t))
    json_money = bag(
        [rec["value"][k]["raw"] for k in
         ("land_market", "improvement", "total_market_appraisal", "assessment")]
        + [s["price"]["raw"] for s in rec["sales"]]
    )
    checks.append(diff("Money strings", json_money, pdf_money))

    pdf_dates = bag(re.findall(r"\b\d{1,2}/\d{1,2}/\d{4}\b", t))
    checks.append(diff("Date strings", bag(s["date_raw"] for s in rec["sales"]),
                       pdf_dates))

    # Every square-foot figure the report prints, wherever it prints it.
    pdf_sqft = bag(re.findall(r"\b\d{1,3}(?:,\d{3})+\b", t))
    json_sqft = bag(
        [f"{a['square_feet']:,}" for b in rec["buildings"] for a in b["areas"]
         if a["square_feet"] and a["square_feet"] >= 1000]
        + [f"{o['area_units']:,}" for o in rec["outbuildings"]
           if o["area_units"] and o["area_units"] >= 1000]
    )
    # The same comma-grouped pattern also matches book numbers and feature units,
    # so only assert that no JSON figure is absent from the source.
    checks.append(diff("Comma-grouped figures present in source",
                       bag(), json_sqft - pdf_sqft))
    return checks


# ----------------------------------------------------------------- pass C

def pass_c(pdf, rec):
    """The report's own arithmetic, checked without looking at the PDF at all."""
    checks = []
    v = rec["value"]
    checks.append(diff(
        "Land + improvement = total appraisal",
        v["total_market_appraisal"]["usd"],
        (v["land_market"]["usd"] or 0) + (v["improvement"]["usd"] or 0)))

    pct = v["assessment_percentage"]["pct"]
    if pct is not None:
        checks.append(diff(
            "Total x assessment % = assessment",
            v["assessment"]["usd"],
            int(round((v["total_market_appraisal"]["usd"] or 0) * pct / 100))))

    checks.append(diff("Land code units = total land units",
                       rec["land"]["total_land_units"],
                       round(sum(c["units"] or 0 for c in rec["land"]["codes"]), 2)))

    checks.append(diff("Buildings parsed = buildings declared",
                       len(rec["buildings"]),
                       rec["general"]["number_of_buildings"] or 0))

    for b in rec["buildings"]:
        checks.append(diff(
            f"Building {b['building']}: areas sum = business living area",
            b["business_living_area"],
            sum(a["square_feet"] or 0 for a in b["areas"])))
    return checks


# ----------------------------------------------------------------- pass D

# A second, independently produced rendering of the same parcel: the state site
# printed from Firefox, against the county viewer printed from Chromium. Nothing
# about its layout is shared with the reports the parser reads.
CROSS_SOURCE = {"112 10900 000": "sumner-assessment-bradford-confirmed.pdf"}

ALT_SALE = re.compile(r"(\d{1,2}/\d{1,2}/\d{4})\s+(\$[\d,]+)\s+(\d+)\s+(\d+)")


def pass_d(rec):
    """Same facts, different document, different renderer, different publisher."""
    alt = HERE / CROSS_SOURCE[rec["parcel_id"]]
    t = text(alt, "-layout")
    checks = []

    for key, label in (("land_market", "Land Market Value"),
                       ("improvement", "Improvement Value"),
                       ("total_market_appraisal", "Total Market Appraisal"),
                       ("assessment", "Assessment")):
        m = re.search(rf"{label}:\s+(\$[\d,]+)", t)
        checks.append(diff(label, rec["value"][key]["raw"],
                           m.group(1) if m else None))

    m = re.search(r"Assessment Percentage:\s+(\d+%)", t)
    checks.append(diff("Assessment Percentage",
                       rec["value"]["assessment_percentage"]["raw"],
                       m.group(1) if m else None))

    m = re.search(r"Total Land Units:\s+([\d.]+)", t)
    checks.append(diff("Total land units", rec["land"]["total_land_units"],
                       float(m.group(1))))

    m = re.search(r"Business Living Area:\s+(\d+)", t)
    checks.append(diff("Business living area",
                       rec["buildings"][0]["business_living_area"], int(m.group(1))))

    sales = ALT_SALE.findall(t)
    checks.append(diff(
        "Sale date/price/book/page",
        bag((s["date_raw"], s["price"]["raw"], s["book"], s["page"])
            for s in rec["sales"]),
        bag(sales)))
    return checks


# -------------------------------------------------------------------- main

def main():
    records = json.loads(DATA.read_text())
    by_file = {}
    for r in records:
        by_file[r["source"]["file"]] = r
        for dup in r["source"].get("duplicate_files", []):
            by_file[dup] = r

    failures = 0
    cross = set(CROSS_SOURCE.values())
    for pdf in sorted(HERE.glob("*.pdf")):
        if pdf.name in cross:
            continue
        rec = by_file.get(pdf.name)
        if rec is None:
            print(f"{pdf.name}: NO RECORD")
            failures += 1
            continue
        dup = "  (duplicate of %s)" % rec["source"]["file"] if pdf.name != rec["source"]["file"] else ""
        print(f"\n{pdf.name}  ->  {rec['parcel_id']}{dup}")
        for label, fn in (("A flowed text", pass_a), ("B raw stream", pass_b),
                          ("C internal maths", pass_c)):
            results = fn(pdf, rec)
            bad = [m for ok, m in results if not ok]
            failures += len(bad)
            print(f"  {label:<18} {len(results) - len(bad)}/{len(results)} checks agree")
            for m in bad:
                print(f"      MISMATCH  {m}")
        if rec["parcel_id"] in CROSS_SOURCE and pdf.name == rec["source"]["file"]:
            results = pass_d(rec)
            bad = [m for ok, m in results if not ok]
            failures += len(bad)
            print(f"  {'D cross-source':<18} {len(results) - len(bad)}/{len(results)}"
                  f" checks agree  ({CROSS_SOURCE[rec['parcel_id']]})")
            for m in bad:
                print(f"      MISMATCH  {m}")

    print("\n" + "=" * 74)
    print("All-parcels roll-up")
    print("=" * 74)
    hdr = f"{'Parcel':<15}{'Situs':<22}{'Appraisal':>15}{'Acres':>10}{'Bldg sqft':>12}{'Sales':>7}"
    print(hdr)
    tot = collections.Counter()
    for r in sorted(records, key=lambda r: -(r["value"]["total_market_appraisal"]["usd"] or 0)):
        sqft = sum(b["business_living_area"] or 0 for b in r["buildings"])
        acres = r["land"]["total_land_units"] or 0
        appr = r["value"]["total_market_appraisal"]["usd"] or 0
        print(f"{r['parcel_id']:<15}{r['situs_address']:<22}{appr:>15,}"
              f"{acres:>10,.2f}{sqft:>12,}{len(r['sales']):>7}")
        tot["appraisal"] += appr
        tot["acres"] += acres
        tot["sqft"] += sqft
        tot["sales"] += len(r["sales"])
        tot["outb"] += len(r["outbuildings"])
        tot["bldg"] += len(r["buildings"])
    print(f"{'TOTAL':<15}{'':<22}{tot['appraisal']:>15,}{tot['acres']:>10,.2f}"
          f"{tot['sqft']:>12,}{tot['sales']:>7}")
    print(f"{tot['bldg']} commercial buildings, {tot['outb']} outbuilding & yard items")

    # Fourth condition: recount the roll-up straight from the source text, by a
    # route that touches none of the per-parcel passes above.
    seen, recount = set(), collections.Counter()
    for pdf in sorted(HERE.glob("*.pdf")):
        if pdf.name in cross:
            continue
        t = text(pdf, "-layout")
        m = re.search(r"Total Market Appraisal:\s+\$([\d,]+)", t)
        appr = int(m.group(1).replace(",", ""))
        acres = float(re.search(r"Total Land Units:\s+([\d.]+)", t).group(1))
        ident = (appr, acres, len(t))
        if ident in seen:          # the duplicate file
            continue
        seen.add(ident)
        recount["appraisal"] += appr
        recount["acres"] += acres
        recount["sales"] += len(SALE_LINE.findall(t))
        recount["bldg"] += len(re.findall(r"Commercial Building #: \d+", t))

    print()
    ok = True
    for k in ("appraisal", "acres", "sales", "bldg"):
        good = round(tot[k], 2) == round(recount[k], 2)
        ok &= good
        print(f"  roll-up {k:<10} {'agrees' if good else 'MISMATCH'}"
              f"   dataset {tot[k]:,.2f}  recount {recount[k]:,.2f}")
    failures += 0 if ok else 1

    print("\n" + ("ALL PASSES AGREE" if failures == 0 else f"{failures} MISMATCHES"))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
