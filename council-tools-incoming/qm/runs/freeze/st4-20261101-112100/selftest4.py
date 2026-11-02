#!/usr/bin/env python3
"""selftest4.py (st4: control moved to its own case C, using a snapshot file) - run-folder copy of freeze-v3 selftest.py 7702a748 (Quartermaster), adapted for st3:
 - REAL sheets scan: Chancellor's sheets_scan v1.1 (33ad034a) copied to <tools>/sheets-scan/sheets_scan.py (no stub);
   ground_check = byte copy of candidate 944d543a at <tools>/ground-check/ground_check_real.py behind a logging wrapper
   at <tools>/ground-check/ground_check.py (log line = calling program + path), so v1.1's same-tree default uses 944d543a.
 - lean sandboxes: each sandbox is pre-seeded with HARDLINKS of the read-only (444) live snapshot files; files a case
   writes to are real copies (PASTE always; QUEUE.md for carry-corrupt). freeze.py's own step-4 copies are unavoidable.
 - disk cap: df before every case; a case runs only if used + estimate + margin < 79.0% of /; a watchdog kills the
   running freeze and stops the run if / reaches 79.0% - 8 MB. Once a case does not fit, all later cases are SKIPPED.
 - zero-copy cases first, then the copy cases in priority order (sheets-side first).
 - FZ/HC are the candidate files themselves (read-only use); every sandbox lives under this run folder; no deletes.
 - control check fixed as in st-20261101-091657 (send_guard --only sheets/).
 - 5b uses Auditor pack sheets c03+c04 (dimmed bad panel, sourced) -> must BLOCK; 5c adds pack sheet c07 (sourced, good
   panels) -> must PASS."""
import fcntl, hashlib, json, os, re, shutil, signal, subprocess, sys, threading, time
RUN = os.path.dirname(os.path.abspath(__file__))
CAND = '/workspace/v608build/council-tools-incoming/qm/freeze-v3'
HERE = CAND; FZ = os.path.join(CAND, 'freeze.py'); HC = os.path.join(CAND, 'hold_check.py')
LIVE = '/workspace/v608build/CURRENT-SNAP.txt'; LIVE_MD5 = 'f6dac2d0e7b391436a160eab1bbf17fe'; LIVE_B = '/workspace/v608build'
R = '/workspace/v608build/round2'; PASTE = '/workspace/v608build/r2h-build/nancys-adventure-english-v6-08-1B-v32-PASTE.md'
VN = 'nancys-adventure-english-v6-08-daily-verses.json'
SCAN_SRC = '/workspace/council-tools/incoming/chancellor-sheets-scan-v1.1/sheets-scan/sheets_scan.py'; SCAN_MD5 = '33ad034a1cf2771187ca35fbe1240720'
GC_SRC = '/workspace/council-tools/incoming/auditor-ground-single-render-v1/ground_check.single-render-v1.py'; GC_MD5 = '944d543a1689f8f49e2def250d7436e2'
PACK = '/workspace/council-tools/incoming/auditor-sheets-scan-cases-v1/cases'
QUICK = '--quick' in sys.argv
ROOT = os.path.join(RUN, 'cases'); os.makedirs(ROOT)
md5 = lambda p: hashlib.md5(open(p, 'rb').read()).hexdigest()
assert md5(FZ) == '0f4fc8ddf7fb4f533ca2d055bafede7f' and md5(HC) == '962ed3ed26efaf06986e6918fd687bb3'
assert md5(SCAN_SRC) == SCAN_MD5 and md5(GC_SRC) == GC_MD5
results = []; case_log = []; CUR = {'name': None}

# ---------------- disk cap
def du():
    s = os.statvfs('/'); size = s.f_blocks * s.f_frsize; used = (s.f_blocks - s.f_bfree) * s.f_frsize; return used, size
U0, SIZE = du(); CAP = int(0.79 * SIZE); MARGIN = 40 * 10**6
PEAK = [U0]; ABORT = {'why': None}; PROCS = set()
DLOG = open(os.path.join(RUN, 'disk.log'), 'a')
def dlog(msg):
    u, s = du(); DLOG.write(f'{time.strftime("%H:%M:%S")} used={u} pct={100*u/s:.3f} {msg}\n'); DLOG.flush(); return u
def watchdog():
    while True:
        u, _ = du(); PEAK[0] = max(PEAK[0], u)
        if u >= CAP - 8 * 10**6 and not ABORT['why']:
            ABORT['why'] = f'watchdog: / reached {100*u/SIZE:.3f}% during {CUR["name"]}'; dlog(ABORT['why'])
            for p in list(PROCS):
                try: os.killpg(p.pid, signal.SIGKILL)
                except Exception: pass
        time.sleep(0.2)
threading.Thread(target=watchdog, daemon=True).start()
dlog(f'start cap={CAP}')

def ok(name, cond, info=''):
    live = md5(LIVE) == LIVE_MD5
    results.append((CUR['name'], name, bool(cond) and live)); print(f'{"PASS" if cond and live else "FAIL"} {name}' + ('' if live else ' [LIVE POINTER CHANGED!]') + (f'  ({info})' if info and not cond else ''), flush=True)

def run_p(cmd, env=None, timeout=600, cwd=None):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=env, cwd=cwd, start_new_session=True); PROCS.add(p)
    try: o, e = p.communicate(timeout=timeout)
    finally: PROCS.discard(p)
    return subprocess.CompletedProcess(cmd, p.returncode, o, e)

