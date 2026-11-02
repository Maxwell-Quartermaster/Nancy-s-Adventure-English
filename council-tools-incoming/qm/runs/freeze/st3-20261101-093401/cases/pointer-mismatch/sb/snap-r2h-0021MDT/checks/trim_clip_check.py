# Trim-band clip check (Auditor: the DOM check misses targets cut by the 3B ceiling trim). In a trimmed render the real scene layer carries
# clip-path:inset(<mb>px 0 0 0): anything drawn above design y <mb> is hidden (only an inert, non-tappable copy may show in the ceiling strip).
# Flags every target (data-tap / data-hit / data-pn / data-name / data-pic plate) inside that layer whose box starts above the clip line.
# Usage: python3 trim_clip_check.py <html> ...   -> one line per file, then TOTAL
import sys, re, json, tempfile, shutil, html as H_
files = sys.argv[1:] if __name__ == '__main__' else []; _argv = sys.argv; sys.argv = ['x']
sys.path.insert(0, '/workspace/v608build/scenes'); import stage_v608 as ST
sys.argv = _argv if __name__ != '__main__' else sys.argv   # leave an importer's argv alone
JS = """<script>addEventListener('load',()=>{const out=[];
for(const L of document.querySelectorAll('div')){const m=(L.getAttribute('style')||'').match(/clip-path:inset\\(([0-9.]+)px 0 0 0\\)/);if(!m)continue;
 const r=L.getBoundingClientRect(),sc=r.height/844,cl=r.top+parseFloat(m[1])*sc;
 for(const e of L.querySelectorAll('[data-tap],[data-hit],[data-pn],[data-name],[data-pic]')){const b=e.getBoundingClientRect();if(!b.width||!b.height)continue;
  if(b.top<cl-0.5)out.push([e.getAttribute('data-name')||e.getAttribute('data-pn')||e.getAttribute('data-pic')||'tap',Math.round(b.top),Math.round(b.bottom),Math.round(cl)])}}
const p=document.createElement('pre');p.id='bbout';p.textContent=JSON.stringify(out);document.body.appendChild(p)})</script>"""
def clipped(doc, w, h):
    d = tempfile.mkdtemp(prefix='tcc-', dir='/tmp/qmtmp'); p = d + '/m.html'; open(p, 'w').write(doc.replace('</body>', JS + '</body>'))
    try: o = ST.run_chrome([f'--window-size={w},{h}', '--dump-dom', 'file://' + p]).stdout
    finally: shutil.rmtree(d, ignore_errors=True)
    return json.loads(H_.unescape(re.search(r'<pre id="bbout">(.*?)</pre>', o, re.S).group(1)))
tot = 0
for f in files:
    w, h = map(int, re.search(r'-(\d+)x(\d+)', f.split('/')[-1]).groups()) if re.search(r'-(\d+)x(\d+)', f.split('/')[-1]) else (390, 844)
    bad = clipped(open(f).read(), w, h); tot += len(bad)
    print(f.split('/')[-1], 'CLIPPED' if bad else 'ok', bad if bad else '')
if __name__ == '__main__': print('TOTAL clipped targets:', tot)
