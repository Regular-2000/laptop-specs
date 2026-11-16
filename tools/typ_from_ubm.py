#!/usr/bin/env python3
"""Rebuild the `typ` / `typ_note` columns ("typical RAM + SSD config as found") from the
raw UserBenchmark pulls.  Run from the Laptop_diagram folder:

    python3 tools/typ_from_ubm.py            # dry run: prints what each row would get
    python3 tools/typ_from_ubm.py --write    # writes dell/thinkpad/hp.csv + appends ubm_stats.csv

Inputs (never edited by this script):
    ubm_raw/*.jsonl        one line per system page pull: {date,u,sys,n,rows:[...]}
                           row = "COMP|name|brand|count|ubm_component_id"  (count = PCs of this model seen with that part)
    ubm_raw/system_map.csv ubm_id,brand,model,label   (model = exact `model` cell of the brand CSV;
                           label = plain name for Lenovo MTM pages)

Everything about HOW the raw rows are grouped lives in this file (size buckets, the 60 %
"dominant" rule, NVMe/SATA guess) - change it here and re-run to regroup; no re-pull needed.
"""
import csv, glob, io, json, os, re, sys, collections

MIN_PCS = 50             # fewer PCs than this on the system page -> row left blank (raw is still kept)
DOMINANT = 0.60          # one size is "the" typical config if it holds >= 60 % of the top-5 counts
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
num = lambda s: int(re.sub(r'[^\d]', '', s) or 0)

def load_raw():
    best = {}
    for f in sorted(glob.glob(os.path.join(ROOT, 'ubm_raw', '*.jsonl'))):
        for ln in open(f, encoding='utf-8'):
            ln = ln.strip()
            if not ln: continue
            d = json.loads(ln)
            sid = d['u'].rstrip('/').split('/')[-1]
            d['id'] = sid
            d['rows'] = [r.split('|') for r in d['rows']]
            if sid not in best or d['date'] >= best[sid]['date']:
                best[sid] = d            # newest pull of a system wins
    return best

def ram_of(name):
    m = re.search(r'(\d+)x(\d+)GB', name)
    if m:
        k, g = int(m.group(1)), int(m.group(2))
        return k * g, '%d×%d' % (k, g), k
    m = re.search(r'(\d+)GB', name)
    return (int(m.group(1)), 'mixed', 0) if m else (0, '', 0)

def cap_of(name):
    # capacity = a stand-alone "256GB" / "1TB" token (NOT the "256TB" inside part numbers like MTFDDAV256TBN)
    ms = re.findall(r'(?<![A-Za-z0-9.])(\d+(?:\.\d+)?)\s?(TB|GB)\b', name)
    g = float(ms[-1][0]) * (1000 if ms[-1][1] == 'TB' else 1) if ms else None
    if g is None: return None
    for lo, hi, lab in [(0, 70, '≤64 GB'), (100, 135, '128 GB'), (170, 200, '180 GB'), (230, 260, '256 GB'),
                        (350, 410, '360–400 GB'), (460, 530, '512 GB'), (900, 1100, '1 TB'), (1800, 2200, '2 TB'),
                        (3600, 4400, '4 TB')]:
        if lo <= g <= hi: return lab
    return '%g GB' % g

NVME = re.compile(r'nvme|pcie|MTFDHBA|SSDPE[KM]|HF[MS]\d+G[DE]|LENSE\d+\w*MSP|TS\w+MTE|\bMZVL|\bMZVK|KXG|KBG|\bPM9[0-9A-Z]|\bPC ?SN|\bSN[5-8]\d\d|BC[57]\d\d|\bPC[4-8]\d\d|2200S|\b2[2-5]\d0\b|\b3[4-5]\d0\b|XG[5-8]|\bP[34]\d{4}|OM3PDP|IM2P|970|980|990', re.I)
SATA = re.compile(r'sata|MTFDDA[VK]|SSDSC|PM8[5-8]\d|CM871|\bKSG|\bMZNL|\bMZ7|\bSC3\d\d|\b1[13]00\b|X[346]00|MX[35]00|BX500|A400|8[4-7]0 ?(?:evo|pro|qvo)|mSATA|2\.5', re.I)
def bus_of(name, brand):
    t = name + ' ' + brand
    if NVME.search(t) and not re.search(r'sata', t, re.I): return 'NVMe'
    if SATA.search(t): return 'SATA'
    return ''

