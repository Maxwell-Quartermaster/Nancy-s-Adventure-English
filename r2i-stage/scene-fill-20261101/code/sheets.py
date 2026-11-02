# Numbered pick sheets, grouped by location, <=6 tiles, neutral captions, footer stamp. S14 is INTERNAL (night B) and never goes to Maxwell.
import os, json, hashlib
from PIL import Image, ImageDraw, ImageFont
B = '/workspace/v608build/scene-fill-20261101/'; V = '/workspace/v608build/'
md5 = lambda p: hashlib.md5(open(p, 'rb').read()).hexdigest()
PTR, PASTE = md5(V + 'CURRENT-SNAP.txt'), md5(V + 'r2h-build/nancys-adventure-english-v6-08-1B-v32-PASTE.md')
assert PTR.startswith('f6dac2d0') and PASTE.startswith('317e91ce')
FB = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 26); FS = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 20)
FF = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', 16)
TOD = dict(m='Morning', d='Midday', a='Afternoon', e='Evening', n='Night', base='No tint', sunset='Sunset sky (concept)', starry='Starry sky (concept)')
LOC = {'park': 'Word Meadow · Park', 'pond': 'Word Meadow · Pond', 'home': 'Home Lake · Home room', 'F-kitchen': 'Home Lake · Kitchen meal set',
       'E-front-desk': 'Home Lake · Front desk', 'farm': 'Golden Fields · Farm'}
ORD = 'base m d a e n'.split()
S = []
n = 0
for loc in ('park', 'pond', 'home', 'F-kitchen', 'E-front-desk', 'farm'):
    for sz in ('390x844', '320x568'):
        tags = [f'{loc}-{t}-{sz}' for t in ORD if os.path.exists(B + f'renders/{loc}-{t}-{sz}.png')]
        n += 1; S.append((f'S{n:02d}-{loc.lower()}-{sz}', f'{LOC[loc]} · {sz}', [(t, TOD[t.split("-")[-2]]) for t in tags]))
S.append(('S13-title', 'Title · clock states', [('title-a-390x844', 'Afternoon · 390x844 (no hint card)'), ('title-a-320x568', 'Afternoon · 320x568 (no hint card)'),
          ('title-e-390x844', 'Evening · 390x844'), ('title-e-320x568', 'Evening · 320x568'), ('title-n-A-320x568', 'Night · 320x568 · A')]))
S.append(('S14-INTERNAL-title-night-AB', 'INTERNAL · Title night 320 · A vs B (not for Maxwell)', [('title-n-A-320x568', 'A · "Good night!" (PASTE greetNight)'),
          ('title-n-B-320x568', 'B · "Good evening!" (instructor patch --night)')]))
for k, v in ((15, 'M1'), (16, 'M3')):
    S.append((f'S{k}-menu-{v.lower()}', f'Main menu · {v} layout', [(f'menu-{v}-{t}-{sz}', f'{TOD[t]} · {sz}') for t in 'en' for sz in ('390x844', '320x568')]))
S.append(('S17-rest', 'Rest screen', [('rest-base-320x568', 'Evening sky · 320x568'), ('rest-sunset-390x844', 'Sunset sky (concept) · 390x844'), ('rest-sunset-320x568', 'Sunset sky (concept) · 320x568'),
          ('rest-starry-390x844', 'Starry sky (concept) · 390x844'), ('rest-starry-320x568', 'Starry sky (concept) · 320x568')]))
TW = 300; PAD = 24
def wrap(text, font, width):   # word-wrap to a pixel width (Watchman: captions must not clip or overlap)
    out, line = [], ''
    for w in text.split(' '):
        t = (line + ' ' + w).strip()
        if font.getlength(t) <= width or not line: line = t
        else: out.append(line); line = w
    out.append(line); return out
out = []
for name, title, tiles in S:
    assert 1 <= len(tiles) <= 6, name
    ims = [Image.open(B + f'renders/{t}.png').convert('RGB') for t, _ in tiles]
    ims = [i.resize((TW, round(i.size[1] * TW / i.size[0])), Image.LANCZOS) for i in ims]
    cols = 3 if len(ims) > 4 else len(ims); rows = (len(ims) + cols - 1) // cols; th = max(i.size[1] for i in ims)
    W = PAD + cols * (TW + PAD)
    caps = [wrap(f'{k + 1}. {cap}', FS, TW) for k, (t, cap) in enumerate(tiles)]; CAPH = 14 + 24 * max(len(c) for c in caps)
    TITLE = f'{name.split("-")[0]} · {title}'; tl = wrap(TITLE, FB, W - 2 * PAD); TOP = 22 + 32 * len(tl) + 16
    FOOT = f'snap-r2h-0021MDT · pointer {PTR[:8]} · PASTE {PASTE[:8]} · scene-fill-20261101 (candidate, not frozen)'; foot = wrap(FOOT, FF, W - 2 * PAD)
    H = TOP + rows * (th + CAPH + 10) + 20 + 20 * len(foot) + 20
    sh = Image.new('RGB', (W, H), '#F6E9C8'); d = ImageDraw.Draw(sh)
    d.rectangle([4, 4, W - 5, H - 5], outline='#C9A227', width=4)
    for i, l in enumerate(tl): d.text((PAD, 22 + 32 * i), l, font=FB, fill='#3A2410')
    for k, (im, (t, cap)) in enumerate(zip(ims, tiles)):
        x = PAD + (k % cols) * (TW + PAD); y = TOP + (k // cols) * (th + CAPH + 10)
        sh.paste(im, (x, y)); d.rectangle([x - 1, y - 1, x + TW, y + im.size[1]], outline='#10170F', width=2)
        for i, l in enumerate(caps[k]): d.text((x, y + im.size[1] + 8 + 24 * i), l, font=FS, fill='#3A2410')
    for i, l in enumerate(foot): d.text((PAD, H - 20 - 20 * (len(foot) - i)), l, font=FF, fill='#6B5320')
    p = B + f'sheets/{name}.png'; sh.save(p, optimize=True)
    src = ''.join(f'{md5(q)}  {q}\n' for t, _ in tiles for q in (B + f'renders/{t}.png', B + f'html/{t}.html'))
    src += f'caption {TITLE}\n' + ''.join(f'caption {k + 1}. {cap}\n' for k, (t, cap) in enumerate(tiles)) + f'caption {FOOT}\n'   # exact (unwrapped) drawn text, for text_check caption checks
    for sc in (p + '.sources.txt', p[:-4] + '.sources.txt'):   # text_check reads <img>.sources.txt first, then <stem>.sources.txt; both carry the same lines
        open(sc, 'w').write(src)
    out.append(dict(sheet=os.path.basename(p), md5=md5(p), tiles=[t for t, _ in tiles], internal='INTERNAL' in name))
json.dump(out, open(B + 'sheets/sheets.json', 'w'), indent=1)
for o in out: print(o['md5'], o['sheet'], len(o['tiles']))
