#!/usr/bin/env python3
# Instructor: exact text for two Maxwell picks so Chancellor can measure them (not estimates).
# Target: v32 PASTE 317e91ce (pointer f6dac2d0). Usage: SRC (--night | --b1 | --b1-pin) [...] [--apply OUT]
#  --night : Night title B (sheet night-title-line): night shows "Good evening!"; greetNight dropped.
#  --b1    : B1 B (sheet B1-reward-pacing): Bloodtide at level 12, Dragonbane at level 16 (data only).
#  --b1-pin: with --b1, keeps both blades at rank 4 (otherwise level unlock = rank 2, the sheet's side effect).
import sys, hashlib
SRC=sys.argv[1]; s=open(SRC,encoding="utf-8").read(); h=hashlib.md5(s.encode()).hexdigest()
BASES={"317e91ce86f073c961f8169183d2bbd3":"v32 PASTE"}
assert h in BASES, "base must be v32 317e91ce"; print("base",BASES[h],h)
P={"--night":[
 ("`uiText.greetMorning`, `greetAfternoon`, `greetEvening` or `greetNight`;","`uiText.greetMorning`, `greetAfternoon` or `greetEvening` (evening and night);"),
 (',"greetNight":{"en":"Good night!","th":"ราตรีสวัสดิ์!"}',"")],
 "--b1":[
 ('"cleaver-bloodtide","en":"Bloodtide Cleaver","unlock":{"type":"bossesWon","n":4}','"cleaver-bloodtide","en":"Bloodtide Cleaver","unlock":{"type":"level","n":12}'),
 ('"greatsword-dragonbane","en":"Dragonbane Greatsword","unlock":{"type":"bossesWon","n":5}','"greatsword-dragonbane","en":"Dragonbane Greatsword","unlock":{"type":"level","n":16}')],
 "--b1-pin":[
 ("bossesWon or secret 4","bossesWon, secret or a gift blade 4")]}
n0=len(s); picked=[k for k in P if k in sys.argv]; assert picked, "pick --night and/or --b1"
assert "--b1-pin" not in picked or "--b1" in picked
for k in picked:
    a0=len(s)
    for a,b in P[k]:
        assert s.count(a)==1,("anchor not unique",a); s=s.replace(a,b)
    print(f"  {k} {len(s)-a0:+d}")
print(f"chars {n0} -> {len(s)} ({len(s)-n0:+d}); bank {188200-len(s)}")
if "--apply" in sys.argv:
    o=sys.argv[sys.argv.index("--apply")+1]; open(o,"w",encoding="utf-8").write(s); print("wrote",o,hashlib.md5(s.encode()).hexdigest())
