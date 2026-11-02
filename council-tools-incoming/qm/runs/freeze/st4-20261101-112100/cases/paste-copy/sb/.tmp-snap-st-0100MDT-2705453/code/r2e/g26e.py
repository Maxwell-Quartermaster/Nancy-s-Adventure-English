# r2e (council steering 11:00 PM MDT, via QM): screen 26 C' tapped at 320 x 568 and 375 x 667, two chips:
#   'frozen' = the r2d chip as frozen ('Words of Jesus ·' + uiText.jesusWords Thai on one flex line), 'br' = a line break between the English and the Thai
#   (0 PASTE chars: the chip label is uiText.jesusWords either way; the ' ·' only separates the two on one line, so the br chip has none).
# Same build as stage_guardian_play.py NAE_G26 (r2d): the chip sits 6 pt under the Guardian banner, the scene fits below the chip, the opened verse sits 12 pt
# under the chip bottom (r2d 320: chip 125-169, verse top 181). Writes round2/r2e/g26e/{html,png}; deletes nothing; screens-v608 and r2d are not touched.
# Run with PYTHONPATH=/tmp/qmtmp/r2e/shim (no-delete shim). Prints the rects and how much of Sam / the heads each opened verse covers.
import sys, os, json, subprocess, re, html as HT
sys.argv = sys.argv[:1]; sys.path.insert(0, '/workspace/v608build/screens'); sys.path.insert(0, '/workspace/v608build/scenes')
MARK = '<!--UI-->'
import play_v608 as PV
Z = PV.Z; _t, _h = PV.top, Z.hud
PV.top = lambda *a, **k: MARK + _t(*a, **k); Z.hud = lambda *a, **k: MARK + _h(*a, **k)
def part26():
    n = 26; slug, st, src, fn = PV.SCR[n]; h = fn(); i = h.index(MARK); return f'{n:02d}-{slug}', h[:i], PV.guardian_chip(h[i:].replace(MARK, ''), n)
UJ = '/tmp/qmtmp/r2e/g26e_ui320.json'
if PV.SE: json.dump(part26()[2], open(UJ, 'w')); sys.exit(0)
name, scene, ui390 = part26()
sv = (PV.W, PV.H); PV.W, PV.H = 375, 667
try: ui375 = part26()[2]
finally: PV.W, PV.H = sv
r = subprocess.run([sys.executable, __file__], env=dict(os.environ, NAE_SE='1'), capture_output=True, text=True); assert r.returncode == 0, r.stderr[-1500:]
ui320 = json.load(open(UJ))
import stage_v608 as ST
G = '/workspace/v608build/round2/r2e/g26e/'
d390 = ST.compose(name, scene, ui390, 390, 844, (1, 0, 0)); m390 = ST.measure(d390, 390, 844); top0 = min(ST.scenery_top(d390, m390['card']), ST.scenery_top(d390.replace("data-pic='plate'", "data-pic='plate' data-deco='plate'"), m390['card']))
BUB = re.search(r"<div class='abs' data-overlay=1 style='left:16px;right:16px;bottom:120px;(.*?)'>(.*?</div>)</div>", ui320, re.S); inner, bst = BUB.group(2), BUB.group(1)
def bubble_span(u):
    k = u.index('z-index:6;box-sizing:border-box;background:#FFF0B8'); k = u.rindex('<div', 0, k); d = 0
    for mm in re.finditer(r'<div\b|</div>', u[k:]):
        d += 1 if mm.group(0) == '<div' else -1
        if d == 0: return k, k + mm.end()
def chip(top, br):
    en, th = PV.u('jesusWords')
    lay = 'display:flex;flex-wrap:wrap;align-items:center;gap:0 6px;' if not br else 'display:flex;flex-direction:column;align-items:flex-start;justify-content:center;'
    return ("<div class='abs' data-chip='jesus' data-tap=1 role='button' style='left:16px;top:%dpx;z-index:6;box-sizing:border-box;min-height:44px;max-width:288px;" % top + lay +
            "background:#FFF0B8;border:2px solid #10170F;border-radius:12px;box-shadow:inset 0 0 0 2px #E8B84A,0 3px 0 #10170F;padding:2px 10px'>"
            "<div class='e15 nw' data-txt=1>" + en + ('' if br else ' ·') + "</div><div class='t17 nw' data-txt=1 style='line-height:1.7'>" + th + "</div></div>")
