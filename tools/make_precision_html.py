#!/usr/bin/env python3
"""Generate precision.html from getac.html (same renderer, Dell Precision config block).

Re-run after fixing a renderer bug in getac.html / panasonic.html so all three stay in sync:
    python3 tools/make_precision_html.py
"""
import re, sys, pathlib

root = pathlib.Path(__file__).resolve().parent.parent
src = (root / 'getac.html').read_text(encoding='utf-8')
out = src

def sub(old, new, count=1, regex=False):
    global out
    if regex:
        out2, n = re.subn(old, new, out, count=count, flags=re.S)
    else:
        n = out.count(old) if count == 0 else min(out.count(old), count)
        out2 = out.replace(old, new) if count == 0 else out.replace(old, new, count)
    if n == 0:
        sys.exit('pattern not found: ' + old[:80])
    out = out2

# ---- head / header -------------------------------------------------------------------
sub('<title>Getac Rugged Timeline — RAM, Storage & Serial Reference</title>',
    '<title>Dell Precision Timeline — RAM, GPU, Screens & Storage Reference</title>')
sub('--accent:#0096d6', '--accent:#4ea1ff')
sub('#win11toggle,#rs232toggle,#rptoggle{', '#win11toggle,#rs232toggle,#rptoggle,#gputoggle{')
sub('#win11toggle.on,#rs232toggle.on,#rptoggle.on{', '#win11toggle.on,#rs232toggle.on,#rptoggle.on,#gputoggle.on{')
sub('.lg,.stf,#win11toggle,#rs232toggle,#rptoggle{', '.lg,.stf,#win11toggle,#rs232toggle,#rptoggle,#gputoggle{')
sub('  .row .v.rsu{', '  .gpul{font-size:12px;line-height:1.5}\n  .gpul b{color:#c3d2ff}\n  .row .v.rsu{')
sub('<h1>Getac <small>· rugged laptops, convertibles &amp; tablets · RAM, storage &amp; serial by year</small></h1>',
    '<h1>Dell Precision <small>· mobile workstations · RAM, GPU, screens &amp; storage by year</small></h1>')
sub('placeholder="Type model, e.g. B300 G7"', 'placeholder="Model or GPU, e.g. 7540 / rtx a2000"')
sub('<div id="rptoggle"', '<div id="gputoggle" title="Graphics. Click to cycle: any → removable graphics card (MXM / Dell module) → soldered discrete GPU → no discrete GPU offered (integrated only). Rows not verified yet are hidden while this is on.">🎮 GPU: any</div>\n    <div id="rptoggle"')
sub('<span class="hint">⊶ = serial port · ⊶° = serial optional · grey = RAM type unverified · 🔒 = soldered · search: "-word" excludes · "portnone" = confirmed no serial</span>',
    '<span class="hint">▣ = removable graphics card (MXM / Dell module) · 🔒 = soldered RAM · grey = not verified yet · search: words AND-ed, "-word" excludes · try "rtx a2000", "mxm", "uma-only", "uhd", "oled", "touch"</span>')
sub('<div class="laddercap">⊶ serial is shown on the chip · <span style="text-transform:none;letter-spacing:0">hover a tab for who it\'s for · blank = not verified yet, never a guess</span></div>',
    '<div class="laddercap">tabs = product line, oldest M-series → 2025 Pro Max · <span style="text-transform:none;letter-spacing:0">hover a tab for what it descends from · GPU and screen options are in the detail panel · blank = not verified yet, never a guess</span></div>')
sub(re.compile(r'<footer>Getac rugged lineup.*?</footer>', re.S).search(out).group(0),
    '<footer>Dell Precision mobile workstations ~2001 → 2026 (M-series → 3000 / 5000 / 7000 → 2025 Dell Pro Max → 2026 Dell Pro Precision). '
    'Specs from Dell\'s own Setup &amp; Specifications guides, Owner\'s / Service manuals and User\'s Guides (dell.com/support) — each panel row cites its source behind ⓘ. '
    '<b>Graphics:</b> the option list is what Dell sold on that model; ▣ = the GPU is a removable card (MXM type-A/B on M4800 → 7540, Dell\'s own module on 7550 → 7770; upgrade / repair possible — check the heatsink and BIOS support), '
    'soldered = on the board for life. <b>Screens:</b> every panel Dell offered; the panel actually fitted varies unit to unit — check the listing photos / service-tag config. '
    'No prices yet (needs a live sold-comps pull).</footer>')

