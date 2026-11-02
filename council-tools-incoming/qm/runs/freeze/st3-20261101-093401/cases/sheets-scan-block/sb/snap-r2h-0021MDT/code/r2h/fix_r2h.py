# r2h render-time fixes (QM executor, Nov 1 2026). Post-processes existing approved HTML; never edits mock code or snapshots.
# Maxwell t467u/t473u/t476u: trees grounded; t-path removed (16/16S look, default) + grass tufts; sidewalk kept as an unrendered toggle.
# t470u/t472u: taller wall (replaces the 1A ceiling crop), tie hangs straight, bed (crib) 8 pt forward. t471u: moon to sky centre.
# t474u: Home Lake colour #D9663F -> #F05A00.
import re, math
SIDEWALK = False          # toggle only (Watchman's spec); default off = path removed like 16/16S
HL_OLD, HL_NEW = '#D9663F', '#F05A00'
CEIL_STRIP = 40
TRIM = '1B'   # Maxwell t492u: 1B = only the front desk and kitchen get the taller wall
WALL_ROOMS = lambda tag: TRIM == '1A' or tag[:3] in ('20-', '21-', '22-')   # kitchen screens; the front desk is stage scene E (stage pipeline, not here)
HUD_BOTTOM = {390: 123.0, 320: 110.9, 375: None}   # screen y of the HUD+chip bottom (390 LOG 123; 320 cap 295 at s .80447, oy -126.44)
def _qy(x, x0, y0, cx, cy, x1, y1):
    lo, hi = 0.0, 1.0
    for _ in range(50):
        t = (lo+hi)/2; xt = (1-t)**2*x0 + 2*t*(1-t)*cx + t*t*x1
        lo, hi = (t, hi) if xt < x else (lo, t)
    t = (lo+hi)/2; return (1-t)**2*y0 + 2*t*(1-t)*cy + t*t*y1
HILL = re.compile(r"<path d='M0 ([\d.]+)q([\d.]+) (-?[\d.]+) ([\d.]+) (-?[\d.]+)t([\d.]+) (-?[\d.]+)V")
def hills(doc):
    out = []
    for m in HILL.finditer(doc):
        y0, a, b, c, d, e, f = map(float, m.groups()); cx, cy = a, y0+b; x1, y1 = c, y0+d; x2, y2 = c+e, y1+f
        out.append((0, y0, cx, cy, x1, y1, 2*x1-cx, 2*y1-cy, x2, y2))
    return out
def grass_y(H, x):
    ys = []
    for x0, y0, cx, cy, x1, y1, rx, ry, x2, y2 in H:
        xx = min(max(x, 0), x2)
        ys.append(_qy(xx, x0, y0, cx, cy, x1, y1) if xx <= x1 else _qy(xx, x1, y1, rx, ry, x2, y2))
    return min(ys) if ys else None
def ground_trees(doc, log, tag):
    H = hills(doc)
    if not H: return doc
    def fa(m):   # <g data-deco='tree'><path d='M{x} {yb}q ...  (P.tree, absolute coords)
        x, yb = float(m.group(1)), float(m.group(2)); g = max(grass_y(H, x), grass_y(H, x+6.6)) + 3
        if yb >= g - 0.5: return m.group(0)
        log.append(f'{tag}: tree at x {x+3.3:.0f} base y {yb:.0f} -> {g:.1f} (+{g-yb:.1f})')
        return m.group(0).replace("<g data-deco='tree'>", f"<g data-deco='tree' data-r2h-ground='{g-yb:.1f}' transform='translate(0 {g-yb:.1f})'>", 1)
    doc = re.sub(r"<g data-deco='tree'><path d='M([\d.]+) ([\d.]+)q", fa, doc)
    def fb(m):   # pine: translate(x yb)scale(s)
        x, yb, s = map(float, m.groups()); g = max(grass_y(H, x-6*s), grass_y(H, x+4*s)) + 3
        if yb >= g - 0.5: return m.group(0)
        log.append(f'{tag}: pine at x {x:.0f} base y {yb:.0f} -> {g:.1f}')
        return f"<g data-deco='tree' data-r2h-ground='{g-yb:.1f}' transform='translate({x:g} {g:.1f})scale({s:g})'>"
    return re.sub(r"<g data-deco='tree' transform='translate\(([\d.]+) ([\d.]+)\)scale\(([\d.]+)\)'>", fb, doc)
def tuft(x, y, col='#0F3A14'):   # the walk 24 / t441u tuft: three small blades
    return f"<path d='M{x-6} {y}q1-7 -2-10M{x-1} {y}q-1-9 1-14M{x+4} {y}q0-7 4-10' stroke='{col}' stroke-width='2.5' fill='none' stroke-linecap='round' data-deco='tuft'/>"
