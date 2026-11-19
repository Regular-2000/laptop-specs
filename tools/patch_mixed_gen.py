#!/usr/bin/env python3
"""One-off (2026-11-19): teach the five hand-written renderers about two-generation rows.

gen = "ddr4/ddr5" (older generation first) means the model is sold with either RAM type.
The chip is split diagonally into both legend colours, the chip face says DDR4/DDR5,
the panel lists both, and the legend hides the chip only when BOTH colours are off.
precision.html inherits all of this from getac.html via tools/make_precision_html.py.
Idempotent: skips a page that already has genVis().
"""
import re, sys, pathlib
root = pathlib.Path(__file__).resolve().parent.parent

CSS = ("  .chip.mixg{color:#fff;text-shadow:0 1px 2px rgba(0,0,0,.65)}\n"
       "  .mixsw{display:inline-block;width:22px;height:11px;border-radius:3px;vertical-align:-1px;"
       "background:linear-gradient(135deg,var(--ddr4) 0 50%,var(--ddr5) 50% 100%)}\n")
HINT = ' · <span class="mixsw"></span> split colour = sold with two RAM generations'

for name in ['dell.html', 'thinkpad.html', 'hp.html', 'getac.html', 'panasonic.html']:
    p = root / name
    s = p.read_text(encoding='utf-8')
    if 'function genVis(' in s:
        print('skip', name); continue
    def rep(old, new, count=1):
        global s
        n = s.count(old)
        if n < count or n == 0:
            sys.exit(f'{name}: pattern not found: {old[:70]}')
        s = s.replace(old, new)
    rep('</style>', CSS + '</style>')
    # hint swatch: end of the first .hint span
    i = s.index('<span class="hint">'); j = s.index('</span>', i)
    s = s[:j] + HINT + s[j:]
    rep("ch.className='chip '+d.gen+(d.sold?' soldered':'');",
        "const GS=String(d.gen).split('/');\n"
        "  ch.className='chip '+(GS.length>1?'mixg':d.gen)+(d.sold?' soldered':'');\n"
        "  if(GS.length>1) ch.style.background='linear-gradient(135deg,var(--'+GS[0]+') 0 50%,var(--'+GS[1]+') 50% 100%)';")
    if "d.ram.split(' ')[0].replace(';','')" in s:
        rep("d.ram.split(' ')[0].replace(';','')",
            "(GS.length>1?GS.map(g=>g.toUpperCase()).join('/'):d.ram.split(' ')[0].replace(';',''))")
    rep("'+GENLABEL[d.gen]+'",
        "'+String(d.gen).split('/').map(g=>GENLABEL[g]).join(' <b>or</b> ')+(String(d.gen).includes('/')?' — this model was sold with either; check the sticks / label on the unit':'')+'")
    s = s.replace("!genOff.has(d.gen)", "genVis(d)")
    rep("function apply(", "function genVis(d){return String(d.gen).split('/').some(g=>!genOff.has(g));}\nfunction apply(")
    p.write_text(s, encoding='utf-8')
    print('patched', name, s.count('genVis('))

# shared loader: compact overlay + saved report draw the split too
sp = root / 'specdata.js'
s = sp.read_text(encoding='utf-8')
if 'mixBg(' not in s:
    s = s.replace("const stripTags=",
        "// two-generation rows (gen = \"ddr4/ddr5\"): diagonal split of both palette colours\n"
        "const mixBg=g=>{const a=String(g).split('/');return a.length>1?'linear-gradient(135deg,'+(GENBG[a[0]]||'#666')+' 0 50%,'+(GENBG[a[1]]||'#666')+' 50% 100%)':null;};\n"
        "const stripTags=", 1)
    s = s.replace("(GENBG[d.gen]||GENBG[String(d.gen).split('/')[0]]||'#666')", "(mixBg(d.gen)||GENBG[d.gen]||'#666')")
    s = s.replace("(d.gen==='ddr5'?';color:#1b1b1b':'')", "(d.gen==='ddr5'?';color:#1b1b1b':mixBg(d.gen)?';color:#fff;text-shadow:0 1px 2px rgba(0,0,0,.6)':'')")
    old = "ch.className='cchip '+d.gen+(optional?' copt':'');"
    assert old in s, 'cchip pattern'
    s = s.replace(old, old + "\n      if(mixBg(d.gen)){ch.style.background=mixBg(d.gen);ch.style.color='#fff';}")
    sp.write_text(s, encoding='utf-8')
    print('patched specdata.js')
