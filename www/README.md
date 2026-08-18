# www/ — where the websites live

Read this before touching anything in here. There are several site codebases and only
one of them is live. The names used to lie about that; they don't any more.

---

## The one that is live

**It is not in this directory.** The live abigcloud.com is at `abigcloud/web/` in the
project root.

```
~/Documents/data_center_research/abigcloud/web/
```

- Repo: `github.com/kissmyfix/abigcloud`
- Deploy: `git push origin main`. A GitHub Action builds it and publishes to GitHub Pages.
- Publish an article: `npm run publish` first, which regenerates the article and the
  source index from the research tree, then push.

This is the merged site: general data-center coverage (Tennessee, TVA, National, Costs
& Benefits) plus an Investigations section that hosts the deep dives. Quid-Pro-NO is the
only deep dive so far.

**Its repo used to be called `quid-pro-no`.** It was renamed at the merge, which is why
the old name still redirects and why the two names seemed like two things. They are one
thing.

---

## What is in here

### `wiki-prototype/`  *(was `abigcloud_v2` — renamed 2026-08-17)*

The unshipped second half of the plan. Thirteen commits, **no git remote**, never
deployed. It exists only on this disk and the backup drives.

It is not a newer version of the live site. It is a different kind of thing: the live
site publishes prose, this one turns the investigation into **data you can navigate**.

- `src/data/investigation/records.ts` — 27 typed records (the IDB, entities, people,
  institutions) with relations between them
- `src/data/investigation/events.json` — 42 timeline events in two lanes, SAID vs PAPER
- Generated dossier pages per entity: `/investigation/gallatin-idb/`, `/beretta/`,
  `/bradford/`, `/archer/`, `/bradley-llp/`, `/city-of-gallatin/`, `/ata-retail/`
- Draft-gated, so none of it publishes unless a flag is flipped

The old name implied it superseded the live site. It doesn't and probably never will as
a whole site. The open question is whether this dossier layer gets rebuilt *into* the
live site, or retired. See `SITE_PLAN.md`.

### `site-archive-v1/`  *(was `abigcloud.com` — renamed 2026-08-17)*

The original single-page site, from when this project was a general data-center deep
dive and before the Quid-Pro-NO investigation existed. Kept as a record of where the
work started. Plus four older `index.*` snapshots. Nothing here is deployed.

### `sumner_pilot_tracker_v2/`

The Sumner County PILOT tracker, a data-driven build. Superseded in intent by the
dossier layer above, not yet retired.

### `idb_comparisons/`, `idb_990_dashboard/`

Single-purpose pages for cycling through IDB data by year and building comparisons.
Prototypes.

---

## The short version

| Directory | What it is | Live? |
|---|---|---|
| `abigcloud/web/` *(project root, not here)* | The site. Prose, topics, investigations. | **Yes** |
| `www/wiki-prototype/` | The investigation as navigable data. Unfinished. | No |
| `www/site-archive-v1/` | Where the project started. | No |
| `www/sumner_pilot_tracker_v2/` | PILOT data tracker. | No |
| `www/idb_comparisons/`, `www/idb_990_dashboard/` | Prototypes. | No |

One site is deployed. Everything in `www/` is either history or a prototype.
