#!/usr/bin/env python3
"""selftest.py - planted-fault self-test for freeze.py and hold_check.py. Owner: Quartermaster.
  python3 selftest.py [--quick]     (--quick skips the two real checks_v608 runs, ~50 s)
Every case runs in its own sandbox under <this dir>/sandbox/st-<time>/ (kept; no-delete rule). The live pointer is checked after every case.
v3 (sheets routing): freeze runs get FREEZE_TOOLS = a small copy of the tools freeze uses (current_snap, send-guard, ground-check,
thai-diff, fit-table) plus a STUB sheets scan (logs what it is given; BLOCKs names in $SHEETS_SCAN_STUB_BLOCK) and a logging
wrapper around ground_check (every path it is asked to check goes to $GC_LOG). tools='live' runs against /workspace/council-tools."""
import fcntl, hashlib, json, os, re, shutil, subprocess, sys, time
HERE = os.path.dirname(os.path.abspath(__file__)); FZ = os.path.join(HERE, 'freeze.py'); HC = os.path.join(HERE, 'hold_check.py')
LIVE = '/workspace/v608build/CURRENT-SNAP.txt'; LIVE_MD5 = 'f6dac2d0e7b391436a160eab1bbf17fe'
R = '/workspace/v608build/round2'; PASTE = '/workspace/v608build/r2h-build/nancys-adventure-english-v6-08-1B-v32-PASTE.md'
VN = 'nancys-adventure-english-v6-08-daily-verses.json'
QUICK = '--quick' in sys.argv
ROOT = os.path.join(HERE, 'sandbox', 'st-' + __import__('datetime').datetime.now(__import__('zoneinfo').ZoneInfo('America/Denver')).strftime('%Y%m%d-%H%M%S')); os.makedirs(ROOT)
md5 = lambda p: hashlib.md5(open(p, 'rb').read()).hexdigest()
results = []

def ok(name, cond, info=''):
    live = md5(LIVE) == LIVE_MD5
    results.append((name, bool(cond) and live)); print(f'{"PASS" if cond and live else "FAIL"} {name}' + ('' if live else ' [LIVE POINTER CHANGED!]') + (f'  ({info})' if info and not cond else ''), flush=True)

def stage(name, extra=None):
    T = os.path.join(ROOT, name, 'stage')
    for d in ('sheets', 'showcase', 'renders/r2x'): os.makedirs(os.path.join(T, d), exist_ok=True)
    shutil.copy2(f'{R}/r2h/png/05-map-day1-390x844.png', f'{T}/sheets/'); shutil.copy2(f'{R}/showcase/showcase-1-opening.png', f'{T}/showcase/')
    shutil.copy2(f'{R}/r2h/html/05-map-day1-390x844.html', f'{T}/renders/r2x/'); shutil.copy2(f'{R}/r2h/png/09-map-later-390x844.png', f'{T}/renders/r2x/')
    if extra: extra(T)
    return T

STUB_SCAN = """#!/usr/bin/env python3
# SELFTEST STUB of Chancellor's sheets scan (NOT the real scan). Logs every file to $SHEETS_SCAN_LOG; BLOCKs basenames in $SHEETS_SCAN_STUB_BLOCK.
import os, sys
fs = sys.argv[1:]
if not fs: print('ERROR no files'); sys.exit(2)
lg = os.environ.get('SHEETS_SCAN_LOG'); blk = set(x for x in os.environ.get('SHEETS_SCAN_STUB_BLOCK', '').split(',') if x); bad = 0
for f in fs:
    if lg: open(lg, 'a').write(os.path.abspath(f) + '\\n')
    if os.path.basename(f) in blk: print(f'BLOCK {f}: planted (stub)'); bad += 1
    else: print(f'PASS {f} (stub)')
print(f'RESULT {"BLOCK" if bad else "PASS"}: {len(fs)} files'); sys.exit(1 if bad else 0)
"""
GC_WRAP = """# selftest wrapper: log every path, then the real ground_check (ground_check_real.py, byte-identical copy)
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ground_check_real as _r
from ground_check_real import *
def check(f, *a, **k):
    lg = os.environ.get('GC_LOG')
    if lg: open(lg, 'a').write(os.path.abspath(f) + '\\n')
    return _r.check(f, *a, **k)
"""
def tools_copy(dst, stub=True, wrap_gc=True):
    """Copy of the tools freeze.py uses into dst/council-tools (reads live, writes only dst)."""
    T = os.path.join(dst, 'council-tools'); os.makedirs(T)
    ig = shutil.ignore_patterns('__pycache__', 'runs', 'selftest-scratch', '*.bak', 'design')
    shutil.copy2('/workspace/council-tools/current_snap.py', T)
    for d in ('send-guard', 'ground-check', 'thai-diff', 'fit-table'): shutil.copytree(f'/workspace/council-tools/{d}', f'{T}/{d}', ignore=ig)
    if wrap_gc:
        os.rename(f'{T}/ground-check/ground_check.py', f'{T}/ground-check/ground_check_real.py'); open(f'{T}/ground-check/ground_check.py', 'w').write(GC_WRAP)
    if stub:
        os.makedirs(f'{T}/sheets-scan'); open(f'{T}/sheets-scan/sheets_scan.py', 'w').write(STUB_SCAN)
    return T
