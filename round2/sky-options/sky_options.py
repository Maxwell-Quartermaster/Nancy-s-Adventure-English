# Sky pick for Maxwell (Auditor ruling 7:25 PM MDT: the sky safe band conflicts with S2). Render-level only; nothing frozen changes.
#  A "safe band": the sky targets sit below the HUD at every size (kite, owl + its branch, lantern + its branch and cord); 390 shifts slightly;
#    320 fits the width (bottom pinned). Edges: any scene target nearer than 19.5 design pt to a side moves in (desk/tent +4, towel and its peg -2, crib/bridge -4): 16 pt+ at 320.
#  B "crop floor": 390 is the 6:09 PM baseline byte for byte; at 320 the scene scales so the sky crops only down to its highest target, and no
#    target comes nearer than 16 pt to the edge (so the art is a little smaller, parchment at the sides); bottom pinned to the card.
# Usage: python3 sky_options.py A|B   -> sky-options/<A|B>/{html,png}/<screen>-{390x844,320x568}.*
import sys, os, json, re, subprocess, shutil
OPT = (sys.argv[1] if len(sys.argv) > 1 else os.environ.get('NAE_SKY', 'A')).upper(); assert OPT in 'AB'
sys.argv = ['x']; sys.path.insert(0, '/workspace/v608build/screens'); sys.path.insert(0, '/workspace/v608build/scenes')
MARK = '<!--UI-->'; NUMS = [10, 14, 21, 22, 23, 33, 34, 35, 36, 54]; ZONES = ('meadow', 'fields', 'lake', 'forest')
import play_v608 as PV
Z = PV.Z
BAND = 312   # design y: a target's top at or below 312 clears the HUD at 320 (y >= 311) and 375 (y >= 290) on the standard ask card
if OPT == 'A':
    M = Z.STOP['meadow']; objs = [list(o) for o in M[7]]
    for o in objs:
        if o[0] == 'kite': o[1], o[2] = 296, BAND          # down into the band, right of the swing set
        if o[0] == 'bus stop': o[2] = 396                  # 12 pt under the kite; bench stays 14 pt below
    Z.STOP['meadow'] = M[:7] + (tuple(map(tuple, objs)),) + M[8:]
    F = Z.STOP['forest']; fo = [list(o) for o in F[7]]
    DO, DL = BAND - 150, BAND - 140                        # owl and lantern move down with their branches
    for o in fo:
        if o[0] == 'owl': o[2] += DO
        if o[0] == 'lantern': o[2] += DL
    Z.STOP['forest'] = F[:7] + (tuple(map(tuple, fo)),) + F[8:]
    _out = Z.outdoor
    def outdoor(w, h, key):
        b = _out(w, h, key)
        if key == 'forest' and w == 390:
            for a, n in ((f"<path d='M390 216h-110' stroke='#5A3A22' stroke-width='8'/><path d='M390 216h-110' stroke='#7A5233' stroke-width='4'/>",
                          f"<path d='M390 {216 + DO}h-110' stroke='#5A3A22' stroke-width='8'/><path d='M390 {216 + DO}h-110' stroke='#7A5233' stroke-width='4'/>"),
                         ("<path d='M64 140V118' stroke-width='2'/><path d='M4 118q60-14 126 2' stroke='#5A3A22' stroke-width='7'/>",
                          f"<path d='M64 {140 + DL}V{118 + DL}' stroke-width='2'/><path d='M4 {118 + DL}q60-14 126 2' stroke='#5A3A22' stroke-width='7'/>")):
                assert b.count(a) == 1, a; b = b.replace(a, n)
        return b
    Z.outdoor = outdoor
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
    json.dump({k: v[1] for k, v in parts().items()}, open(f'/tmp/sky{OPT}_ui.json', 'w')); sys.exit(0)
