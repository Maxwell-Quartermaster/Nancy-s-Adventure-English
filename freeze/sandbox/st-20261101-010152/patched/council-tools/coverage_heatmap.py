# Heatmap of attention per game area (reads coverage-data.json). Maxwell t461u, QM-relayed.
import json, math
from PIL import Image, ImageDraw, ImageFont
D = json.load(open('/workspace/council-tools/coverage-data.json'))
R = D['rows']
COLS = [('renders', 'Renders'), ('nsz', 'Sizes'), ('files', 'Reports'), ('checks', 'Checks'), ('walked', 'Walks'), ('shown', 'Shown')]
for r in R: r['nsz'] = len(r['sizes'])
mx = {k: max(r[k] for r in R) or 1 for k, _ in COLS}
def norm(k, v): return math.log1p(v) / math.log1p(mx[k])
for r in R: r['score'] = sum(norm(k, r[k]) for k, _ in COLS) / len(COLS)
R.sort(key=lambda r: r['score'])
F = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'; FB = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
f = ImageFont.truetype(F, 30); fb = ImageFont.truetype(FB, 30); fs = ImageFont.truetype(F, 24); ft = ImageFont.truetype(FB, 40)
W, RH, NW, CW, TOP = 1170, 62, 600, 95, 200
H = TOP + RH * len(R) + 230
im = Image.new('RGB', (W, H), (243, 231, 205)); d = ImageDraw.Draw(im)
d.text((30, 26), "Nancy's game: attention by area", font=ft, fill=(60, 40, 20))
d.text((30, 80), 'snap-r2d-2233MDT · 31 Oct 2026 · #1 = least attention', font=fs, fill=(90, 70, 40))
d.text((30, 112), 'Red = none or almost none, gold = some, green = most', font=fs, fill=(90, 70, 40))
for j, (k, lab) in enumerate(COLS):
    d.text((NW + j * CW + 6, TOP - 46), lab, font=ImageFont.truetype(FB, 21), fill=(60, 40, 20))
def col(t):
    a = [(196, 72, 52), (222, 170, 70), (92, 150, 82)]
    if t < .5: p, q, u = a[0], a[1], t / .5
    else: p, q, u = a[1], a[2], (t - .5) / .5
    return tuple(int(p[i] + (q[i] - p[i]) * u) for i in range(3))
for i, r in enumerate(R):
    y = TOP + i * RH
    if i % 2: d.rectangle([0, y, W, y + RH], fill=(236, 222, 192))
    nm = r['name'] if len(r['name']) <= 30 else r['name'][:29] + '…'
    d.text((20, y + 14), f"{i+1:>2}", font=fb, fill=(60, 40, 20)); d.text((78, y + 14), nm, font=f, fill=(40, 30, 15))
    for j, (k, _) in enumerate(COLS):
        x = NW + j * CW; v = r[k]
        d.rectangle([x + 3, y + 5, x + CW - 3, y + RH - 5], fill=col(norm(k, v)))
        s = str(v); tw = d.textlength(s, font=fb); d.text((x + (CW - tw) / 2, y + 14), s, font=fb, fill=(255, 255, 255))
y = TOP + RH * len(R) + 20
for line in ['Renders: PNGs found for its screens · Sizes: phone sizes rendered (of 4)',
             'Reports: council .md/.txt files that mention it (keyword match, rough)',
             'Checks: check lines in checks_v608.py · Walks: walk/play-flow notes that cover it',
             'Shown: times its screens or name appear on pick sheets, showcase or QUEUE']:
    d.text((30, y), line, font=fs, fill=(70, 50, 25)); y += 36
im.save('/workspace/council-tools/coverage-heatmap.png', optimize=True)
json.dump([(i + 1, r['id'], round(r['score'], 2)) for i, r in enumerate(R)], open('/tmp/qmtmp/rank.json', 'w'))
print([(i + 1, r['id'], round(r['score'], 2)) for i, r in enumerate(R)])
