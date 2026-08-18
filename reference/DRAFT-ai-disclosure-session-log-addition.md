# DRAFT for your edit — proposed addition to "How This Investigation Uses AI"

Not published. Written 2026-08-17 for Brandon to rewrite in his own voice, cut, or
discard. Suggested placement: after "The verifiable facts of the division of labor."

---

## A dated log of AI work sessions

The division of labor above is the policy. This is the record. Every substantial AI
work session gets an entry, written the day it happened, naming what the tool did and
what I checked afterward. A policy anyone can read is worth less than a log anyone can
audit.

### 2026-08-17

Claude Opus 5, via Claude Code, working on my machine with access to this archive.

**What it did.**

Built the publishing pipeline that puts an article on this site with working citations.
The draft I write uses file paths that only work on my own disk; the pipeline copies each
cited document onto the site and rewrites the link, so a citation you click opens the
document itself. It also generates the Sources index.

Ran OCR over four IRS Form 990 filings that were image-only scans. Those four had been
transcribed by hand and flagged in the archive as a known weakness. They are now
machine-readable, and every figure I had transcribed checks out against the machine
text, including the "Summer County 69549" line and the $2,291,692 "PILOT fees
distributed" entry with no recipient named.

Extracted text from 85 more PDFs across the archive, taking it from 76 of 173 documents
searchable to 161. That made the state Comptroller's PILOT reports searchable for the
first time, which produced a finding I did not have this morning: in the 2022 report,
Woolhawk LLC lists ten parcels worth $24,019,345 and reports $5,539 to the city and
nothing to the county, while another company in the same table reports $6,382 to the
county on one seventh the property value.

Fixed things on this site that were broken: fifteen pages had lost their headings, six
places promised readers a source repository that did not contain the sources, and the
article's hero image was being served at fourteen times the size it needed to be.

**What it got wrong.**

Early in the session it told me a claim of mine was unsupportable, having searched only
TVA's own website and found nothing. TVA is a subject of this investigation. Its silence
is not evidence. I sent it back to look for local reporting, and the reporting existed:
a $1.1 billion overhaul of the Gallatin plant, covered by the Chattanooga Times Free
Press in 2013 and 2016. It also misread one of my own sentences as sloppy when it was
correct as written.

**What it caught in my work.**

Three numbers in my draft did not survive being checked. My count of Tennessee IDBs
filing 990s was wrong, it is eight rather than five. My "$0 to the county" line was
imprecise: zero to the county, but $5,539 to the city. And my most quotable claim, that
Gallatin is the only IDB in Tennessee filing as a 501(c)(4), has no document behind it in
my archive. I would rather find that out here than in a comment section.

**What stayed mine.**

Every word of the article. Every decision about what runs and what does not. The reading
of what any of it means.

**Attribution.** Commits from this session were authored under my GitHub account. That
was an oversight, not a claim: git supports co-authorship and later commits carry a
`Co-Authored-By` trailer naming the tool. This entry is the correction for the ones that
do not.
