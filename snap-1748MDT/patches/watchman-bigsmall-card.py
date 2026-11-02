#!/usr/bin/env python3
"""Watchman v6-08 glitch hunt patch bigsmall-card. NOT APPLIED (Maxwell t419u). Delta +50 chars per file.
W3: Big or small (7.1 :230) holds a sizeSort picture from another zone (fd-25, nm-04, ms-21 ...); nothing says which card its reveal, XP and ledger belong to.
Base: PASTE 476f0b659cb1b940574096915affd203 (186,680 chars; already holds auditor-g1..g9, instructor-*, chancellor-* as QM folded them),
or that PASTE after the earlier watchman-* glitch patches in REPORT order. Refuses any other md5 unless the edit is already there.
Usage: python3 watchman-bigsmall-card.py [--dir SRC] [--out OUTDIR]   dry run by default; --out writes patched copies; never writes in place; idempotent.
"""
import hashlib, os, sys
FILES = ['nancys-adventure-english-v6-08-PASTE.md', 'nancys-adventure-english-FINAL-v6-08.md', 'nancys-adventure-english-v6-08.md']
BASES = {'nancys-adventure-english-v6-08-PASTE.md': ['476f0b659cb1b940574096915affd203', '61c3dcd108d86af681c20f183930a2cf'], 'nancys-adventure-english-FINAL-v6-08.md': ['164af2f78de4e45c0ed9e511f6ee5127', 'bee7f67b403d5a32e1c28c162971ca3d'], 'nancys-adventure-english-v6-08.md': ['15a3bad00c39795d2995f359df4baf74', 'bbb97bada1c53c3f4a503b529673c574']}
EDITS = [['it awards and resumes as a scene card (ledger `card:<runId>:<index>`).', 'it awards, reveals and resumes as the scene card `cs-23` or `cs-24`, the word that fits (ledger `card:<runId>:<index>`).']]
a = sys.argv[1:]; src = a[a.index('--dir')+1] if '--dir' in a else '/workspace'
out = a[a.index('--out')+1] if '--out' in a else None
if out and os.path.abspath(out) == os.path.abspath(src): sys.exit('refusing to write in place')
rc = 0
for f in FILES:
    p = os.path.join(src, f)
    if not os.path.exists(p): print(f, 'missing, skipped'); continue
    t = open(p, encoding='utf-8').read(); m = hashlib.md5(t.encode()).hexdigest()
    if all(t.count(n) == 1 and (o in n or t.count(o) == 0) for o, n in EDITS):
        print(f, 'already applied, unchanged'); new = t
    elif m not in BASES[f]:
        print(f, 'REFUSED: md5', m, 'is not a known base', BASES[f]); rc = 2; continue
    else:
        new = t
        for o, n in EDITS:
            if new.count(o) != 1: print(f, 'REFUSED: anchor count', new.count(o), o[:60]); rc = 2; break
            new = new.replace(o, n)
        else:
            print('%s: %+d chars, %d -> %d, md5 %s -> %s%s' % (f, len(new)-len(t), len(t), len(new), m, hashlib.md5(new.encode()).hexdigest(), '' if out else '  [dry run]'))
        if rc: continue
    if out:
        os.makedirs(out, exist_ok=True); open(os.path.join(out, f), 'w', encoding='utf-8').write(new)
sys.exit(rc)
