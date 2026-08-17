# state_of_tennessee/state_audits/

## Purpose
Annual financial audits filed with the Tennessee Comptroller of the Treasury for the entities in scope — the City of Gallatin and its two boards, the control-group municipalities, and Sumner County — plus a small set of Comptroller investigative records kept for narrative contrast.

## Contents
One directory per **legal entity**, not per municipality. That distinction is load-bearing: the City of Gallatin, the Gallatin Industrial Development Board, and the Gallatin Health, Educational and Housing Facilities Board are three separate corporations that file three separate audits, and the city's own ACFR states the IDB is excluded from its reporting entity.

| Directory | Entity | Coverage |
|---|---|---|
| `gallatin_city/` | City of Gallatin | ACFRs FY2015–FY2025 (11), plus 3 single-page excerpts |
| `gallatin_idb/` | Industrial Development Board of the City of Gallatin | FY2025 |
| `gallatin_hhfb/` | Health, Educational and Housing Facilities Board of the City of Gallatin | FY2025 |
| `westmoreland_city/` | City of Westmoreland | FY2024–FY2025 |
| `westmoreland_idb/` | Industrial Development Board of the City of Westmoreland | FY2023–FY2025 |
| `portland_city/` | City of Portland | FY2025 |
| `sumner_county/` | Sumner County | FY2020, FY2022–FY2025, plus FY19 AFR |
| `investigations/` | Comptroller investigative report and grand jury presentments | 2017, 2026 |

Each directory carries a `derived/` subdirectory holding page-anchored `.txt` extractions, any OCR'd copies, and a `pdf-index.csv`. Sources stay primary; `derived/` is regenerable output.

## Source Type
**Primary Source** — audits and investigative records produced by the Tennessee Comptroller of the Treasury and by contracted CPAs filing with it. The `derived/` subdirectories are **Working Material**.

## Handling Instructions
- Cite the **printed page number** shown on the document, not the `[[page N]]` marker in the extractions — divider pages shift them apart.
- **Seven of these are scans with OCR text layers**, including every one of the board audits. Their `pdf-index.csv` row says `verify figures against page image`. Do not publish a figure from an OCR'd extraction without checking it against the PDF.
- Arithmetic re-derivation is a genuine verification method on financial statements: if revenue lines sum to the stated total, expenses sum to theirs, and the change in net assets ties to beginning and ending balances, OCR digit corruption is effectively ruled out. Do this before trusting numbers out of an `OCR_SCAN` file.
- Rebuild all extractions with `python3 files/bin/pdf-extract.py state_of_tennessee/state_audits`. It skips work already done; add `--force` to redo it.
- Read the entity subdirectory's own `README.md` before working in it — several record findings and known gaps specific to that entity.

## Notes
Filenames beginning `excerpt-` are single-page clippings from a larger report, not the report itself. They were saved for a specific line and are not a substitute for the full document.

Known gap: the **full FY2022 City of Gallatin ACFR** has not been obtained — only a one-page excerpt of its Industrial Development Board fund schedule.