PROBE = r"""<script>addEventListener('load',function(){setTimeout(function(){function R(e){if(!e)return null;var q=e.getBoundingClientRect();return [Math.round(q.left),Math.round(q.top),Math.round(q.right),Math.round(q.bottom)];}
function mtr(e){var t=1e9,rr=null;if(!e)return null;[e].concat([].slice.call(e.querySelectorAll('*'))).forEach(function(x){var q=x.getBoundingClientRect();if(q.height>0&&q.top<t){t=q.top;rr=x;}});return R(rr);}
var o={},tw=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT,null),n;while(n=tw.nextNode()){if(n.textContent.indexOf('The Word Guardian')>=0&&!o.banner){var p=n.parentElement,b=null;for(var a=p;a&&a!==document.body;a=a.parentElement){var q=a.getBoundingClientRect();if(q.height<90&&q.height>20)b=a;}o.banner=R(b);}}
var s=document.querySelector("[data-hero='sam']");o.sam=R(s);o.samTop=mtr(s);var g=[].filter.call(document.querySelectorAll('div'),function(d){return /scaleX\(-1\)/.test(d.getAttribute('style')||'')&&d.querySelector('svg');});o.guardian=g.length?R(g[0]):null;o.gTop=g.length?mtr(g[0]):null;
o.chip=R(document.querySelector("[data-chip='jesus']"));var c=document.querySelector("[data-chip='jesus']");o.chipLines=c?[].map.call(c.children,R):null;o.verse=R(document.querySelector("[data-verse='open']"));o.pic=R(document.querySelector("[data-pic='plate']"));o.card=R(document.querySelector("[data-name='card']"));
var pre=document.createElement('pre');pre.id='PX';pre.textContent=JSON.stringify(o);document.body.appendChild(pre);},400);});</script>"""
def probe(doc, w, h):
    d = '/dev/shm/qm-r2e/g26e'; os.makedirs(d, exist_ok=True); p = d + '/p-%dx%d-%d.html' % (w, h, os.getpid()); open(p, 'w').write(doc.replace('</body>', PROBE + '</body>'))
    o = ST.run_chrome([f'--window-size={w},{h}', '--dump-dom', 'file://' + p]).stdout   # leaves p in place (delete nothing)
    return json.loads(HT.unescape(re.search(r'<pre id="PX">(.*?)</pre>', o, re.S).group(1)))
def inter(a, b):
    if not a or not b: return 0, 0
    x = max(0, min(a[2], b[2]) - max(a[0], b[0])); y = max(0, min(a[3], b[3]) - max(a[1], b[1])); return x, y
OUT = {}
for (w, h), ui in (((320, 568), ui320), ((375, 667), ui375)):
    a, b = bubble_span(ui); bare = ui[:a] + ui[b:]
    m0 = ST.measure(ST.compose(name, scene, bare, w, h, (1, 0, 0)), w, h)
    ban = probe(ST.compose(name, scene, bare, w, h, (1, 0, 0)), w, h)['banner']; CT = ban[3] + 6   # 320: 119 + 6 = 125 (r2d)
    for br in (False, True):
        k = 'br' if br else 'frozen'; u0 = bare + chip(CT, br)
        cr = probe(ST.compose(name, scene, u0, w, h, (1, 0, 0)), w, h)['chip']; cb = cr[3]   # 320 frozen: 169
        m = ST.measure(ST.compose(name, scene, u0, w, h, (1, 0, 0)), w, h); m['top'] = max(m['top'], cb + 2)   # 320 frozen: 125 + 46 (r2d)
        fit = ST.fit_whole(m390, m, w, h, top0)
        VT = cb + 12   # 320 frozen: 181 (r2d)
        verse = f"<div class='abs' data-overlay=1 data-verse='open' style='left:16px;right:16px;top:{VT}px;{bst}'>{inner}</div>"
        rest = ST.compose(name, scene, u0, w, h, fit); opn = ST.compose(name, scene, u0 + verse, w, h, fit)
        for tag, doc in (('rest', rest), ('open', opn)):
            f = f'26-C-{tag}-{k}-{w}x{h}'; open(G + f'html/{f}.html', 'w').write(doc); ST.shot(doc, G + f'png/{f}.png', w, h)
        r = probe(opn, w, h); s = r['sam']; cx, cy = inter(r['verse'], s); gx, gy = inter(r['verse'], r['guardian'])
        OUT[f'{w}x{h}-{k}'] = dict(scale=round(fit[0], 3), chip=r['chip'], chipLines=r['chipLines'], verse=r['verse'], sam=s, samHeight=s[3] - s[1],
            samCoveredPt=cy, samCoveredPct=round(100.0 * cx * cy / ((s[2] - s[0]) * (s[3] - s[1])), 1), samHeadCovered=r['verse'][3] > s[1], guardianCoveredPt=gy, pic=r['pic'])
        print(f'{w}x{h} {k}: scale {fit[0]:.3f}; chip {r["chip"]} lines {r["chipLines"]}; verse {r["verse"]}; Sam {s} ({s[3]-s[1]} pt tall); verse covers Sam {cy} pt of height ({OUT[f"{w}x{h}-{k}"]["samCoveredPct"]}% of his box); Guardian {gy} pt', flush=True)
json.dump(OUT, open(G + 'measure-c-chip.json', 'w'), indent=1); print(G + 'measure-c-chip.json')
