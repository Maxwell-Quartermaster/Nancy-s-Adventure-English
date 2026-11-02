#!/usr/bin/env python3
"""thai-diff (owner: Instructor). Compares Thai runs between a BASE and NEW file.
Usage: thai_diff.py BASE NEW [--manifest PATH] | --selftest
Writes stdout only. Exit 0 = no Thai change, 1 = Thai changed, 2 = selftest fail."""
import sys, re, hashlib, collections, json
RUN = re.compile(r'[\u0E00-\u0E7F][\u0E00-\u0E7F \{\}\w:]*')
def md5(b): return hashlib.md5(b).hexdigest()
def runs(text): return [r.strip() for r in RUN.findall(text) if r.strip()]
def keyed(text):
    """Thai per JSON key path (cards) so a moved-but-unchanged string is caught."""
    try: data = json.loads(text)
    except Exception: return None
    out = {}
    def walk(o, p):
        if isinstance(o, dict):
            for k, v in o.items(): walk(v, p + '.' + str(k))
        elif isinstance(o, list):
            for i, v in enumerate(o):
                kid = v.get('id') if isinstance(v, dict) else None
                walk(v, p + '[' + (str(kid) if kid else str(i)) + ']')
        elif isinstance(o, str) and RUN.search(o): out[p] = o
    walk(data, '$'); return out
def diff(a, b):
    ca, cb = collections.Counter(runs(a)), collections.Counter(runs(b))
    removed = sorted((ca - cb).elements()); added = sorted((cb - ca).elements())
    moved = []
    ka, kb = keyed(a), keyed(b)
    if ka is not None and kb is not None:
        for k in sorted(set(ka) | set(kb)):
            if ka.get(k) != kb.get(k): moved.append(k)
    return sum(ca.values()), sum(cb.values()), removed, added, moved
def report(base, new, manifest=None):
    a, b = open(base, 'rb').read(), open(new, 'rb').read()
    me = md5(open(__file__, 'rb').read())
    mf = md5(open(manifest, 'rb').read()) if manifest else 'none'
    print(f"thai_diff.py {me} | MANIFEST {mf} | base {md5(a)} | new {md5(b)}")
    na, nb, rem, add, mov = diff(a.decode('utf-8'), b.decode('utf-8'))
    print(f"runs base {na} new {nb}")
    for r in rem: print("- " + r)
    for r in add: print("+ " + r)
    for k in mov: print("key changed: " + k)
    if not (rem or add or mov): print("NO THAI CHANGE")
    return 1 if (rem or add or mov) else 0
def selftest():
    base = json.dumps({"cards":[{"id":"c1","th":"หา {word} เจอไหม"},{"id":"c2","th":"สาม"}]}, ensure_ascii=False)
    tone = base.replace("ไหม", "ไหม่")              # planted tone mark
    added = base.replace('"สาม"}', '"สาม"},{"id":"c3","th":"กิน"}')  # planted new run
    moved = json.dumps({"cards":[{"id":"c1","th":"สาม"},{"id":"c2","th":"หา {word} เจอไหม"}]}, ensure_ascii=False)
    punct = "ทดสอบ…ผิด?"; punct2 = "ทดสอบ…ผด?"
    checks = [("clean", diff(base, base), False), ("tone mark", diff(base, tone), True),
              ("added run", diff(base, added), True), ("moved string", diff(base, moved), True),
              ("typo next to punctuation", diff(punct, punct2), True)]
    ok = True
    for name, (_, _, r, a, m), want in checks:
        got = bool(r or a or m); ok &= (got == want)
        print(f"{'PASS' if got == want else 'FAIL'} {name}")
    print("SELFTEST " + ("PASS" if ok else "FAIL")); return 0 if ok else 2
if __name__ == '__main__':
    if '--selftest' in sys.argv: sys.exit(selftest())
    args = [x for x in sys.argv[1:] if not x.startswith('--')]
    mf = sys.argv[sys.argv.index('--manifest') + 1] if '--manifest' in sys.argv else None
    if mf in args: args.remove(mf)
    sys.exit(report(args[0], args[1], mf))
