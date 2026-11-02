# Builds scene-inventory-20261101.{md,json} and the INTERNAL contact sheet from /tmp/inv/rows.json (read-only scan output).
import json, os, collections as C, hashlib, datetime
from PIL import Image, ImageDraw, ImageFont
W = '/workspace'; OUT = W + '/council-tools/'
R = json.load(open('/tmp/inv/rows.json'))
for r in R:
    if r['in_progress'] and r['status'] != 'BEFORE': r['status'] = 'IN-PROGRESS'
man = set(l.split(None, 1)[1].strip() for l in open(W + '/v608build/snap-r2h-0021MDT/renders-MANIFEST.md5'))
LOCS = [('meadow-park', 'Word Meadow', 'Park (swing set, bench, bus stop, kite)', 'Phonics, Sight Words', 1),
        ('meadow-pond', 'Word Meadow', 'Park by a pond (alternate layout)', 'Phonics, Sight Words', 1),
        ('lake-home', 'Home Lake', 'Inside the home (shelf, window, desk, crib, rug)', 'Maxwell Says (day one), Baby and Hospital (after Number guardian)', 2),
        ('lake-kitchen', 'Home Lake', 'Home room set for a meal (small table replaces crib)', "Nancy's Kitchen (day one)", 2),
        ('lake-front-desk', 'Home Lake', 'Hotel front desk', 'Maxwell Says ms-03 to ms-06, ms-21 to ms-23 only (day one)', 3),
        ('fields-farm', 'Golden Fields', 'Farm (corn row, gate, cow, basket)', 'Colors and Shapes, Numbers (after Word guardian)', 4),
        ('forest-woods', 'Echo Forest', 'Night woods (owl, lantern, tent, footbridge), also behind Sound Duel', 'Sound Duel (not one of the 7 zones; after Gentle guardian)', 5)]
TODS = [('m', 'step 1 morning'), ('d', 'step 2 midday'), ('a', 'step 3 afternoon'), ('e', 'step 4 evening'), ('n', 'step 5 night')]
RANK = ['CURRENT', 'IN-PROGRESS', 'CURRENT-LISTED-STALE-LOOK', 'OLD', 'BEFORE']
def uniq(rs):
    d = {}
    for r in rs:
        if r['md5'] not in d or r['path'] in man: d[r['md5']] = r
    return list(d.values())
def cell(loc, tod):
    rs = [r for r in R if r['loc'] == loc and r['tod'] == tod and r['kind'] != 'sheet']
    by = {s: uniq([r for r in rs if r['status'] == s]) for s in RANK}
    best = next((s for s in RANK[:4] if by[s]), 'NEVER')
    return best, by
def pick(rs):
    pr = lambda r: (r['size'] != '390x844', not r['path'].startswith('v608build/round2/r2h'), 'scenes/' not in r['path'], 'wallup' in r['path'], r['path'])
    return sorted(rs, key=pr)[0] if rs else None
SZ = ('320x568', '390x844')
matrix = []; 
for loc, reg, name, zones, tier in LOCS:
    for t, tn in TODS + [('base', 'untinted base (no time of day applied)')]:
        best, by = cell(loc, t)
        if t == 'base' and best == 'NEVER': continue
        cur = by['CURRENT']; cs = sorted({r['size'] for r in cur})
        matrix.append(dict(region=reg, location=loc, location_name=name, zones=zones, tier=tier, tod=t, tod_name=tn, status=best,
                           current_sizes=cs, current=[(r['path'], r['size']) for r in sorted(cur, key=lambda r: r['path'])],
                           in_progress=[(r['path'], r['size']) for r in by['IN-PROGRESS']],
                           listed_stale_look=[(r['path'], r['size'], r.get('stale')) for r in by['CURRENT-LISTED-STALE-LOOK']],
                           old=[(r['path'], r['size']) for r in by['OLD']],
                           counts={s: len(by[s]) for s in RANK}, thumb=(pick(by[best])['path'] if best != 'NEVER' else None),
                           need_320=('320x568' not in cs) and t != 'base', need_390=('390x844' not in cs) and t != 'base'))
