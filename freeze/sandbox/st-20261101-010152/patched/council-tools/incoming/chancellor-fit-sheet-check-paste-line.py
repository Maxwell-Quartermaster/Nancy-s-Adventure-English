"""fit_sheet_check.py - Owner: Chancellor. Refuses a fit/cost sheet unless it carries a line
'PASTE for this sheet: <32-hex md5>' that equals the CURRENT pointer's paste_1b md5 (full value, or its
prefix if the pointer holds only a prefix), and the pointer's paste_1b file is on disk at that md5.
A bare mention of the md5 elsewhere in the sheet (header, chain notes) no longer counts (false-CURRENT fix).
Usage: python3 fit_sheet_check.py [--expect-paste MD5] SHEET.md [...]
       python3 fit_sheet_check.py --selftest
--expect-paste checks a sheet written on a staged candidate before the pointer moves: exit 0 only if the
sheet's PASTE line matches MD5 (prefix allowed), printed as 'CANDIDATE, not pointer'.
Exit 0 = CURRENT (or CANDIDATE with --expect-paste), 1 = STALE, 2 = pointer error or bad usage."""
import sys,os,re,hashlib
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,os.path.dirname(HERE))
import current_snap as cs
LINE=re.compile(r'^PASTE for this sheet: ([0-9a-f]{32})\s*$',re.M)
def md(p): return hashlib.md5(open(p,'rb').read()).hexdigest()
def same(a,b): n=min(len(a),len(b)); return n>=8 and a[:n]==b[:n]
def judge(text,want,expect=None):
    """-> (exit, label, reason). want = pointer paste_1b md5 (full or prefix); expect = --expect-paste value or None."""
    m=LINE.findall(text)
    if not m: return 1,'STALE','no PASTE line'
    if len(set(m))>1: return 1,'STALE','several different PASTE lines: '+', '.join(sorted(set(m)))
    got=m[0]
    if expect:
        if same(got,expect): return 0,('CURRENT' if same(got,want) else 'CANDIDATE, not pointer'),f'PASTE {got[:8]} matches --expect-paste {expect[:8]}'
        return 1,'STALE',f'mismatch: sheet PASTE {got[:8]} vs --expect-paste {expect[:8]}'
    if same(got,want): return 0,'CURRENT',f'PASTE {got[:8]} = pointer paste_1b {want[:8]}'
    return 1,'STALE',f'mismatch: sheet PASTE {got[:8]} vs pointer paste_1b {want[:8]}'
def selftest(want):
    R='/workspace/chancellor/r2h/'
    v32=open(R+'fit-1B-v3.2-0041MDT.md',encoding='utf-8').read()
    import glob; v32a=open(sorted(glob.glob(R+'fit-1B-v3.2a-*MDT.md'))[-1],encoding='utf-8').read()
    old='155f86bbb7819f099029062a257728ff'
    hdr_only=f"# sheet\nBased on: snap, pointer, PASTE {want}\nNo PASTE line here.\n"
    cases=[('v3.2 d01c0b84 (no PASTE line)',v32,None,1),
           ('v3.2a vs live pointer',v32a,None,0),
           ('v3.2a copy, PASTE line set to 155f86bb',LINE.sub('PASTE for this sheet: '+old,v32a),None,1),
           ('v3.2a --expect-paste 155f86bb',v32a,'155f86bb',1),
           ('header names pointer md5, no PASTE line (false-CURRENT regression)',hdr_only,None,1)]
    bad=0
    for name,t,exp,want_rc in cases:
        rc,lab,why=judge(t,want,exp); ok=rc==want_rc; bad|=not ok
        print(f"{'PASS' if ok else 'FAIL'} {name}: exit {rc} {lab} ({why})")
    print('SELFTEST '+('PASS' if not bad else 'FAIL')); return 1 if bad else 0
args=sys.argv[1:]; expect=None
if '--expect-paste' in args:
    i=args.index('--expect-paste')
    if i+1>=len(args) or not re.fullmatch(r'[0-9a-f]{8,32}',args[i+1]): print('usage: --expect-paste needs an 8-32 hex md5'); sys.exit(2)
    expect=args[i+1]; del args[i:i+2]
try:
    ptr=cs.read(); probs=cs.verify(ptr)
except Exception as e: print(f"POINTER ERROR: {e}"); sys.exit(2)
if probs: print("POINTER ERROR: "+"; ".join(probs)); sys.exit(2)
want=ptr.get("paste_1b_md5","")
path=os.path.join(os.path.dirname(ptr["snap_dir"].rstrip("/")),ptr.get("paste_1b_path","").split()[0]) if ptr.get("paste_1b_path") else ""
if not want or not os.path.exists(path) or not same(md(path),want): print(f"POINTER ERROR: paste_1b {want[:8]} missing or md5 mismatch at {path}"); sys.exit(2)
print(f"fit_sheet_check {md(__file__)[:8]} pointer {ptr['pointer_md5'][:8]} snap {ptr['snap']} paste_1b {want[:8]}")
if args==['--selftest']: sys.exit(selftest(want))
if not args: print('usage: fit_sheet_check.py [--expect-paste MD5] SHEET.md [...] | --selftest'); sys.exit(2)
rcs=0
for s in args:
    rc,lab,why=judge(open(s,encoding='utf-8').read(),want,expect)
    print(f"{lab:7} {s} ({md(s)[:8]}): {why}"); rcs|=rc
sys.exit(1 if rcs else 0)
