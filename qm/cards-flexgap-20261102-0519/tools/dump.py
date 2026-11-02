# dump selected pages' html: python3 -B dump.py <srcdir> <390|375|320> <outdir> n1 n2 ...
import sys, os; sys.dont_write_bytecode = True
src, size, od = sys.argv[1], sys.argv[2], sys.argv[3]; ns = [int(x) for x in sys.argv[4:]]
sys.argv = ['x']; sys.path.insert(0, os.path.abspath(src)); import play_v608 as PV
W, H = {'390': (390, 844), '375': (375, 667), '320': (320, 568)}[size]
if size == '375': PV.W, PV.H = 375, 667
os.makedirs(od, exist_ok=True)
for n, (slug, st, srcd, fn) in sorted(PV.SCR.items()):
    if n in ns:
        d = PV.page(W, H, fn())
        if 24 <= n <= 28: d = PV.guardian_chip(d, n)
        open(f'{od}/{n:02d}-{slug}-{W}x{H}.html', 'w', encoding='utf-8').write(d)
