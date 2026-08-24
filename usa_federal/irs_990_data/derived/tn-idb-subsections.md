# Tennessee IDBs by 501(c) subsection

**Corrected 2026-08-24. Seven of the eight are 501(c)(6) business leagues. None is a
501(c)(3).** The earlier version of this file said three were 501(c)(3) charities. That was
wrong, it was drafted into the article, and the article has since been corrected. This file
is the correction of record.

Reproduce the underlying pull with `files/bin/tn-idb-subsections.py`. **That script reads
ProPublica's republication of the IRS Business Master File, which carries the wrong
subsection codes for three of these boards. Re-running it will reproduce the error. Do not
overwrite this file with its raw output.**

Search: organisations in Tennessee matching "industrial development board" that have
filed a Form 990. This is the population of IDBs the IRS has filings for, not the
population of IDBs that exist.

| EIN | Organisation | City | Subsection | NTEE |
|---|---|---|---|---|
| `621333401` | The Industrial Development Board Of Grainger County Tennessee | Rutledge | **501(c)(6) business league** | None |
| `581894755` | Industrial Development Board Of Smithville Tn | Smithville | **501(c)(6) business league** | None |
| `582098755` | Industrial Development Board Of Crockett County Tennessee | Alamo | **501(c)(6) business league** | W01 |
| `384171308` | Industrial Development Board Of The Gallatin Tn | Gallatin | **501(c)(4) social welfare** | None |
| `202703372` | Industrial Development Board Of Gibson County Tennessee | Trenton | **501(c)(6) business league** | S20 |
| `621248814` | Industrial Development Board | Mc Kenzie | **501(c)(6) business league** | None |
| `621373320` | The Industrial Development Board Of The City Of Trenton Tennessee | Trenton | **501(c)(6) business league** | None |
| `621150835` | The Industrial Development Board Of The County Of Mcminn | Athens | **501(c)(6) business league** | None |

## Distribution

- **501(c)(6) business league** — 7
- **501(c)(4) social welfare** — 1
- **501(c)(3) charitable** — 0

## The finding

Of the 8 Tennessee Industrial Development Boards with IRS filings, exactly one is
classified **501(c)(4)**: the Industrial Development Board of the Gallatin TN,
EIN 38-4171308. **Every other one files as a 501(c)(6) business league.**

A 501(c)(6) is a business league — the chamber of commerce category, and the obvious fit
for a board whose whole job is recruiting industry. A 501(c)(4) is a social welfare
organisation, the category that holds advocacy groups. It can lobby without limit, spend on
politics, and never say who paid for it.

Gallatin is the only one of the eight that is not a business league.

**Scope.** This establishes uniqueness among *filers*. It does not establish the total
number of IDBs chartered in Tennessee -- that figure needs its own source.

**Provenance of the correction.** The 501(c)(3) codes in the earlier version came from the
IRS Business Master File as republished by ProPublica. Brandon's determination is that no
Tennessee IDB files as a charity and that the federal record is wrong on those three. On
this investigation's subject matter his unhedged determination outranks the archive; see
the project `CLAUDE.md` under *Evidence discipline*.