spec_cells = [m for m in matrix if m['tod'] != 'base']
# extra time-bearing screens
def extra(loc, tods):
    out = []
    for t in tods:
        best, by = cell(loc, t); cs = sorted({r['size'] for r in by['CURRENT']})
        out.append(dict(screen=loc, tod=t, status=best, current_sizes=cs, current=[(r['path'], r['size']) for r in by['CURRENT']],
                        old=[(r['path'], r['size']) for r in by['OLD']], in_progress=[(r['path'], r['size']) for r in by['IN-PROGRESS']],
                        thumb=(pick(by[best])['path'] if best != 'NEVER' else None), need_320='320x568' not in cs, need_390='390x844' not in cs))
    return out
title = extra('TITLE', ['m', 'a', 'e', 'n'])
rest = extra('REST', ['e'])
menu = extra('MENU', ['m', 'a', 'e', 'n'])
maps = [r for r in R if r['loc'] == 'MAP' and r['kind'] != 'sheet']
mapinfo = {s: sorted({(r['path'], r['size']) for r in uniq([x for x in maps if x['status'] == s])}) for s in RANK}
cnt = C.Counter(m['status'] for m in spec_cells)
need320 = sum(m['need_320'] for m in spec_cells); need390 = sum(m['need_390'] for m in spec_cells)
tn320 = sum(x['need_320'] for x in title); tn390 = sum(x['need_390'] for x in title)
rn320 = sum(x['need_320'] for x in rest); rn390 = sum(x['need_390'] for x in rest)
mn320 = sum(x['need_320'] for x in menu); mn390 = sum(x['need_390'] for x in menu)
data = dict(generated=datetime.datetime.now().strftime('%Y-%m-%d %H:%M MDT'), base=dict(pointer='f6dac2d0e7b391436a160eab1bbf17fe', snap='snap-r2h-0021MDT',
            paste='317e91ce86f073c961f8169183d2bbd3', renders_manifest='62e41535fb1d86d3a05dec854c56f572'),
            status_meaning={'CURRENT': 'listed (path or md5) in snap-r2h-0021MDT renders-MANIFEST.md5 and its paired HTML has none of the stale-look markers (or has no HTML to test: marked look_ok null)',
                            'IN-PROGRESS': 'written by the r2h re-run into v608build/round2/r2h after the freeze; not in the manifest yet',
                            'CURRENT-LISTED-STALE-LOOK': 'listed in the manifest but its HTML still has a superseded look: meadow walkway/ground dots or Home Lake #D9663F chip (fixed in r2h), or the old ask wording Where is the ...? (replaced by P1 t440u)',
                            'OLD': 'not in the manifest (older snaps, screens-v603..v607, mocks, superseded folders)', 'NEVER': 'no render found anywhere scanned'},
            scanned_pngs=len(R), unique_pngs=len({r['md5'] for r in R}), matrix=matrix, title=title, menu=menu, rest=rest, map=mapinfo,
            totals=dict(cells=len(spec_cells), **{k: cnt.get(k, 0) for k in ['CURRENT', 'IN-PROGRESS', 'CURRENT-LISTED-STALE-LOOK', 'OLD', 'NEVER']}),
            renders_needed=dict(scene_320=need320, scene_390=need390, title_320=tn320, title_390=tn390, rest_320=rn320, rest_390=rn390, menu_320=mn320, menu_390=mn390))
