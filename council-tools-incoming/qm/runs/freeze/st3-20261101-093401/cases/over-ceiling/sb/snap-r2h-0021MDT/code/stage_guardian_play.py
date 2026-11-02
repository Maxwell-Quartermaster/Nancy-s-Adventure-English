# Follow-up 9:05 PM MDT (QM-relayed): screens 25-28 (guardian hint letters / Words of Jesus / kneels / win) at 320 x 568 and 375 x 667 on the
# staged walk-24 rule (round2 P5 "the scene shrinks to sit below it", stage_v608.fit_whole): one 390 design scene, scaled as one piece so the
# drawn scenery (meadow deco, guardian, heroes, picture plate) sits below the Guardian banner; HUD, banner and card at the phone's own size.
# The 390 renders are not rewritten (byte-identical). Approved t385u backgrounds kept (scene strings made before stage_v608 loads, as stage320_play).
# Usage: python3 stage_guardian_play.py   (writes screens-v608/{html,png}/<n>-<slug>-{320x568,375x667}.*)
import sys, os, json, subprocess
sys.argv = ['x']; sys.path.insert(0, '/workspace/v608build/screens'); sys.path.insert(0, '/workspace/v608build/scenes')
MARK = '<!--UI-->'; NUMS = [24, 25, 26, 27, 28]
import play_v608 as PV
Z = PV.Z
_t, _h = PV.top, Z.hud
PV.top = lambda *a, **k: MARK + _t(*a, **k); Z.hud = lambda *a, **k: MARK + _h(*a, **k)
def parts():
    out = {}
    for n in NUMS:
        slug, st, src, fn = PV.SCR[n]; h = fn(); i = h.index(MARK); out[f'{n:02d}-{slug}'] = (n, h[:i], PV.guardian_chip(h[i:].replace(MARK, ''), n))
    return out
if PV.SE:   # 320 UI: play_v608 SE guardian branch (r2c: one row of four 60 pt plates, compact card, toast and bubble overlay the scene)
    json.dump({k: v[2] for k, v in parts().items()}, open('/tmp/qmtmp/sgp_ui320.json', 'w')); sys.exit(0)
P390 = parts()
UIS = {}
for wh in ((375, 667), (375, 812)):
    sv = (PV.W, PV.H); PV.W, PV.H = wh
    try: UIS[wh] = {k: ui for k, (n, sc, ui) in parts().items()}
    finally: PV.W, PV.H = sv
r = subprocess.run([sys.executable, __file__], env=dict(os.environ, NAE_SE='1'), capture_output=True, text=True); assert r.returncode == 0, r.stderr[-1500:]
UI320 = json.load(open('/tmp/qmtmp/sgp_ui320.json')); os.remove('/tmp/qmtmp/sgp_ui320.json')
import stage_v608 as ST
O = '/workspace/screens-v608/'
_k24 = [k for k in P390 if k.startswith('24-')][0]; M24 = ST.measure(ST.compose(_k24, P390[_k24][1], P390[_k24][2], 390, 844, (1, 0, 0)), 390, 844)
for name, (n, scene, ui390) in P390.items():
    d390 = ST.compose(name, scene, ui390, 390, 844, (1, 0, 0)); m390 = ST.measure(d390, 390, 844); top0 = min(ST.scenery_top(d390, m390['card']), ST.scenery_top(d390.replace("data-pic='plate'", "data-pic='plate' data-deco='plate'"), m390['card']))   # the picture plate counts as scenery too
    for (w, h), ui in (((375, 667), UIS[(375, 667)][name]), ((375, 812), UIS[(375, 812)][name]), ((320, 568), UI320[name])):
        if n == 28: ui_m = ui.replace("<div class='abs' data-txt=1 style='left:50%;transform:translateX(-50%);top:", "<div class='abs' data-txt=1 style='display:none;left:50%;transform:translateX(-50%);top:")   # r2d: 28's toast overlays the sky (as at 320); it is not the scene top
        else: ui_m = ui
        m = ST.measure(ST.compose(name, scene, ui_m.replace('z-index:6;box-sizing:border-box;background:#FFF0B8', 'z-index:6;display:none;box-sizing:border-box;background:#FFF0B8').replace('data-overlay=1 style=\'', 'data-overlay=1 style=\'display:none;'), w, h, (1, 0, 0)), w, h)   # the Words of Jesus bubble overlays the scene (as at 390); it is not the card
        fit = ST.fit_whole(M24 if (n == 25 and (w, h) == (375, 667)) else m390, m, w, h, top0); doc = ST.compose(name, scene, ui, w, h, fit)   # r2d: 25's 375 x 667 card now matches 24's (one-line hint), so it fits against 24's 390 card line (25's taller 390 card would crop the feet)
        f = f'{name}-{w}x{h}'; open(O + f'html/{f}.html', 'w').write(doc); ST.shot(doc, O + f'png/{f}.png', w, h)
        print(f, 'scale %.3f ox %.1f oy %.1f scenery-top390 %.0f hud %.0f card %.0f' % (*fit, top0, m['top'], m['card']), flush=True)
