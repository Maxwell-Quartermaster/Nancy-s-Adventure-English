#!/usr/bin/env python3
# Instructor sweep 2, v6-08. Spec 7.1 (PASTE :226): 8 color cards (cs-08..cs-15) produce "Where is the red?", "Where is the blue?" ...
# Natural English for a color is "Where is red?". Adds one exception inside the existing list. Thai stays "{word} อยู่ที่ไหน". Spec text only.
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
E = [('sw-15, sw-18, sw-19, sw-24), else', 'sw-15, sw-18, sw-19, sw-24; colors cs-08–cs-15 drop "the": \'Where is red?\'), else', 'paste')]
run(E, ['paste'])
