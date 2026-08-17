# www/sumner_pilot_tracker_v2/

## Purpose
The live, actively-maintained Sumner County PILOT tracker — a data-driven, per-entity/per-year visualization of every known IDB PILOT agreement in Sumner County, plus per-entity working notes (Overview, Assessment Data, Key Findings & Notes, Unanswered Questions, Council Notes, IRS Filings).

## Contents
- `index.html` — thin HTML shell; loads the CSS/JS below and mounts the rendered page
- `css/tracker.css` — all styling (design tokens ported from abigcloud.com, layout, components)
- `js/county-data.js` — county-wide PILOT totals (not entity-specific)
- `js/entities/{entity}.js` — one file per tracked entity: PILOT filings by year, plus the `docs` object holding that entity's Overview/Assessment/Findings/Questions content. Each is generated from `sumner_county/sumner_entities/{entity}/memory/MEMORY.md` — see that directory for the actual source of truth.
- `js/tracker-render.js` — render logic that builds the entire page (nav, tabs, tables, sidebar pie charts) from the files above; nothing entity-specific lives here
- `img/` — currently empty, reserved for future visual assets

## Source Type
**Output Artifact** — this is the investigation's output, not a source. Every figure it displays traces back to `state_of_tennessee/tn_comptroller_pilot_reports/`, `state_of_tennessee/tn_property_assessments/`, `usa_federal/irs_990_data/`, or the corresponding `sumner_county/sumner_entities/{entity}/memory/MEMORY.md`.

## Handling Instructions
- Adding a new entity means: a new `sumner_county/sumner_entities/{entity}/` directory, a new `js/entities/{entity}.js` generated from its memory, a new `<script>` tag in `index.html`, and adding its global to the `ENTITIES_DATA` array assembled inline in `index.html`. Adding a new year for an existing entity is just a data change in that entity's `js/entities/{entity}.js`.
- `js/entities/{entity}.js` is generated, not hand-maintained — the real editing happens in `sumner_county/sumner_entities/{entity}/memory/MEMORY.md`, then gets ported over as an explicit step. These two are not automatically kept in sync (symlinks were tried and dropped — unreliable in this environment), so treat a stale `js/entities/` file as a real possibility, not paranoia.
- Prefer fixed dimensions over content-derived/flex-fill sizing for anything the user can click between (tabs, years, doc categories) — this page has already had a multi-session bug from doing it the "smart"/flexible way
- Watch for CSS specificity when layering a new feature-specific rule on a shared base class (e.g. `.panel`) — a more specific selector only overrides the properties it explicitly sets, not the whole rule
- Verify layout fixes against a real screenshot from an actual browser session when possible — headless-screenshot self-verification has proven unreliable for this page more than once

## Notes
This directory is the successor to `visualizations/sumner_pilot_tracker.html` (original monolithic build, deleted July 2026) and `visualizations/sumner_pilot_tracker_v2.html` + its loose `tracker.css`/`tracker-data.js`/`tracker-render.js` (also deleted July 2026 once copied here). This is now the one true copy — don't resurrect or edit the old `visualizations/` files.
