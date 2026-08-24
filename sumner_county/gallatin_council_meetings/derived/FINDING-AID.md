# Finding Aid — gallatin_council_meetings/

What is *in* the 24 council and committee documents in the parent directory, and where.

`council-index.csv` beside this file records provenance: extraction method, OCR quality,
page counts, date agreement between masthead and filename, duplicates, md5. That answers
"can I trust this file." This answers "what is in it."

Built 2026-08-24 by full-text search across every extraction, including the OCR set.

---

## Read this first: most of these are OCR, and the text is a guess

`council-index.csv` marks the agendas `OCR_SCAN` with `quotable: verify`. The extractions
contain visible errors — `cornmemorate`, `constructin`, `lndustria!`, `appropria ting`.

**Every quotation below is a machine's reading and must be checked against the page image
before it reaches a published page.** They are recorded here so you know which page to open,
not so they can be pasted.

---

## The hot documents

Ranked by density of subject matter. Everything else is routine city business.

| Document | IDB | PILOT | FB/Meta | Woolhawk |
|---|---:|---:|---:|---:|
| `2020-05-12-council-committee-agenda` | 10 | 19 | 0 | 9 |
| `2020-05-12-r2005-24-woolhawk-pilot-terms` **(cited)** | 10 | 18 | 0 | 8 |
| `2020-09-15-city-council-agenda` | 0 | 0 | 2 | 8 |
| `2020-10-06-city-council-agenda` | 0 | 0 | 2 | 8 |
| `2020-06-09-council-committee-agenda` | 4 | 3 | 0 | 1 |
| `2021-01-12-council-committee-agenda` | 5 | 0 | 0 | 0 |
| `2021-02-02-city-council-agenda` | 2 | 0 | 0 | 5 |
| `2022-04-19-city-council-agenda` | 0 | 0 | 2 | 2 |
| `2019-gallatin-annual-financial-report` | 5 | 16 | 0 | 0 |
| `2022-gallatin-annual-financial-report` | 3 | 10 | 0 | 0 |

Only `2020-05-12-r2005-24-woolhawk-pilot-terms` is cited by a published page. The other
nine are not.

---

## Located items

### 2020-09-15 council meeting — the codename is dropped in public

Line 225 of the extraction, in the Mayor's announcements:

> Mayor announced Project Woolhawk is Facebook. She thanked the Economic Development
> Agency Director James Fenton and staff, the Economic Development Agency Board and
> Department Heads.

This is the moment the project's codename is publicly tied to the company, on the record,
with a date and a named thanks. Two lines later the same document refers to infrastructure
"currently under constructin in the Gallatin lndustria! Center to serve the new Facebook"
facility (line 752).

For sequencing against the Woolhawk PILOT resolution of 2020-05-12, four months earlier.

### 2022-04-19 council meeting — Meta pays for Gateway Drive

An ordinance appropriating **$687,741.00** from *Donations from Businesses* to Gateway
Drive Extension Construction. Presented by Councilman Overton, seconded by Councilman Fann.

> EDA Director James Fenton explained the reason for this change and confirmed that META is
> paying for the construction.
>
> Councilwoman George stated that META paid approximately four million dollars for the
> extension of Gateway Drive and created another needed safety access to the industrial
> center.

Motion carried 6 ayes, 0 nays.

**Note the two figures.** The ordinance appropriates $687,741; the councilwoman describes
approximately $4 million. They are not necessarily in conflict — one is a single
appropriation and the other a characterisation of total spend — but nothing in the document
reconciles them, and either figure quoted without the other would misrepresent the page.
Read the full ordinance before using either.

Also note the accounting: Meta's money enters the City as *Donations from Businesses*.

### 2020-10-06 council meeting

Two Facebook mentions, neither substantive. One records that the live-stream was
unavailable on Facebook the platform (line 104) — a false positive for any keyword search.
The other, line 503, has the Mayor requesting council discussion to allow Facebook to work
24 hours, which is a construction-hours variance.

