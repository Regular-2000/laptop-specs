// ===== Shared CSV data loader for the laptop-specs pages =====
// Universal schema (same header for every manufacturer):
//   brand,series,model,year,col,size,cpu,gen,ram,slots,max,sold,w11,tag,
//   st_25sata,st_msata,st_m2sata,st_m2nvme,st_ide,st_emmc,st_m2len,st_note,os,note
//
//   brand  - "dell", "thinkpad", "hp", ...
//   series - tab/group key (ThinkPad: T/X/X1/L/E/P; HP: PB/E7/E8/U/Z; Dell: empty)
//   model  - display name; col - screen-size column (Dell grid: 15/14/13/12)
//   gen    - RAM generation key: sdr|ddr1|ddr2|ddr3|ddr4|ddr5 (drives chip colour)
//   sold   - 1 = soldered RAM;  w11 - 1 = Windows 11 eligible (empty = unknown/0)
//   tag    - short storage label shown on the chip face
//   Structured storage columns (0/blank = no, 1 = present, 2 = optional/config-dependent):
//     st_25sata  - 2.5″ SATA bay          st_msata  - mSATA slot
//     st_m2sata  - M.2 slot, SATA drives  st_m2nvme - M.2 slot, NVMe drives
//     st_ide     - IDE/PATA               st_emmc   - soldered eMMC
//     st_m2len   - M.2 length when NOT 2280 (2242/2230/22110); blank = 2280
//     st_note    - free-text storage oddities (1.8″ drives, WWAN-slot caveats, caddies)
//   os     - optional shipped-OS override; note - optional warning/footnote
//   pwr    - charger: connector family + typical shipped wattage (min-that-works
//            noted only where the gap bites, e.g. workstations / USB-C 45W nag)
//   bat    - battery serviceability: removable / internal / bridge (both)
//   bat_note - interchangeability family + one common part number for searching
//   bat_fam  - canonical battery family key (e.g. T54FJ, CC06, 45N1136). ONLY set when
//              interchangeability is verified — drives the "⇄ same battery" reverse
//              lookup, so empty = link doesn't render (safe). Filling a verified FRU
//              in bat_note? Fill bat_fam too (see BATTERY_HANDOFF.md).
//   url    - MANUAL override for the official spec-page link. Leave blank to use the
//            brand's automatic DuckDuckGo "\ bang" redirect (which finds the page
//            reliably); paste an exact URL here to pin a specific model precisely.
//   aliases- extra searchable model names (variants that share this row's platform,
//            e.g. "X1 Yoga Gen 3" on the X1 Carbon Gen 6 row). Not displayed on the chip.
//
// PROJECT GOAL: ~99% of legit model numbers should be findable via the page search in
// some shape or form (own row, grouped row, or alias) — without bloating the grid.
// A few exotic exceptions (e.g. X1 Fold) are acceptable. Compromise beats completeness.
//
// Add a laptop = add one CSV row. No code changes needed.

// Human-readable storage string composed from the structured columns.
export function genStor(d){
  const p=[]; const opt=v=>v===2?' (opt)':'';
  if(d.st_ide){ const l=(d.st_note||'').includes('1.8″')?'1.8″ IDE (PATA)':'2.5″ IDE (PATA)'; p.push(l+opt(d.st_ide)); }
  if(d.st_25sata) p.push('2.5″ SATA'+opt(d.st_25sata));
  if(d.st_msata) p.push('mSATA'+opt(d.st_msata));
  const len=d.st_m2len||'2280';
  if(d.st_m2sata&&d.st_m2nvme) p.push('M.2 '+len+' SATA/NVMe'+opt(Math.max(d.st_m2sata,d.st_m2nvme)));
  else if(d.st_m2sata) p.push('M.2 '+len+' SATA'+opt(d.st_m2sata));
  else if(d.st_m2nvme) p.push('M.2 '+len+' PCIe NVMe'+opt(d.st_m2nvme));
  if(d.st_emmc) p.push('eMMC'+opt(d.st_emmc));
  let s=p.join(' + ');
  if(d.st_note) s=s?s+' · '+d.st_note:d.st_note;
  return s||'—';
}