json.dump(data, open(OUT + 'scene-inventory-20261101.json', 'w'), indent=1, ensure_ascii=False)
# contact sheet
F = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'; f14 = ImageFont.truetype(F, 14); f12 = ImageFont.truetype(F, 12); f22 = ImageFont.truetype(F, 22)
TW, TH = 140, 303; LW = 250; HD = 80; PAD = 8
rowsC = [(l, [next(m for m in matrix if m['location'] == l[0] and m['tod'] == t) for t, _ in TODS]) for l in LOCS]
rowsC.append((('TITLE', 'Title screen', 'Sword screen (clock: m a e n; no d)', '', 0), [next((x for x in title if x['tod'] == t), None) for t, _ in TODS]))
Wd = LW + 5 * (TW + PAD) + PAD; Ht = HD + len(rowsC) * (TH + 40) + 40
S = Image.new('RGB', (Wd, Ht), '#F6E9C8'); d = ScreenDraw = ImageDraw.Draw(S)
d.rectangle([0, 0, Wd, 34], fill='#A3211A'); d.text((10, 6), 'INTERNAL - NOT FOR MAXWELL YET - scene inventory 2026-11-01 (snap-r2h-0021MDT / PASTE 317e91ce)', fill='white', font=f14)
for i, (t, tn) in enumerate(TODS): d.text((LW + PAD + i * (TW + PAD), 48), tn, fill='#3A2410', font=f12)
COL = {'CURRENT': '#2E7D32', 'IN-PROGRESS': '#1565C0', 'CURRENT-LISTED-STALE-LOOK': '#E08A00', 'OLD': '#8A5F16'}
for j, (l, cells) in enumerate(rowsC):
    y = HD + j * (TH + 40)
    d.text((8, y + 4), l[1], fill='#3A2410', font=f14)
    words = l[2].split(); line = ''; yy = y + 24
    for w_ in words:
        if len(line + w_) > 30: d.text((8, yy), line, fill='#3A2410', font=f12); yy += 16; line = ''
        line += w_ + ' '
    d.text((8, yy), line, fill='#3A2410', font=f12)
    for i, m in enumerate(cells):
        x = LW + PAD + i * (TW + PAD)
        if m is None:
            d.rectangle([x, y, x + TW, y + TH], fill='#DDDDDD', outline='#999999'); d.text((x + 10, y + TH // 2), 'NOT IN SPEC', fill='#555555', font=f12); continue
        if m['status'] == 'NEVER':
            d.rectangle([x, y, x + TW, y + TH], fill='#9E9E9E', outline='#555555'); d.text((x + 14, y + TH // 2 - 8), 'NOT RENDERED', fill='white', font=f14)
            continue
        im = Image.open(W + '/' + m['thumb']).convert('RGB'); im.thumbnail((TW, TH)); S.paste(im, (x, y))
        lab = {'CURRENT': 'CURRENT', 'IN-PROGRESS': 'IN PROGRESS', 'CURRENT-LISTED-STALE-LOOK': 'STALE LOOK', 'OLD': 'OLD ONLY'}[m['status']]
        d.rectangle([x, y + TH - 20, x + TW, y + TH], fill=COL[m['status']]); d.text((x + 4, y + TH - 18), lab, fill='white', font=f12)
        d.text((x, y + TH + 2), ', '.join(s.split('x')[0] for s in m['current_sizes']) or '-', fill='#3A2410', font=f12)
d.text((8, Ht - 30), 'Green CURRENT = in renders-MANIFEST 62e41535 with r2h look. Orange = listed but stale look (pre-r2h scenery or old ask wording). Blue = r2h re-run, not frozen. Brown = old only. Grey = never rendered.', fill='#3A2410', font=f12)
S.save(OUT + 'scene-inventory-20261101-INTERNAL-contact-sheet.png')
print(json.dumps(data['totals']), json.dumps(data['renders_needed']))
for m in matrix: print(m['location'], m['tod'], m['status'], m['current_sizes'], {k: v for k, v in m['counts'].items() if v}, m['thumb'])
for x in title + menu + rest: print(x['screen'], x['tod'], x['status'], x['current_sizes'], len(x['old']), x['in_progress'])
print('MAP', {k: v for k, v in mapinfo.items() if v})
