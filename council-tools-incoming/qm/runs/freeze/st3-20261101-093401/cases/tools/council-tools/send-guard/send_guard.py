#!/usr/bin/env python3
"""send-guard: refuse a send to Maxwell if any attachment isn't in the current snapshot.
Owner: Chancellor. Usage:
  python3 send_guard.py [--snap DIR] FILE [FILE ...]
  With no --snap, uses QM's CURRENT-SNAP.txt pointer. Any --snap that isn't the pointer's snap is refused.
  python3 send_guard.py --selftest
Checks each file's md5 against the snapshot's MANIFEST.md5 + renders-MANIFEST.md5.
Also refuses if the snapshot isn't the one in QM's CURRENT-SNAP.txt pointer, or if the pointer's MANIFEST md5s disagree with disk.
Exit 0 = all clear; 1 = misses (listed); 2 = bad input; 3 = clear but ground skipped (--no-ground, test only). Writes to stdout only."""
import argparse, hashlib, os, re, sys, tempfile, shutil

def md5(p):
    h = hashlib.md5()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''): h.update(b)
    return h.hexdigest()

def manifest_md5s(snap):
    out = {}
    for name in ('MANIFEST.md5', 'renders-MANIFEST.md5'):
        p = os.path.join(snap, name)
        if not os.path.isfile(p): continue
        for line in open(p, encoding='utf-8', errors='replace'):
            m = re.match(r'^([0-9a-f]{32})\s+\*?(.+)$', line.strip())
            if m: out.setdefault(m.group(1), []).append(f'{name}:{m.group(2)}')
    return out

def newest_snap(snap):
    parent = os.path.dirname(os.path.abspath(snap.rstrip('/')))
    snaps = [d for d in os.listdir(parent) if d.startswith('snap-') and os.path.isfile(os.path.join(parent, d, 'MANIFEST.md5'))]
    return max(snaps, key=lambda d: os.path.getmtime(os.path.join(parent, d, 'MANIFEST.md5'))) if snaps else None

def pointer_check(snap):
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    import current_snap as cs
    d = cs.read(); probs = cs.verify(d)
    if os.path.realpath(snap) != os.path.realpath(d['snap_dir']): probs.append(f'STALE-SNAP {snap} is not the pointer snap dir {d["snap_dir"]}')
    elif os.path.basename(snap.rstrip('/')) != d['snap']: probs.append(f'STALE-SNAP {os.path.basename(snap.rstrip("/"))} is not the pointer snap {d["snap"]}')
    return d, probs

def tool_id():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    cs = os.path.join(root, 'current_snap.py'); gc = os.path.join(root, 'ground-check', 'ground_check.py')
    return f'{md5(os.path.abspath(__file__))[:8]} current_snap {md5(cs)[:8] if os.path.isfile(cs) else "none"} ground_check {md5(gc)[:8] if os.path.isfile(gc) else "none"}'

def ground_problems(f):
    try:
        gdir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'ground-check')
        if gdir not in sys.path: sys.path.insert(0, gdir)
        import ground_check
        return ground_check.check(f)
    except Exception as e: return [f'ground-check could not run: {e}']

def stamp(extra=''):
    print(f'send-guard {tool_id()} {extra}'.rstrip())

IMG_EXT = ('.png', '.jpg', '.jpeg', '.webp', '.gif')
def is_image(f):
    try: head = open(f, 'rb').read(8)
    except OSError: return False
    return f.lower().endswith(IMG_EXT) or head.startswith(b'\x89PNG') or head.startswith(b'\xff\xd8\xff')

