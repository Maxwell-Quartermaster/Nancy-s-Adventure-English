#!/usr/bin/env python3
"""hold_check.py - Owner: Quartermaster. Is QM's freeze HOLD in place?
Any bot or tool calls this before editing the build or sending anything:
    python3 /workspace/v608build/freeze/hold_check.py [--hold-file PATH]
Exit 0 = no HOLD (go ahead). Exit 1 = HOLD in place (prints who/when/why; stop work until QM posts RESUME).
The HOLD file is <dir of the pointer>/freeze/HOLD; the pointer is $CURRENT_SNAP or /workspace/v608build/CURRENT-SNAP.txt.
Reads only. Never writes."""
import hashlib, json, os, sys, time

def hold_path():
    if '--hold-file' in sys.argv: return sys.argv[sys.argv.index('--hold-file') + 1]
    ptr = os.environ.get('CURRENT_SNAP', '/workspace/v608build/CURRENT-SNAP.txt')
    return os.path.join(os.path.dirname(os.path.abspath(ptr)), 'freeze', 'HOLD')

def check(path=None):
    """Return None if no HOLD, else a one-line reason."""
    path = path or hold_path()
    if not os.path.exists(path): return None
    try: h = json.load(open(path, encoding='utf-8'))
    except Exception: h = {}
    age = (time.time() - os.path.getmtime(path)) / 60
    rp = path + '.reason'
    why = open(rp, encoding='utf-8').read().strip().splitlines()[0] if os.path.isfile(rp) else h.get('reason', 'freeze in progress')
    ptr = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(path))), 'CURRENT-SNAP.txt'); was = h.get('pointer_md5_at_hold')
    cur = hashlib.md5(open(ptr, 'rb').read()).hexdigest() if os.path.isfile(ptr) else None
    moved = f' POINTER MOVED since the HOLD ({was} -> {cur}).' if was and cur != was else ''   # Auditor fault 8
    return f"HOLD in place ({path}): {why}; snap {h.get('snap', '?')}, started {h.get('started', '?')} ({age:.0f} min ago), by {h.get('by', 'Quartermaster')}.{moved} Stop work; wait for QM's RESUME."

if __name__ == '__main__':
    r = check()
    if r: print(r); sys.exit(1)
    print('no HOLD: clear to work'); sys.exit(0)
