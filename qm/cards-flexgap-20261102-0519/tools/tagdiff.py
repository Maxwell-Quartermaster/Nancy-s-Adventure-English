# tagdiff.py: for each page pair base/new, every changed tag must be (a) a flex box with only `gap:Npx` removed or (b) a child with only
# `margin-left:Npx;` / `margin-top:Npx;` added at the start of its style (or a new style attr); text between tags must be identical.
import sys, os, re, difflib, json
TAG = re.compile(r"(<[^>]*>)")
def ok(a, b):
    if re.sub(r"(^|;)gap:\d+px(;|')", lambda m: m.group(1) if m.group(2) == ';' else m.group(2), a, count=1) == b and 'display:flex' in a: return 'gap-removed'
    if re.sub(r"style=(['\"])(margin-(left|top):\d+px;)", r"style=\1", b, count=1) == a: return 'margin-added'
    if re.sub(r" style='margin-(left|top):\d+px'", '', b, count=1) == a: return 'margin-attr'
    return None
res = {}
for size in sys.argv[1:]:
    A, B = f'html/base-{size}', f'html/new-{size}'
    if size == 'fit320': A, B = 'html/fit320-base', 'html/fit320-new'
    for f in sorted(os.listdir(A)):
        a = TAG.split(open(f'{A}/{f}', encoding='utf-8').read()); b = TAG.split(open(f'{B}/{f}', encoding='utf-8').read())
        kinds = {}; bad = []
        if len(a) != len(b): bad.append('token count %d vs %d' % (len(a), len(b)))
        else:
            for x, y in zip(a, b):
                if x != y:
                    k = ok(x, y) if x.startswith('<') else None
                    if k: kinds[k] = kinds.get(k, 0) + 1
                    else: bad.append((x[:100], y[:100]))
        res[f] = (kinds, bad[:3]); print(size, f, kinds, 'BAD' if bad else 'ok', bad[:2])
