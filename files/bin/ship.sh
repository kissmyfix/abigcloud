#!/usr/bin/env bash
# ship.sh — publish, push, wait for the deploy, confirm the live site serves it.
#
# The whole cycle with zero model tokens. Previously this was ~6 rounds of an AI
# running npm/git/curl by hand each session.
#
#   files/bin/ship.sh                          # commit everything, default message
#   files/bin/ship.sh "fixed the PILOT figure" # commit with a message
#   files/bin/ship.sh -m "msg" -v "some text"  # also assert that text is live
#   files/bin/ship.sh --dry-run                # publish + report, do not push
#
# Exit codes: 0 live and verified, 1 publish/build failed, 2 push failed,
#             3 deploy failed or timed out, 4 live check failed.
#
# With `gh` installed and authenticated it reports WHY a deploy failed, not just
# that it did. Without gh it still works, on the unauthenticated API, blind.

set -uo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SITE="https://abigcloud.com"
API="https://api.github.com/repos/kissmyfix/abigcloud/actions/runs"
DEPLOY_TIMEOUT=600   # seconds to wait for GitHub Actions (queued runs can be slow)
LIVE_TIMEOUT=120     # seconds to wait for the CDN to serve the new build

MSG=""; VERIFY=""; DRY=0
while [[ $# -gt 0 ]]; do
  case "$1" in
    -m|--message) MSG="$2"; shift 2 ;;
    -v|--verify)  VERIFY="$2"; shift 2 ;;
    --dry-run)    DRY=1; shift ;;
    -h|--help)    sed -n '2,20p' "${BASH_SOURCE[0]}"; exit 0 ;;
    *)            MSG="$1"; shift ;;
  esac
done
[[ -z "$MSG" ]] && MSG="Brandon's update to the site"

say()  { printf '\033[36m==>\033[0m %s\n' "$*"; }
ok()   { printf '\033[32m  ok\033[0m %s\n' "$*"; }
die()  { printf '\033[31m FAIL\033[0m %s\n' "$*" >&2; exit "$2"; }

cd "$REPO" || exit 1

# 0. Re-derive the note statuses in memory/brandon-voice-notes.md from the
#    article. Never blocks: a stale marker is not a reason to refuse a publish.
if [[ -f files/bin/sync-voice-notes.py ]]; then
  files/venv/bin/python files/bin/sync-voice-notes.py || true
fi

# 1. Build. build-citations.mjs exits non-zero if a cited document is missing.
say "npm run publish"
if ! (cd web && npm run publish); then
  die "publish failed — usually a @/ citation pointing at a file that is not there" 1
fi
ok "built"

# 2. Anything to send?
if [[ -z "$(git status --porcelain)" ]]; then
  say "nothing changed — checking what is already live"
else
  git add -A
  git commit -q -m "$MSG" -m "Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>" \
    || die "commit failed" 2
  ok "committed: $MSG"
  if [[ $DRY -eq 1 ]]; then say "--dry-run: stopping before push"; exit 0; fi
  say "git push"
  # Explicit remote and ref: a bare `git push` needs branch.<name>.merge to be
  # set, and a fresh clone -- or a branch recreated by a history rewrite -- does
  # not have it. That exits 128 after the commit has already been made, which
  # leaves the work committed but unpushed and reads as "ship.sh is broken".
  # HEAD pushes whatever branch is checked out to the same name on origin.
  git push -q origin HEAD || die "push failed" 2
  ok "pushed"
fi

SHA="$(git rev-parse HEAD)"

# 3. Wait for the Action, and say why if it fails.
#    Uses gh when it is installed: authenticated calls raise the API ceiling from
#    60/hr to 5000, and only gh can read the job log. Without the log a failure
#    reports "step 5 failed" and the build has to be reproduced locally to find
#    out what broke, which cost an hour on 2026-08-18.
say "waiting for deploy of ${SHA:0:8}"
deadline=$(( SECONDS + DEPLOY_TIMEOUT ))
conclusion=""; run_id=""

if command -v gh >/dev/null 2>&1; then
  while (( SECONDS < deadline )); do
    read -r run_id status conclusion <<<"$(gh run list --commit "$SHA" --limit 1 \
      --json databaseId,status,conclusion \
      --jq '.[0] | "\(.databaseId) \(.status) \(.conclusion)"' 2>/dev/null)"
    [[ "$status" == "completed" ]] && break
    sleep 10
  done
else
  while (( SECONDS < deadline )); do
    json="$(curl -sf "$API?head_sha=$SHA&per_page=1")" || { sleep 10; continue; }
    status="$(printf '%s' "$json"     | grep -m1 '"status"'     | cut -d'"' -f4)"
    conclusion="$(printf '%s' "$json" | grep -m1 '"conclusion"' | cut -d'"' -f4)"
    [[ "$status" == "completed" ]] && break
    sleep 10
  done
fi

case "$conclusion" in
  success) ok "deploy succeeded" ;;
  ""|null) die "no completed run for ${SHA:0:8} after ${DEPLOY_TIMEOUT}s — check the Actions tab" 3 ;;
  *)
    printf '\033[31m FAIL\033[0m deploy concluded %s\n' "$conclusion" >&2
    if command -v gh >/dev/null 2>&1 && [[ -n "$run_id" ]]; then
      printf '\n  which step:\n' >&2
      gh run view "$run_id" 2>&1 | sed -n '/JOBS/,$p' | sed 's/^/    /' >&2
      job="$(gh run view "$run_id" --json jobs \
             --jq '.jobs[] | select(.conclusion=="failure") | .databaseId' 2>/dev/null | head -1)"
      if [[ -n "$job" ]]; then
        printf '\n  what it said:\n' >&2
        gh api "repos/kissmyfix/abigcloud/actions/jobs/$job/logs" 2>/dev/null \
          | grep -iE 'error|failed|Required|Cannot|Missing' | tail -12 \
          | sed 's/^[0-9T:.Z-]* //; s/\x1b\[[0-9;]*m//g; s/^/    /' >&2
      fi
      printf '\n  full log:  gh run view %s --log\n' "$run_id" >&2
    fi
    exit 3 ;;
esac

# 4. Confirm the live site actually serves it. Cache-bust so we are not reading
#    a stale copy — a browser cache has already faked a "not deployed" panic once.
check() {
  local path="$1" code
  code="$(curl -s -o /dev/null -w '%{http_code}' -H 'Cache-Control: no-cache' "$SITE$path?cb=$SHA")"
  [[ "$code" == "200" ]] && { ok "200 $path"; return 0; }
  printf '  \033[31m%s\033[0m %s\n' "$code" "$path"; return 1
}
say "checking the live site"
fails=0
for p in / /about/ /faq/ /sources/ /investigations/quid_pro_no/; do
  check "$p" || fails=$((fails+1))
done
(( fails > 0 )) && die "$fails page(s) not serving 200" 4

# 5. Optional: assert a specific string is live (proves the new build, not just a build).
if [[ -n "$VERIFY" ]]; then
  say "looking for: $VERIFY"
  deadline=$(( SECONDS + LIVE_TIMEOUT ))
  while (( SECONDS < deadline )); do
    if curl -s -H 'Cache-Control: no-cache' "$SITE/investigations/quid_pro_no/?cb=$RANDOM" \
       | grep -qF "$VERIFY"; then ok "found on the live page"; exit 0; fi
    sleep 10
  done
  die "not found on the live page after ${LIVE_TIMEOUT}s (CDN lag, or the edit did not ship)" 4
fi

printf '\n\033[32mLive:\033[0m %s\n' "$SITE/investigations/quid_pro_no/"
