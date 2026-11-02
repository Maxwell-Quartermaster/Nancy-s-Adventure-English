#!/usr/bin/env python3
"""Auditor fault kit: freeze.py cases (ported from Auditor's gate /workspace/audit/freeze-gate-91aa8a3e/gate.py and QM's
/workspace/v608build/freeze/selftest.py). Called by run_kit.py, never by hand on live files.
Env: FK_FZ (copy of freeze.py), FK_HC (copy of hold_check.py), FK_TOOLS (copy of council-tools with the gate hook wrapper),
FK_ROOT (scratch dir inside the kit), FK_STAGE (kit stage inputs), FK_HOOKS (kit hooks dir), FK_OUT (results json).
Every freeze call is --sandbox <dir under FK_ROOT>; the live pointer md5 is checked before and after every case."""
import fcntl, hashlib, json, os, re, shutil, subprocess, sys, traceback
FZ = os.environ['FK_FZ']; HC = os.environ['FK_HC']; TOOLS = os.environ['FK_TOOLS']; ROOT = os.environ['FK_ROOT']
STAGE = os.environ['FK_STAGE']; HOOKS = os.environ['FK_HOOKS']; OUT = os.environ['FK_OUT']
ONLY = set(x for x in os.environ.get('FK_ONLY', '').split(',') if x)
assert ROOT.startswith('/workspace/audit/fault-kit/'), ROOT
os.makedirs(ROOT, exist_ok=False)
LIVE = '/workspace/v608build/CURRENT-SNAP.txt'
PASTE0 = '/workspace/v608build/r2h-build/nancys-adventure-english-v6-08-1B-v32-PASTE.md'
VN = '/workspace/nancys-adventure-english-v6-08-daily-verses.json'
PREV = 'snap-r2h-0021MDT'; SNAP = 'snap-fk-0100MDT'
md5 = lambda p: hashlib.md5(open(p, 'rb').read()).hexdigest()
LIVE_MD5 = md5(LIVE)
BASE_ENV = {k: v for k, v in os.environ.items() if k not in ('NAE_FREEZE_RUNNING', 'FREEZE_FAULT', 'GATE_HOOK', 'GATE_STEP6_FAIL', 'CURRENT_SNAP') and not k.startswith('FK_')}
rows = []

def stage(c):
    T = f'{ROOT}/{c}/stage'; shutil.copytree(STAGE, T, copy_function=shutil.copy2); return T
def setup(c):
    sb = f'{ROOT}/{c}/sb'; T = stage(c); P = f'{ROOT}/{c}/PASTE.md'; shutil.copy2(PASTE0, P)
    fz(sb, '--status')
    if not os.path.isfile(f'{sb}/CURRENT-SNAP.txt'): raise RuntimeError('tool did not seed its --sandbox (no CURRENT-SNAP.txt)')
    return sb, T, P
def fz(sb, *args, T=None, P=None, fault=None, hook=None, extra=None, snap=SNAP, timeout=900):
    cmd = [sys.executable, FZ, '--sandbox', sb] + list(args)
    if T: cmd += ['--stage', T, '--paste', P, '--snap-name', snap, '--skip-checks-v608']
    env = dict(BASE_ENV, FREEZE_TOOLS=TOOLS, GATE_SB=sb)
    if P: env['GATE_PASTE'] = P
    if fault: env['FREEZE_FAULT'] = fault
    if hook: env['GATE_HOOK'] = f'{HOOKS}/{hook}'
    if extra: env.update(extra)
    r = subprocess.run(cmd, capture_output=True, text=True, env=env, timeout=timeout)
    return r.returncode, r.stdout + r.stderr
def ptr(sb): return md5(f'{sb}/CURRENT-SNAP.txt')
def hold(sb): return os.path.exists(f'{sb}/freeze/HOLD')
def reason(sb): p = f'{sb}/freeze/HOLD.reason'; return open(p).read() if os.path.isfile(p) else ''
def hc_run(sb): return subprocess.run([sys.executable, HC], env=dict(BASE_ENV, CURRENT_SNAP=f'{sb}/CURRENT-SNAP.txt'), capture_output=True, text=True)
def leftovers(sb):
    L = [n for n in sorted(os.listdir(sb)) if n.startswith(('.tmp-', 'snap-fk'))]
    w = f'{sb}/freeze/work'
    if os.path.isdir(w): L += ['freeze/work/' + n for n in sorted(os.listdir(w)) if n.startswith(('precheck-', 'dryrun-'))]
    return L
