# www/sumner_pilot_tracker_v2/js/

## Purpose
The data and rendering logic that builds the entire tracker page — a deliberate split so that adding data is never an HTML edit.

## Contents
- `county-data.js` — county-wide PILOT totals across all entities/years (not entity-specific)
- `entities/{entity}.js` — one file per tracked entity (11 total): PILOT filings by year (headers/rows/totals/notes), plus that entity's `docs` object (Overview/Assessment Data/Key Findings & Notes/Unanswered Questions/Council Notes/IRS Filings content). Generated from `sumner_county/sumner_entities/{entity}/memory/MEMORY.md`, not hand-maintained directly.
- `tracker-render.js` — builds the nav, tab panels, tables, and sidebar pie-chart geometry from all of the above. Nothing entity-specific lives here.

## Source Type
**Output Artifact** — not a source; the actual facts trace back to `state_of_tennessee/tn_comptroller_pilot_reports/`, `state_of_tennessee/tn_property_assessments/`, `usa_federal/irs_990_data/`, and the corresponding `sumner_county/sumner_entities/{entity}/memory/MEMORY.md`.

## Handling Instructions
- New year of data for an existing entity → edit `entities/{entity}.js` directly (or regenerate it from that entity's memory, if the memory was updated first)
- New entity → new `sumner_county/sumner_entities/{entity}/` directory + memory, new `entities/{entity}.js`, new `<script>` tag and `ENTITIES_DATA` array entry in `index.html`
- New UI behavior or layout logic → `tracker-render.js`
- `entities/{entity}.js` and `sumner_county/sumner_entities/{entity}/memory/MEMORY.md` are two different files with no automatic sync (symlinks were tried, dropped as unreliable here) — if they disagree, treat it as a real possibility and reconcile by hand, don't assume they match

## Notes
None.
