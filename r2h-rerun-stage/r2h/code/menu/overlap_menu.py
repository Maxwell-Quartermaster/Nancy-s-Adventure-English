import json, sys, itertools
bad = 0
for f in sys.argv[1:]:
    d = json.load(open(f)); W, H = d['vw'], d['vh']; safe = H - (34 if H == 844 else 0)
    taps = [e for e in d['el'] if e.get('tap') and e.get('c', '').split()[:1] in (['f9'], ['r9'], [])]
    taps = [e for e in taps if 'bb' in e]
    for e in taps:
        x, y, w, h = e['b']
        if x < 16 - .5 or x + w > W - 16 + .5 or y + h > safe + .5 or w < 44 or h < 44: print(f, 'EDGE', e['bb'], e['b']); bad += 1
    for a, b in itertools.combinations(taps, 2):
        ax, ay, aw, ah = a['b']; bx, by, bw, bh = b['b']
        if ax < bx + bw and bx < ax + aw and ay < by + bh and by < ay + ah: print(f, 'OVERLAP', a['bb'], b['bb']); bad += 1
    # text inside its tap target's box
    print(f, len(taps), 'taps')
sys.exit(1 if bad else 0)
