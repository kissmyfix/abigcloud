# state_audits/sumner_county/

## Purpose
Comptroller-filed financial reports for Sumner County. **Two different document types sit
here and only one of them is a county audit.** Read `derived/FINDING-AID.md` before using
this directory.

## Contents

**County annual financial report** — the county's own audited statements.
- `2019-sumner-county-annual-financial-report.pdf` — FY2019, 243 pp

**Board of Education internal school funds** — activity accounts of individual schools
(balance sheets and revenue statements per school), not county revenue. These are where
**Meta's grants to individual schools are itemised**, FY2023–FY2025; see the finding aid.
- `2559-2020-s-sumcoact-rpt-cpa811-12-24-20.pdf` — FY2020, 167 pp
- `2559-2022-s-sumcoact-rpt-cpa522-12-21-22.pdf` — FY2022, 226 pp
- `2559-2023-s-sumcoact-rpt-cpa522-12-21-23.pdf` — FY2023, 226 pp
- `2559-2024-s-sumcoact-rpt-cpa522-12-24-24.pdf` — FY2024, 230 pp
- `2559-2025-s-sumcoact-rpt-cpa522-12-27-25.pdf` — FY2025, 212 pp

- `derived/` — page-anchored text, `pdf-index.csv`, `FINDING-AID.md`

All born-digital; extraction is authoritative. `2559` is the Comptroller's entity number;
`sumcoact` in the filename means *Sumner County activity funds*.

## Source Type
**Primary Source** — audited financial statements.

## Handling Instructions
- **DIGITAL.** `pdftotext -layout` output is reliable; no OCR caveat applies.
- Cite printed page numbers, not `[[page N]]` markers. In the FY2019 county report the two
  align exactly; that was verified 2026-08-24 and is not assumed for the school reports.
- **The IDB reconciliation cannot be done from the school-funds reports.** The Gallatin
  IDB's FY2025 audit reports paying Sumner County $2,291,692 and Sumner County Schools
  $640,457. Confirming the receiving end needs the county's annual financial report or the
  School Department's audited statements. Neither is held for FY2025. Full-text search of
  all five school reports returns zero hits for IDB, PILOT, payment in lieu, or industrial
  development.

## Notes
Known gaps: **county annual financial reports for FY2020–FY2025 are all missing** — only
FY2019 is held. **FY2021 is missing entirely**, in both document types. No Sumner County
School Department audited financial statements are held for any year.

The FY2022–FY2025 files are large (7.6–9.4MB) because of an inefficient PDF generator, not because they are scans — they carry full digital text at roughly 4,700 characters per page.

**Renamed 2026-07-29:** `FY19SumnerAFR.pdf` is now `2019-sumner-county-annual-financial-report.pdf`.
