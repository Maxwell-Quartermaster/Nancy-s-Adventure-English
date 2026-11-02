# QM play-verse-fix: screenshots + layout facts for html/<which>/*.html through one CDP Chrome (snap code/r2h/cdp_shot.py WS client and shot()),
# profile and TMPDIR inside scratch/ (relative TMPDIR: the socket-length limit). Records the real viewport (innerWidth/innerHeight/DPR) per render.
# Usage: python3 shoot.py old|new   -> png/<which>/*.png, runs/shots-<which>.json. Nothing deleted; Chrome is left to exit when this script ends.
import sys, os, json, glob, re, subprocess, time, urllib.request
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); WHICH = sys.argv[1]; SCR = HERE + '/scratch/'
os.chdir(SCR); os.environ['TMPDIR'] = 'tmp'
sys.path.insert(0, '/workspace/v608build/snap-r2h-0021MDT/code/r2h'); import cdp_shot as C
C.PORT = 9361
prof = SCR + f'cdp-prof-{WHICH}'; os.makedirs(prof, exist_ok=True)
p = subprocess.Popen(['google-chrome', '--headless=new', '--no-sandbox', '--disable-gpu', '--hide-scrollbars', '--no-first-run', f'--remote-debugging-port={C.PORT}',
                      f'--user-data-dir={prof}', 'about:blank'], env=dict(os.environ, TMPDIR='tmp'), cwd=SCR, stdout=subprocess.DEVNULL, stderr=open(SCR + f'chrome-stderr-{WHICH}.txt', 'w'))
for _ in range(100):
    try: urllib.request.urlopen(f'http://127.0.0.1:{C.PORT}/json/version', timeout=1); break
    except Exception: time.sleep(.2)
else: raise SystemExit('chrome did not start')
ver = json.load(urllib.request.urlopen(f'http://127.0.0.1:{C.PORT}/json/version'))['Browser']
ws = C.session()
JS = r"""(()=>{const card=document.querySelector("[data-name='card']");const cr=card?card.getBoundingClientRect():null;
const TH=/[\u0E00-\u0E7F]/;const out={iw:innerWidth,ih:innerHeight,dpr:devicePixelRatio,docW:document.documentElement.scrollWidth,card:cr&&[cr.left,cr.top,cr.right,cr.bottom],thai:[],outside:[],btn:[]};
const btns=[...(card?card.querySelectorAll('[data-tap]'):[])].map(b=>b.getBoundingClientRect());
for(const e of document.querySelectorAll('[data-txt]')){if(e.querySelector('[data-txt]'))continue;let r=e.getBoundingClientRect();if(!r.width)continue;const sb=e.closest('[data-verse-scroll]');if(sb){const q=sb.getBoundingClientRect();r={left:Math.max(r.left,q.left),right:Math.min(r.right,q.right),top:Math.max(r.top,q.top),bottom:Math.min(r.bottom,q.bottom),width:r.width,height:r.height};if(r.bottom<=r.top)continue;}const t=e.textContent;const cs=getComputedStyle(e);
 const inCard=card&&card.contains(e);
 if(TH.test(t))out.thai.push({t:t.slice(0,24),fs:cs.fontSize,lh:cs.lineHeight,lhRatio:(parseFloat(cs.lineHeight)/parseFloat(cs.fontSize)).toFixed(3),inCard,box:[r.left,r.top,r.right,r.bottom].map(Math.round),scrollBox:!!sb,lines:Math.round(r.height/parseFloat(cs.lineHeight))});
 if(inCard&&(r.bottom>cr.bottom-6+0.5||r.top<cr.top-0.5||r.left<cr.left-0.5||r.right>cr.right+0.5))out.outside.push({t:t.slice(0,30),box:[r.left,r.top,r.right,r.bottom].map(Math.round)});
 if(r.right>innerWidth+0.5||r.left<-0.5||r.bottom>innerHeight+0.5)out.outside.push({t:t.slice(0,30),viewport:true,box:[r.left,r.top,r.right,r.bottom].map(Math.round)});
 if(inCard&&!e.closest('[data-tap]'))for(const b of btns)if(!(b.left>=r.right||b.right<=r.left||b.top>=r.bottom||b.bottom<=r.top))out.btn.push({t:t.slice(0,30)});}
const face=card&&card.querySelector('.face');if(face){out.faceScroll=[face.scrollHeight,face.clientHeight]}
const inner=card&&card.querySelector('.face>div');if(inner){const r=inner.getBoundingClientRect();out.contentBottom=Math.round(r.bottom);}
const vb=document.querySelector('[data-verse-scroll]');if(vb){const r=vb.getBoundingClientRect();const th=vb.querySelector('.t17');const tr=th.getBoundingClientRect();const lh=parseFloat(getComputedStyle(th).lineHeight);out.vbox={scrollH:vb.scrollHeight,clientH:vb.clientHeight,thaiLinesVisible:+(Math.max(0,Math.min(r.bottom,tr.bottom)-tr.top)/lh).toFixed(2),thaiLinesTotal:Math.round(tr.height/lh)}}return JSON.stringify(out)})()"""
os.makedirs(HERE + f'/png/{WHICH}', exist_ok=True); res = {'chrome': ver}
for f in sorted(glob.glob(HERE + f'/html/{WHICH}/*.html')):
    tag = os.path.basename(f)[:-5]; w, h = map(int, re.search(r'(\d+)x(\d+)$', tag).groups())
    v = C.shot(ws, f, HERE + f'/png/{WHICH}/{tag}.png', w, h, js=JS); res[tag] = json.loads(v)
    r = res[tag]; print(tag, 'viewport', r['iw'], 'x', r['ih'], 'dpr', r['dpr'], '| thai', [(x['fs'], x['lhRatio'], x['lines']) for x in r['thai'] if x['inCard']], '| outside', len(r['outside']), '| on-buttons', len(r['btn']), '| card', r['card'] and [round(x) for x in r['card']], 'content-bottom', r.get('contentBottom'), 'vbox', r.get('vbox'), flush=True)
json.dump(res, open(HERE + f'/runs/shots-{WHICH}.json', 'w'), indent=1, ensure_ascii=False); print(ver)
ws.call('Browser.close')
