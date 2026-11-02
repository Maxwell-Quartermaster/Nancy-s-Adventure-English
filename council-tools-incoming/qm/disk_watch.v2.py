#!/usr/bin/env python3
"""disk_watch.py - warn at 80% disk use on / (patch, not installed). Read-only: never deletes.

  disk_watch.py [--threshold 80] [--top 10] [--depth 2] [--root DIR ...]
Exit 0 = OK (below threshold), 1 = WARN, 2 = error (bad or unreadable mount, permission error,
a mount reporting 0 total bytes, or any other crash): prints one ERROR line, never a traceback.
v2 (2026-11-01): ERROR + exit 2 on errors, du read errors noted, percent shown without rounding up
to the threshold, own scratch dir runs/disk_watch/.
"""
import argparse, math, os, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SCRATCH = os.path.join(HERE, "runs", "disk_watch")  # this tool's own scratch; never /tmp, never another bot's folder
ROOTS = ["/workspace", "/tmp/qmtmp", "/dev/shm"]


def human(kb):
    v = float(kb)
    for u in ("K", "M", "G", "T"):
        if v < 1024 or u == "T":
            return f"{v:.1f}{u}"
        v /= 1024


def du_dirs(root, depth, timeout):
    """Return [(kb, path)] for dirs under root up to depth (root itself excluded)."""
    if not os.path.isdir(root):
        return [], f"{root}: not present"
    try:
        p = subprocess.run(["du", "-x", "-k", f"--max-depth={depth}", root],
                           capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return [], f"{root}: du timed out after {timeout}s"
    out = []
    err = None
    if p.returncode != 0:
        bad = [l for l in p.stderr.splitlines() if l.strip()]
        err = f"{root}: du could not read {len(bad)} path(s) (sizes may be low): " + (bad[0][:160] if bad else f"du exit {p.returncode}")
    for line in p.stdout.splitlines():
        try:
            kb, path = line.split("\t", 1)
        except ValueError:
            continue
        if os.path.normpath(path) != os.path.normpath(root):
            out.append((int(kb), path))
    return out, err


def leaves_only(rows):
    """Drop a dir if a listed child accounts for it (keeps the report specific, no double counting)."""
    paths = {p for _, p in rows}
    return [(kb, p) for kb, p in rows
            if not any(q != p and q.startswith(p.rstrip("/") + "/") for q in paths)] or rows


def shown(pct):
    """One decimal, rounded down, so 79.99% never prints as 80.0% next to 'below 80%'."""
    return f"{math.floor(pct * 10) / 10:.1f}"


def main(argv=None):
    try:
        return _main(argv)
    except SystemExit:
        raise
    except Exception as e:  # bad mount, permissions, anything else: never look like a WARN (exit 1)
        print(f"ERROR: disk_watch failed: {type(e).__name__}: {e}")
        return 2


def _main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--threshold", type=float, default=80.0)
    ap.add_argument("--top", type=int, default=10)
    ap.add_argument("--depth", type=int, default=2)
    ap.add_argument("--root", action="append", help="dirs to size (default: /workspace /tmp/qmtmp /dev/shm)")
    ap.add_argument("--mount", default="/")
    ap.add_argument("--timeout", type=int, default=600)
    ap.add_argument("--simulate-percent", type=float, help="self-test only: pretend / is at this percent")
    a = ap.parse_args(argv)

    os.makedirs(SCRATCH, exist_ok=True)
    try:
        u = shutil.disk_usage(a.mount)
    except OSError as e:
        print(f"ERROR: cannot read mount {a.mount}: {type(e).__name__}: {e}")
        return 2
    if not u.total:
        print(f"ERROR: mount {a.mount} reports 0 total bytes (not a real disk?)")
        return 2
    pct = 100.0 * u.used / u.total if u.total else 0.0
    if a.simulate_percent is not None:
        pct = a.simulate_percent
    gb = lambda b: b / 1024 ** 3
    sim = f" [SIMULATED {pct:g}%, real {100.0 * u.used / u.total:.1f}%]" if a.simulate_percent is not None else ""
    if pct < a.threshold:
        print(f"OK: {a.mount} at {shown(pct)}% ({gb(u.used):.0f}G used of {gb(u.total):.0f}G, {gb(u.free):.0f}G free), below {a.threshold:g}%{sim}")
        return 0

    rows, notes = [], []
    for r in (a.root or ROOTS):
        d, err = du_dirs(r, a.depth, a.timeout)
        rows += d
        if err:
            notes.append(err)
    top = sorted(leaves_only(rows), reverse=True)[: a.top]
    print(f"WARN: {a.mount} at {shown(pct)}% ({gb(u.used):.0f}G used of {gb(u.total):.0f}G, {gb(u.free):.0f}G free), at or above {a.threshold:g}%{sim}")
    print(f"Top {len(top)} dirs by size (depth {a.depth}, under {', '.join(a.root or ROOTS)}):")
    for i, (kb, p) in enumerate(top, 1):
        print(f"  {i:2d}. {human(kb):>8}  {p}")
    for n in notes:
        print(f"  note: {n}")
    print("Nothing was deleted. Suggest: ask Maxwell (1A/1B, ASKS-LEDGER row first) whether any of these can be archived or removed.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
