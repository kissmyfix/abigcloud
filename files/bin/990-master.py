#!/usr/bin/env python3
"""Aggregate a directory of IRS 990 XML filings into one master XML, then render it.

The IRS renamed most elements around tax year 2016 (TotalRevenueCurrentYear became
CYTotalRevenueAmt, and so on), so every field here carries both spellings and takes
whichever the filing actually used. A field that is genuinely absent stays empty
rather than becoming a zero, because a blank and an explicit zero are different
findings.

Usage: 990-master.py <dir-of-xml> [-o master.xml] [--html page.html]
"""

import argparse
import glob
import os
import re
import xml.etree.ElementTree as ET
from html import escape

# field -> the element names it has gone by, newest first.
FIELDS = {
    "contributions":      ["CYContributionsGrantsAmt", "ContributionsGrantsCurrentYear"],
    "program_revenue":    ["CYProgramServiceRevenueAmt", "ProgramServiceRevenueCY"],
    "investment_income":  ["CYInvestmentIncomeAmt", "InvestmentIncomeCurrentYear"],
    "other_revenue":      ["CYOtherRevenueAmt", "OtherRevenueCurrentYear"],
    "total_revenue":      ["CYTotalRevenueAmt", "TotalRevenueCurrentYear"],
    "grants_paid":        ["CYGrantsAndSimilarPaidAmt", "GrantsAndSimilarAmntsCY"],
    "salaries":           ["CYSalariesCompEmpBnftPaidAmt", "SalariesEtcCurrentYear"],
    "total_expenses":     ["CYTotalExpensesAmt", "TotalExpensesCurrentYear"],
    "revenue_less_exp":   ["CYRevenuesLessExpensesAmt", "RevenuesLessExpensesCY"],
    "total_assets":       ["TotalAssetsEOYAmt", "TotalAssetsEOY"],
    "total_liabilities":  ["TotalLiabilitiesEOYAmt", "TotalLiabilitiesEOY"],
    "net_assets":         ["NetAssetsOrFundBalancesEOYAmt", "NetAssetsOrFundBalancesEOY"],
    "net_assets_boy":     ["NetAssetsOrFundBalancesBOYAmt", "NetAssetsOrFundBalancesBOY"],
    "land_bldg_net":      ["LandBldgEquipCostNetAmt", "LandBuildingsEquipmentBasisNet"],
    "mortgage":           ["MortgNotesPyblSecuredInvstAmt", "MortNotesPyblSecuredInvestProp"],
    "unrestricted":       ["UnrestrictedNetAssetsAmt", "UnrestrictedNetAssets"],
    "restricted_temp":    ["TemporarilyRstrNetAssetsAmt", "TemporarilyRestrictedNetAssets"],
    "government_grants":  ["GovernmentGrantsAmt"],
    "other_changes":      ["OtherChangesInNetAssetsAmt", "ReconcilationOtherChanges"],
    "employees":          ["TotalEmployeeCnt", "TotalNbrEmployees"],
    "volunteers":         ["TotalVolunteersCnt", "TotalNbrVolunteers"],
    "voting_members":     ["VotingMembersGoverningBodyCnt", "NbrVotingMembersGoverningBody"],
    # Yes/No answers that matter more than most dollar figures.
    "grants_gt_5k_to_org": ["GrantsToOrganizationsInd", "MoreThan5000KToOrganizations"],
    "noncash_gt_25k":      ["DeductibleNonCashContributions", "NoncashContributionsInd"],
    "audited":             ["FSAuditedInd", "FSAudited", "IndependentAuditFinancialStmt"],
}

MONEY = {"contributions", "program_revenue", "investment_income", "other_revenue",
         "total_revenue", "grants_paid", "salaries", "total_expenses", "revenue_less_exp",
         "total_assets", "total_liabilities", "net_assets", "net_assets_boy",
         "land_bldg_net", "mortgage", "unrestricted", "restricted_temp",
         "government_grants", "other_changes"}


def strip_ns(root):
    for el in root.iter():
        if "}" in el.tag:
            el.tag = el.tag.split("}", 1)[1]
    return root