TOOLS_COPY = tools_copy(os.path.join(ROOT, 'tools'))
def logs(sb): n = os.path.basename(os.path.dirname(sb)); return os.path.join(ROOT, f'gc-{n}.log'), os.path.join(ROOT, f'scan-{n}.log')
def readlog(p): return open(p).read().split() if os.path.isfile(p) else []

def fz(sb, *args, fault=None, stage_dir=None, paste=PASTE, snap='snap-st-0100MDT', quick=True, timeout=600, env_extra=None, tools=None):
    cmd = [sys.executable, FZ, '--sandbox', sb] + list(args)
    if stage_dir: cmd += ['--stage', stage_dir, '--paste', paste, '--snap-name', snap] + (['--skip-checks-v608'] if quick else [])
    env = dict(os.environ); env.pop('FREEZE_FAULT', None)
    if fault: env['FREEZE_FAULT'] = fault
    if tools == 'live': env.pop('FREEZE_TOOLS', None)
    else: env['FREEZE_TOOLS'] = tools or TOOLS_COPY
    env['GC_LOG'], env['SHEETS_SCAN_LOG'] = logs(sb)
    if env_extra: env.update(env_extra)
    r = subprocess.run(cmd, capture_output=True, text=True, env=env, timeout=timeout)
    return r.returncode, r.stdout + r.stderr

def sbx(name): return os.path.join(ROOT, name, 'sb')
def ptr(sb): return md5(os.path.join(sb, 'CURRENT-SNAP.txt'))
def hold(sb): return os.path.exists(os.path.join(sb, 'freeze', 'HOLD'))
def reason(sb):
    p = os.path.join(sb, 'freeze', 'HOLD.reason'); return open(p).read() if os.path.isfile(p) else ''
def failed_kept(name, rc, out, sb, step, p0):
    ok(f'{name}: exit 1, REASON names step {step}', rc == 1 and re.search(rf'^REASON: step {step} ', out, re.M), out[-400:])
    ok(f'{name}: HOLD kept + HOLD.reason written', hold(sb) and reason(sb).startswith(f'REASON: step {step}'), reason(sb)[:200])
    ok(f'{name}: sandbox pointer unchanged', ptr(sb) == p0)

# 1-2 clean dry run, clean real run (real checks_v608 unless --quick)
sb = sbx('clean'); T = stage('clean')
rc, out = fz(sb, stage_dir=T, quick=QUICK, timeout=900, *['--dry-run']); p0 = ptr(sb)
ok('clean dry run: exit 0, DRY RUN CLEAN', rc == 0 and 'DRY RUN CLEAN' in out, out[-600:])
ok('clean dry run: checks_v608 ran (0 new live False)' if not QUICK else 'clean dry run: checks_v608 skipped (--quick)', QUICK or '0 new live False' in out, out[-600:])
ok('clean dry run: no HOLD, pointer untouched, no snapshot dir', not hold(sb) and p0 == LIVE_MD5 and not os.path.exists(os.path.join(sb, 'snap-st-0100MDT')))
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
prevd = os.path.join(sb, 'snap-r2h-0021MDT'); pm = [l.split('  ', 1) for l in open(os.path.join(prevd, 'MANIFEST.md5')).read().splitlines()]
stg = {'./' + os.path.relpath(os.path.join(d, f), T) for d, _, fs in os.walk(T) for f in fs}
carried = [(h, r) for h, r in pm if r not in ('./DELTA.md', './renders-MANIFEST.md5', './trim-1B/nancys-adventure-english-v6-08-PASTE.md') and r not in stg]   # stage files win (their mtimes come from the stage)
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