# ---------------- lean seeding (hardlinks for the read-only snapshot)
_lp = dict(l.split('=', 1) for l in open(LIVE).read().splitlines() if '=' in l)
SNAPN = _lp['snap']; PASTE_REL = _lp['paste_1b_path'].split()[0]
def preseed(sb, copy=()):
    """What freeze.seed_sandbox does, but snapshot files are hardlinks (all 444, never written) except names in copy."""
    os.makedirs(sb); src = os.path.join(LIVE_B, SNAPN); dst = os.path.join(sb, SNAPN); dirs = []
    for d, ds, fs in os.walk(src):
        rd = os.path.relpath(d, src); td = os.path.normpath(os.path.join(dst, rd)); os.makedirs(td); dirs.append((d, td))
        for f in fs:
            s, t = os.path.join(d, f), os.path.join(td, f); rel = os.path.normpath(os.path.join(rd, f))
            if os.path.islink(s): os.symlink(os.readlink(s), t)
            elif rel in copy: shutil.copy2(s, t)
            else:
                assert not (os.stat(s).st_mode & 0o222), f'live snapshot file is writable, refusing to hardlink: {s}'
                os.link(s, t)
        for x in ds:
            if os.path.islink(os.path.join(d, x)): os.symlink(os.readlink(os.path.join(d, x)), os.path.join(td, x)); ds.remove(x)
    for d, td in reversed(dirs): shutil.copystat(d, td)
    p = os.path.join(sb, PASTE_REL); os.makedirs(os.path.dirname(p)); shutil.copy2(os.path.join(LIVE_B, PASTE_REL), p)
    shutil.copy2(LIVE, os.path.join(sb, 'CURRENT-SNAP.txt'))
    return sb

def stage(name, extra=None):
    T = os.path.join(ROOT, name, 'stage')
    for d in ('sheets', 'showcase', 'renders/r2x'): os.makedirs(os.path.join(T, d), exist_ok=True)
    shutil.copy2(f'{R}/r2h/png/05-map-day1-390x844.png', f'{T}/sheets/'); shutil.copy2(f'{R}/showcase/showcase-1-opening.png', f'{T}/showcase/')
    shutil.copy2(f'{R}/r2h/html/05-map-day1-390x844.html', f'{T}/renders/r2x/'); shutil.copy2(f'{R}/r2h/png/09-map-later-390x844.png', f'{T}/renders/r2x/')
    if extra: extra(T)
    return T
def pack_sheet(T, case, dst):
    """Auditor pack sheet + its sidecar (panel lines are absolute paths into the read-only pack)."""
    s = os.path.join(PACK, case, 'sheet.png'); shutil.copy2(s, os.path.join(T, dst)); shutil.copy2(s + '.sources.txt', os.path.join(T, dst) + '.sources.txt')

GC_WRAP = """# selftest wrapper: log <calling program> TAB <path>, then the real ground_check (ground_check_real.py = 944d543a byte copy)
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ground_check_real as _r
from ground_check_real import *
def check(f, *a, **k):
    lg = os.environ.get('GC_LOG')
    if lg: open(lg, 'a').write(os.path.basename(sys.argv[0] or '-') + '\\t' + os.path.abspath(f) + '\\n')
    return _r.check(f, *a, **k)
"""
def tools_copy(dst, wrap_gc=True):
    T = os.path.join(dst, 'council-tools'); os.makedirs(T)
    ig = shutil.ignore_patterns('__pycache__', 'runs', 'selftest-scratch', '*.bak', 'design')
    shutil.copy2('/workspace/council-tools/current_snap.py', T)
    for d in ('send-guard', 'thai-diff', 'fit-table'): shutil.copytree(f'/workspace/council-tools/{d}', f'{T}/{d}', ignore=ig)
    os.makedirs(f'{T}/ground-check')
    if wrap_gc: shutil.copy2(GC_SRC, f'{T}/ground-check/ground_check_real.py'); open(f'{T}/ground-check/ground_check.py', 'w').write(GC_WRAP)
    else: shutil.copy2(GC_SRC, f'{T}/ground-check/ground_check.py')
    os.makedirs(f'{T}/sheets-scan'); shutil.copy2(SCAN_SRC, f'{T}/sheets-scan/sheets_scan.py')
    return T
TOOLS_COPY = tools_copy(os.path.join(ROOT, 'tools'))
def logs(sb): n = os.path.basename(os.path.dirname(sb)); return os.path.join(ROOT, f'gc-{n}.log'), os.path.join(ROOT, f'scan-{n}.log')
def gclog(p): return [l.split('\t', 1) for l in open(p).read().splitlines()] if os.path.isfile(p) else []
def readlog(p): return [x[1] for x in gclog(p)]
def scan_out(sb, snap='snap-st-0100MDT'):
    p = os.path.join(sb, 'freeze', 'work', f'sheets-scan-{snap}.txt'); return open(p).read() if os.path.isfile(p) else ''

def fz(sb, *args, fault=None, stage_dir=None, paste=PASTE, snap='snap-st-0100MDT', quick=True, timeout=900, env_extra=None, tools=None):
    if ABORT['why']: return 99, 'ABORTED ' + ABORT['why']
    cmd = [sys.executable, FZ, '--sandbox', sb] + list(args)
    if stage_dir: cmd += ['--stage', stage_dir, '--paste', paste, '--snap-name', snap] + (['--skip-checks-v608'] if quick else [])
    env = dict(os.environ); env.pop('FREEZE_FAULT', None)
    if fault: env['FREEZE_FAULT'] = fault
    if tools == 'live': env.pop('FREEZE_TOOLS', None)
    else: env['FREEZE_TOOLS'] = tools or TOOLS_COPY
    env['GC_LOG'], env['SHEETS_SCAN_LOG'] = logs(sb)
    if env_extra: env.update(env_extra)
    r = run_p(cmd, env=env, timeout=timeout)
    return r.returncode, r.stdout + r.stderr

def sbx(name, copy=()): return preseed(os.path.join(ROOT, name, 'sb'), copy)
def ptr(sb): return md5(os.path.join(sb, 'CURRENT-SNAP.txt'))
def hold(sb): return os.path.exists(os.path.join(sb, 'freeze', 'HOLD'))
def reason(sb):
    p = os.path.join(sb, 'freeze', 'HOLD.reason'); return open(p).read() if os.path.isfile(p) else ''
def failed_kept(name, rc, out, sb, step, p0):
    ok(f'{name}: exit 1, REASON names step {step}', rc == 1 and re.search(rf'^REASON: step {step} ', out, re.M), out[-400:])
    ok(f'{name}: HOLD kept + HOLD.reason written', hold(sb) and reason(sb).startswith(f'REASON: step {step}'), reason(sb)[:200])
    ok(f'{name}: sandbox pointer unchanged', ptr(sb) == p0)
