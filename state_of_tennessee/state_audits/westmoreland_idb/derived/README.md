# derived/

## Purpose
Machine-produced text extractions of the PDFs in the parent directory. Regenerable output, never a source.

## Contents
- `<name>.txt` — `pdftotext -layout` extraction with `[[page N]]` markers at each page break
- `<name>-ocr.pdf` — OCR'd copy, present only where the original had no text layer
- `pdf-index.csv` — per-file: kind, pages, chars, chars-per-page, raster share, trust verdict, PDF producer

Rebuild with `python3 files/bin/pdf-extract.py <parent-directory>` (add `--force` to redo existing).

## Source Type
**Working Material** — derived output. The PDFs in the parent are the source; these are a convenience layer.

## Handling Instructions
- **Never cite a `.txt` file.** Cite the PDF, by its printed page number.
- `[[page N]]` is the **PDF page index, not the printed page number** — divider pages shift them apart. Use the marker to navigate, the printed number to cite.
- Check the `trust` column in `pdf-index.csv` before relying on any figure. `OCR_SCAN` means the text is a machine's guess and must be verified against the page image.
- Safe to delete entirely; one command rebuilds it.

## Notes
Grep here first, then open only the pages that matter. That is the point of this directory — searching 10MB of text costs nothing, reading hundreds of page images does not.
