// Renderer for the Sumner County PILOT tracker.
// Takes ENTITIES_DATA / COUNTY_DATA (tracker-data.js) and builds the whole page.
// All entity/year markup is generated here — adding a new entity or year is a data change, not an HTML edit.

const CATEGORY = {
  rent:   { label: "Rent",             base: [58,110,168],  cssVar: "var(--blue-text)" },
  city:   { label: "PILOT &rarr; City",  base: [181,137,12],  cssVar: "var(--gold)" },
  county: { label: "PILOT &rarr; County", base: [200,65,10], cssVar: "var(--accent)" },
};

// Supporting-documents tabs, shared across every entity. Same set for all — add a new category here
// once and it appears on every entity page. An entity with nothing filed for a category just shows
// a placeholder note; that's real information (nothing found yet), not a rendering gap.
const DOC_CATEGORIES = [
  { key: "overview",   label: "Overview" },
  { key: "assessment", label: "Assessment Data" },
  { key: "findings",   label: "Key Findings & Notes" },
  { key: "questions",  label: "Unanswered Questions" },
  { key: "council",    label: "Council Notes" },
  { key: "irs",        label: "IRS Filings" },
];

function parseMoney(raw) {
  if (raw == null) return null;
  const s = String(raw).trim();
  if (s === "" || s === "—" || s === "&mdash;" || /no info/i.test(s)) return null;
  const cleaned = s.replace(/[$,]/g, "").replace(/&mdash;|—/g, "");
  const n = parseFloat(cleaned);
  return isNaN(n) ? null : n;
}

function fmtMoney(n) {
  return "$" + Math.round(n).toLocaleString("en-US");
}

// donut-center total: 2 decimals on millions, no tilde (it's an exact sum)
function fmtShort(n) {
  const abs = Math.abs(n);
  if (abs >= 1e6) return "$" + (n/1e6).toFixed(2) + "M";
  if (abs >= 1e3) return "$" + Math.round(n/1e3) + "K";
  return "$" + Math.round(n);
}

// individual wedge label: 1 decimal on millions, always approximate
function fmtShortSlice(n) {
  const abs = Math.abs(n);
  if (abs >= 1e6) return "~$" + (n/1e6).toFixed(1) + "M";
  if (abs >= 1e3) return "~$" + Math.round(n/1e3) + "K";
  return "~$" + Math.round(n);
}

function shades(base, n) {
  const out = [];
  for (let i=0;i<n;i++) {
    const t = n>1 ? i/(n-1) : 0.5;
    const light = base.map(c => Math.round(c + (255-c)*0.72));
    const dark = base.map(c => Math.round(c*0.4));
    let c;
    if (t < 0.5) {
      const f = t/0.5;
      c = base.map((b,j) => Math.round(light[j] + (b-light[j])*f));
    } else {
      const f = (t-0.5)/0.5;
      c = base.map((b,j) => Math.round(b + (dark[j]-b)*f));
    }
    out.push("#" + c.map(v => v.toString(16).padStart(2,"0")).join(""));
  }
  return out;
}

function luminance(hex) {
  hex = hex.replace("#","");
  const r = parseInt(hex.slice(0,2),16), g = parseInt(hex.slice(2,4),16), b = parseInt(hex.slice(4,6),16);
  return (0.299*r + 0.587*g + 0.114*b) / 255;
}

// yearVals: array of [year, amount] ascending, amount > 0 only
function buildPie(yearVals, catLabel) {
  const total = yearVals.reduce((a,[,v]) => a+v, 0);
  if (total === 0) return { nodata: true, cat: catLabel };
  const base = catLabel.includes("Rent") ? CATEGORY.rent.base : catLabel.includes("City") ? CATEGORY.city.base : CATEGORY.county.base;
  const colors = shades(base, yearVals.length);
  let cum = 0;
  const CX=115, CY=115, R=85;
  const labels = [];
  const stops = [];
  yearVals.forEach(([yr,val], i) => {
    const pct = val/total*100;
    const start = cum, end = cum+pct;
    stops.push(`${colors[i]} ${start.toFixed(2)}% ${end.toFixed(2)}%`);
    const mid = start + pct/2;
    const rad = mid*3.6*Math.PI/180;
    const x = CX + R*Math.sin(rad), y = CY - R*Math.cos(rad);
    const textColor = luminance(colors[i]) > 0.55 ? "#1a1814" : "#faf7f0";
    const show = (pct*3.6) >= 14;
    labels.push({ year: yr, val, x: x.toFixed(1), y: y.toFixed(1), color: textColor, show, swatch: colors[i] });
    cum = end;
  });
  return { nodata: false, total, gradient: stops.join(", "), labels, cat: catLabel };
}

