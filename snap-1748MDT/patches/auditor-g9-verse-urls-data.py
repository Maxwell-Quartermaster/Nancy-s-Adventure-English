#!/usr/bin/env python3
"""G9 (offline): verse enUrl/thUrl (:338/:343) are never said to be data only; rendered as links they leave the standalone app and fail offline.
Auditor patch (Grok 5: Auditor), written against PASTE 3b4bddb3a08a1fb48080dd43ceea6d62.
NOT APPLIED (Maxwell t419u). Text-anchored, not line-anchored.
Default: dry run (reports matches and char delta). --out DIR writes patched copies to DIR; never writes in place.
Usage: python3 auditor-g9-verse-urls-data.py [--dir DIR] [--out OUTDIR]
"""
import sys,os,glob
EDITS=[('Each verse has `status: "VERIFIED"` and its `enUrl`/`thUrl`.', 'Each verse has `status: "VERIFIED"` and its `enUrl`/`thUrl` (data only, never links).')]
def main():
    a=sys.argv[1:]; d=a[a.index('--dir')+1] if '--dir' in a else '/workspace'
    out=a[a.index('--out')+1] if '--out' in a else None
    if out and os.path.abspath(out)==os.path.abspath(d): sys.exit('refusing to write in place')
    fs=[os.path.join(d,n) for n in ('nancys-adventure-english-v6-08-PASTE.md','nancys-adventure-english-FINAL-v6-08.md','nancys-adventure-english-v6-08.md') if os.path.exists(os.path.join(d,n))]
    if not fs: sys.exit('no v6-08 PASTE/FINAL/spec in '+d)
    rc=0
    for f in sorted(fs):
        s=open(f,encoding='utf-8').read(); t=s; tot=0
        for old,new in EDITS:
            n=t.count(old)
            if n!=1: print(os.path.basename(f),'anchor count',n,'for',old[:60]); rc=1; continue
            t=t.replace(old,new); tot+=len(new)-len(old)
        print(os.path.basename(f),'delta %+d chars'%tot,len(s),'->',len(t))
        if out:
            os.makedirs(out,exist_ok=True); open(os.path.join(out,os.path.basename(f)),'w',encoding='utf-8').write(t)
    sys.exit(rc)
if __name__=='__main__': main()