def planted(name, step, fault=None, extra=None, paste=PASTE, prep=None, snap='snap-st-0100MDT', copy=()):
    sb = sbx(name, copy); T = stage(name, extra)
    rc0, _ = fz(sb, '--status')
    if prep: prep(sb)
    p0 = ptr(sb); rc, out = fz(sb, stage_dir=T, fault=fault, paste=paste, snap=snap)
    failed_kept(name, rc, out, sb, step, p0); return sb, rc, out

# ================= cases (name, estimate bytes, n checks, fn)
CASES = []
def case(name, est, nchk):
    def d(fn): CASES.append((name, est, nchk, fn)); return fn
    return d
SNAPB = 75 * 10**6; SMALL = 3 * 10**6

@case('3 verse-byte', SMALL, 3)
def _():
    def verses(T):
        b = bytearray(open(f'/workspace/{VN}', 'rb').read()); i = b.index(b'"en"') + 10; b[i] = b[i] ^ 0x20; open(f'{T}/{VN}', 'wb').write(bytes(b))
    planted('verse-byte', 2, extra=verses)
@case('4 over-ceiling', SMALL, 4)
def _():
    op = os.path.join(ROOT, 'over-PASTE.md'); open(op, 'w', encoding='utf-8').write(open(PASTE, encoding='utf-8').read() + 'x' * 100)
    sb, rc, out = planted('over-ceiling', 1, paste=op); ok('over-ceiling: reason says over the ceiling', 'over the 188,200 ceiling' in out)
@case('5b sheets-scan-block (real scan, dim c03+c04)', SMALL, 4 + 4)
def _():
    def ex(T): pack_sheet(T, 'c03-sheet5-tileD-dim65-path', 'sheets/c03-sheet.png'); pack_sheet(T, 'c04-sheet5-tileD-dim65-float', 'sheets/c04-sheet.png')
    sb = sbx('sheets-scan-block'); T = stage('sheets-scan-block', ex); fz(sb, '--status'); p0 = ptr(sb)
    rc, out = fz(sb, stage_dir=T); gl, sl = logs(sb); so = scan_out(sb); g = gclog(gl)
    failed_kept('sheets-scan BLOCK', rc, out, sb, 3, p0)
    ok('sheets-scan BLOCK: REASON names the sheets scan (exit 1), ground_check never called directly (only via sheets_scan.py)', 'sheets scan exit 1' in out and g and all(c == 'sheets_scan.py' for c, _ in g), out[-300:] + repr(g[:3]))
    ok('[st3] real scan: c03 (dim x0.65 + path) BLOCKs on its bad panel 26D-path-dim65 [dimmed]', re.search(r'^BLOCK \S*/sheets/c03-sheet\.png \[5 panels\]: 26D-path-dim65\.png: .*\[dimmed', so, re.M), so[-600:])
    ok('[st3] real scan: c04 (dim x0.65 + floating tree) BLOCKs on its bad panel 26D-float-dim65', re.search(r'^BLOCK \S*/sheets/c04-sheet\.png \[5 panels\]: 26D-float-dim65\.png: ', so, re.M), so[-600:])
    ok('[st3] real scan: good unsourced stage images PASS whole; BASE = candidate pointer, ground_check = tools-copy wrapper', re.search(r'^PASS  \S*/sheets/05-map-day1-390x844\.png \[whole\]', so, re.M) and re.search(r'^PASS  \S*/showcase/showcase-1-opening\.png \[whole\]', so, re.M) and 'RESULT PASS=2 BLOCK=2 ERROR=0' in so and so.startswith('BASE pointer ') and '/freeze/work/precheck-' in so.splitlines()[0], so[:300])
    ok('[st3] sourced sheets themselves never reach ground_check; their 10 panels do (via sheets_scan.py)', not any(p.endswith(('/c03-sheet.png', '/c04-sheet.png')) for _, p in g) and sum('/cases/c03-' in p or '/cases/c04-' in p for _, p in g) == 10, repr(g))
@case('5d no-scan (live tools, fail closed)', SMALL, 1)
def _():
    sb = sbx('no-scan'); T = stage('no-scan'); fz(sb, '--status', tools='live')
    rc, out = fz(sb, '--dry-run', stage_dir=T, tools='live')
    ok('no sheets scan installed (live tools): exit 1, REASON step 3 names the missing scan', rc == 1 and re.search(r'^REASON: step 3 render: \S*sheets-scan/sheets_scan.py: sheets scan not installed', out, re.M), out[-400:])
@case('5c route() units', 0, 1)
def _():
    r = run_p([sys.executable, '-c', 'import sys,json;sys.path.insert(0,%r);import freeze as f;print(json.dumps([f.route(x) for x in sys.argv[1:]]))' % HERE,
               './showcase/showcase-1-opening.png', './sheets/05-map-day1-390x844.png', './scene-fill-20261101/sheets/S01.png', './sheets/sub/x.png',
               './renders/r2x/09-map-later-390x844.png', './sheets-ref/x.png', './renders/sheets.png', './showcase'], env=dict(os.environ, FREEZE_TOOLS=TOOLS_COPY))
    want = ['sheets', 'sheets', 'sheets', 'sheets', 'single', 'single', 'single', 'single']
    ok('route(): showcase/, sheets/, nested scene-fill/sheets/ and sheets/sub/ -> sheets; normal render, sheets-ref/, a file named sheets.png -> single', r.stdout.strip() == json.dumps(want), r.stdout + r.stderr[-300:])
@case('6 snap-exists', SMALL, 4)
def _():
    sb, rc, out = planted('snap-exists', 1, prep=lambda sb: os.makedirs(os.path.join(sb, 'snap-st-0100MDT'))); ok('existing snap dir: refuses to overwrite', 'already exists' in out)
@case('7 pointer-mismatch', SMALL, 4)
def _():
    sb, rc, out = planted('pointer-mismatch', 1, prep=lambda sb: open(os.path.join(sb, PASTE_REL), 'a').write(' ')); ok('pointer md5 mismatch named', 'pointer paste_1b_md5' in out)
