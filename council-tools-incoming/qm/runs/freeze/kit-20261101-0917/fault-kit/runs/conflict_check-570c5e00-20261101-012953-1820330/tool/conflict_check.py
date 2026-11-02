#!/usr/bin/env python3
"""Chancellor: conflict_check -- when one spec line changes, list every other
line that rules on the same thing, and the char cost of fixing each.
Usage: conflict_check.py PASTE LINE_NO "new line text" [--terms a,b]
Terms default to content words the change removes (old minus new).
Read-only: never edits the PASTE. Exit 0 = no other lines hit, 1 = hits to review, 2 = usage/error."""
import hashlib, re, sys
STOP = set("a an and or but the of to in on at is are be by for with no not nothing anywhere every all its it as".split())
WORD = re.compile(r"[A-Za-z][A-Za-z'-]*")
def words(s): return [w.lower() for w in WORD.findall(s)]
def sentences(line):
    # split on sentence ends; keep trailing space so a cut removes it too
    body = re.sub(r"^\s*(?:[-*]|\d+\.)\s+", "", line)  # list marker stays when a sentence is cut
    return [m.group(0) for m in re.finditer(r"[^.!?;]*[.!?;]\s*|[^.!?;]+$", body) if m.group(0).strip()]
NEG = r"(?:no|never|nothing|not|without)"
def ruling(term, s):
    # term within 3 words after a negation = a line that rules on the term
    return re.search(r"\b%s\b(?:\W+\w+){0,3}?\W+%s\b" % (NEG, re.escape(term)), s, re.I) is not None
def run(paste, ln, new, terms=None):
    text = open(paste, encoding="utf-8").read()
    lines = text.split("\n")
    old = lines[ln-1]
    if terms is None:
        nw = set(words(new))
        terms = sorted({w for w in words(old) if w not in nw and w not in STOP})
    out = {"paste_md5": hashlib.md5(text.encode()).hexdigest(), "chars": len(text),
           "line": ln, "old": old, "new": new, "delta": len(new) - len(old), "terms": terms, "hits": []}
    # tiers: A-ruling = a negation rules on a removed term; B-multi = 2+ removed terms together
    ruled = [t for t in terms if ruling(t, old)] or terms  # terms the old line itself ruled on
    out["ruled"] = ruled
    pats = {t: re.compile(r"\b%s\b" % re.escape(t), re.I) for t in terms}
    for i, l in enumerate(lines, 1):
        if i == ln: continue
        hit = [t for t, p in pats.items() if p.search(l)]
        if not hit or l.lstrip().startswith("{"): continue  # skip JSON data lines
        rules = [t for t in hit if t in ruled and ruling(t, l)]
        tier = "A-ruling" if rules else ("B-multi" if len(hit) > 1 else None)
        if tier is None: continue
        key = rules or hit
        sents = [s for s in sentences(l) if any(pats[t].search(s) for t in key)]
        out["hits"].append({"line": i, "tier": tier, "terms": hit, "text": l.strip(),
                            "sentences": [{"s": s.strip(), "cut_saves": len(s)} for s in sents]})
    return out
def report(o):
    r = ["**Chancellor:** conflict_check on PASTE %s (%d chars), line %d" % (o["paste_md5"], o["chars"], o["line"]),
         "**Chancellor:** old: %s" % o["old"].strip(), "**Chancellor:** new: %s" % o["new"].strip(),
         "**Chancellor:** change delta %+d chars, PASTE would be %d" % (o["delta"], o["chars"] + o["delta"]),
         "**Chancellor:** terms checked: %s (ruled on: %s)" % (", ".join(o["terms"]), ", ".join(o["ruled"])), "**Chancellor:** %d other line(s) hit:" % len(o["hits"])]
    for h in o["hits"]:
        r.append("**Chancellor:** :%d %s [%s] %s" % (h["line"], h["tier"], ",".join(h["terms"]), h["text"][:160]))
        for s in h["sentences"]:
            r.append("**Chancellor:**   cut \"%s\" saves %d" % (s["s"][:120], s["cut_saves"]))
    r.append("**Chancellor:** Hits are candidates only; a human decides which actually conflict.")
    return "\n".join(r)
if __name__ == "__main__":
    a = sys.argv[1:]
    terms = None
    if "--terms" in a:
        i = a.index("--terms"); terms = [t.strip().lower() for t in a[i+1].split(",")]; del a[i:i+2]
    if len(a) != 3: print(__doc__); sys.exit(2)
    o = run(a[0], int(a[1]), a[2], terms)
    print(report(o)); sys.exit(1 if o["hits"] else 0)
