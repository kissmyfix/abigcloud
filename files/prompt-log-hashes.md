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
| `2026-07` | 195093 | `a78def3f9e746fe767f27898f767d2e89f96323ee095f7f4f60519ec7a166a15` |
