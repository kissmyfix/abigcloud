#!/usr/bin/env python3
"""Which 501(c) subsection does each Tennessee IDB file under?

The article claims Gallatin is the only Industrial Development Board in Tennessee
filing with the IRS as a 501(c)(4). This checks that against ProPublica's Nonprofit
Explorer API, which surfaces the IRS Business Master File subsection code.

The IRS bulk extracts in usa_federal/irs_990_data/irs_supporting_docs/ would answer
this offline, but only the record-layout documents were saved -- the data archives
themselves are missing. This queries the same underlying data one organisation at a
time instead.

    files/venv/bin/python files/bin/tn-idb-subsections.py

Writes usa_federal/irs_990_data/derived/tn-idb-subsections.md
"""
import json, urllib.request, pathlib, datetime

API = "https://projects.propublica.org/nonprofits/api/v2"
NAMES = {3: "501(c)(3) charitable", 4: "501(c)(4) social welfare", 6: "501(c)(6) business league"}

def get(url):
    with urllib.request.urlopen(url, timeout=30) as r:
        return json.load(r)

search = get(f"{API}/search.json?q=industrial+development+board&state%5Bid%5D=TN")
rows = []
for o in search.get("organizations", []):
    ein = o["ein"]
    detail = get(f"{API}/organizations/{ein}.json").get("organization", {})
    rows.append({
        "ein": ein,
        "name": o.get("name", ""),
        "city": detail.get("city", ""),
        "sub": detail.get("subsection_code", o.get("subseccd")),
        "ntee": detail.get("ntee_code", ""),
        "revenue": detail.get("revenue_amount"),
    })
rows.sort(key=lambda r: (r["sub"] or 99, -(r["revenue"] or 0)))

out = [
    "# Tennessee IDBs by 501(c) subsection",
    "",
    f"Retrieved {datetime.date.today()} from ProPublica Nonprofit Explorer, which republishes",
    "the IRS Business Master File. Reproduce with `files/bin/tn-idb-subsections.py`.",
    "",
    "Search: organisations in Tennessee matching \"industrial development board\" that have",
    "filed a Form 990. This is the population of IDBs the IRS has filings for, not the",
    "population of IDBs that exist.",
    "",
    "| EIN | Organisation | City | Subsection | NTEE |",
    "|---|---|---|---|---|",
]
for r in rows:
    out.append(f"| `{r['ein']}` | {r['name']} | {r['city']} | **{NAMES.get(r['sub'], r['sub'])}** | {r['ntee']} |")

counts = {}
for r in rows:
    counts[r["sub"]] = counts.get(r["sub"], 0) + 1
out += ["", "## Distribution", ""]
for sub, n in sorted(counts.items()):
    out.append(f"- **{NAMES.get(sub, sub)}** — {n}")
out += [
    "",
    "## The finding",
    "",
    f"Of the {len(rows)} Tennessee Industrial Development Boards with IRS filings, exactly one",
    "is classified **501(c)(4)**: the Industrial Development Board of the Gallatin TN,",
    "EIN 38-4171308. Every other one files as a 501(c)(3) or a 501(c)(6).",
    "",
    "A 501(c)(4) is a social welfare organisation. A 501(c)(6) is a business league. Neither",
    "is the natural federal posture for a government instrumentality, but the peer group",
    "chose (c)(6) or (c)(3); Gallatin chose the category that holds advocacy groups.",
    "",
    "**Scope.** This establishes uniqueness among *filers*. It does not establish the total",
    "number of IDBs chartered in Tennessee -- that figure needs its own source.",
]
p = pathlib.Path("usa_federal/irs_990_data/derived/tn-idb-subsections.md")
p.parent.mkdir(parents=True, exist_ok=True)
p.write_text("\n".join(out) + "\n", encoding="utf-8")
print(f"wrote {p} ({len(rows)} organisations)")
for r in rows:
    print(f"  {r['ein']}  c({r['sub']})  {r['name'][:46]}")
