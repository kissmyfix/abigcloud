"""Search beats for the headline sweep, in three tiers.

Tier A  statewide Tennessee data center coverage
Tier B  Middle Tennessee, including the growth stories that ride alongside
Tier C  Quid-Pro-NO mechanisms; data centers optional

Geographic queries MUST carry a topic term. "Sumner County Tennessee" alone returns
lottery results and obituaries.
"""

BEATS = [
    ("A", "tn-dc",           "Tennessee data center"),
    ("A", "tn-power",        "Tennessee data center electricity ratepayers"),
    ("A", "tn-tva",          "TVA data center rate"),

    ("B", "midtn",           "Middle Tennessee data center"),
    ("B", "gallatin",        "Gallatin Tennessee data center OR annexation OR council"),
    ("B", "sumner",          "Sumner County Tennessee growth OR zoning OR schools"),
    ("B", "nashville",       "Nashville data center OR Metro Council development"),
    ("B", "clarksville",     "Clarksville Montgomery County Tennessee development incentive"),
    ("B", "rutherford",      "Rutherford OR Wilson County Tennessee development data center"),
    ("B", "annex",           "Tennessee city annexation growth impact fees"),

    ("C", "idb",             "Tennessee industrial development board"),
    ("C", "pilot",           "Tennessee payment in lieu of taxes PILOT"),
    ("C", "abate",           "Tennessee property tax abatement incentive"),
    ("C", "idd",             "Tennessee infrastructure development district"),
    ("C", "tif",             "Tennessee tax increment financing"),
    ("C", "comptroller",     "Tennessee comptroller audit county city"),
    ("C", "incentive",       "Tennessee economic development incentive deal"),
]

# Publisher domains that block automated fetches. Skip early rather than pay twice.
BLOCKED = {
    "timesfreepress.com",
    "datacenterdynamics.com",
    "decaturdaily.com",
    "wkrn.com",
    "news.google.com",     # redirect interstitial requires JS
    "fox17.com",           # Sinclair search/article render is JS-driven
    "newschannel9.com",
}

# Headlines that are noise regardless of beat.
NOISE = (
    "lottery results", "obituary", "football schedule", "football scores",
    "high school", "weekend:", "things to do", "arrest", "crash", "shooting",
)
