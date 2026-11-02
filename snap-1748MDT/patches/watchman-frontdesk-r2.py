#!/usr/bin/env python3
"""Watchman v6-08 re-walk (snap-1700MDT) patch frontdesk-r2. NOT APPLIED. Delta +8 chars per file.
W4 r2: "(the run deals them their own scenes)" lets a front desk scene hold fewer than 5 objects, or be topped up with home-room cards in the front desk set; say it holds only them and fills with repeats (7.1 repeat rule; Maxwell Says has 18 pic cards, 6 of them front desk).
Base: snap-1700MDT PASTE 7374cc6fc31eee738a3bc82bfa6d7907 (187,074; FINAL 9bac7263, spec 27d4a1f1), or that after the earlier watchman-*-r2 patches
in REPORT order (scene-apart-r2, count-prop-r2, frontdesk-r2). Refuses any other md5 unless the edit is already there.
Note: this rewrites text that checks_v608.py pins in fixes_v608.WG; QM updates that pin to the new text when folding it in.
Usage: python3 watchman-frontdesk-r2.py [--dir SRC] [--out OUTDIR]   dry run by default; --out writes patched copies; never writes in place; idempotent.
"""
import hashlib, os, sys
FILES = ['nancys-adventure-english-v6-08-PASTE.md', 'nancys-adventure-english-FINAL-v6-08.md', 'nancys-adventure-english-v6-08.md']
BASES = {'nancys-adventure-english-v6-08-PASTE.md': ['7374cc6fc31eee738a3bc82bfa6d7907', 'd11cc92866ca738857bcb706442e2d69', 'df771383c922955d8c9c869c93c31b3b'], 'nancys-adventure-english-FINAL-v6-08.md': ['9bac7263f13b84a3464efcf091723593', '5982ff4aca5353aeb8439c6a0f8af16d', '0f1335aa1754c703329099141de642f8'], 'nancys-adventure-english-v6-08.md': ['27d4a1f1e2b3e407c5bc88af4ea64960', '9ab169b18073e16c8a480be75f4dbb1f', 'a7f87f4da97eb27e2336d5a3d1ee5a60']}
EDITS = [['play in a hotel front desk (the run deals them their own scenes):', 'play in a hotel front desk (only them in that scene, repeats filling it):']]
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
