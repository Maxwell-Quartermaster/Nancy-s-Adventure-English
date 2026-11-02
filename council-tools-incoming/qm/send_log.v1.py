#!/usr/bin/env python3
"""send_log.py - Quartermaster's send log with image fingerprints (patch, not installed).

  send_log.py add --file <png> [--file ...] --to Maxwell --note '...'
  send_log.py check <png>
  send_log.py list
Never deletes or rewrites rows; it only appends.
"""
import argparse, datetime, hashlib, os, sys
from zoneinfo import ZoneInfo

V608 = "/workspace/v608build"
DEFAULT_LOG = os.path.join(V608, "SEND-LOG.md")
DEFAULT_SNAP = os.path.join(V608, "CURRENT-SNAP.txt")
TZ = ZoneInfo("America/Denver")  # Mountain time: MST/MDT label printed per row
HEADER = [
    "**Quartermaster:** SEND-LOG: one row per image sent (send_log.py). Append-only; never edit or delete rows.",
    "**Quartermaster:** Time is Mountain (America/Denver); md5 is the full image md5; pointer = md5 of CURRENT-SNAP.txt at send time.",
    "",
    "| Time (Mountain) | To | File | md5 | Snap | Pointer md5 | Note |",
    "|---|---|---|---|---|---|---|",
]


def md5_file(p):
    h = hashlib.md5()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def read_snap(path):
    kv = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            if "=" in line:
                k, v = line.rstrip("\n").split("=", 1)
                kv.setdefault(k.strip(), v.strip())
    return kv.get("snap", "?"), md5_file(path)


def esc(s):
    return str(s).replace("|", "\\|").replace("\n", " ")


def parse_rows(log):
    rows = []
    if not os.path.exists(log):
        return rows
    with open(log, encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line.startswith("| ") or line.startswith("| Time") or line.startswith("|---"):
                continue
            cells = [c.strip().replace("\\|", "|") for c in line.replace("\\|", "\x00").strip("|").split("|")]
            cells = [c.replace("\x00", "|") for c in cells]
            if len(cells) >= 7:
                rows.append(dict(time=cells[0], to=cells[1], file=cells[2], md5=cells[3],
                                 snap=cells[4], pointer=cells[5], note=cells[6], raw=line))
    return rows


def cmd_add(a):
    missing = [p for p in a.file if not os.path.isfile(p)]
    if missing:
        print("ERROR: file not found: " + ", ".join(missing))
        return 2
    snap, ptr = read_snap(a.snap_file)
    prior = parse_rows(a.log)
    new = not os.path.exists(a.log)
    now = datetime.datetime.now(TZ)
    stamp = now.strftime("%Y-%m-%d %H:%M:%S ") + now.tzname()
    out = []
    for p in a.file:
        ap = os.path.abspath(p)
        m = md5_file(ap)
        if not ap.lower().endswith(".png"):
            print(f"NOTE: {ap} is not a .png; logged anyway")
        dup = [r for r in prior if r["md5"] == m]
        if dup:
            print(f"ALREADY SENT: {ap} md5 {m} was sent {dup[0]['time']} to {dup[0]['to']} ({len(dup)} earlier row(s)); logging this send too")
        out.append(f"| {stamp} | {esc(a.to)} | {esc(ap)} | {m} | {esc(snap)} | {ptr} | {esc(a.note)} |")
        print(f"LOGGED {m} {ap}")
    with open(a.log, "a", encoding="utf-8") as f:
        if new:
            f.write("\n".join(HEADER) + "\n")
        f.write("\n".join(out) + "\n")
    print(f"{len(out)} row(s) appended to {a.log} (snap {snap}, pointer {ptr[:8]})")
    return 0


def cmd_check(a):
    if os.path.isfile(a.png):
        m = md5_file(a.png)
    elif len(a.png) == 32 and all(c in "0123456789abcdef" for c in a.png.lower()):
        m = a.png.lower()
    else:
        print(f"ERROR: not a file or md5: {a.png}")
        return 2
    hits = [r for r in parse_rows(a.log) if r["md5"] == m]
    if not hits:
        print(f"NOT SENT: md5 {m} has no row in {a.log}")
        return 0
    print(f"SENT {len(hits)} time(s): md5 {m}")
    for r in hits:
        print(f"  {r['time']} to {r['to']}: {r['file']} (snap {r['snap']}, pointer {r['pointer'][:8]}) note: {r['note']}")
    return 1


def cmd_list(a):
    rows = parse_rows(a.log)
    if not rows:
        print(f"(no rows in {a.log})")
        return 0
    for r in rows:
        print(r["raw"])
    print(f"{len(rows)} row(s)")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--log", default=DEFAULT_LOG)
    ap.add_argument("--snap-file", default=DEFAULT_SNAP)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("add"); s.add_argument("--file", action="append", required=True)
    s.add_argument("--to", required=True); s.add_argument("--note", default="")
    s = sub.add_parser("check"); s.add_argument("png")
    sub.add_parser("list")
    a = ap.parse_args(argv)
    return {"add": cmd_add, "check": cmd_check, "list": cmd_list}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
