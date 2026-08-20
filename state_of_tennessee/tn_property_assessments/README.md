# Sumner County property assessments, Tax Year 2026

Parcel Details Reports from the Tennessee Property Assessment Data site
(assessment.cot.tn.gov, reached through the Sumner County parcel viewer at
sumnertn.geopowered.com), parsed into one machine-readable file.

## Source Type

**Primary Source.** Official county assessor records — authoritative for
assessed values, ownership, and mailing addresses on file.

## Files

| File | What it is |
|---|---|
| `derived/sumner-assessments.json` | **The dataset.** 4 parcels, Tax Year 2026. Machine-generated — see the `derived/` convention in `files/DATA_MAP.md`. |
| `files/bin/parse-assessment.py` | Regenerates the JSON from the PDFs. |
| `files/bin/verify-assessments.py` | Checks the JSON against the PDFs four independent ways. |
| `sumner-assessment-*.pdf` | Source reports, one per parcel. |
| `unknown-assessment.pdf` | Duplicate download of the Bradford parcel — see below. |
| `sumner-assessment-bradford-confirmed.pdf` | Second, independent rendering of the Bradford parcel. Cross-check source, not parsed. |
| `sumner-assessment-daycare-*.pdf` | The two Gallatin Day Care Centers parcels on Southpark Circle, 108 and 112. Not part of the four-parcel dataset below. |

Regenerate from the project root with `python3 files/bin/parse-assessment.py`, then
`python3 files/bin/verify-assessments.py`. Both resolve this directory from their own
location, so they run from anywhere.

## What the sources actually are

Four parcels, one snapshot each: **Tax Year 2026, Reappraisal 2024**. Not a time
series — every figure here is a single moment, and any year-over-year claim needs
records this directory does not yet hold.

| Parcel | Situs | Jan 1 owner | Total appraisal |
|---|---|---|---|
| `111 00100 000` | GTN5 META LOOP 1 | Industrial Dev Brd of City of Gallatin, c/o Woolhawk LLC Attn: Tax, 1601 Willow Rd, Menlo Park CA 94025 | $519,189,800 |
| `112 01202 000` | GATEWAY DRIVE 1399 | Gallatin City of IDB, Dana A Frazier c/o, 17601 Beretta Drive, Accokeek MD 20607 | $19,112,100 |
| `112 10900 000` | COMMERCE WAY 195 | IFR Land LLC, 10875 Chicago Drive, Zeeland MI 49464 | $2,755,100 |
| `111 00102 000` | GATEWAY DRIVE 1434 | United States of America, 1101 Market St Br 4B, Chattanooga TN 37204 | $0 |

`unknown-assessment.pdf` is a second download of the Bradford parcel. Its bytes
differ from `sumner-assessment-bradford.pdf` but its text is identical, so the
parser keeps one record and notes the duplicate in `source.duplicate_files`
rather than double-counting it.

