#!/usr/bin/env python3
"""Instructor (for QM; Maxwell t64u, t495u, t496u): boss nameplate + red boss bar.
Part A red bar (t495u): the guardian's bar drains red; carve-outs at rule 9 (:32) and the 'No red fills' check.
Part B nameplate on every boss: 0 chars. :227 already gives EVERY guardian run the zone chip with `boss.name`
  (all 5 guardians use it); no text added.
Part C Echo Knight (t496u): same plate, smaller; no bar (bar stays 'the guardian's'; :175 'not a zone guardian').
Boss health only; no player bar or lives (:48 unchanged). No Thai or verses touched.
Base = 1B+Shop 24934ef1 or 1B+Shop+L v2 d06c5344 or v2b c3443fb9. Dry-run unless --apply OUT."""
import hashlib, sys
SRC = sys.argv[1]; BASES = {"24934ef11a870ebe381e9923dc31bfdd": "1B+Shop", "d06c53444a0ff041b6ed4c89fb0aabe2": "1B+Shop+L v2", "c3443fb9dca78a4a96a5b8c5d16cd061": "1B+Shop+L v2b", "d9125bbf763023584dc6b8eafb2656c0": "chain v2b+ramp+flow+zone-mix (155f86bb route)", "1bb1ff6d164df4c973802229828dcbbe": "staged flow-mix"}
t = open(SRC, encoding="utf-8").read(); h = hashlib.md5(t.encode()).hexdigest()
assert "--any-base" not in sys.argv, "--any-base retired (Auditor 7bc298f6): md5 allowlist only"
if True: assert h in BASES, "base is not 1B+Shop 24934ef1 or L v2 d06c5344 / v2b c3443fb9"; print("base", BASES[h], h)
EDITS = [("A", "9. **Nothing red or alarming** anywhere.", "9. **Nothing red or alarming** anywhere but boss bars (t495u)."),
         ("A", "drops the guardian's bar by", "drops the guardian's red bar by"),
         ("A", "No red fills.", "No red fills but boss bars."),
         ("C", "The Echo Knight (`uiText.echoKnight`) shows", "The Echo Knight (`uiText.echoKnight`, small guardian chip) shows")]
n = t; part = {"A": 0, "B": 0, "C": 0}
for p, old, new in EDITS:
    assert n.count(old) == 1, ("anchor count", old, n.count(old)); n = n.replace(old, new)
    part[p] += len(new) - len(old); print(f"  {p} {len(new)-len(old):+d}  {old!r}")
print("parts: A red bar %+d, B nameplate all bosses %+d, C Echo Knight small plate %+d" % (part["A"], part["B"], part["C"]))
print(f"chars {len(t)} -> {len(n)} ({len(n)-len(t):+d}); bank {188200-len(n)}")
if "--apply" in sys.argv:
    OUT = sys.argv[sys.argv.index("--apply") + 1]; assert OUT != SRC; open(OUT, "w", encoding="utf-8").write(n); print("wrote", OUT, hashlib.md5(n.encode()).hexdigest())
