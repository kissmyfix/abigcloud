# sumner_county/gallatin_council_meetings/

## Purpose
Gallatin City Council agendas, minutes, and related city documents pulled manually from gallatintn.gov — the public paper trail of what the council saw, said, and appropriated around the Woolhawk deal and the IDB.

## Contents
23 PDFs + 1 text file, 2018–2026, named to the project scheme (`YYYY-MM-DD-body-type.pdf`,
see `files/DATA_MAP.md`). What each document *is* and why it matters lives in
`memory/MEMORY.md` (session blocks "2026-07-05" and "2026-07-29"). This file is the index
and the handling rules.

`derived/` holds the extraction, all regenerable, nothing hand-edited:
- `derived/*.txt` — page-anchored text, `[[page N]]` at the top of each page. Cite the anchor.
- `derived/ocr/` — six packets whose text layer covered only part of the document, re-OCR'd
  with `ocrmypdf`, plus their text. The originals in this directory are the record and are
  never modified. OCR'd text reads cleanly and is still a machine guess.
- `derived/pdf-index.csv` — extraction class and text volume per file (`files/bin/pdf-extract.py`).
- `derived/council-index.csv` — one row per document: date the city printed on it, date in the
  filename, whether those agree, meeting body, page count, textless pages, extraction class,
  whether it is quotable without opening the page image, md5, duplicates.
  Rebuild: `python3 files/bin/build-council-index.py`
  Re-check: `python3 files/bin/verify-council-index.py` (recounts from source, asserts known
  anchors, exits nonzero on failure)

**Four documents are quotable straight from the text** —
`2019-gallatin-annual-financial-report.pdf`, `2022-gallatin-annual-financial-report.pdf`,
`2020-05-12-r2005-24-woolhawk-pilot-terms.pdf`, `2026-07-meetings-public-notice.pdf`.
Everything else is a scan.

Triaged 2026-07-05, extraction and index built 2026-07-29:

**Crown jewels**
- `2020-05-12-r2005-24-woolhawk-pilot-terms.pdf` — Resolution R2005-24, the actual Woolhawk PILOT terms (extract of the May 12 2020 packet, pages 40–45). 20-full-tax-years-per-building abatement, payment schedule, CapEx clawbacks, § 7-53-305(b) delegation, no city/county split. The citable artifact.
- `2020-09-15-city-council-agenda.pdf` + `2020-10-06` + `2021-02-02` + `2021-02-16` — the "Donations from Business - Woolhawk" (acct 110-36710-256) appropriations: $1M Gateway Drive, 2× $127,769 staff, plus Brown's "Project Woolhawk is Facebook" announcement (Sept 8 2020).
- `2024-10-31-gallatin-city-hall-space-needs-assessment.pdf` — the IDB engaged Studio Eight Design for the City Hall space-needs assessment; Boyle Investment discussions.

**Strong supporting**
- `2020-06-09-council-committee-agenda.pdf` — 524-acre annexation analysis with the city's own Beretta tax math ($113,494 county vs $40,175 city).
- `2020-05-12-council-committee-agenda.pdf` — full packet containing R2005-24.
- `2019-gallatin-annual-financial-report.pdf`, `2022-gallatin-annual-financial-report.pdf` — the IDB carried as a city fund ("used to account for economic development activity in the City") — tension with its independent-501(c)(4) federal posture.
- `2021-01-12-council-committee-agenda.pdf` — IDB reappointments (Assante, Wise; six-year terms) presented by Fenton.

**Context tier**
- `2020-05-05-city-council-agenda.pdf` — Woolhawk water/sewer contract, one week before the PILOT resolution review.
- `2022-05-17-city-council-agenda.pdf` — $930K water + $1.99M sewer line spending on Woolhawk.
- `2022-04-19-city-council-agenda.pdf` — $11,250 from the Donations account; "one-third from Woolhawk's annual payment... covering oversight and construction."
- `2018-06-19-city-council-agenda.pdf` — filed for years as `gnrc-plan-2018.pdf`. It is a council agenda packet; the GNRC regional plan is an attachment starting around p.58. Its two "PILOT" hits are a glossary entry defining "Pilot Study" — false positives, as originally called.
- `2026-07-meetings-public-notice.pdf` — current meeting monitoring.
- `2024-06-21-geda-bates-executive-director.txt` — GEDA/Bates announcement text.
- `2023-03-07-city-council-agenda.pdf` — page 1 born-digital, pages 2–62 were image-only, now OCR'd. Carries the **February 7, 2023 City Council Minutes** in full.

