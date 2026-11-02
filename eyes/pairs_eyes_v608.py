import json, os
from PIL import Image, ImageChops, ImageDraw, ImageFont
F = lambda s: ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', s)
M = json.load(open('eyes-manifest.json'))
tiles = []
for b, v in sorted(M.items()):
    if not v['png']: continue
    before = v['before']   # the same html, unmodified, re-shot with the same shot()
    A = Image.open(before).convert('RGB'); B = Image.open(v['png']).convert('RGB')
    bb = ImageChops.difference(A, B).getbbox()
    if not bb: print('NO DIFF', b); continue
    regs = []   # split into separate figures when the changed areas are far apart
    d = ImageChops.difference(A, B).convert('L').point(lambda x: 255 if x > 8 else 0)
    cols = [x for x in range(d.size[0]) if d.crop((x, 0, x + 1, d.size[1])).getbbox()]
    groups = []; 
    for x in cols:
        if groups and x - groups[-1][1] < 60: groups[-1][1] = x
        else: groups.append([x, x])
    for g0, g1 in groups:
        sb = d.crop((g0, 0, g1 + 1, d.size[1])).getbbox(); regs.append((g0, sb[1], g1 + 1, sb[3]))
    crops = []
    for (x0, y0, x1, y1) in regs:
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2; r = max(70, (x1 - x0) * 1.6, (y1 - y0) * 2.4)
        box = (int(cx - r), int(cy - r * .8), int(cx + r), int(cy + r * .8))
        a = A.crop(box).resize((300, 240), Image.LANCZOS); bb_ = B.crop(box).resize((300, 240), Image.LANCZOS)
        crops.append((a, bb_))
    W = 20 + len(crops) * 640; t = Image.new('RGB', (W, 300), '#F4ECD8'); dr = ImageDraw.Draw(t)
    dr.text((10, 6), b + ('  (Sam + guardian, same rig)' if len(crops) > 1 else ''), fill='#3A2410', font=F(18))
    for i, (a, bb_) in enumerate(crops):
        x = 10 + i * 640; dr.text((x, 34), 'before', fill='#3A2410', font=F(15)); dr.text((x + 310, 34), 'after', fill='#3A2410', font=F(15))
        t.paste(a, (x, 56)); t.paste(bb_, (x + 310, 56))
    p = 'pairs/eyes-%s.png' % b; t.save(p); tiles.append(p)
ims = [Image.open(p) for p in tiles]; cols = 3; w = max(i.size[0] for i in ims); h = 300
S = Image.new('RGB', (cols * (w + 10) + 10, ((len(ims) + cols - 1) // cols) * (h + 10) + 70), 'white'); dr = ImageDraw.Draw(S)
dr.text((10, 14), "Happy eyes (Maxwell t408u): every Sam figure uses Nancy's eyes exactly (her arcs, stroke 1.6, Ink) - before | after crops (390x844; -320x568 rows at 320; sv- = scene-variety mocks)", fill='#3A2410', font=F(22))
for i, im in enumerate(ims): S.paste(im, (10 + (i % cols) * (w + 10), 60 + (i // cols) * (h + 10)))
S.save('contact-eyes-v608.png'); print(len(tiles), S.size)

# contact sheet of every Sam screen AFTER (full screens)
afters = [v['png'] for b, v in sorted(M.items()) if v['png']]
names = [b for b, v in sorted(M.items()) if v['png']]
th = [Image.open(p).convert('RGB') for p in afters]; th = [i.resize((195, 422) if i.size[0] == 780 else (160, 284)) for i in th]
cols = 8; cw, ch = 205, 450
C = Image.new('RGB', (cols * cw + 10, ((len(th) + cols - 1) // cols) * ch + 60), 'white'); dr = ImageDraw.Draw(C)
dr.text((10, 14), "All Sam screens after (v6-08): Nancy's happy eyes everywhere (t408u)", fill='#3A2410', font=F(22))
for i, (im, nm) in enumerate(zip(th, names)):
    x = 10 + (i % cols) * cw; y = 50 + (i // cols) * ch; C.paste(im, (x, y + 18)); dr.text((x, y), nm[:30], fill='#3A2410', font=F(11))
C.save('contact-all-sam-after-v608.png'); print('after sheet', len(th))
