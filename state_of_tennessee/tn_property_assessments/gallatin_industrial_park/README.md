# Gallatin industrial park parcels, Tax Year 2026

Parcel Details Reports for every parcel collected in and around the Gallatin industrial
park, control maps 105, 106, 111 and 112. Gathered 2026-08-29 by clicking the state parcel
viewer, because the assessor's owner field cannot be searched reliably (see below).

## Source Type

**Primary Source.** Official state assessment records, from the Tennessee Property
Assessment Data site (assessment.cot.tn.gov), reached through the parcel viewer at
tnmap.tn.gov. Born-digital browser renderings of the state's own report, not scans: the
text is authoritative and greppable. Retrieved 2026-08-29.

## Files

| File | What it is |
|---|---|
| `sumner-parcel-<map>-<parcel>.pdf` | One Parcel Details Report per parcel. Named by control map and parcel number, which is the only identifier on these records that is stable. |
| `derived/*.txt` | Page-anchored extractions, `files/bin/pdf-extract.py`. |
| `derived/parcels.csv` | **The dataset.** One row per parcel: parcel, address, owner, acres, appraised, assessed. Machine-generated. |
| `derived/pdf-index.csv` | Extraction index and trust bucket per file. |

29 parcels, 1,632.72 acres, $586,256,800 appraised, $2,856,660 assessed.

## Why these were collected by hand

**The owner field cannot be searched.** The assessor's records carry at least seven
different strings for the Gallatin Industrial Development Board:

    INDUSTRIAL DEV BRD OF CITY OF GALLATIN
    INDUSTRIAL DEVELOPMENT BOARD OF THE CITY
    INDUSTRIAL DEVELOPMENT BOARD OF THE CITY OF GALLATIN
    INDUSTRIAL DEVELOPMENT BOARD OF THE CITY OF GALLATIN TENNESSEE
    INDUSTRIAL DEV BD GALLATIN CITY
    GALLATIN CITY OF IDB
    GALLATIN CITY OF IDB DANA A FRAZIER C/O

No single owner search returns them all, and `GALLATIN CITY OF IDB` contains neither the
word "industrial" nor "board". Elsewhere in the archive the same body appears as
`INDUSTRIAL DEVELOPEMENT`, `INDUSTRIAL DEVELOPMNET` and `INDUSTRIAL DEVELPMENT`.

**The fix is `state_of_tennessee/tn_property_assessments/classification_index/`.** Searching by classification code returns a
complete list with parcel IDs, which is how three IDB parcels missed by map-clicking were
found, including two outside the industrial park entirely, on Belvedere Drive and Airport
Road.

## What the records show

**Thirteen parcels are held by the IDB across the county, all inside city limits.** Ten of
them are in this directory. Every one is assessed at **$0**. Eight name
`C/O WOOLHAWK LLC ATTN: TAX, 1601 Willow Rd, Menlo Park CA` as the tax contact. Woolhawk
is the Meta shell, and not one of those eight has a building on it.

The exemption itself is the ordinary PILOT mechanism and is already explained in the
article: the board owns the title, so the property is exempt. What was not known before
this collection is the **extent**: roughly 900 acres, $567.7M of appraised value.

**Two anomalies worth chasing.** `111-00200` (51.03 ac, $4,659,000) is coded `16 - IND PARK`
and `112-01206` (28.56 ac, $10,388,500) is coded `15 - INDUSTRIAL`. Neither carries the
`70 - EXEMPT` land code every other IDB parcel here carries, yet both are assessed at $0.
Under T.C.A. § 67-5-801 industrial property is assessed at 40%. Whether the exemption is
applied by owner rather than by land code is a question for the assessor.

**`112-01204`, GALLATIN DATA CENTERS LLC**, 32.83 acres, is assessed at $525,280 and pays.
That entity is not Woolhawk and had not appeared in this investigation before 2026-08-29.

## Handling

Read `derived/parcels.csv` for figures. Open a PDF only to verify one, or to read the sale
history, which the CSV does not carry.