# ---- data / config block -------------------------------------------------------------
sub('// ===== Data lives in getac.csv', '// ===== Data lives in precision.csv')
sub("const ALL=await loadCSV('getac.csv');", "const ALL=await loadCSV('precision.csv');")
sub(re.compile(r'const YEAROS=\{.*?\};').search(out).group(0),
    'const YEAROS={"2001":"Windows 2000 / XP Pro","2002":"Windows XP Pro","2003":"Windows XP Pro","2004":"Windows XP Pro","2005":"Windows XP Pro","2006":"Windows XP Pro","2007":"Windows XP / Vista Business","2008":"Windows XP / Vista Business","2009":"Windows XP / Vista / 7","2010":"Windows 7 Pro","2011":"Windows 7 Pro","2012":"Windows 7 Pro","2013":"Windows 7 / 8 Pro","2014":"Windows 7 / 8.1 Pro","2015":"Windows 7 / 10 Pro","2016":"Windows 10 Pro (Win 7 option)","2017":"Windows 10 Pro","2018":"Windows 10 Pro","2019":"Windows 10 Pro","2020":"Windows 10 Pro","2021":"Windows 10 / 11 Pro","2022":"Windows 11 Pro","2023":"Windows 11 Pro","2024":"Windows 11 Pro","2025":"Windows 11 Pro","2026":"Windows 11 Pro"};')
meta = '''const META={
"E": {
"label": "3000 · Latitude-based",
"note": "The entry workstation built on a Latitude chassis: M20 (D610) → M2300 (D630) → M2400 (E6400) → M2800 (E6540) → 3510 … 3591, plus the 14″ 3470/3480/3490 → 2025 Dell Pro Max 14/16. Usually a modest NVIDIA/AMD workstation chip or integrated graphics. From 3541 on the xx1 models are the H-series twins of the Latitude 5xx1."
},
"S": {
"label": "5000 · thin (XPS-based)",
"note": "The thin-and-light line on the XPS 15/17 chassis: M3800 → 5510 → 5520 → 5530 (+ 2-in-1) → 5540 → 5550/5750 → 5560/5760 → 5570/5770 → 5680 → 5690, plus the 14″ 5470/5480/5490 → 2025 Dell Pro Max 14/16 Premium. Soldered GPU, mostly 4K/OLED/touch panel options."
},
"W": {
"label": "7000 · 15–16″",
"note": "The full mobile workstation, 15.4–16″: M60 → M70 → M65 → M4300 → M4400 → M4500 → M4600 → M4700 → M4800 → 7510 … 7560 → 7670 → 7680 → 2025 Dell Pro Max 16 Plus. Highest-end GPUs, 4 RAM slots on most, ECC on Xeon. MXM graphics through 7540 — check the panel for each model."
},
"X": {
"label": "7000 · 17–18″",
"note": "The 17″ flagship: M90 → M6300 → M6400 → M6500 → M6600 → M6700 → M6800 → 7710 … 7760 → 7770 → 7780 → 2025 Dell Pro Max 18 Plus. Same platform as the 15″ sibling with the biggest GPUs, more drive bays and the heaviest chargers."
}
};'''
sub(re.compile(r'const META=\{.*?\n\};', re.S).search(out).group(0), meta)
sub('let curSeries=dq?"ALL":"F"', 'let curSeries=dq?"ALL":"W"')
sub(re.compile(r'const order=\[.*?\];\nconst TIER=\{.*?\};\nconst POS =\{.*?\};', re.S).search(out).group(0),
    'const order=["E", "S", "W", "X"];\nconst TIER={"E": "③", "S": "⑤", "W": "⑦", "X": "⑰"};\n'
    'const POS ={"E": "Entry workstation on a Latitude chassis — cheapest, lightest GPU", "S": "Thin workstation on the XPS chassis — 4K/OLED screens, soldered GPU", "W": "Full 15–16″ mobile workstation — biggest GPUs, ECC, 4 RAM slots", "X": "17–18″ flagship — biggest GPUs and screens, heaviest chargers"};')

# search haystack: + GPU / screen text + status tokens
sub("(d.w11?' win11':' no-win11')+(d.sold?' soldered':'')).toLowerCase();}",
    "(d.w11?' win11':' no-win11')+(d.sold?' soldered':'')+' '+sh(d.gpu)+' '+sh(d.scr)+"
    "(d.gpu_mxm===1?' mxm removable-gpu':d.gpu_mxm===0?' soldered-gpu':'')+(UMAONLY(d)?' uma-only':'')).toLowerCase();}\n"
    "function UMAONLY(d){return !!d.gpu&&/^UMA only/i.test(d.gpu);}")
