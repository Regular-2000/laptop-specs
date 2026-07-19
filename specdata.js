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

// Load a CSV file and return an array of model objects using the short
// property names the renderers expect (m, y, col, gen, ram, ...).
export async function loadCSV(url){
  const res=await fetch(url);
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
    const os=get(r,'os'); if(os) o.os=os;
    const note=get(r,'note'); if(note) o.note=note;
    return o;
  });
}
