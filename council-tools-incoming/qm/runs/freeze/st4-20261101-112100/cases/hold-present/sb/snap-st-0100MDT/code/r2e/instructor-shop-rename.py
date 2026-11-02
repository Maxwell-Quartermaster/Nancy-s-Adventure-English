#!/usr/bin/env python3
"""Instructor: rename Golden Pantry -> Shop (t487u). Player-facing words only; code keys
(uiText.pantry, pantry.items, pantryOwned, pantry{earn}) stay. Dry-run unless --apply OUT."""
import hashlib, re, sys
SRC = sys.argv[1]; BASES = {"106a066103da9713220a5e7d6c4285cf": "1A", "2eebff944f7c30ac2e13fdc8e888d398": "1B"}
t = open(SRC, encoding="utf-8").read()
h = hashlib.md5(t.encode()).hexdigest(); assert h in BASES, "PASTE is not 1A 106a0661 or 1B 2eebff94"; print("base", BASES[h], h)
old = '"pantry":{"en":"Golden Pantry","th":"ตู้กับข้าวทองคำ"}'
assert t.count(old) == 1; n = t.replace(old, '"pantry":{"en":"Shop","th":"ร้านดาวทอง"}')
n, a = re.subn(r"Golden Pantry", "Shop", n)
n, b = re.subn(r"\bPantry\b", "Shop", n)
left = re.findall(r"\bPantry\b|ตู้กับข้าว", n)
print(f"uiText 1, 'Golden Pantry' {a}, 'Pantry' {b}, left {len(left)}; chars {len(t)} -> {len(n)} ({len(n)-len(t):+d})")
if len(sys.argv) > 3 and sys.argv[2] == "--apply":
    open(sys.argv[3], "w", encoding="utf-8").write(n); print("wrote", sys.argv[3], hashlib.md5(n.encode()).hexdigest())
