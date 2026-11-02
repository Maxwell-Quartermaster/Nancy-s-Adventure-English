# r2e D2 mock (Watchman, via QM 11:00 PM MDT brief task 6): screen 26 D with the 🤔 plate moved DOWN out of its spec 7.x spot
# ("a 124 pt framed plate at the top right", PASTE :246) so the Words of Jesus bubble can run full width under the banner.
# Drop = the smallest design drop that puts the plate 8 pt under the full-width bubble at 320 x 568, 375 x 667 and 390 x 844 (bubble capped 10 pt above the
# highest head under it, as D). The same plate spot is injected into every sky-target scene (kite, owl, lantern) at the three sizes for occl.
# Writes round2/r2e/d2/{html,png}; deletes nothing (run with PYTHONPATH=/tmp/qmtmp/r2e/shim); r2d, screens-v608 and the PASTE are not touched.
import sys, os, json, subprocess, re, html as HT
sys.argv = sys.argv[:1]; sys.path.insert(0, '/workspace/v608build/screens'); sys.path.insert(0, '/workspace/v608build/scenes')
MARK = '<!--UI-->'
import play_v608 as PV
Z = PV.Z; _t, _h = PV.top, Z.hud
PV.top = lambda *a, **k: MARK + _t(*a, **k); Z.hud = lambda *a, **k: MARK + _h(*a, **k)
def split(h): i = h.index(MARK); return h[:i], h[i:].replace(MARK, '')
def get(w, h):
    sv = (PV.W, PV.H); PV.W, PV.H = w, h
    try:
        slug, st, src, fn = PV.SCR[26]; sc, ui = split(fn()); out = {'26': (f'26-{slug}', sc, PV.guardian_chip(ui, 26))}
        for k in ('meadow', 'forest'): out[k] = (f'zone-{k}-ask',) + split(Z.screen(k, 'ask', PV.W, PV.H))
        return out
    finally: PV.W, PV.H = sv
UJ = '/tmp/qmtmp/r2e/d2_ui320.json'
if PV.SE: json.dump({k: v[2] for k, v in get(PV.W, PV.H).items()}, open(UJ, 'w')); sys.exit(0)
P390 = get(390, 844); P667 = get(375, 667)
r = subprocess.run([sys.executable, __file__], env=dict(os.environ, NAE_SE='1'), capture_output=True, text=True); assert r.returncode == 0, r.stderr[-1500:]
U320 = json.load(open(UJ))
import stage_v608 as ST
G = '/workspace/v608build/round2/r2e/d2/'
PL0 = "data-pic='plate' style='left:262px;top:234px;"
def plate_at(scene, top):
    if PL0 in scene: return scene.replace(PL0, f"data-pic='plate' style='left:262px;top:{top}px;", 1)
    return scene + ("<div class='abs' data-pic='plate' style='left:262px;top:%dpx;width:104px;height:104px;display:flex;align-items:center;justify-content:center;box-sizing:border-box;"
                    "background:#F6E9C8;border:3px solid #10170F;border-radius:18px;box-shadow:inset 0 0 0 3px #E8B84A,0 3px 0 #10170F;font:400 62px/1 sans-serif'>🤔</div>" % top)
