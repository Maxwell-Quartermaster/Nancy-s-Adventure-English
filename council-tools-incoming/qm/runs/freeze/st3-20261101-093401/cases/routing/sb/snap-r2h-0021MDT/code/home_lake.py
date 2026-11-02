# Council call (7:53 PM MDT): extend t444u to every home-lake room. The 390 and 375x812 renders take the 320-frame ceiling crop in the
# 3B look (the 320 ceiling strip under the HUD, plain wall down to the molding); the 320 renders are not touched (byte-identical).
# Rooms: 14, 16, 20, 21, 32, 33, 54, zone lake, tod lake 1-5. Usage: python3 home_lake.py -> home-lake/{html,png}/<room>-{390x844,375x812}.*
import sys, os, re, json, hashlib
sys.argv = ['x']; sys.path.insert(0, '/workspace/v608build/scenes'); sys.path.insert(0, '/workspace/v608build/screens')
import tod_v608 as T
PV, Z = T.PV, T.Z; MARK = '<!--UI-->'
_t, _h = PV.top, Z.hud
PV.top = lambda *a, **k: MARK + _t(*a, **k); Z.hud = lambda *a, **k: MARK + _h(*a, **k)
NUMS = [14, 16, 17, 18, 19, 20, 21, 22, 32, 33, 54]; V = '/workspace/screens-v608/html/'; TD = '/workspace/v608build/scenes/tod/'   # Auditor eb2674be: 17-19 (two-answer) and 22 (kitchen server talk) are Home Lake rooms too
def split(h): i = h.index(MARK); return h[:i], h[i:].replace(MARK, '')
def tod_split(b):
    k = b.index("data-name='back'"); k = b.rindex('<div', 0, k); i = min(b.index(MARK), k) if MARK in b else k
    sty = b[:b.index('</style>') + 8] if b.startswith('<style>') else ''
    return b[:i], sty + b[i:].replace(MARK, '')
def parts(w, h):
    out = {}; sv = PV.W, PV.H; PV.W, PV.H = w, h
    try:
        for n in NUMS: slug = PV.SCR[n][0]; out[f'{n:02d}-{slug}'] = (split(PV.SCR[n][3]()), V + f'{n:02d}-{slug}-320x568.html')
        out['zone-lake-ask'] = (split(Z.screen('lake', 'ask', w, h)), V + 'zone-lake-ask-320x568.html')
        for st in range(1, 6): out[f'lake-step{st}'] = (tod_split(T.body('lake', st, w, h)), TD + f'lake-step{st}-320x568.html')
    finally: PV.W, PV.H = sv
    return out
P390 = parts(390, 844); P812 = parts(375, 812)
import stage_v608 as ST
sys.path.insert(0, '/workspace/v608build/round2/trimcheck'); import trim_clip_check as TC   # Auditor: 1A ', never over a target' (+21)
WORLD = re.compile(r"<div class='abs' data-st='[^']+' style='left:(-?[0-9.]+)px;top:(-?[0-9.]+)px;width:390px;height:844px;overflow:hidden;transform:scale\(([0-9.]+)\)")
def div_end(d, i):   # index just past the </div> closing the div opened at i
    n = 0
    for m in re.compile(r'<div\b|</div>').finditer(d, i):
        n += 1 if m.group(0) == '<div' else -1
        if n == 0: return m.end()
    raise ValueError
def cap_of(f320):
    d = open(f320).read(); ox, oy, s = map(float, WORLD.search(d).groups()); return (ST.measure(d, 320, 568)['top'] - oy) / s
CEIL = 372
CAP = cap_of(V + 'zone-lake-ask-320x568.html')   # one room frame: the home-lake room as the 320 ask shows it (HUD + chip only; ribbon screens would crop into the room)
def wallup(doc, cap, vis, fit):
    s, ox, oy = fit; d = cap - vis; mb = CEIL + 8; m = WORLD.search(doc); k = m.start(); e = div_end(doc, k); world = doc[k:e]
    a = "overflow:hidden;transform:scale"; assert world.count(a) == 1
    real = world.replace(a, f"overflow:hidden;-webkit-clip-path:inset({mb}px 0 0 0);clip-path:inset({mb}px 0 0 0);transform:scale")
    strip = re.sub(r"data-(pn|hit|st|name|hero|tagph|inert)=", r"data-cp-\1=", world.replace(a, f"overflow:hidden;-webkit-clip-path:inset({cap:.1f}px 0 {844 - mb}px 0);clip-path:inset({cap:.1f}px 0 {844 - mb}px 0);transform:scale"))
    strip = strip.replace(f"top:{m.group(2)}px", f"top:{oy - d * s:.2f}px", 1).replace("<div class='abs'", "<div class='abs' aria-hidden='true'", 1)
    band = f"<div class='abs' aria-hidden='true' style='left:{ox:.1f}px;top:{oy + (mb - d) * s:.1f}px;width:{390 * s:.1f}px;height:{d * s:.1f}px;background:#EAD7A8'></div>"
    return doc[:k] + band + strip + real + doc[e:]
O = '/workspace/v608build/round2/ceiling-cap/home-lake/'; os.makedirs(O + 'html', exist_ok=True); os.makedirs(O + 'png', exist_ok=True)
log = []
for name, ((scene, ui390), f320) in P390.items():
    cap = CAP; assert '#EAD7A8' in scene or 'M0 372h390' in scene, name
    m390 = ST.measure(ST.compose(name, scene, ui390, 390, 844, (1, 0, 0)), 390, 844)
    (_, ui8), _ = P812[name]
    for w, h, ui in ((390, 844, ui390), (375, 812, ui8)):
        m = ST.measure(ST.compose(name, scene, ui, w, h, (1, 0, 0)), w, h)
        fit = (1, 0, 0) if w == 390 else ST.fit_capped(scene, m390, m, w, h); fit = (fit[0], fit[1], m['card'] - m390['card'] * fit[0]) if w != 390 else fit
        doc0 = ST.compose(name, scene, ui, w, h, fit); vis = (m['top'] - fit[2]) / fit[0]; f = f'{name}-{w}x{h}'
        if vis >= cap - 0.5: log.append(f'- {f}: shows from design y {vis:.0f}, 320 cap {cap:.0f}: no ceiling to trim (scene fit only)'); doc = doc0
        else:
            doc = wallup(doc0, cap, vis, fit); cl = TC.clipped(doc, w, h)
            if cl: doc = doc0; log.append(f'- {f}: kept its ceiling, never over a target (1A ", never over a target"): the trim would cut {sorted(set(c[0] for c in cl))}')
            else: log.append(f'- {f}: scale {fit[0]:.3f}; trimmed design y {vis:.0f}-{cap:.0f} ({(cap - vis) * fit[0]:.0f} pt) to the 320 frame (3B)')
        open(O + f'html/{f}.html', 'w').write(doc); ST.shot(doc, O + f'png/{f}.png', w, h); print(log[-1], flush=True)
        if w == 390 and name.startswith('20-'):   # 20 has no approved 390 render: the untrimmed one, for the before/after strip
            open(O + f'html/{f}-before.html', 'w').write(doc0); ST.shot(doc0, O + f'png/{f}-before.png', w, h)
open(O + 'LOG.md', 'w').write('# Home-lake rooms, 320-frame ceiling crop (3B)\n' + '\n'.join(log) + '\n')