# chip face: ▣ for MXM
sub("const rsm=d.rs232===1?'⊶ ':d.rs232===2?'⊶° ':d.rs232===0?'':'';",
    "const rsm=(d.gpu_mxm===1?'▣ ':'')+(d.rs232===1?'⊶ ':d.rs232===2?'⊶° ':'');")
sub("const WIN11Y=2019;", "const WIN11Y=2018;")
sub("lr.innerHTML='<td colspan=\"'+span+'\">▲ 2019+ all Windows 11 eligible · 2017–2018 mixed (8th gen yes, 7th gen no — check the chip) · ▼ older = not eligible</td>';",
    "lr.innerHTML='<td colspan=\"'+span+'\">▲ 2018+ (8th gen Core / Xeon E-2100) Windows 11 eligible · ▼ 2017 and older not eligible (7th gen / Xeon E3 v6 are off Microsoft\\'s list)</td>';")

# links: Dell support page (url column) with a search fallback
sub(re.compile(r'// Getac: no stable spec-page URLs.*?function tpProduct\(nm\)\{\n  return .*?;\n\}', re.S).search(out).group(0),
    "// Dell: the url column pins the model's dell.com/support page (Manuals & Documents → Setup & Specifications).\n"
    "function tpProduct(nm){\n  return 'https://www.dell.com/support/search/en-us#q='+encodeURIComponent('Precision '+nm)+'&sort=relevancy&f:langFilter=[en]';\n}")
sub(re.compile(r'function CHG\(s\)\{.*?\n', re.S).search(out).group(0),
    "function CHG(s){const M=[[/7\\.4mm barrel/i,'img/chg-dell74.svg'],[/legacy dell barrel/i,'img/chg-legacy-barrel.svg'],[/usb-c/i,'img/chg-usbc.svg']];const j0=s.indexOf(String.fromCharCode(124,62));const sh0=j0<0?s:s.slice(0,j0);const hit=M.find(p=>p[0].test(sh0));if(!hit)return DEEP(s);const im=hit[1];const sh=j0<0?s:s.slice(0,j0);const dp=j0<0?'':s.slice(j0+2);return DEEP(sh+' <img class=\"chgThumb\" src=\"'+im+'\" alt=\"connector\">'+String.fromCharCode(124,62)+'<img class=\"chgBig\" src=\"'+im+'\" alt=\"connector\"> '+dp);}\n")
sub("const PWRFAMS=[[/7\\.4mm HP barrel/i,'7.4mm HP smart-pin'],[/4\\.5mm blue tip/i,'4.5mm blue tip'],[/usb-c/i,'USB-C']];",
    "const PWRFAMS=[[/7\\.4mm barrel/i,'7.4mm barrel'],[/4\\.5mm small barrel/i,'Dell 4.5mm small barrel'],[/legacy dell barrel/i,'legacy Dell barrel'],[/usb-c/i,'USB-C']];")
sub("const q=encodeURIComponent('Getac '+nm);", "const q=encodeURIComponent('Dell Precision '+nm+' laptop');")
sub("' · Getac '+SERIES[sk].label+", "' · Dell Precision '+SERIES[sk].label+")
sub("(d.url?'Official Getac spec page:':'Look up the Getac spec sheet'+(models.length>1?' (per model)':'')+':')",
    "(d.url?'Dell support page (manuals, specs, drivers):':'Search Dell support'+(models.length>1?' (per model)':'')+':')")
sub("brandLabel:'Getac rugged'", "brandLabel:'Dell Precision'")

# detail panel: graphics + screens rows after Storage / likely config
GPU_ROWS = ("    (d.gpu?'<div class=\"row\"><div class=\"k\">🎮 Graphics options</div><div class=\"v gpul\">'+DEEP(d.gpu+(d.gpu_note?' '+String.fromCharCode(124,62)+' '+d.gpu_note:''))+'</div></div>':'<div class=\"row\"><div class=\"k\">🎮 Graphics options</div><div class=\"v rsu\">Not verified yet</div></div>')+\n"
            "    '<div class=\"row\"><div class=\"k\">▣ GPU module</div><div class=\"v'+(d.gpu_mxm===undefined?' rsu':'')+'\">'+(d.gpu_mxm===1?'Removable card (MXM or Dell module) — not soldered':d.gpu_mxm===0?'Soldered to the motherboard':d.gpu_mxm===2?'Depends on config — see note':UMAONLY(d)?'— (no discrete GPU offered)':'Unverified')+(d.gpu_mxm_note?' · '+DEEP(d.gpu_mxm_note):'')+'</div></div>'+\n"
            "    (d.gpu_typ?'<div class=\"row\"><div class=\"k\">🎮 Likely GPU (random unit)</div><div class=\"v\">'+DEEP(d.gpu_typ+(d.gpu_typ_note?' '+String.fromCharCode(124,62)+' '+d.gpu_typ_note:''))+'</div></div>':'')+\n"
            "    (d.scr?'<div class=\"row\"><div class=\"k\">🖥 Screen options</div><div class=\"v gpul\">'+DEEP(d.scr+(d.scr_note?' '+String.fromCharCode(124,62)+' '+d.scr_note:''))+'</div></div>':'<div class=\"row\"><div class=\"k\">🖥 Screen options</div><div class=\"v rsu\">Not verified yet</div></div>')+\n")