def planted(name, step, fault=None, extra=None, paste=PASTE, prep=None, snap='snap-st-0100MDT'):
    sb = sbx(name); T = stage(name, extra)
    rc0, _ = fz(sb, '--status')   # seeds the sandbox
    if prep: prep(sb)
    p0 = ptr(sb); rc, out = fz(sb, stage_dir=T, fault=fault, paste=paste, snap=snap)
    failed_kept(name, rc, out, sb, step, p0); return sb, rc, out

# 3 verse byte change
def verses(T):
    b = bytearray(open(f'/workspace/{VN}', 'rb').read()); i = b.index(b'"en"') + 10; b[i] = b[i] ^ 0x20; open(f'{T}/{VN}', 'wb').write(bytes(b))
planted('verse-byte', 2, extra=verses)
# 4 over-ceiling
op = os.path.join(ROOT, 'over-PASTE.md'); open(op, 'w', encoding='utf-8').write(open(PASTE, encoding='utf-8').read() + 'x' * 100)
sb, rc, out = planted('over-ceiling', 1, paste=op); ok('over-ceiling: reason says over the ceiling', 'over the 188,200 ceiling' in out)
# 5 (v3) FREEZE_FAULT sendguard_exit3 is a no-op: the sheets leg is always send_guard --no-ground and requires exit 3
sb = sbx('sendguard-exit3'); T = stage('sendguard-exit3'); fz(sb, '--status')
rc, out = fz(sb, '--dry-run', stage_dir=T, fault='sendguard_exit3'); ok('v3 sendguard_exit3 fault is a no-op (sheets leg always --no-ground): dry run exit 0', rc == 0 and 'DRY RUN CLEAN' in out, out[-300:])
# 5b (v3) the old-path sheet in sheets/ goes to the sheets scan, NOT ground_check; a sheets-scan BLOCK fails the freeze
sb = sbx('sheets-scan-block'); T = stage('sheets-scan-block', lambda T: shutil.copy2(f'{R}/r2h/sheets/r2h-before-after.png', f'{T}/sheets/')); fz(sb, '--status'); p0 = ptr(sb)
rc, out = fz(sb, stage_dir=T, env_extra={'SHEETS_SCAN_STUB_BLOCK': 'r2h-before-after.png'}); gl, sl = logs(sb)
failed_kept('sheets-scan BLOCK', rc, out, sb, 3, p0)
ok('sheets-scan BLOCK: REASON names the sheets scan (exit 1), ground_check was never called', 'sheets scan exit 1' in out and readlog(gl) == [] and any(x.endswith('/sheets/r2h-before-after.png') for x in readlog(sl)), out[-300:])
# 5c (v3) routing: showcase/, sheets/, nested sheets (two kinds) and a normal render
r = subprocess.run([sys.executable, '-c', 'import sys,json;sys.path.insert(0,%r);import freeze as f;print(json.dumps([f.route(x) for x in sys.argv[1:]]))' % HERE,
                    './showcase/showcase-1-opening.png', './sheets/05-map-day1-390x844.png', './scene-fill-20261101/sheets/S01.png', './sheets/sub/x.png',
                    './renders/r2x/09-map-later-390x844.png', './sheets-ref/x.png', './renders/sheets.png', './showcase'],
                   env=dict(os.environ, FREEZE_TOOLS=TOOLS_COPY), capture_output=True, text=True)
want = ['sheets', 'sheets', 'sheets', 'sheets', 'single', 'single', 'single', 'single']
ok('route(): showcase/, sheets/, nested scene-fill/sheets/ and sheets/sub/ -> sheets; normal render, sheets-ref/, a file named sheets.png -> single', r.stdout.strip() == json.dumps(want), r.stdout + r.stderr[-300:])
def nested(T):
    for d in ('scene-fill-20261101/sheets', 'sheets/sub'): os.makedirs(os.path.join(T, d))
    shutil.copy2(f'{R}/r2h/png/09-map-later-390x844.png', f'{T}/scene-fill-20261101/sheets/S01-nested.png'); shutil.copy2(f'{R}/r2h/png/09-map-later-390x844.png', f'{T}/sheets/sub/sub-nested.png')
