#!/usr/bin/env python3
# Instructor sweep 2 (Oct 31 2026 MT), v6-08. Thai, cards JSON (embedded in PASTE line 426 and cards.json). NEEDS NANCY.
# 1) cs-07 th "พระเจ้าทรงสร้างสีสันต่างๆค่ะ": missing space after ๆ (every other ๆ in the file has one: bh-25 "ช้าๆ ค่ะ", fd-26). +1
# 2) sw-11 "It is mine." th "นี่ของฉัน": Nancy's line has no particle; its pair sw-12 "นี่ของคุณค่ะ" has ค่ะ. +3
# Usage: python3 instructor-thai-cs07-sw11.py [--apply] [--paste P] [--cards C]   (dry run by default; idempotent)
import sys, os, hashlib
W = os.environ.get('NAE_W', '/workspace/')
PASTE = W + 'nancys-adventure-english-v6-08-PASTE.md'
CARDS = W + 'nancys-adventure-english-v6-08-cards.json'
def run(edits, targets):
    """edits: list of (OLD, NEW, which) with which in {'paste','cards','both'}.
    Default = dry run (prints, writes nothing). --apply writes in place. Paths may be overridden: --paste P --cards C."""
    a = sys.argv[1:]; apply = '--apply' in a
    paths = {'paste': PASTE, 'cards': CARDS}
    for k in ('paste', 'cards'):
        if '--' + k in a: paths[k] = a[a.index('--' + k) + 1]
    for key in targets:
        p = paths[key]; t = open(p, encoding='utf-8').read(); t0 = t
        for old, new, which in edits:
            if which not in (key, 'both'): continue
            if t.count(new) == 1:
                print(f'  {os.path.basename(p)}: already applied: {new[:60]!r}'); continue
            assert t.count(old) == 1, (p, 'expected old text exactly once', old, t.count(old))
            t = t.replace(old, new)
        d = len(t) - len(t0)
        print(f'{os.path.basename(p)}: {len(t0)} -> {len(t)} chars ({d:+d}); md5 {hashlib.md5(t0.encode()).hexdigest()} -> {hashlib.md5(t.encode()).hexdigest()}{"" if apply else "  [dry run, nothing written]"}')
        if apply and t != t0: open(p, 'w', encoding='utf-8').write(t)
E = [('"th":"พระเจ้าทรงสร้างสีสันต่างๆค่ะ"', '"th":"พระเจ้าทรงสร้างสีสันต่างๆ ค่ะ"', 'both'),
     ('"en":"It is mine.","th":"นี่ของฉัน"', '"en":"It is mine.","th":"นี่ของฉันค่ะ"', 'both')]
run(E, ['paste', 'cards'])
