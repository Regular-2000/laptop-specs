#!/usr/bin/env python3
"""Generate eBay searches + title regexes (row_map lines) for grid rows.
   python3 tools/ebay_rows.py            -> prints brand|pull_model|query for rows not yet in row_map.csv
   python3 tools/ebay_rows.py --append   -> also appends them to ebay_raw/row_map.csv
Selection (SM 2026-11-16): soldered-RAM rows from 2015 (gen 5+), socketed rows from 2017 (gen 7+)."""
import csv, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORD = {1:'1st',2:'2nd',3:'3rd'}
def gen_rx(series, n):
    o = ORD.get(n, '%dth' % n)
    s = series
    return r'\b%s\b.*(\bgen\s*%d\b|\b%s\s*gen\b|\bg%d\b)|(\bgen\s*%d\b|\b%s\s*gen\b).*\b%s\b' % (s, n, o, n, n, o, s)
DELL_X = r'\binspiron\b|\bvostro\b|\bprecision\b|\boptiplex\b|\bxps\b'
def dell(m, sold):
    if m.startswith('Pro Plus'):
        n = m.split()[-1]; return ('dell pro %s plus' % n, r'\bpro\s*%s\s*plus\b|\bpro\s*plus\s*%s\b' % (n, n), '')
    if m.startswith('Pro Rugged'):
        n = m.split()[-1]; return ('dell pro rugged %s' % n, r'\bpro\s*rugged\s*%s\b' % n, r'\blatitude\b')
    num = re.match(r'(\d{4})', m).group(1)
    must = r'\blatitude\b.*\b%s\b|\b%s\b.*\blatitude\b' % (num, num)
    if 'Rugged' in m:
        q = 'dell latitude %s rugged' % num; must = r'\b%s\b.*\brugged\b|\brugged\b.*\b%s\b' % (num, num); exc = DELL_X
    else:
        q = 'dell latitude %s' % num; exc = DELL_X + r'|\brugged\b' + ('' if sold else r'|\b2[- ]?in[- ]?1\b')
    return q, must, exc
def thinkpad(m, sold):
    lead = m.split(' / ')[0].strip()
    if lead == 'X1 Titanium Yoga': return ('lenovo thinkpad x1 titanium yoga', r'\bx1\s*titanium\b', '')
    if lead.startswith('T14s Gen 6'): return ('lenovo thinkpad t14s gen 6 snapdragon', gen_rx('t14s', 6), r'\bintel\b|\bryzen\b|\bultra\b')
    g = re.match(r'(.+?)\s+Gen\s+(\d+)$', lead)
    if g:
        ser, n = g.group(1).lower(), int(g.group(2))
        serx = re.sub(r'\s+', r'\\s*', re.escape(ser).replace(r'\ ', ' '))
        exc = []
        if re.fullmatch(r'[tlex]1[3-6]|p1|z1[36]|l1[3-6]|e1[3-6]|t1[4-6]', ser): exc.append(r'\b%ss\b' % ser)
        if ser in ('x1 carbon',): exc.append(r'\byoga\b')
        if ser == 'x13': exc.append(r'\byoga\b|\bx13s\b')
        if ser == 'p1': exc.append(r'\bp1\s*gen\s*1[0-9]')
        exc.append(r'\bgen\s*%d\d' % n)       # gen 1 vs gen 10-13
        return ('lenovo thinkpad %s gen %d' % (ser, n), gen_rx(serx, n), '|'.join(exc))
    tok = lead.lower()
    exc = r'\b%ss\b|\b%sp\b' % (tok, tok)
    return ('lenovo thinkpad %s' % tok, r'\b%s\b' % tok, exc)
def hp(m, sold):
    parts = [p.strip() for p in m.split(' / ')]
    lead = next((p for p in parts if re.match(r'84\d\s+G', p)), parts[0])
    L = lead.lower()
    special = {
      'folio 1020 g1': ('hp elitebook folio 1020 g1', r'\b1020\s*g1\b', ''),
      'elite folio': ('hp elite folio', r'\belite\s*folio\b', r'\b1020\b|\b9470m?\b|\b1040\b|\b9480m?\b'),
      'dragonfly g1': ('hp elite dragonfly', r'\bdragonfly\b', r'\bg[2-9]\b|\bmax\b'),
      'zbook ultra g1a': ('hp zbook ultra g1a', r'\bultra\s*g1a\b', ''),
      'zbook 8 g1i': ('hp zbook 8 g1i', r'\bzbook\s*8\s*g1i\b', ''),
      'zbook fury g1i 16': ('hp zbook fury g1i', r'\bfury\b.*\bg1i\b', ''),
    }
    if L in special: return special[L]
    m2 = re.match(r'(x360 )?(\d{3,4})\s+(g\d+)$', L)
    if m2:
        x, num, g = m2.groups()
        line = 'probook' if num[0] in '46' and len(num) == 3 else 'elitebook'
        q = 'hp %s %s%s %s' % (line, x or '', num, g)
        must = r'\b%s\s*%s\b' % (num, g)
        if x: must = r'\bx360\b.*' + must
        exc = '' if x or num == '1040' else r'\bx360\b'
        return (q, must, exc)
    m3 = re.match(r'(dragonfly) (g\d)$', L)
    if m3: return ('hp elite dragonfly %s' % m3.group(2), r'\bdragonfly\b.*\b%s\b' % m3.group(2), r'\bmax\b')
    m4 = re.match(r'(zbook )?(firefly|fury|power|studio)?\s*(\d{2})?\s*(g\d+)$', L)
    if m4:
        _, fam, sz, g = m4.groups()
        bits = [b for b in (fam, sz, g) if b]
        q = 'hp zbook ' + ' '.join(bits)
        must = r'\bzbook\b.*' + r'\s*'.join(r'\b%s\b' % b if i == 0 else b + r'\b' for i, b in enumerate(bits))
        exc = '' if fam else r'\bstudio\b|\bfirefly\b|\bfury\b|\bpower\b|\b15u\b|\b15v\b|\bcreate\b'
        return (q, must, exc)
    raise ValueError('no rule for hp ' + m)
def main():
    path = os.path.join(ROOT, 'ebay_raw', 'row_map.csv')
    have = {(r['brand'], r['csv_model']) for r in csv.DictReader(open(path, encoding='utf-8'))}
    new = []
    for b, f in (('dell', dell), ('thinkpad', thinkpad), ('hp', hp)):
        for x in csv.DictReader(open(os.path.join(ROOT, b + '.csv'), encoding='utf-8', newline='')):
            y = int(x['year'] or 0); s = x['sold'] == '1'
            if not ((s and y >= 2015) or (not s and y >= 2017)) or (b, x['model']) in have: continue
            q, must, exc = f(x['model'], s)
            re.compile(must, re.I); exc and re.compile(exc, re.I)
            new.append([b, x['model'], x['model'], must, exc, q])
    for n in new: print('%s|%s|%s' % (n[0], n[1], n[5]))
    if '--append' in sys.argv:
        with open(path, 'a', encoding='utf-8', newline='') as fh:
            csv.writer(fh, lineterminator='\n').writerows([n[:5] for n in new])
        print('appended', len(new))
if __name__ == '__main__': main()
