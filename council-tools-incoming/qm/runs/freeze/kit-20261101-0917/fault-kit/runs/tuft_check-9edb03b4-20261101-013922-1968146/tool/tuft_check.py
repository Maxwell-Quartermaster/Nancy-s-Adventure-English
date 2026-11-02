#!/usr/bin/env python3
# tuft_check (owner: Watchman) - MAXWELL-EYE ME3 / OLD-LOOK O3: outdoor grass must carry three-stroke tufts, not rocks or dots.
# Base: snap-r2h-0021MDT, pointer /workspace/v608build/CURRENT-SNAP.txt 907062f0f1a143efcb283223d70fcbe6. Pillow + numpy only.
# Approved look (16/16S, t441u; tile 11 critique, MAXWELL-EYE ME3): t441u_outdoor.py:29-30 PV.tuft = three round-capped strokes,
#   colour #0F3A14, stroke-width 2.5 pt, heights ~10/14/10 pt, x offsets -6/-1/+4 pt; placed per scene by stage_v608.py:98-106 TUFTS.
# Old look it replaces (t441u_outdoor.py:36-37): r=3 pt dot circles #FFE27A / #FFF8E1 / #F2A0A8 on the meadow ("dot flowers and pebbles").
# Grass: #36A13D near / #259D39 far (P.ground), as in ground_check. Dimmed scenes (pause card / scrim): grass palette scaled by k, as v2.
# A grass BAND = a connected region of grass (tol 12, 8 px block grid) covering >= BAND_MIN_PT2 pt^2 and >= 30 pt tall.
#   Scale s: a phone-shaped image (H/W 1.4-2.4, width <= 900 px) uses image width / 390; a sheet uses band width / 390 (a band spans ~one tile).
#   BLOCK "bare grass"  : band has no tuft (tuft = >= 2 thin upright #0F3A14 strokes side by side; on sheet thumbnails, s < .7,
#                         a >= 3 px dark-green fleck fully ringed by grass-green counts, since strokes blur below 2 px).
#   BLOCK "rock dot"    : a small round non-green blob fully ringed by grass (diam 4-14 pt, fill >= .55 of its box, aspect <= 1.6).
#   t545u (Maxwell via QM, Nov 1 2026): flag a dot ONLY when it sits on grass. Each of the 4 sides of its 2 px ring must be >= 80% grass
#     and the ring >= 90% overall; a dot touching dirt, path, sand, hill or any non-grass surface is left alone (PASS), so pebbles stay.
#   ASK "bare grass" (t527u: bare grass that never had circles is an ASK, not a BLOCK): reported, exit stays 0 unless a rock dot BLOCKs.
# Blind spots (stay on the eye list): Echo Forest / Golden Fields / night grounds (not the meadow greens), coloured scrims,
#   tufts drawn in another colour, tufts mostly hidden under a card (only a clipped tuft visible reads bare, e.g. r2h 28-guardian-win-390), and
#   'before' panels, which always BLOCK by design.
# Writes stdout only; --selftest writes PNGs into ./selftest/ next to this file. Never deletes. Exit 0 PASS, 2 BLOCK/FAIL, 1 usage.
import sys, os, glob, hashlib
import numpy as np
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
def hexrgb(h): h = h.lstrip('#'); return np.array([int(h[i:i+2], 16) for i in (0, 2, 4)], float)
GRASS = [hexrgb('#36A13D'), hexrgb('#259D39')]
TUFT = hexrgb('#0F3A14')
TOL_GRASS, TOL_TUFT = 12, 18   # flat SVG fills: 12 keeps canopy #489B3B (18 off #36A13D) out of the grass
BAND_MIN_PT2 = 9000       # visible grass area (pt^2) below which a band is too small to expect tufts (thumbnail corners, slivers)
DIMS = [round(1 - .05*i, 2) for i in range(13)]
def near(a, cols, tol):
    m = np.zeros(a.shape[:2], bool)
    for c in cols: m |= (np.abs(a - c) <= tol).all(axis=2)
    return m