function renderPieCell(pie) {
  if (pie.nodata) {
    return `<div class="p-cell">
      <div class="p-pie-wrap"><div class="p-pie nodata"></div><div class="p-donut-hole nodata"><div class="p-donut-cat">${pie.cat}</div><div class="p-pie-label">$0.00</div><div class="p-pie-sub">No Data Reported</div></div></div>
      <div class="p-key"><div class="p-key-row p-key-note">$0.00 reported in every year with data on file.</div></div>
    </div>`;
  }
  const labelsHtml = pie.labels.filter(l=>l.show).map(l => {
    const fs = l.val < 100000 ? " font-size:11px;" : "";
    return `<div class="p-slice-val" style="left:${l.x}px; top:${l.y}px; color:${l.color};${fs}">${fmtShortSlice(l.val)}</div>`;
  }).join("\n");
  const keyHtml = pie.labels.map(l => {
    const note = l.show ? "" : `<span class="p-key-note">&nbsp;too small to label</span>`;
    return `<div class="p-key-row"><div class="p-swatch" style="background:${l.swatch};"></div><div class="p-key-yr">${l.year}</div><div class="p-key-amt">${fmtMoney(l.val)}</div>${note}</div>`;
  }).join("\n");
  const yrs = pie.labels.map(l=>l.year);
  const yrRange = yrs.length>1 ? `${yrs[0]}&ndash;${yrs[yrs.length-1]}` : yrs[0];
  return `<div class="p-cell">
    <div class="p-pie-wrap">
      <div class="p-pie" style="background: conic-gradient(${pie.gradient});"></div>
      <div class="p-donut-hole"><div class="p-donut-cat">${pie.cat}</div><div class="p-pie-label">${fmtShort(pie.total)}</div><div class="p-pie-sub">Total, ${yrRange}</div></div>
${labelsHtml}
    </div>
    <div class="p-key">
${keyHtml}
    </div>
  </div>`;
}

function cellClass(header, value) {
  if (/no info/i.test(value)) return "noinfo";
  if (["Rent","PILOT/CI","PILOT/CO"].includes(header) && parseMoney(value) === 0) return "zero";
  return "";
}

function renderYearPanel(entity, year, ydata, active) {
  const id = `${entity.prefix}-${year}`;
  if (ydata.type === "absent") {
    return `<div id="${id}" class="panel${active?" active":""}"><div class="absent-note">${ydata.note}</div></div>`;
  }
  const { headers, rows, total, warn, totalsLine } = ydata;

  const theadCells = headers.map(h => `<th>${h}</th>`).join("");
  const bodyRows = rows.map(r => {
    const cells = headers.map(h => {
      const v = r[h] ?? "";
      const cls = cellClass(h, v);
      return `<td${cls?` class="${cls}"`:""}>${v}</td>`;
    }).join("");
    return `<tr>${cells}</tr>`;
  }).join("\n        ");
  const totCells = headers.map(h => {
    const v = total[h] ?? "";
    const cls = ["Rent","PILOT/CI","PILOT/CO"].includes(h) ? cellClass(h, v) : "";
    return `<td${cls?` class="${cls}"`:""}>${v}</td>`;
  }).join("");

  const warnHtml = warn ? `<div class="warn-box">${warn}</div>\n    ` : "";

  return `<div id="${id}" class="panel${active?" active":""}">
    <div class="totals-line">${totalsLine}</div>
    ${warnHtml}<div class="table-wrap"><table>
      <thead><tr>${theadCells}</tr></thead>
      <tbody>
        ${bodyRows}
        <tr class="totrow">${totCells}</tr>
      </tbody>
    </table></div>
  </div>`;
}

function entitySidebarPies(entity) {
  const years = Object.keys(entity.years).filter(y => entity.years[y].type === "data").sort();
  const seriesFor = (header) => years
    .map(y => [y, parseMoney(entity.years[y].total[header])])
    .filter(([,v]) => v != null && v > 0);
  const rentPie = buildPie(seriesFor("Rent"), "Rent");
  const cityPie = buildPie(seriesFor("PILOT/CI"), "PILOT &rarr; City");
  const countyPie = buildPie(seriesFor("PILOT/CO"), "PILOT &rarr; County");
  return [countyPie, cityPie, rentPie].map(renderPieCell).join("\n      ");
}

