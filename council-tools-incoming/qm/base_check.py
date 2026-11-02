#!/usr/bin/env python3
"""base_check.py - check a council post's 'Based on:' line against CURRENT-SNAP.txt (patch, not installed).

  base_check.py "<post text>"      or      base_check.py --file post.md
Output per base line: MATCH, STALE (with what is live) or MISSING (no base line).
Exit 0 = all MATCH, 1 = STALE or MISSING, 2 = error.
"""
import argparse, hashlib, re, sys

DEFAULT_SNAP = "/workspace/v608build/CURRENT-SNAP.txt"
BASE_RE = re.compile(r"Based on:\s*(.*)", re.I)
SNAP_RE = re.compile(r"\b(snap-[A-Za-z0-9-]+?)(?=[,;\s.]|$)")
PTR_RE = re.compile(r"\bpointer\s+`?([0-9a-fA-F]{6,32})")
PASTE_RE = re.compile(r"\bPASTE\s+`?([0-9a-fA-F]{6,32})")


def live(path):
    raw = open(path, "rb").read()
    kv = {}
    for line in raw.decode("utf-8", "replace").splitlines():
        if "=" in line:
            k, v = line.split("=", 1)
            kv.setdefault(k.strip(), v.strip())
    return dict(snap=kv.get("snap", ""), pointer=hashlib.md5(raw).hexdigest(),
                paste=kv.get("paste_1b_md5", ""))


def check_line(text, lv):
    # stop at the Ready-to-paste sentence if it shares the line
    text = re.split(r"Ready to paste", text, flags=re.I)[0]
    s, p, q = SNAP_RE.search(text), PTR_RE.search(text), PASTE_RE.search(text)
    got = dict(snap=s.group(1) if s else None, pointer=p.group(1).lower() if p else None,
               paste=q.group(1).lower() if q else None)
    probs = []
    if got["snap"] is None: probs.append("snap missing")
    elif got["snap"] != lv["snap"]: probs.append(f"snap {got['snap']} != live {lv['snap']}")
    if got["pointer"] is None: probs.append("pointer missing")
    elif not lv["pointer"].startswith(got["pointer"]): probs.append(f"pointer {got['pointer']} != live {lv['pointer'][:8]}")
    if got["paste"] is None: probs.append("PASTE missing")
    elif not lv["paste"].startswith(got["paste"]): probs.append(f"PASTE {got['paste']} != live {lv['paste'][:8]}")
    return got, probs


def run(post, snap_file):
    lv = live(snap_file)
    livestr = f"{lv['snap']}, pointer {lv['pointer'][:8]}, PASTE {lv['paste'][:8]}"
    lines = [m.group(1) for m in (BASE_RE.search(l) for l in post.splitlines()) if m]
    if not lines:
        return 1, [f"MISSING: no 'Based on:' line. Live base: Based on: {livestr}"]
    out, rc = [], 0
    for i, t in enumerate(lines, 1):
        got, probs = check_line(t, lv)
        tag = f"[base line {i}] " if len(lines) > 1 else ""
        if probs:
            rc = 1
            out.append(f"{tag}STALE: {'; '.join(probs)}. Live: {livestr}")
        else:
            out.append(f"{tag}MATCH: {got['snap']}, pointer {got['pointer']}, PASTE {got['paste']}")
    return rc, out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("text", nargs="?")
    ap.add_argument("--file")
    ap.add_argument("--snap-file", default=DEFAULT_SNAP)
    a = ap.parse_args(argv)
    if a.file:
        post = open(a.file, encoding="utf-8").read()
    elif a.text is not None:
        post = a.text
    elif not sys.stdin.isatty():
        post = sys.stdin.read()
    else:
        ap.error("give post text or --file")
    rc, out = run(post, a.snap_file)
    print("\n".join(out))
    return rc


if __name__ == "__main__":
    sys.exit(main())
