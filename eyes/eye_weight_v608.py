# Eye-weight pick for Maxwell: A = Nancy's exact arcs (v6-08 now), B = darker, thicker arc (stroke 2.2, Ink, round caps). Screens 10 and 39 at 390.
import sys, json; sys.path.insert(0, '/workspace/v606build'); sys.path.insert(0, '/workspace/v608build/eyes')
from render_title_v606 import shot
from PIL import Image, ImageChops, ImageDraw, ImageFont
import eyes_v608 as EY
F = lambda s: ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', s)
THICK = "<path d='M32.8 21.4q2.2-3.2 4.4 0M42.8 21.4q2.2-3.2 4.4 0' stroke='#10170F' stroke-width='2.2' fill='none' stroke-linecap='round'/>"
M = json.load(open('eyes-manifest.json')); rows = []
for b in ('10-word-meadow-scene', '39-character-gear-rows'):
    src = open(M[b]['src'], encoding='utf-8').read(); a, _ = EY.apply(src); bb = a.replace(EY.NANCY, THICK)
    pa, pb = '/tmp/ew-%s-A.png' % b[:2], '/tmp/ew-%s-B.png' % b[:2]
    shot(a, pa, 390, 844); shot(bb, pb, 390, 844)
    A, B = Image.open(pa).convert('RGB'), Image.open(pb).convert('RGB'); x0, y0, x1, y1 = ImageChops.difference(A, B).getbbox()
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2; box = (cx - 70, cy - 56, cx + 70, cy + 56)
    rows.append((b, A, B, A.crop(box).resize((420, 336), Image.LANCZOS), B.crop(box).resize((420, 336), Image.LANCZOS)))
W = 20 + 2 * 400 + 2 * 440 + 30; H = 70 + len(rows) * 900
S = Image.new('RGB', (W, H), '#F4ECD8'); d = ImageDraw.Draw(S)
d.text((20, 14), "Sam's eyes: A = Nancy's exact arcs (now in v6-08)   B = darker, thicker arc", fill='#3A2410', font=F(24))
d.text((20, 44), 'Which eyes for Sam: A or B?', fill='#7A1E12', font=F(18))
for i, (b, A, B, ca, cb) in enumerate(rows):
    y = 80 + i * 900
    d.text((20, y), 'A  ' + b, fill='#3A2410', font=F(16)); S.paste(A.resize((390, 844)), (20, y + 24))
    d.text((420, y), 'B  ' + b, fill='#3A2410', font=F(16)); S.paste(B.resize((390, 844)), (420, y + 24))
    d.text((830, y), 'A zoom', fill='#3A2410', font=F(16)); S.paste(ca, (830, y + 24))
    d.text((830, y + 380), 'B zoom', fill='#3A2410', font=F(16)); S.paste(cb, (830, y + 404))
S.save('eye-weight-A-B.png'); print(S.size)