function renderEntityPage(entity) {
  const years = Object.keys(entity.years).sort();
  const yearTabs = years.map(y => {
    const hasData = entity.years[y].type === "data";
    const stateClass = hasData ? " tab-hasdata" : " tab-nodata";
    return `<div class="tab${stateClass}${y===entity.defaultYear?" active":""}" onclick="showTab('${entity.prefix}','${y}')">${y}</div>`;
  }).join("\n    ");
  const yearPanels = years.map(y => renderYearPanel(entity, y, entity.years[y], y===entity.defaultYear)).join("\n  ");

  const docs = entity.docs || {};
  const docTabs = DOC_CATEGORIES.map((c, i) =>
    `<div class="tab${i===0?" active":""}" onclick="showDoc('${entity.prefix}','${c.key}')">${c.label}</div>`
  ).join("\n    ");
  const docPanels = DOC_CATEGORIES.map((c, i) => {
    const content = docs[c.key];
    const body = content ? content : `<div class="doc-note">Nothing added yet for ${entity.name} &mdash; ${c.label}.</div>`;
    return `<div id="${entity.prefix}-doc-${c.key}" class="panel${i===0?" active":""}">${body}</div>`;
  }).join("\n  ");

  return `<div id="${entity.id}" class="corp-page">
  <div class="corp-body">
  <div class="corp-main">
  <div class="tabs-row">
  <div class="tabs-row-title">
  <h1>${entity.name}</h1>
  <div class="corp-addr">${entity.addr}</div>
  </div>
  <div class="tabs">
    ${docTabs}
  </div>
  </div>
  <div class="docs-block">
  ${docPanels}
  </div>
  <div class="year-block">
  <div class="tabs">
    ${yearTabs}
  </div>
  ${yearPanels}
  </div>
  </div>

  <div class="corp-sidebar">
  <div class="chart-wrap">
    <div class="chart-title">Reported financial amounts, by category</div>
    <div class="p-grid">
      ${entitySidebarPies(entity)}
    </div>
  </div>
  </div>
  </div>
</div>`;
}

function renderBarCol(title, colorVar, items) {
  const max = Math.max(...items.map(i=>i.value));
  const rows = items.map(i => {
    const pct = (i.value/max*100).toFixed(1);
    return `<div class="bar-row"><div class="bar-label">${i.label}</div><div class="bar-track"><div class="bar-fill" style="width:${pct}%; background:${colorVar};"></div></div><div class="bar-val">${fmtMoney(i.value)}</div></div>`;
  }).join("\n        ");
  return `<div class="bar-col">
        <div class="bar-col-title" style="color:${colorVar};">${title}</div>
        ${rows}
      </div>`;
}

function renderCountyTotals(county) {
  return `<div id="countytotals" class="corp-page active">
  <h1>Sumner County — PILOT Totals</h1>
  <p class="sub">${county.subtitle}</p>

  <div class="chart-wrap" style="max-width:1000px;">
    <div class="chart-title">All-time totals, as reported</div>
    <div class="totals" style="margin-bottom:0;">
      <div class="tot"><div class="l">Total Rent</div><div class="v blue">${fmtMoney(county.totals.rent)}</div></div>
      <div class="tot"><div class="l">PILOT &rarr; City</div><div class="v gold">${fmtMoney(county.totals.city)}</div></div>
      <div class="tot"><div class="l">PILOT &rarr; County</div><div class="v red">${fmtMoney(county.totals.county)}</div></div>
    </div>
  </div>

  <div class="chart-wrap" style="max-width:1000px; margin-top:20px;">
    <div class="chart-title">By entity, all-time totals (entities with $0 reported in a category are omitted from that column)</div>
    <div class="bar-section">
      ${renderBarCol("Rent", "var(--blue-text)", county.bars.rent)}
      ${renderBarCol("PILOT &rarr; City", "var(--gold)", county.bars.city)}
      ${renderBarCol("PILOT &rarr; County", "var(--red-text)", county.bars.county)}
    </div>
    <div class="p-key" style="margin-top:20px;">
      <div class="p-key-row p-key-note">${county.note}</div>
    </div>
  </div>
</div>`;
}

function renderNav(entities) {
  const entityBtns = entities.map(e => `<div class="corp-btn" onclick="showCorp('${e.id}')">${e.navLabel}</div>`).join("\n  ");
  return `<div class="corp-btn active" onclick="showCorp('countytotals')">Sumner County Totals</div>
  ${entityBtns}`;
}

function showCorp(id) {
  document.querySelectorAll(".corp-page").forEach(p => p.classList.remove("active"));
  document.querySelectorAll(".corp-btn").forEach(b => b.classList.remove("active"));
  document.getElementById(id).classList.add("active");
  event.target.classList.add("active");
}

function showTab(prefix, year) {
  const panel = document.getElementById(`${prefix}-${year}`);
  const block = panel.closest(".year-block");
  block.querySelectorAll(".panel").forEach(p => p.classList.remove("active"));
  block.querySelectorAll(".tab").forEach(t => t.classList.remove("active"));
  panel.classList.add("active");
  event.target.classList.add("active");
}

function showDoc(prefix, key) {
  const panel = document.getElementById(`${prefix}-doc-${key}`);
  const page = panel.closest(".corp-page");
  page.querySelectorAll(".docs-block .panel").forEach(p => p.classList.remove("active"));
  page.querySelectorAll(".tabs-row .tab").forEach(t => t.classList.remove("active"));
  panel.classList.add("active");
  event.target.classList.add("active");
}

function renderApp() {
  document.getElementById("corp-nav").innerHTML = renderNav(ENTITIES_DATA);
  const pages = [renderCountyTotals(COUNTY_DATA), ...ENTITIES_DATA.map(renderEntityPage)];
  document.getElementById("corp-pages").innerHTML = pages.join("\n\n");
}

document.addEventListener("DOMContentLoaded", renderApp);
