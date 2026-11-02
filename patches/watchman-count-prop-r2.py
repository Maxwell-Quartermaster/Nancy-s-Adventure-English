#!/usr/bin/env python3
"""Watchman v6-08 re-walk (snap-1700MDT) patch count-prop-r2. NOT APPLIED. Delta +6 chars per file.
W2 r2: in "Scenery copies of the prop hide; it and Big or small are never the spoken target." the "it" can read as the prop; name Count it.
Base: snap-1700MDT PASTE 7374cc6fc31eee738a3bc82bfa6d7907 (187,074; FINAL 9bac7263, spec 27d4a1f1), or that after the earlier watchman-*-r2 patches
in REPORT order (scene-apart-r2, count-prop-r2, frontdesk-r2). Refuses any other md5 unless the edit is already there.
Note: this rewrites text that checks_v608.py pins in fixes_v608.WG; QM updates that pin to the new text when folding it in.
Usage: python3 watchman-count-prop-r2.py [--dir SRC] [--out OUTDIR]   dry run by default; --out writes patched copies; never writes in place; idempotent.
"""
import hashlib, os, sys
FILES = ['nancys-adventure-english-v6-08-PASTE.md', 'nancys-adventure-english-FINAL-v6-08.md', 'nancys-adventure-english-v6-08.md']
BASES = {'nancys-adventure-english-v6-08-PASTE.md': ['7374cc6fc31eee738a3bc82bfa6d7907', 'd11cc92866ca738857bcb706442e2d69'], 'nancys-adventure-english-FINAL-v6-08.md': ['9bac7263f13b84a3464efcf091723593', '5982ff4aca5353aeb8439c6a0f8af16d'], 'nancys-adventure-english-v6-08.md': ['27d4a1f1e2b3e407c5bc88af4ea64960', '9ab169b18073e16c8a480be75f4dbb1f']}
EDITS = [['Scenery copies of the prop hide; it and Big or small', 'Scenery copies of the prop hide; Count it and Big or small']]
a = sys.argv[1:]; src = a[a.index('--dir')+1] if '--dir' in a else '/workspace'
out = a[a.index('--out')+1] if '--out' in a else None
if out and os.path.abspath(out) == os.path.abspath(src): sys.exit('refusing to write in place')
rc = 0
for f in FILES:
    p = os.path.join(src, f)
    if not os.path.exists(p): print(f, 'missing, skipped'); continue
    t = open(p, encoding='utf-8').read(); m = hashlib.md5(t.encode()).hexdigest()
    if all(t.count(n) == 1 and t.count(o) == 0 for o, n in EDITS):
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