@case('8 fit-stale', SMALL, 4)
def _():
    sb, rc, out = planted('fit-stale', 3, extra=lambda T: open(f'{T}/fit-sheet-test.md', 'w').write('Fit sheet. PASTE for this sheet: 155f86bb\n')); ok('mid-way check fail: fit_sheet_check STALE stops the freeze', 'fit_sheet_check exit 1' in out)
@case('11 unwritable', SMALL, 4)
def _():
    def ro(sb): os.chmod(sb, 0o555)
    sb, rc, out = planted('unwritable', 4, prep=ro); os.chmod(sb, 0o755); ok('unwritable dir: clean fail at step 4, no snap', not os.path.exists(os.path.join(sb, 'snap-st-0100MDT')) and 'write failed' in out, out[-300:])
@case('17b hold-moved', SMALL, 3)
def _():
    sb = sbx('hold-moved'); T = stage('hold-moved'); fz(sb, '--hold', 'fault 8 test'); open(os.path.join(sb, 'CURRENT-SNAP.txt'), 'a').write('working=moved under HOLD (selftest)\n'); p1 = ptr(sb)
    rc, out = fz(sb, '--status'); ok('fault 8: --status exit 1 says POINTER MOVED since the HOLD', rc == 1 and 'POINTER MOVED since the HOLD' in out, out[-300:])
    r = run_p([sys.executable, HC], env=dict(os.environ, CURRENT_SNAP=os.path.join(sb, 'CURRENT-SNAP.txt')))
    ok('fault 8: hold_check exit 1 says POINTER MOVED since the HOLD', r.returncode == 1 and 'POINTER MOVED since the HOLD' in r.stdout, r.stdout)
    rc, out = fz(sb, '--force-clear', stage_dir=T); ok('fault 8: --force-clear refuses (exit 2), pointer and HOLD left as they are', rc == 2 and 'MOVED since the HOLD' in out and ptr(sb) == p1 and hold(sb), out[-300:])
@case('19-20 manual + hold_check', SMALL, 8)
def _():
    sb = sbx('manual'); fz(sb, '--status')
    ok('--status with no HOLD: exit 0', fz(sb, '--status')[0] == 0)
    rc, out = fz(sb, '--hold', 'Maxwell asked to stop'); ok('--hold: exit 0, HOLD written, broadcast printed', rc == 0 and hold(sb) and 'QM HOLD: Maxwell asked to stop. Stop work now.' in out)
    ok('--hold again: exit 2', fz(sb, '--hold', 'again')[0] == 2)
    rc, out = fz(sb, '--status'); ok('--status with HOLD: exit 1, shows reason', rc == 1 and 'Maxwell asked to stop' in out)
    rc, out = fz(sb, '--release'); ok('--release: exit 0, HOLD archived, RESUME with Based-on sync', rc == 0 and not hold(sb) and 'QM RESUME' in out and 'Based on:' in out)
    e = dict(os.environ, CURRENT_SNAP=os.path.join(sb, 'CURRENT-SNAP.txt'))
    ok('hold_check: exit 0 with no HOLD', run_p([sys.executable, HC], env=e).returncode == 0)
    fz(sb, '--hold', 'hold_check test'); r = run_p([sys.executable, HC], env=e)
    ok('hold_check: exit 1 + reason with HOLD', r.returncode == 1 and 'hold_check test' in r.stdout)
    fz(sb, '--release')
    ok('hold_check --hold-file on a missing file: exit 0', run_p([sys.executable, HC, '--hold-file', os.path.join(ROOT, 'nope')]).returncode == 0)
@case('21 guards (live refused)', 0, 3)
def _():
    T = stage('guards'); env = dict(os.environ); env.pop('FREEZE_FAULT', None); env.pop('FREEZE_TOOLS', None)
    r = run_p([sys.executable, FZ, '--stage', T, '--paste', PASTE, '--snap-name', 'snap-st-live'], env=dict(env, FREEZE_FAULT='step6_bad_pointer'))
    ok('FREEZE_FAULT without --sandbox: exit 2, nothing done', r.returncode == 2 and not os.path.exists('/workspace/v608build/freeze/HOLD'))
    r = run_p([sys.executable, FZ, '--stage', T, '--paste', PASTE, '--snap-name', 'snap-st-live', '--skip-checks-v608'], env=env)
    ok('--skip-checks-v608 without --sandbox: exit 2', r.returncode == 2)
    r = run_p([sys.executable, FZ, '--sandbox', '/workspace/v608build', '--status'], env=env)
    ok('--sandbox pointing at live v608build: exit 2', r.returncode == 2)
@case('21c no-carry', 4 * 10**6, 1)
def _():
    sb = sbx('no-carry'); T = stage('no-carry'); fz(sb, '--status')
    rc, out = fz(sb, '--no-carry', stage_dir=T); sd = os.path.join(sb, 'snap-st-0100MDT'); n_files = sum(len(f) for _, _, f in os.walk(sd))
    ok('--no-carry: exit 0, snap = 4 stage files + PASTE + 3 manifests/DELTA only', rc == 0 and n_files == 8 and not os.path.exists(os.path.join(sd, 'QUEUE.md')) and '--no-carry: stage + PASTE only' in open(os.path.join(sd, 'DELTA.md')).read(), f'rc={rc} files={n_files} ' + out[-200:])
@case('21d carry-corrupt', SMALL, 4)
def _():
    def corrupt(sb):
        f = os.path.join(sb, SNAPN, 'QUEUE.md'); assert os.stat(f).st_nlink == 1, 'QUEUE.md must be a real copy'
        os.chmod(os.path.dirname(f), 0o755); os.chmod(f, 0o644); open(f, 'a').write('tampered\n')
    sb, rc, out = planted('carry-corrupt', 3, prep=corrupt, copy=('QUEUE.md',))
    ok('corrupted carried file: named, no new snap, pointer untouched', 'carried file md5' in out and 'QUEUE.md' in out and not os.path.exists(os.path.join(sb, 'snap-st-0100MDT')), out[-300:])
