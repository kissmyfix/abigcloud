#!/usr/bin/env bash
# headline-bot v1: sweep -> extract -> generate.
#
#   files/bin/headline-bot/run.sh            # Claude API (needs ANTHROPIC_API_KEY)
#   files/bin/headline-bot/run.sh --cli      # local `claude` binary, no key needed
#
# Output lands in files/bin/headline-bot/state/queue.json for review.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PY="$HERE/../../venv/bin/python"

BACKEND=api
[[ "${1:-}" == "--cli" ]] && BACKEND=cli

echo "== sweep =="
"$PY" "$HERE/sweep.py" "${@:2}"
echo
echo "== extract =="
"$PY" "$HERE/extract.py"
echo
echo "== generate ($BACKEND) =="
"$PY" "$HERE/generate.py" --backend "$BACKEND"
