---
title: 'Tennessee IDBs by 501(c) subsection'
description: 'Source document cited in the investigation.'
---

# **Tennessee IDBs by 501(c) subsection**

<p class="src-back"><a href="/sources/">All sources</a></p>

<p class="src-file"><a href="/sources/usa_federal/irs_990_data/derived/tn-idb-subsections.md" download>Download the original file</a> &middot; <code>tn-idb-subsections.md</code></p>

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

| EIN | Organisation | City | Subsection | Basis of that code | IRS ruling |
|---|---|---|---|---|---|
| `621333401` | The Industrial Development Board Of Grainger County Tennessee | Rutledge | **501(c)(6) business league** | BMF codes this c3 | 1993-01-01 |
| `581894755` | Industrial Development Board Of Smithville Tn | Smithville | **501(c)(6) business league** | self-reported, no BMF record | none |
| `582098755` | Industrial Development Board Of Crockett County Tennessee | Alamo | **501(c)(6) business league** | BMF codes this c3 | 2020-02-01 |
| `384171308` | Industrial Development Board Of The Gallatin Tn | Gallatin | **501(c)(4) social welfare** | **self-reported, no BMF record** | **none** |
| `202703372` | Industrial Development Board Of Gibson County Tennessee | Trenton | **501(c)(6) business league** | IRS determination | 2005-09-01 |
| `621248814` | Industrial Development Board | Mc Kenzie | **501(c)(6) business league** | IRS determination | 1991-11-01 |
| `621373320` | The Industrial Development Board Of The City Of Trenton Tennessee | Trenton | **501(c)(6) business league** | IRS determination | 1991-03-01 |
| `621150835` | The Industrial Development Board Of The County Of Mcminn | Athens | **501(c)(6) business league** | IRS determination | 1983-07-01 |

## Distribution

- **501(c)(6) business league** — 7
- **501(c)(4) social welfare** — 1
- **501(c)(3) charitable** — 0

## Why the earlier version said three were 501(c)(3)

The generating script read one field, `subsection_code`, for all eight organisations and
printed the results in a single column. **That field does not mean the same thing for every
row**, and the difference is the whole reason the table was wrong.

Two of the eight have **no IRS Business Master File record at all.** ProPublica marks them
`data_source: xml_backfill`, meaning the record was assembled by parsing filed 990 XML
rather than from the IRS master file. For those, the subsection is **a box the filer ticked
on its own return.** No application, no determination letter, no IRS ruling date, and
`exempt_organization_status_code` is null.

Those two are **Smithville and Gallatin.**

Smithville's 501(c)(3) came off three returns from 2013, 2014 and 2015, with total revenue
of $672, $1,521 and $2,650. It is a self-description on a near-dormant filing, and the
earlier table presented it beside genuine IRS determinations as though it were the same
kind of fact.

Grainger and Crockett do carry BMF records coding them 501(c)(3), with ruling dates and
deductible-contribution codes. Brandon's determination is that no Tennessee IDB is a
charity and that the federal record is wrong on those two. That is recorded here as the
finding of record; the underlying BMF codes are noted in the table above so nobody
rediscovers them and assumes the file is stale.

**The methodological point, which outlives this table.** A subsection code sourced from an
IRS determination and a subsection code sourced from a filer's own checkbox are different
grades of evidence. Any future table built off this API must carry the `data_source` field
alongside the code, or it will silently repeat this.

Gallatin is a self-declared 501(c)(4) with no IRS determination behind it, which is the
article's point and which this data confirms.

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

