#!/usr/bin/env python3
"""Build the `typ` / `typ_note` columns ("📦 Likely config — random unit") for the brand CSVs.

    python3 tools/typ_build.py            # dry run: prints what each row would get
    python3 tools/typ_build.py --write    # writes dell / thinkpad / hp .csv

MAIN source   = eBay ACTIVE listing titles  (ebay_raw/<date>_active.json  +  ebay_raw/row_map.csv)
               = the population you actually buy from. Odds are rounded to 5 %, shares < 5 % dropped.
SECOND opinion = UserBenchmark system pages (ubm_raw/*.jsonl + ubm_raw/system_map.csv), shown behind ⓘ.
                 Used for the main line only when a row has no eBay pull.

All parsing / grouping rules live in this file — change them and re-run; raw data is never edited.
"""
import csv, glob, io, json, os, re, sys, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import typ_from_ubm as U                                   # UBM raw loader + RAM/SSD parsers

ROOT = U.ROOT
MIN_SHOW = 10                   # fewer usable listings than this -> no eBay line at all (UBM fallback or blank)
THIN = 50                       # fewer usable listings than this -> line gets "(thin sample)"


# ---------- CPU-generation guard (Dell reused 3440/3450/3540/3550 etc.; sellers drop the "E" on E5450) ----------
def row_min_gen(cpu):
    """Lowest Intel Core generation the grid row allows (None = can't tell, e.g. AMD / Celeron / ARM)."""
    c = cpu.lower()
    if 'core ultra' in c and not re.search(r'\d+(st|nd|rd|th)\s*gen', c): return 14
    g = [int(x) for x in re.findall(r'(\d+)(?:st|nd|rd|th)(?:/\d+(?:st|nd|rd|th))*\s*gen', c)]
    g += [int(x) for x in re.findall(r'(\d+)(?:st|nd|rd|th)\s*/', c)]
    for name, n in (('broadwell', 5), ('skylake', 6), ('kaby lake r', 8), ('kaby lake', 7), ('whiskey', 8), ('comet', 10),
                    ('tiger', 11), ('alder lake', 12), ('raptor', 13), ('meteor', 13), ('lunar', 14), ('arrow', 14)):
        if name in c and not ('n100' in c or 'n200' in c or 'celeron' in c): g.append(n)
    return min(g) if g else None
def title_gen(t):
    m = re.search(r'\bi[3579][- ]?(1[0-4])\d{2,3}[a-z]{0,2}\b', t, re.I)
    if m: return int(m.group(1))
    m = re.search(r'\bi[3579][- ]?([2-9])\d{3}[a-z]{0,2}\b', t, re.I)
    if m: return int(m.group(1))
    m = re.search(r'\b(\d{1,2})(?:st|nd|rd|th)\s*gen', t, re.I)
    if m: return int(m.group(1))
    return None
# ---------- eBay title parsing ----------
DROP = re.compile(r'\blot\b|\bqty\b|\bbulk\b|\(\s*\d+\s*\)\s*(dell|hp|lenovo)|\b\d+\s*x\s*(dell|hp|lenovo|latitude)|'
                  r'for parts|parts only|parts/repair|parts repair|not working|\bas[- ]is\b|broken|no post|no boot|no power|'
                  r'bios lock|locked|motherboard|\bup ?to\b|\bmixed\b|\d+\s*-\s*\d+\s?gb|\d+\s?/\s?\d+\s?gb\b|\bupgradable\b', re.I)
NO_RAM = re.compile(r'\bno\b[\s/,&a-z]{0,20}?\b(ram|memory|mem)\b|\bw/?o\s*(ram|memory)\b', re.I)
NO_SSD = re.compile(r'\bno\b[\s/,&a-z]{0,25}?\b(ssd|hdd|hd|nvme|drive|storage|hard ?drive|m\.?2)\b|\bw/?o\s*(ssd|hdd|drive|storage)\b', re.I)
RAM_TOK = re.compile(r'(?<![\d.])(\d{1,2})\s?gb\b(?!\s*(ssd|nvme|m\.?2|hdd|sata|emmc|storage|solid|hd\b|flash))', re.I)
RAM_OK = {2, 4, 6, 8, 12, 16, 20, 24, 32, 40, 48, 64}
CAP_TOK = re.compile(r'(?<![\d.])(\d+(?:\.\d+)?)\s?(tb|gb|g)\b|(?<![\d.])(128|240|250|256|480|500|512|1000)\s?(nvme|ssd|m\.?2)', re.I)