def find_first(root, names):
    for n in names:
        el = root.find(f".//{n}")
        if el is not None and (el.text or "").strip():
            return el.text.strip()
    return ""


def officers(root):
    out = []
    for grp in root.iter():
        if grp.tag not in ("Form990PartVIISectionAGrp", "Form990PartVIISectionA"):
            continue
        name = ""
        for t in ("PersonNm", "PersonName", "NamePerson"):
            el = grp.find(t)
            if el is not None and el.text:
                name = el.text.strip(); break
        title = ""
        for t in ("TitleTxt", "Title"):
            el = grp.find(t)
            if el is not None and el.text:
                title = el.text.strip(); break
        comp = ""
        for t in ("ReportableCompFromOrgAmt", "CompensationAmount"):
            el = grp.find(t)
            if el is not None and el.text:
                comp = el.text.strip(); break
        if name:
            out.append((name, title, comp))
    return out


def parse(path):
    root = strip_ns(ET.parse(path).getroot())
    rec = {"file": os.path.basename(path)}
    rec["period_end"] = find_first(root, ["TaxPeriodEndDt", "TaxPeriodEndDate"])
    rec["fy"] = rec["period_end"][:4] if rec["period_end"] else ""
    rec["derived"] = root.get("returnVersion", "").startswith("DERIVED")
    for k, names in FIELDS.items():
        rec[k] = find_first(root, names)
    rec["officers"] = officers(root)
    return rec


def build_master(records, out):
    r = ET.Element("ShalomZoneMaster")
    ET.SubElement(r, "Note").text = (
        "Aggregated from the per-year filings in this directory. Values are copied "
        "verbatim from each return; nothing is computed except the deltas marked "
        "computed=\"true\". A blank field means the filing did not report it.")
    yrs = ET.SubElement(r, "Years")
    prev = None
    for rec in records:
        y = ET.SubElement(yrs, "Year", fy=rec["fy"], periodEnd=rec["period_end"],
                          source="derived-ocr" if rec["derived"] else "irs-efile-xml")
        for k in FIELDS:
            if rec[k] != "":
                ET.SubElement(y, k).text = rec[k]
        # The gap between what operations produced and what the balance sheet did.
        try:
            boy, eoy, rle = (int(rec["net_assets_boy"]), int(rec["net_assets"]),
                             int(rec["revenue_less_exp"]))
            ET.SubElement(y, "unexplained_change", computed="true").text = str(eoy - boy - rle)
        except (ValueError, TypeError):
            pass
        offs = ET.SubElement(y, "officers")
        for n, t, c in rec["officers"]:
            ET.SubElement(offs, "officer", name=n, title=t, comp=c)
        prev = rec
    ET.indent(r, space="  ")
    ET.ElementTree(r).write(out, encoding="utf-8", xml_declaration=True)


def fmt(v, money):
    if v == "":
        return "—"
    if money:
        try:
            n = int(v)
            return ("-$" if n < 0 else "$") + f"{abs(n):,}"
        except ValueError:
            return v
    if v in ("true", "false"):
        return "Yes" if v == "true" else "No"
    return v


ROWS = [
    ("Revenue", None),
    ("Contributions and grants", "contributions"),
    ("Government grants", "government_grants"),
    ("Program service revenue", "program_revenue"),
    ("Investment income", "investment_income"),
    ("Other revenue", "other_revenue"),
    ("TOTAL REVENUE", "total_revenue"),
    ("Expenses", None),
    ("Salaries and benefits", "salaries"),
    ("Grants paid out", "grants_paid"),
    ("TOTAL EXPENSES", "total_expenses"),
    ("Revenue less expenses", "revenue_less_exp"),
    ("Balance sheet", None),
    ("Land, buildings, equipment (net)", "land_bldg_net"),
    ("Total assets", "total_assets"),
    ("Mortgage payable", "mortgage"),
    ("Total liabilities", "total_liabilities"),
    ("Net assets, start of year", "net_assets_boy"),
    ("Net assets, end of year", "net_assets"),
    ("Unrestricted", "unrestricted"),
    ("Temporarily restricted", "restricted_temp"),
    ("Answers and counts", None),
    ("Gave any org more than $5,000?", "grants_gt_5k_to_org"),
    ("Received non-cash gifts over $25k?", "noncash_gt_25k"),
    ("Financial statements audited?", "audited"),
    ("Employees", "employees"),
    ("Volunteers", "volunteers"),
    ("Voting board members", "voting_members"),
]