def reasonline(out): m = re.search(r'^REASON: .*$', out, re.M); return m.group(0)[:230] if m else (out.strip().splitlines() or [''])[-1][:230]
def rec(cid, actual, passed, rc=None):
    live = md5(LIVE) == LIVE_MD5
    rows.append(dict(id=cid, exit=rc, actual=actual[:600], verdict='PASS' if passed and live else 'FAIL', live_pointer_unchanged=live))
    print(f'{rows[-1]["verdict"]} {cid} exit={rc} :: {actual[:240]}', flush=True)
def failed(sb, rc, out, step, p0):
    return rc == 1 and re.search(rf'^REASON: step {step} ', out, re.M) is not None and hold(sb) and reason(sb).startswith(f'REASON: step {step}') and ptr(sb) == p0
def std_fail(cid, step, fault_env=None, hook=None, prep=None, extra=None, more=None, paste=None):
    sb, T, P = setup(cid)
    if paste: P = paste(cid, P)
    if prep: prep(sb, T, P)
    p0 = ptr(sb); rc, out = fz(sb, T=T, P=P, fault=fault_env, hook=hook, extra=extra)
    ok = failed(sb, rc, out, step, p0); note = ''
    if more: ok2, note = more(sb, T, P, rc, out, p0); ok = ok and ok2
    rec(cid, f'{reasonline(out)} | HOLD={hold(sb)} ptr_same={ptr(sb)==p0} left={leftovers(sb)} {note}', ok, rc)
    return sb, T, P, rc, out
no_snap = lambda sb, T, P, rc, out, p0: (not os.path.exists(f'{sb}/{SNAP}'), f'final_snap_exists={os.path.exists(f"{sb}/{SNAP}")}')
CASES = []
def case(cid):
    def deco(fn): CASES.append((cid, fn)); return fn
    return deco

@case('F0-clean')
def _():
    sb, T, P = setup('F0-clean'); p0 = ptr(sb)
    rc, out = fz(sb, '--dry-run', T=T, P=P)
    rec('F0a-clean-dry-run', reasonline(out) if rc else ('DRY RUN CLEAN' if 'DRY RUN CLEAN' in out else out[-200:]), rc == 0 and 'DRY RUN CLEAN' in out and ptr(sb) == p0 and not hold(sb), rc)
    rc, out = fz(sb, T=T, P=P); snapd = f'{sb}/{SNAP}'
    man = [l.split('  ', 1) for l in open(f'{snapd}/MANIFEST.md5').read().splitlines()] if os.path.isfile(f'{snapd}/MANIFEST.md5') else []
    mt_bad = []
    for h, rel in man:
        r_ = rel[2:]
        if r_ in ('MANIFEST.md5', 'renders-MANIFEST.md5', 'DELTA.md'): continue
        src = f'{T}/{r_}' if os.path.isfile(f'{T}/{r_}') else (P if r_ == 'trim-1B/nancys-adventure-english-v6-08-PASTE.md' else f'{sb}/{PREV}/{r_}')
        if os.stat(f'{snapd}/{r_}').st_mtime_ns != os.stat(src).st_mtime_ns: mt_bad.append(r_)
    md5_bad = [rel for h, rel in man if md5(f'{snapd}/{rel[2:]}') != h]
    rec('F9-pass-copy2-clean-run', f'{reasonline(out) if rc else "frozen"}; {len(man)} MANIFEST lines, md5 mismatches {len(md5_bad)}, mtime mismatches {len(mt_bad)} {mt_bad[:3]}; pointer moved {ptr(sb)!=p0}; HOLD={hold(sb)}',
        rc == 0 and bool(man) and not md5_bad and not mt_bad and ptr(sb) != p0 and not hold(sb), rc)

