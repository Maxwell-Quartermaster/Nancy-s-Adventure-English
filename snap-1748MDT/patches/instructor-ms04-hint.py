#!/usr/bin/env python3
# Instructor sweep 2, v6-08. ms-04 hint.letters "C____-out i_ a_ e_____." shows "out" in full; every other word is masked. 0 chars.
# (ms-04 is fill:true / Example until Maxwell confirms, so Nancy does not see it yet.)
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
E = [('"C____-out i_ a_ e_____."', '"C____-o__ i_ a_ e_____."', 'both')]
run(E, ['paste', 'cards'])