sub("    (d.typ?'<div class=\"row\"><div class=\"k\">📦 Likely config (random unit)</div>",
    GPU_ROWS + "    (d.typ?'<div class=\"row\"><div class=\"k\">📦 Likely config (random unit)</div>")

# GPU filter toggle
sub("const RSMODES=", "let gpuMode=0;\nconst GPUMODES=['🎮 GPU: any','🎮 GPU: ▣ removable card','🎮 GPU: soldered dGPU','🎮 GPU: integrated only'];\n"
    "function gpuPass(d){if(!gpuMode)return true;if(gpuMode===1)return d.gpu_mxm===1;if(gpuMode===2)return d.gpu_mxm===0;return UMAONLY(d);}\nconst RSMODES=")
sub("function rsPass(d){if(!rsMode)return true;", "function rsPass(d){if(!gpuPass(d))return false;if(!rsMode)return true;")
sub("if(rpMax) extras.push('CPU re-paste level ≤'+rpMax);",
    "if(rpMax) extras.push('CPU re-paste level ≤'+rpMax);\n    if(gpuMode) extras.push(GPUMODES[gpuMode].replace('🎮 ',''));")
sub("const rt=document.getElementById('rs232toggle');",
    "const gt=document.getElementById('gputoggle');\ngt.onclick=()=>{gpuMode=(gpuMode+1)%4;gt.textContent=GPUMODES[gpuMode];gt.classList.toggle('on',gpuMode>0);apply();};\nconst rt=document.getElementById('rs232toggle');")
sub('rpMax=0;syncRp();', 'rpMax=0;syncRp();gpuMode=0;var _g=document.getElementById("gputoggle");if(_g){_g.classList.remove("on");_g.textContent=GPUMODES[0];}')


# ---- mixed RAM generation (gen = "ddr4/ddr5": Dell sells both builds under one model) ----
sub("  .chip.unk{", "  .chip.mixg{color:#fff;text-shadow:0 1px 2px rgba(0,0,0,.6)}\n  .chip.unk{")
sub("ch.className='chip '+d.gen+(d.sold?' soldered':'');",
    "const GS=d.gen.split('/');\n  ch.className='chip '+(GS.length>1?'mixg':d.gen)+(d.sold?' soldered':'');\n"
    "  if(GS.length>1) ch.style.background='linear-gradient(135deg,var(--'+GS[0]+') 0 50%,var(--'+GS[1]+') 50% 100%)';")
sub("(d.gen==='unk'?'RAM ?':d.ram.split(' ')[0].replace(';',''))",
    "(d.gen==='unk'?'RAM ?':GS.length>1?GS.map(g=>g.toUpperCase()).join('/'):d.ram.split(' ')[0].replace(';',''))")
sub("'+GENLABEL[d.gen]+'", "'+d.gen.split('/').map(g=>GENLABEL[g]).join(' <b>or</b> ')+(d.gen.includes('/')?' — Dell sells both builds under this model; check the sticks / label on the unit':'')+'")
sub("models:all.filter(d=>!genOff.has(d.gen)&&", "models:all.filter(d=>genVis(d)&&")
sub("const genOk=!genOff.has(d.gen);", "const genOk=genVis(d);")
sub("function rsPass(d){", "function genVis(d){return d.gen.split('/').some(g=>!genOff.has(g));}\nfunction rsPass(d){")

# Toughbook part-number matcher is not needed (harmless) — leave it.
assert 'Getac' not in out.split('<script')[0] or True
left = [l for l in out.splitlines() if 'Getac' in l]
if left:
    print('WARNING lines still mentioning Getac:', *left[:5], sep='\n  ')
(root / 'precision.html').write_text(out, encoding='utf-8')
print('wrote precision.html', len(out))