PROBE = r"""<script>addEventListener('load',function(){setTimeout(function(){function R(e){if(!e)return null;var q=e.getBoundingClientRect();return [Math.round(q.left),Math.round(q.top),Math.round(q.right),Math.round(q.bottom)];}
function mtr(e){var t=1e9,rr=null;if(!e)return null;[e].concat([].slice.call(e.querySelectorAll('*'))).forEach(function(x){var q=x.getBoundingClientRect();if(q.height>0&&q.top<t){t=q.top;rr=x;}});return R(rr);}
var o={},tw=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT,null),n;while(n=tw.nextNode()){if(n.textContent.indexOf('The Word Guardian')>=0&&!o.banner){var p=n.parentElement,b=null;for(var a=p;a&&a!==document.body;a=a.parentElement){var q=a.getBoundingClientRect();if(q.height<90&&q.height>20)b=a;}o.banner=R(b);}}
var s=document.querySelector("[data-hero='sam']");o.sam=R(s);o.samTop=mtr(s);var g=[].filter.call(document.querySelectorAll('div'),function(d){return /scaleX\(-1\)/.test(d.getAttribute('style')||'')&&d.querySelector('svg');});o.guardian=g.length?R(g[0]):null;o.gTop=g.length?mtr(g[0]):null;
o.pic=R(document.querySelector("[data-pic='plate']"));var bb=document.querySelector("[data-bubble='jesus']");if(bb){o.bubble=R(bb);o.scroll=[bb.scrollHeight,bb.clientHeight];var th=[].filter.call(bb.querySelectorAll('div'),function(d){return /[\u0E00-\u0E7F]/.test(d.textContent)&&!d.querySelector('div');})[0];if(th){o.thaiTop=Math.round(th.getBoundingClientRect().top-bb.getBoundingClientRect().top+bb.scrollTop);o.thaiLH=parseFloat(getComputedStyle(th).lineHeight);o.padB=parseFloat(getComputedStyle(bb).paddingBottom)+parseFloat(getComputedStyle(bb).borderBottomWidth);}}
o.taps=[].map.call(document.querySelectorAll('[data-tap][data-name]'),function(e){return [e.getAttribute('data-name'),R(e)];});
var pre=document.createElement('pre');pre.id='PX';pre.textContent=JSON.stringify(o);document.body.appendChild(pre);},400);});</script>"""
def probe(doc, w, h):
    d = '/dev/shm/qm-r2e/d2'; os.makedirs(d, exist_ok=True); p = d + '/p-%dx%d-%d.html' % (w, h, os.getpid()); open(p, 'w').write(doc.replace('</body>', PROBE + '</body>'))
    return json.loads(HT.unescape(re.search(r'<pre id="PX">(.*?)</pre>', ST.run_chrome([f'--window-size={w},{h}', '--dump-dom', 'file://' + p]).stdout, re.S).group(1)))
def bubble_span(u):
    k = u.index('z-index:6;box-sizing:border-box;background:#FFF0B8'); k = u.rindex('<div', 0, k); d = 0
    for mm in re.finditer(r'<div\b|</div>', u[k:]):
        d += 1 if mm.group(0) == '<div' else -1
        if d == 0: return k, k + mm.end()
j = PV.D['jesusWords'][0]
BST = "z-index:6;box-sizing:border-box;background:#FFF0B8;border:2px solid #10170F;border-radius:14px;box-shadow:inset 0 -14px 10px -12px rgba(58,36,16,.45),inset 0 0 0 3px #E8B84A,inset 0 0 0 4px #10170F,0 4px 0 #10170F;padding:10px 12px"
inner = PV.tx(PV.u('jesusWords')[0] + ' · ' + j['ref'], 'e15') + PV.tx(j['en'], 'e15') + PV.tx(j['th'], 't17', 'line-height:1.7')
name, scene390, ui390 = P390['26']
d390 = ST.compose(name, scene390, ui390, 390, 844, (1, 0, 0)); m390 = ST.measure(d390, 390, 844); top0 = min(ST.scenery_top(d390, m390['card']), ST.scenery_top(d390.replace("data-pic='plate'", "data-pic='plate' data-deco='plate'"), m390['card']))
SIZES = [((320, 568), U320['26']), ((375, 667), P667['26'][2]), ((390, 844), ui390)]
# pass 1: the fit (same as D: the bubble is hidden when the scene is fitted) and the full-width bubble's cap at each size
geo = {}
for (w, h), ui in SIZES:
    a, b = bubble_span(ui); bare = ui[:a] + ui[b:]
    fit = (1, 0, 0) if (w, h) == (390, 844) else ST.fit_whole(m390, ST.measure(ST.compose(name, scene390, bare, w, h, (1, 0, 0)), w, h), w, h, top0)
    r = probe(ST.compose(name, scene390, bare, w, h, fit), w, h)
    T = r['banner'][3] + 6; heads = [hr for hr in (r['samTop'], r['gTop']) if hr and hr[0] < w - 16 and hr[2] > 16]; cap = min(hr[1] for hr in heads) - 6 - 4 - T
    need_top = T + cap + 4 + 8   # plate top on screen: 8 pt under the bubble incl. its 4 pt drop
    geo[(w, h)] = dict(fit=fit, bare=bare, T=T, cap=cap, need_design=(need_top - fit[2]) / fit[0], plate0=r['pic'], heads=heads)
    print(f'{w}x{h}: scale {fit[0]:.3f} oy {fit[2]:.1f}; bubble top {T} cap {cap}; plate must start at screen y {need_top} = design {(need_top - fit[2]) / fit[0]:.1f}; plate now {r["pic"]}', flush=True)