// Minimal RFC-4180 CSV parser (handles quoted fields, "" escapes, CR/LF).
export function parseCSV(text){
  const rows=[]; let row=[], field='', inQ=false;
  for(let i=0;i<text.length;i++){
    const c=text[i];
    if(inQ){
      if(c==='"'){ if(text[i+1]==='"'){field+='"';i++;} else inQ=false; }
      else field+=c;
    }else if(c==='"') inQ=true;
    else if(c===','){ row.push(field); field=''; }
    else if(c==='\n'||c==='\r'){
      if(c==='\r'&&text[i+1]==='\n') i++;
      row.push(field); field='';
      if(row.length>1||row[0]!=='') rows.push(row);
      row=[];
    }else field+=c;
  }
  if(field!==''||row.length){ row.push(field); if(row.length>1||row[0]!=='') rows.push(row); }
  return rows;
}

// ===== Compact view + report export (per brand, filter-aware) =====
// The "▤ report" button on each renderer calls showCompactList() with the models that
// pass the page's CURRENT filters (storage chips, RAM legend, Win11, search, ⇄ fam).
// It opens a dense read-only overlay — the whole answer on one screen instead of
// matches scattered across the year grid — with three actions:
//   ⬇ save report (.html)  → standalone light/print-friendly file, self-contained,
//                            titled by the active filters, one context line per chip
//                            (storage by default; battery/charger when a ⇄ fam filter
//                            is active — so it works for ANY filter type, not just storage)
//   ⧉ copy as text         → paste-ready plain text (eBay descriptions etc.)
//   ✕ close (Esc)
// loadAllBrands() (all three CSVs concatenated — identical 32-col schema) is kept
// exported for the future merged all-brands table; the overlay is per-brand by design.

const BRAND_FILES=[['thinkpad','ThinkPad · Lenovo / IBM','thinkpad.csv'],
                   ['dell','Dell','dell.csv'],
                   ['hp','HP','hp.csv']];
let _allBrands=null;
export async function loadAllBrands(){
  if(_allBrands) return _allBrands;
  const lists=await Promise.all(BRAND_FILES.map(b=>loadCSV(b[2]).catch(()=>[])));
  _allBrands=lists.flat();
  return _allBrands;
}

const ST_LABEL={bay25:'2.5″ SATA',ide:'2.5″ IDE (PATA)',msata:'mSATA',m2sata:'M.2 SATA',nvme:'M.2 NVMe',m2only:'SATA-only M.2'};
const ST_COL={bay25:'st_25sata',ide:'st_ide',msata:'st_msata',m2sata:'st_m2sata',nvme:'st_m2nvme',m2only:'st_m2sata'};
// gen palette duplicated here so the exported report is self-contained (no CSS vars)
const GENBG={sdr:'#8d6e63',ddr1:'#7d8799',ddr2:'#b07aa1',ddr3:'#4e79a7',ddr4:'#59a14f',ddr5:'#f28e2b'};

const stripTags=s=>String(s==null?'':s).replace(/<[^>]*>/g,'');
const shortOf=s=>{const t=String(s==null?'':s);const j=t.indexOf(String.fromCharCode(124,62));return j<0?t:t.slice(0,j);};
const escH=s=>String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
// context line shown under each model in the exported report (and in chip tooltips):
// battery / charger info when a ⇄ fam filter drove the query, storage otherwise
function ctxOf(d,kind){
  if(kind==='bat') return stripTags(shortOf(d.bat||''))+(d.bat_fam?' · '+d.bat_fam:'');
  if(kind==='pwr') return stripTags(shortOf(d.pwr||''));
  return stripTags(d.stor||'');
}

