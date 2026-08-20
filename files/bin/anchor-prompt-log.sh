#!/usr/bin/env bash
# Publish a SHA-256 for each CLOSED month of the prompt log.
#
# The log itself is private and stays private. Its hash is committed to the
# public repository, where the commit's own timestamp dates the content. That
# turns "a text file he could have written yesterday" into "this exact content
# existed on this date," without publishing a word of it.
#
# Only closed months are anchored. The current month is still being appended to,
# so its hash changes every time Brandon types, and a hash that changes proves
# nothing.
#
# Re-running is safe and is the point: a month whose hash no longer matches its
# published value has been modified since it was anchored. That is reported as a
# MISMATCH and the script exits non-zero.
#
#     files/bin/anchor-prompt-log.sh

set -uo pipefail

LOG_DIR="${HOME}/.claude/prompt_log/data_center_research"
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
MANIFEST="$REPO/files/prompt-log-hashes.md"
THIS_MONTH="$(date '+%Y-%m')"

[ -d "$LOG_DIR" ] || { echo "no prompt log at $LOG_DIR"; exit 1; }

if [ ! -f "$MANIFEST" ]; then
    cat > "$MANIFEST" <<'HEADER'
# Prompt log hashes

The prompt log records every message typed to Claude Code on this project. It is private
and is not published. What is published is a SHA-256 for each completed month, committed
here so that the commit's own date establishes when that content existed.

Anyone handed a copy of a monthly log can verify it is the same file that was hashed:

    sha256sum prompt-log-2026-07.md

and compare against the row below. A match means the file has not changed since the date of
the commit that added its row. A mismatch means it has.

Only closed months appear. The month in progress is still being appended to.

| Month | Bytes | SHA-256 |
|---|---|---|
HEADER
    echo "created $MANIFEST"
fi

added=0; mismatched=0; unchanged=0

for f in "$LOG_DIR"/prompt-log-*.md; do
    [ -e "$f" ] || continue
    base="$(basename "$f")"
    month="${base#prompt-log-}"; month="${month%.md}"

    if [ "$month" = "$THIS_MONTH" ]; then
        echo "skip     $month (still open)"
        continue
    fi

    sum="$(sha256sum "$f" | cut -d' ' -f1)"
    bytes="$(stat -c%s "$f")"
    existing="$(grep -F "| \`$month\` |" "$MANIFEST" | grep -o '[0-9a-f]\{64\}' | head -1)"

    if [ -z "$existing" ]; then
        printf '| `%s` | %s | `%s` |\n' "$month" "$bytes" "$sum" >> "$MANIFEST"
        echo "ANCHORED $month  $sum"
        added=$((added+1))
    elif [ "$existing" = "$sum" ]; then
        echo "ok       $month (unchanged since anchoring)"
        unchanged=$((unchanged+1))
    else
        echo "MISMATCH $month"
        echo "         published: $existing"
        echo "         actual:    $sum"
        echo "         This file has been modified since it was anchored."
        mismatched=$((mismatched+1))
    fi
done

echo
echo "$added anchored, $unchanged verified, $mismatched mismatched."
[ "$added" -gt 0 ] && echo "Commit $MANIFEST to publish the new hashes."
[ "$mismatched" -gt 0 ] && exit 1
exit 0