def run(snap, files, check_newest=True, use_pointer=False, only=None, ground=False):
    if not os.path.isfile(os.path.join(snap, 'MANIFEST.md5')):
        stamp(f'snap {snap}'); print(f'ERROR no MANIFEST.md5 in {snap}'); return 2
    man = manifest_md5s(snap)
    mman = md5(os.path.join(snap, 'MANIFEST.md5'))
    rp = os.path.join(snap, 'renders-MANIFEST.md5')
    rman = md5(rp) if os.path.isfile(rp) else 'none'
    print(f'send-guard {tool_id()} snap {os.path.basename(snap.rstrip("/"))} MANIFEST {mman[:8]} renders-MANIFEST {rman[:8]}')
    bad = 0
    if use_pointer:
        try: d, probs = pointer_check(snap)
        except Exception as e: print(f'ERROR pointer unreadable: {e}'); return 2
        print(f'pointer {d["pointer_md5"][:8]} snap {d["snap"]}')
        for p in probs: print(p); bad += 1
    elif check_newest:
        nw = newest_snap(snap)
        if nw and nw != os.path.basename(snap.rstrip('/')):
            print(f'STALE-SNAP newer snapshot exists: {nw}'); bad += 1
    if not files:
        print('ERROR no attachments given'); return 2
    names = {}
    for h, locs in man.items():
        for l in locs: names.setdefault(os.path.basename(l), set()).add(h)
    for f in files:
        if not os.path.isfile(f):
            print(f'MISS {f}: file not found'); bad += 1; continue
        h = md5(f)
        if h in man and only:
            hits = [l for l in man[h] if any(l.split(':', 1)[1].lstrip('./').startswith(o) for o in only)]
            if not hits:
                print(f'MISS {h[:8]} {f}: in snapshot but not under --only {",".join(only)} ({man[h][0]})'); bad += 1; continue
            loc = hits[0]
        elif h in man: loc = man[h][0]
        if h in man:
            dup = names.get(os.path.basename(loc), set()) - {h}
            print(f'OK   {h[:8]} {f} = {loc}' + (f'  WARN same name has {len(dup)} other md5(s) in this snapshot; confirm this is the approved look' if dup else ''))
        else: print(f'MISS {h[:8]} {f}: not in this snapshot'); bad += 1
        if ground and is_image(f):
            for w in ground_problems(f): print(f'GRND {h[:8]} {f}: {w}'); bad += 1
    print(f'RESULT {"BLOCK" if bad else "CLEAR"}: {len(files)} files, {bad} problems')
    return 1 if bad else 0

