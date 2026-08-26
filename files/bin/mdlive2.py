#!/usr/bin/env python3
"""mdlive2 — single-pane markdown editor with raw/live toggle.

v2 of Brandon's markdown editor. Same server, new front end: one pane instead
of a split screen, a formatting toolbar, and a toggle that switches between raw
markdown and a site-accurate live preview.

    files/venv/bin/python files/bin/mdlive2.py web/content/faq.md 8181
    # then open http://localhost:8181

The original mdlive.py is untouched and keeps working on its usual port.
"""
import http.server, socketserver, os, sys, json, urllib.parse, mimetypes, tempfile

MD   = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else "README.md")
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 8181

def _find_root(start):
    d = os.path.dirname(start)
    while d != "/":
        if os.path.isdir(os.path.join(d, ".git")):
            return d
        d = os.path.dirname(d)
    return os.path.dirname(os.path.dirname(start))

ROOT = _find_root(MD)

SKIP = {".git", "node_modules", "dist", ".astro", "venv", "__pycache__",
        ".remember", "derived"}

def listing():
    out = []
    for base in (os.path.join(ROOT, "web", "content"),):
        for dirpath, dirnames, filenames in os.walk(base):
            dirnames[:] = [d for d in dirnames if d not in SKIP and not d.startswith(".")]
            for fn in filenames:
                if not fn.endswith(".md") or fn.startswith("."):
                    continue
                rel = os.path.relpath(os.path.join(dirpath, fn), ROOT).replace(os.sep, "/")
                if rel.startswith("web/content/sources/"):
                    continue
                out.append({"rel": rel, "size": os.path.getsize(os.path.join(ROOT, rel))})

    home = os.path.join(ROOT, "web", "index.md")
    if os.path.isfile(home):
        out.append({"rel": "web/index.md", "size": os.path.getsize(home)})

    for e in out:
        rel = e["rel"]
        if rel == "web/index.md":
            e["group"], e["label"] = "Home", "index.md"
        else:
            inner = rel[len("web/content/"):]
            e["group"] = "Top level" if "/" not in inner else inner.split("/")[0]
            e["label"] = inner
    order = {"Home": 0, "Top level": 1}
    out.sort(key=lambda r: (order.get(r["group"], 2), r["group"], r["rel"]))
    return out

def resolve(rel):
    if not rel:
        return MD
    full = os.path.normpath(os.path.join(ROOT, rel))
    return full if full.startswith(ROOT) and os.path.isfile(full) else None