# r2c 26 options at 320 (council 9:49 PM MDT, QM-relayed; Instructor's chip proposal): NAE_G26=1 writes
#   26-A (as staged: the bubble sits above the card, over Sam), 26-B (the bubble under the banner, its own scroll box, over the picture plate),
#   26-C rest (a small chip under the banner; covers nothing, the scene sits below it) and 26-C open (a tap on the chip opens the verse over the scene).
# Render-only; files go to round2/r2c/g26/ (screens-v608 is not touched).
if os.environ.get('NAE_G26') == '1':
    import re as _re
    _D = os.environ.get('NAE_G26D') == '1'   # r2d: staged copies go to round2/r2d/g26d/ (r2c/g26 untouched); the chip carries the existing uiText.jesusWords Thai (copied from cards.json), no new Thai
    G = '/workspace/v608build/round2/r2d/g26d/' if _D else '/workspace/v608build/round2/r2c/g26/'; os.makedirs(G + 'html', exist_ok=True); os.makedirs(G + 'png', exist_ok=True)
    name = [k for k in P390 if k.startswith('26-')][0]; n, scene, ui390 = P390[name]; ui = UI320[name]
    BUB = _re.search(r"<div class='abs' data-overlay=1 style='left:16px;right:16px;bottom:120px;(.*?)'>(.*?</div>)</div>", ui, _re.S)
    inner = BUB.group(2); bst = BUB.group(1)
    d390 = ST.compose(name, scene, ui390, 390, 844, (1, 0, 0)); m390 = ST.measure(d390, 390, 844); top0 = min(ST.scenery_top(d390, m390['card']), ST.scenery_top(d390.replace("data-pic='plate'", "data-pic='plate' data-deco='plate'"), m390['card']))
    CHIP = ("<div class='abs' data-chip='jesus' data-tap=1 role='button' style='left:16px;top:125px;z-index:6;box-sizing:border-box;min-height:44px;max-width:288px;display:flex;flex-wrap:wrap;align-items:center;gap:0 6px;"
            "background:#FFF0B8;border:2px solid #10170F;border-radius:12px;box-shadow:inset 0 0 0 2px #E8B84A,0 3px 0 #10170F;padding:2px 10px'>"
            "<div class='e15 nw' data-txt=1>" + ('' if _D else '📜 ') + PV.u('jesusWords')[0] + " ·</div><div class='t17 nw' data-txt=1 style='line-height:1.7'>" + (PV.u('jesusWords')[1] if _D else 'พระวจนะของพระเยซู') + "</div></div>")
    def without_bubble(u): return u[:BUB.start()] + u[BUB.end():]
    V = {
     'A': ui,
     'B': ui.replace("left:16px;right:16px;bottom:120px;" + bst, "left:16px;right:16px;top:125px;max-height:134px;overflow-y:auto;-webkit-overflow-scrolling:touch;" + bst.replace('box-shadow:', 'box-shadow:inset 0 -14px 10px -12px rgba(58,36,16,.45),', 1), 1).replace("data-overlay=1 style='left:16px;right:16px;top:125px", "data-overlay=1 data-scroll='jesus' style='left:16px;right:16px;top:125px", 1),
     'C-rest': without_bubble(ui) + CHIP,
     'C-open': without_bubble(ui) + CHIP + f"<div class='abs' data-overlay=1 style='left:16px;right:16px;top:181px;{bst}'>{inner}</div>"}
    rows = []
    for k, u in V.items():
        mu = u.replace("data-overlay=1 style='", "data-overlay=1 style='display:none;").replace("data-overlay=1 data-scroll='jesus' style='", "data-overlay=1 data-scroll='jesus' style='display:none;")
        if k == 'C-open': mu = (without_bubble(ui) + CHIP)   # the opened verse is a passing overlay; the fit is the resting one
        m = ST.measure(ST.compose(name, scene, mu, 320, 568, (1, 0, 0)), 320, 568)
        if k.startswith('C'): m['top'] = max(m['top'], 125 + 46)   # the chip is UI under the banner; the scene starts below it
        fit = ST.fit_whole(m390, m, 320, 568, top0); doc = ST.compose(name, scene, u, 320, 568, fit)
        f = f'26-{k}-320x568'; open(G + f'html/{f}.html', 'w').write(doc); ST.shot(doc, G + f'png/{f}.png', 320, 568)
        rows.append((k, fit[0])); print(f, 'scale %.3f' % fit[0], flush=True)
