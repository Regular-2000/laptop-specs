// ===== Shared CSV data loader for the laptop-specs pages =====
// Universal schema (same header for every manufacturer):
//   brand,series,model,year,col,size,cpu,gen,ram,slots,max,sold,w11,tag,stor,os,note
//
//   brand  - "dell", "thinkpad", ("hp" later, ...)
//   series - tab/group key (ThinkPad: T/X/X1/L/E/P; Dell: empty)
//   model  - display name; col - screen-size column (Dell grid: 15/14/13/12)
//   gen    - RAM generation key: sdr|ddr1|ddr2|ddr3|ddr4|ddr5 (drives chip colour)
//   sold   - 1 = soldered RAM;  w11 - 1 = Windows 11 eligible (empty = unknown/0)
//   tag    - short storage label shown on the chip face; stor - full storage description
//   os     - optional shipped-OS override; note - optional warning/footnote
//
// Add a laptop = add one CSV row. No code changes needed.

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
      tag:get(r,'tag'), stor:get(r,'stor')
    };
    const y=get(r,'year'); if(y) o.y=+y;
    const col=get(r,'col'); if(col) o.col=+col;
    const sold=get(r,'sold'); if(sold) o.sold=+sold;
    const w11=get(r,'w11'); o.w11=w11?+w11:0;
    const os=get(r,'os'); if(os) o.os=os;
    const note=get(r,'note'); if(note) o.note=note;
    return o;
  });
}