def selftest():
    base = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'selftest-scratch'); os.makedirs(base, exist_ok=True)
    d = tempfile.mkdtemp(prefix='run-', dir=base)
    try:
        old = os.path.join(d, 'snap-a'); new = os.path.join(d, 'snap-b')
        for s in (old, new): os.makedirs(s)
        cur = os.path.join(new, 'tile.png'); open(cur, 'wb').write(b'current')
        stale = os.path.join(old, 'tile.png'); open(stale, 'wb').write(b'stale')
        open(os.path.join(old, 'MANIFEST.md5'), 'w').write(f'{md5(stale)}  ./tile.png\n')
        import time; time.sleep(0.05)
        gst = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'ground-check', 'runs', 'selftest')
        dirty = os.path.join(new, 'dirty.png'); shutil.copy(os.path.join(gst, 'tile6-planted-path.png'), dirty)
        dirtyj = os.path.join(new, 'dirty-renamed.jpg'); shutil.copy(dirty, dirtyj)
        open(os.path.join(new, 'MANIFEST.md5'), 'w').write(f'{md5(cur)}  ./sheets/tile.png\n{md5(stale)}  ./round1/tile.png\n{md5(dirty)}  ./sheets/dirty.png\n')
        rend = os.path.join(new, 'r.png'); open(rend, 'wb').write(b'render')
        open(os.path.join(new, 'renders-MANIFEST.md5'), 'w').write(f'{md5(rend)}  screens/r.png\n')
        ptr = os.path.join(d, 'CURRENT-SNAP.txt')
        open(ptr, 'w').write(f'snap=snap-b\nmanifest_md5={md5(os.path.join(new,"MANIFEST.md5"))}\nrenders_manifest_md5={md5(os.path.join(new,"renders-MANIFEST.md5"))}\npaste_1a_md5=x\npaste_1a_chars=1\nbank=1\n')
        os.environ['CURRENT_SNAP'] = ptr
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        import importlib, current_snap; importlib.reload(current_snap); current_snap.POINTER = ptr
        null = open(os.devnull, 'w'); so = sys.stdout; sys.stdout = null
        try:
            r = [run(new, [cur], False, True), run(new, [cur, stale], False, True, ['sheets/']), run(old, [stale], False, True),
                 run(new, [os.path.join(d, 'nope.png')], False, True), run(new, [], False, True),
                 run(new, [rend], False, True), run(new, [stale], False, True, ['sheets/'])]
            open(os.path.join(old, 'MANIFEST.md5'), 'a').close(); os.utime(os.path.join(old, 'MANIFEST.md5'))
            r.append(run(old, [stale], False, True))
            lk = os.path.join(d, 'lk'); os.makedirs(lk); os.symlink(old, os.path.join(lk, 'snap-b'))
            r.append(run(os.path.join(lk, 'snap-b'), [stale], False, True))
            bad = os.path.join(d, 'bad-ptr.txt'); open(bad, 'w').write(open(ptr).read().replace('manifest_md5=', 'manifest_md5=0', 1))
            os.environ['CURRENT_SNAP'] = bad; importlib.reload(current_snap)
            r.append(run(new, [cur], False, True))
            open(bad, 'w').write(open(ptr).read().replace('renders_manifest_md5=', 'renders_manifest_md5=0', 1)); importlib.reload(current_snap)
            r.append(run(new, [cur], False, True))
            os.environ['CURRENT_SNAP'] = ptr; importlib.reload(current_snap)
            import subprocess
            cli = lambda *a: subprocess.run([sys.executable, os.path.abspath(__file__), *a], env=dict(os.environ, CURRENT_SNAP=ptr), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode
            r += [cli('--no-ground', '--only', 'sheets/', cur), cli('--no-ground', '--only', 'sheets/', stale), cli('--no-ground', '--snap', old, stale),
                  cli('--only', 'sheets/', dirty), cli('--only', 'sheets/', dirtyj), cli('--no', '--only', 'sheets/', cur)]
            r.append(subprocess.run([sys.executable, os.path.abspath(__file__), '--no-ground', cur], env=dict(os.environ, CURRENT_SNAP=os.path.join(d, 'nope.txt')), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode)
            first = subprocess.run([sys.executable, os.path.abspath(__file__), '--no-ground', cur], env=dict(os.environ, CURRENT_SNAP=ptr), capture_output=True, text=True).stdout.splitlines()[:1]
            r.append(int(bool(first) and ' current_snap ' in first[0] and ' ground_check ' in first[0]))
        finally: sys.stdout = so
        gp = lambda n: len(ground_problems(os.path.join(gst, n))) > 0 if os.path.isfile(os.path.join(gst, n)) else None
        r += [int(bool(gp('tile6-clean.png'))), int(bool(gp('tile6-planted-path.png'))), int(bool(gp('tile6-planted-float.png'))), int(bool(ground_problems(os.path.join(d, 'not-a-png.png'))))]
        want = [0, 1, 1, 1, 2, 0, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 2, 2, 1, 0, 1, 1, 1]
        ok = r == want
        print(f'selftest {"PASS" if ok else "FAIL"} {sum(a==b for a,b in zip(r,want))}/{len(want)}: clean={r[0]} stale-in-only={r[1]} non-pointer-snap={r[2]} missing={r[3]} empty={r[4]} renders-manifest={r[5]} old-name-outside-only={r[6]} touched-old-MANIFEST={r[7]} symlink-to-old={r[8]} pointer-md5-mismatch={r[9]} pointer-renders-mismatch={r[10]} cli-noground-clean={r[11]} cli-only={r[12]} cli-old-snap={r[13]} cli-ground-default={r[14]} cli-renamed-jpg={r[15]} cli-abbrev={r[16]} cli-no-pointer={r[17]} stamp-3-tools={r[18]} ground-clean={r[19]} ground-path={r[20]} ground-float={r[21]} ground-unreadable={r[22]} (want {want})')
        return 0 if ok else 1
    finally:
        print(f'note: selftest scratch kept at {d} (no-delete rule; a few bytes)')

if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter, allow_abbrev=False)
    ap.add_argument('--snap'); ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--only', help='comma list of snapshot path prefixes a file must be listed under, e.g. sheets/,showcase/')
    ap.add_argument('--no-ground', action='store_true', help='skip the ground-check pixel pass (old path stroke, floating trees); sends to Maxwell must not use this')
    ap.add_argument('files', nargs='*')
    a = ap.parse_args()
    if a.selftest: stamp('selftest'); sys.exit(selftest())
    if not a.snap:
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        import current_snap as cs
        try: a.snap = cs.read()['snap_dir']
        except Exception as e: stamp('snap ?'); print(f'ERROR pointer unreadable: {e}'); sys.exit(2)
    only = [o.strip().lstrip('./') for o in a.only.split(',')] if a.only else None
    rc = run(a.snap, a.files, check_newest=False, use_pointer=True, only=only, ground=not a.no_ground)
    if a.no_ground:
        print('GROUND SKIPPED (--no-ground): test only, NOT valid for a send to Maxwell')
        if rc == 0: rc = 3
    sys.exit(rc)
