# state_of_tennessee/tn_comptroller_pilot_reports/

## Purpose
PILOT reports filed with the Tennessee Comptroller — the official self-reported record of active tax abatement agreements, organized by county for comparison work.

## Contents
- `sumner_county/` — Sumner County PILOT reports, 2015–2022 PDFs + 2023–2025 ODS
- `hamilton_county/` — Hamilton County (Chattanooga) comparison set, 2014–2025
- `gibson_county/` — Gibson County comparison set (the other sizable 990-filing IDB), 2015–2025
- `tn_comptroller_archived/` — statewide annual PILOT reports 2014–2025 + `idb_debt-reports.xlsx`
- `2024-idb-annual-report.pdf`, `2025-idb-annual-debt-reporting-request.pdf` — loose Comptroller
  IDB filings at this level (renamed to the project scheme 2026-07-29 from `FY2024IDBReport.pdf`
  and `FY2025IDBAnnualDebtReportingRequest.pdf`)
- `comptroller-idb-debt-reporting-guidelines.pdf` — **Tennessee State Funding Board Guidelines,
  Debt Reporting by Industrial Development Boards**, 4 pages. The rules the filings in
  `tn_comptroller_archived/idb_debt-reports.xlsx` are made under: § 7-53-304 requires every IDB
  to maintain an aggregate listing of its direct and conduit debt and to report defaults to the
  SFB; § 9-21-134 adds covenant violations and rating downgrades. Its text layer is **OCR**, so
  quote from the page image, not from `derived/`
- `derived/` — **Working Material, not Comptroller filings**: the project-built master spreadsheets compiled from the reports above. `tn-statewide-pilot-master-2014-2025.csv` (13,630 rows, 81 counties, 2014–2025) is the current one; **`sumner_idb_master_2017-2025.csv` is known incomplete and should not be cited** — see that directory's README

## Source Type
**Primary Source — Self-Reported.** Official Comptroller filings, but the underlying data is self-reported by the corporations and IDBs. Authoritative for what was reported; scrutinize whether what was reported is accurate.

## Handling Instructions
- Cite by entity name, PILOT year, and filing date; note the self-reported nature for figures that can't be cross-referenced
- The Woolhawk entry is the central record — compare against `state_of_tennessee/tn_property_assessments/` and `usa_federal/irs_990_data/`
- The county subdirectories are the control-group evidence base: normal registry deals produce county payments at 1.5–2x city payments; Woolhawk's $0 county payment is a documented deviation, not a structural limitation. The key control-group figures: North American Stamping Group — $8.5M assessment, $50,000 to Sumner County; Archer Datacenters — same IDB, same address, same year as Woolhawk, $53,000 to Sumner County; Woolhawk — $531M assessment, $0 to Sumner County
- This is the most accessible plain-language proof that the $0 county payment was a choice, not an inevitability

## Notes
This directory became the canonical PILOT-report home in July 2026 when the old root-level `pilot_data/` (byte-identical duplicates plus the derived CSVs now in `derived/`) was dissolved. Two more duplicates were cleared 2026-07-29: `IDB Annual Report Data.xlsx` (byte-identical to `tn_comptroller_archived/idb_debt-reports.xlsx`, which is the copy the build scripts read) and `SFBGuidelinesIDBDebtReporting.pdf` (byte-identical to the surviving `comptroller-idb-debt-reporting-guidelines.pdf`, which moved into this directory from the `state_of_tennessee/` root on 2026-07-29). The Comptroller's Best Interest Determination criteria (the standard Rosemary Bates' "we wanted low job numbers" quote contradicts) are still not in the project — open gap.
