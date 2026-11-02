# K3 time of day (Auditor gate 1975f0b8): step = 1 + zoneRuns[zone] mod 5, set at run start; 1 morning .. 5 night, then morning again.
# Renders the zone scene at each step for all four zones at 390x844 and 320x568, and one labelled strip per zone and size.
# CSS/var swap only: the title's sky palette + a light tint; props, layout and taps unchanged (same as spec 7.1).
import sys, os
sys.path.insert(0, '/workspace/v608build/screens'); sys.argv = ['x']
import play_v608 as PV
from PIL import Image, ImageDraw, ImageFont
Z = PV.Z; _sky0 = Z.sky
TOD = {1: ('m', ''), 2: ('a', 'rgba(255,255,255,.10)'), 3: ('a', 'rgba(255,190,110,.08)'), 4: ('e', 'rgba(255,130,60,.16)'), 5: ('n', 'rgba(11,27,51,.45)')}
SUN = {'m': (-170, 120), 'a': (-20, -30), 'e': (60, 70), 'n': (0, 0)}
OUT = '/workspace/v608build/scenes/tod/'
def doc(key, step, w, h):
    tod, tint = TOD[step]
    sun = SUN[tod] if tod not in 'ae' or key == 'fields' else (-170, 120)   # keep the sun clear of the kite, owl and window targets
    Z.sky = lambda w_, h_, t_, s_: _sky0(w_, h_, tod, sun if w_ > 320 else (sun[0] * .6, sun[1] * .6))
    try: body = Z.screen(key, 'ask', w, h)
    finally: Z.sky = _sky0
    if tint:
        i = body.index("<div class='abs'", body.index('data-name') - 400) if False else None
        ov = f"<div class='abs' style='left:0;top:0;width:{w}px;height:{h}px;background:{tint};pointer-events:none'></div>"
        # tint the scene, not the HUD or card: insert before the top bar (hud16 starts with the Back plate)
        k = body.index("data-name='back'"); k = body.rindex('<div', 0, k)
        body = body[:k] + ov + body[k:]
    return PV.page(w, h, body)
if __name__ == '__main__':
    font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 22)
    for key in ('meadow', 'fields', 'lake', 'forest'):
        for (w, h, suf) in ((390, 844, '390'), (320, 568, '320x568')):
            ims = []
            for st in range(1, 6):
                d = doc(key, st, w, h); n = f'{key}-step{st}-{suf}'
                open(OUT + n + '.html', 'w').write(d); PV.S.shot(d, OUT + n + '.png', w, h, 'tod-' + n); ims.append(Image.open(OUT + n + '.png').convert('RGB').resize((w, h)))
            names = ['1 morning', '2 day', '3 afternoon', '4 evening', '5 night']
            S = Image.new('RGB', (5 * (w + 10) + 10, h + 90), '#F6E9C8'); dr = ImageDraw.Draw(S)
            dr.text((10, 8), f'{key}: time of day by zone step = 1 + zoneRuns[{key}] mod 5 (K3), set at run start; run 6 is morning again', fill='#3A2410', font=font)
            for i, im in enumerate(ims): S.paste(im, (10 + i * (w + 10), 80)); dr.text((14 + i * (w + 10), 46), f'step {names[i]}', fill='#3A2410', font=font)
            S.save(OUT + f'strip-{key}-steps-{suf}.png'); print(key, suf, flush=True)
