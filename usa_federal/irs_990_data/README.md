# usa_federal/irs_990_data/

## Purpose
Federal 990 filings by the Industrial Development Board of the City of Gallatin, Tennessee — the most analytically dense primary source in the project.

## Contents
- `gallatin_idb/` — all publicly available Gallatin IDB 990 filings, 2020 (990-EZ) through 2024, plus the IRS search-results capture. `idb2020.pdf` is the as-filed graphic print (formerly `idb2020-verbose-version.pdf`); a content-identical ProPublica re-render was deduplicated 2026-07-05 after verifying the Part III program-service text matched.
- `gibson_county_idb/` — comparison filings from the only other TN IDB of comparable size that files 990s
- `gallatin_shalom_zone/` — 990s for Gallatin Shalom Zone Inc., EIN 62-1800512, whose filings
  are prepared by the same accountant as the IDB's. Moved into its own directory 2026-08-19
  from four loose files in this one.
- `irs_supporting_docs/` — IRS bulk financial-extract archives (2016–2024) and `irs990-501c-tn.png`, the ProPublica screenshot behind the eight-TN-IDBs count

## Source Type
**Primary Source**

Federal tax filings signed under penalty of perjury. The IDB's own self-reported documentation of governance, finances, and program activities.

## Handling Instructions
- Cite by filing year and specific part/line number
- Work methodically across filing years — changes between years are often more significant than what any single year says
- Key 990 findings (this list is the canonical index of them; verify against the filings in `gallatin_idb/` before citing):
  - 2020 990-EZ: $102,948 in beginning assets (disproves false 2020 formation date)
  - 2020 only: J. Michael Patterson as preparer, names Beretta and Bradford explicitly
  - 2021 forward: Joe Osterfeld CPA replaces Patterson; Bradford and Beretta disappear
  - Mission statement change: "recruit and facilitate industrial development" (2021) → PILOT payment administration (2022)
  - Part 3, 2022: significant program changes question answered No
  - IDB name evolution: "of the City of" quietly removed across three years
  - $45K consulting fee + $12K management fee in FY2024 with zero 1099s filed
  - Board non-review of filings per Stark's own disclosure
- The 501(c)(4) filing status — vs. 501(c)(6) for the other seven Tennessee IDBs that file — is itself a primary source finding; document it as such
- Cross-check every numeric figure against the actual filing (part and line number) before it goes into any analysis or draft — never carry a figure forward from working notes alone

## Notes
These filings are signed under penalty of perjury. Two problems on the same form — a false answer on Part 3 and a misleading mission statement that conflates Gallatin (city) with Sumner (county) — are documented in `memory/MEMORY.md` (working theories: "The 990 is the alibi") and the entity memory files. The 990 is the alibi. The paper trail runs elsewhere.
