#!/usr/bin/env python3
import os, re, sys
from _selftest_lib import T, run, scratch
t = T("disk_watch selftest"); d = scratch("disk_watch")
sizes = {"big/a": 900, "big/b": 300, "mid": 400, "small": 20}
for i in range(12):
    sizes[f"many/d{i:02d}"] = 10 + i
for rel, kb in sizes.items():
    p = os.path.join(d, rel); os.makedirs(p, exist_ok=True)
    open(os.path.join(p, "blob"), "wb").write(os.urandom(kb * 1024))
files = sorted(os.path.join(r, f) for r, _, fs in os.walk(d) for f in fs)

rc, o = run("disk_watch.py", "--simulate-percent", "85", "--root", d)
t.ok(rc == 1 and o.startswith("WARN"), "85% -> WARN, exit 1", o)
listed = re.findall(r"^\s+\d+\.\s+\S+\s+(\S+)$", o, re.M)
t.ok(len(listed) == 10, "WARN lists exactly top 10 dirs", o)
t.ok(listed[0].endswith("big/a") and listed[1].endswith("mid"), "largest dirs first (big/a 900K, then mid 400K)", o)
t.ok("Nothing was deleted" in o and "ask Maxwell" in o, "WARN says nothing deleted and to ask Maxwell", o)
rc, o = run("disk_watch.py", "--simulate-percent", "80", "--root", d)
t.ok(rc == 1 and o.startswith("WARN"), "exactly 80% -> WARN (threshold is >=)", o)
rc, o = run("disk_watch.py", "--simulate-percent", "79.9", "--root", d)
t.ok(rc == 0 and o.startswith("OK") and len(o.strip().splitlines()) == 1, "79.9% -> one-line OK, exit 0", o)
rc, o = run("disk_watch.py", "--simulate-percent", "90", "--root", d, "--root", os.path.join(d, "no-such-dir"))
t.ok(rc == 1 and "not present" in o, "missing root (like /tmp/qmtmp today) reported, not fatal", o)
rc, o = run("disk_watch.py", "--simulate-percent", "90", "--root", d, "--top", "3")
t.ok(len(re.findall(r"^\s+\d+\.", o, re.M)) == 3, "--top 3 lists 3", o)
rc, o = run("disk_watch.py")
real = re.search(r"at ([\d.]+)%", o)
t.ok(real and ((float(real.group(1)) < 80) == (rc == 0)), f"real / check: exit {rc} agrees with live {real.group(1) if real else '?'}%", o)
after = sorted(os.path.join(r, f) for r, _, fs in os.walk(d) for f in fs)
t.ok(after == files, "no file deleted by any run")
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "disk_watch.py")).read()
t.ok(not re.search(r"\b(os\.remove|os\.unlink|rmtree|rmdir|\"rm\"|'rm')", src), "source has no delete calls")
print("real run: " + o.strip())
# --- v2: Auditor gate L1-0141 cases
rc, o = run("disk_watch.py", "--mount", "/no/such/mount")
t.ok(rc == 2 and o.startswith("ERROR") and "Traceback" not in o, "D-mount (gate): bad mount -> ERROR, exit 2, no traceback", o)
rc, o = run("disk_watch.py", "--mount", "/proc")
t.ok(rc == 2 and o.startswith("ERROR"), "mount with 0 total bytes (/proc) -> ERROR, exit 2 (not OK 0.0%)", o)
locked = os.path.join(d, "locked"); os.makedirs(os.path.join(locked, "inner"))
noperm = os.path.join(d, "noperm"); os.makedirs(noperm); os.chmod(noperm, 0)
try:
    rc, o = run("disk_watch.py", "--mount", noperm + "/x")
    t.ok(rc == 2 and o.startswith("ERROR") and "Traceback" not in o, "permission-denied mount path -> ERROR, exit 2", o)
    rc, o = run("disk_watch.py", "--simulate-percent", "85", "--root", d)
    t.ok(rc == 1 and "could not read" in o, "unreadable dir under a root -> still WARN exit 1, with a du note", o)
finally:
    os.chmod(noperm, 0o755)
rc, o = run("disk_watch.py", "--simulate-percent", "80", "--root", d)
t.ok(rc == 1 and o.startswith("WARN"), "v2 still: exactly 80% -> WARN, exit 1", o)
rc, o = run("disk_watch.py", "--simulate-percent", "79.9", "--root", d)
t.ok(rc == 0 and o.startswith("OK"), "v2 still: 79.9% -> OK, exit 0", o)
rc, o = run("disk_watch.py", "--simulate-percent", "79.99", "--root", d)
t.ok(rc == 0 and "at 79.9%" in o, "79.99% prints 79.9% (never '80.0% ... below 80%')", o)
here = os.path.dirname(os.path.abspath(__file__))
t.ok(os.path.isdir(os.path.join(here, "runs", "disk_watch")), "tool made its own scratch dir qm/runs/disk_watch/ (os.makedirs)")
src2 = open(os.path.join(here, "disk_watch.py")).read()
t.ok('os.path.join(HERE, "runs", "disk_watch")' in src2 and not re.search(r"\b(os\.remove|os\.unlink|rmtree|rmdir)", src2),
     "source: scratch under qm/runs/, still no delete calls")
print("scratch kept at " + d)
sys.exit(t.done())
