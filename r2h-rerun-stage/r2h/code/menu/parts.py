# Pieces lifted from the approved map render (screens-v608 05-map-day1, r2h colour fix applied) for the r2h menu/map concepts.
import re
SRC = '/workspace/v608build/round2/r2h/html/05-map-day1-390x844.html'
D = open(SRC).read()
def div_end(d, i):
    n = 0
    for m in re.compile(r'<div\b|</div>').finditer(d, i):
        n += 1 if m.group(0) == '<div' else -1
        if n == 0: return m.end()
    raise ValueError(i)
def el(bb, d=D):
    m = re.search(r"<div[^>]*data-bb='%s'" % re.escape(bb), d); i = m.start(); return d[i:div_end(d, i)]
HEAD = D[:D.index('<body')]
BODY_OPEN = D[D.index('<body'):D.index('>', D.index('<body')) + 1]
DEFS = D[4909:8177]                      # hidden symbol svg (#rH, #rF, #rE, frames...)
ART = D[8177:D.index('</svg>', 8177) + 6]
WASH = D[17133:D.index('</svg>', 17133) + 6]
def svg_at(i): return D[i:D.index('</svg>', i) + 6]
