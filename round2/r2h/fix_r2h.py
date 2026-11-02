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
WALK = re.compile(r"<path d='M[\d.]+ (?:844|568)q[^']*' stroke='#(?:E8D9A8|D8C99A)' stroke-width='(?:20|26)'[^>]*/>")   # Watchman 2b: the M140/M118/M330 strokes at 390 and 320
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
    doc = WALK.sub(sidewalk() if SIDEWALK else '', doc); log.append(f'{tag}: brush-stroke walkway removed (16/16S look)'); return doc
# Maxwell t527u (game-wide): no low-detail circle dots on grass; every one becomes the t441u three-blade tuft (the 11-12 / W24 / 48 style).
# This is the one ground pass every r2h page goes through (fix() below), independent of the walkway fix, so every page inherits it.
# Where every converted tuft ends up under the UI (the ask/reward card covers y 660-690), the page would read as bare grass, so the
# W24 open-grass set (stage_v608 TUFTS['W24-walk-B']) plus one centre tuft is added in the same ground layer (behind heroes and props).
OPEN_TUFTS = [(60, 532), (24, 604), (374, 604), (196, 612), (352, 548)]
HIDDEN_TUFT_PAGES = ('12-', '15-', '23-', '24-', '25-', '26-', '27-', '28-', '30-', '37-')   # tuft_check b19579ac BLOCK "bare grass" on the r2h afters before this pass
def ground_dots(doc, log, tag):
    k = [0]; first = [None]
    def fd(m):
        k[0] += 1; t = tuft(float(m.group(1)), float(m.group(2)) + 3)
        return t
    m0 = DOT.search(doc)
    if not m0: return doc
    doc = DOT.sub(fd, doc); log.append(f'{tag}: {k[0]} ground dots -> tufts (t527u)')
    if tag.startswith(HIDDEN_TUFT_PAGES) and "data-r2h='open-tufts'" not in doc:
        i = doc.find("data-deco='tuft'/>", m0.start()) + len("data-deco='tuft'/>")
        doc = doc[:i] + "<g data-r2h='open-tufts'>" + ''.join(tuft(x, y) for x, y in OPEN_TUFTS) + '</g>' + doc[i:]
        log.append(f'{tag}: open-grass tufts {OPEN_TUFTS} (converted tufts sit under the card)')
    return doc
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
def r2tp(doc, log, tag):   # sheetkit r2tp (15dda05b): the round-2 ask wording, before every other fix (Watchman 2a)
    d2 = re.sub(r'Where is the ([a-z]+)\?', r'Can you find the \1?', doc); d2 = re.sub(r'([a-z]+) อยู่ที่ไหน', r'หา \1 เจอไหม', d2)
    if d2 != doc: log.append(f'{tag}: r2tp ask wording (Can you find the X? / หา X เจอไหม)')
    return d2
