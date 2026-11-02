#!/usr/bin/env python3
# ground-check (owner: Watchman; for QM's r2h "16/16S look everywhere"). No browser: reads PNGs with Pillow + numpy only.
# Flags (a) the old scene path stroke and (b) floating round-crowned trees. Writes nothing except --selftest scratch in ./runs/.
# Colours come from the draw code (cited in README): path #E8D9A8 @ .85 (mock-t328u/find_t328u.py:72,:76; t441u_outdoor.py; stage_v608.py
# W24/B) and #D8C99A @ .8 (stage_v608.py:36-37, scene A); grass #36A13D near / #259D39 far (P.ground); tree trunk #8A5A34, trunk shade
# #6C4425, canopy #7ECA72 / #489B3B / #28792D (mock-t277u/style_test.py:23-28 via P.tree).
import sys, os, hashlib, glob, json
import numpy as np
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
def hexrgb(h): h = h.lstrip('#'); return np.array([int(h[i:i+2], 16) for i in (0, 2, 4)], float)
def blend(fg, bg, a): return a*hexrgb(fg) + (1-a)*hexrgb(bg)
GRASS = [hexrgb('#36A13D'), hexrgb('#259D39')]
PATH = [hexrgb('#E8D9A8'), blend('#E8D9A8', '#36A13D', .85), blend('#E8D9A8', '#259D39', .85),
        hexrgb('#D8C99A'), blend('#D8C99A', '#36A13D', .8), blend('#D8C99A', '#259D39', .8)]
TRUNK = [hexrgb('#8A5A34'), hexrgb('#6C4425')]
CANOPY = [hexrgb('#7ECA72'), hexrgb('#28792D')]   # #489B3B is left out: within tolerance of grass #36A13D
TOL_PATH, TOL_GRASS, TOL_TREE = 14, 22, 20
def near(a, cols, tol):
    m = np.zeros(a.shape[:2], bool)
    for c in cols: m |= (np.abs(a - c) <= tol).all(axis=2)
    return m
def hdilate(m, r):   # True where any True lies within r px left/right (cumulative sum, no scipy)
    c = np.cumsum(np.pad(m.astype(np.int32), ((0, 0), (r+1, r))), axis=1); return (c[:, 2*r+1:] - c[:, :-2*r-1]) > 0
def components(m, maxn=4000):
    lab = np.zeros(m.shape, np.int32); out = []; ys, xs = np.nonzero(m); H, W = m.shape
    for y0, x0 in zip(ys, xs):
        if lab[y0, x0]: continue
        k = len(out) + 1; st = [(y0, x0)]; lab[y0, x0] = k; pts = []
        while st:
            y, x = st.pop(); pts.append((y, x))
            for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                v, u = y+dy, x+dx
                if 0 <= v < H and 0 <= u < W and m[v, u] and not lab[v, u]: lab[v, u] = k; st.append((v, u))
        out.append(np.array(pts))
        if len(out) >= maxn: break
    return out
