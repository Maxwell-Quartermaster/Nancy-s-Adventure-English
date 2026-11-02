# Emoji placement/size decision sheet for screen 12 (reveal, ph-07 hug) at 390: current | A | B | C. Pictures are intentional (framed plate or object-sized prop), never over or beside Sam.
import sys; sys.path.insert(0, '/workspace/v608build/screens'); sys.argv = ['x']
import play_v608 as P
from PIL import Image, ImageDraw, ImageFont
c = P.C['ph-07']; e = P.D['encouragement'][0]
def plate(x, y, sz, fs):
    return (f"<div class='abs' style='left:{x}px;top:{y}px;width:{sz}px;height:{sz}px;display:flex;align-items:center;justify-content:center;box-sizing:border-box;background:#F6E9C8;border:3px solid #10170F;border-radius:18px;box-shadow:inset 0 0 0 3px #E8B84A,0 3px 0 #10170F;font:400 {fs}px/1 sans-serif'>{c['pic']}</div>")
def scr(pic='', in_card=False):
    b, g = P.base('meadow', 'cheer', hide=('kite',))
    word = [P.tx(c['en'].upper(), 'e22'), P.tx(c['th'], 't17 nw'), P.tx(c['respell'], 'e15')]
    if in_card: word = [f"<div style='display:flex;align-items:center;justify-content:center;gap:12px'><div style='width:72px;height:72px;flex:none;display:flex;align-items:center;justify-content:center;box-sizing:border-box;background:#FFF8E1;border:3px solid #10170F;border-radius:14px;box-shadow:inset 0 0 0 2px #E8B84A;font:400 44px/1 sans-serif'>{c['pic']}</div><div style='text-align:left'>{''.join(word)}</div></div>"]
    return P.page(390, 844, b + pic + P.top('meadow', 65, .68) + P.ribbon(e['en'], e['th']) + P.card(word, 190 if not in_card else 200,
                  [P.gbtn(*P.u('replay'), 110), P.gbtn(*P.u('sayItOutLoud'), 150), P.gbtn(*P.D['gotItText'].values(), 100)]))
OPT = [('now', 'Now (v6-08): 112 px emoji, no frame, left of Sam', scr(P.big(c['pic'], 30, 220, 112))),
       ('A', 'A: framed plate 124 px (same plate as 17-19), top right, clear of Sam', scr(plate(246, 218, 124, 76))),
       ('B', 'B: small framed picture inside the card, next to the word', scr('', True)),
       ('C', 'C: object-sized prop (64 px) on the grass, with a shadow', scr(P.big(c['pic'], 262, 452, 64)))]
for k, t, doc in OPT: open(f'emoji12-{k}.html', 'w').write(doc); P.S.shot(doc, f'emoji12-{k}.png', 390, 844, 'e12' + k)
F = lambda s: ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', s)
S = Image.new('RGB', (20 + 4*410, 844 + 130), '#F4ECD8'); d = ImageDraw.Draw(S)
d.text((20, 12), 'Screen 12 (reveal "hug") at 390: where the picture goes and how big', fill='#3A2410', font=F(22))
d.text((20, 44), 'Which picture placement for screen 12: now, A, B or C?', fill='#7A1E12', font=F(17))
for i, (k, t, _) in enumerate(OPT):
    d.text((20 + i*410, 80), t if len(t) < 48 else t[:t.rfind(' ', 0, 48)], fill='#3A2410', font=F(13))
    if len(t) >= 48: d.text((20 + i*410, 96), t[t.rfind(' ', 0, 48)+1:], fill='#3A2410', font=F(13))
    S.paste(Image.open(f'emoji12-{k}.png').convert('RGB').resize((390, 844)), (20 + i*410, 116))
S.save('emoji12-now-A-B-C-390.png'); print('ok')
