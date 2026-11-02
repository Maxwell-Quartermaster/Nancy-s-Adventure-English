# Maxwell t444u: the 320x568 fit-to-width frame of an indoor room is the target at every size. Render-level "ceiling cap":
# the scene keeps the width fit (same props-to-screen proportion; HUD, card and taps full size; bottom pinned to the card), and on taller
# phones the art above the line the 320 frame shows (cap = design y visible under the HUD at 320) is cropped; the band between the HUD
# and the cap is plain parchment. Same knob as sky option B (a top crop line per scene), set from the 320 frame instead of the highest target.
# 320 is not re-rendered (byte-identical). Usage: python3 ceil_cap.py [scene names]  -> ceiling-cap/{html,png}/<scene>-<w>x<h>.*
import sys, os, re, json, hashlib
names = sys.argv[1:] or ['E-lake-front-desk', 'F-lake-night-table']; sys.argv = ['x']
sys.path.insert(0, '/workspace/v608build/scenes'); sys.path.insert(0, '/workspace/v608build/screens')
import stage_v608 as ST
O = '/workspace/v608build/round2/ceiling-cap/'; os.makedirs(O + 'html', exist_ok=True); os.makedirs(O + 'png', exist_ok=True)
SRC = '/workspace/v608build/scenes/stage/html/'
WORLD = re.compile(r"<div class='abs' data-st='[^']+' style='left:(-?[0-9.]+)px;top:(-?[0-9.]+)px;width:390px;height:844px;overflow:hidden;transform:scale\(([0-9.]+)\)")
def cap_of(name):   # design y at the HUD's bottom edge in the 320 frame
    d = open(SRC + f'{name}-320x568.html').read(); ox, oy, s = map(float, WORLD.search(d).groups())
    return (ST.measure(d, 320, 568)['top'] - oy) / s
def capped(doc, cap):
    a = "overflow:hidden;transform:scale"; assert doc.count(a) == 1
    return doc.replace(a, f"overflow:hidden;-webkit-clip-path:inset({cap:.1f}px 0 0 0);clip-path:inset({cap:.1f}px 0 0 0);transform:scale")
WALL = '#EAD7A8'
def wallup(doc, cap, vis, fit, ceil):   # alternative: the ceiling strip the 320 frame shows (cap .. molding) slides up under the HUD; plain wall fills down to the molding
    s, ox, oy = fit; d = cap - vis; mb = ceil + 8
    m = WORLD.search(doc); i = m.start(); j = doc.index("<div class='abs' data-tap=1", i) if "data-tap=1" in doc[i:] else None
    k = doc.index(m.group(0)); e = doc.index("</div><div class='abs' data-tap=1", k) + 6   # end of the world div (hits follow it)
    world = doc[k:e]
    a = "overflow:hidden;transform:scale"
    real = world.replace(a, f"overflow:hidden;-webkit-clip-path:inset({mb}px 0 0 0);clip-path:inset({mb}px 0 0 0);transform:scale")
    strip = re.sub(r"data-(pn|hit|st|name|hero|tagph)=", r"data-cp-\1=", world.replace(a, f"overflow:hidden;-webkit-clip-path:inset({cap:.1f}px 0 {844 - mb}px 0);clip-path:inset({cap:.1f}px 0 {844 - mb}px 0);transform:scale"))
    strip = strip.replace(f"top:{m.group(2)}px", f"top:{oy - d * s:.2f}px", 1).replace("<div class='abs'", "<div class='abs' aria-hidden='true'", 1)
    band = f"<div class='abs' aria-hidden='true' style='left:0;top:{oy + (mb - d) * s:.1f}px;width:{390 * s:.1f}px;height:{d * s:.1f}px;background:{WALL}'></div>"
    return doc[:k] + band + strip + real + doc[e:]
md = []
for name in names:
    cap = cap_of(name)
    stage, ui390 = ST.stage_of(name); stage, log = ST.fit_stage(name, stage, ui390)
    for w, h in ((390, 844), (375, 667), (375, 812)):
        ui = ui390 if w == 390 else ST.ui_at(name, w, h)
        if w == 390: fit = (1, 0, 0)
        else:
            m390 = ST.measure(ST.compose(name, stage, ui390, 390, 844, (1, 0, 0)), 390, 844)
            m = ST.measure(ST.compose(name, stage, ui, w, h, (1, 0, 0)), w, h); fit = ST.fit_for(m390, m, w, h)
        doc0 = ST.compose(name, stage, ui, w, h, fit); f = f'{name}-{w}x{h}'
        same = os.path.exists(SRC + f + '.html') and hashlib.md5(doc0.encode()).hexdigest() == hashlib.md5(open(SRC + f + '.html', 'rb').read()).hexdigest()
        m = ST.measure(doc0, w, h); vis = (m['top'] - fit[2]) / fit[0]   # design y now visible under the HUD
        if vis >= cap - 0.5: md.append(f'- {f}: shows from design y {vis:.0f}, cap {cap:.0f}: nothing to crop (not re-rendered)'); continue
        doc = capped(doc0, cap); open(O + f'html/{f}.html', 'w').write(doc); ST.shot(doc, O + f'png/{f}.png', w, h)
        dw = wallup(doc0, cap, vis, fit, ST.CEIL[name]); open(O + f'html/{f}-wallup.html', 'w').write(dw); ST.shot(dw, O + f'png/{f}-wallup.png', w, h)
        md.append(f'- {f}: rebuilt == staged render: {same}; cropped design y {vis:.0f}-{cap:.0f} ({(cap - vis) * fit[0]:.0f} pt of ceiling/wall) above the cap'); print(md[-1], flush=True)
open(O + 'CAP.md', 'a').write('\n'.join(md) + '\n')
