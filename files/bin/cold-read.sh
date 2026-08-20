#!/usr/bin/env bash
# cold-read.sh — set up a cold read of the project's own documentation.
#
# A fresh agent reads only the orientation files, answers thirteen fixed
# questions, and the gap between its answers and files/cold-read/answer-key.md is
# the measurement. Full procedure and how to score it: files/cold-read/PROTOCOL.md
#
# This script does the bookkeeping. Claude spawns the agent, because a shell
# cannot.
#
# It also builds the sandbox the agent is pointed at: a hardlinked mirror of the
# project with files/cold-read/ removed. An earlier run was invalidated when the
# agent found the answer key and said so — it had answered everything perfectly
# because it had read the answers. Asking it not to look is not a control. The
# key being absent from the tree it can see is.
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

# --- the sandbox -------------------------------------------------------------
# A real copy, not hardlinks. Hardlinking would mirror 400MB instantly, but a
# write inside the sandbox would then reach the real archive, and a subagent
# staying read-only is an assumption rather than a guarantee. A few seconds of
# copying is the cheaper mistake.
#
# Excluded: files/cold-read/ so the key, the prompt and every past run are simply
# absent; .git/ because its history carries the key; and the bulk that a
# documentation read has no use for — the gitignored mp3s, the venv, build output.
SANDBOX="${HOME}/.claude/scratch/data_center_research/cold-read-sandbox"
rm -rf "$SANDBOX"
mkdir -p "$SANDBOX"
rsync -a \
      --exclude 'files/cold-read/' \
      --exclude 'files/bin/cold-read.sh' \
      --exclude '.git/' \
      --exclude 'files/venv/' \
      --exclude 'podcasts/mp3s/' \
      --exclude 'web/node_modules/' \
      --exclude 'web/dist/' \
      --exclude 'web/.astro/' \
      --exclude '.remember/' \
      "$REPO/" "$SANDBOX/" 2>/dev/null

# The whole control rests on this being true, so it is checked rather than assumed.
# Checked structurally, by filename: an earlier version grepped for a phrase from the
# key and matched its own source, which is the sort of thing that makes a guard look
# like it is working while it refuses every run.
if [[ -e "$SANDBOX/files/cold-read" ]] \
   || find "$SANDBOX" -name 'answer-key.md' -o -name 'cold-read.sh' | grep -q .; then
	warn "answer material found in the sandbox — refusing to run"
	exit 1
fi
say "sandbox: $SANDBOX  ($(du -sh "$SANDBOX" | cut -f1), answer key absent, verified)"

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
say "It is pointed at the sandbox, not the project. Do not correct that path."
say "Then score it against files/cold-read/answer-key.md, verify every Q13 item"
say "by grep before acting, and fill in the run file."
printf '\033[2m%s\033[0m\n' "────────────────────────────────────────────────────────"
sed "s|/home/brandon/Documents/data_center_research|$SANDBOX|g" "$DIR/prompt.md"
