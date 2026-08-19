#!/usr/bin/env bash
# whos-editing.sh — is Brandon in this file right now?
#
# mdlive autosaves as he types. Writing to a file it has open races his buffer:
# a clean buffer silently reloads from disk (his cursor survives, unsaved text
# does not), a dirty one refuses and shows him a conflict note he has to clear.
# Either way he loses time, and on 2026-08-18 it cost an hour of confusion.
#
#   files/bin/whos-editing.sh <path>     -> exits 1 and warns if mdlive has it
#   files/bin/whos-editing.sh            -> lists whatever mdlive has open
#
# Check before any scripted edit to a content file. If it is open, ask first.

set -uo pipefail
open=$(pgrep -af "mdlive\.py" | grep -v whos-editing | sed 's/.*mdlive\.py //' | awk '{print $1}')

if [[ $# -eq 0 ]]; then
	[[ -z "$open" ]] && { echo "mdlive is not running"; exit 0; }
	echo "mdlive has open:"; printf '  %s\n' $open; exit 0
fi

target="$(realpath -m "$1")"
for f in $open; do
	if [[ "$(realpath -m "$f")" == "$target" ]]; then
		printf '\033[33mOPEN IN MDLIVE:\033[0m %s\n' "$1" >&2
		echo "Writing to it now races his buffer. Ask before editing." >&2
		exit 1
	fi
done
exit 0
