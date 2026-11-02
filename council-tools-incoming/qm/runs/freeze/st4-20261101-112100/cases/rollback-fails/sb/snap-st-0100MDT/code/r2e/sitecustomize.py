# r2e no-delete shim (QM, Oct 31 2026): every delete call is logged and skipped. Nothing is ever removed.
import os, shutil, sys
_LOG = '/tmp/qmtmp/r2e/nodelete.log'
def _skip(kind):
    def f(p, *a, **k):
        try: open(_LOG, 'a').write(f'{kind} skipped: {p} (pid {os.getpid()}, {sys.argv[0] if sys.argv else ""})\n')
        except Exception: pass
    return f
shutil.rmtree = _skip('rmtree'); os.remove = _skip('remove'); os.unlink = _skip('unlink'); os.rmdir = _skip('rmdir'); os.removedirs = _skip('removedirs')
import tempfile; tempfile.tempdir = os.environ.get('QM_TMP', '/dev/shm/qm-r2e'); os.makedirs(tempfile.tempdir, exist_ok=True)
_mk = tempfile.mkdtemp
def _mkdtemp(suffix=None, prefix=None, dir=None): return _mk(suffix, prefix, tempfile.tempdir)   # every temp dir lands under QM_TMP (default /dev/shm/qm-r2e: RAM, so the disk stays under 95%), so leftovers are easy to list
tempfile.mkdtemp = _mkdtemp
