# t527u (1:43 AM decision): map screens 05/07/08/09 in the stage get the menu flower -> tuft pass (menu/flowers.py, also in fix_r2h.mapflowers),
# then a render into the stage with the shared sidecar writer (html_md5 at render time, html_md5_src render, png_md5).
import sys, os; HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, '/workspace/v608build/round2/r2h'); sys.path.insert(0, HERE)   # stage fix_r2h first; cdp_shot/sidecar from round2
import fix_r2h as F, cdp_shot as C, sidecar as S
assert F.__file__.startswith(HERE), F.__file__
R = os.path.dirname(HERE) + '/'
for t in sys.argv[1:]:
    h = R + f'html/{t}.html'; doc = open(h, encoding='utf-8').read(); log = []; new = F.mapflowers(doc, log, t)
    if new != doc: open(h, 'w', encoding='utf-8').write(new)
    print('\n'.join(log) or f'{t}: no flowers')
ws = C.session()
for t in sys.argv[1:]:
    w, hh = map(int, t.rsplit('-', 1)[1].split('x')); S.shot(ws, R + f'html/{t}.html', R + f'png/{t}.png', w, hh); print('shot', t, flush=True)
