#!/usr/bin/env python3
"""sheets_scan.py - ground check for send sheets, judged per panel. Author: Chancellor (QM assignment, Nov 1 2026).
Split out of freeze.py per-panel v2 (c19c845f) so freeze-v3 can call it after send_guard --no-ground.

  CURRENT_SNAP=/path/to/CURRENT-SNAP.txt python3 sheets_scan.py FILE [FILE...]
  python3 sheets_scan.py --selftest

Per FILE:
  image with X.png.sources.txt (or X.sources.txt) listing image lines "md5  path": every panel must exist and match its md5
    (else BLOCK), then each panel goes through ground_check.check() as one render. The sheet itself is not ground-checked.
  image with no sources file (or one listing no image): the whole file goes through ground_check.check().
  anything else (json, txt, sources.txt): SKIP line, counts neither way.
Exit: 0 PASS (every file clear), 1 BLOCK (a problem found), 2 ERROR (bad usage, CURRENT_SNAP unset/unreadable, a FILE or
  panel that cannot be read, ground_check would not load). ERROR wins over BLOCK. Both mean not sendable.
Ground check used: ../ground-check/ground_check.py next to this file's own folder (installed: $TOOLS/ground-check, the
  same tree freeze runs from, FREEZE_TOOLS copies included); SHEETS_SCAN_GROUND overrides the path, for testing a candidate only. Panels are checked one at a time, never in parallel (ground_check
  swaps shared settings, KNOWN-LIMITS A6).
Writes nothing and deletes nothing. --selftest makes its own scratch folder with makedirs under this tool's folder
  (never /tmp) and keeps it."""
import hashlib, importlib.util, os, sys, time

IMG_EXT = ('.png', '.jpg', '.jpeg', '.webp')
TOOLS = os.environ.get('TOOLS', '/workspace/council-tools')
def is_img(f): return f.lower().endswith(IMG_EXT)
def md5(p): return hashlib.md5(open(p, 'rb').read()).hexdigest()

def sources_of(f):
    """Same rule as freeze.py v2: [(md5, abs path)] of image lines in X.png.sources.txt (else X.sources.txt); None when there is
    no sources file or it lists no image. A relative path is taken from the sheet's own folder."""
    for c in (f + '.sources.txt', os.path.splitext(f)[0] + '.sources.txt'):
        if os.path.isfile(c):
            out = []
            for line in open(c, encoding='utf-8', errors='replace'):
                p = line.split(None, 1)
                if len(p) == 2 and len(p[0]) == 32 and is_img(p[1].strip()):
                    path = p[1].strip()
                    out.append((p[0].lower(), path if os.path.isabs(path) else os.path.join(os.path.dirname(os.path.abspath(f)), path)))
            return out or None
    return None

def load_ground():
    # v1.1: default is the ground_check in the SAME tools tree as this file (<tools>/sheets-scan/ -> <tools>/ground-check/),
    # so a freeze run on a FREEZE_TOOLS copy judges with that copy's ground_check, never silently with the live one.
    path = os.environ.get('SHEETS_SCAN_GROUND') or os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'ground-check', 'ground_check.py')
    s = importlib.util.spec_from_file_location('sheets_scan_gc', path); m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    if not callable(getattr(m, 'check', None)): raise RuntimeError(f'{path} has no check(path)')
    return m, path

def scan(files, out=print):
    ptr = os.environ.get('CURRENT_SNAP', '')
    if not files: out('ERROR usage: sheets_scan.py FILE [FILE...] (CURRENT_SNAP set to the candidate pointer)'); return 2
    if not ptr or not os.path.isfile(ptr): out(f'ERROR CURRENT_SNAP unset or not a file: {ptr!r}'); return 2
    try: gc, gpath = load_ground()
    except Exception as e: out(f'ERROR ground_check would not load: {type(e).__name__}: {e}'); return 2
    out(f'BASE pointer {md5(ptr)[:8]} ({ptr}); ground_check {md5(gpath)[:8]}')
    worst, n = 0, {'PASS': 0, 'BLOCK': 0, 'ERROR': 0, 'SKIP': 0}
    for f in files:
        if not os.path.isfile(f): out(f'ERROR {f}: no such file'); n['ERROR'] += 1; worst = 2; continue
        if not is_img(f): out(f'SKIP  {f}: not an image'); n['SKIP'] += 1; continue
        src = sources_of(f); why, err = [], []
        targets = [(None, f)] if src is None else src
        for h, p in targets:
            if h is not None:
                if not os.path.isfile(p): why.append(f'panel missing {p} (sources.txt {h[:8]})'); continue
                if md5(p) != h: why.append(f'panel stale {p} (sources.txt {h[:8]}, disk {md5(p)[:8]})'); continue
            try: probs = gc.check(p)
            except Exception as e: err.append(f'{p}: {type(e).__name__}: {e}'); continue
            why += [f'{os.path.basename(p)}: {q}' for q in probs]
        mode = 'whole' if src is None else f'{len(src)} panels'
        if err: out(f'ERROR {f} [{mode}]: ' + '; '.join(err + why)); n['ERROR'] += 1; worst = 2
        elif why: out(f'BLOCK {f} [{mode}]: ' + '; '.join(why)); n['BLOCK'] += 1; worst = max(worst, 1)
        else: out(f'PASS  {f} [{mode}]'); n['PASS'] += 1
    out('RESULT ' + ' '.join(f'{k}={v}' for k, v in n.items()) + f' exit {worst}')
    return worst