def dim_level(a):   # tight match (4 per channel) so an undimmed scene is not read as x0.95
    cnt = {k: int(near(a, [c*k for c in GRASS], 4).sum()) for k in DIMS}
    best = max(DIMS, key=lambda k: cnt[k])
    return 1.0 if cnt[1.0] >= .8 * cnt[best] else best
def label(m, maxn=20000):   # 4-connected components of a (sparse or small) mask -> list of (ys, xs)
    lab = np.zeros(m.shape, np.int32); out = []; H, W = m.shape
    for y0, x0 in zip(*np.nonzero(m)):
        if lab[y0, x0]: continue
        k = len(out) + 1; st = [(y0, x0)]; lab[y0, x0] = k; ys = []; xs = []
        while st:
            y, x = st.pop(); ys.append(y); xs.append(x)
            for v, u in ((y+1, x), (y-1, x), (y, x+1), (y, x-1)):
                if 0 <= v < H and 0 <= u < W and m[v, u] and not lab[v, u]: lab[v, u] = k; st.append((v, u))
        out.append((np.array(ys), np.array(xs)))
        if len(out) >= maxn: break
    return out
def runlen(m, axis):   # length of the True run each pixel belongs to, along axis; runs touching the border get a huge length
    if axis == 0: return runlen(m.T, 1).T
    H, W = m.shape; out = np.zeros(m.shape, np.int32)
    p = np.zeros((H, W + 2), bool); p[:, 1:-1] = m
    d = np.diff(p.astype(np.int8), axis=1)
    for y in np.nonzero(m.any(axis=1))[0]:
        s = np.nonzero(d[y] == 1)[0]; e = np.nonzero(d[y] == -1)[0]
        for a0, b0 in zip(s, e):
            out[y, a0:b0] = (b0 - a0) if (a0 > 0 and b0 < W) else 10**6
    return out
def bands(grass, blk=8):
    H, W = grass.shape; h, w = H // blk, W // blk
    g = grass[:h*blk, :w*blk].reshape(h, blk, w, blk).mean(axis=(1, 3)) > .5
    for ys, xs in label(g):
        y0, y1, x0, x1 = ys.min()*blk, (ys.max()+1)*blk, xs.min()*blk, (xs.max()+1)*blk
        yield (y0, y1, x0, x1), len(ys)*blk*blk
