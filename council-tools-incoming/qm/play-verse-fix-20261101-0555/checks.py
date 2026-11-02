# QM play-verse-fix: the r2h render checks on old and new html, as round2/r2h/cdp_checks.py does them (one CDP Chrome):
#   DOM check = Watchman domcheck_r2.py JS (6cd930d1), occlusion sweep = snap code/occl_qm.py JS (aa963b83), plus snap code/banner_check.py JS (901b5c4a)
#   and its pass rules on the guardian page 26. Injected copies go to scratch/chk/<which>/; profile + TMPDIR in scratch/. Usage: python3 checks.py old|new
import sys, os, re, json, glob, subprocess, time, urllib.request
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); WHICH = sys.argv[1]; SCR = HERE + '/scratch/'
os.chdir(SCR); os.environ['TMPDIR'] = 'tmp'
sys.path.insert(0, '/workspace/v608build/snap-r2h-0021MDT/code/r2h'); import cdp_shot as C
C.PORT = 9362
DC = re.search(r'JS=r"""(.*?)"""', open('/workspace/watchman/rewalk-1700/domcheck_r2.py').read(), re.S).group(1)
OC = re.search(r'JS=r"""(.*?)"""', open('/workspace/v608build/snap-r2h-0021MDT/code/occl_qm.py').read(), re.S).group(1)
BC = re.search(r'JS = """(.*?)"""', open('/workspace/v608build/snap-r2h-0021MDT/code/banner_check.py').read(), re.S).group(1)
prof = SCR + f'chk-prof-{WHICH}'; T = SCR + f'chk/{WHICH}/'; os.makedirs(prof, exist_ok=True); os.makedirs(T, exist_ok=True)
p = subprocess.Popen(['google-chrome', '--headless=new', '--no-sandbox', '--disable-gpu', '--hide-scrollbars', '--no-first-run', f'--remote-debugging-port={C.PORT}',
                      f'--user-data-dir={prof}', 'about:blank'], env=dict(os.environ, TMPDIR='tmp'), cwd=SCR, stdout=subprocess.DEVNULL, stderr=open(SCR + f'chk-stderr-{WHICH}.txt', 'w'))
for _ in range(100):
    try: urllib.request.urlopen(f'http://127.0.0.1:{C.PORT}/json/version', timeout=1); break
    except Exception: time.sleep(.2)
else: raise SystemExit('chrome did not start')
ws = C.session(); out = {}; tot = {'dom': 0, 'occl': 0, 'banner': 0}
for f in sorted(glob.glob(HERE + f'/html/{WHICH}/*.html')):
    b = os.path.basename(f); w, h = map(int, re.search(r'(\d+)x(\d+)\.html$', b).groups()); s = open(f).read(); r = {}
    jobs = [('dom', DC.replace('__W__', str(w)).replace('__H__', str(h)), 'dc'), ('occl', OC.replace('%W%', str(w)).replace('%H%', str(h)), 'OCC')]
    if b.startswith('26-'): jobs.append(('banner', BC, 'bbout'))
    for k, js, pre in jobs:
        q = T + k + '--' + b; open(q, 'w').write(s.replace('</body>', js + '</body>') if '</body>' in s else s + js); v = None
        for t in range(3):
            v = C.shot(ws, q, None, w, h, wait=1.2 + t, js=f"(document.getElementById('{pre}')||{{}}).textContent||''")
            if v: break
        r[k] = json.loads(v) if v else 'NO-OUTPUT'
    dom = r['dom']['issues'] if isinstance(r['dom'], dict) else ['NO-OUTPUT']; occ = r['occl'] if isinstance(r['occl'], list) else ['NO-OUTPUT']
    line = f"{b[:-5]} | dom issues {len(dom)} {json.dumps(dom, ensure_ascii=False)[:400]} | occl hits {len(occ)} {json.dumps(occ, ensure_ascii=False)[:300]}"
    tot['dom'] += len(dom); tot['occl'] += len(occ)
    if 'banner' in r:   # banner_check.py pass rules
        x = r['banner']; iss = []
        if x['bb'] is None: iss.append('no Guardian banner')
        elif x['st'] < x['bb'] - 0.5: iss.append(f"scene {x['who']} top {x['st']:.0f} above banner bottom {x['bb']:.0f}")
        for k_, l, rt, t in x['taps']:
            if k_ in ('back', 'hearth-flame'): continue
            if l < 16 - .5 or rt > w - 16 + .5: iss.append(f'{k_} edge {l:.0f}/{w - rt:.0f}')
            if x['bb'] is not None and t < x['bb']: iss.append(f'{k_} under the banner')
        tot['banner'] += len(iss); line += f" | banner issues {len(iss)} {iss}"
    out[b] = r; print(line, flush=True)
json.dump(out, open(HERE + f'/runs/checks-{WHICH}.json', 'w'), ensure_ascii=False, indent=1)
print(f"TOTAL {WHICH}: dom issues {tot['dom']}, occl hits {tot['occl']}, banner issues {tot['banner']} (banner on 26 only)")
ws.call('Browser.close')
