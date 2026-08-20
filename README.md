# It's a Big Cloud
## abigcloud.com

---

**Data centers are being built across Middle Tennessee. This is the record of what they
cost, who agreed to it, and whether the promises were kept.**

The site is at [abigcloud.com](https://abigcloud.com). This repository is the evidence behind it.

---

## Why This Repository Exists

The site covers data centers: what they consume, what they are promised, and what the
public gets back. TVA and the ratepayers who fund it, the national picture, and the
Middle Tennessee sites in particular, from Gallatin to Memphis.

The source material behind this work is not linkable web content. It is meeting minutes, property assessments, federal tax filings, legislative archives, and audio recordings. Most of it exists as documents nobody has put online in any usable form.

So it lives here, in the open. Every document an article cites is also published on the site itself, listed at [abigcloud.com/sources](https://abigcloud.com/sources/), so a citation opens the document rather than a footnote. The originals are in this repository, organised by jurisdiction. If a claim is made, the document behind it is one click away and you can read it yourself.

Every document here is a public record or was obtained through lawful public channels. Nothing has been altered. Where documents came from public portals, the retrieval method and date are noted.

This is not a legal filing. It is not a formal complaint. It is not affiliated with any political party, advocacy group, or media organization. It is one resident's attempt to answer a simple question, **have the promises been kept?**, using only public records and primary sources.

If any claim is inaccurate, [open an issue](https://github.com/kissmyfix/abigcloud/issues). That is the point of putting it here.

---


## The Investigations

Investigations are the deep dives, where one deal gets followed all the way down. More
are coming. One has been carried to any real length so far.

| Investigation | Status |
|---|---|
| **[Quid-Pro-NO!](https://abigcloud.com/investigations/quid_pro_no/)** — Meta, Gallatin, the Industrial Development Board, and the PILOT structure | Part 1 published, in progress |

---

## The Evidence

Everything below is a primary source document or public record. Nothing has been altered. Where documents were obtained through public portals, the retrieval method and date are noted. The repo is organized by jurisdiction, the same way the failures stack.

It leans heavily toward Quid-Pro-NO right now. That is a reflection of what has been
worked so far, not of what the archive is for.

---

### `sumner_county/` — Where the Deal Lives

**`gallatin_idb_data/`** — The IDB itself: meeting minutes, agendas (when they exist), and everything specific to the board that controls the money.

| Key Document | What It Shows |
|---|---|
| IDB corporate history (SOS) | Chartered 1994, dissolved 2012, reinstated 2013. Registered agent changed from City Attorney → GEDA July 2018, mid-negotiation. Preston Stark current registered agent and 990 filer. |
| Woolhawk property assessment | $519M total appraised value. Assessment: **$0**. Six "Exceptional" commercial buildings on 512 acres. Land code: EXEMPT. |
| IDB meeting notices | Shared Monday 4:30 PM slot with a twin board. Same members, two names, depending on which hat is needed. |

**`gallatin_council_meetings/`** — City Council and work-session agendas from gallatintn.gov, 2019–2026. Key dates: May 12 and June 9, 2020 — the window around the land assembly closing at $8.27M (Book 5218, Page 424) and the quit-claim deeds transferring property into the IDB at $0.

**`sumner_entities/`** — Every corporation with a Sumner County PILOT agreement, 2015–2026. One directory per entity, each with its own `memory/MEMORY.md`. Includes Beretta, Bradford, Archer, ATA Retail, Gap Inc, NASG, Shoals, Solon, Stev-Ham, Unipres. These are the comparators — how did normal PILOT agreements work before the Woolhawk deal rewrote the playbook?

---

### `state_of_tennessee/` — Where the Rules Got Rewritten

**`tn_annotated_code/`** — The statutes that govern all of this.

| Statute | What It Controls |
|---|---|
| T.C.A. § 7-53-301 | IDB board composition — directors shall not be officers or employees of the municipality |
| T.C.A. § 7-53-302 | Corporate powers — all meetings shall be open to the public |
| T.C.A. § 7-53-305 | Tax exemption, PILOT authority, comptroller reporting, best-interest determination requirement |
| T.C.A. § 7-53-308 | Net earnings shall be paid to the municipality after expenses and obligations |
| T.C.A. § 67-5-502 | Property tax assessment — the section amended by SB0708 |
| T.C.A. § 8-44-110 | Open Meetings Act / Sunshine Law |

**`tn_comptroller_pilot_reports/`** — State comptroller PILOT reports, 2014–2025. Multi-county data. The Gallatin IDB is an outlier — compare its filings against Gibson County, Hamilton County, Portland, and Chattanooga to see the standard everyone else follows.

**`tn_property_assessments/`** — Property assessment records from the Tennessee parcel viewer. Woolhawk, Beretta, Bradford, TVA parcels. The Woolhawk assessment — $519M appraised, $0 assessed — is the clearest single document in this repo.

**SB0708 / HB1269 / Public Chapter 265** — The 2019 amendment.

| Document | What It Shows |
|---|---|
| `hb1269-sb708-as-introduced.pdf` | Original bill text — would have required PILOT payments equal to ad valorem taxes |
| `pc265-sb708-as-enacted.pdf` | Public Chapter 265 as signed — adds "or instrumentality thereof" to § 67-5-502(c) and (d). Passed April 18, signed April 30, 2019. Immediate effect. |
| `pc265-sb708-fiscal-memo.pdf` | Fiscal memorandum — original fiscal impact exceeding $2.72M rewritten to "unknown" and "not significant" after the amendment gutted the bill |

A statute untouched since 1955, amended during the Woolhawk negotiation window, adding the exact language the deal structure required. No public explanation for why it suddenly needed changing.

---

### `usa_federal/` — Where Nobody Was Looking

**`irs_990_data/`** — All available Gallatin IDB Form 990 filings (FY2020–2024), plus Gibson County IDB comparison filings.

| Tax Year | Key Findings |
|---|---|
| FY2020 | Marked "initial return." Claims formation year 2020 (actual: 1994). Tenants listed as beneficiaries. $999 internal discrepancy. "Summer County" (their typo). Three preparers across five years. |
| FY2021 | Board admits 990 not reviewed before filing. Largest expense: $107K in property taxes — a tax-exempt entity whose biggest line item is the thing it exists to not pay. |
| FY2022 | Mission statement rewritten, "no significant changes" checked. Cash→accrual accounting switch. First school payment: $74K. |
| FY2023 | Woolhawk money arrives. Revenue: $1.8M. School payment: $901K. Net assets balloon to $904K. The board is hoarding. |
| FY2024 | Revenue: $2.2M. Expenses: $3M. $2.29M flushed in a single line — "PILOT fees distributed" — to unnamed recipients. $45K consulting and $12K management fees to unnamed parties. Net assets collapse from $904K to $148K. Filed months ahead of the established pattern. |

The Gallatin IDB is the only one of 423 Tennessee IDBs filing as a 501(c)(4). It is not listed in the IRS Exempt Organizations Business Master File. Self-declared status. Fabricated formation year. No formal IRS recognition.

**`tva/`** — TVA material: in-lieu-of-tax payments, power agreements, capacity data. TVA doubled the Gallatin Steam Plant's capacity. A 161 KV transmission line runs through the middle of the Meta campus. The infrastructure was there — or was put there — before the public knew why.

---

### `the_players/` — Who Made This Happen

Profiles of individuals in scope. Key figures:

| Name | Role | Significance |
|---|---|---|
| James Fenton | GEDA Executive Director (~12 years; prior Cheatham County) | Negotiated Woolhawk. Signed Project Skillet NDA. Moved IDB registered agent to his own agency. Narrated the deal on a podcast without saying PILOT, IDB, or abatement once. |
| Lilibeth Leon | GEDA employee | Authored capstone report justifying IDB fund retention. Admitted agreement was deliberately written with ambiguous distribution language. |
| Preston Stark | IDB Director / registered agent / 990 filer | Signs the federal filings. Current registered agent since 2021. |
| Mayor Paige Brown | Mayor of Gallatin | City executive during the deal window |
| Randy Boyd | UT System president (Nov 2018–); former TNECD Commissioner (2015–16) | Candidate match for the successor who approved the trust land release after DiPietro said no |
| Sen. John Stevens | TN Senate | Sponsor, SB0708 |
| Rep. Andy Holt | TN House | Sponsor, HB1269 |
| Leonard Assante | IDB board member | Named on 990s |
| Susan High-McAuley | Former registered agent | Replaced by Stark in 2021; served during the deal negotiation window |
| Rosemary Bates | TCED capstone author (March 2021) | Wrote the earlier capstone referenced in Leon's report — established the "strategic recruitment" narrative |

---

### `podcasts/` — What They Said When They Thought Nobody Was Analyzing It

Raw audio (`mp3s/`), Whisper transcripts (`transcripts/`), and `manifest.csv` tracking source episodes. The Fenton interview is the centerpiece — a victory-lap narration of the entire Woolhawk saga where he describes maneuvering a university trust, calling in state senators, and resolving utility disputes weeks before announcement, then closes with "we didn't give them anything."

---

## Key Findings

**The IDB is a unicorn.** One of 423 Industrial Development Boards in Tennessee. The only one filing as a 501(c)(4). The only one absent from the IRS Exempt Organizations master file. Self-declared tax status with a fabricated formation year.

**The agreement was engineered for discretion.** The standard 35/65 city-county PILOT split was replaced with ambiguous language giving an appointed board control over distribution — a change documented and justified in an academic paper written by the deal team's own staff.

**A 64-year-old law was rewritten mid-deal.** SB0708, adding "or instrumentality thereof" to § 67-5-502, passed during the Woolhawk negotiation window with immediate effect. The fiscal memo's impact estimate collapsed from $2.72M to "unknown" between the original bill and the amendment. No public explanation for why a 1955 statute suddenly needed changing.

**Oversight was moved, not maintained.** The IDB's registered agent was transferred from the City Attorney — the independent legal office — to the economic development agency negotiating the deal, in July 2018, mid-negotiation.

**The same dollars were claimed three ways.** Meta's PILOT obligation payments were simultaneously presented as corporate philanthropy (Meta PR), strategic IDB distribution (City of Gallatin), and statutory compliance (IRS filings). Same money. Three stories. Depending on who's asking.

**The land was assembled through political relationships.** 800 acres, partly held in a university trust. The UT president said no. His successor — the state's former Economic Development Commissioner — said yes. Fenton describes the whole sequence on a podcast like a war story.

**Every safeguard either failed or was bypassed.** No public agendas. No posted minutes. No independent web presence. Ghost listing on the city website. Comptroller filings with no follow-up. Federal filings never verified by the IRS. Press coverage that never got past the press release.

---

## Repo Structure

```
abigcloud/
├── web/                         # The website. abigcloud.com is built from here.
├── the_players/                           # Profiles of individuals in scope
├── podcasts/
│   ├── transcripts/                       # 24 whisper transcripts, 13.2 hours of audio
│   └── manifest.csv                       # Episode source tracking
├── sumner_county/
│   ├── gallatin_idb_data/                 # IDB minutes, agendas, SOS filing history
│   ├── gallatin_council_meetings/         # City council PDFs from gallatintn.gov
│   └── sumner_entities/                   # All PILOT entities 2015-2026, one dir each
│       ├── woolhawk/                      # Meta
│       ├── beretta/
│       ├── bradford/
│       └── .../                           # Archer, ATA, Gap, NASG, Shoals, Solon, etc.
├── state_of_tennessee/
│   ├── tn_annotated_code/                 # T.C.A. statutory text, SB 708
│   ├── tn_comptroller_pilot_reports/      # State comptroller PILOT data by county
│   ├── state_audits/                      # Comptroller audits, one dir per entity
│   └── tn_property_assessments/           # Parcel viewer records
├── usa_federal/
│   ├── irs_990_data/                      # Gallatin IDB 990s 2020-2024 + comparisons
│   └── tva/                               # TVA in-lieu payments, power agreements
├── web_articles/                          # News coverage, saved with full provenance
└── files/                                 # Scripts, the directory map, tooling
```

Most PDFs have a `derived/` folder beside them holding page-anchored text, so the archive
is searchable rather than just downloadable. Anything saved from the web carries a header
recording its source, original URL, archive copy, and retrieval date.

**Reading the article:** [abigcloud.com/investigations/quid_pro_no/](https://abigcloud.com/investigations/quid_pro_no/).
Every citation there opens the document itself, and they are all listed at
[abigcloud.com/sources](https://abigcloud.com/sources/).

**Browsing PDFs on GitHub:** GitHub's in-browser preview often fails on large files. Use
"Download" or "Raw", or clone the repo.

---

## License

Four categories, four different answers. Full terms in [`LICENSE`](LICENSE).

| What | Terms |
|---|---|
| Original writing — the article, explainers, READMEs | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) |
| Original code — `files/bin/`, `web/src/`, `web/scripts/` | MIT |
| Government records — audits, 990s, PILOT reports, council packets | Public records. No rights claimed. |
| Third-party articles, transcripts, and saved pages | Copyright their publishers. Archived for reference, not licensed by this project. |

Attribution appreciated. Forks encouraged. If you own something in the fourth category and
want it removed, open an issue.
