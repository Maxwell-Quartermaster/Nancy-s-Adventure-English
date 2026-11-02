# K3 time of day (Auditor gate 1975f0b8): step = 1 + zoneRuns[zone] mod 5, set at run start; 1 morning .. 5 night, then morning again.
# Renders the zone scene at each step for all four zones at 390x844 and 320x568, and one labelled strip per zone and size.
# CSS/var swap only: the title's sky palette + a light tint; props, layout and taps unchanged (same as spec 7.1).
import sys, os
SE = os.environ.get('NAE_SE') == '1'   # V4: one size per process so Echo Forest can use the Sound Duel screen at that size
sys.path.insert(0, '/workspace/v608build/screens'); sys.argv = ['x']
import play_v608 as PV
from PIL import Image, ImageDraw, ImageFont
Z = PV.Z; _sky0 = Z.sky
# Watchman glitch hunt R7: steps 1-3 must read apart: the sky stops swap per step (1 dawn peach, 2 bright midday, 3 gold afternoon) plus a light tint
STOPS = {1: ('#7FA7DE', '#F9CFA4'), 2: ('#58ABF4', '#F2F8FF'), 3: ('#3F86D9', '#F6D98E')}
TOD = {1: ('m', 'rgba(255,170,110,.12)'), 2: ('a', 'rgba(255,255,255,.16)'), 3: ('a', 'rgba(255,196,80,.16)'), 4: ('e', 'rgba(255,130,60,.16)'), 5: ('n', 'rgba(11,27,51,.45)')}
SUN = {'m': (-170, 120), 'a': (-20, -30), 'e': (60, 70), 'n': (0, 0)}
OUT = '/workspace/v608build/scenes/tod/'
def doc(key, step, w, h): return PV.page(w, h, body(key, step, w, h))
def body(key, step, w, h):
    tod, tint = TOD[step]
    sun = SUN[tod] if tod not in 'ae' or key == 'fields' else (-170, 120)   # keep the sun clear of the kite, owl and window targets
    Z.sky = lambda w_, h_, t_, s_: _sky0(w_, h_, tod, sun if w_ > 320 else (sun[0] * .6, sun[1] * .6))
    # V4 (re-walk): Echo Forest has no find-and-tap zone; its time of day is shown on the Sound Duel screen (scenery not tappable)
    try: body = PV.duel(None) if key == 'forest' else Z.screen(key, 'ask', w, h)
    finally: Z.sky = _sky0
    if step in STOPS: body = f"<style>#sk stop{{stop-color:{STOPS[step][0]}}}#sk stop+stop{{stop-color:{STOPS[step][1]}}}</style>" + body
    if key == 'forest' and step <= 2:   # R8: dawn mist, no night star dots (spec: Echo Forest at m/d is the same woods in dawn mist)
        mk = Z.mk
        for a_, c_ in ((mk(255, .34, .30), mk(130, .32, .42)), (mk(258, .26, .28), mk(150, .26, .52)), (mk(250, .30, .30), mk(140, .34, .30)), (mk(250, .34, .30), mk(140, .36, .34))): body = body.replace(a_, c_)   # the same dawn-mist woods as render H
        import re as _re; body = _re.sub(r"<circle cx='[0-9.]+' cy='[0-9.]+' r='2.4' fill='#FFF3A8' stroke='none'/>", '', body)
    if tint:
        i = body.index("<div class='abs'", body.index('data-name') - 400) if False else None
        ov = f"<div class='abs' style='left:0;top:0;width:{w}px;height:{h}px;background:{tint};pointer-events:none'></div>"
        # tint the scene, not the HUD or card: insert before the top bar (hud16 starts with the Back plate)
        k = body.index("data-name='back'"); k = body.rindex('<div', 0, k)
        body = body[:k] + ov + body[k:]
    return body
if __name__ == '__main__':
    font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 22)
    for key in ('meadow', 'fields', 'lake', 'forest'):
        for (w, h, suf) in (((320, 568, '320x568'),) if SE else ((390, 844, '390'),)):
            ims = []
            for st in range(1, 6):
                d = doc(key, st, w, h); n = f'{key}-step{st}-{suf}'
                open(OUT + n + '.html', 'w').write(d); PV.S.shot(d, OUT + n + '.png', w, h, 'tod-' + n); ims.append(Image.open(OUT + n + '.png').convert('RGB').resize((w, h)))
            names = ['1 morning', '2 day', '3 afternoon', '4 evening', '5 night']
            S = Image.new('RGB', (5 * (w + 10) + 10, h + 90), '#F6E9C8'); dr = ImageDraw.Draw(S)
            dr.text((10, 8), (f'{key}: time of day by zone step = 1 + zoneRuns[{key}] mod 5 (K3), set at run start; run 6 is morning again' if key != 'forest' else 'Echo Forest (Sound Duel): step = 1 + Sound Duel rounds mod 5 (W5), set at round start; round 6 is dawn again'), fill='#3A2410', font=font)
            for i, im in enumerate(ims): S.paste(im, (10 + i * (w + 10), 80)); dr.text((14 + i * (w + 10), 46), f'step {names[i]}', fill='#3A2410', font=font)
            S.save(OUT + f'strip-{key}-steps-{suf}.png'); print(key, suf, flush=True)