@case('C control: ground_check logger (snapshot file)', SMALL, 1)
def _():
    # st4 fix: the st3 control sent a STAGE file that is not in the sandbox snapshot -> send_guard MISS, ground never ran.
    # Use a file that IS in the seeded snapshot, under its own --only prefix, so send_guard reaches ground_check.
    sb = sbx('control'); f = os.path.join(sb, SNAPN, 'renders/r2h/png/05-map-day1-390x844.png'); cl = os.path.join(ROOT, 'gc-control.log')
    r = run_p([sys.executable, os.path.join(TOOLS_COPY, 'send-guard/send_guard.py'), '--only', 'renders/', f], env=dict(os.environ, GC_LOG=cl, CURRENT_SNAP=os.path.join(sb, 'CURRENT-SNAP.txt')))
    ok('control: ground_check logger records a direct send_guard ground call', r.returncode == 0 and readlog(cl) == [f] and gclog(cl)[0][0] == 'send_guard.py', (r.stdout[-300:], gclog(cl)))
# ---- copy cases, priority order
@case('5c routing dry run (real scan, good sourced c07)', SNAPB, 8 + 1)
def _():
    def nested(T):
        for d in ('scene-fill-20261101/sheets', 'sheets/sub'): os.makedirs(os.path.join(T, d))
        shutil.copy2(f'{R}/r2h/png/09-map-later-390x844.png', f'{T}/scene-fill-20261101/sheets/S01-nested.png'); shutil.copy2(f'{R}/r2h/png/09-map-later-390x844.png', f'{T}/sheets/sub/sub-nested.png')
        pack_sheet(T, 'c07-S02-park-8fe1165e', 'showcase/c07-sheet.png')
    sb = sbx('routing'); T = stage('routing', nested); fz(sb, '--status'); p0 = ptr(sb)
    rc, out = fz(sb, '--dry-run', stage_dir=T); gl, sl = logs(sb); so = scan_out(sb); g = gclog(gl)
    sc = re.findall(r'^(?:PASS |BLOCK|ERROR) (\S+) \[', so, re.M)
    sgp = os.path.join(sb, 'freeze', 'work', 'send-guard-snap-st-0100MDT.txt'); sg = open(sgp).read() if os.path.isfile(sgp) else ''
    ok('routing dry run: exit 0, DRY RUN CLEAN, pointer untouched', rc == 0 and 'DRY RUN CLEAN' in out and ptr(sb) == p0, out[-400:])
    ok('routing: showcase/ file -> sheets scan only', os.path.join(T, 'showcase/showcase-1-opening.png') in sc, sc)
    ok('routing: sheets/ file -> sheets scan only', os.path.join(T, 'sheets/05-map-day1-390x844.png') in sc, sc)
    ok('routing: nested scene-fill-20261101/sheets/ and sheets/sub/ files -> sheets scan only', os.path.join(T, 'scene-fill-20261101/sheets/S01-nested.png') in sc and os.path.join(T, 'sheets/sub/sub-nested.png') in sc, sc)
    ok('routing: sheets scan got exactly the 5 sheets/showcase images (4 + sourced c07), not the normal render [st3: was 4]', len(sc) == 5 and not any('/renders/' in x for x in sc), sc)
    ok('routing: ground_check never called directly (every call came from sheets_scan.py; none on a renders/ file) [st3: real scan]', all(c == 'sheets_scan.py' for c, _ in g) and not any('/renders/' in p for _, p in g), repr(g))
    ok('routing: send_guard ran --no-ground with nested --only prefixes, every sheets/showcase file OK in the candidate snapshot [st3: 6 files]', 'GROUND SKIPPED' in sg and 'GRND' not in sg and 'RESULT CLEAR: 6 files' in sg and 'OK ' in sg and 'S01-nested.png = MANIFEST.md5:./scene-fill-20261101/sheets/S01-nested.png' in sg, sg[-500:])
    ok('routing: normal render (renders/r2x/) not given to send_guard or the sheets scan (unchanged from 91aa8a3e)', '/renders/' not in sg and not any('/renders/' in x for x in sc), sg[-300:])
    ok('[st3] real scan: sourced c07 PASSes on its 4 good panels, the sheet itself is not ground-checked; RESULT PASS=5 exit 0', re.search(r'^PASS  \S*/showcase/c07-sheet\.png \[4 panels\]', so, re.M) and 'RESULT PASS=5 BLOCK=0 ERROR=0 SKIP=0 exit 0' in so and not any(p.endswith('/c07-sheet.png') for _, p in g) and sum('/cases/c07-' in p for _, p in g) == 4, so[-500:])
