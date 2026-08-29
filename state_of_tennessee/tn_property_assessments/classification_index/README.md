# Sumner County parcels by classification code, 2026-08-29

Thirteen CSV exports from the Tennessee Property Assessment Data search
(assessment.cot.tn.gov), one per classification code the search offers, covering Sumner
County. Retrieved 2026-08-29.

## Source Type

**Primary Source, index only.** These are the state's own search results, not full records.

## Files

| File | Classification |
|---|---|
| `2026-08-29-sumner-class-city.csv` | 02 - City |
| `2026-08-29-sumner-class-county.csv` | 01 - County |
| `2026-08-29-sumner-class-residential.csv` | 00 - Residential |
| `2026-08-29-sumner-class-commercial.csv` | Commercial |
| `2026-08-29-sumner-class-industrial.csv` | Industrial |
| `2026-08-29-sumner-class-agricultural.csv` | Agricultural |
| `2026-08-29-sumner-class-farm.csv` | Farm |
| `2026-08-29-sumner-class-religious.csv` | Religious |
| `2026-08-29-sumner-class-edu-sci-char.csv` | Educational / scientific / charitable |
| `2026-08-29-sumner-class-other-exempt.csv` | Other exempt |
| `2026-08-29-sumner-class-state.csv` | State |
| `2026-08-29-sumner-class-state-assessed.csv` | State assessed |
| `2026-08-29-sumner-class-federal.csv` | Federal |

## What is and is not in them

Eleven columns: Owner, Property Address, Control Map, Group, Parcel, Special Interest,
Parcel ID, Subdivision, Lot, Class, Sale Date.

**No acreage. No appraised value. No assessment. No land code. No deed history. No owner
mailing address.** Every figure this investigation has drawn from parcel records lives in
the PDF, not here.

**These are a finding aid, never a substitute for the record.** They answer "what exists
and where," completely, in one query. Pull the Parcel Details PDF for anything else.

## Why this set matters

The owner name cannot be searched reliably. The Gallatin IDB appears under at least seven
different strings (listed in `state_of_tennessee/tn_property_assessments/gallatin_industrial_park/README.md`). Classification is a
structured field that cannot be spelled seven ways, so enumerating every code gives a
complete typed index in which an IDB parcel must appear somewhere regardless of how its
owner name was typed.

Querying, no import needed:

    duckdb -c "select * from read_csv_auto('2026-08-29-sumner-class-*.csv', union_by_name=true, filename=true) where upper(Owner) like '%INDUSTRIAL%'"
