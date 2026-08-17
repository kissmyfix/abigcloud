// Render logic for the IDB 990 comparison page. Nothing entity-specific lives
// here — all facts live in overview.js (GALLATIN_990_DATA / OVERVIEW_CONCLUSIONS).
// Adding a year or a figure is a data edit there, not an HTML edit here.

function fmtMoney(n) {
  const neg = n < 0;
  const v = "$" + Math.abs(Math.round(n)).toLocaleString("en-US");
  return neg ? "-" + v : v;
}

function flagBadge(flag, label) {
  const text = label || { confirmed: "Confirmed", unverified: "Unverified", corrected: "Corrected" }[flag];
  return `<span class="src-flag ${flag}">${text}</span>`;
}

function renderOverview(conclusions) {
  const cards = conclusions.map(c => `
    <div class="overview-card">
      <div class="oc-flag">${flagBadge(c.flag)}</div>
      <div class="oc-text">${c.text}</div>
    </div>`).join("\n");
  return `<div class="overview-grid">${cards}</div>`;
}

function renderBreakdownTable(bd) {
  if (!bd) return "";
  const rows = bd.rows.map(([label, amt]) =>
    `<tr><td>${label}</td><td class="bd-amt">${fmtMoney(amt)}</td></tr>`
  ).join("\n");
  return `
    <div class="bd-section-title">${bd.title}</div>
    <table class="bd-table">
      ${rows}
      <tr class="bd-total"><td>Total</td><td class="bd-amt">${fmtMoney(bd.total)}</td></tr>
    </table>`;
}

function renderYearPanel(year, y, active) {
  const netClass = y.net < 0 ? " neg" : "";
  const statGrid = `
    <div class="stat-grid">
      <div class="stat-card"><div class="stat-value">${fmtMoney(y.revenue)}</div><div class="stat-label">Total revenue</div></div>
      <div class="stat-card"><div class="stat-value">${fmtMoney(y.expenses)}</div><div class="stat-label">Total expenses</div></div>
      <div class="stat-card"><div class="stat-value${netClass}">${fmtMoney(y.net)}</div><div class="stat-label">Revenue less expenses</div></div>
      <div class="stat-card"><div class="stat-value">${fmtMoney(y.assetsEnd)}</div><div class="stat-label">Net assets, end of year</div></div>
    </div>`;

  const missionFlag = y.missionChangedFlag ? flagBadge(y.missionChangedFlag, y.missionChangedFlag === "corrected" ? "Changed, marked “No”" : "Consistent") : "";
  const mission = `
    <div class="mission-quote">
      <span class="mq-label">Stated mission (Part III / Part I, Line 1) ${missionFlag}</span>
      &ldquo;${y.mission}&rdquo;
    </div>`;

  const filingLine = `
    <div class="filing-line">
      <span><b>Form:</b> ${y.formType}</span>
      <span><b>Fiscal year:</b> ${y.fiscalYear}</span>
      <span><b>Preparer:</b> ${y.preparer}</span>
      <span><b>Signed:</b> ${y.signedDate}</span>
    </div>`;

  const revBd = y.revenueBreakdown ? `
    <div class="bd-section-title">Revenue breakdown (Part VIII)</div>
    <table class="bd-table">
      ${y.revenueBreakdown.rows.map(([l,a]) => `<tr><td>${l}</td><td class="bd-amt">${fmtMoney(a)}</td></tr>`).join("\n")}
      <tr class="bd-total"><td>Total</td><td class="bd-amt">${fmtMoney(y.revenueBreakdown.total)}</td></tr>
    </table>` : "";

  const expBdA = renderBreakdownTable(y.expenseBreakdownA);
  const expBdB = renderBreakdownTable(y.expenseBreakdownB);
  const bdNote = (y.expenseBreakdownA && y.expenseBreakdownB) ?
    `<div class="bd-note">These two breakdowns are from the same filing, same signature, and describe the same category of spending — they do not reconcile.</div>` : "";

  const govRows = y.flags.map(f => `
    <div class="gov-row">
      <span class="gov-q">${f.q}</span>
      ${flagBadge(f.flag)}
      <span class="gov-detail">${f.a}</span>
    </div>`).join("\n");

  const boardNote = y.boardReviewNote ? `<div class="bd-note" style="margin-top:10px;">Schedule O, on board review timing: &ldquo;${y.boardReviewNote}&rdquo;</div>` : "";

  return `<div id="panel-${year}" class="panel${active ? " active" : ""}">
    ${statGrid}
    ${mission}
    ${filingLine}
    ${revBd}
    ${expBdA}
    ${expBdB}
    ${bdNote}
    <div class="bd-section-title">Governance &amp; consistency checks</div>
    ${govRows}
    ${boardNote}
  </div>`;
}

function tabFlagClass(y) {
  const flags = y.flags.map(f => f.flag);
  if (flags.includes("corrected")) return " flag-corrected";
  if (flags.includes("unverified")) return " flag-unverified";
  return " flag-confirmed";
}

function renderYearBlock(data) {
  const years = Object.keys(data.years).sort();
  const defaultYear = years[years.length - 1];
  const tabs = years.map(y =>
    `<div class="tab${y === defaultYear ? " active" : ""}${tabFlagClass(data.years[y])}" onclick="showYear('${y}')">${y}</div>`
  ).join("\n");
  const panels = years.map(y => renderYearPanel(y, data.years[y], y === defaultYear)).join("\n");
  return `<div class="year-block">
    <div class="tabs">${tabs}</div>
    ${panels}
  </div>`;
}

function showYear(year) {
  document.querySelectorAll(".year-block .panel").forEach(p => p.classList.remove("active"));
  document.querySelectorAll(".year-block .tab").forEach(t => t.classList.remove("active"));
  document.getElementById(`panel-${year}`).classList.add("active");
  event.target.classList.add("active");
}

function renderApp() {
  document.getElementById("overview-mount").innerHTML = renderOverview(OVERVIEW_CONCLUSIONS);
  document.getElementById("years-mount").innerHTML = renderYearBlock(GALLATIN_990_DATA);
}

document.addEventListener("DOMContentLoaded", renderApp);
