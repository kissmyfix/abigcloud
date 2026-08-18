# How many Industrial Development Boards are there in Tennessee?

**423**, by the count described below. Recorded 2026-08-17.

## There is no official number

No Tennessee agency publishes a register of Industrial Development Boards. The Comptroller
publishes PILOT reporting, but only for boards that report. The IRS lists only the eight
that file a Form 990. The Secretary of State registers IDBs as corporations, but does not
categorise them as a class.

So the figure has to be counted, and the count has to state its method.

## The method

Search the Tennessee Secretary of State business entity register:

**https://tncab.tnsos.gov/portal/business-entity-search**

Query for variations of "Industrial Development Board" — the boards are not consistently
named. Real examples from the IRS filer list alone show four different constructions:

- `Industrial Development Board Of The Gallatin Tn`
- `The Industrial Development Board Of The City Of Trenton Tennessee`
- `The Industrial Development Board Of The County Of Mcminn`
- `Industrial Development Board` *(Mc Kenzie, no place name at all)*

Counting the union of those variations gives **423** registered entities.

## What the number is and is not

**It is** a count of corporations registered with the Tennessee Secretary of State whose
names identify them as Industrial Development Boards.

**It is not** a count of currently active boards. The register includes dissolved and
administratively dissolved entities. The Gallatin IDB itself was administratively
dissolved in 2012 and reinstated in 2013, so it would have appeared throughout.

**It is not** an official figure, because none exists.

## Why it is still worth stating

The claim it supports does not depend on precision. The point is that hundreds of these
boards are registered in Tennessee, only eight have ever filed a federal return, and of
those eight exactly one filed as a 501(c)(4). Whether the denominator is 400 or 450, the
numerator is one.

Anyone who thinks the count is wrong can run the same search. That is the standard being
offered: not "trust this number", but "here is how it was produced, produce a better one."

## Related

- `usa_federal/irs_990_data/derived/tn-idb-subsections.md` — the eight filers and their
  subsections, from the IRS Business Master File via ProPublica. Reproducible with
  `files/bin/tn-idb-subsections.py`.