def pct(c, tot): return '%d%%' % round(100.0 * c / tot) if tot else '0%'
gsort = lambda lab: float(re.sub(r'[^\d.]', '', lab.split('–')[0]) or 0) * (1000 if 'TB' in lab else 1)

def derive(d, soldered):
    n = num(d['n'])
    ram = collections.OrderedDict(); ssd = collections.Counter(); bus = collections.Counter()
    hdd = 0; ramtot = 0; ssdtot = 0
    for comp, name, brand, cnt, cid in d['rows']:
        c = num(cnt)
        if comp == 'RAM':
            g, cfg, sticks = ram_of(name)
            if not g: continue
            ram.setdefault(g, collections.Counter())[cfg] += c; ramtot += c
        elif comp == 'SSD':
            lab = cap_of(name)
            if not lab: continue
            ssd[lab] += c; ssdtot += c
            b = bus_of(name, brand)
            if b: bus[b] += c
        elif comp == 'HDD': hdd += c
    if not ramtot and not ssdtot: return None, None
    # ---- RAM
    rt = sorted(((sum(v.values()), g) for g, v in ram.items()), reverse=True)
    def rlab(g):
        cfg = ram[g].most_common(1)[0][0]
        if soldered or cfg == 'mixed' or int(cfg.split('×')[0]) >= 4: return '%d GB' % g
        return '%d GB (%s)' % (g, cfg)
    if rt:
        pick = [rt[0][1]] if (rt[0][0] >= DOMINANT * ramtot or len(rt) == 1) else sorted([rt[0][1], rt[1][1]])
        rs = ' / '.join(rlab(g) for g in pick) + (' soldered' if soldered else '')
    else: rs = ''
    # ---- SSD
    st = ssd.most_common()
    if st:
        pick = [st[0][0]] if (st[0][1] >= DOMINANT * ssdtot or len(st) == 1) else sorted([st[0][0], st[1][0]], key=gsort)
        bt = sum(bus.values())
        b = 'SSD'
        if bt >= 0.5 * ssdtot:
            top, tc = bus.most_common(1)[0]
            b = top if tc >= 0.75 * bt else 'SSD (NVMe + SATA mix)'
        if len(pick) == 2 and pick[0].endswith(' GB') and pick[1].endswith(' GB'):
            ss = pick[0][:-3] + ' / ' + pick[1] + ' ' + b
        else: ss = ' / '.join(pick) + ' ' + b
    else: ss = ''
    typ = ' · '.join(x for x in (rs, ss) if x)
    # ---- evidence
    name = d['sys'].replace('System / ', '') + (' (%s)' % d['label'] if d.get('label') else '')
    ev = ['UserBenchmark · %s · %s PCs%s · pulled %s.' % (name, d['n'] or '?', ' — small sample' if n < 200 else '', d['date'])]
    if rt:
        parts = []
        for c, g in sorted(rt, key=lambda x: x[1]):
            cf = ', '.join('%s %s' % (k, pct(v, ramtot)) for k, v in ram[g].most_common()) if len(ram[g]) > 1 else ram[g].most_common(1)[0][0]
            parts.append('%d GB %s (%s)' % (g, pct(c, ramtot), cf))
        ev.append('RAM — ' + ' · '.join(parts) + (' [top-5 parts = %s of PCs]' % pct(ramtot, n) if n else '') + '.')
    if st:
        ev.append('SSD — ' + ' · '.join('%s %s' % (k, pct(v, ssdtot)) for k, v in sorted(st, key=lambda x: gsort(x[0]))) +
                  (' [top-5 parts = %s of PCs]' % pct(ssdtot, n) if n else '') + '.')
    if hdd and hdd >= 0.15 * max(ssdtot, 1): ev.append('HDD also seen (%d units in top-5).' % hdd)
    ev.append('As found on benchmarked machines — owner upgrades included, so not the factory config; shares are within the visible top-5 parts only.')
    return typ, ' '.join(ev)

