#!/usr/bin/env python3
"""Auditor v6-08 pre-sweep, patch U1 (0 chars; renamed from P1 to avoid clashing with QM's P1). NOT APPLIED (Maxwell t419u).

Bug: section 18 (Thai Review Queue) says "all 91 `uiText` entries", but the cards
JSON has 97 `uiText` entries in 3b4bddb3 (meta.uiTextEntries 97; section 16 says `uiText` (97);
every entry is NEEDS NANCY by meta.thStatusDefault). Stale since v6-06 (92 then).
Fix: write the live count, read from the same file's cards JSON (PASTE) or the
companion cards file (FINAL/spec). Length-neutral while the count has 2 digits.

Usage (dry run, prints the change, writes nothing):
  python3 auditor-u1-uitext-count.py [file ...]        default: the v6-08 PASTE
Write patched copies elsewhere (never in place):
  python3 auditor-u1-uitext-count.py --out DIR [file ...]
Gate base: PASTE 3b4bddb3a08a1fb48080dd43ceea6d62 (185,611); also dry-run OK on b6ee2183
(anchor-based; asserts exactly one hit and equal length).
"""
import json, os, re, sys
W = os.environ.get('NAE_W', '/workspace/')
args = sys.argv[1:]; out = None
if args[:1] == ['--out']: out, args = args[1], args[2:]
files = args or [W + 'nancys-adventure-english-v6-08-PASTE.md']
OLD = re.compile(r'all (\d+) `uiText` entries')
for f in files:
    t = open(f, encoding='utf-8').read()
    if '\n```json\n' in t:
        n = len(json.loads(t[t.index('\n```json\n') + 9:t.rindex('\n```')])['uiText'])
    else:
        n = len(json.load(open(os.path.join(os.path.dirname(f) or '.', 'nancys-adventure-english-v6-08-cards.json'), encoding='utf-8'))['uiText'])
    m = OLD.findall(t)
    assert len(m) == 1, (f, 'anchor count', len(m))
    new = OLD.sub('all %d `uiText` entries' % n, t)
    assert len(new) == len(t), (f, 'not length-neutral', len(new) - len(t))
    print('%s: "all %s `uiText` entries" -> "all %d `uiText` entries" (%+d chars)%s' % (f, m[0], n, len(new) - len(t), '' if m[0] != str(n) else ' [already correct]'))
    if out:
        os.makedirs(out, exist_ok=True); p = os.path.join(out, os.path.basename(f))
        assert os.path.abspath(p) != os.path.abspath(f), 'refusing to write in place'
        open(p, 'w', encoding='utf-8').write(new); print('  wrote', p)
