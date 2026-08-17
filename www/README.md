# www/

## Purpose
Home of the actual website root directories — the deployable/servable artifacts of this investigation, as opposed to the working data and drafts that live everywhere else in the project.

## Contents
- `SITE_PLAN.md` — **read this first for any site work**: the locked 2026-07-06 decisions for the combined-site rebuild (stack, schema, two-axis architecture, pipeline, security posture, phases)
- `abigcloud_v2/` — the active rebuild: Astro static site, local git repo, own README with repo mechanics. Phase 1 (verbatim migration) + step-2 wiki skin complete; supersedes the tracker and, at deploy time, `abigcloud.com/`
- `sumner_pilot_tracker_v2/` — the Sumner County PILOT tracker, the active data-driven build (slated to be superseded by the rebuild's dossier/wiki phase)
- `abigcloud.com/` — a local working copy of the live investigation site, for reference now and direct editing later
- `idb_comparisons` - a single page for cycling through the IDB data by year and create comparisons from the data.

## Source Type
**Output Artifact** — these are what the investigation produces for public consumption, not source material for it.

## Handling Instructions
- Don't treat anything here as a source of facts — every figure traces back to a source directory elsewhere in the project (`state_of_tennessee/tn_comptroller_pilot_reports/`, `state_of_tennessee/tn_property_assessments/`, `usa_federal/irs_990_data/`, etc.)
- Frameworks, build steps, and tooling are all on the table when they serve the site — the constraint is that Brandon can explain the stack (he'll learn what he doesn't know yet), not that tooling is forbidden. Don't pre-reject an approach to protect a "no build step" rule; propose the best tool for the job and note what it adds
- Keep deployed output self-contained and document any build step in the subdirectory's README (what generates what, and the command to run)
- `abigcloud.com/` is a snapshot of the live site as of when it was copied in, not necessarily current — re-pull from the live site before assuming it's up to date

## Notes
Created July 2026 when the Sumner PILOT tracker moved out of `visualizations/` (a drafts folder) into a proper site-root structure. `abigcloud.com/` was added at the same time in anticipation of future work on the main site, not because anything here needed it today.