@case('F1a-fit-sheet-stale')
def _(): std_fail('F1a-fit-sheet-stale', 3, prep=lambda sb, T, P: open(f'{T}/fit-sheet-test.md', 'w').write('Fit sheet. PASTE for this sheet: 155f86bb\n'), more=no_snap)
@case('F1b-sendguard-BLOCK-hook')
def _(): std_fail('F1b-sendguard-BLOCK-hook', 3, hook='block.py', more=no_snap)
@case('F1c-sendguard-exit3')
def _():
    sb, T, P, rc, out = std_fail('F1c-sendguard-exit3', 3, fault_env='sendguard_exit3', more=lambda sb, T, P, rc, out, p0: ('send_guard exit 3' in out, ''))

def kept_edit(sb):
    t = open(f'{sb}/CURRENT-SNAP.txt').read(); return 'hand-edited' in t and f'snap={PREV}' in t
def f2(cid, **kw):
    sb, T, P = setup(cid); p0 = ptr(sb); rc, out = fz(sb, T=T, P=P, **kw); k = kept_edit(sb)
    ok = k and rc == 1 and 'REASON: step 5 pointer' in out and 'moved by hand' in out and hold(sb) and reason(sb).startswith('REASON: step 5')
    rec(cid, f'{reasonline(out)} | hand_edit_kept={k} left={leftovers(sb)}', ok, rc)
@case('F2a-handmove-FREEZE_FAULT')
def _(): f2('F2a-handmove-FREEZE_FAULT', fault='pointer_handmove')
@case('F2b-handmove-by-other-process-hook')
def _(): f2('F2b-handmove-by-other-process-hook', hook='handmove.py')

def f3(cid, **kw):
    sb, T, P = setup(cid); p0 = ptr(sb); rc, out = fz(sb, T=T, P=P, **kw)
    s_rc, s_out = fz(sb, '--status'); r2, o2 = fz(sb, T=T, P=P); hc = hc_run(sb)
    ok = rc in (9, -9) and hold(sb) and not reason(sb) and ptr(sb) == p0 and s_rc == 1 and 'STALE HOLD' in s_out and r2 == 2 and hc.returncode == 1
    r3, o3 = fz(sb, '--force-clear', T=T, P=P)
    rec(cid, f'crash exit {rc}, status={s_rc} STALE={"STALE HOLD" in s_out} rerun={r2} hold_check={hc.returncode}; force-clear rerun exit {r3}', ok and r3 == 0, rc)
@case('F3a-crash_after_hold-FREEZE_FAULT')
def _(): f3('F3a-crash_after_hold-FREEZE_FAULT', fault='crash_after_hold')
@case('F3b-SIGKILL-mid-step3-hook')
def _(): f3('F3b-SIGKILL-mid-step3-hook', hook='kill.py')

@case('F4a-paste_copy_corrupt-FREEZE_FAULT')
def _(): std_fail('F4a-paste_copy_corrupt-FREEZE_FAULT', 4, fault_env='paste_copy_corrupt', more=no_snap)
@case('F4b-source-PASTE-changed-mid-freeze-hook')
def _(): std_fail('F4b-source-PASTE-changed-mid-freeze-hook', 4, hook='pastechange.py', more=no_snap)

@case('F5a-ENOSPC-FREEZE_FAULT')
def _(): std_fail('F5a-ENOSPC-FREEZE_FAULT', 4, fault_env='manifest_enospc', more=lambda sb, T, P, rc, out, p0: (not os.path.exists(f'{sb}/{SNAP}') and 'Half-built snapshot left' in out, 'tmp_named=' + str('Half-built snapshot left' in out)))
@case('F5b-unwritable-parent-EACCES')
def _():
    sb = f'{ROOT}/F5b-unwritable-parent-EACCES/sb'
    try: std_fail('F5b-unwritable-parent-EACCES', 4, prep=lambda sb, T, P: os.chmod(sb, 0o555), more=no_snap)
    finally:
        if os.path.isdir(sb): os.chmod(sb, 0o755)

