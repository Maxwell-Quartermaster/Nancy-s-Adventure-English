# r2d: rendered rects for the 26 layout checks (banner, Sam, Guardian, card, plates, the Jesus bubble and its scroll). Usage: rects26.py <html> <w> <h> -> JSON
import subprocess, re, sys, os, json, html as H, tempfile
JS = r"""<script>window.addEventListener('load',function(){setTimeout(function(){
function R(e){if(!e)return null;var q=e.getBoundingClientRect();return [Math.round(q.left),Math.round(q.top),Math.round(q.right),Math.round(q.bottom)];}
var o={};var tw=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT,null),n;
while(n=tw.nextNode()){if(n.textContent.indexOf('The Word Guardian')>=0&&!o.banner){var p=n.parentElement,b=null;for(var a=p;a&&a!==document.body;a=a.parentElement){var q=a.getBoundingClientRect();if(q.height<90&&q.height>20)b=a;}o.banner=R(b);}
 if(n.textContent.trim()=='คิด'){o.kid=R(n.parentElement);}}
o.sam=R(document.querySelector("[data-hero='sam']"));
var g=[].filter.call(document.querySelectorAll('div'),function(d){return /scaleX\(-1\)/.test(d.getAttribute('style')||'')&&d.querySelector('svg');});o.guardian=g.length?R(g[0]):null;function mt(e){var t=1e9;if(!e)return null;[e].concat([].slice.call(e.querySelectorAll('*'))).forEach(function(x){var q=x.getBoundingClientRect();if(q.height>0&&q.top<t)t=q.top;});return Math.round(t);}o.gtop=g.length?mt(g[0]):null;function mtr(e){var t=1e9,rr=null;if(!e)return null;[e].concat([].slice.call(e.querySelectorAll('*'))).forEach(function(x){var q=x.getBoundingClientRect();if(q.height>0&&q.top<t){t=q.top;rr=x;}});return R(rr);}o.gheadRect=g.length?mtr(g[0]):null;o.sheadRect=mtr(document.querySelector("[data-hero='sam']"));o.stop=mt(document.querySelector("[data-hero='sam']"));
o.card=R(document.querySelector("[data-name='card']"));o.plates=[].map.call(document.querySelectorAll("[data-name='plate']"),R);
o.pic=R(document.querySelector("[data-pic='plate']"));var bb=document.querySelector("[data-bubble='jesus']")||[].filter.call(document.querySelectorAll('div'),function(d){return /background:#FFF0B8/.test(d.getAttribute('style')||'')&&/Words of Jesus/.test(d.textContent)&&!d.hasAttribute('data-chip');})[0];
if(bb){o.bubble=R(bb);o.bubbleScroll=[bb.scrollHeight,bb.clientHeight];var th=[].filter.call(bb.querySelectorAll('div'),function(d){return /[\u0E00-\u0E7F]/.test(d.textContent)&&!d.querySelector('div');});o.thai=th.map(function(d){var cs=getComputedStyle(d);return [cs.fontSize,cs.lineHeight];});var hd=bb.querySelector('div');o.head=[hd.textContent,getComputedStyle(hd).cursor,hd.hasAttribute('data-tap')||hd.getAttribute('role')=='button'];var th0=th.length?th[0]:null;if(th0){var bq=bb.getBoundingClientRect(),tq=th0.getBoundingClientRect();o.thaiTop=Math.round(tq.top-bq.top+bb.scrollTop);o.padB=parseFloat(getComputedStyle(bb).paddingBottom)+parseFloat(getComputedStyle(bb).borderBottomWidth);o.thaiLH=parseFloat(getComputedStyle(th0).lineHeight);}}
var pre=document.createElement('pre');pre.id='RX';pre.textContent=JSON.stringify(o);document.body.appendChild(pre);},400);});</script>"""
def rects(f, w, h):
    s = open(f).read(); s = s.replace('</body>', JS + '</body>') if '</body>' in s else s + JS
    d = '/tmp/qmtmp/rx'; os.makedirs(d, exist_ok=True); p = d + '/x.html'; open(p, 'w').write(s)
    r = subprocess.run(['google-chrome', '--headless=new', '--no-sandbox', '--disable-gpu', '--virtual-time-budget=2000', f'--window-size={w},{h}', '--dump-dom', 'file://' + p], capture_output=True, text=True, timeout=120, env=dict(os.environ, TMPDIR=d))
    os.remove(p)   # only the file this script wrote; the empty dir stays (delete nothing else)
    return json.loads(H.unescape(re.search(r'<pre id="RX">(.*?)</pre>', r.stdout, re.S).group(1)))
if __name__ == '__main__': print(json.dumps(rects(sys.argv[1], int(sys.argv[2]), int(sys.argv[3])), ensure_ascii=False))