# a GB figure right after a graphics card (or followed by GDDR/VRAM) is video memory, not system RAM
GPU_BEFORE = re.compile(r'((rtx|gtx|quadro|geforce|radeon)\s*(pro\s*)?[a-z]?\s?\d{0,4}\s*(ti|super|ada|max-q)?|\b[atpw]\d{3,4}m?|\bmx\s?\d{3}|\bnvidia|\bgpu)\s*[-,(]?\s*$', re.I)
GPU_AFTER = re.compile(r'^\s?(gddr|vram|video|graphics|dedicated)', re.I)
def ram_of(t):
    if NO_RAM.search(t): return 'none'
    for m in RAM_TOK.finditer(t):
        n = int(m.group(1))
        if GPU_BEFORE.search(t[max(0, m.start() - 30):m.start()]) or GPU_AFTER.search(t[m.end():m.end() + 12]): continue
        if n in RAM_OK: return n
    return None

def ssd_of(t):
    for m in CAP_TOK.finditer(t):
        if m.group(1):
            g = float(m.group(1)) * (1000 if m.group(2).lower() == 'tb' else 1)
        else:
            g = float(m.group(3))
        if g >= 100 and g not in RAM_OK:
            return '128 GB' if g < 200 else '256 GB' if g < 300 else '512 GB' if g < 800 else '1 TB+'
    if NO_SSD.search(t): return 'none'
    return None

def odds(counter):
    n = sum(counter.values())
    out = []
    for k, v in counter.most_common():
        p = int(5 * round(20.0 * v / n)) if n else 0
        if p: out.append((k, p))
    return out, n

def fmt(pairs, unit_gb=True):
    return ' · '.join('%s ~%d%%' % ((('%s GB' % k) if isinstance(k, int) else k), p) for k, p in pairs)

def load_ebay():
    rows = list(csv.DictReader(open(os.path.join(ROOT, 'ebay_raw', 'row_map.csv'), encoding='utf-8')))
    cpu = {}
    for b in ('dell', 'thinkpad', 'hp'):
        for x in csv.DictReader(open(os.path.join(ROOT, b + '.csv'), encoding='utf-8', newline='')): cpu[(b, x['model'])] = x['cpu']
    rmap = {(r['brand'], r['pull_model']): r for r in rows}
    best = {}
    for f in sorted(glob.glob(os.path.join(ROOT, 'ebay_raw', '*_active.json'))):
        d = json.load(open(f, encoding='utf-8'))
        for p in d['pulls']:
            if p.get('status') != 200: continue
            p['date'] = d['date']; p['file'] = os.path.basename(f)
            best[(p['brand'], p['model'])] = p            # later files win
    res = {}
    for k, p in best.items():
        m = rmap.get(k)
        if not m: print('!! eBay pull without row_map entry:', k); continue
        must = re.compile(m['must'], re.I); exc = re.compile(m['exclude'], re.I) if m['exclude'] else None
        mg = row_min_gen(cpu.get((p['brand'], m['csv_model']), ''))
        seen = set(); ram = collections.Counter(); ssd = collections.Counter(); kept = drop = 0; oldcpu = 0
        for it in p['items']:
            t = it['t']
            if not must.search(t) or (exc and exc.search(t)): continue
            if DROP.search(t) or re.search(r'parts', it.get('cond', ''), re.I): drop += 1; continue
            tg = title_gen(t)
            if mg and tg and tg < mg: oldcpu += 1; continue
            if mg and mg >= 12 and re.search(r'\bhdd\b|\bhard drive\b|\bdvd', t, re.I) and not tg: oldcpu += 1; continue
            key = re.sub(r'[^a-z0-9]', '', t.lower())
            if key in seen: continue
            seen.add(key); kept += 1
            r = ram_of(t); s = ssd_of(t)
            if r is not None: ram[r] += 1
            if s is not None: ssd[s] += 1
        res[(p['brand'], m['csv_model'])] = dict(p=p, kept=kept, drop=drop, ram=ram, ssd=ssd, lead=m['pull_model'], oldcpu=oldcpu, mingen=mg)
    return res