def build_html(records, out):
    years = [r["fy"] for r in records]
    # Per-year panel
    panels = []
    for r in records:
        rows = []
        for label, key in ROWS:
            if key is None:
                rows.append(f'<tr class="sec"><td colspan="3">{escape(label)}</td></tr>')
                continue
            v = fmt(r[key], key in MONEY)
            cls = ""
            if key == "grants_paid" and r[key] not in ("", "0"):
                cls = "hot"
            if key == "grants_gt_5k_to_org" and r[key] == "false" and r["grants_paid"] not in ("", "0"):
                cls = "hot"
            rows.append(f'<tr class="{cls}"><td>{escape(label)}</td><td class="v">{escape(v)}</td><td></td></tr>')
        try:
            gap = int(r["net_assets"]) - int(r["net_assets_boy"]) - int(r["revenue_less_exp"])
        except (ValueError, TypeError):
            gap = None
        gaphtml = ""
        if gap:
            gaphtml = (f'<div class="gap">Balance sheet moved {fmt(str(gap), True)} more than '
                       f'operations explain.</div>')
        offs = "".join(
            f"<li><b>{escape(n)}</b> <span>{escape(t)}</span>"
            + (f' <em>{fmt(c, True)}</em>' if c and c != "0" else "") + "</li>"
            for n, t, c in r["officers"]) or "<li class='none'>No officers listed on this return.</li>"
        src = ("Derived from an OCR'd scan, not an IRS release"
               if r["derived"] else "IRS e-file XML")
        panels.append(f"""<section class="panel" id="fy{r['fy']}">
  <h2>Fiscal year ending {escape(r['period_end'] or r['fy'])}</h2>
  <p class="src">{escape(src)} &middot; {escape(r['file'])}</p>
  {gaphtml}
  <div class="cols">
    <table>{''.join(rows)}</table>
    <div class="people"><h3>Officers and directors</h3><ul>{offs}</ul></div>
  </div>
</section>""")

    # Trend table across all years
    trend_keys = [("Total revenue", "total_revenue"), ("Total expenses", "total_expenses"),
                  ("Net assets", "net_assets"), ("Grants paid out", "grants_paid")]
    head = "".join(f"<th>{y}</th>" for y in years)
    trows = []
    for label, key in trend_keys:
        cells = "".join(
            f'<td class="{"hot" if key=="grants_paid" and r[key] not in ("","0") else ""}">{fmt(r[key], True)}</td>'
            for r in records)
        trows.append(f"<tr><th>{label}</th>{cells}</tr>")

    nav = "".join(f'<button data-y="{y}">{y}</button>' for y in years)

    html = f"""<!doctype html>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Gallatin Shalom Zone — filings</title>
<style>
:root{{--bg:#edeae1;--bg2:#e3dfd5;--ink:#1a1814;--ink2:#4a4640;--ink3:#807b74;
--accent:#c8410a;--teal:#0e6b5c;--gold:#b5890c;--border:rgba(26,24,20,.14);}}
@media(prefers-color-scheme:dark){{:root{{--bg:#232019;--bg2:#2c2820;--ink:#f0ece3;
--ink2:#c8c2b8;--ink3:#8a8278;--accent:#e8691a;--teal:#22a08a;--gold:#d4a820;
--border:rgba(240,236,227,.12);}}}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--ink);
font:15px/1.5 'DM Sans',system-ui,sans-serif;-webkit-font-smoothing:antialiased}}
header{{padding:28px 24px 0;max-width:1100px;margin:0 auto}}
h1{{font-family:'DM Serif Display',Georgia,serif;font-weight:400;font-size:32px;margin:0 0 4px}}
header p{{color:var(--ink3);margin:0 0 18px;font-size:14px}}
nav{{position:sticky;top:0;background:var(--bg);padding:10px 24px;border-bottom:1px solid var(--border);
z-index:5;display:flex;gap:4px;flex-wrap:wrap;justify-content:center}}
nav button{{font:600 13px/1 'DM Sans',system-ui,sans-serif;padding:8px 11px;border:1px solid var(--border);
background:var(--bg2);color:var(--ink2);border-radius:6px;cursor:pointer}}
nav button.on{{background:var(--accent);color:#fff;border-color:var(--accent)}}
main{{max-width:1100px;margin:0 auto;padding:24px}}
.panel{{display:none}} .panel.on{{display:block}}
.panel h2{{font-family:'DM Serif Display',Georgia,serif;font-weight:400;font-size:26px;margin:0 0 2px}}
.src{{color:var(--ink3);font-size:12px;margin:0 0 16px}}
.gap{{background:var(--bg2);border-left:3px solid var(--gold);padding:10px 14px;
border-radius:0 6px 6px 0;margin:0 0 16px;font-size:14px;color:var(--ink2)}}
.cols{{display:grid;grid-template-columns:1fr 300px;gap:26px}}
@media(max-width:820px){{.cols{{grid-template-columns:1fr}}}}
table{{width:100%;border-collapse:collapse;font-size:14px}}
td,th{{padding:5px 8px;border-bottom:1px solid var(--border);text-align:left}}
td.v{{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}}
tr.sec td{{background:var(--bg2);font-size:11px;letter-spacing:.12em;text-transform:uppercase;
font-weight:700;color:var(--ink3);border-bottom:none;padding-top:14px}}
tr.hot td,td.hot{{background:rgba(200,65,10,.10);font-weight:600}}
.people h3{{font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:var(--ink3);margin:0 0 8px}}
.people ul{{list-style:none;padding:0;margin:0;font-size:13px}}
.people li{{padding:5px 0;border-bottom:1px solid var(--border)}}
.people span{{color:var(--ink3)}} .people em{{color:var(--accent);font-style:normal;font-weight:600}}
.people li.none{{color:var(--ink3);font-style:italic}}
.trend{{margin-top:34px;overflow-x:auto}}
.trend h3{{font-family:'DM Serif Display',Georgia,serif;font-weight:400;font-size:20px;margin:0 0 8px}}
.trend table{{min-width:900px;font-size:13px}}
.trend th:first-child{{white-space:nowrap}}
.trend td{{text-align:right;font-variant-numeric:tabular-nums}}
</style>
<header>
  <h1>Gallatin Shalom Zone</h1>
  <p>EIN 62-1800512 &middot; 600 Small Street, Gallatin &middot; {len(records)} annual filings, {years[0]}–{years[-1]}</p>
</header>
<nav>{nav}</nav>
<main>
{''.join(panels)}
<div class="trend"><h3>Across every year</h3><table><tr><th></th>{head}</tr>{''.join(trows)}</table></div>
</main>
<script>
const btns=[...document.querySelectorAll('nav button')];
function show(y){{
  document.querySelectorAll('.panel').forEach(p=>p.classList.toggle('on',p.id==='fy'+y));
  btns.forEach(b=>b.classList.toggle('on',b.dataset.y===y));
  location.hash=y;
}}
btns.forEach(b=>b.onclick=()=>show(b.dataset.y));
show(location.hash.slice(1)||btns[btns.length-1].dataset.y);
</script>
"""
    open(out, "w").write(html)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dir")
    ap.add_argument("-o", "--out", default=None)
    ap.add_argument("--html", default=None)
    a = ap.parse_args()

    files = sorted(glob.glob(os.path.join(a.dir, "*.xml")))
    files = [f for f in files if "master" not in os.path.basename(f).lower()]
    records = sorted((parse(f) for f in files), key=lambda r: r["period_end"] or r["fy"])

    master = a.out or os.path.join(a.dir, "MASTER-shalomzone-990s.xml")
    build_master(records, master)
    print(f"{len(records)} filings -> {master}")

    if a.html:
        build_html(records, a.html)
        print(f"                -> {a.html}")


if __name__ == "__main__":
    main()