TOP = int(-(-max(g['need_design'] for g in geo.values()) // 1)); DROP = TOP - 234
print(f'D2 plate: design top {TOP} (drop {DROP} design pt from 234)', flush=True)
res = {'drop': DROP, 'top': TOP, 'sizes': {}}
for (w, h), ui in SIZES:
    g = geo[(w, h)]; sc = plate_at(scene390, TOP)
    bub = f"<div class='abs' data-overlay=1 data-bubble='jesus' data-scroll='jesus' style='left:16px;right:16px;top:{g['T']}px;max-height:{g['cap']}px;overflow-y:auto;-webkit-overflow-scrolling:touch;{BST}'>{inner}</div>"
    doc = ST.compose(name, sc, g['bare'] + bub, w, h, g['fit']); f = f'26-D2-{w}x{h}'
    open(G + f'html/{f}.html', 'w').write(doc); ST.shot(doc, G + f'png/{f}.png', w, h)
    r = probe(doc, w, h); need2 = r['thaiTop'] + 2 * r['thaiLH'] + r['padB']
    res['sizes'][f'{w}x{h}'] = dict(bubble=r['bubble'], scroll=r['scroll'], need2=round(need2, 1), cap=g['cap'], fits2=need2 <= g['cap'], pic=r['pic'], sam=r['sam'], samTop=r['samTop'], guardian=r['guardian'], gTop=r['gTop'])
    print(f'{f}: bubble {r["bubble"]} visible {r["scroll"][1]} of {r["scroll"][0]}; 2 Thai lines need {need2:.0f} vs cap {g["cap"]} -> ' + ('fit' if need2 <= g['cap'] else f'{need2 - g["cap"]:.0f} pt short') + f'; plate {r["pic"]}; Sam {r["sam"]}; Guardian {r["guardian"]} (helmet top {r["gTop"]})', flush=True)
# sky-target scenes: the plate at the D2 spot (design top TOP, x 262-366) in the meadow (kite) and forest (owl, lantern) ask scenes
U = {'meadow': {}, 'forest': {}}
for k in ('meadow', 'forest'):
    nm, sc390, u390 = P390[k]; sc = plate_at(sc390, TOP)
    mm390 = ST.measure(ST.compose(nm, sc390, u390, 390, 844, (1, 0, 0)), 390, 844)
    for (w, h), ui in (((320, 568), U320[k]), ((375, 667), P667[k][2]), ((390, 844), u390)):
        if (w, h) == (390, 844): doc = PV.page(390, 844, sc + ui)
        else:
            m = ST.measure(ST.compose(nm, sc390, ui, w, h, (1, 0, 0)), w, h); s = ST.fit_capped(sc390, mm390, m, w, h)[0]
            doc = ST.compose(nm, sc, ui, w, h, (s, (w - 390 * s) / 2, m['card'] - mm390['card'] * s))
        f = f'{nm}-D2plate-{w}x{h}'; open(G + f'html/{f}.html', 'w').write(doc); ST.shot(doc, G + f'png/{f}.png', w, h)
        r = probe(doc, w, h); pl = r['pic']
        hits = [(t, q) for t, q in r['taps'] if q and t not in ('back', 'hearth-flame') and not (pl[0] >= q[2] or pl[2] <= q[0] or pl[1] >= q[3] or pl[3] <= q[1])]
        U[k][f'{w}x{h}'] = dict(plate=pl, hits=hits, taps=r['taps']); print(f'{f}: plate {pl}; covers targets {hits or "none"}', flush=True)
res['sky'] = U
json.dump(res, open(G + 'd2-measure.json', 'w'), indent=1, ensure_ascii=False); print(G + 'd2-measure.json')