const CMP_CSS=`
#cmpOverlay{position:fixed;inset:0;z-index:100;background:var(--bg,#12151c);color:var(--text,#e8ebf2);overflow:auto;padding:14px 18px 40px}
#cmpOverlay .cmp-top{display:flex;flex-wrap:wrap;gap:10px;align-items:baseline;border-bottom:1px solid var(--line,#333b4d);padding-bottom:8px;margin-bottom:4px}
#cmpOverlay h2{margin:0;font-size:17px}
#cmpOverlay h2 small{color:var(--dim,#9aa3b5);font-weight:normal}
#cmpOverlay .cmp-b{cursor:pointer;user-select:none;font-size:12px;border:1px solid var(--line,#333b4d);border-radius:6px;padding:3px 10px;background:var(--panel,#1b1f2a);color:var(--dim,#9aa3b5)}
#cmpOverlay .cmp-b:hover{color:var(--text,#e8ebf2);border-color:var(--accent,#0096d6)}
#cmpOverlay .cmp-x{margin-left:auto}
#cmpOverlay .cmp-sub{width:100%;color:var(--dim,#9aa3b5);font-size:11.5px}
#cmpOverlay .cmp-yr{display:flex;gap:6px;align-items:baseline;padding:1px 0;border-bottom:1px solid #1e2430}
#cmpOverlay .cmp-y{flex:0 0 40px;font-size:11.5px;font-weight:bold;color:var(--dim,#9aa3b5)}
#cmpOverlay .cmp-chips{flex:1;display:flex;flex-wrap:wrap;gap:3px;padding:2px 0}
#cmpOverlay .cchip{font-size:12px;line-height:1.15;padding:2px 7px;border-radius:5px;border:1.5px solid transparent;cursor:default;white-space:nowrap}
#cmpOverlay .cchip.sdr{background:var(--sdr,#8d6e63)} #cmpOverlay .cchip.ddr1{background:var(--ddr1,#7d8799)}
#cmpOverlay .cchip.ddr2{background:var(--ddr2,#b07aa1)} #cmpOverlay .cchip.ddr3{background:var(--ddr3,#4e79a7)}
#cmpOverlay .cchip.ddr4{background:var(--ddr4,#59a14f)} #cmpOverlay .cchip.ddr5{background:var(--ddr5,#f28e2b);color:#1b1b1b}
#cmpOverlay .cchip.copt{border-color:rgba(255,255,255,.55);border-style:dashed}
#cmpOverlay .cmp-none{color:var(--dim,#9aa3b5);font-style:italic;font-size:12.5px;padding:6px 0}
#cmpOverlay .cmp-foot{margin-top:16px;color:var(--dim,#9aa3b5);font-size:11px;border-top:1px solid var(--line,#333b4d);padding-top:8px}
`;

// Standalone light-theme report document (self-contained: inline CSS, no scripts).
function buildReportHTML(o){
  const yrs=[...new Set(o.models.map(d=>d.y))].sort((a,b)=>b-a);
  const rows=yrs.map(yr=>{
    const chips=o.models.filter(d=>d.y===yr).map(d=>{
      const optional=o.single&&d[ST_COL[o.single]]===2;
      return '<span class="c" style="background:'+(GENBG[d.gen]||'#666')+
        (d.gen==='ddr5'?';color:#1b1b1b':'')+(optional?';border:1.5px dashed rgba(0,0,0,.45)':'')+'">'+
        '<b>'+escH(d.m)+(optional?' °':'')+'</b><small>'+escH((d.y?d.y+' · ':'')+ctxOf(d,o.ctxKind))+'</small></span>';
    }).join('');
    return '<div class="yr"><div class="y">'+(yr||'—')+'</div><div class="cc">'+chips+'</div></div>';
  }).join('\n');
  const optNote=o.single?' · ° / dashed = '+ST_LABEL[o.single]+' optional / config-dependent':'';
  return '<!DOCTYPE html>\n<html lang="en"><head><meta charset="UTF-8">'+
    '<meta name="viewport" content="width=device-width, initial-scale=1.0">'+
    '<title>'+escH(o.brandLabel+' — '+o.title)+'</title><style>'+
    'body{margin:0;font:14px/1.4 -apple-system,"Segoe UI",Roboto,Arial,sans-serif;background:#fff;color:#1a2433}'+
    '.hd{background:#0f2d52;color:#fff;padding:16px 26px}'+
    '.hd h1{margin:0;font-size:22px}.hd h1 span{color:#5dd0f0}'+
    '.hd .s{color:#c9dcea;font-size:12.5px;margin-top:4px}'+
    'main{padding:12px 22px}'+
    '.yr{display:flex;gap:10px;align-items:baseline;border-bottom:1px solid #e3e9f0;padding:3px 0}'+
    '.y{flex:0 0 44px;font-weight:bold;font-size:13px;color:#5b7185}'+
    '.cc{flex:1;display:flex;flex-wrap:wrap;gap:4px;padding:3px 0}'+
    '.c{display:inline-flex;flex-direction:column;color:#fff;border-radius:6px;padding:3px 9px;border:1.5px solid transparent}'+
    '.c b{font-size:13px;line-height:1.15}.c small{font-size:10px;opacity:.9;line-height:1.2;margin-top:1px}'+
    'footer{margin:14px 22px 20px;padding-top:8px;border-top:1px solid #e3e9f0;color:#5b7185;font-size:11.5px}'+
    '@media print{.hd{-webkit-print-color-adjust:exact;print-color-adjust:exact}.c{-webkit-print-color-adjust:exact;print-color-adjust:exact}}'+
    '</style></head><body>'+
    '<div class="hd"><h1>'+escH(o.brandLabel)+' — <span>'+escH(o.title)+'</span></h1>'+
    '<div class="s">'+o.models.length+' rows (a chip may group several models)'+
    (o.extras.length?' · filters: '+escH(o.extras.join(' · ')):'')+
    ' · generated '+o.date+' · '+escH(o.src)+'</div></div>'+
    '<main>\n'+rows+'\n</main>'+
    '<footer>Always verify the exact sub-model / configuration before buying'+optNote+
    '. Source: '+escH(o.src)+'</footer></body></html>';
}

