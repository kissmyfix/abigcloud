# Sumner County PILOT filings, 2015–2025

State comptroller PILOT (payment in lieu of taxes) filings for Sumner County,
parsed from the source reports into one machine-readable file.

## Files

| File | What it is |
|---|---|
| `derived/sumner-pilot.json` | **The dataset.** 131 filing lines, 2015–2025. Machine-generated — see the `derived/` convention in `files/DATA_MAP.md`. |
| `files/bin/parse-sumner-pilot.py` | Regenerates the JSON from the source documents. |
| `files/bin/verify-sumner-pilot.py` | Recounts every year straight from the source and prints ALL AGREE or the disagreement. |
| `2015-…` – `2022-pilot-sumner.pdf` | Source PDFs, one per report year. |
| `2023-2025-pilot-sumner.pdf.ods` | Source spreadsheet covering 2023, 2024, 2025. |

Regenerate from the project root with `python3 files/bin/parse-sumner-pilot.py`, then `python3 files/bin/verify-sumner-pilot.py`. Both resolve this directory from their own location, so they run from anywhere.

## What the sources actually are

Not Sumner-only reports — each PDF is an excerpt of the **statewide** roll, cropped
to a window containing the Sumner block plus neighbouring counties. Every year's
Sumner block is bounded on both sides by another county's rows, so each block is
verifiably complete; `source.block_complete` records this per record.

The reports change shape repeatedly. 2015 names no counties at all (Sumner is code
`83`) and carries no address, city, email or lease-begin. 2017 introduces a case
number and drops it again after 2020. Real-vs-personal only becomes an explicit
column in 2020. Six distinct layouts in eleven years.

## Reading the data

One record per **filing line** — report year × lessee × parcel × property type.

```json
{
  "report_year": 2024,
  "lessee": "WOOLHAWK LLC",
  "property": { "parcel": "111 00100 000", "type": "personal",
                "type_source": "column", "code": "ID01" },
  "amounts": {
    "est_value":    { "raw": "$360,247,200.00", "usd": 360247200 },
    "pilot_county": { "raw": "",                "usd": null }
  },
  "source": { "file": "…", "locator": "Sheet1!row38", "block_complete": true }
}
```

Three things to know before using it:

**`null` and `0` are different facts.** An empty cell means the filing reported
nothing; `0` means it reported zero. Woolhawk's county-PILOT is `null` in all five
years it appears; The Gap's 2024 city-PILOT is a reported `$0.00`. The dataset has
62 explicit zeros and 313 nulls — do not conflate them.

**Every value keeps its `raw` string** next to the typed one, so the filings' own
sloppiness stays visible and the numbers stay summable.

**`type_source`** says whether Real/Personal came from a real column (`column`,
2020 onward) or was inferred from the parcel's `P` suffix
(`inferred_from_parcel_suffix`, before 2020). Never present an inference as a filing.

Dates are ISO. Money is whole USD. `NO INFO` becomes `null` plus a `flags` entry.

## How it was parsed

PDFs are read from word coordinates (`pdftotext -bbox-layout`) rather than flowed
text, so a column a filer left empty stays empty instead of collapsing. Columns are
located by combining the header labels (which name and order them) with the
positions where the data actually starts (headers are centred, values are left
aligned, so the label alone puts the boundary in the wrong place). Money columns are
pinned separately because they are right aligned.

2015 and 2021 carry no header row anywhere in the crop; their column positions were
measured off the word coordinates and are recorded explicitly in `FALLBACK` in the
parser, with a comment on how to re-derive them.

The `.ods` is read straight from its cells, cross-checking each displayed money
string against the numeric value stored in the sheet.

## Verified against source

Confirmed by hand from the source documents: 2017's block is exactly 11 rows bounded
by Tipton; 2019's Shoals figures ($7,947,200 / $1,041,940) are genuinely what was
filed, not a parse artefact; 2016's Bradford `$0` estimated value is likewise real.

Not yet verified line by line — spot checks only. Anything headed for print should
be checked against the PDF first.
