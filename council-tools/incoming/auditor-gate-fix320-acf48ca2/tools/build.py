# Watchman gate harness: build every SCR page of <src>/play_v608.py at one size, in Python only (no Chrome, no shot()).
# Usage: python3 -B build.py <srcdir> <390|375|320> <out.json> [htmldir]   (320 needs NAE_SE=1 in env)
import sys, os, json, hashlib
sys.dont_write_bytecode = True
src, size, outp = sys.argv[1], sys.argv[2], sys.argv[3]; hdir = sys.argv[4] if len(sys.argv) > 4 else None
EV = []
WATCH = ('open', 'os.remove', 'os.unlink', 'os.rename', 'os.replace', 'os.rmdir', 'shutil.rmtree', 'shutil.copyfile', 'os.mkdir', 'os.symlink',
         'socket.connect', 'socket.getaddrinfo', 'socket.bind', 'subprocess.Popen', 'os.system', 'os.exec', 'os.posix_spawn', 'os.fork',
         'tempfile.mkstemp', 'tempfile.mkdtemp', 'urllib.Request', 'os.putenv', 'os.unsetenv', 'os.chmod', 'os.truncate')
def hook(ev, args):
    if ev in WATCH:
        if ev == 'open':
            p, mode, flags = args
            if not isinstance(p, str): return
            w = (isinstance(mode, str) and any(c in mode for c in 'wax+')) or (isinstance(flags, int) and flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT))
            EV.append(('open-w' if w else 'open-r', os.path.realpath(p)))
        else: EV.append((ev, repr(args)[:200]))
sys.addaudithook(hook)
sys.argv = ['x']
sys.path.insert(0, os.path.abspath(src))
import play_v608 as PV
assert os.path.dirname(os.path.abspath(PV.__file__)) == os.path.abspath(src), PV.__file__
W, H = {'390': (390, 844), '375': (375, 667), '320': (320, 568)}[size]
assert PV.SE == (size == '320')
if size == '375': PV.W, PV.H = 375, 667
res = {}
for n, (slug, st, srcd, fn) in sorted(PV.SCR.items()):
    try:
        d = PV.page(W, H, fn())
        if 24 <= n <= 28: d = PV.guardian_chip(d, n)
        b = d.encode('utf-8'); res[f'{n:02d}-{slug}'] = hashlib.md5(b).hexdigest()
        if hdir and n in (26, 30, 37):
            os.makedirs(hdir, exist_ok=True); open(f'{hdir}/{n:02d}-{slug}-{W}x{H}.html', 'w', encoding='utf-8').write(d)
    except BaseException as e:
        res[f'{n:02d}-{slug}'] = 'ERROR ' + type(e).__name__ + ': ' + str(e)[:200]
reads = sorted({p for k, p in EV if k == 'open-r'}); writes = sorted({p for k, p in EV if k == 'open-w'})
other = [e for e in EV if not e[0].startswith('open')]
json.dump({'src': src, 'size': size, 'pages': res, 'reads': reads, 'writes': writes, 'other': other}, open(outp, 'w'), indent=1, ensure_ascii=False)
print(size, len(res), 'pages;', sum(v.startswith('ERROR') for v in res.values()), 'errors;', len(reads), 'reads;', len(writes), 'writes;', len(other), 'other events')
