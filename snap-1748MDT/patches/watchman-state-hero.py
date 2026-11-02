#!/usr/bin/env python3
# Watchman playtest v6-08 (Oct 31, 2026): `state.hero` (6.1 / section 3 Hero, "persists") is not in the one state record list (section 10),
# so restore's "all keys" check and the backup never carry the chosen hero. Adds `hero, ` before `giftGems`. +6 chars.
# Usage: python3 watchman-state-hero.py <path-to-PASTE-copy>   (refuses on md5 mismatch; idempotent)
import sys, hashlib
BASE = '3b4bddb3a08a1fb48080dd43ceea6d62'   # working PASTE at 4:2x PM MDT (185,611 chars)
OLD = 'pips, streak, giftGems, settings{slowMode, restWeeks}}'
NEW = 'pips, streak, hero, giftGems, settings{slowMode, restWeeks}}'
p = sys.argv[1]; b = open(p, 'rb').read(); t = b.decode('utf-8')
if NEW in t and OLD not in t: print('already applied; no change', hashlib.md5(b).hexdigest()); sys.exit(0)
md5 = hashlib.md5(b).hexdigest()
if md5 != BASE: sys.exit(f'REFUSED: md5 {md5} != expected base {BASE}')
assert t.count(OLD) == 1, 'anchor not found exactly once'
t2 = t.replace(OLD, NEW); open(p, 'w', encoding='utf-8').write(t2)
print('applied', len(t), '->', len(t2), f'({len(t2)-len(t):+d})', hashlib.md5(t2.encode()).hexdigest())
