# QM play-verse-fix render driver. Usage: python3 render.py old|new
# Builds pages 26, 30, 37 at 320x568, 375x667, 390x844 from <which>/play_v608.py through the snap's r2h path:
#   390: play_v608 page() (+ guardian_chip for 24-28), as play_v608 __main__ -> screens-v608/html
#   26 at 320/375: stage_guardian_play.py's compose (UI from play_v608 at that size, 320 UI from an NAE_SE=1 child, fit_whole via stage_v608.measure)
#   30, 37 at 320/375: NO snap render path exists (the snap only renders them at 390); play_v608 page() at that size (320 via NAE_SE=1, 375 via PV.W/H) is used instead
#   then fix_r2h.fix (render-time fixes) and cdp_shot-style CDP screenshots (Emulation.setDeviceMetricsOverride).
# Writes only inside this folder; TMPDIR is scratch/tmp; nothing is deleted (stage_v608's own rmtree is replaced by a no-op here).
import sys, os, json, subprocess
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); WHICH = sys.argv[1]; assert WHICH in ('old', 'new')
SCR = HERE + '/scratch/'; os.chdir(SCR); os.environ['TMPDIR'] = 'tmp'   # relative on purpose: Chrome's SingletonSocket path under this long folder would pass the 107-byte unix socket limit
import tempfile; tempfile.tempdir = SCR + 'tmp'
MODE = sys.argv[2] if len(sys.argv) > 2 else 'main'
sys.argv = ['x']
sys.path.insert(0, '/workspace/v608build/screens'); sys.path.insert(0, '/workspace/v608build/scenes')
sys.path.insert(0, HERE + '/' + WHICH)   # our copy of play_v608 wins over the live screens/ one
import play_v608 as PV
assert os.path.dirname(os.path.abspath(PV.__file__)) == HERE + '/' + WHICH, PV.__file__
NUMS = [26, 30, 37]; MARK = '<!--UI-->'
if MODE == 'se':   # child, NAE_SE=1: 320 UI parts for 26 (as stage_guardian_play) and full 320 pages for 30/37 (as play_v608 __main__ SE)
    assert PV.SE
    out = {}
    _t, _h = PV.top, PV.Z.hud
    PV.top = lambda *a, **k: MARK + _t(*a, **k); PV.Z.hud = lambda *a, **k: MARK + _h(*a, **k)
    slug, st, src, fn = PV.SCR[26]; h = fn(); i = h.index(MARK); out['ui26'] = PV.guardian_chip(h[i:].replace(MARK, ''), 26)
    PV.top, PV.Z.hud = _t, _h
    for n in (30, 37): slug, st, src, fn = PV.SCR[n]; out[f'p{n}'] = PV.page(320, 568, fn())
    json.dump(out, open(SCR + f'{WHICH}-se320.json', 'w'), ensure_ascii=False); sys.exit(0)
sys.path.insert(0, '/workspace/v608build/snap-r2h-0021MDT/code/r2h'); import fix_r2h as F
docs = {}
for n in NUMS:   # 390 (play_v608 __main__)
    slug, st, src, fn = PV.SCR[n]; d = PV.page(390, 844, fn())
    if 24 <= n <= 28: d = PV.guardian_chip(d, n)
    docs[(n, slug, 390, 844)] = d
for n in (30, 37):   # 375 x 667: no snap path; play_v608 at that size
    slug, st, src, fn = PV.SCR[n]; sv = (PV.W, PV.H); PV.W, PV.H = 375, 667
    try: docs[(n, slug, 375, 667)] = PV.page(375, 667, fn())
    finally: PV.W, PV.H = sv
# 26 at 320/375: stage_guardian_play.py logic
_t, _h = PV.top, PV.Z.hud
PV.top = lambda *a, **k: MARK + _t(*a, **k); PV.Z.hud = lambda *a, **k: MARK + _h(*a, **k)
slug26 = PV.SCR[26][0]; name26 = f'26-{slug26}'
def part26():
    h = PV.SCR[26][3](); i = h.index(MARK); return h[:i], PV.guardian_chip(h[i:].replace(MARK, ''), 26)
scene, ui390 = part26()
sv = (PV.W, PV.H); PV.W, PV.H = 375, 667
try: ui375 = part26()[1]
finally: PV.W, PV.H = sv
# stage_guardian_play also needs 24's 390 parts only for 25 at 375; 26 uses its own m390. UI at 320 from the NAE_SE=1 child:
r = subprocess.run([sys.executable, __file__, WHICH, 'se'], env=dict(os.environ, NAE_SE='1'), capture_output=True, text=True); assert r.returncode == 0, r.stderr[-1500:]
SE = json.load(open(SCR + f'{WHICH}-se320.json')); ui320 = SE['ui26']
for n in (30, 37): docs[(n, PV.SCR[n][0], 320, 568)] = SE[f'p{n}']
PV.top, PV.Z.hud = _t, _h
import stage_v608 as ST
class _SH:   # no deletes: stage_v608 rmtree()s its own temp dirs; here they stay under scratch/tmp
    @staticmethod
    def rmtree(*a, **k): pass
class _TF:
    @staticmethod
    def mkdtemp(prefix='', dir=None):
        d = tempfile.mkdtemp(prefix=prefix, dir=SCR + 'tmp')
        return os.path.relpath(d, SCR) if prefix == 'stg-' else d   # run_chrome's TMPDIR: relative (socket length); html dirs stay absolute for file:// URLs
ST.shutil = _SH; ST.tempfile = _TF
d390 = ST.compose(name26, scene, ui390, 390, 844, (1, 0, 0)); m390 = ST.measure(d390, 390, 844)
top0 = min(ST.scenery_top(d390, m390['card']), ST.scenery_top(d390.replace("data-pic='plate'", "data-pic='plate' data-deco='plate'"), m390['card']))
FITS = {}
for (w, h), ui in (((375, 667), ui375), ((320, 568), ui320)):
    m = ST.measure(ST.compose(name26, scene, ui.replace('z-index:6;box-sizing:border-box;background:#FFF0B8', 'z-index:6;display:none;box-sizing:border-box;background:#FFF0B8').replace('data-overlay=1 style=\'', 'data-overlay=1 style=\'display:none;'), w, h, (1, 0, 0)), w, h)
    fit = ST.fit_whole(m390, m, w, h, top0); FITS[f'{w}x{h}'] = fit
    docs[(26, slug26, w, h)] = ST.compose(name26, scene, ui, w, h, fit)
os.makedirs(HERE + f'/html/{WHICH}', exist_ok=True); log = {'fits26': FITS, 'fixlog': [], 'files': {}}
for (n, slug, w, h), d in sorted(docs.items()):
    tag = f'{n:02d}-{slug}-{w}x{h}'; d2, lg = F.fix(d, tag, w); log['fixlog'] += lg
    p = HERE + f'/html/{WHICH}/{tag}.html'; open(p, 'w').write(d2); log['files'][tag] = p
json.dump(log, open(HERE + f'/runs/build-{WHICH}.json', 'w'), indent=1, ensure_ascii=False)
print(json.dumps(log['fits26'])); print('\n'.join(sorted(log['files'])))