sb = sbx('routing'); T = stage('routing', nested); fz(sb, '--status'); p0 = ptr(sb)
rc, out = fz(sb, '--dry-run', stage_dir=T); gl, sl = logs(sb); sc = readlog(sl)
sg = open(os.path.join(sb, 'freeze', 'work', 'send-guard-snap-st-0100MDT.txt')).read() if os.path.isfile(os.path.join(sb, 'freeze', 'work', 'send-guard-snap-st-0100MDT.txt')) else ''
ok('routing dry run: exit 0, DRY RUN CLEAN, pointer untouched', rc == 0 and 'DRY RUN CLEAN' in out and ptr(sb) == p0, out[-400:])
ok('routing: showcase/ file -> sheets scan only', os.path.join(T, 'showcase/showcase-1-opening.png') in sc, sc)
ok('routing: sheets/ file -> sheets scan only', os.path.join(T, 'sheets/05-map-day1-390x844.png') in sc, sc)
ok('routing: nested scene-fill-20261101/sheets/ and sheets/sub/ files -> sheets scan only', os.path.join(T, 'scene-fill-20261101/sheets/S01-nested.png') in sc and os.path.join(T, 'sheets/sub/sub-nested.png') in sc, sc)
ok('routing: sheets scan got exactly the 4 sheets/showcase images, not the normal render', len(sc) == 4 and not any('/renders/' in x for x in sc), sc)
ok('routing: ground_check was called on NOTHING (no sheets/showcase path reached it)', readlog(gl) == [], readlog(gl))
ok('routing: send_guard ran --no-ground with nested --only prefixes, every sheets/showcase file OK in the candidate snapshot', 'GROUND SKIPPED' in sg and 'GRND' not in sg and 'RESULT CLEAR: 4 files' in sg and 'OK ' in sg and 'S01-nested.png = MANIFEST.md5:./scene-fill-20261101/sheets/S01-nested.png' in sg, sg[-500:])
ok('routing: normal render (renders/r2x/) not given to send_guard or the sheets scan (unchanged from 91aa8a3e)', '/renders/' not in sg and not any('/renders/' in x for x in sc), sg[-300:])
# control: the ground_check logger works (send_guard WITH ground on the tools copy logs the path)
cl = os.path.join(ROOT, 'gc-control.log')
r = subprocess.run([sys.executable, os.path.join(TOOLS_COPY, 'send-guard/send_guard.py'), os.path.join(T, 'sheets/05-map-day1-390x844.png')], env=dict(os.environ, GC_LOG=cl, CURRENT_SNAP=os.path.join(sb, 'CURRENT-SNAP.txt')), capture_output=True, text=True)
ok('control: ground_check logger records a direct send_guard ground call', readlog(cl) == [os.path.join(T, 'sheets/05-map-day1-390x844.png')], readlog(cl))
# 5d (v3) live tools have no sheets scan installed: a stage with sheets/showcase fails closed at step 3; a stage with none still passes
sb = sbx('no-scan'); T = stage('no-scan'); fz(sb, '--status', tools='live')
rc, out = fz(sb, '--dry-run', stage_dir=T, tools='live')
ok('no sheets scan installed (live tools): exit 1, REASON step 3 names the missing scan', rc == 1 and re.search(r'^REASON: step 3 render: \S*sheets-scan/sheets_scan.py: sheets scan not installed', out, re.M), out[-400:])
def nosheets(T):
    for d in ('sheets', 'showcase'): os.rename(os.path.join(T, d), os.path.join(T, d + '-moved-by-selftest'))
