"""Shared reader for QM's build pointer /workspace/v608build/CURRENT-SNAP.txt. Owner: Chancellor.
QM (build lead) updates the pointer on every freeze; tools refuse anything that disagrees with it."""
import os, hashlib
POINTER = os.environ.get('CURRENT_SNAP', '/workspace/v608build/CURRENT-SNAP.txt')
def md5(p):
    h = hashlib.md5()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''): h.update(b)
    return h.hexdigest()
class HoldError(RuntimeError): pass
def hold(path=POINTER):
    """QM freeze HOLD (Maxwell t511u): reason string if <pointer dir>/freeze/HOLD exists, else None."""
    h = os.path.join(os.path.dirname(os.path.abspath(path)), 'freeze', 'HOLD')
    if not os.path.exists(h): return None
    r = h + '.reason'
    return open(r, encoding='utf-8').read().strip().splitlines()[0] if os.path.isfile(r) else 'freeze in progress (see freeze/HOLD)'
def read(path=POINTER):
    # Tools refuse to read the pointer while QM's HOLD is in place; freeze.py itself sets NAE_FREEZE_RUNNING=1.
    _h = None if os.environ.get('NAE_FREEZE_RUNNING') == '1' else hold(path)
    if _h: raise HoldError(f'QM HOLD in place: {_h}; stop work until QM posts RESUME')
    d = {}
    for line in open(path, encoding='utf-8'):
        if '=' in line:
            k, v = line.rstrip('\n').split('=', 1); d[k.strip()] = v.strip()
    for k in ('snap', 'manifest_md5', 'paste_1a_md5', 'paste_1a_chars', 'bank'):
        if k not in d: raise ValueError(f'pointer {path} missing {k}')
    d['snap_dir'] = os.path.join(os.path.dirname(os.path.abspath(path)), d['snap'])
    d['pointer_md5'] = md5(path)
    return d
def verify(d):
    """Return list of problems between pointer and disk."""
    probs = []
    m = os.path.join(d['snap_dir'], 'MANIFEST.md5')
    if not os.path.isfile(m): return [f'{m} missing']
    if md5(m) != d['manifest_md5']: probs.append(f'MANIFEST {md5(m)[:8]} != pointer {d["manifest_md5"][:8]}')
    r = os.path.join(d['snap_dir'], 'renders-MANIFEST.md5')
    if os.path.isfile(r) and not d.get('renders_manifest_md5'): probs.append('pointer has no renders_manifest_md5 but renders-MANIFEST.md5 exists')
    elif d.get('renders_manifest_md5') and os.path.isfile(r) and md5(r) != d['renders_manifest_md5']:
        probs.append(f'renders-MANIFEST {md5(r)[:8]} != pointer {d["renders_manifest_md5"][:8]}')
    return probs
