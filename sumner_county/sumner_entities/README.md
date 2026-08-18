# sumner_county/sumner_entities/

## Purpose
Per-entity working notes for all 11 corporations known to have a Sumner County IDB PILOT agreement (2015–2026), one subdirectory each — general-purpose homes for everything about that entity, not just what the tracker needs.

## Contents
11 subdirectories: `beretta/`, `bradford/`, `woolhawk/`, `shoals/`, `solon/`, `nasg/`, `unipres/`, `stev_ham/`, `archer/`, `gap_inc/`, `ata_retail/`. Each has a `memory/MEMORY.md` for that entity's findings — this is the actual source of truth. Beretta is the only one with the full treatment (Promises Made/Kept, Assessment Data, Key Findings, Unanswered Questions) — the other 10 are populated with whatever's already been established in conversation/tracker data (totals, anomalies, open questions) but haven't had the full research pass yet.

## Source Type
**Working Material** — analysis and notes we've produced, not primary source documents. See each entity's own README for where its real source material lives.

## Handling Instructions
- Not citable as fact on its own — always trace back to the primary source directories (`state_of_tennessee/tn_comptroller_pilot_reports/`, `state_of_tennessee/tn_property_assessments/`, `usa_federal/irs_990_data/`, `sumner_county/gallatin_idb_data/`, etc.)
- Directory names are shorthand, not always the exact corporate name — check the entity's own README for the full legal name
- ~~`www/sumner_pilot_tracker_v2/js/entities/{entity}.js` is generated from the corresponding `memory/MEMORY.md`, not symlinked or otherwise auto-synced — regenerating it is an explicit step whenever the memory changes in a way that should show up on the site~~
  > **The PILOT tracker was deleted 2026-08-17** along with the rest of `www/`. The generation step described below no longer applies; nothing is generated from this memory today. If a data-driven view is ever rebuilt, it should be generated at build time from the sources rather than hand-maintained. See `files/DATA_MAP.md`.

## Notes
Created July 2026, replacing an earlier plan to dump all entity-specific findings into the single project-level `memory/MEMORY.md` — that didn't scale past a couple of entities. `memory/MEMORY.md` now stays reserved for cross-entity theories and patterns (the rogue-IDB thesis, the rent-mechanism finding, etc.), not entity-specific facts. An earlier plan to make each entity's site data a symlinked `site/` subdirectory was also dropped — symlinks "proved unreliable," which was solved 2026-07-06: the Documents mount carried a `nosymfollow` fstab option that let symlinks be created but never followed. That option has since been removed (fstab backup: `/etc/fstab.bak-20260706`), so symlinks now work normally here — the generated-copy convention for tracker data remains by choice, not necessity.
