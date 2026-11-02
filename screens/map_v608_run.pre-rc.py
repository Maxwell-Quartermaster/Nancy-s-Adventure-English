# Map choosers 07/08 from v604build/screens/map_v604.py (read-only) with the v6-08 cards and Sam's happy eyes.
# Fixes (Auditor gate 1975f0b8; Watchman sweep P9): 'Coming next' sits inside its row plate (right-aligned, no clipping); the Home Lake bubble opens upward so it never covers the hero strip.
import sys, json
s = open('/workspace/v604build/screens/map_v604.py', encoding='utf-8').read()
for a, b in [("OUT = '/workspace/v604build/screens/'", "OUT = '/workspace/screens-v608/'"), ("nancys-adventure-english-v6-04-cards.json", "nancys-adventure-english-v6-08-cards.json"),
             ("cn = (\"<div class='cn' data-txt=1>", "cn = (\"<div class='cn' data-txt=1 style='position:static;transform:none;width:auto;white-space:nowrap;padding:1px 6px;margin-left:auto;margin-right:8px;flex:none'>"),
             ("    bx, by, bw = 22, ry + rh + 12, 346\n", "    bx, by, bw = 22, ry + rh + 12, 346\n    if region_i == 2: by = ry - (len(zones)*72 + 26) - 8   # opens upward: bottom 8 px above the row, clear of the hero strip\n")]:
    assert s.count(a) == 1, a; s = s.replace(a, b)
s = s[:s.index("if __name__ == '__main__':")]
sys.path.insert(0, '/workspace/v608build/eyes'); import eyes_v608 as EY
g = {'__name__': 'map_v608'}; exec(compile(s, 'map_v608', 'exec'), g)
for n in (7, 8):
    slug, st, src, fn = g['SCR'][n]; doc = EY.apply(fn())[0]
    open(g['OUT'] + f'html/{n:02d}-{slug}.html', 'w').write(doc); g['T'].shot(doc, g['OUT'] + f'png/{n:02d}-{slug}.png', 390, 844, f'/tmp/v608m-{n}.html'); print(n, slug)