PAGE = r"""<!doctype html>
<html lang="en-US"><head><meta charset="utf-8">
<base href="__BASE__">
<title>__NAME__</title>
<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
<link rel="stylesheet" href="/files/web/node_modules/@fontsource-variable/dm-sans/index.css">
<link rel="stylesheet" href="/files/web/node_modules/@fontsource/dm-serif-display/400.css">
<link rel="stylesheet" href="/files/web/node_modules/@fontsource/dm-serif-display/400-italic.css">
<style>
 :root{--bg:#faf9f7;--fg:#1c1b19;--mut:#6b675f;--rule:#e0ddd6;--acc:#8a5a2b;
       --code:#f0eee9;--pane:#fff}
 @media(prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#16151a;--fg:#e8e6e1;--mut:#96918a;
       --rule:#2e2c33;--acc:#d9a066;--code:#1e1d23;--pane:#1a191f}}
 :root[data-theme="dark"]{--bg:#16151a;--fg:#e8e6e1;--mut:#96918a;
       --rule:#2e2c33;--acc:#d9a066;--code:#1e1d23;--pane:#1a191f}
 *{box-sizing:border-box}
 html,body{height:100%;margin:0}
 body{background:var(--bg);color:var(--fg);display:flex;flex-direction:column;
      font:15px/1.6 system-ui,sans-serif;overflow:hidden}
 #bar{flex:0 0 36px;display:flex;align-items:center;gap:14px;padding:0 14px;
      border-bottom:1px solid var(--rule);font:12px ui-monospace,Menlo,monospace;
      color:var(--mut)}
 #dot{width:7px;height:7px;border-radius:50%;background:#3fb950;transition:.2s}
 #dot.hit{background:var(--acc);transform:scale(1.9)}
 #dot.err{background:#f85149}
 .grow{flex:1}
 button{background:none;border:1px solid var(--rule);color:var(--mut);border-radius:4px;
        padding:3px 9px;font:11px ui-monospace,monospace;cursor:pointer}
 button:hover{color:var(--fg);border-color:var(--acc)}
 button.active{color:var(--acc);border-color:var(--acc)}
 #toolbar{flex:0 0 32px;display:flex;align-items:center;gap:6px;padding:0 14px;
          border-bottom:1px solid var(--rule);background:var(--code)}
 #toolbar button{font-size:12px;padding:2px 8px;border:none;color:var(--mut)}
 #toolbar button:hover{color:var(--fg);background:var(--rule);border-radius:3px}
 #toolbar .sep{width:1px;height:16px;background:var(--rule);margin:0 2px}
 #pane{flex:1;min-height:0;position:relative;overflow:hidden}
 #editor{position:absolute;inset:0;display:flex;background:var(--pane);overflow:auto}
 #preview{position:absolute;inset:0;overflow:auto;display:none}
 #gut{flex:0 0 3.6em;text-align:right;padding:14px 8px 40vh 0;color:var(--mut);
      font:13px/1.7 ui-monospace,Menlo,monospace;user-select:none;background:var(--code)}
 #gut .cur{color:var(--acc);font-weight:700;background:var(--pane);
      box-shadow:inset 2px 0 0 var(--acc)}
 #band{position:absolute;pointer-events:none;display:none;z-index:0;
      background:var(--code);box-shadow:inset 2px 0 0 var(--acc)}
 #ed{flex:1;border:0;outline:0;resize:none;background:transparent;color:var(--fg);
     position:relative;z-index:1;
     caret-color:var(--acc);
     padding:14px 14px 40vh;font:13px/1.7 ui-monospace,Menlo,monospace;
     white-space:pre-wrap;overflow-wrap:break-word;overflow:hidden}
 #mirror{position:absolute;visibility:hidden;pointer-events:none;left:-9999px;top:0;
     padding:0;font:13px/1.7 ui-monospace,Menlo,monospace;
     white-space:pre-wrap;overflow-wrap:break-word}
 #gut div{height:auto}
 #note{color:var(--acc);cursor:pointer}
 .hid{display:none}
 #home{flex:1;overflow:auto;padding:38px 40px 20vh}
 #home h1{font:600 15px/1.4 ui-monospace,Menlo,monospace;color:var(--fg);
      margin:0 0 4px}
 #home p.sub{font:12px/1.5 ui-monospace,Menlo,monospace;color:var(--mut);
      margin:0 0 26px}
 #home .grp{font:11px/1 ui-monospace,Menlo,monospace;color:var(--mut);
      text-transform:uppercase;letter-spacing:.08em;
      margin:22px 0 7px;padding-bottom:6px;border-bottom:1px solid var(--rule)}
 #home a{display:block;padding:6px 9px;margin:0 -9px;border-radius:4px;
      font:13px/1.5 ui-monospace,Menlo,monospace;color:var(--fg);
      text-decoration:none;cursor:pointer}
 #home a:hover{background:var(--code);color:var(--acc)}
 #home a .rel{color:var(--mut);font-size:11px;margin-left:10px}
 #pick{background:var(--pane);color:var(--fg);border:1px solid var(--rule);
       border-radius:4px;padding:3px 6px;max-width:44ch;
       font:12px ui-monospace,Menlo,monospace;cursor:pointer}
 #pick:hover{border-color:var(--acc)}
</style></head>
<body>
<div id="bar">
  <span id="dot"></span>
  <select id="pick" title="open another file"></select>
  <span id="meta"></span>
  <span id="note" class="hid">file changed on disk — click to load</span>
  <span class="grow"></span>
  <span id="pos"></span>
  <button id="ref">copy line ref</button>
  <button id="theme" title="cycle light/dark/system">&#9790;</button>
  <button id="toggle">live</button>
</div>
<div id="toolbar" class="hid">
  <button data-act="bold" title="Bold (Ctrl+B)"><b>B</b></button>
  <button data-act="italic" title="Italic (Ctrl+I)"><i>I</i></button>
  <span class="sep"></span>
  <button data-act="h1" title="Heading 1">H1</button>
  <button data-act="h2" title="Heading 2">H2</button>
  <button data-act="h3" title="Heading 3">H3</button>
  <button data-act="h4" title="Heading 4">H4</button>
  <span class="sep"></span>
  <button data-act="link" title="Link (Ctrl+K)">link</button>
  <button data-act="code" title="Inline code">&lt;&gt;</button>
  <span class="sep"></span>
  <button data-act="quote" title="Blockquote (red)" style="color:#c8410a">&gt;</button>
  <button data-act="q-teal" title="Teal callout" style="color:#0a4f43">&gt;t</button>
  <button data-act="q-blue" title="Blue callout" style="color:#1c4f85">&gt;b</button>
  <button data-act="q-gold" title="Gold callout" style="color:#8a6d2b">&gt;g</button>
  <button data-act="q-green" title="Green callout" style="color:#1c8a5c">&gt;v</button>
  <span class="sep"></span>
  <button data-act="ul" title="Unordered list">&#8226; list</button>
  <button data-act="ol" title="Ordered list">1. list</button>
  <span class="sep"></span>
  <button data-act="codeblock" title="Code block">```</button>
  <button data-act="table" title="Table">&#9638;</button>
  <button data-act="caption" title="Image with caption">img</button>
  <button data-act="infobox" title="Info box">box</button>
  <span class="sep"></span>
  <button data-act="hr" title="Horizontal rule">—</button>
  <button data-act="comment" title="Comment (Ctrl+/)">&lt;!--&gt;</button>
</div>
<div id="home" class="hid">
  <h1>web/content</h1>
  <p class="sub">every page of the site. pick one to edit.</p>
  <div id="homelist"></div>
</div>
<div id="pane" class="hid">
  <div id="editor"><div id="gut"></div><div id="band"></div>
    <textarea id="ed" spellcheck="true"></textarea>
    <div id="mirror"></div></div>
  <div id="preview"></div>
</div>
<script>
const ed=document.getElementById('ed'), preview=document.getElementById('preview'),
      gut=document.getElementById('gut'), dot=document.getElementById('dot'),
      note=document.getElementById('note'), meta=document.getElementById('meta'),
      pos=document.getElementById('pos'), toolbar=document.getElementById('toolbar'),
      editorPane=document.getElementById('editor');
let known=null, dirty=false, saveT=null, pending=null;
let FILE=null;
let ALL=[], ticking=false;
let mode='raw';
const pick=document.getElementById('pick');

async function loadListing(){
  const r=await (await fetch('/api/files')).json();
  ALL = r.files;
  let html='<option value="">— all files —</option>', seen=null;
  for(const f of r.files){
    if(f.group!==seen){ if(seen!==null) html+='</optgroup>';
      html+=`<optgroup label="${f.group}">`; seen=f.group; }
    html+=`<option value="${f.rel}"${f.rel===FILE?' selected':''}>${f.label}</option>`;
  }
  if(seen!==null) html+='</optgroup>';
  pick.innerHTML=html;
}

function showHome(){
  let html='', seen=null;
  for(const f of ALL){
    if(f.group!==seen){ html+=`<div class="grp">${f.group}</div>`; seen=f.group; }
    html+=`<a data-rel="${f.rel}">${f.label}<span class="rel">${f.rel}</span></a>`;
  }
  document.getElementById('homelist').innerHTML=html;
  document.getElementById('home').classList.remove('hid');
  document.getElementById('pane').classList.add('hid');
  toolbar.classList.add('hid');
  meta.textContent=''; pos.textContent='';
}
function openFile(rel){
  FILE = rel;
  known = null; pending = null;
  note.classList.add('hid');
  history.replaceState(null,'','?f='+encodeURIComponent(FILE));
  document.getElementById('home').classList.add('hid');
  document.getElementById('pane').classList.remove('hid');
  setMode('raw');
  for(const o of pick.options) o.selected = (o.value===FILE);
  tick();
  if(!ticking){ ticking=true; setInterval(tick,500); }
}
document.getElementById('homelist').addEventListener('click',e=>{
  const a=e.target.closest('a[data-rel]');
  if(a) openFile(a.dataset.rel);
});
pick.onchange = async () => {
  if(dirty) await save();
  if(!pick.value){
    FILE=null; known=null; pending=null;
    history.replaceState(null,'',location.pathname);
    showHome(); return;
  }
  openFile(pick.value);
};

function setMode(m){
  mode=m;
  const btn=document.getElementById('toggle');
  if(mode==='raw'){
    editorPane.style.display='flex';
    preview.style.display='none';
    toolbar.classList.remove('hid');
    btn.textContent='live';
    btn.classList.remove('active');
  } else {
    render();
    editorPane.style.display='none';
    preview.style.display='block';
    toolbar.classList.add('hid');
    btn.textContent='raw';
    btn.classList.add('active');
  }
}
document.getElementById('toggle').onclick=()=>{
  if(mode==='raw'){
    curLineForScroll = (ed.value.slice(0,ed.selectionStart).match(/\n/g)||[]).length + 1;
    setMode('live');
    scrollPreviewToLine(curLineForScroll);
  } else {
    setMode('raw');
    ed.focus();
  }
};
let curLineForScroll=1;
function scrollPreviewToLine(line){
  const target = (proseEl||preview);
  const blks = target.querySelectorAll('.blk');
  let best = null;
  for(const b of blks){
    if(+b.dataset.line <= line) best = b;
  }
  if(best) best.scrollIntoView({block:'start',behavior:'instant'});
}

const mirror=document.getElementById('mirror');
function autosize(){ ed.style.height='auto'; ed.style.height=ed.scrollHeight+'px'; }
function gutter(lines){
  const cs=getComputedStyle(ed);
  mirror.style.width=(ed.clientWidth
    - parseFloat(cs.paddingLeft) - parseFloat(cs.paddingRight))+'px';
  mirror.innerHTML=lines.map(l=>'<div>'+(l?l.replace(/[&<>]/g,
    c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c])):'&nbsp;')+'</div>').join('');
  gut.innerHTML=[...mirror.children].map((d,i)=>
    '<div style="height:'+d.offsetHeight+'px">'+(i+1)+'</div>').join('');
}
const band=document.getElementById('band');
function curline(){
  const n=(ed.value.slice(0,ed.selectionStart).match(/\n/g)||[]).length;
  const kids=gut.children;
  for(let i=0;i<kids.length;i++) kids[i].classList.toggle('cur',i===n);
  const m=mirror.children[n];
  if(!m){ band.style.display='none'; return; }
  const cs=getComputedStyle(ed);
  band.style.top=(ed.offsetTop+parseFloat(cs.paddingTop)+m.offsetTop)+'px';
  band.style.height=m.offsetHeight+'px';
  band.style.left=ed.offsetLeft+'px';
  band.style.width=ed.offsetWidth+'px';
  band.style.display='block';
}

let shadow=null;
async function siteStyles(){
  shadow=preview.attachShadow({mode:'open'});
  let css='';
  try{
    css=await (await fetch('/files/web/src/styles/global.css')).text();
    css=css.replace(/^@import\s+['"][^'"]*['"];\s*$/gm,'')
           .replace(/:root:not\(([^)]+)\)/g,':host(:not($1))')
           .replace(/:root(\[[^\]]+\])/g,':host($1)')
           .replace(/:root/g,':host');
  }catch(e){ css=''; }
  shadow.innerHTML='<style>'
    +':host{display:block;background:var(--bg);color:var(--ink2);'
    +'padding:28px 34px 40vh;box-sizing:border-box;min-height:100%}'
    +'.prose{max-width:100%}'
    +css
    +'</style><div class="prose"></div>';
  return shadow.querySelector('.prose');
}
let proseEl=null;

function render(){
  const t=ed.value;
  const toks=marked.lexer(t);
  let line=1, html='';
  for(const tk of toks){
    const sub=[tk]; sub.links=toks.links;
    html+='<div class="blk" data-line="'+line+'">'+marked.parser(sub)+'</div>';
    line+=(tk.raw.match(/\n/g)||[]).length;
  }
  if(proseEl) proseEl.innerHTML=html; else preview.innerHTML=html;
  const calloutMap={finding:'is-finding',red:'is-finding',context:'is-context',blue:'is-context',
    caution:'is-caution',gold:'is-caution',verified:'is-verified',green:'is-verified',
    source:'is-source',teal:'is-source'};
  (proseEl||preview).querySelectorAll('blockquote').forEach(bq=>{
    const fp=bq.querySelector('p:first-child');
    if(!fp) return;
    const cm=fp.innerHTML.match(/^\[!(finding|red|context|blue|caution|gold|verified|green|source|teal)\]\s*/i);
    if(cm){
      bq.className=calloutMap[cm[1].toLowerCase()];
      fp.innerHTML=fp.innerHTML.slice(cm[0].length);
      if(!fp.innerHTML.trim()) fp.remove();
    }
  });
  const lines=t.split('\n');
  meta.textContent=lines.length+' lines · '
    +(t.trim()?t.trim().split(/\s+/).length:0)+' words';
  if(mode==='raw'){
    autosize();
    gutter(lines);
    curline();
  }
  (proseEl||preview).querySelectorAll('img').forEach(im=>{
    if(!im.complete) im.addEventListener('load',()=>{},{once:true});
  });
}
let rt=null;
window.addEventListener('resize',()=>{ clearTimeout(rt); rt=setTimeout(render,120); });

function lineOf(i){ return ed.value.slice(0,i).split('\n').length; }
function showPos(){
  const a=lineOf(ed.selectionStart), b=lineOf(ed.selectionEnd);
  pos.textContent = a===b ? 'L'+a : 'L'+a+'–'+b;
}
async function save(){
  dirty=false;
  const body=ed.value;
  const r=await fetch('/save?f='+encodeURIComponent(FILE),
                      {method:'POST',headers:{'Content-Type':'text/plain'},body});
  const j=await r.json(); known=j.mtime;
  dot.classList.add('hit'); setTimeout(()=>dot.classList.remove('hit'),500);
}
ed.addEventListener('input',()=>{
  dirty=true; render();
  clearTimeout(saveT); saveT=setTimeout(save,600);
});
ed.addEventListener('keyup',()=>{showPos();curline()});
ed.addEventListener('click',()=>{showPos();curline()});

/* ---- formatting helpers ---- */
function wrapSelection(before, after){
  const s=ed.selectionStart, e=ed.selectionEnd, t=ed.value;
  const sel=t.slice(s,e);
  ed.value=t.slice(0,s)+before+sel+after+t.slice(e);
  if(sel.length){
    ed.selectionStart=s; ed.selectionEnd=s+before.length+sel.length+after.length;
  } else {
    ed.selectionStart=ed.selectionEnd=s+before.length;
  }
  ed.focus(); dirty=true; render();
  clearTimeout(saveT); saveT=setTimeout(save,600);
}
function prefixLine(prefix){
  const s=ed.selectionStart, t=ed.value;
  const lineStart=t.lastIndexOf('\n',s-1)+1;
  ed.value=t.slice(0,lineStart)+prefix+t.slice(lineStart);
  ed.selectionStart=ed.selectionEnd=s+prefix.length;
  ed.focus(); dirty=true; render();
  clearTimeout(saveT); saveT=setTimeout(save,600);
}
function insertLine(text){
  const s=ed.selectionStart, t=ed.value;
  const lineStart=t.lastIndexOf('\n',s-1)+1;
  const before=t.slice(0,lineStart);
  const after=t.slice(lineStart);
  ed.value=before+text+'\n'+after;
  ed.selectionStart=ed.selectionEnd=lineStart+text.length+1;
  ed.focus(); dirty=true; render();
  clearTimeout(saveT); saveT=setTimeout(save,600);
}
function insertComment(){
  const s=ed.selectionStart, t=ed.value;
  const open='<!-- @c ', close=' -->';
  ed.value=t.slice(0,s)+open+close+t.slice(s);
  ed.selectionStart=ed.selectionEnd=s+open.length;
  ed.focus(); dirty=true; render();
  clearTimeout(saveT); saveT=setTimeout(save,600);
}

const actions={
  bold:    ()=>wrapSelection('**','**'),
  italic:  ()=>wrapSelection('*','*'),
  h1:      ()=>prefixLine('# '),
  h2:      ()=>prefixLine('## '),
  h3:      ()=>prefixLine('### '),
  h4:      ()=>prefixLine('#### '),
  link:    ()=>{
    const s=ed.selectionStart, e=ed.selectionEnd, t=ed.value;
    const sel=t.slice(s,e);
    if(sel.length){
      ed.value=t.slice(0,s)+'['+sel+'](url)'+t.slice(e);
      ed.selectionStart=s+sel.length+3;
      ed.selectionEnd=s+sel.length+6;
    } else {
      ed.value=t.slice(0,s)+'[text](url)'+t.slice(s);
      ed.selectionStart=s+1;
      ed.selectionEnd=s+5;
    }
    ed.focus(); dirty=true; render();
    clearTimeout(saveT); saveT=setTimeout(save,600);
  },
  code:    ()=>wrapSelection('`','`'),
  quote:   ()=>prefixLine('> '),
  'q-teal':  ()=>prefixLine('> [!source]\n> '),
  'q-blue':  ()=>prefixLine('> [!context]\n> '),
  'q-gold':  ()=>prefixLine('> [!caution]\n> '),
  'q-green': ()=>prefixLine('> [!verified]\n> '),
  ul:      ()=>prefixLine('- '),
  ol:      ()=>prefixLine('1. '),
  codeblock: ()=>{
    const s=ed.selectionStart, e=ed.selectionEnd, t=ed.value;
    const sel=t.slice(s,e);
    const block='\n```\n'+(sel||'')+(sel?'':'')+'\n```\n';
    ed.value=t.slice(0,s)+block+t.slice(e);
    ed.selectionStart=ed.selectionEnd=s+5+(sel?sel.length:0);
    ed.focus(); dirty=true; render();
    clearTimeout(saveT); saveT=setTimeout(save,600);
  },
  table: ()=>{
    const tpl='\n| Column 1 | Column 2 | Column 3 |\n| --- | --- | --- |\n| | | |\n';
    const s=ed.selectionStart, t=ed.value;
    ed.value=t.slice(0,s)+tpl+t.slice(s);
    ed.selectionStart=ed.selectionEnd=s+3;
    ed.focus(); dirty=true; render();
    clearTimeout(saveT); saveT=setTimeout(save,600);
  },
  caption: ()=>{
    const s=ed.selectionStart, t=ed.value;
    const tpl='\n![alt](url)\n*caption*\n';
    ed.value=t.slice(0,s)+tpl+t.slice(s);
    ed.selectionStart=s+3; ed.selectionEnd=s+6;
    ed.focus(); dirty=true; render();
    clearTimeout(saveT); saveT=setTimeout(save,600);
  },
  infobox: ()=>{
    const s=ed.selectionStart, t=ed.value;
    const tpl='\n<div class="info-box">\n\n### Label\n\n- Item\n- Item\n\n</div>\n';
    ed.value=t.slice(0,s)+tpl+t.slice(s);
    ed.selectionStart=s+26; ed.selectionEnd=s+31;
    ed.focus(); dirty=true; render();
    clearTimeout(saveT); saveT=setTimeout(save,600);
  },
  hr:      ()=>insertLine('---'),
  comment: ()=>insertComment(),
};

toolbar.addEventListener('click',e=>{
  const btn=e.target.closest('button[data-act]');
  if(!btn) return;
  const act=actions[btn.dataset.act];
  if(act) act();
});

ed.addEventListener('keydown',e=>{
  if((e.ctrlKey||e.metaKey) && e.key==='/'){
    e.preventDefault(); insertComment();
  }
  if((e.ctrlKey||e.metaKey) && e.key==='b'){
    e.preventDefault(); actions.bold();
  }
  if((e.ctrlKey||e.metaKey) && e.key==='i'){
    e.preventDefault(); actions.italic();
  }
  if((e.ctrlKey||e.metaKey) && e.key==='k'){
    e.preventDefault(); actions.link();
  }
  if((e.ctrlKey||e.metaKey) && e.key==='e'){
    e.preventDefault();
    document.getElementById('toggle').click();
  }
});

document.getElementById('ref').onclick=()=>{
  const lines=ed.value.split('\n');
  const a=lineOf(ed.selectionStart), b=lineOf(ed.selectionEnd);
  const out=[]; for(let i=a;i<=b;i++) out.push(i+': '+lines[i-1]);
  navigator.clipboard.writeText(out.join('\n'));
  pos.textContent='copied '+(a===b?'L'+a:'L'+a+'–'+b);
};

function load(txt,mt){ ed.value=txt; known=mt; dirty=false; render(); note.classList.add('hid'); }
note.onclick=()=>{ if(pending){ load(pending.text,pending.mtime); pending=null; } };
async function tick(){
  try{
    const s=await (await fetch('/state?f='+encodeURIComponent(FILE||'')
                               +'&t='+Date.now())).json();
    if(s.rel && s.rel!==FILE){ FILE=s.rel; }
    if(s.base){ document.querySelector('base').href=s.base; }
    if(s.rel){ document.title=s.rel.split('/').pop(); }
    dot.classList.remove('err');
    if(known===null){ load(s.text,s.mtime); return; }
    if(s.mtime!==known){
      if(dirty){ pending=s; note.classList.remove('hid'); }
      else{
        const y=editorPane.scrollTop, c=ed.selectionStart;
        load(s.text,s.mtime);
        editorPane.scrollTop=y;
        ed.selectionStart=ed.selectionEnd=Math.min(c,ed.value.length);
        dot.classList.add('hit'); setTimeout(()=>dot.classList.remove('hit'),700);
      }
    }
  }catch(e){ dot.classList.add('err'); }
}
FILE = new URLSearchParams(location.search).get('f') || null;
siteStyles().then(el=>{ proseEl=el; }).finally(()=>{
  loadListing().then(()=>{
    if(!FILE){ showHome(); return; }
    document.getElementById('pane').classList.remove('hid');
    setMode('raw');
    tick(); ticking=true; setInterval(tick,500);
  });
});
/* ---- theme toggle ---- */
const themeBtn=document.getElementById('theme');
const themes=['system','light','dark'];
let themeIdx=0;
const themeIcons={system:'☾',light:'☀',dark:'☽'};
themeBtn.onclick=()=>{
  themeIdx=(themeIdx+1)%3;
  const t=themes[themeIdx];
  if(t==='system') document.documentElement.removeAttribute('data-theme');
  else document.documentElement.setAttribute('data-theme',t);
  if(shadow){
    const host=shadow.host;
    if(t==='system') host.removeAttribute('data-theme');
    else host.setAttribute('data-theme',t);
  }
  themeBtn.textContent=themeIcons[t];
  themeBtn.title=t+' theme';
};
window.addEventListener('beforeunload',e=>{ if(dirty){ save(); } });
</script></body></html>"""


