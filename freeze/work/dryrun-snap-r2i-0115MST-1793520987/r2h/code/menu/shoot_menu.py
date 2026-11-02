import sys, os; sys.path.insert(0, '/workspace/v608build/round2/r2h'); import cdp_shot as C, sidecar as S
H='/workspace/v608build/r2h-rerun-stage/r2h/html/'; O='/workspace/v608build/r2h-rerun-stage/r2h/png/'
ws = C.session()
for n in sys.argv[1:]:
    w, h = map(int, n.rsplit('-', 1)[1].split('x')); S.shot(ws, H + n + '.html', O + n + '.png', w, h); print('ok', n, flush=True)