WALK = re.compile(r"<path d='M140 844q20-140 120-250' stroke='#E8D9A8' stroke-width='26' opacity='\.85'/>")
DOT = re.compile(r"<circle cx='([\d.]+)' cy='([\d.]+)' r='3' fill='#[0-9A-Fa-f]{6}' stroke-width='1\.5'/>")
def sidewalk():   # toggle only (unrendered): Watchman spec, VP at the hill crest behind the swing set, 40% -> 7% width
    n, vp, base = 7, (214, 404), (205, 844); wn, wf = 156, 27; pts_l, pts_r, joints = [], [], []
    for i in range(21):
        t = i/20; y = base[1] + (vp[1]-base[1])*t; cx = base[0] + (vp[0]-base[0])*t; w = wn + (wf-wn)*t
        pts_l.append((cx-w/2, y)); pts_r.append((cx+w/2, y))
    poly = ' '.join(f'{x:.1f},{y:.1f}' for x, y in pts_l + pts_r[::-1]); gap = 90.0; y = 844.0; j = ''
    while y - gap > 420:
        y -= gap; t = (844-y)/440; cx = base[0]+(vp[0]-base[0])*t; w = wn+(wf-wn)*t; j += f"M{cx-w/2:.1f} {y:.1f}h{w:.1f}"; gap *= .8
    return (f"<polygon points='{poly}' fill='#D6CFC1' stroke='#10170F' stroke-width='2' stroke-opacity='.65' data-deco='sidewalk'/>"
            f"<path d='M{pts_l[0][0]:.1f} 844L{pts_l[-1][0]:.1f} {vp[1]}l3 0L{pts_l[0][0]+10:.1f} 844z' fill='#BDB5A6' stroke='none'/><path d='{j}' stroke='#A9A396' stroke-width='1.5'/>")
def meadow(doc, log, tag):
    if not WALK.search(doc): return doc
    doc = WALK.sub(sidewalk() if SIDEWALK else '', doc); log.append(f'{tag}: brush-stroke walkway removed (16/16S look)')
    k = [0]
    def fd(m):
        k[0] += 1; return tuft(float(m.group(1)), float(m.group(2)) + 3)
    doc = DOT.sub(fd, doc); log.append(f'{tag}: {k[0]} ground dots -> tufts'); return doc
WORLD = re.compile(r"data-st='[^']+' style='left:(-?[\d.]+)px;top:(-?[\d.]+)px;width:390px;height:844px;overflow:hidden;transform:scale\(([\d.]+)\)")
TIE_IN = "<!-- Private family use. Original redraw of a CC0 Openclipart winner. --><path d='M40 10.5c4-5 16-8 19-5s-6 8-17 9' stroke-width='8'/>"
def room(doc, log, tag, w):
    if "M0 0h390v372H0z' fill='#D8C08A'" not in doc: return doc
    wall = WALL_ROOMS(tag)
    m = WORLD.search(doc); ox, oy, s = (map(float, m.groups()) if m else (0.0, 0.0, 1.0))
    vis = (HUD_BOTTOM[w] - oy) / s; ce = round(min(372, vis + CEIL_STRIP), 1)
    a = "<path d='M0 372h390v8H0z' fill='#C9A46A' stroke-width='2'/>"; assert doc.count(a) == 1, tag
    if wall: doc = doc.replace(a, a + f"<path d='M0 {ce}h390V380H0z' fill='#EAD7A8' stroke='none' data-r2h='taller-wall'/><path d='M0 {ce}h390' stroke-width='3'/><path d='M0 {ce}h390v8H0z' fill='#C9A46A' stroke-width='2'/>")
    if wall: log.append(f'{tag}: wall top 372 -> {ce} (design; ceiling {CEIL_STRIP} pt under the HUD from y {vis:.0f}); scale {s:.5f} unchanged')
    # tie: hang straight down, top of the knot at the peg (88,458 -> icon 32,4.6), the art turned upright (-28.1 deg, its blade axis)
    n = doc.count(TIE_IN)
    if n:
        doc = re.sub(r"(<svg[^>]*viewBox='0 0 64 64'[^>]*>)(<!-- Private family use\. Original redraw of a CC0 Openclipart winner\. --><path d='M40 10\.5c4-5 16-8 19-5s-6 8-17 9'.*?)(</svg>)",
                     lambda q: q.group(1) + "<g data-r2h='tie-plumb' transform='translate(32 5)rotate(-28.1)translate(-38 -11)'>" + q.group(2) + '</g>' + q.group(3), doc, flags=re.S)
        log.append(f'{tag}: tie x{n} hangs straight from the peg')
    # bed (crib) 8 pt forward onto the floor (no scale change)
    def cb(q): return q.group(1) + f"{float(q.group(2))+8:g}" + q.group(3)
    n0 = len(re.findall(r"data-(?:pn|name)='crib'", doc)) if tag.startswith('54-') else 0   # t472u bed forward: tile 10 (screen 54) only
    if not n0: return doc
    doc = re.sub(r"(data-(?:pn|name)='crib'[^>]*?top:)([\d.]+)(px)", cb, doc)
    doc = re.sub(r"(<ellipse cx='306' cy=')662(' rx='57' ry='3')", r"\g<1>670\2", doc)
    if n0: log.append(f'{tag}: crib +8 pt forward ({n0} tags)')
    return doc
MOON = "<path d='M262 128a10 10 0 1 0 8 16 8 8 0 1 1-8-16z' fill='#F3EBD0'/>"
def forest(doc, log, tag):
    if MOON in doc and ("='owl'" in doc): doc = doc.replace(MOON, "<path d='M147 128a10 10 0 1 0 8 16 8 8 0 1 1-8-16z' fill='#F3EBD0'/>"); log.append(f'{tag}: moon path x 262 -> 147 (drawn at about x 195, the sky centre)')
    return doc
def homelake(doc, log, tag):
    n = doc.count(HL_OLD)
    if n: doc = doc.replace(HL_OLD, HL_NEW); log.append(f'{tag}: Home Lake colour x{n} {HL_OLD} -> {HL_NEW}')
    return doc
def fix(doc, tag, w):
    log = []
    for f in (meadow, ground_trees, forest, homelake): doc = f(doc, log, tag)
    doc = room(doc, log, tag, w)
    return doc, log
