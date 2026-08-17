// Data and high-level conclusions for the Gallatin IDB 990 comparison (2020–2024).
// Every figure here traces back to usa_federal/irs_990_data/gallatin_idb/idb2020.pdf,
// idb2021.pdf, idb2022.pdf, idb2023.pdf, idb2024.pdf. This file holds the facts;
// idb-render.js holds the (entity-agnostic) rendering logic.

const OVERVIEW_CONCLUSIONS = [
  {
    flag: "corrected",
    text: "The <strong>2020 filing contradicts itself internally</strong>: Schedule O says $69,549 went to Sumner County; Part III, filed in the same document, says only $17,474 did — with two new names, Beretta and Bradford, absorbing the other $53,074."
  },
  {
    flag: "corrected",
    text: "The <strong>mission statement changes materially between 2021 and 2022</strong>, moving from generic recruitment language to a specific (and misleadingly worded) description of PILOT administration — while the form answers 'No' to having made any significant change, both years."
  },
  {
    flag: "unverified",
    text: "<strong>$45,000 in \"consulting fees\" and $12,000 in \"management\" fees</strong> appear for the first time in 2024, paid to no one named on the return, the same year net assets swing from a $904,342 high to $148,027."
  },
  {
    flag: "unverified",
    text: "The board went from <strong>reporting no independent audit (2020–2021)</strong> to <strong>self-reporting one every year from 2022 on</strong> — the same year the mission statement changed and the first direct \"Sumner County School\" payment line appears."
  }
];