@case('1-2 clean dry + real run', 2 * SNAPB + 5 * 10**6, 20)
def _():
    sb = sbx('clean'); T = stage('clean')
    rc, out = fz(sb, stage_dir=T, quick=QUICK, timeout=900, *['--dry-run']); p0 = ptr(sb)
    ok('clean dry run: exit 0, DRY RUN CLEAN', rc == 0 and 'DRY RUN CLEAN' in out, out[-600:])
    ok('clean dry run: checks_v608 ran (0 new live False)' if not QUICK else 'clean dry run: checks_v608 skipped (--quick)', QUICK or '0 new live False' in out, out[-600:])
    ok('clean dry run: no HOLD, pointer untouched, no snapshot dir', not hold(sb) and p0 == LIVE_MD5 and not os.path.exists(os.path.join(sb, 'snap-st-0100MDT')))
    if ABORT['why'] or not fits(SNAPB + 3 * 10**6, 'clean real run'):
        CUR['partial'] = 'clean real run skipped (disk)'; return
    rc, out = fz(sb, '--note', 'selftest clean run', stage_dir=T, quick=QUICK, timeout=900)
    new = ptr(sb); snapd = os.path.join(sb, 'snap-st-0100MDT')
    ok('clean real run: exit 0', rc == 0, out[-600:])
    ok('clean real run: sandbox pointer moved and verifies', new != p0 and 'step 6 self-check OK' in out)
    ok('clean real run: HOLD cleared, no HOLD.reason', not hold(sb) and not reason(sb))
    ok('clean real run: backup .pre-<snap> = old pointer', md5(os.path.join(sb, 'CURRENT-SNAP.txt.pre-snap-st-0100MDT')) == p0)
    txt = open(os.path.join(sb, 'CURRENT-SNAP.txt')).read()
    ok('clean real run: pointer fields (snap, paste_1b_path in snap, chars, bank, updated MT)', all(x in txt for x in ('snap=snap-st-0100MDT\n', 'paste_1b_path=snap-st-0100MDT/trim-1B/nancys-adventure-english-v6-08-PASTE.md\n', 'paste_1b_chars=188116\n', 'bank=84\n', 'paste_1b_md5=317e91ce86f073c961f8169183d2bbd3\n')) and re.search(r'updated=2026-\d\d-\d\d \d\d:\d\d M[DS]T', txt))
    man = open(os.path.join(snapd, 'MANIFEST.md5')).read().splitlines()
    ok('clean real run: MANIFEST md5 = pointer, every listed md5 re-checks, renders-MANIFEST listed', md5(os.path.join(snapd, 'MANIFEST.md5')) in txt and all(md5(os.path.join(snapd, l.split('  ', 1)[1][2:])) == l.split()[0] for l in man) and any(l.endswith('./renders-MANIFEST.md5') for l in man))
    ok('clean real run: PASTE copy in trim-1B = source md5', md5(os.path.join(snapd, 'trim-1B/nancys-adventure-english-v6-08-PASTE.md')) == md5(PASTE))
    ok('clean real run (fault 9 pass case): copy2 kept every snapshot mtime = source mtime',
       all(os.stat(os.path.join(snapd, rel)).st_mtime_ns == os.stat(os.path.join(T, rel)).st_mtime_ns for rel in ('sheets/05-map-day1-390x844.png', 'showcase/showcase-1-opening.png', 'renders/r2x/05-map-day1-390x844.html'))
       and os.stat(os.path.join(snapd, 'trim-1B/nancys-adventure-english-v6-08-PASTE.md')).st_mtime_ns == os.stat(PASTE).st_mtime_ns)
    prevd = os.path.join(sb, SNAPN); pm = [l.split('  ', 1) for l in open(os.path.join(prevd, 'MANIFEST.md5')).read().splitlines()]
    stg = {'./' + os.path.relpath(os.path.join(d, f), T) for d, _, fs in os.walk(T) for f in fs}
    carried = [(h, r) for h, r in pm if r not in ('./DELTA.md', './renders-MANIFEST.md5', './trim-1B/nancys-adventure-english-v6-08-PASTE.md') and r not in stg]
    ok('carry default: every previous-snap file present in the new snap, md5-identical', len(carried) > 600 and all(os.path.isfile(os.path.join(snapd, r[2:])) and md5(os.path.join(snapd, r[2:])) == h for h, r in carried), f'{len(carried)} carried')
    ok('carry default: carried files keep the previous snap mtimes (copy2)', all(os.stat(os.path.join(snapd, r[2:])).st_mtime_ns == os.stat(os.path.join(prevd, r[2:])).st_mtime_ns for h, r in carried))
    dl = open(os.path.join(snapd, 'DELTA.md')).read()
    ok('carry default: DELTA lists carried/new/changed counts and per-file status', f'Carried: {len(carried)}.' in dl and 'Stage new: 3.' in dl and 'Stage same as carried: 1.' in dl and '- stage-same: ./showcase/showcase-1-opening.png ' in dl and 'Stage overrides (changed): 1.' in dl and '## Per-file status' in dl and '- carried: ./QUEUE.md ' in dl and '- stage-new: ./sheets/05-map-day1-390x844.png ' in dl and '- stage-overrides: ./trim-1B/nancys-adventure-english-v6-08-PASTE.md ' in dl, dl[:600])
    wm = open(os.path.join(sb, 'freeze', 'watchman-msg.txt')).read().strip(); rs = open(os.path.join(sb, 'freeze', 'resume-msg.txt')).read()
    ok('clean real run: HOLD, RESUME+SYNC and Watchman messages printed', 'QM HOLD: freeze snap-st-0100MDT in progress. Stop work now. No edits, no sends, no patches past this point until RESUME.' in out and 'QM RESUME+SYNC' in out and wm in out)
    ok('clean real run: Watchman ping is exactly FREEZE <md5> <snap>, and is the last line before the sandbox note', wm == f'FREEZE {new} snap-st-0100MDT' and out.strip().splitlines()[-2] == wm)
    ok('clean real run: RESUME names pointer/snap/paste/chars/bank, Based-on sync proof, ack as backstop after release',
       all(x in rs for x in (new, 'snap-st-0100MDT', '317e91ce86f073c961f8169183d2bbd3', '188,116', 'bank 84', f'Based on: snap-st-0100MDT, pointer {new[:8]}', 'Backstop only, now that HOLD is released', 'watcher.py --ack <you>', 'Work toward this pointer only')))
    ok('clean real run: last-freeze.json FROZEN', json.load(open(os.path.join(sb, 'freeze', 'last-freeze.json')))['result'] == 'FROZEN')
    so = scan_out(sb); g = gclog(logs(sb)[0])
    ok('[st3] clean real run: real sheets scan PASS on the 2 stage sheets/showcase images, ground_check only via sheets_scan.py', 'RESULT PASS=2 BLOCK=0 ERROR=0 SKIP=0 exit 0' in so and g and all(c == 'sheets_scan.py' for c, _ in g), so[-300:] + repr(g))
@case('5 sendguard-exit3 no-op dry run', SNAPB, 1)
def _():
    sb = sbx('sendguard-exit3'); T = stage('sendguard-exit3'); fz(sb, '--status')
    rc, out = fz(sb, '--dry-run', stage_dir=T, fault='sendguard_exit3'); ok('v3 sendguard_exit3 fault is a no-op (sheets leg always --no-ground): dry run exit 0', rc == 0 and 'DRY RUN CLEAN' in out, out[-300:])
@case('5d no-sheets (live tools) dry run', SNAPB, 1)
def _():
    def nosheets(T):
        for d in ('sheets', 'showcase'): os.rename(os.path.join(T, d), os.path.join(T, d + '-moved-by-selftest'))
    sb = sbx('no-sheets'); T = stage('no-sheets', nosheets); fz(sb, '--status', tools='live')
    rc, out = fz(sb, '--dry-run', stage_dir=T, tools='live')
    ok('stage with no sheets/showcase (live tools): dry run exit 0, scan not needed', rc == 0 and 'DRY RUN CLEAN' in out and 'no sheets/ or showcase/ files in stage' in out, out[-400:])
