# S5 (Auditor round 2): the remaining 320x568 scene renders on the P3 layout (D2 fit to width): the 390 scene, scaled to 320/390 as one
# piece, bottom pinned to the 320 card, sky cropped under the HUD; the HUD, card and 44 pt tap areas at full size (stage_v608.compose).
# Approved screens keep their t385u backgrounds (the scene strings are made before stage_v608 applies the t441u outdoor fixes).
# Usage: python3 stage320_play.py   (writes screens-v608/{html,png}/<n>-<slug>-320x568.* and zone-<key>-ask-320x568.*)
import sys, os, json, subprocess
sys.argv = ['x']; sys.path.insert(0, '/workspace/v608build/screens'); sys.path.insert(0, '/workspace/v608build/scenes')
MARK = '<!--UI-->'; NUMS = [10, 14, 21, 22, 23, 33, 34, 35, 36, 54]; ZONES = ('meadow', 'fields', 'lake', 'forest')
R2 = os.environ.get('NAE_R2TP') == '1'   # round 2 P1 ask render: screen 10 only, staged tapPrompt (stage_v608.compose swaps the text)
if R2: NUMS, ZONES = [10], ()
import play_v608 as PV
Z = PV.Z
_t, _h = PV.top, Z.hud
PV.top = lambda *a, **k: MARK + _t(*a, **k); Z.hud = lambda *a, **k: MARK + _h(*a, **k)
def parts():
    out = {}
    for n in NUMS:
        slug, st, src, fn = PV.SCR[n]; h = fn(); i = h.index(MARK); out[f'{n:02d}-{slug}'] = (h[:i], h[i:].replace(MARK, ''))
    for k in ZONES:
        h = Z.screen(k, 'ask', PV.W, PV.H); i = h.index(MARK); out[f'zone-{k}-ask'] = (h[:i], h[i:].replace(MARK, ''))
    return out
if PV.SE:
    json.dump({k: v[1] for k, v in parts().items()}, open('/tmp/s320play_ui.json', 'w')); sys.exit(0)
P390 = parts()
r = subprocess.run([sys.executable, __file__], env=dict(os.environ, NAE_SE='1'), capture_output=True, text=True); assert r.returncode == 0, r.stderr[-1500:]
UI320 = json.load(open('/tmp/s320play_ui.json')); os.remove('/tmp/s320play_ui.json')
import stage_v608 as ST   # applies the t441u outdoor fixes to later scene strings only; P390 is already made
O = '/workspace/screens-v608/'
for name, (scene, ui390) in P390.items():
    m390 = ST.measure(ST.compose(name, scene, ui390, 390, 844, (1, 0, 0)), 390, 844)
    m = ST.measure(ST.compose(name, scene, UI320[name], 320, 568, (1, 0, 0)), 320, 568)
    fit = ST.fit_capped(scene, m390, m, 320, 568); doc = ST.compose(name, scene, UI320[name], 320, 568, fit)   # round2b B (t445u)
    if R2: f = '/workspace/v608build/round2/renders/ask-can-you-find-320x568'; open(f + '.html', 'w').write(doc); ST.shot(doc, f + '.png', 320, 568); print(f); continue
    f = f'{name}-320x568'; open(O + f'html/{f}.html', 'w').write(doc); ST.shot(doc, O + f'png/{f}.png', 320, 568)
    print(f, 'scale %.3f oy %.1f card390 %.0f card320 %.0f hud %.0f' % (fit[0], fit[2], m390['card'], m['card'], m['top']), flush=True)