def check(path):
    a = np.asarray(Image.open(path).convert('RGB'), float); H, W = a.shape[:2]; why = []
    grass = near(a, GRASS, TOL_GRASS)
    # (a) path stroke: path-coloured pixels with grass within r px on the same row (keeps parchment/card tans out)
    r = max(6, W // 40)
    pm = near(a, PATH, TOL_PATH) & hdilate(grass, r)
    n = int(pm.sum()); thr = max(40, int(0.0004 * H * W))
    if n >= thr:
        ys, xs = np.nonzero(pm); why.append(f'path stroke: {n} px (min {thr}) in box x{xs.min()}-{xs.max()} y{ys.min()}-{ys.max()}')
    # (b) floating tree: a trunk blob with canopy just above it whose bottom row has no grass within g px below
    tm = near(a, TRUNK, TOL_TREE); cl = near(a, CANOPY[:1], TOL_TREE) & ~grass; cd = near(a, CANOPY[1:], TOL_TREE) & ~grass; cm = cl | cd
    for c in components(tm):
        if len(c) < 8: continue
        y0, y1, x0, x1 = c[:, 0].min(), c[:, 0].max(), c[:, 1].min(), c[:, 1].max(); h, w = y1-y0+1, x1-x0+1
        if h < 4 or w < 2 or h < 1.2*w: continue   # 1 px slivers at sheet scale are outlines or swing-set legs, not trunks   # trunks are upright; benches, desks and shelves are wide
        sl = (slice(max(0, y0-2*h), y0+2), slice(max(0, x0-2*w), min(W, x1+2*w+1)))
        if cm[sl].sum() < max(4, w*h//2) or not cl[sl].any() or not cd[sl].any(): continue   # needs both canopy tones over it, or it is not a tree
        g = max(4, int(round(0.35*h)))
        below = grass[y1+1:min(H, y1+1+g), max(0, x0-1):min(W, x1+2)]
        if below.size == 0 or below.sum() == 0:
            why.append(f'floating tree: trunk x{x0}-{x1} y{y0}-{y1}, no grass in the {g} px below its foot')
    return why
def md5(p): return hashlib.md5(open(p, 'rb').read()).hexdigest()
def run(folder):
    man = next((p for p in [os.path.join(folder, 'MANIFEST.md5'), os.path.join(os.path.dirname(os.path.abspath(folder)), 'MANIFEST.md5')] if os.path.exists(p)), None)
    print(f'ground_check {md5(os.path.abspath(__file__))} | folder {os.path.abspath(folder)} | MANIFEST ' + (f'{md5(man)} ({man})' if man else 'none'))
    files = sorted(glob.glob(os.path.join(folder, '**', '*.png'), recursive=True)); nb = 0
    for f in files:
        why = check(f); nb += bool(why)
        print(f"{os.path.relpath(f, folder)}  {md5(f)}  {'BLOCK' if why else 'PASS'}" + (' | ' + ' ; '.join(why) if why else ''))
    print(f'summary: {len(files)} png, {nb} BLOCK, {len(files)-nb} PASS'); return 2 if nb else 0
def selftest():
    src = '/workspace/v608build/scenes/stage/png/W24-walk-B-390x844.png'   # tile 16 render: both trees grounded (t441u), tufts
    d = os.path.join(HERE, 'runs', 'selftest'); os.makedirs(d, exist_ok=True)
    im = Image.open(src).convert('RGB'); s = im.width / 390
    clean = im.crop((0, 0, im.width, int(720*s)))   # rows above the ask card: drops the old stroke's sliver under the card (y > 724 pt)
    clean.save(os.path.join(d, 'tile6-clean.png'))
    p = clean.copy(); dr = ImageDraw.Draw(p); col = tuple(int(round(v)) for v in PATH[1])
    pts = [((1-t)**2*140 + 2*t*(1-t)*160 + t*t*260, (1-t)**2*720 + 2*t*(1-t)*560 + t*t*594) for t in [i/40 for i in range(41)]]
    dr.line([(x*s, y*s) for x, y in pts], fill=col, width=int(26*s)); p.save(os.path.join(d, 'tile6-planted-path.png'))
    q = clean.copy(); box = tuple(int(v*s) for v in (346, 320, 390, 380))   # right tree (x 372, foot y 376.3 pt): lift it 76 pt into the sky
    cut = clean.crop(box); keep = Image.fromarray((~near(np.asarray(cut, float), GRASS, TOL_GRASS)).astype(np.uint8) * 255)   # the tree only, not the grass it stood in
    q.paste(cut, (box[0], box[1] - int(76*s)), keep); q.save(os.path.join(d, 'tile6-planted-float.png'))
    res = {n: check(os.path.join(d, n)) for n in ('tile6-clean.png', 'tile6-planted-path.png', 'tile6-planted-float.png')}
    ok = (not res['tile6-clean.png'] and any(w.startswith('path') for w in res['tile6-planted-path.png'])
          and any(w.startswith('floating') for w in res['tile6-planted-float.png']))
    print(f'ground_check {md5(os.path.abspath(__file__))} selftest ' + ('PASS' if ok else 'FAIL') + f' | src {md5(src)} | scratch {d}')
    for n, w in res.items(): print(f"  {n}  {md5(os.path.join(d, n))}  {'BLOCK' if w else 'PASS'}" + (' | ' + ' ; '.join(w) if w else ''))
    return 0 if ok else 2
if __name__ == '__main__':
    if sys.argv[1:2] == ['--selftest']: sys.exit(selftest())
    if len(sys.argv) < 2: print('usage: ground_check.py FOLDER [FOLDER...] | --selftest'); sys.exit(1)
    sys.exit(max(run(f) for f in sys.argv[1:]))
