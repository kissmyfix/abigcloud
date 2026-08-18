# banners/

## Purpose
Page banner art for abigcloud.com. Every page renders one, so these files set the
first impression of the site and, because they sit above the content, its
vertical rhythm.

## The size requirement (site convention)

Every banner ships as **two crops of the same scene**, both mandatory:

| crop | file suffix | pixels | ratio | shown on |
|---|---|---|---|---|
| wide | `<name>.jpg` | **2000 x 334** | ~6:1 | viewports above 700px |
| narrow | `<name>-narrow.jpg` | **1000 x 667** | 3:2 | viewports 700px and under |

These are not suggestions. `src/components/Banner.astro` renders every banner at
these two ratios no matter what the file is, so an off-spec image does not change
the page height. It just gets trimmed by `object-fit: cover`, and the build prints
a `[banner]` warning naming the file. A missing narrow crop warns too.

The reason for the lock: banners used to take their height from whatever the file
happened to be, so clicking from a 2000x334 page to the 2000x500 TVA banner shoved
the whole page down 120px. Fix the crop, not the CSS.

Note the narrow crop is a genuinely different composition, not a resize. A 6:1
cinematic frame becomes an unreadable sliver on a phone, so recompose it: find the
subject, crop 3:2 around it.

Also worth knowing when composing: the page fades the banner into the background at
both edges, and hard in the bottom half on dark theme. Don't put anything that has
to read clearly in the bottom third or the top 10%.

To add a banner: export both crops here, then point the page at the wide one in
frontmatter (`heroImage` and `heroImageNarrow`, both required, see `content/tva.md`).
Pages that set neither inherit `home-banner.jpg`.

## Contents
- `home-banner.jpg` / `-narrow` — the default, inherited by every page without its own
- `tva-coal-barges.jpg` / `-narrow` — used by `content/tva.md`

## Source Type
**Output Artifact** — site design assets, not evidence.

## Handling Instructions
- Not citable. Nothing here is a source for any factual claim in an article.
- Provenance matters anyway: before a photo goes live, confirm it is ours to publish
  (own work, public domain, or a license that permits it) and record where it came
  from. A stock photo of the wrong dam undercuts the reporting around it.
- `tva-coal-barges.jpg` was cropped from a 2000x500 original on 2026-07-31; the
  uncropped version is in git history if a different crop window is ever wanted.

## Notes
The wide ratio is 2000x334 rather than a round 6:1 because `home-banner.jpg` was
already that shape and it became the template.
