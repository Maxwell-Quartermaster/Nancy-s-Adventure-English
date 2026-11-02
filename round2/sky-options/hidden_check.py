# Hidden-target / edge check for the sky options: every scene target (not HUD/card buttons) must sit wholly below the HUD's bottom edge,
# and 16 pt+ from both sides; also flags scene targets that reach under the card. Uses /tmp/dc1.py taps (domcheck_r2) + stage measure.
import sys, json, re, subprocess
sys.argv = sys.argv[:1] + sys.argv[1:]; sys.path.insert(0, '/workspace/v608build/scenes'); sys.path.insert(0, '/workspace/v608build/screens')
files = sys.argv[1:]; sys.argv = ['x']
import stage_v608 as ST
UI = {'back', 'hearth-flame', 'hint', 'listen', 'btn', 'plate', 'tile'}
out = subprocess.run([sys.executable, '/tmp/dc1.py'] + files, capture_output=True, text=True).stdout.splitlines()
tot = {'hud': 0, 'edge': 0, 'card': 0, 'targets': 0}
for i, f in enumerate(files):
    taps = eval(out[2 * i].split('taps: ', 1)[1]); iss = out[2 * i + 1]
    w, h = map(int, re.search(r'-(\d+)x(\d+)(?:-wallup)?\.html$', f).groups())
    m = ST.measure(open(f).read(), w, h) if (w != 390 or 'data-ui=1' in open(f).read()) else json.load(open(f.split('/html/')[0] + '/measure390.json'))[f.split('/')[-1][:-5]]   # 390 play pages carry no data-ui; the same scene + UI measured at s = 1
    bad = []
    for k, x0, y0, x1, y1 in taps:
        if k in UI: continue
        tot['targets'] += 1
        if y0 < m['top']: bad.append(('underHUD', k, y0, round(m['top']))); tot['hud'] += 1
        if x0 < 16 or x1 > w - 16: bad.append(('edge<16', k, x0, w - x1)); tot['edge'] += 1
        if y1 > m['card']: bad.append(('reachesCard', k, y1, round(m['card']))); tot['card'] += 1
    print(f.split('/')[-1], 'HUD', round(m['top']), 'card', round(m['card']), bad or 'ok', '| dc1', iss.strip())
print('TOTAL', json.dumps(tot))
