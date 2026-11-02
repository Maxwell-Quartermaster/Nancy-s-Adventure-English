# DOM check (watchman domcheck_r2 JS) and occlusion sweep (r2c occl_qm JS), run through the one CDP Chrome (no per-run profiles, nothing deleted).
import re, sys, os, json, time, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import cdp_shot as C
DC = re.search(r'JS=r"""(.*?)"""', open('/workspace/watchman/rewalk-1700/domcheck_r2.py').read(), re.S).group(1)
OC = re.search(r'JS=r"""(.*?)"""', open('/workspace/v608build/round2/r2c/occl_qm.py').read(), re.S).group(1)
T = '/tmp/qmtmp/r2h/cdpchk/'; os.makedirs(T, exist_ok=True)
ws = C.session(); out = {}
for f in sys.argv[1:]:
    w, h = map(int, re.search(r'(\d+)x(\d+)', os.path.basename(f)).groups()); s = open(f).read(); r = {}
    for k, js, pre in (('dom', DC.replace('__W__', str(w)).replace('__H__', str(h)), 'dc'), ('occl', OC.replace('%W%', str(w)).replace('%H%', str(h)), 'OCC')):
        d = s.replace('</body>', js + '</body>') if '</body>' in s else s + js
        p = T + k + '--' + os.path.basename(f); open(p, 'w').write(d)
        v = None
        for t in range(3):
            v = C.shot(ws, p, None, w, h, wait=1.2 + t, js=f"(document.getElementById('{pre}')||{{}}).textContent||''")
            if v: break
        r[k] = json.loads(v) if v else 'NO-OUTPUT'
    out[f] = r
    dom = r['dom']; iss = dom.get('issues') if isinstance(dom, dict) else dom
    print(os.path.basename(f), 'dom', json.dumps(iss, ensure_ascii=False)[:300], '| occl', (json.dumps(r['occl'], ensure_ascii=False)[:300] if r['occl'] else '[]'), flush=True)
json.dump(out, open('/tmp/qmtmp/r2h/cdp_checks.json', 'w'), ensure_ascii=False)