def check(path):
    a = np.asarray(Image.open(path).convert('RGB'), float)
    k = dim_level(a); why = []
    grass = near(a, [c*k for c in GRASS], TOL_GRASS*k)
    tuftc = near(a, [TUFT*k], max(8, TOL_TUFT*k))
    tag = f' [dimmed x{k}]' if k < 1 else ''
    Hh, Ww = grass.shape; phone = 1.4 <= Hh / Ww <= 2.4 and Ww <= 900   # a single phone render (<= 3x of 300 pt): scale = width / 390 pt; wider = a sheet
    small_t = (a[..., 1] - a[..., 0] >= 25*k) & (a[..., 1] - a[..., 2] >= 20*k) & (a[..., 1] <= 110*k) & (a[..., 0] <= 60*k)   # dark tuft green, any blend (ink #10170F and canopy #28792D fall outside)
    for (y0, y1, x0, x1), area in bands(grass):
        if x1 - x0 < (.2 * Ww if phone else 60): continue   # tree crowns and slivers, not a ground band
        s = Ww / 390.0 if phone else (x1 - x0) / 390.0   # sheets: a band spans about one tile width
        sr = s
        if area < BAND_MIN_PT2 * sr * sr or (y1 - y0) < 30 * sr: continue
        G = grass[y0:y1, x0:x1]; T = tuftc[y0:y1, x0:x1]; A = a[y0:y1, x0:x1]
        # tufts: thin upright #0F3A14 strokes, grouped side by side
        strokes = []
        for ys, xs in label(T):
            h = ys.max() - ys.min() + 1; w = xs.max() - xs.min() + 1
            if 5*s <= h <= 22*s and w <= 5*s and h >= 1.8*w: strokes.append((xs.mean(), ys.max(), h))
        strokes.sort(); tufts = []; used = set()
        for i, (xi, bi, hi) in enumerate(strokes):
            if i in used: continue
            grp = [i] + [j for j, (xj, bj, hj) in enumerate(strokes) if j > i and j not in used and abs(xj - xi) <= 14*s and abs(bj - bi) <= 5*s]
            if len(grp) >= 2: used.update(grp); tufts.append((int(xi) + x0, int(bi) + y0))
        # rock dots: small round non-grass blobs ringed by grass (runs end in grass on all four sides)
        ng = ~G; dmax = int(round(14*s)); dmin = 4*s
        small = ng & (runlen(ng, 1) <= dmax) & (runlen(ng, 0) <= dmax)
        rocks = []
        for ys, xs in label(small):
            h = ys.max() - ys.min() + 1; w = xs.max() - xs.min() + 1
            if max(h, w) < dmin or max(h, w) > dmax or max(h, w) > 1.6*min(h, w) or len(ys) < .55*h*w: continue
            if T[ys, xs].mean() > .5: continue   # a tuft stroke bundle, not a rock
            col = A[ys, xs].mean(axis=0)
            if col[1] > col[0] + 25 and col[1] > col[2] + 25: continue   # green blob (canopy, shade), not a rock or dot
            ry0, ry1, rx0, rx1 = max(0, ys.min()-2), min(G.shape[0], ys.max()+3), max(0, xs.min()-2), min(G.shape[1], xs.max()+3)
            box = G[ry0:ry1, rx0:rx1]; ring = np.concatenate([box[:2].ravel(), box[-2:].ravel(), box[:, :2].ravel(), box[:, -2:].ravel()])
            sides = [box[:2].mean(), box[-2:].mean(), box[:, :2].mean(), box[:, -2:].mean()]
            if ring.mean() < .90 or min(sides) < .80: continue   # t545u: only a dot on grass; any non-grass side (dirt, path, sand) = leave it
            rocks.append((int(xs.mean()) + x0, int(ys.mean()) + y0, int(max(h, w))))
        if not tufts and s < .7:
            GN = (A[..., 1] - A[..., 0] >= 25*k) & (A[..., 1] - A[..., 2] >= 20*k)   # grass or a grass/tuft blend (an ink edge is not)   # sheet thumbnails: a tuft is a 1-2 px dark-green fleck; accept any fleck cluster on grass
            for ys, xs in label(small_t[y0:y1, x0:x1]):
                if len(ys) < 3 or ys.max() - ys.min() > 12 or xs.max() - xs.min() > 12: continue
                by0, by1, bx0, bx1 = max(0, ys.min()-2), min(G.shape[0], ys.max()+3), max(0, xs.min()-2), min(G.shape[1], xs.max()+3)
                box = GN[by0:by1, bx0:bx1]; ring = np.concatenate([box[:2].ravel(), box[-2:].ravel(), box[:, :2].ravel(), box[:, -2:].ravel()])
                if ring.mean() >= .99: tufts.append((int(xs.mean()) + x0, int(ys.mean()) + y0)); break   # a free-standing fleck in open grass, not an anti-aliased outline edge
        loc = f'band x{x0}-{x1} y{y0}-{y1}'
        if rocks: why.append(f'rock dot: {len(rocks)} round blob(s) on grass, e.g. ' + ', '.join(f'({x},{y}) {d}px' for x, y, d in rocks[:4]) + f' in {loc}{tag}')
        if not tufts: why.append(f'ASK bare grass: no tufts in {loc} ({area} px grass, s {s:.2f}){tag}')
    return why
