# Shared sheet maker (round2b): tan parchment, Maxwell style. Tiles at true pt size (a 320 phone is drawn smaller than a 390 one).
from PIL import Image, ImageDraw, ImageFont
import textwrap
B = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'; R = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
F = lambda s, b=True: ImageFont.truetype(B if b else R, s)
INK, RED, GOLD, BG = '#3A2410', '#7A1E12', '#B8860B', '#F4ECD8'
def wrap(d, x, y, text, font, width, fill=INK, gap=4):
    for para in text.split('\n'):
        for line in textwrap.wrap(para, width) or ['']:
            d.text((x, y), line, fill=fill, font=font); y += font.size + gap
    return y
def sheet(out, title, question, tiles, footer, cols=None, tag=None):
    """tiles: [(num, caption, png, (w, h))]; num is a big label ('1', '1A' ...) or None. Rows of `cols` tiles."""
    import sys as _s; _s.path.insert(0, '/workspace/v608build/round2/asset-depth'); import round_totals as _RT; _l = _RT.for_sheet(out)   # Chancellor 8:20 PM MDT: round total on every pick sheet
    if _l: footer = footer + ' ' + _l
    cols = cols or len(tiles); rows = [tiles[i:i + cols] for i in range(0, len(tiles), cols)]
    colw = max(t[3][0] for t in tiles) + 30; rowh = [max(t[3][1] for t in r) + 190 for r in rows]
    W = 30 + cols * colw; H = 150 + sum(rowh) + 40 + 22 * (1 + len(footer) // 110 + footer.count('\n'))
    S = Image.new('RGB', (max(W, 900), H), BG); d = ImageDraw.Draw(S)
    y = wrap(d, 30, 16, title, F(24), 90); y = wrap(d, 30, y + 4, question, F(18), 110, RED) + 10
    for r, rh in zip(rows, rowh):
        for i, (num, cap, png, (w, h)) in enumerate(r):
            x = 30 + i * colw
            if num:
                d.rounded_rectangle((x, y, x + 64 + 16 * (len(num) - 1), y + 50), 10, fill=INK); d.text((x + 12, y + 6), num, fill='#FFF8E1', font=F(34))
            wrap(d, x + (90 + 16 * (len(num) - 1) if num else 0), y + 2, cap, F(14, False), 36 if num else 44)
            im = Image.open(png).convert('RGB').resize((w, h), Image.LANCZOS)
            S.paste(im, (x, y + 150)); d.rectangle((x - 1, y + 149, x + w, y + 150 + h), outline=GOLD, width=2)
        y += rh
    wrap(d, 30, y, footer, F(14, False), 150)
    S.save(out); return out
import re, os, sys, hashlib
def r2tp(html, w, h, outdir='/workspace/v608build/round2/sheets/r2tp/'):
    """the staged round 2 ask (t440u) on a render: 'Can you find the …?' / 'หา … เจอไหม' (sheet copies only; the source render is untouched)"""
    sys.path.insert(0, '/workspace/v608build/scenes'); sys.path.insert(0, '/workspace/v608build/screens')
    import stage_v608 as ST
    d = open(html).read()
    d2 = re.sub(r'Where is the ([a-z]+)\?', r'Can you find the \1?', d); d2 = re.sub(r'([a-z]+) อยู่ที่ไหน', r'หา \1 เจอไหม', d2)
    os.makedirs(outdir, exist_ok=True); b = os.path.basename(os.path.dirname(os.path.dirname(html))) + '--' + os.path.basename(html)[:-5]; p = outdir + b + '.png'
    if d2 != d: open(outdir + b + '.html', 'w').write(d2); ST.shot(d2, p, w, h); return p
    return html.replace('/html/', '/png/')[:-5] + '.png'