@case('F6-lock-held')
def _():
    sb, T, P = setup('F6-lock-held'); p0 = ptr(sb)
    lf = open(f'{sb}/freeze/freeze.lock', 'a+'); fcntl.flock(lf, fcntl.LOCK_EX | fcntl.LOCK_NB)
    try: rc, out = fz(sb, T=T, P=P); h_rc, _ = fz(sb, '--hold', 'x'); r_rc, _ = fz(sb, '--release')
    finally: fcntl.flock(lf, fcntl.LOCK_UN); lf.close()
    rec('F6-lock-held', f'freeze {rc} hold {h_rc} release {r_rc} HOLD={hold(sb)} | {reasonline(out)}', rc == 2 and h_rc == 2 and r_rc == 2 and not hold(sb) and ptr(sb) == p0, rc)

def f7(cid, **kw):
    sb, T, P = setup(cid); p0 = ptr(sb); rc, out = fz(sb, T=T, P=P, **kw); r = reason(sb); t = open(f'{sb}/CURRENT-SNAP.txt').read()
    m = re.search(r'^manifest_md5=(\w+)', t, re.M); prev_ok = bool(m) and md5(f'{sb}/{PREV}/MANIFEST.md5') == m.group(1)
    ok = rc == 1 and 'REASON: step 6' in out and ptr(sb) == p0 and f'ROLLED BACK to {p0}' in r and f'snap={PREV}\n' in t and prev_ok and hold(sb)
    rec(cid, f'{reasonline(out)} | ptr_restored={ptr(sb)==p0} prev_manifest_ok={prev_ok} left={leftovers(sb)}', ok, rc)
@case('F7a-step6_bad_pointer-FREEZE_FAULT')
def _(): f7('F7a-step6_bad_pointer-FREEZE_FAULT', fault='step6_bad_pointer')
@case('F7b-step6-verify-fail-independent')
def _(): f7('F7b-step6-verify-fail-independent', extra={'GATE_STEP6_FAIL': '1'})
@case('F7c-rollback-fails')
def _():
    sb, T, P = setup('F7c-rollback-fails'); p0 = ptr(sb); rc, out = fz(sb, T=T, P=P, fault='step6_bad_pointer,rollback_fails'); r = reason(sb)
    s_rc, s_out = fz(sb, '--status'); rl, _ = fz(sb, '--release')
    rec('F7c-rollback-fails', f'{reasonline(out)} | HOLD={hold(sb)} status={s_rc} moved={"POINTER MOVED" in s_out} release={rl}',
        rc == 1 and hold(sb) and 'NOT ROLLED BACK' in r and 'cp ' in r and s_rc == 1 and 'POINTER MOVED' in s_out and rl == 2, rc)

@case('F8a-manual-HOLD-then-freeze')
def _():
    sb, T, P = setup('F8a-manual-HOLD-then-freeze'); fz(sb, '--hold', 'manual hold (fault kit)'); p0 = ptr(sb); rc, out = fz(sb, T=T, P=P)
    rec('F8a-manual-HOLD-then-freeze', f'{(out.strip().splitlines() or [""])[0][:200]} | ptr_same={ptr(sb)==p0}', rc == 2 and ptr(sb) == p0 and hold(sb), rc)
@case('F8b-failed-freeze-HOLD-then-pointer-moved')
def _():
    c = 'F8b-failed-freeze-HOLD-then-pointer-moved'; sb, T, P = setup(c); open(f'{T}/fit-sheet-test.md', 'w').write('Fit sheet. PASTE for this sheet: 155f86bb\n'); p0 = ptr(sb)
    rc, out = fz(sb, T=T, P=P)
    open(f'{sb}/CURRENT-SNAP.txt', 'a').write('working=hand-moved while HOLD in place (fault kit)\n'); p1 = ptr(sb)
    s_rc, s_out = fz(sb, '--status'); hc = hc_run(sb)
    os.remove(f'{T}/fit-sheet-test.md')   # kit scratch stage copy only
    r2, o2 = fz(sb, '--force-clear', T=T, P=P); p2 = ptr(sb)
    fs = 'moved since the hold' in s_out.lower(); ff = r2 != 0 and p2 == p1 and 'moved since the hold' in o2.lower(); fh = 'moved since the hold' in hc.stdout.lower()
    rec(c, f'first run exit {rc}; --status flags={fs}; hold_check flags={fh}; --force-clear exit {r2} flags={ff}', fs and ff and fh, rc)
