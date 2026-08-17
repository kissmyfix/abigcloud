# podcasts/

## Purpose
Local and regional podcast episodes featuring the officials and boosters in scope — on-record spoken statements, transcribed for search and citation.

## Contents
- `mp3s/` — source audio, named `show-episode-title` (slugified 2026-07-29 to the project
  convention: lowercase, dashes, no spaces)
- `transcripts/` — faster-whisper text output, one .txt per episode, same stem as its mp3
- `manifest.csv` — GUID-to-name mapping from the original downloads; its `new_filename`
  column is the current on-disk name

## Source Type
**Primary Source** — recorded public statements by named officials (mayors, commissioners, state officials). The words are theirs; the transcription is machine-generated.

## Handling Instructions
- Whisper transcripts contain recognition errors — before quoting anyone in output, verify the exact wording against the mp3 timestamp
- Cite by show, episode title, and speaker
- The Growing Pains series is being read as a coordinated PR effort (see `memory/PINBOARD.md`) — treat its framing as message discipline to document, not neutral description

## Notes
All 23 episodes are transcribed as of 2026-07-29 (the "Better Together / Sam Sandlin" episode noted as queued here previously is done). The transcription scripts live in `files/bin/` (`batch-transcribe.py`, `transcribe.py`) — see that README for the venv dependency.
