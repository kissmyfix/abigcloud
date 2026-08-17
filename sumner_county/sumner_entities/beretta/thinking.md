# Thinking Notes — Beretta Land Chain of Title & State Grant (2026-07-01)

Recap of the live thread, in order, so the reasoning doesn't get lost.

## 1. Where this started
The 2014 TN Fiscal Review Committee cumulative fiscal note (`state_of_tennessee/tn_annotated_code/2014-06-12-cumulative-fiscal-note-2014-session.pdf` (formerly `2014-tn-bill-beretta.pdf`; the Beretta entry is item 813, p.46)) surfaced Public Chapter 813 (SB2600/HB2502, 108th GA): a $167.6M state general obligation bond bill that included **$8,000,000 in grants to the Industrial Development Board of the City of Gallatin for the Beretta U.S.A. Corp. project**. Passed House 75-16, Senate 31-0, signed by Gov. Haslam 5/16/2014, effective 4/25/2014. Confirmed as Tennessee's standard FastTrack Infrastructure Development Program mechanism — same bill gave $44.4M to the Montgomery County IDB for Hankook Tire the same year. This was a public, roll-call-voted appropriation, not a secret one — a different animal from the sealed Woolhawk PILOT agreement.

Press-reported total incentive stack for Beretta: ~$1.75M in land (100 acres) + ~$2.2M 10-year local property tax abatement (city-administered via the IDB) + "more than $10 million" in state capital and training grants (the $8M FastTrack grant likely being the capital-grant component of that $10M+ figure).

Brandon's read: this state-grant apparatus is a separate mechanism from the PILOT/990/rent story and shouldn't become a rabbit hole on its own — but it raises the question of whether Gallatin was actively lobbying both Beretta and the state to land this grant, and whether the IDB used the $8M to develop the land specifically to entice Beretta.

## 2. The land chain-of-title puzzle
Working from `state_of_tennessee/tn_property_assessments/sumner-assessment-beretta.pdf` (parcel PB28 PG193-194 LT4, Ctrl Map 112, Parcel 012.02). Verified sale history, chronological:

| Date | Price | Book/Page | Instrument | Vac/Imp | Qualification |
|---|---|---|---|---|---|
| 6/11/1957 | $0 | WB12/21 | — | Vacant | — |
| 12/31/1975 | $0 | 360/571 | — | Vacant | — |
| 1/27/1976 | $0 | 361/627 | — | Vacant | — |
| 7/10/1987 | $0 | 541/517 | — | Vacant | — |
| 5/12/2008 | $1,452,332 | 2962/797 | Warranty Deed | Vacant | Multiple Parcels |
| 5/13/2008 | $3,615,848 | 2962/802 | Warranty Deed | Vacant | Multiple Parcels |
| 5/14/2008 | $0 | 2962/808 | — | Vacant | — |
| 7/28/2014 | $0 | 3983/136 | Quitclaim Deed | Improved | — |
| 8/7/2014 | $170,922 | 3983/425 | Warranty Deed | Vacant | — |
| 8/28/2014 | $0 | 4001/628 | Quitclaim Deed | Improved | — |
| 12/13/2017 | $0 | 4673/606 | Easement | Vacant | — |

Note: the 2008 entries are three straight days (5/12 → 5/13 → 5/14), not spread over two weeks as first estimated — tightens the case that these were linked transactions, not coincidental timing.

**Brandon's working theory, in his own reasoning (preserved as stated, including his self-correction mid-thought):**

> Party A buys land for $1.45M on 5/12/2008, sells to Party B the next day for $3.61M — doubling the value overnight. Six years later Party B quitclaims to Party C for $0 (7/28/2014). Party C sells to Party D a week later for $170,922 (8/7/2014). Party D quitclaims two weeks later to Party E for $0 (8/28/2014). Working backwards, Party E is likely the IDB of Gallatin, Party D is likely Beretta USA being "given" the land for free. But who are A, B, and C? Party A had a potential windfall; Party B apparently accepted losing $3.6M in value by quitclaiming for $0 six years later — unless Party B and Party C are functionally the same actor and the "loss" is illusory (a related-party transfer, not an arms-length one).
>
> Initial hypothesis was that the IDB itself was the 2008 purchaser, holding the land dormant until 2014 — consistent with 2008 being the year Leon's report says the IDB's tiered-PILOT framework began. **Brandon corrected this mid-thought**: that can't be right, because the mechanism established elsewhere in this investigation is that quitclaims-for-$0 are how land moves *into* IDB ownership to trigger the tax exemption — not how the IDB would dispose of land it already held. The 7/28/2014 quitclaim is far more likely the transfer that first brought the parcel into IDB custody, meaning something else (a private buyer, possibly Beretta itself, or an intermediary entity) held the land from 2008 to 2014.
>
> This leaves an unresolved question: if the IDB didn't hold this land from 2008–2014, who did, and why did it change hands three times in six years (2008 purchase → 2014 quitclaim → 2014 warranty deed resale → 2014 quitclaim again) before landing with the IDB? There may be a third, not-yet-named party whose involvement explains the warranty-deed sale sandwiched between the two 2014 quitclaims.

## 3. New finding: the mailing address parallel
Current owner record: **"GALLATIN CITY OF IDB, DANA A FRAZIER C/O, 17601 BERETTA DRIVE, ACCOKEEK MD 20607."** Accokeek, MD is the town of Beretta's original U.S. plant — the one they left over Maryland's post-Newtown gun legislation. The Gallatin IDB's own property tax correspondence for land it holds in Tennessee is routed to a Maryland address bearing Beretta's name, care of an individual (Dana A. Frazier) not otherwise identified in this investigation.

This is the same structural pattern already logged in project memory for Woolhawk (IDB's landlord mail routed to Meta's Menlo Park HQ rather than Gallatin) — see the open follow-up item in `memory/MEMORY.md`: "Check parcel mailing-address-on-file for all 11 entities — how many reroute the IDB's own landlord mail to the tenant side." Beretta is now a second confirmed instance of the same routing pattern, a decade before Woolhawk. Strengthens the "standing IDB playbook across multiple deals" theory already logged (see the corrected board-reinstatement sequence entry in `memory/MEMORY.md`).

## 4. Open threads to chase
- Pull the actual recorded deeds for Book/Page 2962/797, 2962/802, 2962/808, 3983/136, 3983/425, 4001/628 from the Sumner County Register of Deeds — these will name the real Party A through E and resolve the chain-of-title question directly rather than by inference.
- Identify Dana A. Frazier — role, relationship to Beretta or the IDB.
- Confirm whether the 5/12–5/14/2008 sequence and the 7/28–8/28/2014 sequence are, in fact, related — or whether the 2008 activity was unrelated land assembly that only later got pulled into the Beretta deal.
- Reconcile timing: the state bond bill was effective 4/25/2014 and signed 5/16/2014 — meaning it predates all three 2014 land transactions (7/28, 8/7, 8/28). Consistent with the state grant enabling site work/acquisition ahead of the transfer into IDB hands, but not yet confirmed.
- See `idb-beretta-deal.md` in this same directory for the separate, still-open questions about the $2.2M PILOT tax savings, the $45M investment vs. the current $19.1M total appraisal, and whether the 10-year PILOT term has actually expired given the parcel still shows a 0% assessment percentage in Tax Year 2026.