P390 = parts()
r = subprocess.run([sys.executable, __file__, OPT], env=dict(os.environ, NAE_SE='1'), capture_output=True, text=True); assert r.returncode == 0, r.stderr[-1500:]
UI320 = json.load(open(f'/tmp/sky{OPT}_ui.json')); os.remove(f'/tmp/sky{OPT}_ui.json')
O = f'/workspace/v608build/round2/sky-options/{OPT}/'; os.makedirs(O + 'html', exist_ok=True); os.makedirs(O + 'png', exist_ok=True)
import stage_v608 as ST   # loads after the scene strings are made (its t441u outdoor block never reaches them)
TAP = re.compile(r"data-tap=1 role='button' data-name='([^']+)'[^>]*?style='left:(-?[0-9.]+)px;top:(-?[0-9.]+)px;width:([0-9.]+)px;height:([0-9.]+)px")
def edges(scene):   # A only: furniture 16 pt+ from the edge at 320 (design x >= 20, right <= 370); the towel's peg moves with it
    for k, x, y, a, b in [(k, float(x), float(y), float(a), float(b)) for k, x, y, a, b in TAP.findall(scene)]:
        dx = 20 - x if x < 19.5 else (370 - x - a if x + a > 370.5 else 0)
        if dx and y < 844:
            scene = ST.shift(scene, k, 0, dx, 0); EDGE.append(f'{k} {dx:+.0f}')
            if k == 'towel': scene = scene.replace("<circle cx='344' cy='424' r='4.5'", f"<circle cx='{344 + dx:.0f}' cy='424' r='4.5'")
    return scene
EDGE = []
if OPT == 'A': P390 = {k: (edges(sc), ui) for k, (sc, ui) in P390.items()}
# 390: the play page itself (B: identical to the approved files; the zones have no approved 390 file, so the baseline code renders them)
for name, (scene, ui) in P390.items():
    doc = PV.page(390, 844, scene + ui); f = f'{name}-390x844'
    open(O + f'html/{f}.html', 'w').write(doc); PV.S.shot(doc, O + f'png/{f}.png', 390, 844, f'sky{OPT}-{name}')
print('edge moves:', EDGE)
log = []; M390 = {}
for name, (scene, ui390) in P390.items():
    m390 = ST.measure(ST.compose(name, scene, ui390, 390, 844, (1, 0, 0)), 390, 844)
    M390[name + '-390x844'] = m390
    m = ST.measure(ST.compose(name, scene, UI320[name], 320, 568, (1, 0, 0)), 320, 568)
    w, card0, card, top = 320, m390['card'], m['card'], m['top'] + 6
    taps = [(k, float(x), float(y), float(a), float(b)) for k, x, y, a, b in TAP.findall(scene)]
    s = w / 390 if OPT == 'A' else ST.fit_capped(scene, m390, m, w, 568)[0]   # B: stage_v608.fit_capped (the staged round2b fit)
    fit = (s, (w - 390 * s) / 2, card - card0 * s); doc = ST.compose(name, scene, UI320[name], 320, 568, fit); f = f'{name}-320x568'
    open(O + f'html/{f}.html', 'w').write(doc); ST.shot(doc, O + f'png/{f}.png', 320, 568)
    log.append(f'{f}: scale {s:.3f}, offset {fit[1]:.1f}, {fit[2]:.1f}; card390 {card0:.0f}, card {card:.0f}, HUD {m["top"]:.0f}'); print(log[-1], flush=True)
for name, (scene, ui390) in P390.items():   # round2b (1): 375x812, UI from the 390 code at that size
    PV.W, PV.H = 375, 812
    try: h8 = (lambda n: PV.SCR[int(n[:2])][3]() if n[0].isdigit() else Z.screen(n.split('-')[1], 'ask', 375, 812))(name)
    finally: PV.W, PV.H = 390, 844
    ui8 = h8[h8.index(MARK):].replace(MARK, '')
    m390 = M390[name + '-390x844']; m = ST.measure(ST.compose(name, scene, ui8, 375, 812, (1, 0, 0)), 375, 812)
    s = 375 / 390 if OPT == 'A' else ST.fit_capped(scene, m390, m, 375, 812)[0]
    fit = (s, (375 - 390 * s) / 2, m['card'] - m390['card'] * s); doc = ST.compose(name, scene, ui8, 375, 812, fit); f = f'{name}-375x812'
    open(O + f'html/{f}.html', 'w').write(doc); ST.shot(doc, O + f'png/{f}.png', 375, 812)
    log.append(f'{f}: scale {s:.3f}, offset {fit[1]:.1f}, {fit[2]:.1f}; card390 {m390["card"]:.0f}, card {m["card"]:.0f}, HUD {m["top"]:.0f}'); print(log[-1], flush=True)
json.dump(M390, open(O + 'measure390.json', 'w'), indent=0); open(O + 'FIT.md', 'w').write(f'# Option {OPT} 320 fits\n' + '\n'.join('- ' + l for l in log) + '\n')
