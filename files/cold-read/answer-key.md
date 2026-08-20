# Answer key — what a cold read should conclude

**Valid as of `2d0cc47`, 2026-08-19 — and stale.** The 2026-08-19 housekeeping pass
restructured the tree after that commit and none of it is committed yet: `reference/` was
deleted, `angles/` and Brandon's Beretta notes moved out of the project, `files/cold-read/`
itself became gitignored, and the Shalom Zone 990s got their own directory. Items 3 and 9
below were rewritten to match. **Do not run a cold read against this key until Brandon has
confirmed it**, because a key he has not agreed to is only Claude's opinion of Claude's own
documentation.

Update this file *before* running the test, not after. A key written after seeing the
report grades the report against itself and measures nothing.

Answers here are the settled understanding Brandon and Claude agree on. The cold agent
never sees this file.

---

**1. The project.** abigcloud.com is a site about data centers, built so a cold reader can
understand a complex subject, focused on Middle Tennessee. TVA, ratepayer costs, the
national picture, xAI in Memphis, Fisk, Hendersonville. Brandon Smith is an independent
investigative journalist; the work runs on public records.

**2. Quid-Pro-NO.** One deep-dive investigation *inside* the site: Meta, Gallatin, the
Industrial Development Board, the PILOT structure. The crown jewel and the only
investigation developed to any degree, but **not** the site's purpose. Describing the
project as "the IDB investigation" is wrong.

**3. Structure.** One git repo (`github.com/kissmyfix/abigcloud`), one website (`web/`).
Around it: a public evidence archive (statutes, audits, 990s, council packets, transcripts,
player profiles) and a private working layer that is not published — `memory/` inside the tree, and outside this project outside it, which holds `angles/` and everything else parked out of the project. Directory index is `files/DATA_MAP.md`.

**4. Publishing.** Same process for both. Every page is edited directly under
`web/content/`; what you edit is what ships. There are no drafts and nothing regenerates
over your work. Ship with `files/bin/ship.sh "message"`, which publishes, commits, pushes,
waits on the GitHub Action, and confirms the live pages serve 200. Underneath it is
`cd web && npm run publish && git push`.

**5. Citations.** Write `@/` for the research archive root, e.g.
`[text](@/web_articles/foo.txt)`. The publish step copies the document into
`web/public/sources/`, rewrites the link, and lists it at `/sources/`. A cited **text**
document also gets its own rendered page at `/sources/<slug>/` — `.md` formatted, `.txt`
verbatim in `<pre>`, PDFs skipped. The rewrite is one-way. Publishing exits non-zero if a
cited document is missing. Pages under `web/content/sources/` are generated: never
hand-edited, never cited.

**6. Scope of the evidence standard.** It applies **at publication**, not while Brandon is
thinking. A working theory needs no citation; asking him to source a hunch is the failure,
not the discipline. Being wrong mid-investigation is expected. Being wrong at publication
is not.

**7. Modes.** Five, in `.claude/skills/investigative-journalist/SKILL.md`: Theorizing/
soundboard (**the default when he thinks out loud** — contribute, do not audit),
Verification, Adversarial/stress-test, Co-counsel, Alignment. Plus two project-specific
ones in CLAUDE.md: Build and Write. Mode switches are explicit and immediate.

**8. Working rules.** Do not audit unbidden. When he says drop it, it is dropped. Never
take a source at face value, least of all a subject's own record. When he says a document
exists, it exists — that is a search problem, never a credibility problem. **His unhedged
assertion outranks the archive.** Name conventions and say why they are conventions.
Answer at the length asked. Never comment on typos; never introduce em dashes. List mode
means answer the item and park everything else. He edits small prose fixes directly on
github.com and may not say so, so fetch before pushing.

**9. State of the work.** Part 1 is published and live, still being verified in places;
Parts 2+ are in progress. What is sourced and what is not lives in
~~`angles/citation-worklist.md`~~. Findings live in `memory/MEMORY.md` and
`memory/TIMELINE.md`; leads in `memory/PINBOARD.md`.

**10. Known-and-accepted.** Several site topic sections are thin by choice, not oversight.
The Sumner PILOT tracker was deleted with `www/` in commit `ebb3e4d` and is recoverable
from git. Whether Project Skillet went to Huntsville or Birmingham is recorded as DISPUTED,
Brandon says Huntsville and that outranks Fenton's podcast account. The Meta "$1.4M+" and
the IDB's school payments are stated in the article as the same money; the documents do not
settle that, and it is flagged in the worklist for Brandon's own pass. A cold agent
flagging any of these has read correctly; they are not defects.
