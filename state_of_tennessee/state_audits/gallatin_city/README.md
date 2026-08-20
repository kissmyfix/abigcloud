# state_audits/gallatin_city/

## Purpose
Annual Comprehensive Financial Reports for the City of Gallatin — the government whose ACFR either does or does not account for the boards distributing PILOT money in its name.

## Contents
- `1688-YYYY-c-gallatin-*.pdf` — full ACFRs, FY2015–FY2025 (FY2022 missing; see Notes). The `1688` prefix is the Comptroller's entity number for the City of Gallatin.
- `excerpt-gallatin-acfr-fy2021-idb-fund.pdf` — one page: Industrial Development Board Fund, statement of revenues, expenditures and changes in fund balance, budget and actual, FY2021. Original filename `Microsoft Word - Cover & Divider Pages - 1688-2021-c-gallatin-rpt-cpa811-8-17-22-rev1.pdf`.
- `excerpt-gallatin-acfr-fy2022-idb-fund.pdf` — one page: same schedule, FY2022. Original filename `1688-2022-c-gallatin-rpt-cpa811-12-31-22.pdf` — note it carried a full-report filename despite being a single page.
- `excerpt-gallatin-acfr-fy2023-notes.pdf` — one page: Notes to Financial Statements, FY2023. Original filename `Gallatin 2023 - 1688-2023-c-gallatin-rpt-cpa811-12-21-23.pdf`.
- `derived/` — page-anchored text extractions and `pdf-index.csv`.

## Source Type
**Primary Source** — audited financial statements filed with the Tennessee Comptroller. All eleven full ACFRs are born-digital; extraction is authoritative.

## Handling Instructions
- Cite printed page numbers, not `[[page N]]` markers.
- **Two different things are named "Industrial Development Board" in these records and they are not the same entity.** The city operates an *Industrial Development Board Fund* inside its own governmental funds, while the *Industrial Development Board of Gallatin, Tennessee* is a separate corporation filing its own audit (`state_of_tennessee/state_audits/gallatin_idb/`). Never merge their figures or treat one's totals as the other's.
- The FY2022 excerpt records the city fund receiving "Payment in lieu from industry" of **$182,548 actual against $265,025 budgeted** — an order of magnitude below what the IDB corporation reports for FY2025. The relationship between the two PILOT streams is unresolved.

## Notes
**The city classifies the IDB as a "Related Organization," deliberately outside its reporting entity.** FY2023 ACFR, Note 1: the City's "accountability for these organizations does not extend beyond making the appointments... the City does not provide funding, has no obligation for the debt issued by the Housing Authority and the IDB, and cannot impose its will upon the operations." This is the documented reason the IDB never appears as a component unit — and it is the opposite of how the same auditor treats Westmoreland's IDB.

**Open lead — the IDB fund appears to vanish after FY2023.** Occurrences of "Industrial Development Board" run 4–6 per ACFR from FY2015 through FY2023, then drop to exactly **one** in FY2024 and FY2025, and that single mention is boilerplate about historic conduit debt. Not yet confirmed whether the fund was genuinely removed or is present under different wording.

Known gap: the full FY2022 ACFR has not been obtained.

**One document, two provenances.** `1688-2022-c-gallatin-rpt-cpa811-12-31-22.pdf` (the
Comptroller-filed copy) and `sumner_county/gallatin_council_meetings/2022-gallatin-annual-financial-report.pdf`
(the gallatintn.gov copy) are the same FY2022 ACFR — different PDF bytes, byte-identical text
extraction. Both are kept because they are filed by source, but they are one piece of
evidence, not two. Confirmed 2026-07-29.