BOSS_FILL = {'24-': 1.0, '25-': 0.8, '26-': 0.7, '27-': 0.0}   # boss step (aa778f86): red bar drops one tenth per right card; kneels when empty
CHIP_BOTTOM = {390: 114.7, 375: 114.7, 320: 102.7}   # the zone chip (boss.name) bottom, from the r2h sidecars
def bossplate(doc, log, tag, w):
    k = tag[:3]
    if k not in BOSS_FILL or "data-r2h='boss-plate'" in doc: return doc
    W = 390 if w == 390 else w; y = CHIP_BOTTOM[w] + 6; f = BOSS_FILL[k]; bw = W - 32 - 24
    if w != 390:   # 375/320: no sky room above the bubble (top 136.9 / 124.9), so a 12 pt red bar sits in the gap under the zone chip (the chip is the nameplate)
        x0 = 16
        blk = (f"<div data-r2h='boss-plate' data-bb='boss-bar' data-fill='{f:.1f}' style='position:absolute;left:{x0}px;top:{CHIP_BOTTOM[w] + 5}px;width:{w - 16 - x0}px;height:12px;box-sizing:border-box;border:2px solid #10170F;border-radius:7px;background:#3A2410;overflow:hidden;z-index:50'>"
               f"<div style='position:absolute;left:0;top:0;bottom:0;width:{f*100:.0f}%;background:#C8343A'></div></div>")
        i = doc.rfind('</body>'); doc = (doc[:i] + blk + doc[i:]) if i >= 0 else doc + blk
        log.append(f'{tag}: red boss bar ({int(f*10)}/10) under the zone chip, y {CHIP_BOTTOM[w] + 5}-{CHIP_BOTTOM[w] + 17}'); return doc
    blk = (f"<div data-r2h='boss-plate' data-bb='boss-plate' style='position:absolute;left:16px;top:{y}px;width:{W-32}px;box-sizing:border-box;padding:4px 12px 8px;background:#F6E9C8;border:3px solid #10170F;border-radius:10px;box-shadow:inset 0 0 0 2px #E8B84A,0 3px 0 #10170F;z-index:50'>"
           f"<div style='display:flex;gap:8px;align-items:baseline;justify-content:center;white-space:nowrap'><span data-txt=1 style=\"font:400 20px/1.1 'Lilita One',sans-serif;color:#3A2410\">The Word Guardian</span><span data-txt=1 style='font:400 17px/1.7 Kanit,Thonburi,sans-serif;color:#3A2410'>ผู้พิทักษ์คำ</span></div>"
           f"<div data-bb='boss-bar' data-fill='{f:.1f}' style='position:relative;height:12px;border:2px solid #10170F;border-radius:6px;background:#3A2410;overflow:hidden'><div style='position:absolute;left:0;top:0;bottom:0;width:{f*100:.0f}%;background:#C8343A'></div></div></div>")
    i = doc.rfind('</body>'); doc = (doc[:i] + blk + doc[i:]) if i >= 0 else doc + blk
    log.append(f'{tag}: Word Guardian plate + red bar ({int(f*10)}/10) under the zone chip at y {y}'); return doc
def echoplate(doc, log, tag, w):
    if not tag.startswith('36-') or "data-r2h='echo-plate'" in doc: return doc
    blk = (f"<div data-r2h='echo-plate' data-bb='echo-plate' style='position:absolute;left:16px;top:{CHIP_BOTTOM[w] + 6}px;padding:2px 10px;background:#F6E9C8;border:3px solid #10170F;border-radius:10px;box-shadow:inset 0 0 0 2px #E8B84A,0 3px 0 #10170F;white-space:nowrap;z-index:50'>"
           f"<span data-txt=1 style=\"font:400 20px/1.1 'Lilita One',sans-serif;color:#3A2410\">Echo Knight</span> <span data-txt=1 style='font:400 17px/1.7 Kanit,Thonburi,sans-serif;color:#3A2410'>อัศวินเสียงสะท้อน</span></div>")
    i = doc.rfind('</body>'); doc = (doc[:i] + blk + doc[i:]) if i >= 0 else doc + blk
    log.append(f'{tag}: Echo Knight mini plate (no bar)'); return doc
SHOP = ((">GOLDEN PANTRY<", ">Shop<"), (">ตู้กับข้าวทองคำ<", ">ร้านดาวทอง<"))   # Shop rename (t487u): uiText.pantry in PASTE 317e91ce, whole strings only
def shop(doc, log, tag):
    for a, b in SHOP:
        n = doc.count(a)
        if n: doc = doc.replace(a, b); log.append(f'{tag}: {a[1:-1]} -> {b[1:-1]} x{n} (uiText.pantry)')
    return doc
# Instructor copy fault (37 rest screen): the verse block comes straight from PASTE 317e91ce (verses.rest, verses.attribution tags), never retyped:
# no added quote marks (:344), the THSV11 Thai line under the English (:404), and (ESV)/(THSV11) as separate small tags, not "ESV · THSV11" (:346).
PASTE_1B = '/workspace/v608build/r2h-build/nancys-adventure-english-v6-08-1B-v32-PASTE.md'
def _paste_data():
    import json as _j
    for ln in open(PASTE_1B, encoding='utf-8').read().split('\n'):
        if ln.startswith('{"version":"v6-08"'): return _j.loads(ln)
