# Auditor: write chosen SCR pages (same calls as build.py, incl. guardian_chip on 24-28) to <outdir>
import sys, os; sys.dont_write_bytecode = True
src, outd, pages = sys.argv[1], sys.argv[2], [int(x) for x in sys.argv[3].split(',')]; sys.argv = ['x']; sys.path.insert(0, os.path.abspath(src))
import play_v608 as PV
W, H = (320, 568) if PV.SE else (390, 844); os.makedirs(outd, exist_ok=True)
for n, (slug, st, srcd, fn) in sorted(PV.SCR.items()):
    if n in pages:
        d = PV.page(W, H, fn())
        if 24 <= n <= 28: d = PV.guardian_chip(d, n)
        open(f'{outd}/{n:02d}-{slug}.html', 'w', encoding='utf-8').write(d)
