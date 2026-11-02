# List the html renders for Auditor's occl.py (b798bdf0): "<file> <w> <h>" per line. Sizes from -WxH in the name, else 390 x 844.
import glob, re
G = ['/workspace/screens-v608/html/*.html', '/workspace/v608build/scenes/stage/html/*.html', '/workspace/v608build/round2/ceiling-cap/html/*.html',
     '/workspace/v608build/round2/ceiling-cap/home-lake/html/*.html', '/workspace/v608build/round2/ceiling-cap/home-lake/png-r2ask/html/*.html',
     '/workspace/v608build/round2/sky-options/B/html/*.html', '/workspace/v608build/round2/sky-options/B/png-r2ask/html/*.html',
     '/workspace/v608build/round2/showcase/tiles/*.html', '/workspace/v608build/scenes/tod/*.html']
for g in G:
    for f in sorted(glob.glob(g)):
        m = re.search(r'-(\d{3})x?(\d{3})?(?:-[a-z]+)?\.html$', f); m2 = re.search(r'-(\d+)x(\d+)', f.rsplit('/', 1)[1])
        w, h = (int(m2.group(1)), int(m2.group(2))) if m2 else ((320, 568) if f.endswith('-320.html') else (390, 844))
        print(f, w, h)
