#!/usr/bin/env python3
import hashlib, os, sys
from _selftest_lib import T, run, scratch
t = T("base_check selftest"); d = scratch("base_check")
SNAPF = "/workspace/v608build/CURRENT-SNAP.txt"
raw = open(SNAPF, "rb").read(); ptr = hashlib.md5(raw).hexdigest()
kv = dict(l.split("=", 1) for l in raw.decode().splitlines() if "=" in l)
snap, paste = kv["snap"].strip(), kv["paste_1b_md5"].strip()
good = f"Based on: {snap}, pointer {ptr[:8]}, PASTE {paste[:8]}."
cases = [
    ("live base line -> MATCH", f"**QM:** hi\n**QM:** {good} Ready to paste: none yet.", 0, "MATCH"),
    ("full 32-char pointer -> MATCH", f"Based on: {snap}, pointer {ptr}, PASTE {paste}", 0, "MATCH"),
    ("base + stage MANIFEST + scene-fill extras -> MATCH", f"**Watchman:** Based on: {snap}, pointer {ptr[:8]}, PASTE {paste[:8]}, scene-fill 6848a5e0, ground_check f46a2d29. Ready to paste: none yet.", 0, "MATCH"),
    ("REAL SLIP: snap-r2e-2313MDT -> STALE", f"**Auditor:** Based on: snap-r2e-2313MDT, pointer {ptr[:8]}, PASTE {paste[:8]}.", 1, "STALE"),
    ("old snap AND old pointer/PASTE -> STALE", "Based on: snap-r2e-2313MDT, pointer 0badf00d, PASTE 155f86bb.", 1, "STALE"),
    ("stale pointer only -> STALE", f"Based on: {snap}, pointer deadbeef, PASTE {paste[:8]}", 1, "STALE"),
    ("pre-v3.2 PASTE 155f86bb -> STALE", f"Based on: {snap}, pointer {ptr[:8]}, PASTE 155f86bb", 1, "STALE"),
    ("live v5-37 md5 used as PASTE -> STALE", f"Based on: {snap}, pointer {ptr[:8]}, PASTE acc534a5", 1, "STALE"),
    ("pointer field missing -> STALE", f"Based on: {snap}, PASTE {paste[:8]}", 1, "pointer missing"),
    ("no base line -> MISSING", "**Chancellor:** done.\nReady to paste: none yet.", 1, "MISSING"),
    ("two base lines, second stale -> exit 1", f"{good}\nBased on: snap-r2g-2326MDT, pointer {ptr[:8]}, PASTE {paste[:8]}", 1, "[base line 2] STALE"),
    ("STALE names what is live", "Based on: snap-r2e-2313MDT, pointer 0badf00d, PASTE 155f86bb.", 1, f"Live: {snap}, pointer {ptr[:8]}, PASTE {paste[:8]}"),
    ("backticked md5s -> MATCH", f"Based on: {snap}, pointer `{ptr[:8]}`, PASTE `{paste[:8]}`", 0, "MATCH"),
]
for label, text, want_rc, want in cases:
    rc, o = run("base_check.py", text)
    t.ok(rc == want_rc and want in o, label, o)
p = os.path.join(d, "post.md"); open(p, "w").write(f"**QM:** x\n{good}\n")
rc, o = run("base_check.py", "--file", p)
t.ok(rc == 0 and "MATCH" in o, "--file works", o)
fake = os.path.join(d, "SNAP.txt"); open(fake, "w").write("snap=snap-r2e-2313MDT\npaste_1b_md5=155f86bb000000000000000000000000\n")
rc, o = run("base_check.py", "--snap-file", fake, good)
t.ok(rc == 1 and "STALE" in o, "--snap-file override: current post vs older snap file -> STALE", o)
print("scratch kept at " + d)
sys.exit(t.done())