def selftest():
    import csv, shutil, subprocess
    from PIL import Image
    here = os.path.dirname(os.path.abspath(__file__))
    sd = os.path.join(here, 'selftest-runs', f'{time.strftime("%Y%m%d-%H%M%SZ", time.gmtime())}-{os.getpid()}'); os.makedirs(sd)
    ptr = '/workspace/v608build/CURRENT-SNAP.txt'
    PACK = os.path.join(TOOLS, 'incoming', 'auditor-sheets-scan-cases-v1')
    ok = tot = 0
    def run(args, env_over, want, name):
        nonlocal ok, tot
        env = dict(os.environ, CURRENT_SNAP=ptr); env.update(env_over)
        env = {k: v for k, v in env.items() if v is not None}
        r = subprocess.run([sys.executable, os.path.abspath(__file__)] + args, env=env, capture_output=True, text=True, timeout=900)
        tb = 'Traceback' in r.stderr
        good = r.returncode == want and not tb; tot += 1; ok += good
        print(f"{'OK ' if good else 'BAD'} {name}: want {want} got {r.returncode}{' TRACEBACK' if tb else ''} | {r.stdout.strip().splitlines()[-2 if len(r.stdout.strip().splitlines()) > 1 else -1][:110] if r.stdout.strip() else r.stderr.strip()[-110:]}")
    # pack: every PASS/BLOCK sheet from Auditor's case pack, one file per run
    for row in csv.DictReader(open(os.path.join(PACK, 'expected.csv'))):
        if row['expected'] in ('PASS', 'BLOCK'):
            run([os.path.join(PACK, row['file'])], {}, 0 if row['expected'] == 'PASS' else 1, 'pack ' + row['file'].split('/')[1])
    # synthetic cases, built in our own scratch
    a = os.path.join(PACK, 'cases'); tile = next(os.path.join(r, x) for r, _, fs in os.walk(a) for x in sorted(fs) if x == '26A.png')
    good_tile = os.path.join(sd, 'tile.png'); shutil.copy2(tile, good_tile)
    sheet = os.path.join(sd, 'sheet.png'); Image.new('RGB', (40, 40), (244, 239, 228)).save(sheet)
    open(sheet + '.sources.txt', 'w').write(f'caption test sheet\n{md5(good_tile)}  {good_tile}\n')
    run([sheet], {}, 0, 'sourced sheet, clean panel -> PASS')
    stale = os.path.join(sd, 'stale.png'); shutil.copy2(sheet, stale)
    open(stale + '.sources.txt', 'w').write(f'{"0" * 32}  {good_tile}\n')
    run([stale], {}, 1, 'stale panel md5 -> BLOCK')
    miss = os.path.join(sd, 'miss.png'); shutil.copy2(sheet, miss)
    open(miss + '.sources.txt', 'w').write(f'{md5(good_tile)}  {os.path.join(sd, "nope.png")}\n')
    run([miss], {}, 1, 'missing panel -> BLOCK')
    rel = os.path.join(sd, 'rel.png'); shutil.copy2(sheet, rel)
    open(rel + '.sources.txt', 'w').write(f'{md5(good_tile)}  tile.png\n')
    run([rel], {}, 0, 'relative panel path -> PASS')
    bad = os.path.join(sd, 'bad-panel.png'); open(bad, 'wb').write(b'not a png')
    bs = os.path.join(sd, 'badsheet.png'); shutil.copy2(sheet, bs)
    open(bs + '.sources.txt', 'w').write(f'{md5(bad)}  {bad}\n')
    run([bs], {}, 2, 'unreadable panel -> ERROR')
    j = os.path.join(sd, 'x.json'); open(j, 'w').write('{}')
    run([j], {}, 0, 'non-image -> SKIP, exit 0')
    run([os.path.join(sd, 'absent.png')], {}, 2, 'missing FILE -> ERROR')
    run([sheet], {'CURRENT_SNAP': None}, 2, 'CURRENT_SNAP unset -> ERROR')
    run([sheet], {'CURRENT_SNAP': os.path.join(sd, 'no-ptr.txt')}, 2, 'CURRENT_SNAP not a file -> ERROR')
    run([sheet], {'SHEETS_SCAN_GROUND': os.path.join(sd, 'no-gc.py')}, 2, 'ground_check missing -> ERROR')
    run([], {}, 2, 'no FILE -> ERROR')
    run([sheet, stale], {}, 1, 'mixed PASS+BLOCK -> BLOCK')
    run([stale, bs], {}, 2, 'BLOCK+ERROR -> ERROR wins')
    print(f'SELFTEST {ok}/{tot} (scratch kept: {sd})')
    return 0 if ok == tot else 1

if __name__ == '__main__':
    if sys.argv[1:2] == ['--selftest']: sys.exit(selftest())
    sys.exit(scan(sys.argv[1:]))
