# Rest screen 37: 320x568 (stage320_play method: 390 scene scaled as one piece + 320 UI via stage_v608.compose, then the r2h fixes),
# plus the worn restSky variants Sunset / Starry at 390 and 320 (CONCEPT palettes: the spec gives only the names, pantry sky-sunset / trophy sky-starry).
import sys, os, json, subprocess, hashlib
sys.dont_write_bytecode = True
B = '/workspace/v608build/scene-fill-20261101/'; V = '/workspace/v608build/'
sys.argv = ['x']; sys.path.insert(0, V + 'screens'); sys.path.insert(0, V + 'scenes')
MARK = '<!--UI-->'
import re, html as _h
_PL = open(V + 'r2h-build/nancys-adventure-english-v6-08-1B-v32-PASTE.md', encoding='utf-8').read().split('\n')
_PJ = json.loads(next(l for l in _PL if l.startswith('{"version":"v6-08"')))
VR, VA = _PJ['verses']['rest'], _PJ['verses']['attribution']
VOLD = ("<div class='e20' data-txt=1 style=''>Matthew 11:28</div><div class='e15' data-txt=1 style='font-size:18px'>“Come to me, all who labor and are heavy laden, and I will give you rest.”</div>"
        "<div class='e15' data-txt=1 style=''>ESV · THSV11</div>")
TAG = "<div class='e15' data-txt=1 data-tag='{k}' style='font-size:13px;opacity:.85'>{t}</div>"   # PASTE :346 tagRule: separate small text, never joined to the verse
VNEW = (f"<div class='e20' data-txt=1 style=''>{_h.escape(VR['ref'], False)}</div>"
        f"<div class='e15' data-txt=1 data-verse='en' style='font-size:18px'>{_h.escape(VR['en'], False)}</div>" + TAG.format(k='esvTag', t=_h.escape(VA['esvTag'], False)) +
        f"<div class='t17' data-txt=1 data-verse='th' style='line-height:1.7'>{_h.escape(VR['th'], False)}</div>" + TAG.format(k='thsv11Tag', t=_h.escape(VA['thsv11Tag'], False)))
CH = {320: int(os.environ.get('QM_REST_CH320', '176')), 390: int(os.environ.get('QM_REST_CH390', '260'))}
CARD = re.compile(r"(data-name='card' style='left:16px;top:)[0-9.]+(px;width:[0-9.]+px;height:)[0-9.]+(px;')")
def setcard(doc, ch, H):
    d, n = CARD.subn(lambda m: f"{m.group(1)}{H - 8 - ch}{m.group(2)}{ch}{m.group(3)}" if ch else m.group(0), doc); assert n == 1; return d
def verse(doc):
    assert doc.count(VOLD) == 1; return doc.replace(VOLD, VNEW)
import play_v608 as PV
Z = PV.Z; _t = PV.top; PV.top = lambda *a, **k: MARK + _t(*a, **k)
def part():
    slug, st, src, fn = PV.SCR[37]; h = fn(); i = h.index(MARK); return h[:i], h[i:].replace(MARK, '')
if PV.SE:   # 320 layout only (390 untouched): the 390 card (260 pt) and ribbon (340 pt wide, top 150) leave no room for the hero at 568,
    # so the ribbon goes to 126 at 296 pt and the card to 176 pt (content height at 288 pt wide; text sizes unchanged)
    _r, _c = PV.ribbon, PV.card
    PV.ribbon = lambda en, th, y=150: _r(en, th, 126).replace('padding:2px 16px', 'padding:2px 10px', 1)
    PV.card = lambda lines, ch, *a, **k: _c(lines, CH[320] if ch == 260 else ch, *a, **k)
    _rest = PV.SCR[37][3]
    PV.SCR[37] = PV.SCR[37][:3] + ((lambda: _rest().replace('white-space:normal;width:340px', 'white-space:normal;width:296px')),)
    json.dump(verse(part()[1]), open('/tmp/qmtmp/rest-ui.json', 'w')); sys.exit(0)
