# selftest wrapper: log <calling program> TAB <path>, then the real ground_check (ground_check_real.py = 944d543a byte copy)
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ground_check_real as _r
from ground_check_real import *
def check(f, *a, **k):
    lg = os.environ.get('GC_LOG')
    if lg: open(lg, 'a').write(os.path.basename(sys.argv[0] or '-') + '\t' + os.path.abspath(f) + '\n')
    return _r.check(f, *a, **k)
