import re
import sys

full_path = sys.argv[1]
out_path = sys.argv[2]

# Keywords tied to the Gallatin IDB / Meta-Woolhawk investigation.
# Grouped loosely by theme for readability in the narrowed output.
KEYWORDS = [
    # People
    "fenton", "rosemary bates", "bates", "stark", "leon", "lilibeth",
    "jouvence", "mumpower", "frazier",
    # Entities / orgs
    "geda", "idb", "industrial development board", "city attorney",
    "gallatin", "sumner county", "woolhawk", "meta", "beretta", "bradford",
    "tva", "comptroller",
    # Mechanisms / legal terms
    "pilot", "quitclaim", "abatement", "990", "non-reporting", "audit",
    "subpoena", "lease", "rent", "tax exempt", "assessment", "reinstat",
    "dissolution", "board", "council", "resolution", "subsidy",
    "payment in lieu", "governmental instrumentality", "501(c)",
    "best interest determination", "economic impact",
]

# build case-insensitive regex, longest phrases first to avoid partial overlap issues
KEYWORDS_SORTED = sorted(KEYWORDS, key=len, reverse=True)
pattern = re.compile(r"(" + "|".join(re.escape(k) for k in KEYWORDS_SORTED) + r")", re.IGNORECASE)

with open(full_path) as f:
    lines = f.readlines()

line_re = re.compile(r"^\[(?P<start>[\d:.]+) --> (?P<end>[\d:.]+)\] (?P<text>.*)$")

entries = []
for line in lines:
    m = line_re.match(line.strip())
    if not m:
        continue
    entries.append((m.group("start"), m.group("end"), m.group("text")))

hits = set()
for i, (start, end, text) in enumerate(entries):
    if pattern.search(text):
        hits.add(i)

# expand each hit with 1 line of context before/after, merge overlapping ranges
CONTEXT = 1
ranges = []
for i in sorted(hits):
    lo = max(0, i - CONTEXT)
    hi = min(len(entries) - 1, i + CONTEXT)
    ranges.append((lo, hi))

merged = []
for lo, hi in ranges:
    if merged and lo <= merged[-1][1] + 1:
        merged[-1] = (merged[-1][0], max(merged[-1][1], hi))
    else:
        merged.append((lo, hi))

with open(out_path, "w") as out:
    out.write("NARROWED TRANSCRIPT — sections matching investigation keywords\n")
    out.write(f"({len(merged)} clusters, {len(hits)} matching lines out of {len(entries)} total)\n")
    out.write("=" * 70 + "\n\n")
    for lo, hi in merged:
        block_start = entries[lo][0]
        block_end = entries[hi][1]
        out.write(f"--- [{block_start} --> {block_end}] ---\n")
        for j in range(lo, hi + 1):
            marker = ">>" if j in hits else "  "
            out.write(f"{marker} [{entries[j][0]}] {entries[j][2]}\n")
        out.write("\n")

print(f"Wrote {len(merged)} clusters ({len(hits)} matching lines) to {out_path}")
