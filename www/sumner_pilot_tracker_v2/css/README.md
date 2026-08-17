# www/sumner_pilot_tracker_v2/css/

## Purpose
Styling for the Sumner PILOT tracker — one file, no build step.

## Contents
`tracker.css` — design tokens (colors, fonts) ported from abigcloud.com's live CSS, plus all layout/component rules for the tracker (nav, tabs, tables, pie charts, promise boxes, bar charts).

## Source Type
**Output Artifact** — not a source; see `www/sumner_pilot_tracker_v2/README.md` for the full picture.

## Handling Instructions
- Color tokens should match abigcloud.com's actual live values — re-pull from the live site if this ever drifts, don't guess
- Default to fixed heights/widths for anything interactive (tabs, years, doc categories) rather than content-derived flex-fill sizing — see the parent README for why
- When adding a scoped override for one feature (e.g. `.docs-block .panel`), double check it overrides every property it needs to, not just the ones that seem relevant — an unset property falls through from a less-specific rule

## Notes
None.