VERSE_BLOCK = re.compile(r"<div class='e20' data-txt=1 style=''>([^<]+)</div><div class='e15' data-txt=1 style='([^']*)'>[^<]*</div>(?:<div class='t17' data-txt=1 style=''>[^<]*</div>)?<div class='e15' data-txt=1 style=''>ESV · THSV11</div>")
REST_CARD = "data-name='card' style='left:16px;top:576px;width:358px;height:260px;'"
VERSE_PAGES = ('29-verse-scroll-gift', '37-rest-screen', '44-scroll-reopened')   # Instructor copy faults (37) + Maxwell 1:33 AM decision (29, 44)
def _paste_verse(d, ref):
    """the verse object for ref from PASTE data: verses.* first, then zones[].boss.scroll (where the boss scrolls live)"""
    hits = []
    def walk(o, path):
        if isinstance(o, dict):
            if o.get('ref') == ref and 'en' in o and 'th' in o and o.get('status') == 'VERIFIED': hits.append((path, o))
            for k, v in o.items(): walk(v, path + '.' + k)
        elif isinstance(o, list):
            for i, v in enumerate(o): walk(v, path + f'[{i}]')
    walk(d.get('verses', {}), 'verses')
    if not hits:
        for i, z in enumerate(d.get('zones', [])): walk(z.get('boss', {}), f'zones[{i}].boss')
    if len({(o['en'], o['th']) for _, o in hits}) != 1: raise SystemExit(f'verse {ref}: {len(hits)} PASTE matches, not one text')
    return hits[0]
def restverse(doc, log, tag):
    if not tag.startswith(VERSE_PAGES) or not VERSE_BLOCK.search(doc): return doc
    d = _paste_data(); att = d['verses']['attribution']
    import html as _h
    e = lambda t: _h.escape(t, quote=False).replace('\n', '<br>')
    def rep(m):
        path, v = _paste_verse(d, _h.unescape(m.group(1))); en_style = m.group(2) if 'line-height' in m.group(2) else m.group(2) + ';line-height:1.35'
        log.append(f"{tag}: verse {v['ref']} from PASTE {path} en+th, tags {att['esvTag']} {att['thsv11Tag']} separate")
        return (f"<div class='e20' data-txt=1 style=''>{e(v['ref'])}</div>"
                f"<div class='e15' data-txt=1 data-verse='en' style='{en_style}'>{e(v['en'])}</div>"
                f"<div class='e15' data-txt=1 data-tag='esv' style='font-size:12px;line-height:1.4;opacity:.85'>{e(att['esvTag'])}</div>"
                f"<div class='t17' data-txt=1 data-verse='th' style=''>{e(v['th'])}</div>"
                f"<div class='e15' data-txt=1 data-tag='thsv11' style='font-size:12px;line-height:1.4;opacity:.85'>{e(att['thsv11Tag'])}</div>")
    doc = VERSE_BLOCK.sub(rep, doc)
    if tag.startswith('37-rest-screen') and REST_CARD in doc:
        doc = doc.replace(REST_CARD, "data-name='card' style='left:16px;top:556px;width:358px;height:280px;'", 1); log.append(f'{tag}: card top 576->556 h 260->280 (fits the added Thai line)')
    return doc

def fix(doc, tag, w):
    log = []
    doc = shop(doc, log, tag)
    doc = r2tp(doc, log, tag)
    doc = bossplate(doc, log, tag, w)   # echoplate() not used: screen 36 already shows the Echo Knight chip (no bar)
    for f in (meadow, ground_dots, ground_trees, forest, homelake, restverse): doc = f(doc, log, tag)
    doc = room(doc, log, tag, w)
    return doc, log
