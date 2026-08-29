#!/usr/bin/env bash
# Watch inbox/ and run the intake worker when a file finishes landing there.
#
#   files/bin/intake-watch.sh          run in the foreground
#   systemctl --user start abigcloud-intake    run as a service
#
# inotifywait fires on close_write (a finished write) and moved_to (a drag or
# an mv). Both mean the file is complete; neither fires mid-download, because
# browsers write to a .part or .crdownload first and rename on completion.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
INBOX="$ROOT/inbox"
LOG="$ROOT/files/.intake.log"
SETTLE=3          # seconds of quiet before running, so a burst is one run

mkdir -p "$INBOX"

command -v inotifywait >/dev/null || {
  echo "inotifywait not found. Install with: sudo apt install inotify-tools" >&2
  exit 1
}

log() { printf '%s  %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$*" | tee -a "$LOG"; }

log "watching $INBOX"
python3 "$ROOT/files/bin/intake.py" >>"$LOG" 2>&1 || true

while true; do
  # Block until something lands. --exclude keeps our own output from retriggering.
  inotifywait -q -r -e close_write -e moved_to \
    --exclude '(derived/|NEEDS-FILING\.md$|\.part$|\.crdownload$|\.tmp$)' \
    "$INBOX" >/dev/null || true

  # Coalesce a burst: wait for SETTLE seconds of quiet before doing the work.
  while inotifywait -q -r -t "$SETTLE" -e close_write -e moved_to \
        --exclude '(derived/|NEEDS-FILING\.md$|\.part$|\.crdownload$|\.tmp$)' \
        "$INBOX" >/dev/null 2>&1; do :; done

  log "change detected, running intake"
  if python3 "$ROOT/files/bin/intake.py" >>"$LOG" 2>&1; then
    n=$(grep -c '^- \[ \] filed' "$INBOX/NEEDS-FILING.md" 2>/dev/null || echo 0)
    log "done, $n awaiting filing"
    command -v notify-send >/dev/null && \
      notify-send "abigcloud intake" "$n document(s) awaiting filing" || true
  else
    log "intake FAILED, see $LOG"
  fi
done
