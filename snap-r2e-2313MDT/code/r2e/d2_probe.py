# r2e: re-probe the D2 sky renders already written by d2_mock.py (plate vs every tap target); render-free, deletes nothing.
import sys, json, re, glob
sys.argv = sys.argv[:1]; exec(open('/workspace/v608build/round2/r2e/d2_mock.py').read().split("UJ = ")[0].split('import play_v608')[0])
sys.path.insert(0, '/workspace/v608build/scenes'); import stage_v608 as ST, os, html as HT
src = open('/workspace/v608build/round2/r2e/d2_mock.py').read(); PROBE = re.search(r'PROBE = (r""".*?""")', src, re.S).group(1); PROBE = eval(PROBE)
def probe(doc, w, h):
    d = '/dev/shm/qm-r2e/d2'; os.makedirs(d, exist_ok=True); p = d + '/q-%dx%d-%d.html' % (w, h, os.getpid()); open(p, 'w').write(doc.replace('</body>', PROBE + '</body>'))
    return json.loads(HT.unescape(re.search(r'<pre id="PX">(.*?)</pre>', ST.run_chrome([f'--window-size={w},{h}', '--dump-dom', 'file://' + p]).stdout, re.S).group(1)))
res = json.load(open('/workspace/v608build/round2/r2e/d2/d2-measure.json'))
for f in sorted(glob.glob('/workspace/v608build/round2/r2e/d2/html/zone-*-D2plate-*.html')):
    k = f.split('zone-')[1].split('-')[0]; w, h = map(int, re.search(r'(\d+)x(\d+)\.html', f).groups())
    r = probe(open(f).read(), w, h); pl = r['pic']
    hits = [(t, q) for t, q in r['taps'] if q and t not in ('back', 'hearth-flame') and not (pl[0] >= q[2] or pl[2] <= q[0] or pl[1] >= q[3] or pl[3] <= q[1])]
    res['sky'][k][f'{w}x{h}'] = dict(plate=pl, hits=hits, taps=r['taps']); print(f.split('/')[-1], 'plate', pl, 'covers', hits or 'none', '| targets', [(t, q) for t, q in r['taps'] if t in ('kite', 'owl', 'lantern')])
json.dump(res, open('/workspace/v608build/round2/r2e/d2/d2-measure.json', 'w'), indent=1, ensure_ascii=False)
