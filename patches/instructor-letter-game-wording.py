#!/usr/bin/env python3
# Instructor: letter-game wording fixes from Auditor gate 7bc298f6. Target: chain PASTE 155f86bb (snap-r2h-0021MDT).
# 1) repeats: plates include repeated letters (BOOK needs two O plates)  2) reward lands on the full word, not each letter
import sys, hashlib
SRC=sys.argv[1]; s=open(SRC,encoding="utf-8").read(); h=hashlib.md5(s.encode()).hexdigest()
BASES={"155f86bbb7819f099029062a257728ff":"r2h chain (ground)"}
assert h in BASES, "base must be chain 155f86bb"; print("base",BASES[h],h)
R=[("6 letter plates (its letters plus decoys)","6 letter plates (its letters, repeats too, plus decoys)"),
   ("`uiText.spellIt`. Right = that card's usual reward;","`uiText.spellIt`. The full word = that card's usual reward and reveal;")]
n0=len(s)
for a,b in R:
    assert s.count(a)==1, ("anchor not unique",a); s=s.replace(a,b); print(f"  {len(b)-len(a):+d}  {a!r}")
print(f"chars {n0} -> {len(s)} ({len(s)-n0:+d}); bank {188200-len(s)}")
if "--apply" in sys.argv:
    o=sys.argv[sys.argv.index("--apply")+1]; open(o,"w",encoding="utf-8").write(s); print("wrote",o,hashlib.md5(s.encode()).hexdigest())