@case('F8c-manual-HOLD-pointer-moved-status-release')
def _():
    c = 'F8c-manual-HOLD-pointer-moved-status-release'; sb, T, P = setup(c); fz(sb, '--hold', 'manual'); open(f'{sb}/CURRENT-SNAP.txt', 'a').write('working=moved under HOLD\n')
    s_rc, s_out = fz(sb, '--status'); rl, rl_out = fz(sb, '--release')
    rec(c, f'--status exit {s_rc} flags={"moved since the hold" in s_out.lower()}; --release exit {rl} MOVED={"MOVED since the HOLD" in rl_out}', 'moved since the hold' in s_out.lower() and 'MOVED since the HOLD' in rl_out, s_rc)
@case('F8d-manual-HOLD-moved-force-clear')
def _():
    c = 'F8d-manual-HOLD-moved-force-clear'; sb, T, P = setup(c); fz(sb, '--hold', 'manual'); keep = open(f'{sb}/CURRENT-SNAP.txt').read()
    open(f'{sb}/CURRENT-SNAP.txt', 'a').write('working=moved under manual HOLD\n'); p1 = ptr(sb); hc = hc_run(sb)
    rc, out = fz(sb, '--force-clear', T=T, P=P)
    ok = rc == 2 and 'moved since the hold' in out.lower() and ptr(sb) == p1 and hold(sb) and hc.returncode == 1 and 'POINTER MOVED since the HOLD' in hc.stdout
    rec(c, f'hold_check {hc.returncode}; force-clear {rc} | ptr_left={ptr(sb)==p1} HOLD={hold(sb)}', ok, rc)
    open(f'{sb}/CURRENT-SNAP.txt', 'w').write(keep); r2, o2 = fz(sb, '--force-clear', T=T, P=P)
    rec('F8e-pointer-restored-then-force-clear', reasonline(o2) if r2 else 'frozen', r2 == 0 and not hold(sb), r2)
@case('F8f-moved-then-release-then-freeze')
def _():
    c = 'F8f-moved-then-release-then-freeze'; sb, T, P = setup(c); fz(sb, '--hold', 'manual'); open(f'{sb}/CURRENT-SNAP.txt', 'a').write('working=moved under HOLD\n')
    rl, rl_out = fz(sb, '--release'); r3, o3 = fz(sb, T=T, P=P)
    rec(c, f'release {rl} MOVED={"MOVED since the HOLD" in rl_out}; freeze {r3} {reasonline(o3) if r3 else ""}', rl == 0 and 'MOVED since the HOLD' in rl_out and r3 == 0, r3)

@case('F9a-plain_copy-FREEZE_FAULT')
def _(): std_fail('F9a-plain_copy-FREEZE_FAULT', 4, fault_env='plain_copy', more=lambda sb, T, P, rc, out, p0: (not os.path.exists(f'{sb}/{SNAP}') and 'mtime not preserved' in out, ''))

def wr(sb):
    d = f'{sb}/{PREV}'; os.chmod(d, 0o755)
    for r, ds, fs in os.walk(d):
        for n in ds: os.chmod(os.path.join(r, n), 0o755)
        for n in fs: os.chmod(os.path.join(r, n), 0o644)