@case('14 step6 rollback', SNAPB, 3)
def _():
    sb = sbx('step6'); T = stage('step6'); fz(sb, '--status'); p0 = ptr(sb)
    rc, out = fz(sb, stage_dir=T, fault='step6_bad_pointer'); r = reason(sb)
    ok('step-6 failure: exit 1, REASON step 6', rc == 1 and 'REASON: step 6 current_snap' in out, out[-400:])
    ok('step-6 failure: pointer rolled back to the pre-freeze md5 automatically', ptr(sb) == p0 and 'POINTER MOVED to' in r and 'ROLLED BACK to ' + p0 in r)
    ok('step-6 failure: restored pointer names the old, complete snap (not the new one)', f'snap={SNAPN}' in open(os.path.join(sb, 'CURRENT-SNAP.txt')).read() and hold(sb))
@case('15 rollback-fails', SNAPB, 2)
def _():
    sb = sbx('rollback-fails'); T = stage('rollback-fails'); fz(sb, '--status'); p0 = ptr(sb)
    rc, out = fz(sb, stage_dir=T, fault='step6_bad_pointer,rollback_fails'); r = reason(sb)
    ok('rollback fails: HOLD kept, reason says POINTER MOVED ... NOT ROLLED BACK + restore command', rc == 1 and hold(sb) and 'POINTER MOVED to' in r and 'NOT ROLLED BACK' in r and 'cp ' in r, r[:300])
    ok('rollback fails: --release refuses while the pointer does not verify', fz(sb, '--release')[0] == 2)
@case('13 handmove', SNAPB, 2)
def _():
    sb = sbx('handmove'); T = stage('handmove'); fz(sb, '--status')
    rc, out = fz(sb, stage_dir=T, fault='pointer_handmove')
    ok('hand-moved pointer: exit 1 at step 5, refuses to write', rc == 1 and 'REASON: step 5 pointer' in out and 'moved by hand' in out, out[-300:])
    ok('hand-moved pointer: the hand edit is left as-is (not overwritten), HOLD kept', 'hand-edited during HOLD' in open(os.path.join(sb, 'CURRENT-SNAP.txt')).read() and f'snap={SNAPN}' in open(os.path.join(sb, 'CURRENT-SNAP.txt')).read() and hold(sb))
@case('9 paste-copy', SNAPB, 4)
def _():
    sb, rc, out = planted('paste-copy', 4, fault='paste_copy_corrupt'); ok('paste copy mismatch: no snapshot at the final name', not os.path.exists(os.path.join(sb, 'snap-st-0100MDT')) and 'PASTE copy md5' in out)
@case('10 enospc', SNAPB, 4)
def _():
    sb, rc, out = planted('enospc', 4, fault='manifest_enospc'); ok('ENOSPC: clean fail, no half-written snap at the final name, tmp named', not os.path.exists(os.path.join(sb, 'snap-st-0100MDT')) and 'No space left' in out and 'Half-built snapshot left' in out)
@case('12 plain-copy', SNAPB, 4)
def _():
    sb, rc, out = planted('plain-copy', 4, fault='plain_copy'); ok('fault 9: plain copy (mtimes lost) fails the freeze', 'mtime not preserved' in out)
@case('16 hold-present', SNAPB, 2)
def _():
    sb = sbx('hold-present'); T = stage('hold-present'); fz(sb, '--hold', 'planted hold'); p0 = ptr(sb)
    rc, out = fz(sb, stage_dir=T); ok('HOLD present: exit 2, pointer unchanged', rc == 2 and 'HOLD already present' in out and ptr(sb) == p0)
    rc, out = fz(sb, '--force-clear', stage_dir=T); ok('HOLD present + --force-clear: freeze runs, old HOLD archived', rc == 0 and any('cleared' in f for f in os.listdir(os.path.join(sb, 'freeze', 'holds'))), out[-300:])
@case('17 crash + stale HOLD', SNAPB, 4)
def _():
    sb = sbx('crash'); T = stage('crash'); fz(sb, '--status')
    rc, out = fz(sb, stage_dir=T, fault='crash_after_hold')
    ok('crash: process died, HOLD left, no reason', rc == 9 and hold(sb) and not reason(sb))
    h = json.load(open(os.path.join(sb, 'freeze', 'HOLD'))); h['started_epoch'] -= 7200; json.dump(h, open(os.path.join(sb, 'freeze', 'HOLD'), 'w'))
    rc, out = fz(sb, '--status'); ok('stale HOLD: --status exit 1 shows age and STALE', rc == 1 and 'STALE HOLD' in out and '(120 min)' in out, out)
    rc, out = fz(sb, stage_dir=T); ok('stale HOLD: freeze refuses without --force-clear (exit 2)', rc == 2)
    rc, out = fz(sb, '--force-clear', stage_dir=T); ok('stale HOLD: --force-clear freezes cleanly', rc == 0 and not hold(sb))
