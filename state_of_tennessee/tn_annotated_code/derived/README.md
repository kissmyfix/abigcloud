# tn_annotated_code/derived/

## Purpose
Plain-text extractions of the statutes and bill documents held as PDFs in the parent
directory, so statutory language can be searched and quoted without opening a viewer.

## Contents
- `tca-7-53-301-board-of-directors.txt`, `tca-7-53-302-corporate-powers.txt`,
  `tca-7-53-305-tax-exemption-pilot.txt`, `tca-7-53-308.txt` — the Title 7 Chapter 53
  sections the whole investigation runs on.
- `hb1269-sb708-as-introduced.txt`, `pc265-sb708-as-enacted.txt`,
  `pc265-sb708-fiscal-memo.txt` — the bill as introduced, the act as enacted, and the
  fiscal memo. Read as introduced against as enacted; the difference is the finding.
- `pdf-index.csv` — kind, pages, and trust rating per source file, written by the
  extractor.

## Source Type
**Derived.** Machine output from `files/bin/pdf-extract.py`. Regenerable, never
hand-edited. See the `derived/` convention in `files/DATA_MAP.md`.

## Handling Instructions
- **Statutory text is quoted from the statute, not from this extraction.** For anything
  going into published prose, confirm the wording against the source PDF or against the
  official Tennessee code, and cite the section number.
- Extraction can drop or mangle subsection lettering and indentation, which in statutory
  text is meaning, not formatting. Check structure, not just words.
- Search here freely. Cite from the parent.

## Notes
These four sections are the ones cited most often across `memory/`, ~~`angles/`~~, and
`web/content/reference/`. If a fifth becomes load-bearing, extract it rather than paraphrasing from
memory.
