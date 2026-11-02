# Guardian banner check (9:05 PM MDT follow-up): on guardian screens the drawn scene (data-st: deco, props, heroes, guardian, picture plate)
# (sky, sun and clouds may crop under the HUD) starts below the Guardian banner's bottom edge; also every tap target 16 pt+ from both sides and none under the HUD/banner.
# Usage: python3 banner_check.py <html> ...
import sys, re, json, tempfile, shutil, html as H_
files = sys.argv[1:]; sys.argv = ['x']
sys.path.insert(0, '/workspace/v608build/scenes'); import stage_v608 as ST
JS = """<script>addEventListener('load',()=>{const b=document.querySelector('[data-guardian-hud]');const bb=b?b.getBoundingClientRect().bottom:null;let st=1e9,who='';
for(const e of document.querySelectorAll('[data-st] [data-deco],[data-st] [data-pn],[data-st] [data-hero],[data-st] [data-pic],[data-st] [data-name],[data-st] svg[viewBox="0 0 80 60"]')){const r=e.getBoundingClientRect();if(!r.width||!r.height||e.getAttribute('data-deco')=='tufts')continue;if(r.top<st){st=r.top;who=e.getAttribute('data-deco')||e.getAttribute('data-pn')||e.getAttribute('data-pic')||e.getAttribute('data-name')||(e.hasAttribute('data-hero')?'hero':'guardian helmet')}}
const taps=[];for(const e of document.querySelectorAll('[data-tap],[data-hit]')){const r=e.getBoundingClientRect();if(r.width)taps.push([e.getAttribute('data-name')||'tap',r.left,r.right,r.top])}
const hh=[...document.querySelectorAll('[data-st] [data-hero]')].map(e=>Math.round(e.getBoundingClientRect().height));const p=document.createElement('pre');p.id='bbout';p.textContent=JSON.stringify({bb,st,who,taps,hh});document.body.appendChild(p)})</script>"""
bad = 0
for f in files:
    w, h = map(int, re.search(r'-(\d+)x(\d+)\.html$', f).groups())
    d = tempfile.mkdtemp(prefix='gbc-', dir='/tmp/qmtmp'); p = d + '/m.html'; open(p, 'w').write(open(f).read().replace('</body>', JS + '</body>'))
    try: o = ST.run_chrome([f'--window-size={w},{h}', '--dump-dom', 'file://' + p]).stdout
    finally: shutil.rmtree(d, ignore_errors=True)
    r = json.loads(H_.unescape(re.search(r'<pre id="bbout">(.*?)</pre>', o, re.S).group(1)))
    iss = []
    if r['bb'] is None: iss.append('no Guardian banner')
    elif r['st'] < r['bb'] - 0.5: iss.append(f"scene {r['who']} top {r['st']:.0f} above banner bottom {r['bb']:.0f}")
    for k, l, rt, t in r['taps']:
        if k in ('back', 'hearth-flame'): continue
        if l < 16 - .5 or rt > w - 16 + .5: iss.append(f'{k} edge {l:.0f}/{w - rt:.0f}')
        if r['bb'] is not None and t < r['bb']: iss.append(f'{k} under the banner')
    bad += len(iss); print(f.split('/')[-1], f"banner bottom {r['bb']:.0f}, scene top {r['st']:.0f} ({r['who']}), hero {r['hh']} pt", 'ok' if not iss else iss)
print('TOTAL banner/edge issues:', bad)
