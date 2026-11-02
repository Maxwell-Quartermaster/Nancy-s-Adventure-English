# Re-shoots every Sam screen with eyes_v608 (Nancy's exact happy eyes): app screens (best source: screens-v607 > screens-v606 > screens-v604) -> screens-v608/,
# scene-variety mocks (mocks-scene-variety-t401u/html, read-only) -> v608build/eyes/scene-variety/. Each also re-shot unmodified (before/) with the same shot().
import sys, os, glob, json, concurrent.futures as cf
sys.path.insert(0, '/workspace/v608build/eyes'); sys.path.insert(0, '/workspace/v606build')
from eyes_v608 import apply
from render_title_v606 import shot
E = '/workspace/v608build/eyes/'
def best():
    out = {}
    for p in sorted(glob.glob('/workspace/screens-v604/html/*.html')): out[os.path.basename(p)[:-5]] = p
    for d in ('/workspace/screens-v606/html/', '/workspace/screens-v607/html/'):
        for p in sorted(glob.glob(d + '*.html')):
            b = os.path.basename(p)[:-5]
            if b.endswith('-390check'): b = b[:-9]
            out[b] = p
    for p in sorted(glob.glob('/workspace/mocks-scene-variety-t401u/html/*.html')): out['sv-' + os.path.basename(p)[:-5]] = p
    return out
def one(item):
    b, p = item; w, h = (320, 568) if b.endswith('-320x568') else (390, 844)
    html, n = apply(open(p, encoding='utf-8').read())
    if not n: return b, p, n, None, None
    od = (E + 'scene-variety/') if b.startswith('sv-') else '/workspace/screens-v608/'
    open(od + 'html/%s.html' % b, 'w', encoding='utf-8').write(html); shot(html, od + 'png/%s.png' % b, w, h)
    shot(open(p, encoding='utf-8').read(), E + 'before/%s.png' % b, w, h)
    return b, p, n, od + 'png/%s.png' % b, E + 'before/%s.png' % b
if __name__ == '__main__':
    src = best(); res = {}
    with cf.ProcessPoolExecutor(6) as ex:
        for b, p, n, png, bf in ex.map(one, sorted(src.items())): res[b] = dict(src=p, subs=n, png=png, before=bf)
    json.dump(res, open(E + 'eyes-manifest.json', 'w'), indent=1)
    print(sum(1 for v in res.values() if v['png']), 'changed of', len(res))