@case('18 lock', SNAPB, 3)
def _():
    sb = sbx('lock'); T = stage('lock'); fz(sb, '--status')
    lf = open(os.path.join(sb, 'freeze', 'freeze.lock'), 'a+'); fcntl.flock(lf, fcntl.LOCK_EX | fcntl.LOCK_NB)
    rc, out = fz(sb, stage_dir=T); ok('lock held: second freeze refused (exit 2), no HOLD written', rc == 2 and 'another freeze is running' in out and not hold(sb))
    ok('lock held: --release refused (exit 2)', fz(sb, '--release')[0] == 2)
    fcntl.flock(lf, fcntl.LOCK_UN); lf.close()
    env = dict(os.environ, FREEZE_TOOLS=TOOLS_COPY); env.pop('FREEZE_FAULT', None)
    A = subprocess.Popen([sys.executable, FZ, '--sandbox', sb, '--stage', T, '--paste', PASTE, '--snap-name', 'snap-st-A', '--skip-checks-v608'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=env, start_new_session=True); PROCS.add(A)
    time.sleep(0.4); rcB, outB = fz(sb, stage_dir=T, snap='snap-st-B'); outA = A.communicate()[0]; PROCS.discard(A)
    ok('two freezes at once: one runs (0), the other is refused (2)', A.returncode == 0 and rcB == 2 and 'another freeze is running' in outB, f'A={A.returncode} B={rcB} ' + outA[-300:])
@case('21b override', SNAPB, 1)
def _():
    def q(T): open(f'{T}/QUEUE.md', 'w').write('QUEUE overridden by the stage (selftest)\n')
    sb = sbx('override'); T = stage('override', q); fz(sb, '--status')
    rc, out = fz(sb, stage_dir=T); sd = os.path.join(sb, 'snap-st-0100MDT')
    ok('stage overrides a carried file: exit 0, snap QUEUE.md = stage bytes, DELTA says stage-overrides', rc == 0 and md5(os.path.join(sd, 'QUEUE.md')) == md5(os.path.join(T, 'QUEUE.md')) and '- stage-overrides: ./QUEUE.md ' in open(os.path.join(sd, 'DELTA.md')).read() and md5(os.path.join(sd, 'COSTS-and-LEDGER.md')) == md5(os.path.join(sb, SNAPN, 'COSTS-and-LEDGER.md')), out[-300:])
@case('22 patched hold-check diff', SNAPB + 3 * 10**6, 6)
def _():
    P = os.path.join(ROOT, 'patched'); os.makedirs(P); tools_copy(P, wrap_gc=False)
    pr = run_p(['patch', '-p1', '-i', '/workspace/council-tools/incoming/qm-hold-check.diff'], cwd=P)
    ok('hold-check diff applies cleanly to a copy', pr.returncode == 0, pr.stdout + pr.stderr)
    sb = sbx('patched'); T = stage('patched'); pe = {'FREEZE_TOOLS': os.path.join(P, 'council-tools')}
    rc, out = fz(sb, stage_dir=T, env_extra=pe); ok('with the diff applied: a clean freeze still runs through its own HOLD (exit 0)', rc == 0, out[-400:])
    fz(sb, '--hold', 'diff test', env_extra=pe)
    e2 = {k: v for k, v in os.environ.items() if k != 'NAE_FREEZE_RUNNING'}; e2['CURRENT_SNAP'] = os.path.join(sb, 'CURRENT-SNAP.txt')
    r = run_p([sys.executable, os.path.join(P, 'council-tools/send-guard/send_guard.py'), '--only', 'sheets/', os.path.join(T, 'sheets/05-map-day1-390x844.png')], env=e2)
    ok('with the diff applied: send_guard BLOCKs (exit 1) during a HOLD', r.returncode == 1 and 'HOLD in place' in r.stdout, r.stdout[-300:])
    r = run_p([sys.executable, '-c', f'import sys;sys.path.insert(0,{os.path.join(P, "council-tools")!r});import current_snap as c;c.read()'], env=e2)
    ok('with the diff applied: current_snap.read raises HoldError during a HOLD', r.returncode != 0 and 'HoldError' in r.stderr)
    fz(sb, '--release', env_extra=pe)
    r = run_p([sys.executable, os.path.join(P, 'council-tools/send-guard/send_guard.py'), '--only', 'sheets/', os.path.join(T, 'sheets/05-map-day1-390x844.png')], env=e2)
    ok('with the diff applied: after --release send_guard is CLEAR (exit 0)', r.returncode == 0, r.stdout[-300:])
    env = dict(os.environ); env.pop('FREEZE_FAULT', None)
    r = run_p([sys.executable, FZ, '--status'], env=dict(env, FREEZE_TOOLS=os.path.join(P, 'council-tools')))
    ok('FREEZE_TOOLS without --sandbox: exit 2', r.returncode == 2)

# ================= runner
def fits(est, name):
    u = dlog(f'gate {name} est={est}')
    return u + est + MARGIN < CAP
STOPPED = None; summary = []
only = [a for a in sys.argv[1:] if not a.startswith('--')]
for name, est, nchk, fn in CASES:
    if only and not any(name.startswith(o) for o in only): continue
    if STOPPED or ABORT['why'] or not fits(est, name):
        STOPPED = STOPPED or ABORT['why'] or f'{name}: used {du()[0]:,} + est {est:,} + margin {MARGIN:,} would reach {100*(du()[0]+est+MARGIN)/SIZE:.2f}% (cap 79.0%)'
        summary.append((name, 'SKIP', nchk, STOPPED)); print(f'SKIP {name} ({nchk} checks): {STOPPED}', flush=True); continue
    CUR['name'] = name; CUR.pop('partial', None); n0 = len(results); u0 = du()[0]
    print(f'--- {name}', flush=True)
    try: fn()
    except Exception as e: ok(f'{name}: harness exception', False, f'{type(e).__name__}: {e}')
    u1 = dlog(f'done {name} delta={du()[0]-u0}')
    summary.append((name, 'RAN', len(results) - n0, CUR.get('partial', '') + f' disk delta {(u1-u0)/1e6:+.1f} MB'))
CUR['name'] = 'final'
ok('live CURRENT-SNAP.txt md5 is still ' + LIVE_MD5, md5(LIVE) == LIVE_MD5)
ok('no live HOLD left', not os.path.exists('/workspace/v608build/freeze/HOLD'))
ok('[st3] live freeze/freeze.py still 91aa8a3e', md5('/workspace/v608build/freeze/freeze.py') == '91aa8a3e12bc477ecee27222d97ba621')
n = sum(1 for *_, p in results if p)
print('\nCASES:'); [print(f'  {s:4} {nm} [{k} checks] {why}') for nm, s, k, why in summary]
print(f'\nSELFTEST3 {n}/{len(results)} checks passed; skipped cases: {sum(1 for x in summary if x[1]=="SKIP")} ({sum(x[2] for x in summary if x[1]=="SKIP")} checks)  (root {ROOT}; live pointer {md5(LIVE)}; peak used {PEAK[0]:,} = {100*PEAK[0]/SIZE:.3f}%)')
dlog(f'end peak={PEAK[0]}')
sys.exit(0 if n == len(results) else 1)
