# tn_comptroller_archived/

## Purpose
The Tennessee Comptroller's **statewide** annual PILOT reports — every industrial
development board and health/educational facility board in the state, all 95 counties,
2014 through 2025. This is the denominator: it lets any Sumner County finding be stated
as a deviation from statewide practice rather than an isolated observation.

## Contents
- `2014-pilot.pdf` … `2022-pilot.pdf` — nine annual reports as PDF tables, 9–25 pages each
- `2023-pilot.xlsx`, `2024-pilot.xlsx`, `2025-pilot.xlsx` — the same report as spreadsheets
- `idb_debt-reports.xlsx` — IDB debt reporting, three sheets (2021, 2022, 2023), parsed
  into `../derived/tn-idb-debt-master-2021-2023.csv` — **1,273 rows, 197 entities** — by
  `files/bin/build-idb-debt-master.py`, verified by `files/bin/verify-idb-debt-master.py`

Parsed into `../derived/tn-statewide-pilot-master-2014-2025.csv` — **13,630 rows across 81
of the 95 counties** (the other 14 filed no PILOT agreements in any of these years) — by
`files/bin/build-statewide-pilot-master.py`, verified by
`files/bin/verify-statewide-pilot-master.py`.

## Source Type
**Primary Source — Self-Reported.** Official Comptroller filings, but every figure in
them is self-reported by the lessee corporations and their IDBs. Authoritative for *what
was reported*; a blank or a zero is evidence of what the filer chose to state, not proof
of what was owed.

## Handling Instructions
- Cite by report year, county, lessee, and filing date. Report year is the year the
  Comptroller published, not the tax year the figures describe.
- **A blank PILOT_COUNTY is not the same as $0.** The source leaves cells empty; the
  parser preserves the distinction rather than coercing blanks to zero. Woolhawk's county
  column is empty in every filing, which is a stronger fact than a reported zero — the
  county payment was never stated at all.
- These are the uncropped originals. The per-county sets in `../sumner_county/`,
  ~~`../hamilton_county/`~~, and ~~`../gibson_county/`~~ were crops of these same reports (moved
  out of the project 2026-08-19), so a
  figure appearing in both is **not** independent corroboration.
- The 2014–2015 layout is different and thinner: 15 columns instead of 19–20, no address,
  city, email, case number, or lease-begin field, and **counties identified by numeric
  code only**. Rows from those years carry correspondingly empty columns — that is the
  source, not a parse failure.

## Notes

**County code mapping.** The 2014–2015 reports identify counties by number. 73 of the 95
code→name pairs are proven directly by the 2016 and 2017 reports, which print name and
code side by side; those two years agree on every county they share, with zero conflicts.
Four codes used in 2014–2015 — **29, 48, 64, 81** — appear in no name-bearing report and
are filled from the published alphabetical list as Grainger, Lake, Moore, and Stewart.
Every row relying on one of those four is flagged in the `SOURCE_NOTE` column. If any of
those four counties ever becomes load-bearing for a published claim, confirm the code
against a Comptroller source first.

**Combined property-description field, 2014–2015.** Those years have one `Prop.Desc.`
column holding either a parcel ID or a street address, inconsistently. The parser routes
address-looking values to `PROPERTY_ADDRESS` and flags each one in `SOURCE_NOTE`. 155
rows total carry a note.

**Repeated header rows.** Every source repeats its header row — on each PDF page, and
scattered mid-file in all three spreadsheets (57 times in 2023, 59 each in 2024 and 2025).
In the 2024 and 2025 spreadsheets those repeated headers **also carry the next county's
name in the first cell**, where the column label should be, so a header row is both a row
to discard and the marker for which county the rows beneath it belong to. Any future
parser that skips them naively will silently misattribute every row that follows.

**Unmined lead — the 2025 workbook's leftover sheets.** `2025-pilot.xlsx` ships with nine
extra worksheets the Comptroller left in the file. `Sheet4` is a **1,561-row** extract
carrying a `Case #` column and 2023 filing dates — more rows than the 2023 report itself
(1,219) and a field the 2023 file does not have. `Sheet3` and `Sheet7` are further
partial extracts. Only the first sheet (`Query Results`) is the filed 2025 report and only
it is parsed. What is in Sheet4 that is not in the published 2023 report is an open
question worth answering.

**What the debt file says about Gallatin.** The Gallatin IDB reports **No Debt** in 2021,
2022, and 2023 — it has never borrowed, in its own name or as a conduit. So has the
separately registered **Industrial Development Board of the County of Sumner**, which is a
distinct filer from the Gallatin board. And **no data center anywhere in Tennessee carries
IDB debt** in any of the three years: all 1,273 rows were scanned for data center, Meta,
Woolhawk, Archer, hyperscale, and every major cloud operator, with zero hits. The Woolhawk
arrangement involved no bond financing at all — it is pure abatement.

Two secondary connections in the same county. **Portland's IDB financed the Sumner control
group**: conduit debt for North American Stamping ($28M), Shoals/Solon ($25.5M), Kyowa
America ($26.5M), SIF Portland/RB Distribution ($50M), Stevison Ham ($7M), Bennett
Properties/ATA Retail ($3.45M), plus direct debt of its own ($550K to buy a building).
**Hendersonville's IDB financed apartments and a Catholic high school** — Waterview
Apartments ($13.3M), Hickory Pointe Apartments ($5.925M), Pope John Paul II High School
($13M) — in-county precedent for an IDB funding non-industrial projects, which is the
question the City Hall / Boyle Investment engagement raises.

**Caution on denominators.** This file lists only **189, 189, and 184 distinct IDBs** for
2021, 2022, and 2023 (197 across all three years), and roughly two thirds report No Debt
each year. Whatever population the "423 IDBs" figure describes, it is not this one.
