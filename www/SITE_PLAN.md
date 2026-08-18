# SITE_PLAN.md — The Combined abigcloud.com Rebuild
*Decisions locked 2026-07-06 (soundboard session). This file is the source of truth for
the site work; a future agent starting site work reads this first. Edit freely — like
everything else, AI drafted it, Brandon owns it.*

---

## Intent

One site serving two audiences: the public record of the investigation (articles, in
Brandon's voice), and a "modernized wiki" — the source of truth that lets any future
reader deep-dive the mountain of gathered data without spending the months it took to
pull together. Design reference: the "Article One" congressional dossier UI
(`visualizations/wiki_ui_suggestion/` — adapt the card grammar and grouped sidebar, not a
1:1 copy; trade the SaaS palette for something that reads as *record*).

**The main character is the Gallatin IDB.** Not the root of the hierarchy — the center
of gravity. It is the node where the most connections converge, and its dossier is the
site's hot center.

## The two-axis structure

1. **Jurisdiction tree (containment — "the system"):** State of Tennessee → Comptroller,
   UT Knoxville, TVA + IRS 990 data (federal, filed here for simplicity; records carry
   `level: federal` so the data stays honest) → counties (Sumner, Gibson, Hamilton — each
   county follows the same subtree shape) → boards (Gallatin IDB, Portland IDB, County
   IDB, Board of Education) → entities. `the_players` is top-level: people cut across
   jurisdictions. Generated from `part_of` relations, never hand-maintained.
   - Parallel county subtrees make the comparison case structurally (Hamilton/Chattanooga
     publishes everything; Gallatin publishes nothing — same shape, opposite contents).
   - Empty/unresolved branches are data (Portland IDB = the attribution question, visible).
2. **Story graph (connection — "the story"):** typed, dated, sourced relations between
   records; backlinks and chips generated at build. A reader descends the tree to learn
   the system, then the graph carries them through deals, people, and money.

Site sections (sidebar groups, Article One style): Overview (IDB dossier) · The Deals
(11 entity sub-dossiers) · The People · The Money (county totals demoted to a rollup
page here) · Timeline · Documents · Reference (glossary). First content modeled: the
Gallatin IDB record itself.

## Schema (stress-tested against the v2 tracker data)

- **Six record types:** `entity`, `person`, `org` (with `kind`: government/board/company/
  firm), `document`, `event` (from `memory/TIMELINE.md`, already site-shaped), `term`
  (from `reference/`). Parcels = structured field on entities for v1; promote to a
  seventh type if parcel-level analysis grows.
- **Relations:** verb + target id + date range where known + source document id. Starting
  vocabulary: `part_of`, `lessor_of`, `counsel_for`, `board_member_of`, `administers`,
  `employed_by`, `signed`, `commissioned`, `parent_of`, `governed_by_instrument`. Dates
  on relations wherever the record supports them (the network map needs them to animate).
- **Registry/money data as rows, not prose:** the full registry row (est. value, rent,
  PILOT city/county, filed date, lease begin/end, parcel id, prop code) with per-row
  `source_doc` and `attribution: verified|unverified`, plus a three-way reporting status:
  **reported / not-reported / unknown** — "marked N in the state record" is a finding,
  not missing data. No formatted strings, no HTML in data (the v2 tracker's core flaw).
- **Aggregates are never stored, always computed at build** from rows, filtered by
  attribution — the blocked 90.2%/$42.18M figure is currently hardcoded in
  `sumner_pilot_tracker_v2/js/county-data.js` and must not survive migration as a stored
  number.
- **Publish gating enforced by the build:** every record/page carries `publish:
  true|false`; production builds include only published content. Sensitivity is
  mechanical, not memory-dependent.
- IDs reuse the research tree's shorthand (`woolhawk`, `stev_ham`, `preston_stark`).
  Encode both "Woolhawk"/"Wool Hawk" style aliases in an `aka` field.
- Content records are generated from the research tree's memory files as an explicit,
  reviewed step (same convention as the old tracker) — research stays messy, site
  content is the curated sourced subset.

## Stack

- **Astro, fully static output** (content collections + zod validation: malformed
  records or dangling relation ids fail the build by name). Components for the card
  grammar; zero client JS by default.
- **Pagefind** for client-side full-text search (indexes at build time, no server).
- **No SSR, no app server, no database, ever** — nothing to run or patch in production.
- Vanilla JS islands only where interactivity earns it.

## Pipeline & security posture (decided 2026-07-06)

> **SUPERSEDED 2026-08-17.** The plan below was never implemented. What actually
> happens today is recorded here instead; the original text is kept underneath for
> the record.

**Live pipeline (verified 2026-08-17):**

- The published site is **`abigcloud/web/`** in this tree, a clone of
  **`github.com/kissmyfix/abigcloud`**.
- **Deploy = `git push origin main`.** A GitHub Actions workflow
  (`.github/workflows/deploy.yml`) runs `npm ci && npm run build` in `web/` and
  publishes `web/dist/` to **GitHub Pages**. The custom domain is set by
  `web/public/CNAME`.
- **`npm run publish`** regenerates the article and the source index from this
  research tree first, then builds. Use it instead of `npm run build` when a draft
  has changed.
- `site.abigcloud.com` no longer resolves; the CT-log exposure noted below is closed.
- `192.168.1.4` is not part of the pipeline. It answers on :80 with a 403 and has no
  `/var/www/html`. Nothing depends on it.
- **Open:** `www.abigcloud.com` points at Cloudflare and returns HTTP 530 (origin
  unreachable). The apex is fine. Needs a DNS fix.
- **Open:** the research corpus has no public home yet. It is committed locally but
  its remote was removed — the old `quid-pro-no` remote turned out to be the *site*
  repo under its former name, and pushing 452MB of PDFs there would have broken the
  Pages build. Needs a new repo (e.g. `abigcloud-sources`), which needs a browser.

<details><summary>Original 2026-07-06 plan, not implemented</summary>

- Develop on **asus**; preview via Astro dev server, **LAN-only for now**.
- **Git: local repo only, no GitHub remote.** Optional later: bare repo on another LAN
  box (pve/hplaptop) over ssh as backup — zero third parties either way.
- Staging: `site.abigcloud.com` → hplaptop:80 (currently serves only a 404). **Do not
  deploy anything sensitive to hplaptop while that public route exists** (subdomains
  leak via CT logs; the Caddy block has no auth). Before real staging: add `basicauth`
  to that block or repoint it.
- Production: rsync `dist/` → proxy (`192.168.1.4`) `/var/www/html`, already served by
  Caddy with good headers. Open item: confirm write ownership of `/var/www/html`.

</details>

## Phases

1. **Migrate current live abigcloud.com verbatim** to the Astro pipeline — current
   public content only (re-pull from live first; the local `www/site-archive-v1/` copy may
   be stale). Proves the pipeline end-to-end at zero stakes. Ships.
2. **The wiki/dossier buildout** — schema content, IDB dossier first as the locked
   template (template-before-replicate rule), then the 11 entities, tree + graph nav.
   **Sensitive and unpublished until Brandon explicitly says publish.** The pinned
   numbers rebuild (registry PDFs → attributed rows) is the same task as populating the
   money tables.
3. **The time-scrubbed network map** (see PINBOARD 2026-07-06): the relations dataset
   rendered as an interactive graph (Cytoscape.js candidate), time scrubber animating
   2008→present, opening centered on the Gallatin IDB, first ring expanded, edge-type
   filters, node click → side panel + dossier link. The map is a lens; dossier pages
   stay canonical.

## Status

- **Scaffolded 2026-07-06:** `www/wiki-prototype/` — minimal Astro (Node upgraded 20→22 via
  NodeSource for Astro 5), local git repo on `main`, dev server LAN-bound
  (`npm run dev` → http://192.168.1.6:4321), build verified. Environment fix along the
  way: removed `nosymfollow` from the Documents and Coding mounts (it broke npm's
  symlinks; fstab backup at `/etc/fstab.bak-20260706`).

- **Dark mode shipped 2026-07-06**: covers both the shell tokens and the legacy content
  palette (which already had a `prefers-color-scheme` dark set in the original site's
  CSS). Toggle simplified same day to two states: defaults to system, one click flips,
  persists.
- **Stage closed 2026-07-06 (changelist round + bug pass):** Phase 1 migration and the
  step-2 wiki skin are complete and stage-approved. Group overview pages exist at
  /report/<group-slug>/ (clickable breadcrumbs/cards/sidebar names; future home of
  per-group visualizations). Content-collection workflow live (option a: authoring in
  the research tree, copying into src/content/snippets/ IS the publish step; aboutme.md
  is the first). Framing ticker PARKED (component kept). Bug pass verified: zero broken
  internal links, zero stale anchors, zero external hosts (fonts self-hosted end to end).
- **Copy conventions:** Claude has standing permission to fix Brandon's typos and
  formatting while preserving his voice. NEVER add em dashes, anywhere, in any copy.
- **Homepage end-state vision (Brandon, changelist):** the clickable timeline/mindmap
  spine as the navigational centerpiece, possibly a clickable Middle Tennessee map;
  every dataset gets a glanceable widget up front with the technical source material
  one discoverable step deeper. "Digestible at first glance, expandable into the
  boring material in the same easy-to-discover place."
- **Planned interactive component — context popovers:** on future content pages,
  references to entities/terms/documents (e.g. "990", "PILOT", an entity name) are
  clickable: open an in-page, closable popover with the glossary explainer or record
  summary plus a link to the full dossier/reference page (Wikipedia-preview pattern;
  native `<dialog>`/Popover API, no framework). Rendered from the same records the
  backlinks use — one data source, three surfaces (page, popover, graph).

- **Investigation layer v0.1 built 2026-07-06 (draft-gated):** /investigation/ routes
  exist only when DRAFTS=1 (`npm run dev`, `npm run build:drafts`); the public
  `npm run build` was verified to emit zero investigation output. 30 curated records
  (IDB hub + 11 entities + people + institutions), per-fact status flags
  (established/provisional/blocked/open) with sources, SAID/PAPER timeline rendered
  from memory/TIMELINE.md (42 entries), jurisdiction-tree page, backlink chips, term
  popovers from the reference glossary. County-wide rent aggregation deliberately
  absent (the blocked 90.2% figure); Portland four hard-flagged lessor-unverified.
  v0.1 data is hand-curated in src/data/investigation/records.ts; graduates to the
  full schema/content-collections in the data phase.

## Open items

- Re-pull live abigcloud.com before migration (local copy may be stale).
- Confirm `/var/www/html` ownership on proxy for the deploy script.
- What web server answers on hplaptop:80 (matters only when staging goes real).
- Relationship vocabulary review against Brandon's head — cheap to add verbs early.
- Delete/move the stray terminal screenshot in `visualizations/wiki_ui_suggestion/`.
- Set a global git identity on asus (`git config --global user.name/user.email`) — the
  first commit used per-command overrides.