`sumner-assessment-bradford-confirmed.pdf` is the same parcel from the state site
(`assessment.cot.tn.gov`) printed from Firefox, where the other four are the county
viewer printed from Chromium. Different layout, different producer, no shared
geometry — so the parser skips it (it detects the viewer's header line) and
`files/bin/verify-assessments.py` uses it as a cross-source check instead.

`parcel_id` is written in the same shape the comptroller PILOT filings use
(`111 00100 000`), so this dataset joins to
`state_of_tennessee/tn_comptroller_pilot_reports/sumner_county/derived/sumner-pilot.json`
on that key.

## Reading the data

One record per parcel. Nested sections are arrays, because their length varies
wildly: Woolhawk carries 5 commercial buildings, 35 outbuilding & yard items and
12 sales; the TVA parcel carries none of the first two and 13 sales.

```json
{
  "parcel_id": "111 00100 000",
  "situs_address": "GTN5 META LOOP 1",
  "value": { "total_market_appraisal": { "raw": "$519,189,800", "usd": 519189800 },
             "assessment_percentage": { "raw": "0%", "pct": 0 } },
  "buildings": [ { "building": 2, "actual_year_built": 2023,
                   "business_living_area": 981430,
                   "areas": [ … ], "features": [ … ] } ],
  "sales": [ { "date": "2020-05-18", "price": { "raw": "$8,268,000", … } } ]
}
```

Three things to know before using it:

**Money keeps its `raw` string** beside the typed `usd`, same as the PILOT
dataset, so the source's own formatting stays visible and the numbers stay
summable. `null` means the report printed nothing; `0` means it printed zero.

**Building numbers are the report's, not an index.** Woolhawk's five buildings
are numbered 2 through 6 — there is no building 1 on that parcel.

**Assessment is not appraisal.** Three of the four parcels are assessed at 0% and
carry an assessment of $0 against real appraised value. Bradford, the only
non-exempt parcel here, is assessed at 40%.

## How it was parsed

Word coordinates (`pdftotext -bbox-layout`), not flowed text. The report is a
four-column grid and lays commercial buildings out side by side; flowed text
interleaves two buildings into one unusable stream. A building panel owns two
grid columns, and its tables can spill onto following pages, so the parser
claims pages forward until one opens a new building or a full-width section.

Table cells are assigned by **overlap** with the header span rather than by a
left-edge cut, because alignment is inconsistent: money and areas are right
aligned and can start well left of their header (`$8,268,000` starts 19pt left
of "Price"), while type descriptions run well past theirs.

## Verified against source

`files/bin/verify-assessments.py` checks every parcel three ways, none of which import the parser,
plus a fourth where a second document exists:

- **A — flowed text.** `pdftotext -layout` read by line shape: the five value
  figures, tax year, acres, declared building count, building numbers, and every
  sale row's date/price/book/page.
- **B — raw stream.** `pdftotext -raw` as multisets: every `$` string and every
  date in the PDF must appear exactly as often in the JSON, and no comma-grouped
  figure in the JSON may be absent from the source. Catches drops and duplicates.
- **C — internal maths.** Land + improvement = total appraisal; total ×
  assessment % = assessment; land code units = total land units; buildings
  parsed = buildings declared; and per building, the interior/exterior areas sum
  to the stated business living area.
- **D — cross-source.** For Bradford only, the same facts read out of a second,
  independently produced document: the five value figures, land units, business
  living area, and every sale's date/price/book/page. Two publishers agreeing is
  a stronger claim than any single-document check can make.

Fifth condition: an all-parcels roll-up recounted straight from the source text.

All passes agree on all four parcels. The per-building area check is the strongest
of them — Woolhawk's building 2 sums seven area rows to exactly its stated 981,430
sq ft, which no column misread would survive.

## Open items

**The README figure for Woolhawk was $531M+; this record says $519,189,800.**
Not yet reconciled. It could be a different tax year, or a figure that combined
parcels. Do not print either number until that is settled — it starts here.

**Control parcels are missing.** North American Stamping and Archer Datacenters
were meant to be in this directory for comparative analysis. They are not.
They need pulling from the parcel viewer.

**Sales rows are the assessor's, not deeds.** A `$0` price with a quitclaim
instrument is a transfer, not a sale at zero. Cite the instrument type alongside
any price.


## Naming, 2026-08-19

Four files were renamed to the `sumner-assessment-<subject>.pdf` convention. Three had
kept the parcel viewer's own download names, which encode a download date and a parcel
id with `+` characters in them (~~`ParcelDetails-8_3_2026-083135M+A+01200+000.pdf`~~) and say
nothing about whose parcel it is. A fourth, ~~`lates-meta-parcel-assessment.pdf`~~, carried a
typo and was content-identical to `sumner-assessment-woolhawk.pdf` from the same source
and producer, so it was removed and the article citation repointed at the primary. A
second download of the 112 Southpark parcel, byte-identical in text to the first, was
removed at the same time.