// opts: { models, brandLabel, stOnKeys, allStOn, extras, ctxKind }
export function showCompactList(opts){
  const old=document.getElementById('cmpOverlay'); if(old) old.remove();
  if(!document.getElementById('cmpCSS')){
    const st=document.createElement('style'); st.id='cmpCSS'; st.textContent=CMP_CSS;
    document.head.appendChild(st);
  }
  // one storage filter lit → mark config-dependent (value 2) chips as "optional"
  const single=(!opts.allStOn&&opts.stOnKeys.length===1)?opts.stOnKeys[0]:null;
  const stTitle=opts.allStOn?'all storage types':(opts.stOnKeys.map(k=>ST_LABEL[k]).join(' + ')||'no storage filter (nothing lit)');
  const extras=(opts.extras||[]).filter(Boolean);
  const src=location.hostname+location.pathname;
  const date=new Date().toISOString().slice(0,10);

  const ov=document.createElement('div'); ov.id='cmpOverlay';
  const top=document.createElement('div'); top.className='cmp-top';
  const h2=document.createElement('h2');
  h2.innerHTML='▤ '+escH(opts.brandLabel)+' — '+escH(stTitle)+' <small>('+opts.models.length+' rows · a chip may group several models)</small>';
  top.appendChild(h2);
  const dl=document.createElement('span'); dl.className='cmp-b'; dl.textContent='⬇ save report (.html)'; top.appendChild(dl);
  const cp=document.createElement('span'); cp.className='cmp-b'; cp.textContent='⧉ copy as text'; top.appendChild(cp);
  const x=document.createElement('span'); x.className='cmp-b cmp-x'; x.textContent='✕ close (Esc)'; top.appendChild(x);
  const subBits=[];
  if(extras.length) subBits.push('Other active filters: '+extras.join(' · '));
  if(single) subBits.push('dashed chip = '+ST_LABEL[single]+' optional / config-dependent — verify exact config');
  if(subBits.length){
    const sub=document.createElement('div'); sub.className='cmp-sub';
    sub.textContent=subBits.join(' · '); top.appendChild(sub);
  }
  ov.appendChild(top);

  const txt=[opts.brandLabel+' — '+stTitle+(extras.length?' ('+extras.join(' · ')+')':'')];
  if(!opts.models.length){
    const n=document.createElement('div'); n.className='cmp-none'; n.textContent='no matches';
    ov.appendChild(n); txt.push('no matches');
  }
  const years=[...new Set(opts.models.map(d=>d.y))].sort((a,b)=>b-a);
  for(const yr of years){
    const line=document.createElement('div'); line.className='cmp-yr';
    const yc=document.createElement('div'); yc.className='cmp-y'; yc.textContent=yr||'—';
    line.appendChild(yc);
    const cc=document.createElement('div'); cc.className='cmp-chips';
    const names=[];
    for(const d of opts.models.filter(r=>r.y===yr)){
      const optional=single&&d[ST_COL[single]]===2;
      const ch=document.createElement('span');
      ch.className='cchip '+d.gen+(optional?' copt':'');
      ch.textContent=d.m+(optional?' °':'');
      ch.title=(d.series?d.series+' · ':'')+ctxOf(d,opts.ctxKind)+' · '+d.ram+' · max '+d.max+
        (optional?' · '+ST_LABEL[single]+' optional/config-dependent':'');
      cc.appendChild(ch);
      names.push(d.m+(optional?' (opt)':''));
    }
    line.appendChild(cc); ov.appendChild(line);
    txt.push('  '+(yr||'—')+': '+names.join(' · '));
  }
  const foot=document.createElement('div'); foot.className='cmp-foot';
  foot.textContent=(single?'° / dashed = slot optional or config-dependent — always verify the exact sub-model. ':'Always verify the exact sub-model. ')+'Source: '+src;
  ov.appendChild(foot);
  txt.push('','Always verify the exact sub-model/config. Source: '+src);

  dl.onclick=()=>{
    const html=buildReportHTML({models:opts.models,brandLabel:opts.brandLabel,title:stTitle,
      extras,single,ctxKind:opts.ctxKind,src,date});
    const slug=s=>s.toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/^-+|-+$/g,'').slice(0,50);
    const a=document.createElement('a');
    a.href=URL.createObjectURL(new Blob([html],{type:'text/html'}));
    a.download='report-'+slug(opts.brandLabel)+'-'+slug(stTitle)+'-'+date+'.html';
    a.click(); setTimeout(()=>URL.revokeObjectURL(a.href),5000);
    dl.textContent='✓ saved'; setTimeout(()=>dl.textContent='⬇ save report (.html)',1500);
  };
  cp.onclick=()=>{
    navigator.clipboard.writeText(txt.join('\n')).then(
      ()=>{cp.textContent='✓ copied'; setTimeout(()=>cp.textContent='⧉ copy as text',1500);},
      ()=>{cp.textContent='✗ copy failed'; setTimeout(()=>cp.textContent='⧉ copy as text',1500);});
  };
  const close=()=>{ov.remove();document.removeEventListener('keydown',esc);};
  const esc=e=>{if(e.key==='Escape')close();};
  x.onclick=close;
  document.addEventListener('keydown',esc);
  document.body.appendChild(ov);
}