const GALLATIN_990_DATA = {
  entityName: "Industrial Development Board of the City of Gallatin, TN",
  ein: "38-4171308",
  years: {
    2020: {
      formType: "990-EZ",
      fiscalYear: "07-01-2020 to 06-30-2021",
      revenue: 100048,
      expenses: 114692,
      net: -14644,
      assetsBegin: 102948,
      assetsEnd: 88304,
      mission: "Recruit and Facilitate industrial development in the City of Gallatin, Tennessee",
      missionChangedFlag: null, // 990-EZ has no Part III Line 2/3 equivalent
      significantChange: null,
      audited: null, // not asked in the same way on the EZ
      boardReviewNote: null,
      preparer: "J Michael Patterson",
      signedDate: "2021-11-14",
      board: ["Allen Ramsey (Chair)", "Ryan Clinard (Vice Chair)", "Larry Wise (Treasurer)", "Joanne Walker (Secretary)", "Derrick Jackson", "Leonard Assante", "P J Davis"],
      revenueBreakdown: null, // EZ doesn't itemize revenue the way full 990 does
      expenseBreakdownA: {
        title: "Schedule O (tied to Part I, Line 16 \"Other expenses\")",
        rows: [["Sumner County", 69549], ["Legal", 5557]],
        total: 75106
      },
      expenseBreakdownB: {
        title: "Part III, Line 28 (\"Total program service expenses\")",
        rows: [["Sumner County", 17474], ["Beretta", 39919], ["Bradford", 13155]],
        total: 70548
      },
      flags: [
        { q: "Independent audit?", a: "Not asked in this form's equivalent section", flag: "unverified" },
        { q: "Significant change in program services?", a: "No mechanism to ask on 990-EZ this year", flag: "unverified" },
        { q: "Internal consistency of \"payments in lieu of taxes\" figures", a: "Schedule O ($75,106 total, $69,549 to Sumner County) does not reconcile with Part III ($70,548 total, $17,474 to Sumner County) — same return, same signature.", flag: "corrected" }
      ]
    },
    2021: {
      formType: "990",
      fiscalYear: "07-01-2021 to 06-30-2022",
      revenue: 145425,
      expenses: 136802,
      net: 8623,
      assetsBegin: 88304,
      assetsEnd: 98131,
      mission: "Recruit and facilitate industrial development in the City of Gallatin TN",
      missionChangedFlag: "confirmed",
      significantChange: "No",
      audited: "No",
      boardReviewNote: "Due to time constraints, the board reviews the Form 990 after it is filed. The board administrator reviews it prior to filing.",
      preparer: "Joe Osterfeld CPA",
      signedDate: "2022-11-21",
      board: ["Allan Ramsey (Chair)", "Ryan Clinard (Vice Chair)", "Joanne Walker (Secretary)", "Leonard Assante", "Neil Burgess", "Britanie Earle", "Derrick Jackson"],
      revenueBreakdown: { rows: [["Pilot payments", 123537], ["Legal payments", 15129], ["Maintenance fees", 3277], ["Application fees", 3482]], total: 145425 },
      expenseBreakdownA: {
        title: "Part IX (Statement of Functional Expenses)",
        rows: [["Legal", 18096], ["Accounting", 750], ["Other (11g)", 3966], ["Insurance", 1204], ["Property taxes", 107488], ["Lawn care, Industrial Park", 5211], ["Public notice", 87]],
        total: 136802
      },
      expenseBreakdownB: null,
      flags: [
        { q: "Independent audit?", a: "No", flag: "unverified" },
        { q: "Significant change in program services?", a: "No — despite the mission statement changing substantively the following year", flag: "unverified" },
        { q: "Board review before filing?", a: "No — the board's own Schedule O narrative states it reviews the form only after filing", flag: "corrected" }
      ]
    },
    2022: {
      formType: "990",
      fiscalYear: "07-01-2022 to 06-30-2023",
      revenue: 334268,
      expenses: 244797,
      net: 89471,
      assetsBegin: 98131,
      assetsEnd: 187602,
      mission: "The IDB is responsible for administration of the PILOT program which involves payments in lieu of taxes. Payments are primarily payments to the county (Gallatin) in which the City of Gallatin is located. Other expenses are related to the operation of the Industrial Park.",
      missionChangedFlag: "corrected",
      significantChange: "No",
      audited: "Yes",
      boardReviewNote: "The board administrator reviews it prior to filing. The board reviews the form at the next board meeting.",
      preparer: "John P Young PC",
      signedDate: "2023-11-13",
      board: ["Phil Carver", "Derrick Jackson", "Jesse Maness", "Stan Carver", "Neil Burgess", "Leonard Assante", "Allan Ramsey (Chair)", "Preston Stark (Board Administrator)", "Joanne Walker (Secretary)", "Ryan Clinard (Vice Chair)"],
      revenueBreakdown: { rows: [["Pilot payments", 326731], ["Maintenance fees", 4372], ["Legal fees", 1559], ["Other fees", 1606]], total: 334268 },
      expenseBreakdownA: {
        title: "Part IX (Statement of Functional Expenses)",
        rows: [["Legal", 15627], ["Accounting", 400], ["Advertising", 683], ["Office", 269], ["Occupancy", 8890], ["Insurance", 2408], ["Property taxes", 141791], ["Payment, Sumner County School", 74622], ["Fees", 107]],
        total: 244797
      },
      expenseBreakdownB: null,
      flags: [
        { q: "Independent audit?", a: "Yes — first year claiming one, same year mission text changed", flag: "unverified" },
        { q: "Significant change in program services?", a: "No — filed the same year the mission statement was rewritten from generic recruitment language to PILOT-fund administration language", flag: "corrected" },
        { q: "Mission statement wording", a: "\"Payments are primarily payments to the county (Gallatin) in which the City of Gallatin is located\" — conflates the city and the county; Sumner County is the county, not Gallatin", flag: "corrected" },
        { q: "First \"Sumner County School\" line item", a: "$74,622 — first year this specific payment category appears, separate from the general \"Property taxes\" line", flag: "unverified" }
      ]
    },
    2023: {
      formType: "990",
      fiscalYear: "07-01-2023 to 06-30-2024",
      revenue: 1796648,
      expenses: 1079908,
      net: 716740,
      assetsBegin: 187602,
      assetsEnd: 904342,
      mission: "The IDB is responsible for administration of the PILOT program which involves payments in lieu of taxes. Payments are primarily payments to the county (Gallatin) in which the City of Gallatin is located. Other expenses are related to the operation of the Industrial Park.",
      missionChangedFlag: "confirmed", // unchanged from 2022, i.e. consistent with the (already flagged) prior year
      significantChange: "No",
      audited: "Yes",
      boardReviewNote: "The board administrator reviews it prior to filing. The board reviews the form at the next board meeting.",
      preparer: "John P Young PC",
      signedDate: "2024-11-13",
      board: ["Phil Carver", "Derrick Jackson", "Jesse Maness", "Stan Carver", "Leonard Assante", "Neil Burgess (Vice-Chair)", "Preston Stark (Board Administrator)", "Allan Ramsey (Chair)", "Joanne Walker (Secretary)"],
      revenueBreakdown: { rows: [["Pilot payments", 1758136], ["Maintenance fees", 34371], ["Other fees", 4141]], total: 1796648 },
      expenseBreakdownA: {
        title: "Part IX (Statement of Functional Expenses)",
        rows: [["Accounting", 4641], ["Office", 1755], ["Occupancy", 9384], ["Insurance", 1204], ["PILOT fees distributed", 155475], ["Payment, Sumner County School", 901080], ["Fees", 3032], ["Miscellaneous", 3337]],
        total: 1079908
      },
      expenseBreakdownB: null,
      flags: [
        { q: "Independent audit?", a: "Yes (self-reported, as in 2022)", flag: "unverified" },
        { q: "Significant change in program services?", a: "No", flag: "unverified" },
        { q: "Sumner County School payment", a: "$901,080 — a 12x jump from 2022's $74,622, tracking the Woolhawk buildings coming online", flag: "unverified" }
      ]
    },
    2024: {
      formType: "990",
      fiscalYear: "07-01-2024 to 06-30-2025",
      revenue: 2242221,
      expenses: 2998536,
      net: -756315,
      assetsBegin: 904342,
      assetsEnd: 148027,
      mission: "The IDB is responsible for administration of the PILOT program which involves payments in lieu of taxes. Payments are primarily payments to the county (Gallatin) in which the City of Gallatin is located. Other expenses are related to the operation of the Industrial Park.",
      missionChangedFlag: "confirmed",
      significantChange: "No",
      audited: "Yes",
      boardReviewNote: "The board administrator reviews it prior to filing. The board reviews the form at the next board meeting.",
      preparer: "John P Young PC",
      signedDate: "2025-08-15",
      board: ["Allan Ramsey", "Derrick Jackson", "Phil Carver", "Stan Carver", "Jesse Maness", "Don Cunningham", "Joanne Walker (Secretary)", "Leonard Assante (Treasurer)", "Neil Burgess (Chair)", "Preston Stark (Board Administrator)"],
      revenueBreakdown: { rows: [["Pilot payments", 2210996], ["Maintenance fees", 19372], ["Legal fees", 9980], ["Other fees", 1873]], total: 2242221 },
      expenseBreakdownA: {
        title: "Part IX (Statement of Functional Expenses)",
        rows: [["Management", 12000], ["Office", 1766], ["Occupancy", 6364], ["Insurance", 1204], ["PILOT fees distributed", 2291692], ["Payment, Sumner County School", 640457], ["Consulting fees", 45000], ["Miscellaneous", 53]],
        total: 2998536
      },
      expenseBreakdownB: null,
      flags: [
        { q: "Independent audit?", a: "Yes (self-reported)", flag: "unverified" },
        { q: "Significant change in program services?", a: "No", flag: "unverified" },
        { q: "New unnamed-recipient fees", a: "$45,000 \"Consulting fees\" + $12,000 \"Management\" — first appearance of either line, no recipient named, no 1099s on file", flag: "corrected" },
        { q: "Net assets", a: "Fell from $904,342 to $148,027 in one year — a $756,315 loss, the only losing year on record", flag: "unverified" },
        { q: "Filing timing", a: "Signed 2025-08-15 — months earlier than every prior year's November signature, a break from the established pattern", flag: "unverified" }
      ]
    }
  }
};
