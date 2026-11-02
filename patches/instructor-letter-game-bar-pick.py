#!/usr/bin/env python3
"""Instructor: OPTIONAL Maxwell pick, +13: Letter game is never the spoken target (like Count it, Big or small). Run after v2b. Dry-run unless --apply OUT."""
import hashlib, sys
t=open(sys.argv[1],encoding="utf-8").read(); print("base",hashlib.md5(t.encode()).hexdigest())
o,n="Count it, Big or small: never the spoken target","Count it, Big or small, Letter game: never the spoken target"
assert t.count(o)==1 and "Letter game (Phonics" in t; r=t.replace(o,n); print(f"chars {len(t)} -> {len(r)} ({len(r)-len(t):+d})")
if len(sys.argv)>3 and sys.argv[2]=="--apply": assert sys.argv[3]!=sys.argv[1]; open(sys.argv[3],"w",encoding="utf-8").write(r); print("wrote",sys.argv[3],hashlib.md5(r.encode()).hexdigest())
