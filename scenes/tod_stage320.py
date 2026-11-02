# S5: the 20 time-of-day 320x568 renders on the P3 layout (D2 fit to width): the 390 scene at each step, scaled 320/390 as one piece,
# bottom pinned to the 320 card; the 320 HUD, tint and card at full size. Backgrounds stay the approved ones (made before stage_v608 loads).
# Usage: python3 tod_stage320.py   (rewrites tod/<zone>-step<n>-320x568.{html,png} and tod/strip-<zone>-steps-320x568.png)
import sys, os, json, subprocess
sys.argv = ['x']; sys.path.insert(0, '/workspace/v608build/scenes'); sys.path.insert(0, '/workspace/v608build/screens')
SE = os.environ.get('NAE_SE') == '1'
import tod_v608 as T
PV, Z = T.PV, T.Z; MARK = '<!--UI-->'
_t, _h = PV.top, Z.hud
PV.top = lambda *a, **k: MARK + _t(*a, **k); Z.hud = lambda *a, **k: MARK + _h(*a, **k)
def parts(w, h):
    out = {}
    for key in ('meadow', 'fields', 'lake', 'forest'):
        for st in range(1, 6):
            b = T.body(key, st, w, h)
            k = b.index("data-name='back'"); k = b.rindex('<div', 0, k)   # the tint overlay sits just before the HUD: it goes with the UI
            i = min(b.index(MARK), k) if MARK in b else k
            sty = b[:b.index('</style>') + 8] if b.startswith('<style>') else ''
            out[f'{key}-step{st}'] = (b[:i], sty + b[i:].replace(MARK, ''))
    return out
if SE:
    json.dump({k: v[1] for k, v in parts(320, 568).items()}, open('/tmp/tod320_ui.json', 'w')); sys.exit(0)
P390 = parts(390, 844)
r = subprocess.run([sys.executable, __file__], env=dict(os.environ, NAE_SE='1'), capture_output=True, text=True); assert r.returncode == 0, r.stderr[-1500:]
UI = json.load(open('/tmp/tod320_ui.json')); os.remove('/tmp/tod320_ui.json')
import stage_v608 as ST
from PIL import Image, ImageDraw, ImageFont
font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 22); names = ['1 morning', '2 day', '3 afternoon', '4 evening', '5 night']
for key in ('meadow', 'fields', 'lake', 'forest'):
    ims = []
    for st in range(1, 6):
        n = f'{key}-step{st}'; scene, ui390 = P390[n]
        m390 = ST.measure(ST.compose(n, scene, ui390, 390, 844, (1, 0, 0)), 390, 844); m = ST.measure(ST.compose(n, scene, UI[n], 320, 568, (1, 0, 0)), 320, 568)
        fit = ST.fit_capped(scene, m390, m, 320, 568); d = ST.compose(n, scene, UI[n], 320, 568, fit); f = T.OUT + n + '-320x568'   # round2b B (t445u): crop capped, 16 pt edges
        open(f + '.html', 'w').write(d); ST.shot(d, f + '.png', 320, 568); ims.append(Image.open(f + '.png').convert('RGB').resize((320, 568)))
        print(n, 'scale %.3f oy %.1f' % (fit[0], fit[2]), flush=True)
    w, h = 320, 568; S = Image.new('RGB', (5 * (w + 10) + 10, h + 90), '#F6E9C8'); dr = ImageDraw.Draw(S)
    dr.text((10, 8), (f'{key} at 320 (one layout, fit to width): time of day by zone step = 1 + zoneRuns[{key}] mod 5 (K3)' if key != 'forest' else 'Echo Forest (Sound Duel) at 320, fit to width: step = 1 + Sound Duel rounds mod 5 (W5)'), fill='#3A2410', font=font)
    for i, im in enumerate(ims): S.paste(im, (10 + i * (w + 10), 80)); dr.text((14 + i * (w + 10), 46), f'step {names[i]}', fill='#3A2410', font=font)
    S.save(T.OUT + f'strip-{key}-steps-320x568.png'); print(key, 'strip', flush=True)
