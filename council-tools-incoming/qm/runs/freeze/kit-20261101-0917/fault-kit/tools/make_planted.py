#!/usr/bin/env python3
"""Auditor fault kit: build the planted images for the tuft_check cases and the ground_check multi-panel cases (kit v1.1).
Deterministic; reads only kit copies (cases/*/src, cases/ground_check/sheets); writes only into the kit's cases/ dirs."""
import os, sys
import numpy as np
from PIL import Image, ImageDraw
K = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, f'{K}/cases/ground_check'); import panels
hexrgb = lambda h: np.array([int(h.lstrip('#')[i:i+2], 16) for i in (0, 2, 4)], float)
GRASS = [hexrgb('#36A13D'), hexrgb('#259D39')]
def grassmask(a, tol=12):
    m = np.zeros(a.shape[:2], bool)
    for c in GRASS: m |= (np.abs(a - c) <= tol).all(axis=2)
    return m
# ---- tuft_check: base = approved tile 16 / W24 (t441u), the same source as Watchman's selftest
src = Image.open(f'{K}/cases/tuft_check/src/W24-walk-B-390x844.png').convert('RGB'); s = src.width / 390; g = grassmask(np.asarray(src, float))
def on_grass(x, y, r):   # (x, y, r) in pt: the whole box around the mark is grass in the clean image
    X, Y, R = int(x * s), int(y * s), int(r * s); return bool(g[Y - R:Y + R, X - R:X + R].all())
def dot(dr, x, y, r, fill): dr.ellipse((x*s - r*s, y*s - r*s, x*s + r*s, y*s + r*s), fill=fill, outline='#10170F', width=max(1, int(1.5*s)))
T = f'{K}/cases/tuft_check/images'; checks = {}
src.save(f'{T}/U01-clean.png')
im = src.copy(); dot(ImageDraw.Draw(im), 110, 515, 3, '#FFE27A'); im.save(f'{T}/U02-circle-dot-on-grass.png'); checks['U02 dot box on grass'] = on_grass(110, 515, 6)
im = src.copy(); dr = ImageDraw.Draw(im); dr.ellipse((55*s, 548*s, 110*s, 582*s), fill='#A47B4F'); dot(dr, 83, 565, 4, '#9A968C'); im.save(f'{T}/U03-pebble-on-dirt.png'); checks['U03 dirt patch area >= 75% grass'] = g[int(548*s):int(582*s), int(55*s):int(110*s)].mean() >= .75
im = src.copy(); dr = ImageDraw.Draw(im); dr.rectangle((40*s, 588*s, 140*s, 612*s), fill='#EAD7A0'); dot(dr, 90, 600, 4, '#9A968C'); im.save(f'{T}/U04-pebble-on-sand-strip.png'); checks['U04 strip area was grass'] = on_grass(90, 600, 11)
im = src.copy(); dr = ImageDraw.Draw(im); dr.ellipse((55*s, 548*s, 110*s, 582*s), fill='#A47B4F'); dot(dr, 55, 565, 4, '#9A968C'); im.save(f'{T}/U05-dot-on-grass-dirt-edge.png')
im = src.copy(); dr = ImageDraw.Draw(im); dr.ellipse((55*s, 548*s, 110*s, 582*s), fill='#A47B4F'); dot(dr, 83, 565, 4, '#9A968C'); dot(dr, 110, 515, 3, '#FFE27A'); im.save(f'{T}/U06-pebble-on-dirt-plus-dot-on-grass.png')
# ---- ground_check multi-panel: true positive = old path stroke painted on the grass of panel 1 (Midday) of the real S01 sheet only
G = f'{K}/cases/ground_check'; sheet, boxes = panels.split(f'{G}/sheets/S01-park-390x844.png'); x0, y0, x1, y1 = boxes[0]
a = np.asarray(sheet, float).copy(); pg = np.zeros(a.shape[:2], bool); sub = a[y0:y1, x0:x1]; pg[y0:y1, x0:x1] = grassmask(sub, 22) | (np.abs(sub - hexrgb('#56B05C')).max(axis=2) <= 14)   # scene-fill grass renders as ~#56B05C on these sheets
gy = np.nonzero(pg[:, x0:x1].sum(1) > 40)[0]; lo, hi = gy.min(), gy.max()
m = Image.new('L', sheet.size, 0); dr = ImageDraw.Draw(m); w = x1 - x0
pts = [((1-t)**2*(x0+.25*w) + 2*t*(1-t)*(x0+.35*w) + t*t*(x0+.6*w), (1-t)**2*(hi+20) + 2*t*(1-t)*((lo+hi)/2) + t*t*(lo-5)) for t in [i/40 for i in range(41)]]
dr.line(pts, fill=255, width=max(8, int(26 * w / 390)))   # 26 pt wide at panel scale, as planted.py
mk = (np.asarray(m) > 0) & pg; a[mk] = 0.85 * hexrgb('#E8D9A8') + 0.15 * hexrgb('#36A13D')
Image.fromarray(a.round().astype(np.uint8)).save(f'{G}/sheets/S01-path-in-panel1.png'); checks[f'S01 panel-1 stroke px painted ({int(mk.sum())}) > 300'] = int(mk.sum()) > 300
for k, v in checks.items(): print(('ok  ' if v else 'BAD ') + k)
sys.exit(0 if all(checks.values()) else 1)