### 2020-05-12 — the Woolhawk PILOT pair

Two documents from the same date. `r2005-24-woolhawk-pilot-terms` is the resolution and is
already cited. `2020-05-12-council-committee-agenda` is the committee agenda around it and
is **not** cited, despite carrying comparable density (10 IDB, 19 PILOT, 9 Woolhawk). If the
article characterises what the committee was told or asked, this is the document that
carries it.

### The two annual financial reports

`2019-gallatin-annual-financial-report.pdf` and `2022-gallatin-annual-financial-report.pdf`
sit in this directory rather than under `state_audits/gallatin_city/`, which holds FY2015
through FY2025 of the same series. Both are `DIGITAL` with authoritative extraction, unlike
the OCR'd agendas around them.

**They are not duplicates. Do not delete either one.**

### FY2019 exists here in two versions, and they disagree

| | This directory | `state_audits/gallatin_city/` |
|---|---|---|
| File | `2019-gallatin-annual-financial-report.pdf` | `1688-2019-c-gallatin-rpt-cpa6-12-31-19.pdf` |
| Pages | 120 | 120 |
| PDF created | 28 Dec 2019 01:21:32 | 28 Dec 2019 01:21:32 |
| PDF modified | **30 Dec 2019** | **9 Jan 2020** |
| md5 | `641cdd7b2244…` | `5ebef9d1e7a1…` |

Identical title page, identical page count, identical creation timestamp. The copy under
`state_audits/` was modified ten days later and is the **later version**. Text extractions
differ across 431 lines.

**What changed.**

*Three names in the directory of officials.* The earlier version lists Anne Kemp, Ronald E.
Mayberry and Julie Brakenbury as council members. The later version lists Linda Love,
Steve Fann and Shawn Fennell in those positions. A December-to-January swap spanning a
change of council is an ordinary explanation and has not been confirmed.

*A consistent $47,500, in three places.* Earlier version first, later version second:

| Line | Earlier (30 Dec) | Later (9 Jan) | Δ |
|---|---|---|---|
| Charges for services | $104,226,929 | $104,274,429 | +$47,500 |
| Total revenues | $109,363,702 | $109,411,202 | +$47,500 |
| General government | $10,146,985 | $10,194,485 | +$47,500 |

Narrative figures in the MD&A move with it: $15.42M becomes $15.47M, $11.64M becomes
$11.68M, $30.90M becomes $30.95M, and transfers of ($1.56M) become ($1.61M).

**Status: unexplained.** A revision to an audited financial statement between filings is
ordinary in itself; nothing here establishes why this one happened or whether it was
disclosed. What the archive can say is that two versions exist, which one is later, and
exactly what moved. **Cite the 9 Jan 2020 version as the report of record**, and if the
earlier one is ever quoted, say which version it is.

### FY2022 is a true duplicate

Run 2026-08-24. Both copies are 142 pages, share a creation timestamp of 31 Dec 2022
13:29:17, and their text extractions are **byte-identical** — zero differing lines,
458,653 characters each. The PDFs differ only in metadata and modification date.

Cite `state_audits/gallatin_city/1688-2022-c-gallatin-rpt-cpa811-12-31-22.pdf`. The copy
here is redundant and can go whenever the tree is next tidied.

The FY2019 pair above was checked the same way and is **not** the same case. Do not
generalise from one to the other.

---

## Search notes

```
grep -n -i "term" *.txt ocr/*.txt
```

- **`ocr/` holds a second extraction of several documents.** `council-index.csv` records
  which text file is authoritative per source PDF. Searching both directories returns the
  same passage twice.
- **"Facebook" is not a reliable proxy for the company here.** It also means the streaming
  platform the council meetings were broadcast on.
- **"in lieu of tax" in the annual financial reports is the utility's payment to the City**,
  a different mechanism from an IDB PILOT.