# ---------- UserBenchmark second opinion ----------
def ubm_odds(d):
    ram = collections.Counter(); ssd = collections.Counter()
    for comp, name, brand, cnt, cid in d['rows']:
        c = U.num(cnt)
        if comp == 'RAM':
            g = U.ram_of(name)[0]
            if g: ram[g] += c
        elif comp == 'SSD':
            lab = U.cap_of(name)
            if lab: ssd['1 TB+' if lab in ('1 TB', '2 TB', '4 TB') else lab] += c
    return odds(ram)[0], odds(ssd)[0]

def main():
    write = '--write' in sys.argv
    eb = load_ebay()
    raw = U.load_raw()
    smap = list(csv.DictReader(open(os.path.join(ROOT, 'ubm_raw', 'system_map.csv'), encoding='utf-8')))
    ub = collections.defaultdict(list)
    for m in smap:
        if m['ubm_id'] in raw:
            raw[m['ubm_id']]['label'] = m.get('label', ''); ub[(m['brand'], m['model'])].append(raw[m['ubm_id']])
    filled = 0
    for brand in ('dell', 'thinkpad', 'hp'):
        p = os.path.join(ROOT, brand + '.csv')
        rows = list(csv.reader(io.StringIO(open(p, encoding='utf-8', newline='').read())))
        H = rows[0]; iT, iN, iM = H.index('typ'), H.index('typ_note'), H.index('model')
        for r in rows[1:]:
            k = (brand, r[iM]); e = eb.get(k); us = ub.get(k)
            if not e and not us:
                continue
            note = []; line = ''
            if e and e['kept'] < MIN_SHOW:
                note.append('eBay: only %d usable listings for "%s" on %s — too few to show odds.' % (e['kept'], e['p']['query'], e['p']['date']))
                e = None
            if e:
                ro, rn = odds(e['ram']); so, sn = odds(e['ssd'])
                thin = ' (thin sample)' if e['kept'] < THIN else ''
                line = 'RAM ' + fmt(ro) + '<br>SSD ' + fmt(so) + thin
                q = e['p']
                note.append('eBay active listings (US), %s, search "%s"%s: %d listings counted (identical titles once; '
                            'lots, for-parts, spec ranges%s dropped), RAM stated in %d, SSD in %d. "none" = sold without '
                            'RAM / without a drive. 32 GB+ and 1 TB+ are mostly refurbisher upgrades.'
                            % (q['date'], q['query'], (' — lead model ' + e['lead'] + ' only') if '/' in r[iM] else '',
                               e['kept'], (' and %d older-CPU look-alikes' % e['oldcpu']) if e['oldcpu'] else '', rn, sn))
            if us:
                d = max(us, key=lambda x: U.num(x['n']))
                if U.num(d['n']) >= U.MIN_PCS:
                    ur, uss = ubm_odds(d)
                    name = d['sys'].replace('System / ', '') + (' (%s)' % d['label'] if d.get('label') else '')
                    txt = 'RAM ' + fmt(ur) + ' · SSD ' + fmt(uss)
                    note.append('Second opinion — UserBenchmark (%s, %s PCs, %s; benchmarked machines, owner upgrades '
                                'included, top-5 parts only): %s.' % (name, d['n'], d['date'], txt))
                    if not line: line = 'RAM ' + fmt(ur) + '<br>SSD ' + fmt(uss) + ' (benchmark data)'
            if not line:
                if r[iT] or r[iN]: r[iT], r[iN] = '', ''
                continue
            r[iT], r[iN] = line, ' '.join(note); filled += 1
            print('%-9s %-32s %s' % (brand, r[iM][:32], line.replace('<br>', '  |  ')))
        if write:
            out = io.StringIO(); csv.writer(out, lineterminator='\n').writerows(rows)
            open(p, 'w', encoding='utf-8', newline='').write(out.getvalue())
    print('rows filled:', filled, '(written)' if write else '(dry run)')

if __name__ == '__main__': main()
