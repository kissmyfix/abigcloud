# podcasts/transcripts/

## Purpose
Machine transcriptions of the audio in `podcasts/mp3s/`, so episodes can be searched,
quoted, and cited by passage instead of by timestamp hunting.

## Contents
24 `.txt` files. Twenty-three are one per episode, named to match the source `.mp3`
exactly so the pair is obvious.
`2026-tucker-carlson-oleary-utah-data-center-interview.txt` has no `.mp3` and no
`manifest.csv` row: it came from a video interview and moved here from `web_articles/` on
2026-08-19. One naming exception: the Fenton interview is `fenton-on-podcast-full.txt`. A narrowed
keyword extract of it also existed and was deleted 2026-08-18 — it had cut the passage
where Fenton names the Project Skillet NDA, which is one of the things the article cites
him for. Narrowing a transcript to save context was solving a problem that did not exist;
quote from the full transcript. Every
transcript here was slugified alongside its mp3 on 2026-07-29; the publisher-titled
duplicate of `fenton-on-podcast-full.txt` was byte-identical and deleted that day. Old names
are recoverable from `podcasts/manifest.csv`.

## Source Type
**Working Material derived from a Primary Source.** The transcript is machine output. The
recording it came from is the primary source, and the recording is what gets cited.

## Handling Instructions
- **Quote the audio, cite the audio.** Whisper misrenders names, numbers, and local place
  names in particular. Confirm any sentence against the recording before it appears in
  published prose.
- Search and read here freely. This is the fast path into a corpus that would otherwise
  take a full day to listen through.
- Do not hand-correct a transcript. If one is bad enough to matter, re-run it. These are
  regenerable output in the same sense as anything in a `derived/` directory.
- Attribute to the speaker and the episode, not to this file.

## Notes
Sits outside the `derived/` convention only because it predates it and the pairing with
`mp3s/` is already clear. Treat it as derived material regardless.
