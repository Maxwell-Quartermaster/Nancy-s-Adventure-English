#!/usr/bin/env python3
"""Auditor gate L1-0207 new quote_check cases (a)-(c) + perf. Runs COPIES only; writes only results here. No deletes."""
import os, re, subprocess, sys, time, json
H = os.path.dirname(os.path.abspath(__file__)); G = os.path.dirname(H)
TOOLS = {"v3": os.path.join(G, "qm", "quote_check.py"), "v2": os.path.join(G, "qm", "quote_check.v2.py")}
D = os.path.join(G, "data"); PASTE = f"{D}/nancys-adventure-english-v6-08-1B-v32-PASTE.md"
REAL = ["--rulings", f"{D}/SETTLED-RULINGS.md", "--ledger", f"{D}/ASKS-LEDGER.c7461aa0.md", "--paste", PASTE]
SYN = ["--rulings", os.path.join(H, "SYN-RULINGS-v3.md"), "--ledger", f"{D}/ASKS-LEDGER.c7461aa0.md", "--paste", PASTE]
def run(tool, base, post, seed="0"):
    env = dict(os.environ, PYTHONHASHSEED=seed, PYTHONDONTWRITEBYTECODE="1")
    p = subprocess.run([sys.executable, TOOLS[tool], *base, post], capture_output=True, text=True, env=env)
    o = (p.stdout + p.stderr).strip()
    v = re.findall(r"^(?:ok  |FLAG) line \d+: ([A-Z-]+):", o, re.M)
    return p.returncode, v, o
C = [  # id, base, post, expected verdict, required
 ("A1-ledger-same-text-later-whole", SYN, '**Maxwell (t910u, QM chat):** "Soft blue tiles"', "VERBATIM"),
 ("A2-ledger-first-row-longer-later-row-whole", SYN, '**Maxwell (t911u, QM chat):** "Make the gate glow gold"', "VERBATIM"),
 ("A3-ledger-one-row-two-quotes-whole-second", SYN, '**Maxwell (t912u, QM chat):** "Keep the shop small"', "VERBATIM"),
 ("A4-ledger-altered", SYN, '**Maxwell (t911u, QM chat):** "Make the gate glow green"', "ALTERED"),
 ("A5-ledger-cut", SYN, '**Maxwell (t910u, QM chat):** "Players love the soft blue"', "ALTERED"),
 ("A6-ledger-cut-no-tnum", SYN, '**Maxwell:** "Make the gate glow"', "FLAG"),
 ("A7-ledger-whole-no-tnum", SYN, '**Maxwell:** "Make the gate glow gold"', "VERBATIM"),
 ("B1-ascii-inside-word-start", REAL, '**Auditor:** the PASTE label is "olors and Shapes"', "SPEC-CUT"),
 ("B2-ascii-inside-word-end", REAL, '**Auditor:** the PASTE label is "The Gentle Guardia"', "SPEC-CUT"),
 ("B3-T6c-thai-inside-longer-word", REAL, '**Instructor:** the PASTE says "ขนมปังบาร์"', "SPEC-CUT"),
 ("B4-thai-mid-verse-run", REAL, '**Instructor:** the PASTE says "ดาวิดก็พูดกับคนฟีลิสเตีย"', "SPEC-CUT"),
 ("B5-T6b-thai-altered", REAL, '**Instructor:** the PASTE says "ขนมปัน"', "SPEC-ALTERED"),
 ("B6-T6-thai-whole", REAL, '**Instructor:** the PASTE says "ขนมปัง"', "SPEC-VERBATIM"),
 ("C1-multi-line-whole-later-Baby", REAL, '**Auditor:** the PASTE label is "Baby and Hospital"', "SPEC-VERBATIM"),
 ("C2-multi-line-whole-later-Gentle", REAL, '**Auditor:** the PASTE name is "The Gentle Guardian"', "SPEC-VERBATIM"),
 ("C3-multi-line-whole-later-Gold", REAL, '**Auditor:** the PASTE says "Gold card border"', "SPEC-VERBATIM"),
 ("C4-multi-line-whole-later-Big", REAL, '**Auditor:** the PASTE says "Big or small?"', "SPEC-VERBATIM"),
]
OKV = {"VERBATIM", "SPEC-VERBATIM"}
res = []
for i, base, post, exp in C:
    row = dict(id=i, expect=exp)
    for tool in ("v3", "v2"):
        seen = set(); rcs = set(); out = ""
        for seed in ([str(s) for s in range(12)] if i.startswith("A") else ["0"]):
            rc, v, o = run(tool, base, post, seed); seen.add(tuple(v)); rcs.add(rc); out = out or o
        row[tool] = dict(verdicts=sorted(seen), rcs=sorted(rcs), out=out)
    v3 = row["v3"]; vs = {x for t in v3["verdicts"] for x in t}
    if exp == "FLAG": ok = v3["rcs"] == [1] and not (vs & OKV)
    elif exp in OKV: ok = v3["rcs"] == [0] and len(v3["verdicts"]) == 1 and vs == {exp}
    else: ok = v3["rcs"] == [1] and len(v3["verdicts"]) == 1 and vs == {exp}
    row["ok"] = ok; res.append(row)
    print(f"{'PASS' if ok else 'FAIL'} {i}: expect {exp}; v3 {v3['verdicts']} exit {v3['rcs']}; (v2 {row['v2']['verdicts']} exit {row['v2']['rcs']})")
    if not ok: print("     " + v3["out"].replace("\n", "\n     ")[:600])
print(f"TOTAL new {sum(r['ok'] for r in res)}/{len(res)}")
# perf: whole-PASTE scan
def timed(post, base=REAL):
    t = time.time(); rc, v, o = run("v3", base, post); return time.time() - t, rc, v
lines = [l for l in open(PASTE, encoding="utf-8").read().splitlines()]
vals = sorted(set(re.findall(r'"(?:en|th)"\s*:\s*"([^"]{3,80})"', "\n".join(lines))))
big = "\n".join(f'**Auditor:** the PASTE says "{v}"' for v in vals)
print("PERF single T6:", "%.2fs" % timed('**Instructor:** the PASTE says "ขนมปัง"')[0])
print("PERF single Thai not-found (thai_near full scan):", "%.2fs" % timed('**Instructor:** the PASTE says "กขคงจฉชซฌญฎฏฐ"')[0])
t, rc, v = timed(big); print(f"PERF big post {len(vals)} spec-quote lines (all PASTE en/th values): {t:.2f}s, exit {rc}, {len(v)} checked, flagged {sum(x not in OKV for x in v)}")
open(os.path.join(H, "big-post.md"), "w", encoding="utf-8").write(big)
json.dump(res, open(os.path.join(H, "results.json"), "w"), ensure_ascii=False, indent=1)