### Renamed 2026-07-29 — old → new

Notes written before this date use the old names. Two byte-identical copies Brandon had
prefixed as relevance flags (`important-…`, `the-most-importanat-yet-…`) were removed once
what they were flagging was recorded in `memory/MEMORY.md`.

| was | is |
|---|---|
| `woolhawk-terms.pdf` | `2020-05-12-r2005-24-woolhawk-pilot-terms.pdf` |
| `gnrc-plan-2018.pdf` | `2018-06-19-city-council-agenda.pdf` |
| `2019 Audit.pdf` | `2019-gallatin-annual-financial-report.pdf` |
| `2022-budget.pdf` (an ACFR, not a budget) | `2022-gallatin-annual-financial-report.pdf` |
| `24-10-31_Gallatin City Hall - Programming Document - Final_202507281053078786.pdf` | `2024-10-31-gallatin-city-hall-space-needs-assessment.pdf` |
| `2020-june-gallatin-agenda-woolhawk.pdf` | `2020-06-16-city-council-agenda.pdf` |
| `2020-july-gallain-council-agenda-woolhawk.pdf` | `2020-07-21-city-council-agenda.pdf` |
| `2020-sept-gallain-meeting-woolhawk-mayor.pdf` | `2020-09-15-city-council-agenda.pdf` |
| `geda-bates-announce.txt` | `2024-06-21-geda-bates-executive-director.txt` |
| `July Meetings 2026 Public Notice.pdf` | `2026-07-meetings-public-notice.pdf` |
| `<Month DD YYYY> City Council Meeting Agenda.pdf` | `YYYY-MM-DD-city-council-agenda.pdf` |
| `<Month DD YYYY> Council Work Session Agenda.pdf` | `YYYY-MM-DD-council-committee-agenda.pdf` |

The three 2020 `-woolhawk-` names had months in them that were not the meeting date: those
packets are the June 16, July 21, and September 15 meetings.

## Source Type
**Primary Source** — the city's own agendas, minutes, resolutions, budgets, and audits.

## Handling Instructions
- Cite by document, meeting date, and (for packets) the printed packet page number (e.g., "05/12/2020 Council Work Session Agenda, p. 42")
- Agenda packets contain draft resolutions; confirm passage in the corresponding meeting minutes before citing anything as adopted
- Text extraction quality varies — several packets are OCR-of-scan with garbled dollar amounts (e.g., "5127,769" = $127,769); verify figures against the page image before quoting. `council-index.csv`'s `quotable` column says which files this applies to (all but four)
- **The 2022-04-19 and 2022-05-17 packets garbled their own masthead dates** ("April t9,2022", "May t7,2022"). A date parser reading page 1 lands on the approval-of-minutes line instead and returns the *previous* meeting's date. Both were read off the page image by hand on 2026-07-29 and are pinned as verifier anchors. The May 17 OCR also corrupts the meeting time to "5:00 pm"; the image says 6:00 pm
- The 2020-05-12 packet's PDF pages now match the city's printed packet numbering exactly after OCR, so "packet p.40" and "PDF p.40" are the same page. That is asserted in the verifier — do not assume it holds for other packets without checking

## Notes
Absence is data here too: match these records against the statutory checklist in `state_of_tennessee/README.md` — the documents that should exist for a valid PILOT (county notice, county response, cost/benefit analysis) have not surfaced in these packets.

**One document, two provenances.** `2022-gallatin-annual-financial-report.pdf` (pulled from
gallatintn.gov) and `state_of_tennessee/state_audits/gallatin_city/1688-2022-c-gallatin-rpt-cpa811-12-31-22.pdf`
(the Comptroller-filed copy) are the same FY2022 ACFR — different PDF bytes, byte-identical
text extraction. Both are kept because they are filed by source, but they are one piece of
evidence, not two. Confirmed 2026-07-29.
