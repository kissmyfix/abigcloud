# derived/

## Purpose
Project-built master spreadsheets compiled from the Comptroller PILOT reports in the
sibling directories. Nothing here is a filing — every file is output of a parser in
`files/bin/`, and every figure in it should be traceable back to a source report.

## Contents
| File | Rows | Built by | Status |
|---|---|---|---|
| `tn-statewide-pilot-master-2014-2025.csv` | 13,630 | `files/bin/build-statewide-pilot-master.py` | **Current.** 81 counties with filings, 2014–2025 |
| `tn-idb-debt-master-2021-2023.csv` | 1,273 | `files/bin/build-idb-debt-master.py` | **Current.** IDB debt reporting, 197 entities, 2021–2023 |
| `hamilton-county-pilot-master-2014-2025.csv` | — | `files/bin/build-hamilton-master.py` | Superseded in scope; despite the filename it starts at **2016** (the builder has no 2014–2015 layout) |
| `sumner_idb_master_2017-2025.csv` | — | `files/bin/parse-sumner-pilot.py` | **Known incomplete — do not cite. See below.** |
| `sumner_county_totals_2016-2025.csv` | — | (rolled up from the Sumner master) | Inherits the Sumner master's gaps — re-derive before use |

Since 2026-07-29 this directory also holds a page-anchored text extraction and a
`pdf-index.csv` for the one PDF filed loose in the parent —
`comptroller-idb-debt-reporting-guidelines.pdf`. That extraction is **OCR**, not born-digital
text: read it to find a passage, then quote the page image.

## Source Type
**Working Material / Output Artifact.** Not citable as a source. Cite the underlying
Comptroller report, then use these files to find it.

## Handling Instructions
- Rebuild rather than hand-edit. Both statewide scripts need `pdfplumber`, `pandas`, and
  `openpyxl`; build a venv if the imports fail.
- The statewide master preserves the difference between a **blank** and a **zero** in the
  PILOT columns. Do not fill blanks with 0 — an unstated county payment and a reported
  county payment of $0 are different facts, and the distinction is load-bearing.
- The county-cropped sets are crops of the same statewide reports, so a figure appearing
  in both a county master and the statewide master is **not** independent corroboration.

## Notes

**The debt master is a different schema, deliberately.** `tn-idb-debt-master-2021-2023.csv`
reports borrowing, not abatement, and shares no columns with the PILOT masters beyond the
year. It carries no COUNTY column: entity names imply a county, but resolving "Industrial
Development Board of the City of Portland" to Sumner is inference, so the entity name is
left raw rather than inventing a join key. Join on entity name, by hand, knowingly.
`HAS_DEBT` is the one derived field — it is simply `DEBT_TYPE != "No Debt"`.

**`sumner_idb_master_2017-2025.csv` is not trustworthy (found 2026-07-28).** Building the
statewide master gave the first independent parse of the same underlying reports, and the
two disagree. Checked against Sumner blocks counted by hand directly off the cropped
source PDFs:

| Report year | Source block | Statewide master | Sumner master |
|---|---|---|---|
| 2016 | 8 | 8 | 0 |
| 2017 | 11 | 11 | 7 |
| 2018 | 6 | 6 | 10 |
| 2020 | 9 | 9 | 6 |
| 2022 | 19 | 19 | 16 |

The statewide parse matches the source in 5 of 5 checkable years; the Sumner master
matches in none. It drops entities that are plainly in its own source file — NHC
Healthcare–Sumner, Gallatin SLP, NASG Tennessee North 2, ATA Retail Services — and it
carries rows under the wrong year: its `2017-pilot-sumner.pdf` rows include Beretta and
Bradford with **2016** filing dates, which do not appear in that file's Sumner block.

**What this does and does not put in doubt.** Any claim resting on a Sumner *count* or a
Sumner *total* from that file needs rechecking against the statewide master. The Woolhawk
findings survive intact and are now independently confirmed: the statewide parse
reproduces **41 Woolhawk filings, 2021–2025, $3,321,650 in city PILOT, nothing to the
county in any of them,** and a top EST_VALUE of **$519,189,800** — all matching the
figures reached earlier from the cropped data.
