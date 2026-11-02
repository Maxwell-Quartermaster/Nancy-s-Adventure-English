# Sidecar JSON per PNG, read from the live DOM at capture time (parent steer 00:39 MDT).
import json, os, sys, hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import cdp_shot as C
SNAP = 'pointer f6dac2d0 (base snap-r2h-0021MDT; renders feed the next freeze)'; PASTE = '317e91ce86f073c961f8169183d2bbd3'
JS = r"""(()=>{const W=innerWidth,H=innerHeight,o=[];
const tap=e=>e.matches('button,a,[onclick],[role=button],[data-tap]');
for(const e of document.querySelectorAll('body *')){ if(e.closest('svg')&&e.tagName.toLowerCase()!=='svg')continue;
 const t=e.tagName.toLowerCase(); if(t==='i'||t==='b'||t==='style'||t==='script'||t==='defs')continue;
 const r=e.getBoundingClientRect(); if(r.width<1||r.height<1||r.right<=0||r.bottom<=0||r.left>=W||r.top>=H)continue;
 const cs=getComputedStyle(e); if(cs.visibility==='hidden'||cs.display==='none'||+cs.opacity===0)continue;
 let own=''; for(const n of e.childNodes) if(n.nodeType===3) own+=n.textContent; own=own.trim();
 const bb=e.getAttribute('data-bb')||e.getAttribute('data-name')||'', ip=tap(e);
 if(!own&&!bb&&!e.id&&!ip&&!e.getAttribute('role'))continue;
 const x={t:t,b:[+r.x.toFixed(1),+r.y.toFixed(1),+r.width.toFixed(1),+r.height.toFixed(1)]};
 if(e.id)x.id=e.id; if(bb)x.bb=bb; const c=(e.getAttribute('class')||'').trim(); if(c)x.c=c; const ro=e.getAttribute('role'); if(ro)x.role=ro;
 if(own)x.txt=own.slice(0,80); if(cs.transform&&cs.transform!=='none'){x.tf=cs.transform; const m=cs.transform.match(/matrix\(([^,]+),\s*([^,]+)/); if(m)x.rot=+(Math.atan2(+m[2],+m[1])*180/Math.PI).toFixed(2);}
 if(cs.zIndex!=='auto')x.z=+cs.zIndex; if(ip)x.tap=1; o.push(x);}
return JSON.stringify({vw:W,vh:H,el:o});})()"""
def shot(ws, html, png, w, h, wait=1.2, js=None):
    r = C.shot(ws, html, png, w, h, wait, (js + ';' if js else '') + JS)
    d = json.loads(r); d = {'vw': d['vw'], 'vh': d['vh'], 'snap': SNAP, 'paste_md5': PASTE, 'html': os.path.basename(html), 'html_md5': hashlib.md5(open(html, 'rb').read()).hexdigest(), 'html_md5_src': 'render', 'png': os.path.basename(png), 'png_md5': hashlib.md5(open(png, 'rb').read()).hexdigest(), 'el': d['el']}
    open(os.path.splitext(png)[0] + '.json', 'w').write(json.dumps(d, ensure_ascii=False, separators=(',', ':')))
    return d
