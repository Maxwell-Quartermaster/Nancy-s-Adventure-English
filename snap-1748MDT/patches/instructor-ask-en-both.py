#!/usr/bin/env python3
# Instructor sweep 2, v6-08. Spec 7.1 (PASTE :226): "({word} = `en`)" does not say the Thai line uses `en` too. The v6-08 scene renders
# A (ship) and F (croissant) filled the Thai {word} with `th` ("เรือ อยู่ที่ไหน", "ขนมปังเนยรูปพระจันทร์เสี้ยว อยู่ที่ไหน"), which gives Nancy
# the answer. Build could do the same. Spec text only.
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
E = [('({word} = `en`)', '({word} = `en` in both lines, never `th`)', 'paste')]
run(E, ['paste'])