class H(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass

    def do_GET(self):
        p = urllib.parse.urlparse(self.path).path
        if p == "/":
            base = "/files/" + os.path.relpath(os.path.dirname(MD), ROOT) + "/"
            self._send((PAGE.replace("__BASE__", base)
                            .replace("__NAME__", os.path.basename(MD))).encode(),
                       "text/html; charset=utf-8")
        elif p == "/api/files":
            self._send(json.dumps({"files": listing(),
                                   "current": os.path.relpath(MD, ROOT)}).encode(),
                       "application/json")
        elif p == "/state":
            q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            target = resolve((q.get("f") or [""])[0])
            if not target:
                self._send(json.dumps({"mtime": 0, "text": "# no such file"}).encode(),
                           "application/json"); return
            try:
                st = os.stat(target)
                d = {"mtime": st.st_mtime,
                     "text": open(target, encoding="utf-8", errors="replace").read(),
                     "rel": os.path.relpath(target, ROOT),
                     "base": "/files/" + os.path.relpath(os.path.dirname(target), ROOT) + "/"}
            except OSError as e:
                d = {"mtime": 0, "text": f"# unreadable\n\n{e}"}
            self._send(json.dumps(d).encode(), "application/json")
        elif p.startswith("/files/"):
            rel = urllib.parse.unquote(p[len("/files/"):])
            full = os.path.normpath(os.path.join(ROOT, rel))
            if not full.startswith(ROOT) or not os.path.isfile(full):
                self.send_error(404); return
            self._send(open(full, "rb").read(),
                       mimetypes.guess_type(full)[0] or "application/octet-stream")
        else:
            self.send_error(404)

    def do_POST(self):
        u = urllib.parse.urlparse(self.path)
        if u.path != "/save":
            self.send_error(404); return
        q = urllib.parse.parse_qs(u.query)
        target = resolve((q.get("f") or [""])[0])
        if not target:
            self.send_error(404); return
        n = int(self.headers.get("Content-Length", 0))
        text = self.rfile.read(n).decode("utf-8")
        fd, tmp = tempfile.mkstemp(dir=os.path.dirname(target), prefix=".mdlive-")
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(text)
        os.replace(tmp, target)
        self._send(json.dumps({"mtime": os.stat(target).st_mtime}).encode(),
                   "application/json")

    def _send(self, body, ctype):
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)


class S(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


if __name__ == "__main__":
    print(f"mdlive2  file={MD}\n         root={ROOT}\n         http://localhost:{PORT}", flush=True)
    S(("0.0.0.0", PORT), H).serve_forever()