sb = sbx('no-sheets'); T = stage('no-sheets', nosheets); fz(sb, '--status', tools='live')
rc, out = fz(sb, '--dry-run', stage_dir=T, tools='live')
ok('stage with no sheets/showcase (live tools): dry run exit 0, scan not needed', rc == 0 and 'DRY RUN CLEAN' in out and 'no sheets/ or showcase/ files in stage' in out, out[-400:])
# 6 existing snap dir
sb, rc, out = planted('snap-exists', 1, prep=lambda sb: os.makedirs(os.path.join(sb, 'snap-st-0100MDT'))); ok('existing snap dir: refuses to overwrite', 'already exists' in out)
# 7 pointer md5 mismatch (pointer's own paste_1b changed on disk)
sb, rc, out = planted('pointer-mismatch', 1, prep=lambda sb: open(os.path.join(sb, 'r2h-build/nancys-adventure-english-v6-08-1B-v32-PASTE.md'), 'a').write(' ')); ok('pointer md5 mismatch named', 'pointer paste_1b_md5' in out)
# 8 a check fails mid-way (fit sheet naming an old PASTE -> fit_sheet_check exit 1)
sb, rc, out = planted('fit-stale', 3, extra=lambda T: open(f'{T}/fit-sheet-test.md', 'w').write('Fit sheet. PASTE for this sheet: 155f86bb\n')); ok('mid-way check fail: fit_sheet_check STALE stops the freeze', 'fit_sheet_check exit 1' in out)
# 9 paste copy md5 mismatch
sb, rc, out = planted('paste-copy', 4, fault='paste_copy_corrupt'); ok('paste copy mismatch: no snapshot at the final name', not os.path.exists(os.path.join(sb, 'snap-st-0100MDT')) and 'PASTE copy md5' in out)
# 10 disk full while writing MANIFEST
sb, rc, out = planted('enospc', 4, fault='manifest_enospc'); ok('ENOSPC: clean fail, no half-written snap at the final name, tmp named', not os.path.exists(os.path.join(sb, 'snap-st-0100MDT')) and 'No space left' in out and 'Half-built snapshot left' in out)
# 11 unwritable snapshot parent (real EACCES)
def ro(sb): os.chmod(sb, 0o555)
sb, rc, out = planted('unwritable', 4, prep=ro); os.chmod(sb, 0o755); ok('unwritable dir: clean fail at step 4, no snap', not os.path.exists(os.path.join(sb, 'snap-st-0100MDT')) and 'write failed' in out, out[-300:])
# 12 plain copy breaks mtimes (Auditor fault 9)
sb, rc, out = planted('plain-copy', 4, fault='plain_copy'); ok('fault 9: plain copy (mtimes lost) fails the freeze', 'mtime not preserved' in out)
# 13 pointer hand-moved during HOLD
sb = sbx('handmove'); T = stage('handmove'); fz(sb, '--status'); p0 = ptr(sb)
rc, out = fz(sb, stage_dir=T, fault='pointer_handmove')
ok('hand-moved pointer: exit 1 at step 5, refuses to write', rc == 1 and 'REASON: step 5 pointer' in out and 'moved by hand' in out, out[-300:])
ok('hand-moved pointer: the hand edit is left as-is (not overwritten), HOLD kept', 'hand-edited during HOLD' in open(os.path.join(sb, 'CURRENT-SNAP.txt')).read() and 'snap=snap-r2h-0021MDT' in open(os.path.join(sb, 'CURRENT-SNAP.txt')).read() and hold(sb))
# 14 failure AFTER the pointer moved -> automatic rollback (Watchman)
sb = sbx('step6'); T = stage('step6'); fz(sb, '--status'); p0 = ptr(sb)
rc, out = fz(sb, stage_dir=T, fault='step6_bad_pointer'); r = reason(sb)
ok('step-6 failure: exit 1, REASON step 6', rc == 1 and 'REASON: step 6 current_snap' in out, out[-400:])
ok('step-6 failure: pointer rolled back to the pre-freeze md5 automatically', ptr(sb) == p0 and 'POINTER MOVED to' in r and 'ROLLED BACK to ' + p0 in r)
ok('step-6 failure: restored pointer names the old, complete snap (not the new one)', 'snap=snap-r2h-0021MDT' in open(os.path.join(sb, 'CURRENT-SNAP.txt')).read() and hold(sb))
# 15 rollback itself fails -> the record says so with restore instructions
sb = sbx('rollback-fails'); T = stage('rollback-fails'); fz(sb, '--status'); p0 = ptr(sb)
rc, out = fz(sb, stage_dir=T, fault='step6_bad_pointer,rollback_fails'); r = reason(sb)
ok('rollback fails: HOLD kept, reason says POINTER MOVED ... NOT ROLLED BACK + restore command', rc == 1 and hold(sb) and 'POINTER MOVED to' in r and 'NOT ROLLED BACK' in r and 'cp ' in r, r[:300])
ok('rollback fails: --release refuses while the pointer does not verify', fz(sb, '--release')[0] == 2)
# 16 HOLD already present -> exit 2; --force-clear proceeds
sb = sbx('hold-present'); T = stage('hold-present'); fz(sb, '--hold', 'planted hold'); p0 = ptr(sb)
rc, out = fz(sb, stage_dir=T); ok('HOLD present: exit 2, pointer unchanged', rc == 2 and 'HOLD already present' in out and ptr(sb) == p0)
rc, out = fz(sb, '--force-clear', stage_dir=T); ok('HOLD present + --force-clear: freeze runs, old HOLD archived', rc == 0 and any('cleared' in f for f in os.listdir(os.path.join(sb, 'freeze', 'holds'))), out[-300:])
# 17 stale HOLD after a crash
sb = sbx('crash'); T = stage('crash'); fz(sb, '--status')
rc, out = fz(sb, stage_dir=T, fault='crash_after_hold')
ok('crash: process died, HOLD left, no reason', rc == 9 and hold(sb) and not reason(sb))
h = json.load(open(os.path.join(sb, 'freeze', 'HOLD'))); h['started_epoch'] -= 7200; json.dump(h, open(os.path.join(sb, 'freeze', 'HOLD'), 'w'))
rc, out = fz(sb, '--status'); ok('stale HOLD: --status exit 1 shows age and STALE', rc == 1 and 'STALE HOLD' in out and '(120 min)' in out, out)
rc, out = fz(sb, stage_dir=T); ok('stale HOLD: freeze refuses without --force-clear (exit 2)', rc == 2)
rc, out = fz(sb, '--force-clear', stage_dir=T); ok('stale HOLD: --force-clear freezes cleanly', rc == 0 and not hold(sb))
# 17b Auditor fault 8: HOLD in place, pointer moved under it -> --status and hold_check say so, --force-clear refuses (exit 2) and leaves the pointer
sb = sbx('hold-moved'); T = stage('hold-moved'); fz(sb, '--hold', 'fault 8 test'); open(os.path.join(sb, 'CURRENT-SNAP.txt'), 'a').write('working=moved under HOLD (selftest)\n'); p1 = ptr(sb)
rc, out = fz(sb, '--status'); ok('fault 8: --status exit 1 says POINTER MOVED since the HOLD', rc == 1 and 'POINTER MOVED since the HOLD' in out, out[-300:])
r = subprocess.run([sys.executable, HC], env=dict(os.environ, CURRENT_SNAP=os.path.join(sb, 'CURRENT-SNAP.txt')), capture_output=True, text=True)
ok('fault 8: hold_check exit 1 says POINTER MOVED since the HOLD', r.returncode == 1 and 'POINTER MOVED since the HOLD' in r.stdout, r.stdout)
rc, out = fz(sb, '--force-clear', stage_dir=T); ok('fault 8: --force-clear refuses (exit 2), pointer and HOLD left as they are', rc == 2 and 'MOVED since the HOLD' in out and ptr(sb) == p1 and hold(sb), out[-300:])
# 18 two concurrent freezes (fcntl lock)
sb = sbx('lock'); T = stage('lock'); fz(sb, '--status')
lf = open(os.path.join(sb, 'freeze', 'freeze.lock'), 'a+'); fcntl.flock(lf, fcntl.LOCK_EX | fcntl.LOCK_NB)
rc, out = fz(sb, stage_dir=T); ok('lock held: second freeze refused (exit 2), no HOLD written', rc == 2 and 'another freeze is running' in out and not hold(sb))
ok('lock held: --release refused (exit 2)', fz(sb, '--release')[0] == 2)
fcntl.flock(lf, fcntl.LOCK_UN); lf.close()
env = dict(os.environ); env.pop('FREEZE_FAULT', None)
A = subprocess.Popen([sys.executable, FZ, '--sandbox', sb, '--stage', T, '--paste', PASTE, '--snap-name', 'snap-st-A', '--skip-checks-v608'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=env)
time.sleep(0.4); rcB, outB = fz(sb, stage_dir=T, snap='snap-st-B'); outA = A.communicate()[0]
ok('two freezes at once: one runs (0), the other is refused (2)', A.returncode == 0 and rcB == 2 and 'another freeze is running' in outB, f'A={A.returncode} B={rcB}')
# 19 --hold / --status / --release
sb = sbx('manual'); fz(sb, '--status')
ok('--status with no HOLD: exit 0', fz(sb, '--status')[0] == 0)
rc, out = fz(sb, '--hold', 'Maxwell asked to stop'); ok('--hold: exit 0, HOLD written, broadcast printed', rc == 0 and hold(sb) and 'QM HOLD: Maxwell asked to stop. Stop work now.' in out)
ok('--hold again: exit 2', fz(sb, '--hold', 'again')[0] == 2)
rc, out = fz(sb, '--status'); ok('--status with HOLD: exit 1, shows reason', rc == 1 and 'Maxwell asked to stop' in out)
rc, out = fz(sb, '--release'); ok('--release: exit 0, HOLD archived, RESUME with Based-on sync', rc == 0 and not hold(sb) and 'QM RESUME' in out and 'Based on:' in out)
# 20 hold_check exit codes
e = dict(os.environ, CURRENT_SNAP=os.path.join(sb, 'CURRENT-SNAP.txt'))
ok('hold_check: exit 0 with no HOLD', subprocess.run([sys.executable, HC], env=e, capture_output=True).returncode == 0)
fz(sb, '--hold', 'hold_check test'); r = subprocess.run([sys.executable, HC], env=e, capture_output=True, text=True)
ok('hold_check: exit 1 + reason with HOLD', r.returncode == 1 and 'hold_check test' in r.stdout)
fz(sb, '--release')
ok('hold_check --hold-file on a missing file: exit 0', subprocess.run([sys.executable, HC, '--hold-file', os.path.join(ROOT, 'nope')], capture_output=True).returncode == 0)
# 21 guards: faults and the skip flag are refused without --sandbox (live untouched)
r = subprocess.run([sys.executable, FZ, '--stage', T, '--paste', PASTE, '--snap-name', 'snap-st-live'], env=dict(env, FREEZE_FAULT='step6_bad_pointer'), capture_output=True, text=True)
ok('FREEZE_FAULT without --sandbox: exit 2, nothing done', r.returncode == 2 and not os.path.exists('/workspace/v608build/freeze/HOLD'))
r = subprocess.run([sys.executable, FZ, '--stage', T, '--paste', PASTE, '--snap-name', 'snap-st-live', '--skip-checks-v608'], env=env, capture_output=True, text=True)
ok('--skip-checks-v608 without --sandbox: exit 2', r.returncode == 2)
r = subprocess.run([sys.executable, FZ, '--sandbox', '/workspace/v608build', '--status'], env=env, capture_output=True, text=True)
ok('--sandbox pointing at live v608build: exit 2', r.returncode == 2)
# 21b carry: the stage overrides a carried file
def q(T): open(f'{T}/QUEUE.md', 'w').write('QUEUE overridden by the stage (selftest)\n')
sb = sbx('override'); T = stage('override', q); fz(sb, '--status')
rc, out = fz(sb, stage_dir=T); sd = os.path.join(sb, 'snap-st-0100MDT')
ok('stage overrides a carried file: exit 0, snap QUEUE.md = stage bytes, DELTA says stage-overrides', rc == 0 and md5(os.path.join(sd, 'QUEUE.md')) == md5(os.path.join(T, 'QUEUE.md')) and '- stage-overrides: ./QUEUE.md ' in open(os.path.join(sd, 'DELTA.md')).read() and md5(os.path.join(sd, 'COSTS-and-LEDGER.md')) == md5(os.path.join(sb, 'snap-r2h-0021MDT', 'COSTS-and-LEDGER.md')), out[-300:])
# 21c --no-carry
sb = sbx('no-carry'); T = stage('no-carry'); fz(sb, '--status')
rc, out = fz(sb, '--no-carry', stage_dir=T); sd = os.path.join(sb, 'snap-st-0100MDT'); n_files = sum(len(f) for _, _, f in os.walk(sd))
ok('--no-carry: exit 0, snap = 4 stage files + PASTE + 3 manifests/DELTA only', rc == 0 and n_files == 8 and not os.path.exists(os.path.join(sd, 'QUEUE.md')) and '--no-carry: stage + PASTE only' in open(os.path.join(sd, 'DELTA.md')).read(), f'rc={rc} files={n_files} ' + out[-200:])
# 21d a corrupted carried file fails before the pointer moves
def corrupt(sb):
    f = os.path.join(sb, 'snap-r2h-0021MDT', 'QUEUE.md'); os.chmod(os.path.dirname(f), 0o755); os.chmod(f, 0o644); open(f, 'a').write('tampered\n')
sb, rc, out = planted('carry-corrupt', 3, prep=corrupt)
ok('corrupted carried file: named, no new snap, pointer untouched', 'carried file md5' in out and 'QUEUE.md' in out and not os.path.exists(os.path.join(sb, 'snap-st-0100MDT')), out[-300:])
# 22 the proposed council-tools/incoming/qm-hold-check.diff on a COPY of council-tools (live tools untouched)
P = os.path.join(ROOT, 'patched'); os.makedirs(P); tools_copy(P, stub=True, wrap_gc=False)   # v3: small copy (was cp -a of all 8.8 GB) + stub sheets scan
pr = subprocess.run(['patch', '-p1', '-i', '/workspace/council-tools/incoming/qm-hold-check.diff'], cwd=P, capture_output=True, text=True)
ok('hold-check diff applies cleanly to a copy', pr.returncode == 0, pr.stdout + pr.stderr)
sb = sbx('patched'); T = stage('patched'); pe = {'FREEZE_TOOLS': os.path.join(P, 'council-tools')}
rc, out = fz(sb, stage_dir=T, env_extra=pe); ok('with the diff applied: a clean freeze still runs through its own HOLD (exit 0)', rc == 0, out[-400:])
fz(sb, '--hold', 'diff test', env_extra=pe)
e2 = {k: v for k, v in os.environ.items() if k != 'NAE_FREEZE_RUNNING'}; e2['CURRENT_SNAP'] = os.path.join(sb, 'CURRENT-SNAP.txt')
r = subprocess.run([sys.executable, os.path.join(P, 'council-tools/send-guard/send_guard.py'), '--only', 'sheets/', os.path.join(T, 'sheets/05-map-day1-390x844.png')], env=e2, capture_output=True, text=True)
ok('with the diff applied: send_guard BLOCKs (exit 1) during a HOLD', r.returncode == 1 and 'HOLD in place' in r.stdout, r.stdout[-300:])
r = subprocess.run([sys.executable, '-c', f'import sys;sys.path.insert(0,{os.path.join(P, "council-tools")!r});import current_snap as c;c.read()'], env=e2, capture_output=True, text=True)
ok('with the diff applied: current_snap.read raises HoldError during a HOLD', r.returncode != 0 and 'HoldError' in r.stderr)
fz(sb, '--release', env_extra=pe)
r = subprocess.run([sys.executable, os.path.join(P, 'council-tools/send-guard/send_guard.py'), '--only', 'sheets/', os.path.join(T, 'sheets/05-map-day1-390x844.png')], env=e2, capture_output=True, text=True)
ok('with the diff applied: after --release send_guard is CLEAR (exit 0)', r.returncode == 0, r.stdout[-300:])
r = subprocess.run([sys.executable, FZ, '--status'], env=dict(env, FREEZE_TOOLS=os.path.join(P, 'council-tools')), capture_output=True, text=True)
ok('FREEZE_TOOLS without --sandbox: exit 2', r.returncode == 2)
# final
ok('live CURRENT-SNAP.txt md5 is still ' + LIVE_MD5, md5(LIVE) == LIVE_MD5)
ok('no live HOLD left', not os.path.exists('/workspace/v608build/freeze/HOLD'))
n = sum(1 for _, p in results if p)
print(f'\nSELFTEST {n}/{len(results)} {"PASS" if n == len(results) else "FAIL"}  (sandbox {ROOT}; live pointer {md5(LIVE)})')
sys.exit(0 if n == len(results) else 1)