def is_image(p):
    try: h = open(p, 'rb').read(12)
    except OSError: return False
    return h.startswith(b'\x89PNG') or h.startswith(b'\xff\xd8\xff') or h.startswith(b'GIF8') or (h[:4] == b'RIFF' and h[8:12] == b'WEBP')
def md5(p): return hashlib.md5(open(p, 'rb').read()).hexdigest()
def run(folder):
    print(f'tuft_check {md5(os.path.abspath(__file__))} | folder {os.path.abspath(folder)}')
    files = sorted(f for f in glob.glob(os.path.join(folder, '**', '*'), recursive=True) if os.path.isfile(f) and is_image(f)); nb = 0; na = 0
    for f in files:
        why = check(f); blk = any(w.startswith('rock') for w in why); nb += blk; na += bool(why) and not blk
        print(f"{os.path.relpath(f, folder)}  {md5(f)}  {'BLOCK' if blk else ('ASK' if why else 'PASS')}" + (' | ' + ' ; '.join(why) if why else ''), flush=True)
    print(f'summary: {len(files)} images, {nb} BLOCK, {na} ASK, {len(files)-nb-na} PASS'); return 2 if nb else 0
TUFTS_W24 = [(60, 532), (24, 604), (374, 604)]   # stage_v608.py:99 W24-walk-B
def selftest():
    src = '/workspace/v608build/scenes/stage/png/W24-walk-B-390x844.png'   # tile 16, approved (t441u): tufts, grounded trees
    d = os.path.join(HERE, 'selftest'); os.makedirs(d, exist_ok=True)
    im = Image.open(src).convert('RGB'); s = im.width / 390
    clean = im.copy(); clean.save(os.path.join(d, 'w24-clean.png'))
    a = np.asarray(im).copy(); g = near(a.astype(float), GRASS, TOL_GRASS)
    for x, y in TUFTS_W24:   # (a) tufts removed: every non-grass pixel in the tuft box becomes near grass
        y0, y1, x0, x1 = int((y-17)*s), int((y+3)*s), int((x-10)*s), int((x+10)*s)
        box = a[y0:y1, x0:x1]; box[~g[y0:y1, x0:x1]] = (0x36, 0xA1, 0x3D)
    bare = Image.fromarray(a); bare.save(os.path.join(d, 'w24-no-tufts.png'))
    rock = bare.copy(); dr = ImageDraw.Draw(rock)   # (b) the old dots / pebbles where the tufts were
    for (x, y), c in zip(TUFTS_W24, ('#FFE27A', '#F2A0A8', '#9A968C')):
        r = 3*s if c != '#9A968C' else 5*s
        dr.ellipse((x*s - r, (y-4)*s - r, x*s + r, (y-4)*s + r), fill=c, outline='#10170F', width=max(1, int(1.5*s)))
    rock.save(os.path.join(d, 'w24-rock-dots.png'))
    mix = clean.copy(); dr = ImageDraw.Draw(mix)   # (c) tufts kept, one grey rock added on open grass left of the hero (32, 556 pt)
    dr.ellipse((32*s - 5*s, 556*s - 5*s, 32*s + 5*s, 556*s + 5*s), fill='#9A968C', outline='#10170F', width=max(1, int(1.5*s)))
    mix.save(os.path.join(d, 'w24-tufts-plus-rock.png'))
    dirt = clean.copy(); dr = ImageDraw.Draw(dirt)   # (d) t545u: a dirt patch with pebbles on it, and a pebble on the dirt edge -> must PASS
    dr.ellipse((150*s, 640*s, 260*s, 690*s), fill='#C8A26B')
    for (x, y, c) in ((180, 665, '#9A968C'), (215, 660, '#FFE27A'), (240, 668, '#F2A0A8'), (152, 665, '#9A968C')):
        dr.ellipse((x*s - 4*s, y*s - 4*s, x*s + 4*s, y*s + 4*s), fill=c, outline='#10170F', width=max(1, int(1.5*s)))
    dirt.save(os.path.join(d, 'w24-pebbles-on-dirt.png'))
    edge = clean.copy(); dr = ImageDraw.Draw(edge)   # (f) a pebble resting on a thin dirt path edge (dirt under one side only) -> must PASS
    dr.ellipse((28*s, 552*s, 36*s, 560*s), fill='#9A968C', outline='#10170F', width=max(1, int(1.5*s)))   # same pebble as (c), 32,556 pt
    dr.rectangle((31*s, 560.5*s, 50*s, 562.5*s), fill='#C8A26B')   # dirt path edge under its bottom-right; b19579ac BLOCKed this, t545u leaves it
    edge.save(os.path.join(d, 'w24-pebble-on-path-edge.png'))
    both = dirt.copy(); dr = ImageDraw.Draw(both)   # (e) pebbles on dirt kept AND one dot on open grass -> rock (only the grass one)
    dr.ellipse((32*s - 5*s, 556*s - 5*s, 32*s + 5*s, 556*s + 5*s), fill='#9A968C', outline='#10170F', width=max(1, int(1.5*s)))
    both.save(os.path.join(d, 'w24-dirt-plus-grass-dot.png'))
    for n, src_im in (('w24-dim70-clean.png', clean), ('w24-dim70-no-tufts.png', bare)):
        Image.fromarray(np.clip(np.asarray(src_im, float)*.7, 0, 255).round().astype(np.uint8)).save(os.path.join(d, n))
    for n, src_im in (('w24-thumb35-clean.png', clean), ('w24-thumb35-no-tufts.png', bare)):   # sheet-thumbnail scale (s .35, as on r2h-before-after)
        src_im.resize((136, 295), Image.LANCZOS).save(os.path.join(d, n))
    want = {'w24-thumb35-clean.png': None, 'w24-thumb35-no-tufts.png': 'ASK bare', 'w24-clean.png': None, 'w24-dim70-clean.png': None, 'w24-no-tufts.png': 'ASK bare', 'w24-rock-dots.png': 'rock',
            'w24-tufts-plus-rock.png': 'rock', 'w24-dim70-no-tufts.png': 'ASK bare', 'w24-pebbles-on-dirt.png': None, 'w24-pebble-on-path-edge.png': None, 'w24-dirt-plus-grass-dot.png': 'rock'}
    extra = {f'/workspace/v608build/scenes/stage/png/W24-walk-B-{z}.png': None for z in ('375x667', '320x568')}
    extra['/workspace/v608build/scenes/stage/png/B-meadow-listen-and-find-390x844.png'] = None
    ok = True; lines = []
    for n, w in list(want.items()) + list(extra.items()):
        p = n if n.startswith('/') else os.path.join(d, n); r = check(p)
        good = (not r) if w is None else any(x.startswith(w) for x in r); ok &= good
        lines.append(f"  {'ok ' if good else 'BAD'} {os.path.basename(p)}  {md5(p)}  {('BLOCK' if any(x.startswith('rock') for x in r) else 'ASK') if r else 'PASS'}" + (' | ' + ' ; '.join(r) if r else '') + f"  (want {'PASS' if w is None else w})")
    print(f'tuft_check {md5(os.path.abspath(__file__))} selftest ' + ('PASS' if ok else 'FAIL') + f' | src {md5(src)} | scratch {d}')
    print('\n'.join(lines)); return 0 if ok else 2
if __name__ == '__main__':
    if sys.argv[1:2] == ['--selftest']: sys.exit(selftest())
    if len(sys.argv) < 2: print('usage: tuft_check.py FOLDER|FILE [...] | --selftest'); sys.exit(1)
    rc = 0
    for f in sys.argv[1:]:
        if os.path.isfile(f):
            w = check(f); b = any(x.startswith('rock') for x in w)
            print(f"{f}  {'BLOCK' if b else ('ASK' if w else 'PASS')}" + (' | ' + ' ; '.join(w) if w else '')); rc = max(rc, 2 if b else 0)
        else: rc = max(rc, run(f))
    sys.exit(rc)
