# Finding Aid — tn_comptroller_pilot_reports/

**Start with the CSVs in this directory, not the PDFs.** This is the best-compressed part
of the archive: twelve years of statewide comptroller PILOT filings already parsed into
four tables. The PDFs upstairs are the citable record; these are how you find the row.

Built 2026-08-24.

---

## The four tables

| File | Rows | Covers |
|---|---:|---|
| `tn-statewide-pilot-master-2014-2025.csv` | 13,630 | Every PILOT filing in Tennessee, 2014–2025 |
| `tn-idb-debt-master-2021-2023.csv` | 1,273 | IDB debt reporting, 2021–2023 |
| `sumner_idb_master_2017-2025.csv` | 99 | Sumner County line items, one row per lessee-year |
| `sumner_county_totals_2016-2025.csv` | 9 | Sumner County aggregates, one row per year |

**Statewide** — `YEAR, COUNTY, PROJ_TYPE, FILING_DATE, CASE_NO, LESSEE, PROPERTY_ADDRESS,
CITY, PARCEL_ID, PROP_TYPE, PROP_CODE, CONTACT, CONTACT_TITLE, EMAIL, …`
The comparison set. Any claim about how Gallatin compares to the rest of Tennessee is
answerable here without opening a PDF.

**Debt** — `YEAR, ENTITY, DEBT_NAME, ORIGINAL_AMOUNT, OUTSTANDING_FYE, PROJECT, DEBT_TYPE,
HAS_DEBT, SOURCE_SHEET`

**Sumner line items** — `source, date_received, lessee, est_value, rent, pilot_city,
pilot_county, lease_begin, lease_end, raw_row`. `raw_row` preserves the unparsed original,
so a parse can always be checked against what was on the page.

**Sumner totals** — computed from the line items, not transcribed.

---

## What the Sumner totals show

| Year | Est. value | Rent | PILOT city | PILOT county | Entities |
|---|---:|---:|---:|---:|---:|
| 2016 | $31,076,264 | $2,867,686 | $0 | $0 | 6 |
| 2017 | $184,277,996 | $3,954,422 | $0 | $0 | 7 |
| 2019 | $26,351,192 | $4,094,024 | $12,126 | $21,500 | 5 |
| 2020 | $21,486,138 | $3,042,359 | $18,204 | $38,845 | 5 |
| 2021 | $55,152,129 | $2,961,839 | $98,844 | $110,224 | 7 |
| 2022 | $46,434,076 | $12,349,639 | $37,632 | $68,485 | 6 |
| 2023 | $115,414,634 | $4,212,189 | $202,612 | $73,380 | 6 |
| 2024 | $430,356,064 | $820,689 | $1,231,064 | $256,488 | 4 |
| 2025 | $554,547,379 | $667,578 | $1,893,678 | $67,069 | 3 |

**2018 is absent from the series.** Whether the filing is missing from the archive or was
never made is not established here.

Three movements worth reading against each other rather than separately:

*Value rises roughly eighteenfold* across the series, $31M to $554M.

*Rent falls to a quarter of where it started*, $2.87M to $667K, and the fall is abrupt:
$4.2M in 2023 to $820K in 2024.

*Entity count falls from six to three* while value climbs, so the later totals rest on
fewer, much larger arrangements.

*County PILOT peaks in 2024 at $256,488 and falls to $67,069 in 2025*, while city PILOT
rises to $1.89M in the same year.

None of that is a finding on its own. The line-item table is where each movement resolves
to a named lessee, and `raw_row` is where the parse can be checked. **Do not quote these
aggregates without going down to the rows that produced them.**

`Archer Datacenters` first appears in the 2021 rows.

---

## Documents upstairs

- `2024-idb-annual-report.pdf` — the comptroller's own annual report on IDBs
- `2025-idb-annual-debt-reporting-request.pdf` — the request letter sent to boards
- `comptroller-idb-debt-reporting-guidelines.pdf` — what boards are told to file, and what
  the obligation actually is. Read this before characterising any board's filing as late,
  incomplete, or non-compliant.
- `2025-pilot-reporting.xlsx` — current-year workbook

`sumner_county/` holds the per-year Sumner PILOT filings 2015–2022 as filed, plus
`derived/woolhawk-pilot-reporting.md` and `sumner-pilot.json`.
`tn_comptroller_archived/` holds the statewide filings 2014–2022 and `idb_debt-reports.xlsx`.

**Cite the PDF, by its printed page.** The CSVs are derived and regenerable; they are how
you locate a figure, never what carries it.