def main():
    write = '--write' in sys.argv
    raw = load_raw()
    smap = list(csv.DictReader(open(os.path.join(ROOT, 'ubm_raw', 'system_map.csv'), encoding='utf-8')))
    by = collections.defaultdict(list)
    for m in smap:
        if m['ubm_id'] in raw:
            raw[m['ubm_id']]['label'] = m.get('label', '')
            by[(m['brand'], m['model'])].append(raw[m['ubm_id']])
        else: print('!! mapped but no raw pull:', m)
    unm = set(raw) - {m['ubm_id'] for m in smap}
    if unm: print('!! raw pulls with no row mapping:', sorted(unm))
    filled = 0
    for brand in ('dell', 'thinkpad', 'hp'):
        p = os.path.join(ROOT, brand + '.csv')
        rows = list(csv.reader(io.StringIO(open(p, encoding='utf-8', newline='').read())))
        H = rows[0]; iT, iN, iM, iS = H.index('typ'), H.index('typ_note'), H.index('model'), H.index('sold')
        seen = set()
        for r in rows[1:]:
            ds = by.get((brand, r[iM]))
            if not ds: continue
            seen.add(r[iM])
            d = max(ds, key=lambda x: num(x['n']))
            if num(d['n']) < MIN_PCS:
                print('   (only %s PCs - left blank) %s %s' % (d['n'], brand, r[iM])); r[iT], r[iN] = '', ''; continue
            typ, note = derive(d, r[iS] == '1')
            if not typ: print('   (no RAM/SSD data)', brand, r[iM]); continue
            others = [x['sys'].replace('System / ', '') for x in ds if x is not d]
            if '/' in r[iM]: note = note.replace(' · pulled', ' (this one system stands in for the whole row) · pulled', 1)
            if others: note += ' Other pulls for this row: ' + ', '.join(others) + '.'
            r[iT], r[iN] = typ, note; filled += 1
            print('%-9s %-34s %s' % (brand, r[iM][:34], typ))
        for k in by:
            if k[0] == brand and k[1] not in seen: print('!! no CSV row named', k)
        if write:
            out = io.StringIO(); csv.writer(out, lineterminator='\n').writerows(rows)
            open(p, 'w', encoding='utf-8', newline='').write(out.getvalue())
    print('rows filled:', filled, '(written)' if write else '(dry run)')
    if write:   # flat log for ad-hoc regrouping (same file the July proof run started)
        p = os.path.join(ROOT, 'ubm_stats.csv')
        have = {tuple(r[k] for k in ('date', 'ubm_url', 'component', 'item', 'config')) for r in csv.DictReader(open(p, encoding='utf-8'))}
        mrow = {m['ubm_id']: m for m in smap}; add = []
        for sid, d in raw.items():
            m = mrow.get(sid, {'brand': '', 'model': ''})
            for comp, name, brand, cnt, cid in d['rows']:
                item, cfg = name, ''
                if comp == 'RAM':
                    mm = re.search(r'\s*(\d+x\d+GB|\d+GB)\s*$', name)
                    if mm: item, cfg = name[:mm.start()].strip() or name, mm.group(1)
                elif comp in ('SSD', 'HDD'): cfg = cap_of(name) or ''
                row = [d['date'], m['brand'], m['model'], d['sys'].replace(' System / ', ' '), d['u'], str(num(d['n'])), comp.lower(), item, cfg, str(num(cnt))]
                if (row[0], row[4], row[6], row[7], row[8]) not in have: add.append(row)
        with open(p, 'a', encoding='utf-8', newline='') as f: csv.writer(f, lineterminator='\n').writerows(add)
        print('ubm_stats.csv: +%d rows' % len(add))

if __name__ == '__main__': main()
