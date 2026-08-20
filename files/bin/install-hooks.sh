#!/usr/bin/env bash
#
# install-hooks.sh — point git at the hooks kept in this repository.
#
# Git's own hook directory, .git/hooks/, is not versioned: a hook put there exists on one
# machine and disappears on the next clone. Setting core.hooksPath makes git read the
# versioned directory instead, so the hooks are reviewable in the repo and travel with it.
#
# Run once per clone:  files/bin/install-hooks.sh
set -euo pipefail
REPO="$(git rev-parse --show-toplevel)"
cd "$REPO"

git config core.hooksPath files/hooks
chmod +x files/hooks/* 2>/dev/null || true
echo "core.hooksPath -> files/hooks"
for h in files/hooks/*; do
	[ -f "$h" ] && echo "  installed: $(basename "$h")"
done

# The deny list holds exact strings that must never be committed — a person's name, a home
# address, an account number. It therefore contains the data it protects, so it lives inside
# .git, which is never committed and never pushed.
DENY="$REPO/.git/pii-denylist"
if [ ! -f "$DENY" ]; then
	cat > "$DENY" <<'SEED'
# Exact strings that must never be committed. One per line, case-insensitive,
# matched literally. Blank lines and # comments ignored.
#
# This file lives inside .git on purpose: it is never committed and never pushed,
# because it necessarily contains the very details it exists to protect.
#
# Add a line for each: household name, street address, utility or bank account
# number, personal email address. Then test with:
#
#     echo "the string" > /tmp/t.md && git add -f /tmp/t.md   # (do not actually do this)
#
# Seeded empty. The pattern checks in files/hooks/pre-commit run regardless.
SEED
	echo "  created: .git/pii-denylist (empty — add the strings you want blocked)"
else
	echo "  found:   .git/pii-denylist ($(grep -cvE '^\s*(#|$)' "$DENY") entr(y|ies))"
fi

echo
echo "The hook can be skipped with 'git commit --no-verify' when you mean to."
