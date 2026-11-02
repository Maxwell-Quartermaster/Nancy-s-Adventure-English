# fit320.py <srcdir> <outdir>: the shipped 320x568 fit-to-width docs for 34-36 = snap-r2h-0021MDT renders/screens/<n>-320x568.html with its
# 320 UI layer (play_v608 SE output after top()) swapped for <srcdir>'s; stage_v608.compose's fit depends on HUD/card only, not the plate.
import sys, os, glob; sys.dont_write_bytecode = True
src, od = sys.argv[1], sys.argv[2]; sys.argv = ['x']; sys.path.insert(0, os.path.abspath(src)); os.environ['NAE_SE'] = '1'
import play_v608 as PV; assert PV.SE
MARK = '<!--UI-->'; Z = PV.Z; _t = PV.top; PV.top = lambda *a, **k: MARK + _t(*a, **k)
B = '/workspace/qm/fix-320-20261102-0457/base'; os.makedirs(od, exist_ok=True)
import importlib.util
def ui(mod, n): slug, st, s_, fn = mod.SCR[n]; h = fn(); return slug, h[h.index(MARK) + len(MARK):]
spec = importlib.util.spec_from_file_location('pv_base', B + '/play_v608.py'); PB = importlib.util.module_from_spec(spec); spec.loader.exec_module(PB)
_tb = PB.top; PB.top = lambda *a, **k: MARK + _tb(*a, **k)
for n in (34, 35, 36):
    slug, unew = ui(PV, n); _, ubase = ui(PB, n)
    snap = open(f'/workspace/v608build/snap-r2h-0021MDT/renders/screens/{n}-{slug}-320x568.html', encoding='utf-8').read()
    c = snap.count(ubase); print(n, slug, 'base UI found in snap doc:', c, '; UI changed:', ubase != unew)
    assert c == 1
    open(f'{od}/{n}-{slug}-320x568.html', 'w', encoding='utf-8').write(snap.replace(ubase, unew))
