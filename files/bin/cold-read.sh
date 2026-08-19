#!/usr/bin/env bash
# cold-read.sh — set up a cold read of the project's own documentation.
#
# A fresh agent reads only the orientation files, answers ten fixed questions,
# and the gap between its answers and files/cold-read/answer-key.md is the
# measurement. Full procedure and how to score it: files/cold-read/PROTOCOL.md
#
# This script does the bookkeeping. Claude spawns the agent, because a shell
# cannot.
#
#   files/bin/cold-read.sh          # start a run: stamp a file, print the prompt
#   files/bin/cold-read.sh --check  # is the answer key stale? which runs exist?
#   files/bin/cold-read.sh --prompt # print the agent prompt and nothing else

set -uo pipefail
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
DIR="$REPO/files/cold-read"
KEY="$DIR/answer-key.md"
SHA="$(git -C "$REPO" rev-parse --short HEAD)"
TODAY="$(date +%Y-%m-%d)"

say() { printf '\033[36m==>\033[0m %s\n' "$*"; }
warn() { printf '\033[33m !\033[0m %s\n' "$*"; }

# The key records the commit it was written against. If HEAD has moved, the
# baseline predates the thing being tested and the run measures nothing.
key_sha="$(grep -om1 'Valid as of `[^`]*`' "$KEY" | tr -d '`' | awk '{print $4}')"
key_date="$(grep -om1 'Valid as of `[^`]*`, [0-9-]*' "$KEY" | awk '{print $NF}')"

if [[ "${1:-}" == "--prompt" ]]; then cat "$DIR/prompt.md"; exit 0; fi

if [[ "${1:-}" == "--check" ]]; then
	say "answer key: valid as of $key_sha ($key_date)"
	say "HEAD:       $SHA"
	if [[ "$key_sha" == "$SHA" ]]; then
		printf '\033[32m  current\033[0m\n'
	else
		behind=$(git -C "$REPO" rev-list --count "$key_sha..HEAD" 2>/dev/null || echo '?')
		warn "STALE — $behind commit(s) of change since the key was written"
		git -C "$REPO" log --oneline "$key_sha..HEAD" 2>/dev/null | sed 's/^/    /'
	fi
	echo
	say "previous runs:"
	ls "$DIR/runs"/[0-9]*.md 2>/dev/null | sed 's#.*/#    #' || echo "    none yet"
	exit 0
fi

# --- start a run -----------------------------------------------------------
if [[ "$key_sha" != "$SHA" ]]; then
	warn "The answer key is stale (written at $key_sha, HEAD is $SHA)."
	warn "Update $KEY and its 'Valid as of' line FIRST, and have Brandon confirm it."
	warn "A key written after the report grades the report against itself."
	echo
fi

RUN="$DIR/runs/$TODAY.md"
if [[ -e "$RUN" ]]; then
	n=2; while [[ -e "$DIR/runs/$TODAY-$n.md" ]]; do n=$((n+1)); done
	RUN="$DIR/runs/$TODAY-$n.md"
fi
sed -e "s/YYYY-MM-DD/$TODAY/" -e "0,/<sha>/s//$SHA/" -e "0,/<sha>/s//$key_sha/" \
	"$DIR/runs/TEMPLATE.md" > "$RUN"
say "run file: ${RUN#$REPO/}"
echo
say "Spawn a general-purpose subagent with the prompt below, verbatim."
say "Then score it against files/cold-read/answer-key.md, verify every Q10 item"
say "by grep before acting, and fill in the run file."
printf '\033[2m%s\033[0m\n' "────────────────────────────────────────────────────────"
cat "$DIR/prompt.md"
