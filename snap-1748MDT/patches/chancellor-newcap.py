#!/usr/bin/env python3
"""Chancellor v6-08 patch newcap. NOT APPLIED (Maxwell t419u). C1 (0 chars): the v5 cap of 3 never-seen cards was set for 10-card runs; a v6 run has 25 scene targets, so a zone shows only 3 new pictures per run and repeats the rest 2-3x. 8 keeps the same 3-in-10 share (7.5 of 25).
Base: PASTE 3b4bddb3a08a1fb48080dd43ceea6d62 (185,611); also anchors once in a077a328 (snap-1621MDT).
Usage: python3 chancellor-newcap.py [--out DIR] [file]   (dry run by default; never writes in place; idempotent)
"""
import hashlib, os, sys
EDITS = [
 [
  "at most 3 never-seen (`seen`) once the zone has 7 seen",
  "at most 8 never-seen (`seen`) once the zone has 7 seen"
 ],
 [
  "at most 3 never-seen cards once the zone has 7 seen",
  "at most 8 never-seen cards once the zone has 7 seen"
 ]
]
BASES = {'3b4bddb3a08a1fb48080dd43ceea6d62', 'a077a3282f31eb268131ecb97fb1a33d'}
a = sys.argv[1:]; out = None
if a[:1] == ['--out']: out, a = a[1], a[2:]
f = a[0] if a else '/workspace/v608build/snap-1604MDT/nancys-adventure-english-v6-08-PASTE.md'
t = open(f, encoding='utf-8').read(); md5 = hashlib.md5(t.encode()).hexdigest()
if all(t.count(n) == 1 and t.count(o) == 0 for o, n in EDITS if o not in n): print(f, 'already applied'); sys.exit(0)
if md5 not in BASES: print('warning: base md5', md5, 'is not a known v6-08 base; anchors checked anyway')
new = t
for o, n in EDITS:
    assert new.count(o) == 1, ('anchor count', o, new.count(o)); new = new.replace(o, n)
print('%s: %+d chars, %d -> %d, md5 %s' % (f, len(new) - len(t), len(t), len(new), hashlib.md5(new.encode()).hexdigest()))
if out:
    os.makedirs(out, exist_ok=True); p = os.path.join(out, os.path.basename(f))
    assert os.path.abspath(p) != os.path.abspath(f), 'refusing to write in place'
    open(p, 'w', encoding='utf-8').write(new); print('  wrote', p)