// Load a CSV file and return an array of model objects using the short
// property names the renderers expect (m, y, col, gen, ram, ...).
export async function loadCSV(url){
  // no-cache = always revalidate against the server's ETag, so a CSV edit shows up on
  // the next normal refresh instead of being masked by a stale browser-cached copy
  // (cheap 304 when unchanged, fresh download only when the file actually changed).
  const res=await fetch(url,{cache:'no-cache'});
  if(!res.ok) throw new Error('Could not load '+url+' ('+res.status+')');
  const rows=parseCSV(await res.text());
  const head=rows.shift();
  const idx=Object.fromEntries(head.map((h,i)=>[h.trim(),i]));
  const get=(r,k)=>{const v=r[idx[k]];return v===undefined?'':v.trim();};
  return rows.map(r=>{
    const o={
      brand:get(r,'brand'), series:get(r,'series'),
      m:get(r,'model'), size:get(r,'size'), cpu:get(r,'cpu'), gen:get(r,'gen'),
      ram:get(r,'ram'), slots:get(r,'slots'), max:get(r,'max'),
      tag:get(r,'tag')
    };
    const y=get(r,'year'); if(y) o.y=+y;
    const col=get(r,'col'); if(col) o.col=+col;
    const sold=get(r,'sold'); if(sold) o.sold=+sold;
    const w11=get(r,'w11'); o.w11=w11?+w11:0;
    for(const k of ['st_25sata','st_msata','st_m2sata','st_m2nvme','st_ide','st_emmc']){
      const v=get(r,k); o[k]=v?+v:0;
    }
    o.st_m2len=get(r,'st_m2len');
    const sn=get(r,'st_note'); if(sn) o.st_note=sn;
    o.stor=genStor(o);
    const al=get(r,'aliases'); if(al) o.aliases=al;
    const pw=get(r,'pwr'); if(pw) o.pwr=pw;
    const bt=get(r,'bat'); if(bt) o.bat=bt;
    const bn=get(r,'bat_note'); if(bn) o.bat_note=bn;
    const bf=get(r,'bat_fam'); if(bf) o.bat_fam=bf;
    const ur=get(r,'url'); if(ur) o.url=ur;
    const pr=get(r,'price'); if(pr) o.price=pr;
    const pn=get(r,'price_note'); if(pn) o.price_note=pn;
    const os=get(r,'os'); if(os) o.os=os;
    const note=get(r,'note'); if(note) o.note=note;
    return o;
  });
}