# r2d (10:07 PM MDT, Watchman 26-D, QM-relayed): NAE_G26D=1 writes 26-D at 320 x 568, 375 x 667 and 375 x 812 to round2/r2d/g26d/ (staging; screens-v608 not touched).
#   r2d-2 (10:18 PM MDT, Instructor via QM): the 🤔 picture plate stays on the scene where staged 26 has it (the bubble closes after 6 s or a tap).
#   One layout at every size: the bubble sits just under the Guardian banner, its height capped so it ends 6 pt above the highest head (Sam or the
#   Guardian's helmet) incl. its 4 pt drop, and its right edge 8 pt left of the picture plate (a full-width bubble would cover the plate); Thai scrolls inside (17 px, lh 1.7).
if os.environ.get('NAE_G26D') == '1':
    import re as _re
    sys.path.insert(0, '/workspace/v608build/round2/r2d'); import rects26 as RX
    G = '/workspace/v608build/round2/r2d/g26d/'; os.makedirs(G + 'html', exist_ok=True); os.makedirs(G + 'png', exist_ok=True)
    name = [k for k in P390 if k.startswith('26-')][0]; n, scene, ui390 = P390[name]
    d390 = ST.compose(name, scene, ui390, 390, 844, (1, 0, 0)); m390 = ST.measure(d390, 390, 844); top0 = min(ST.scenery_top(d390, m390['card']), ST.scenery_top(d390.replace("data-pic='plate'", "data-pic='plate' data-deco='plate'"), m390['card']))
    sceneD = scene   # r2d-2: the plate stays
    def bubble_span(u):
        k = u.index('z-index:6;box-sizing:border-box;background:#FFF0B8'); k = u.rindex('<div', 0, k); d = 0
        for mm in _re.finditer(r'<div\b|</div>', u[k:]):
            d += 1 if mm.group(0) == '<div' else -1
            if d == 0: return k, k + mm.end()
    j = PV.D['jesusWords'][0]; pic = PV.C['sw-19']['pic']
    BST = "z-index:6;box-sizing:border-box;background:#FFF0B8;border:2px solid #10170F;border-radius:14px;box-shadow:inset 0 -14px 10px -12px rgba(58,36,16,.45),inset 0 0 0 3px #E8B84A,inset 0 0 0 4px #10170F,0 4px 0 #10170F;padding:10px 12px"
    inner = PV.tx(PV.u('jesusWords')[0] + ' · ' + j['ref'], 'e15') + PV.tx(j['en'], 'e15') + PV.tx(j['th'], 't17', 'line-height:1.7')
    for (w, h), ui in (((320, 568), UI320[name]), ((375, 667), UIS[(375, 667)][name]), ((375, 812), UIS[(375, 812)][name])):
        a, b = bubble_span(ui); bare = ui[:a] + ui[b:]
        m = ST.measure(ST.compose(name, scene, bare, w, h, (1, 0, 0)), w, h); fit = ST.fit_whole(m390, m, w, h, top0)   # same fit as staged 26 (its bubble is hidden when measured)
        f = f'26-D-{w}x{h}'; probe = G + f'html/{f}.probe.html'; open(probe, 'w').write(ST.compose(name, sceneD, bare, w, h, fit))
        r = RX.rects(probe, w, h); os.remove(probe)   # our own probe file
        T = r['banner'][3] + 6; RGT = w - (r['pic'][0] - 8)   # right inset: 8 pt clear of the plate
        heads = [hr for hr in (r['sheadRect'], r['gheadRect']) if hr and hr[0] < w - RGT and hr[2] > 16]   # r2d-3 (Auditor H3): cap above the heads under the bubble (Sam; the helmet sits right of it)
        cap = min(hr[1] for hr in heads) - 6 - 4 - T
        full = [16, T, w - 16, T + cap + 4]; pl = r['pic']; hit = not (pl[0] >= full[2] or pl[2] <= full[0] or pl[1] >= full[3] or pl[3] <= full[1])
        print(f'26-D {w}x{h}: picture plate {pl}; a full-width bubble {full} would ' + ('overlap it by x %d-%d, y %d-%d' % (max(pl[0], full[0]), min(pl[2], full[2]), max(pl[1], full[1]), min(pl[3], full[3])) if hit else 'not touch it'), flush=True)
        bub = f"<div class='abs' data-overlay=1 data-bubble='jesus' data-scroll='jesus' style='left:16px;right:{RGT}px;top:{T}px;max-height:{cap}px;overflow-y:auto;-webkit-overflow-scrolling:touch;{BST}'>{inner}</div>"
        doc = ST.compose(name, sceneD, bare + bub, w, h, fit); open(G + f'html/{f}.html', 'w').write(doc); ST.shot(doc, G + f'png/{f}.png', w, h)
        r2 = RX.rects(G + f'html/{f}.html', w, h); need2 = r2['thaiTop'] + 2 * r2['thaiLH'] + r2['padB']   # 2 full Thai lines (17 px, lh 1.7) before the scroll (10:27 PM steering)
        print(f'{f}: visible {r2["bubbleScroll"][1]} of {r2["bubbleScroll"][0]}; Thai starts at {r2["thaiTop"]}; 2 full Thai lines need {need2:.0f} (+{max(0, need2 - (cap)):.0f} pt over the cap {cap}); ' + ('fits' if need2 <= cap else 'does NOT fit above the heads'), flush=True)
        print(f, 'scale %.3f banner-bottom %d bubble top %d cap %d right %d (width %d) heads sam %d guardian %d' % (fit[0], r['banner'][3], T, cap, w - RGT, w - RGT - 16, r['stop'], r['gtop']), flush=True)
