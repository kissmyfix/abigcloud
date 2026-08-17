#!/usr/bin/env bash
# UserPromptSubmit hook: append to the monthly prompt log.
#
# Normally logs the prompt Brandon typed. If the prompt is exactly the trigger
# word, it logs Claude's previous response instead - marked, because the log
# lives under monologues/ and AI text there has to be identifiable later.
#
# Reads the hook's JSON on stdin. Never blocks an ordinary prompt: a failure
# anywhere still exits 0. Only a pin exits 2, deliberately.

set -uo pipefail

DIR=/home/brandon/Documents/data_center_research/files/prompt_log
# One file per month - the log is append-only forever, so it has to roll over.
OUT="$DIR/prompt-log-$(date '+%Y-%m').md"
TRIGGER='pinthat'
MARK='[Claude — response to the prompt above]'

mkdir -p "$DIR" 2>/dev/null

payload=$(cat)
prompt=$(printf '%s' "$payload" | jq -r '.prompt // empty')
transcript=$(printf '%s' "$payload" | jq -r '.transcript_path // empty')

# Trigger match is lenient: leading slash, surrounding space, any case.
normalized=$(printf '%s' "$prompt" | tr -d '[:space:]' | tr '[:upper:]' '[:lower:]')
normalized=${normalized#/}

body="$prompt"
pinned=0
if [[ "$normalized" == "$TRIGGER" ]]; then
    pinned=1
    # Most recent assistant turn, text blocks only, joined. -c keeps it to one
    # line so head can pick the latest before decoding.
    reply=$(tac "$transcript" 2>/dev/null \
        | jq -c 'select(.type=="assistant")
                 | [.message.content[]? | select(.type=="text") | .text]
                 | select(length>0) | join("\n\n")' 2>/dev/null \
        | head -n 1 | jq -r . 2>/dev/null)

    if [[ -n "$reply" && "$reply" != "null" ]]; then
        body="$MARK"$'\n\n'"$reply"
    else
        # Nothing to pin - say so rather than writing the trigger word in.
        body="$MARK"$'\n\n'"(pin failed: could not read the last response from the transcript)"
    fi
fi

{ printf "\n---\n%s\n\n" "$(date '+%Y-%m-%d %H:%M:%S')"; printf '%s\n' "$body"; } >> "$OUT" 2>/dev/null

# Exit 2 on a pin erases the prompt and blocks it, so the trigger word never
# becomes a turn - the append happens with no model invocation at all.
if (( pinned )); then
    printf 'pinned to %s (%s lines)\n' "${OUT##*/}" "$(printf '%s' "$body" | wc -l)" >&2
    exit 2
fi

exit 0
