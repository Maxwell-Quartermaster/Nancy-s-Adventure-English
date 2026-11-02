# Auditor: write pages 34-36 at the current size (NAE_SE=1 for 320) to <outdir>; same calls as build.py
import sys, os; sys.dont_write_bytecode = True
src, outd = sys.argv[1], sys.argv[2]; sys.argv = ['x']; sys.path.insert(0, os.path.abspath(src))
import play_v608 as PV
os.makedirs(outd, exist_ok=True)
for n, (slug, st, srcd, fn) in sorted(PV.SCR.items()):
    if n in (34, 35, 36): open(f'{outd}/{n:02d}-{slug}.html', 'w', encoding='utf-8').write(PV.page(PV.W, PV.H, fn()))
