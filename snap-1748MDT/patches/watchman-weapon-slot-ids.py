#!/usr/bin/env python3
# Watchman playtest v6-08 (Oct 31, 2026): 7 of the 18 weapons are unnamed shop slots ("tierNames[t] + type name", 11.1 Shop rows) with no id,
# yet buying records `buy:<id>`, gift rings count `owned`, and reconcile (11.3) drops any equipped id not owned. Gives each unnamed slot a fixed id.
# Usage: python3 watchman-weapon-slot-ids.py <path-to-PASTE-copy>   (refuses on md5 mismatch; idempotent; can run after watchman-state-hero.py)
import sys, hashlib

OLD = "else `tierNames[t]` + type name with the type's `weaponParts` art."
NEW = "else `tierNames[t]` + type name with the type's `weaponParts` art, id `<tierName>-<type>` lower case (`star-axe1`), kept in `owned`."
p = sys.argv[1]; b = open(p, 'rb').read(); t = b.decode('utf-8')
if NEW in t: print('already applied; no change', hashlib.md5(b).hexdigest()); sys.exit(0)
md5 = hashlib.md5(b).hexdigest()
ok = md5 == '3b4bddb3a08a1fb48080dd43ceea6d62' or ('pips, streak, hero, giftGems' in t and hashlib.md5(t.replace('pips, streak, hero, giftGems', 'pips, streak, giftGems').encode()).hexdigest() == '3b4bddb3a08a1fb48080dd43ceea6d62')
if not ok: sys.exit(f'REFUSED: md5 {md5} is not the expected base 3b4bddb3 (or base + watchman-state-hero)')
assert t.count(OLD) == 1, 'anchor not found exactly once'
t2 = t.replace(OLD, NEW); open(p, 'w', encoding='utf-8').write(t2)
print('applied', len(t), '->', len(t2), f'({len(t2)-len(t):+d})', hashlib.md5(t2.encode()).hexdigest())
