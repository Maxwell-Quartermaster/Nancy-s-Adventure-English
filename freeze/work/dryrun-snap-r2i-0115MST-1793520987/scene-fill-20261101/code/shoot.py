# One private headless Chrome (port 9349, /tmp/qmtmp/cdp) so the r2h job's Chrome (9339) is never touched.
import os, sys, json, time, hashlib
sys.dont_write_bytecode = True
B = '/workspace/v608build/scene-fill-20261101/'; sys.path.insert(0, B + 'code'); import cdp_shot as C
sys.path.insert(0, '/workspace/v608build/round2/r2h'); import sidecar as SR   # only its DOM JS string is used
J = json.load(open(B + 'code/' + (sys.argv[1] if len(sys.argv) > 1 else 'jobs.json')))
p = C.start(); ws = C.session(); n = 0
try:
    for j in J['jobs']:
        html = B + f"html/{j['tag']}.html"; png = B + f"renders/{j['tag']}.png"
        assert hashlib.md5(open(html, 'rb').read()).hexdigest() == j['html_md5'], j['tag']   # html_md5 = the exact HTML file rendered
        r = C.shot(ws, html, png, j['w'], j['h'], 1.2, SR.JS); d = json.loads(r)
        side = dict(vw=d['vw'], vh=d['vh'], png=os.path.basename(png), html=os.path.basename(html), html_md5=j['html_md5'], source_html=j['src'], source_html_md5=j['src_md5'],
                    paste_md5=J['paste_md5'], pointer_md5=J['pointer_md5'], png_md5=hashlib.md5(open(png, 'rb').read()).hexdigest(), html_md5_src='render', snap='snap-r2h-0021MDT (candidate, not frozen)', loc=j['loc'], tod=j['tod'], note=j['note'], fixes=j['fixes'], el=d['el'])
        json.dump(side, open(png[:-4] + '.json', 'w'), ensure_ascii=False, separators=(',', ':')); n += 1; print(j['tag'], flush=True)
finally:
    p.terminate()
print('shot', n)