md5 = lambda p: hashlib.md5(open(p, 'rb').read()).hexdigest()
PTR, PASTE = md5(V + 'CURRENT-SNAP.txt'), md5(V + 'r2h-build/nancys-adventure-english-v6-08-1B-v32-PASTE.md')
assert PTR.startswith('f6dac2d0') and PASTE.startswith('317e91ce')
scene, ui390 = part()
r = subprocess.run([sys.executable, __file__], env=dict(os.environ, NAE_SE='1'), capture_output=True, text=True); assert r.returncode == 0, r.stderr[-1500:]
ui320 = json.load(open('/tmp/qmtmp/rest-ui.json')); os.remove('/tmp/qmtmp/rest-ui.json')
import stage_v608 as ST
sys.path.insert(0, V + 'round2/r2h'); import fix_r2h as F
EV = "background:linear-gradient(#4F64A8 0%,#F4A862 45%,rgba(244,168,98,0) 60%);opacity:.72"
STARS = ''.join(f"<circle cx='{x}' cy='{y}' r='{r}' fill='#FFF8E1' stroke='none'/>" for x, y, r in
                ((30, 120, 1.6), (78, 70, 1.2), (122, 140, 1.8), (170, 96, 1.2), (214, 60, 1.6), (262, 128, 1.2), (300, 84, 1.8), (352, 112, 1.4), (58, 190, 1.2), (330, 176, 1.6), (240, 200, 1.2), (150, 210, 1.4)))
SKY = {'base': None,
       'sunset': "background:linear-gradient(#E8664A 0%,#FFB36B 42%,rgba(255,179,107,0) 62%);opacity:.78",
       'starry': "background:linear-gradient(#0B1B3A 0%,#2E4370 45%,rgba(46,67,112,0) 64%);opacity:.86"}
def sky(doc, k, w):
    if SKY[k] is None: return doc
    assert doc.count(EV) == 1, k; d = doc.replace(EV, SKY[k])
    if k == 'starry':   # stars sit in the sky band under the ribbon, before the hero (390 coords; the 320 scene is scaled with its stage)
        i = d.index(SKY[k]); j = d.index('</div>', i) + 6
        d = d[:j] + f"<svg class='abs' data-name='stars-sky' style='left:0;top:0;pointer-events:none' width='390' height='260' viewBox='0 0 390 260'>{STARS}</svg>" + d[j:]
    return d
src390 = B + 'src-snapshot/37-rest-screen-390x844.html'; d390 = setcard(verse(open(src390).read()), CH[390], 844)
ui390 = verse(ui390)
name = '37-rest-screen'
m390 = ST.measure(ST.compose(name, scene, ui390, 390, 844, (1, 0, 0)), 390, 844)
m = ST.measure(ST.compose(name, scene, ui320, 320, 568, (1, 0, 0)), 320, 568)
fit = ST.fit_capped(scene, m390, m, 320, 568)
fit = (fit[0], fit[1], max(fit[2], 568 - fit[0] * 844))   # the taller PASTE verse card pushes the pinned scene up past its own bottom; keep the ground to the screen bottom (no bare parchment strip)
J = []
for k in ('base', 'sunset', 'starry'):
    for w, h in ((390, 844), (320, 568)):
        if k == 'base' and w == 390: continue   # current: round2/r2h 37-rest-screen-390x844 (3c780acd)
        tag = f'rest-{k}-{w}x{h}'
        if w == 390: doc = sky(d390, k, 390); fixes = ['sky ' + k]; src = src390
        else:
            doc = ST.compose(name, sky(scene, k, 390), ui320, 320, 568, fit); r = F.fix(doc, tag, 320)
            doc, fixes = (r if isinstance(r, tuple) else (r, ['r2h fix'])); fixes = list(fixes) + ([] if k == 'base' else ['sky ' + k]); src = V + 'screens/play_v608.py:rest() + stage_v608.compose'
        p = B + f'html/{tag}.html'; open(p, 'w').write(doc)
        J.append(dict(tag=tag, src=src, src_md5=md5(src390) if w == 390 else md5(V + 'screens/play_v608.py'), html_md5=md5(p), w=w, h=h, loc='REST', tod=k, fixes=fixes,
                      note=('rest screen at 320 (spec: fixed evening sky)' if k == 'base' else f'restSky {k} - CONCEPT palette, spec names only') + (' fit %.3f' % fit[0] if w == 320 else '')))
json.dump(dict(pointer_md5=PTR, paste_md5=PASTE, jobs=J), open(B + 'code/jobs-rest.json', 'w'), indent=1, ensure_ascii=False)
print(len(J), 'rest pages; fit', fit)
