#!/usr/bin/env python3
"""Check gallatin-idb-990.json without trusting the transcription that made it.

Four of the five filings are image-only PDFs and this machine has no OCR, so the
dataset is a transcription, not a parse. That is the weakness these passes are
built around:

  A  internal arithmetic   each filing's own lines must close
  B  cross-year chain      end-of-year net assets must equal the next year's
                           beginning, across all five filings
  C  restatement check     each filing's stated prior-year figures against what
                           the prior filing itself reported
  D  text layer            2024 only, mechanically re-read from the PDF

Pass B is the strong one: it spans five separately transcribed documents, so a
single mistyped digit anywhere in the chain breaks it.

Run with:  python3 bin/verify-990.py
"""

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
HERE = ROOT / "usa_federal" / "irs_990_data" / "gallatin_idb"
DATA = HERE / "gallatin-idb-990.json"


def check(results, name, got, want):
    ok = got == want
    results.append((ok, f"{name}: {got}" if ok else f"{name}: {got} vs expected {want}"))


def pass_a(rec, results):
    """The filing's own arithmetic."""
    y = rec["filing_year"]
    rev, exp = rec["revenue"], rec["expenses"]

    items = [i["amount"] for i in (rev.get("itemization") or []) if i.get("amount")]
    if items:
        check(results, f"{y} revenue itemization sums to total", sum(items), rev["total"])

    items = [i["amount"] for i in (exp.get("itemization") or []) if i.get("amount")]
    if items:
        # The 990-EZ itemises only line 16; the full 990 itemises everything.
        target = exp.get("other_expenses", exp["total"])
        label = "other expenses" if "other_expenses" in exp else "total"
        check(results, f"{y} expense itemization sums to {label}", sum(items), target)

    if exp.get("program_service") is not None and exp.get("management_and_general") is not None:
        check(results, f"{y} expense columns sum to total",
              exp["program_service"] + exp["management_and_general"] + (exp.get("fundraising") or 0),
              exp["total"])

    na = rec["net_assets"]
    check(results, f"{y} revenue less expenses", rev["total"] - exp["total"],
          na["revenue_less_expenses"])

    rolled = (na["beginning"] + na["revenue_less_expenses"]
              + (na.get("prior_period_adjustments") or 0)
              + (na.get("other_changes") or 0))
    check(results, f"{y} net assets roll to end-of-year", rolled, na["end"])


def pass_b(records, results):
    """The chain across filings."""
    for prev, nxt in zip(records, records[1:]):
        check(results,
              f"{prev['filing_year']} end -> {nxt['filing_year']} beginning",
              prev["net_assets"]["end"], nxt["net_assets"]["beginning"])


def pass_c(records, results):
    """Prior-year columns against what the prior filing actually said.

    Reported as findings rather than failures: a restatement is the filer's
    doing, not a transcription error.
    """
    notes = []
    for prev, nxt in zip(records, records[1:]):
        stated = nxt.get("prior_year_reported")
        if not stated:
            continue
        for key, label in (("total_revenue", "revenue"), ("total_expenses", "expenses")):
            if key in stated:
                actual = (prev["revenue"]["total"] if key == "total_revenue"
                          else prev["expenses"]["total"])
                if stated[key] != actual:
                    notes.append(
                        f"{nxt['filing_year']} restates {prev['filing_year']} {label} "
                        f"as {stated[key]:,}; that filing reported {actual:,}")
    return notes


def pass_d(records, results):
    """2024 has a text layer, so re-read it mechanically."""
    rec = next((r for r in records if r["source"].get("text_layer")), None)
    if not rec:
        return
    pdf = HERE / rec["source"]["file"]
    t = subprocess.run(["pdftotext", "-layout", str(pdf), "-"],
                       capture_output=True, text=True, check=True).stdout
    t = re.sub(r"\s+", " ", t).upper()

    for label, amount in [(i["label"], i["amount"]) for i in rec["revenue"]["itemization"]
                          + rec["expenses"]["itemization"] if i.get("amount")]:
        near = r".{0,80}?"
        found = bool(re.search(re.escape(label.upper()) + near + f"{amount:,}", t)) or \
                bool(re.search(f"{amount:,}" + near + re.escape(label.upper()), t))
        check(results, f"2024 text layer confirms {label} = {amount:,}", found, True)

    check(results, "2024 text layer confirms total revenue",
          f"{rec['revenue']['total']:,}" in t, True)
    check(results, "2024 text layer confirms total expenses",
          f"{rec['expenses']['total']:,}" in t, True)
    check(results, "2024 text layer confirms name as filed",
          rec["identity"]["name_as_filed"].upper() in t, True)


def main():
    records = sorted(json.loads(DATA.read_text()), key=lambda r: r["filing_year"])
    results = []

    print("Pass A  internal arithmetic")
    for rec in records:
        pass_a(rec, results)
    report(results)

    print("\nPass B  cross-year net-asset chain")
    b = []
    pass_b(records, b)
    report(b)
    results += b

    print("\nPass C  prior-year restatements")
    for n in pass_c(records, results):
        print(f"  finding  {n}")

    print("\nPass D  2024 text layer")
    d = []
    pass_d(records, d)
    report(d)
    results += d

    print("\n" + "=" * 72)
    print(f"{'Year':<6}{'Form':<8}{'Revenue':>14}{'Expenses':>14}{'Net assets end':>18}")
    for r in records:
        print(f"{r['filing_year']:<6}{r['form']:<8}{r['revenue']['total']:>14,}"
              f"{r['expenses']['total']:>14,}{r['net_assets']['end']:>18,}")
    pilot_in = sum(i["amount"] or 0 for r in records for i in (r["revenue"]["itemization"] or [])
                   if "PILOT" in i["label"].upper() or "Pilot" in i["label"])
    schools = sum(i["amount"] for r in records for i in r["expenses"]["itemization"]
                  if "SCHOOL" in i["label"].upper())
    print(f"\nPILOT revenue across all filings: ${pilot_in:,}")
    print(f"Paid to Sumner County Schools:    ${schools:,}")

    bad = [m for ok, m in results if not ok]
    print("\n" + ("ALL CHECKS AGREE" if not bad else f"{len(bad)} MISMATCHES"))
    for m in bad:
        print(f"  MISMATCH  {m}")
    return 1 if bad else 0


def report(results):
    bad = [m for ok, m in results if not ok]
    print(f"  {len(results) - len(bad)}/{len(results)} checks agree")
    for m in bad:
        print(f"      MISMATCH  {m}")


if __name__ == "__main__":
    sys.exit(main())