def c_append(sb, T, P): wr(sb); open(f'{sb}/{PREV}/QUEUE.md', 'a').write('tampered\n')
def c_flip(sb, T, P):
    wr(sb); man = [l.split('  ', 1)[1].strip()[2:] for l in open(f'{sb}/{PREV}/MANIFEST.md5') if l.strip()]
    f = next(f'{sb}/{PREV}/{r}' for r in man if r.endswith('.png') and '/' in r); st = os.stat(f); b = bytearray(open(f, 'rb').read()); b[len(b) // 2] ^= 1
    open(f, 'wb').write(bytes(b)); os.utime(f, ns=(st.st_atime_ns, st.st_mtime_ns))
def c_missing(sb, T, P): wr(sb); os.rename(f'{sb}/{PREV}/QUEUE.md', f'{os.path.dirname(sb)}/QUEUE.md.moved-out')
def c_extra(sb, T, P): wr(sb); open(f'{sb}/{PREV}/EXTRA-unlisted.md', 'w').write('not in MANIFEST\n')
def c_manifest(sb, T, P):
    wr(sb); f = f'{sb}/{PREV}/QUEUE.md'; open(f, 'a').write('tampered\n'); m = f'{sb}/{PREV}/MANIFEST.md5'
    s = open(m).read(); s = re.sub(r'^[0-9a-f]{32}(  \./QUEUE\.md)$', md5(f) + r'\1', s, flags=re.M); open(m, 'w').write(s)
pc = lambda sb, T, P, rc, out, p0: (not os.path.exists(f'{sb}/{SNAP}') and not [x for x in leftovers(sb) if x.startswith('.tmp-')], f'final_snap={os.path.exists(f"{sb}/{SNAP}")}')
@case('F10a-carried-QUEUE.md-appended')
def _(): std_fail('F10a-carried-QUEUE.md-appended', 3, prep=c_append, more=pc)
@case('F10b-carried-png-1bit-flip-mtime-restored')
def _(): std_fail('F10b-carried-png-1bit-flip-mtime-restored', 3, prep=c_flip, more=pc)
@case('F10c-carried-file-missing')
def _(): std_fail('F10c-carried-file-missing', 3, prep=c_missing, more=pc)
@case('F10d-unlisted-file-in-prev-snap')
def _(): std_fail('F10d-unlisted-file-in-prev-snap', 3, prep=c_extra, more=pc)
@case('F10e-carried-file-corrupted-AFTER-carry-check-hook')
def _(): std_fail('F10e-carried-file-corrupted-AFTER-carry-check-hook', 4, hook='carrycorrupt_mid.py', more=no_snap)
@case('F10f-file-and-prev-MANIFEST-both-edited')
def _(): std_fail('F10f-file-and-prev-MANIFEST-both-edited', 1, prep=c_manifest, more=pc)

# ---- from QM's selftest.py (planted faults not in the gate)
def verses(sb, T, P):
    b = bytearray(open(VN, 'rb').read()); i = b.index(b'"en"') + 10; b[i] = b[i] ^ 0x20; open(f'{T}/{os.path.basename(VN)}', 'wb').write(bytes(b))
@case('S1-verse-byte-changed')
def _(): std_fail('S1-verse-byte-changed', 2, prep=verses, more=no_snap)
def over(cid, P):
    op = f'{ROOT}/{cid}/over-PASTE.md'; open(op, 'w', encoding='utf-8').write(open(P, encoding='utf-8').read() + 'x' * 100); return op
@case('S2-paste-over-188200-ceiling')
def _(): std_fail('S2-paste-over-188200-ceiling', 1, paste=over, more=lambda sb, T, P, rc, out, p0: ('ceiling' in out, ''))
@case('S3-snap-dir-already-exists')
def _(): std_fail('S3-snap-dir-already-exists', 1, prep=lambda sb, T, P: os.makedirs(f'{sb}/{SNAP}'), more=lambda sb, T, P, rc, out, p0: ('already exists' in out, ''))
@case('S4-pointer-paste-md5-mismatch')
def _(): std_fail('S4-pointer-paste-md5-mismatch', 1, prep=lambda sb, T, P: open(f'{sb}/r2h-build/nancys-adventure-english-v6-08-1B-v32-PASTE.md', 'a').write(' '), more=lambda sb, T, P, rc, out, p0: ('paste_1b_md5' in out, ''))

for cid, fn in CASES:
    if ONLY and cid not in ONLY: continue
    try: fn()
    except Exception as e:
        rec(cid, f'HARNESS EXCEPTION (counts as FAIL): {e.__class__.__name__}: {e} | {traceback.format_exc().splitlines()[-2][:200]}', False)
    # free disk: remove this case's sandbox (inside the kit scratch dir only)
    d = os.path.join(ROOT, cid)
    for sub in os.listdir(ROOT):
        p = os.path.join(ROOT, sub)
        if os.path.isdir(p) and p.startswith('/workspace/audit/fault-kit/'):
            subprocess.run(['chmod', '-R', 'u+w', p]); shutil.rmtree(p, ignore_errors=True)
json.dump(dict(live_pointer_before=LIVE_MD5, live_pointer_after=md5(LIVE), rows=rows), open(OUT, 'w'), indent=1)
