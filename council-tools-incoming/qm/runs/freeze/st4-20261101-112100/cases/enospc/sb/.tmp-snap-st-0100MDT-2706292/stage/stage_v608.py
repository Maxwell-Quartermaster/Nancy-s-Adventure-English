# Maxwell t439u/t441u (6:11-6:16 PM MDT): ONE scene layout for every phone. Each scene (A-H, and screen 24 walk B) is drawn once in the
# 390x844 design box; on any phone the whole stage scales as one piece (uniform s, centred, parchment letterbox where the shape differs),
# so props keep their spot on their furniture. Props are placed relative to their anchor (hook, shelf top, desk top, table, bench, post,
# road, water, grass) by their measured ink, not by the screen. HUD and the ask card stay at the phone's own size (UI, not scaled).
# Taps: a scaled prop gets an unscaled hit area (44 pt+, centred on it). Render-only (0 PASTE chars).
# Usage: python3 stage_v608.py [build|check] ; writes stage/html, stage/png, stage/CHECK.md (small files only).
import os, sys, json, re, subprocess, tempfile, shutil, concurrent.futures as CF
ARGV = sys.argv[1:]
HERE = '/workspace/v608build/scenes'; OUT = os.environ.get('NAE_STAGE_OUT', HERE + '/stage/')   # round 2 renders write elsewhere
SIZES = [(390, 844), (375, 667), (320, 568)]
DW, DH = 390, 844
MARK = '<!--UI-->'
def _mark(mod):
    t0 = mod.top
    mod.top = lambda *a, **k: MARK + t0(*a, **k)
if os.environ.get('NAE_SE') == '1':   # child: the 320x568 UI (HUD + ask card) from the approved 320 code
    sys.argv = ['x']; sys.path.insert(0, HERE); import scenes320_v608 as S3
    PV = S3.PV; _mark(PV)
    ui = {}
    for n, fn in S3.M.items():
        if n.startswith('C10'): continue
        h = fn(); ui[n] = h[h.index(MARK) + len(MARK):]
    _pl0 = PV.plates   # 320: two 128 pt plates fit the 288 pt card (264 inside); words stay 20 px
    PV.plates = lambda ch, wrong=None, right=None, h=52, wd=128, cls=None: _pl0(ch, wrong, right, h, wd, cls).replace("class='e15 nw'", "class='e20 nw'")
    PV.R2C_SE = False   # r2c: the walk keeps its staged 320 card; only 25-28 take the compact guardian card
    h = PV.grun('sw-15', 1.0); ui['W24-walk-B'] = h[h.index(MARK) + len(MARK):]
    json.dump(ui, open('/tmp/stage_ui320.json', 'w')); sys.exit(0)
sys.argv = ['x']; sys.path.insert(0, HERE); sys.path.insert(0, '/workspace/v608build/screens')
import scenes_v608 as SV
g = SV.g; PV = SV.PV; P = PV.P; Z = PV.Z; S = PV.S
_mark(PV)
import t441u_outdoor as T441; T441.apply(P, Z); PV.grass_y = T441.grass_y; PV.tuft = T441.tuft   # t441u outdoor fixes: stage scenes only (S2)
# A: the pathway stays low (t441u), as in every park
_A0 = g['M']['A-meadow-evening-pond']
def _A():
    h = _A0(); a = "<path d='M300 844q-40-140 -150-260' stroke='#D8C99A' stroke-width='26' opacity='.8'/>"
    assert h.count(a) == 1; return h.replace(a, "<path d='M330 844q-30-70 -190-120' stroke='#D8C99A' stroke-width='26' opacity='.8'/>")
g['M']['A-meadow-evening-pond'] = _A
# D: the word plates are UI anchored to their basket (they keep the phone's own size); placeholders here
def _tagph(x, y, en, th, w=96): return f"<i data-tagph='{en}' data-x='{x}' data-y='{y}' data-w='{w}'></i>"
# W24: screen 24 walk B (t441u): the walker stands on the grass, centred between the screen edge and Sam, a little bigger (52 pt, was 40)
WALK = (30, 434, 52)
def _w24():
    h = PV.grun('sw-15', 1.0); a = PV.tplate('🚶'); assert h.count(a) == 1
    return h.replace(a, PV.gprop('🚶', *WALK).replace("data-pic='prop'", "data-pic='prop' data-pn='walker'", 1), 1)
SCENES = dict(g['M']); SCENES['W24-walk-B'] = _w24
ZONE = {'A': 'meadow', 'B': 'meadow', 'C': 'fields', 'D': 'fields', 'E': 'lake', 'F': 'lake', 'G': 'forest', 'H': 'forest', 'W': 'meadow'}
# Anchors in design (390) points: (prop data-name or data-pn, nth, mode, ax, ay, what). hang: ink top on (ax, ay); stand: ink bottom on it.
# ax must fall inside the prop's ink; the fit moves the prop so its ink centre (hang: its ring, 72% in, top right) sits on ax.
ANCH = {
 'E-lake-front-desk': [('keys', 0, 'hang', 57, 406, 'middle hook (rack 386-398, hook to 408)'), ('book', 0, 'stand', 164, 473, 'shelf top 474'),
                       ('truck', 0, 'stand', 318, 532, 'road 524-536 in the window')],
 # F and A spacing: the 44 pt hit areas stay 8 pt apart and 16 pt from the edge at the smallest scale (A .64 at 320x568, F .82)
 'F-lake-night-table': [('bread', 0, 'stand', 66, 437, 'shelf top 438'), ('sundae', 0, 'stand', 47, 580, 'desk top (19% of 112 from 558.5)'),
                        ('eggs', 0, 'stand', 111, 580, 'desk top'), ('croissant', 0, 'stand', 270, 585, 'table cloth top 586'), ('spaghetti', 0, 'stand', 336, 585, 'table cloth top 586')],
 'A-meadow-evening-pond': [('bread', 0, 'stand', 307, 613, 'bench back rail top 614'), ('ship', 0, 'stand', 306, 523, 'pond water (cy 520)'),
                           ('shop', 0, 'stand', 211, None, 'far hill grass line')],
 'C-fields-count-it': [('hat', 0, 'stand', 72, 381, 'fence post top 384')],
 'W24-walk-B': [('walker', 0, 'stand', 56, 484, 'grass, centred 0..Sam')],
}
CEIL = {'E-lake-front-desk': 372, 'F-lake-night-table': 372}
def split(h): i = h.index(MARK); return h[:i], h[i + len(MARK):]
def run_chrome(args, timeout=90):
    d = tempfile.mkdtemp(prefix='stg-', dir='/tmp')
    try: return subprocess.run(['google-chrome', '--headless=new', '--no-sandbox', '--disable-gpu', '--hide-scrollbars', '--virtual-time-budget=800'] + args,
                               env=dict(os.environ, TMPDIR=d), capture_output=True, text=True, timeout=timeout)
    finally: shutil.rmtree(d, ignore_errors=True)
def shot(doc, png, w, h):
    d = tempfile.mkdtemp(prefix='stgp-', dir='/tmp'); p = d + '/p.html'; open(p, 'w').write(doc)
    try: run_chrome(['--force-device-scale-factor=2', f'--window-size={w},{h}', f'--screenshot={png}', 'file://' + p])
    finally: shutil.rmtree(d, ignore_errors=True)
# MEAS uses the phone size given, not innerWidth/innerHeight (headless Chrome windows have a minimum width).
MEAS = """<script>addEventListener('load',()=>{const W=%W%,H=%H%;let top=0,card=H,st=H;
for(const e of document.querySelectorAll('[data-ui] *, [data-ui]')){const r=e.getBoundingClientRect();if(!r.width||!r.height)continue;
 if(r.top<.3*H&&r.height<.25*H)top=Math.max(top,r.bottom);if(r.top>.45*H&&r.width>.6*W)card=Math.min(card,r.top)}
for(const e of document.querySelectorAll('[data-st] [data-name],[data-st] [data-hero],[data-st] [data-pn],[data-st] [data-tagph]')){const r=e.getBoundingClientRect();if(r.height)st=Math.min(st,r.top)}
let hb=0;for(const e of document.querySelectorAll('[data-st] [data-hero]')){const r=e.getBoundingClientRect();hb=Math.max(hb,r.bottom)}
const pre=document.createElement('pre');pre.id='bbout';pre.textContent=JSON.stringify({top,card,st,hb});document.body.appendChild(pre)})</script>"""
def measure(doc, w, h):
    d = tempfile.mkdtemp(prefix='stgm-', dir='/tmp'); p = d + '/m.html'; open(p, 'w').write(doc.replace('</body>', MEAS.replace('%W%', str(w)).replace('%H%', str(h)) + '</body>'))
    try: o = run_chrome([f'--window-size={w},{h}', '--dump-dom', 'file://' + p]).stdout
    finally: shutil.rmtree(d, ignore_errors=True)
    import html as H_; return json.loads(H_.unescape(re.search(r'<pre id="bbout">(.*?)</pre>', o, re.S).group(1)))
def els(stage, key):   # (start, end) of the opening tag of each element carrying data-name / data-pn = key
    return [m for m in re.finditer(r"<div class='abs'[^>]*?data-(?:name|pn)='%s'[^>]*>" % re.escape(key), stage)]
def tagnum(t, k): m = re.search(r"%s:(-?[0-9.]+)px" % k, t); return float(m.group(1))
def shift(stage, key, nth, dx, dy):   # move a prop (and the contact shadow / water ring drawn just before it) by dx, dy design points
    m = els(stage, key)[nth]; t = m.group(0)
    t2 = re.sub(r"left:(-?[0-9.]+)px", lambda q: f"left:{float(q.group(1)) + dx:.1f}px", t, count=1)
    t2 = re.sub(r"top:(-?[0-9.]+)px", lambda q: f"top:{float(q.group(1)) + dy:.1f}px", t2, count=1)
    pre = stage[:m.start()]; sh = re.search(r"<div class='abs' style='left:(-?[0-9.]+)px;top:(-?[0-9.]+)px;width:[0-9.]+px;height:10px;border-radius:50%[^']*'></div>$", pre)
    if sh:
        s2 = f"<div class='abs' style='left:{float(sh.group(1)) + dx:.1f}px;top:{float(sh.group(2)) + dy:.1f}px" + sh.group(0)[sh.group(0).index(';width'):]
        pre = pre[:sh.start()] + s2
    return pre + t2 + stage[m.end():]
# D2 fit to width: the sky crops under the HUD at 375 and 320, so sky targets come down (design top >= 306 pt keeps them clear of the HUD at 320)
MOVE = {'B-meadow-listen-and-find': [('kite', 0, 26, 156), ('bus stop', 0, 0, 30)], 'A-meadow-evening-pond': [('rain', 0, 0, 110)]}
TUFTS = {'B-meadow-listen-and-find': [(64, 578), (256, 524), (372, 616)], 'A-meadow-evening-pond': [(30, 522), (36, 596), (258, 604)],
         'W24-walk-B': [(60, 532), (24, 604), (374, 604)]}
def stage_of(name):
    g['tag'] = _tagph
    st, ui = split(SCENES[name]())
    for k, n, dx, dy in MOVE.get(name, []): st = shift(st, k, n, dx, dy)
    if name in TUFTS:   # S1: tufts on open grass above the card, behind the hero and props
        k = st.find('data-hero='); h0 = st.rfind("<div class='abs' style='", 0, k)
        st = st[:h0] + "<svg class='abs' data-deco='tufts' style='left:0;top:0' width='390' height='844' viewBox='0 0 390 844'>" + ''.join(PV.tuft(x, y) for x, y in TUFTS[name]) + '</svg>' + st[h0:]
    return st, ui
def ui_at(name, w, h):   # the phone's own HUD + ask card (390 and 375 from the 390 code at that size; 320 from the approved 320 code)
    if (w, h) == (320, 568): return UI320[name]
    sv = (PV.W, PV.H, g['W'], g['H'])
    PV.W, PV.H, g['W'], g['H'] = w, h, w, h
    try: return split(SCENES[name]())[1]
    finally: PV.W, PV.H, g['W'], g['H'] = sv
PARCH = '#F6E9C8'
CHIP = re.compile(r"<div class='abs' style='left:8px;top:([0-9.]+)px;border-radius:10px;background:rgba\(255,248,225,\.92\);border:2px solid (#[0-9A-F]{6});padding:0 10px;display:flex;gap:8px;align-items:center'>.*?</div></div>")
LABEL = re.compile(r"<div class='abs' style='left:[0-9.]+px;top:150px;width:180px;z-index:4'><div data-txt=1 style='background:(#[0-9A-F]{6});[^']*'>(<div class='e15 nw'[^>]*>[^<]*</div>)(<div class='t17 nw'[^>]*>[^<]*</div>)</div><div style='height:14px;[^']*'><div style='height:100%;width:([0-9]+)%;[^']*'></div></div></div>")
def guardian_on_hud(ui):
    """S3 (7:01 PM steering): the guardian label goes on the HUD's chip line, above both heroes, at every phone size (render only).
    One plate in the guardian tint, en and th on one line, the health bar as a 6 px strip under it; the zone chip makes way on this screen."""
    m = LABEL.search(ui)
    if not m: return ui
    c = CHIP.search(ui); assert c, 'zone chip not found'
    tint, en, th, frac = m.group(1), m.group(2), m.group(3), m.group(4)
    plate = (f"<div class='abs' data-guardian-hud=1 style='left:8px;right:8px;top:{c.group(1)}px;z-index:4'>"
             f"<div data-txt=1 style='background:{tint};border:2px solid #10170F;border-radius:10px 10px 0 0;padding:0 10px;display:flex;gap:8px;align-items:center;justify-content:center'>"
             f"<i style='width:12px;height:12px;border-radius:50%;background:{c.group(2)};border:2px solid #10170F'></i>{en}{th}</div>"
             f"<div style='height:6px;border:2px solid #10170F;border-top:0;border-radius:0 0 8px 8px;background:#E4DCC8;overflow:hidden'><div style='height:100%;width:{frac}%;background:{tint}'></div></div></div>")
    ui = ui[:m.start()] + ui[m.end():]
    return ui[:c.start()] + plate + ui[c.end():]
def compose(name, stage, ui, w, h, fit=None, ink=None):
    """fit = (s, ox, oy). ink: list of data-ink ids to leave visible (others hidden) for the ink diff; None = normal page."""
    s, ox, oy = fit
    st = stage.replace("data-tap=1 role='button' ", "data-hit=1 ").replace("data-tap='1' role='button' ", "data-hit=1 ")
    # word plates (D): UI at the phone's size, bottom-centre on the basket top they sit on
    tags = ''
    for m in re.finditer(r"<i data-tagph='([^']+)' data-x='([0-9.]+)' data-y='([0-9.]+)' data-w='([0-9.]+)'></i>", st):
        en, x, y, tw = m.group(1), *map(float, m.groups()[1:])
        bx, by = ox + s*(x + tw/2), oy + s*(y + 56); pw, ph = (88, 48) if w == 320 else (tw, 56)
        tags += f"<div class='abs' data-anchor-ui='{en}' style='left:{bx - pw/2:.1f}px;top:{by - ph:.1f}px;z-index:3'>" + PV.fr(None, None, pw, ph, '<div style=text-align:center>' + PV.tx(en, 'e17 nw') + '</div>', 'gs6', face='#F6E9C8', tap=True, st=(), name='tag-' + en) + '</div>'
    # unscaled hit areas for the scaled props: 44 pt or the prop's own size, centred on it
    hits = ''
    for m in re.finditer(r"<div class='abs' data-hit=1 data-name='([^']+)'[^>]*style='left:(-?[0-9.]+)px;top:(-?[0-9.]+)px;width:([0-9.]+)px;height:([0-9.]+)px", st):
        n, x, y, ew, eh = m.group(1), *map(float, m.groups()[1:])
        cx, cy = ox + s*(x + ew/2), oy + s*(y + eh/2); hw, hh = max(44, s*ew), max(44, s*eh)
        hits += f"<div class='abs' data-tap=1 role='button' data-name='{n}' aria-label='{n}' style='left:{cx - hw/2:.1f}px;top:{cy - hh/2:.1f}px;width:{hw:.1f}px;height:{hh:.1f}px;z-index:2'></div>"
    st = re.sub(r"(<div class='abs' data-hit=1 )data-name='([^']+)'", r"\1data-pn='\2'", st)
    hide = ''
    if ink is not None:
        hide = "<style>[data-ui],[data-ui] *,[data-anchor-ui],[data-anchor-ui] *,body>[data-tap]{visibility:hidden!important}[data-ink]{visibility:hidden!important}" + ''.join(f"[data-ink='{k}']{{visibility:visible!important}}" for k in ink) + "</style>"
    ui = guardian_on_hud(ui)
    world = (f"<div class='abs' data-st='{name}' style='left:{ox:.2f}px;top:{oy:.2f}px;width:{DW}px;height:{DH}px;overflow:hidden;"
             f"transform:scale({s:.5f});transform-origin:0 0'>{st}</div>")
    body = (hide + f"<div class='abs' style='left:0;top:0;width:{w}px;height:{h}px;background:{PARCH}'></div>" + world + hits + tags +
            f"<div class='abs' data-ui=1 style='left:0;top:0;width:{w}px;height:{h}px;pointer-events:none'><div style='pointer-events:auto'>{ui}</div></div>")
    doc = PV.page(w, h, body)
    if os.environ.get('NAE_R2TP') == '1':   # round 2 P1 (t440u) staged tapPrompt, render only
        doc = re.sub(r'Where is the ([a-z]+)\?', r'Can you find the \1?', doc); doc = re.sub(r'([a-z]+) อยู่ที่ไหน', r'หา \1 เจอไหม', doc)
    return doc
def tag_ink(stage, name):   # mark each anchored prop (and every other named prop) with data-ink=<key#nth>
    keys = []
    for key in sorted({a[0] for a in ANCH.get(name, [])} | set(re.findall(r"data-(?:name|pn)='([^']+)'", stage[:stage.find(MARK)] if MARK in stage else stage))):
        if key.startswith('tag-'): continue
        for i, m in reversed(list(enumerate(els(stage, key)))):
            stage = stage[:m.start()] + m.group(0).replace("<div class='abs'", f"<div class='abs' data-ink='{key}#{i}'", 1) + stage[m.end():]
            keys.append(f'{key}#{i}')
    return stage, sorted(set(keys))
def inkboxes(name, stage, ui, w, h, fit, keys):
    """ink box of each prop in phone CSS px: screenshot with all props hidden vs with only that prop shown (2x), bbox of the changed pixels"""
    from PIL import Image, ImageChops
    d = tempfile.mkdtemp(prefix='stgi-', dir='/tmp')
    try:
        jobs = [('base', [])] + [(k, [k]) for k in keys]
        def one(j):
            k, vis = j; p = f"{d}/{abs(hash(k))}.png"; shot(compose(name, stage, ui, w, h, fit, ink=vis), p, w, h); return k, p
        with CF.ThreadPoolExecutor(6) as ex: res = dict(ex.map(one, jobs))
        b = Image.open(res['base']).convert('RGB'); out = {}
        for k in keys:
            df = ImageChops.difference(Image.open(res[k]).convert('RGB'), b).convert('L').point(lambda v: 255 if v > 24 else 0)
            bb = df.getbbox(); out[k] = [v / 2 for v in bb] if bb else None
        return out
    finally: shutil.rmtree(d, ignore_errors=True)
def fit_for(meas390, meas, w, h):
    card0, st0 = meas390['card'], meas390['st']; top, card = meas['top'] + 6, meas['card']
    s = min(w / DW, 1.0)   # D2 (7:01 PM steering): fit to the width, bottom pinned to the card, the sky crops under the HUD
    return s, 0.0, card - card0*s
DECO = """<script>addEventListener('load',()=>{let t=1e9;for(const e of document.querySelectorAll('[data-st] [data-deco],[data-st] [data-pn],[data-st] [data-hero]')){const r=e.getBoundingClientRect();if(r.height&&r.bottom<=%C%)t=Math.min(t,r.top)}
const p=document.createElement('pre');p.id='bbout';p.textContent=JSON.stringify({top:t});document.body.appendChild(p)})</script>"""
def scenery_top(doc, card0):   # top of the drawn scenery (swing set, trees, walker, heroes) in the 390 design box, s = 1
    d = tempfile.mkdtemp(prefix='stgd-', dir='/tmp'); p = d + '/m.html'; open(p, 'w').write(doc.replace('</body>', DECO.replace('%C%', str(card0)) + '</body>'))
    try: o = run_chrome(['--window-size=390,844', '--dump-dom', 'file://' + p]).stdout
    finally: shutil.rmtree(d, ignore_errors=True)
    import html as H_; return json.loads(H_.unescape(re.search(r'<pre id="bbout">(.*?)</pre>', o, re.S).group(1)))['top']
WHOLE = {'W24-walk-B'}   # Maxwell t445u (Watchman 8:26 PM MDT): the walk scene shrinks at 320/375 so all its scenery sits below the Guardian banner, as at 390
def fit_whole(meas390, meas, w, h, top0):
    card0, top, card = meas390['card'], meas['top'] + 6, meas['card']; s = min(w / DW, 1.0)
    if card0 - top0 > 0: s = min(s, (card - top) / (card0 - top0))
    return s, (w - DW * s) / 2, card - card0 * s
TAPRE = re.compile(r"data-(?:tap=1 role='button'|hit=1) data-(?:name|pn)='([^']+)'[^>]*?style='left:(-?[0-9.]+)px;top:(-?[0-9.]+)px;width:([0-9.]+)px;height:([0-9.]+)px")
def fit_capped(scene, meas390, meas, w, h):   # round2b B (Maxwell t445u, Auditor 48295eae): fit the width, but the crop never puts a target under the HUD
    """(the scene shrinks to fit instead) and targets keep 16 pt from the screen edge; bottom pinned to the card, centred (parchment at the sides)"""
    card0, top, card = meas390['card'], meas['top'] + 6, meas['card']; s = min(w / DW, 1.0)
    taps = [(float(x), float(y), float(a), float(b)) for k, x, y, a, b in TAPRE.findall(scene)]
    sky = min([y for x, y, a, b in taps if y + b <= card0] or [card0])
    if card0 - sky > 0: s = min(s, (card - top) / (card0 - sky))
    for x, y, a, b in taps:
        if x < DW / 2: s = min(s, (w / 2 - 16) / (DW / 2 - x))
        if x + a > DW / 2: s = min(s, (w / 2 - 16) / (x + a - DW / 2))
    return s, (w - DW * s) / 2, card - card0 * s
def anchor_target(name, a):
    key, nth, mode, ax, ay, what = a
    if ay is None: ay = round(PV.grass_y(ax, 390, 420) + 3, 1)
    return ax, ay
def fit_stage(name, stage, ui):
    """move each anchored prop so its measured ink sits on its anchor (design box, s = 1); two passes"""
    log = []
    for it in range(2):
        st2, keys = tag_ink(stage, name)
        want = [f'{a[0]}#{a[1]}' for a in ANCH.get(name, [])]
        ib = inkboxes(name, st2, ui, DW, DH, (1, 0, 0), want)
        for a in ANCH.get(name, []):
            k = f'{a[0]}#{a[1]}'; x0, y0, x1, y1 = ib[k]; ax, ay = anchor_target(name, a)
            if a[2] == 'hang': dx, dy = ax - (x0 + .72*(x1 - x0)), ay - y0   # the key's ring is at its top right (72% in)
            else: dx, dy = ax - (x0 + x1)/2, ay - y1
            if abs(dx) > .4 or abs(dy) > .4: stage = shift(stage, a[0], a[1], round(dx, 1), round(dy, 1))
            log.append((it, k, [round(v, 1) for v in ib[k]], round(dx, 1), round(dy, 1)))
    return stage, log
def check(name, stage, ui, w, h, fit, meas, ref):
    global CARD390, HB390
    """every anchored prop touches its anchor (within 1.5 px), no prop above the ceiling, past an edge, under the HUD or into the card;
       every other prop keeps its design place (scaled) within 1.5 px"""
    s, ox, oy = fit
    st2, keys = tag_ink(stage, name)
    ib = inkboxes(name, st2, ui, w, h, fit, keys)
    TAPS = set(re.findall(r"data-tap=1 role='button' data-name='([^']+)'", stage))
    rows, bad = [], 0
    T = lambda x, y: (ox + s*x, oy + s*y)
    an = {f'{a[0]}#{a[1]}': a for a in ANCH.get(name, [])}
    for k in keys:
        b = ib[k]
        if not b: rows.append((k, 'NO INK', 'FAIL')); bad += 1; continue
        x0, y0, x1, y1 = b; msg = []; ok = True
        if k in an:
            a = an[k]; ax, ay = T(*anchor_target(name, a))
            gap = (y0 - ay) if a[2] == 'hang' else (ay - y1)
            inside = x0 - 1 <= ax <= x1 + 1
            ok &= abs(gap) <= 1.5 and inside; msg.append(f"{a[2]} {a[5]}: gap {gap:+.1f} px, anchor x {'inside' if inside else 'OUTSIDE'} ink")
        elif k in ref:
            rx0, ry0, rx1, ry1 = ref[k]; (ex0, ey0), (ex1, ey1) = T(rx0, ry0), T(rx1, ry1)
            dd = max(abs(ex0 - x0), abs(ey1 - y1), abs(ex1 - x1)); ok &= dd <= 1.5 + 2*(1 - s); msg.append(f"keeps its design place: off by {dd:.1f} px")
        lim_l, lim_r = max(0, ox) + 2, min(w, ox + DW*s) - 2
        if x0 < lim_l or x1 > lim_r: ok = False; msg.append('past the edge')
        if y0 < meas['top'] - 1: ok = False; msg.append(f'under the HUD ({y0:.0f} < {meas["top"]:.0f})')
        if name in CEIL and y0 < T(0, CEIL[name])[1] + 1: ok = False; msg.append('into the ceiling')
        if y1 > meas['card'] + 1:   # a target, or anything the 390 design shows whole (cows to count), must stay fully in view; scenery may sit behind the card
            if k.split('#')[0] in TAPS or (k in ref and ref[k][3] <= CARD390 + 1): ok = False; msg.append('runs into the card')
            else: msg.append('scenery, partly behind the card (as at 390)')
        rows.append((k, f'ink {x0:.1f},{y0:.1f}-{x1:.1f},{y1:.1f}; ' + '; '.join(msg), 'ok' if ok else 'FAIL')); bad += (not ok)
    hb_ok = meas['hb'] <= meas['card'] + 1 or meas['hb'] - meas['card'] <= s*(HB390 - CARD390) + 1.5
    rows.append(('hero', f"feet/bottom {meas['hb']:.1f}, card top {meas['card']:.1f}", 'ok' if hb_ok else 'FAIL')); bad += (not hb_ok)
    return rows, bad
if __name__ == '__main__':
    mode = ARGV[0] if ARGV else 'build'
    only = ARGV[1:]
    os.makedirs(OUT + 'html', exist_ok=True); os.makedirs(OUT + 'png', exist_ok=True)
    r = subprocess.run([sys.executable, __file__], env=dict(os.environ, NAE_SE='1'), capture_output=True, text=True)
    assert r.returncode == 0, r.stderr[-2000:]
    UI320 = json.load(open('/tmp/stage_ui320.json')); os.remove('/tmp/stage_ui320.json')
    report = ['# Scene stage check (stage_v608.py)', '', 'One design box (390x844) per scene, scaled as one piece; HUD and card at the phone size. Sizes: ' + ', '.join(f'{a}x{b}' for a, b in SIZES), '']
    fits = {}; total_bad = 0
    for name in SCENES:
        if only and name[0] not in only: continue
        stage, ui390 = stage_of(name)
        stage, log = fit_stage(name, stage, ui390)
        report.append(f'## {name}')
        for it, k, b, dx, dy in log: report.append(f'- fit pass {it + 1}: {k} ink {b} moved {dx:+.1f}, {dy:+.1f} pt')
        st2, keys = tag_ink(stage, name); ref = inkboxes(name, st2, ui390, DW, DH, (1, 0, 0), keys)
        m390 = measure(compose(name, stage, ui390, DW, DH, (1, 0, 0)), DW, DH)
        CARD390, HB390 = m390['card'], m390['hb']
        top0 = scenery_top(compose(name, stage, ui390, DW, DH, (1, 0, 0)), m390['card']) if name in WHOLE else None
        if top0 is not None: report.append(f'- scenery top (swing set, trees, walker, heroes) at 390: {top0:.1f} pt; 320/375 shrink so it clears the banner')
        for w, h in SIZES:
            ui = ui390 if (w, h) == (DW, DH) else ui_at(name, w, h)
            m = measure(compose(name, stage, ui, w, h, (1, 0, 0)), w, h)
            fit = (1, 0, 0) if (w, h) == (DW, DH) else (fit_whole(m390, m, w, h, top0) if name in WHOLE else fit_for(m390, m, w, h))
            doc = compose(name, stage, ui, w, h, fit); f = f'{name}-{w}x{h}'
            open(OUT + f'html/{f}.html', 'w').write(doc); shot(doc, OUT + f'png/{f}.png', w, h)
            m['hb'] = measure(doc, w, h)['hb']   # the hero as placed by the fit
            rows, bad = check(name, stage, ui, w, h, fit, m, ref); total_bad += bad
            report.append(f'### {w}x{h}: scale {fit[0]:.3f}, offset {fit[1]:.1f}, {fit[2]:.1f}; HUD bottom {m["top"]:.0f}, card top {m["card"]:.0f}: {"PASS" if not bad else f"{bad} FAIL"}')
            report += [f'- {k}: {t} [{o}]' for k, t, o in rows]
            print(f, 'scale %.3f' % fit[0], 'PASS' if not bad else f'{bad} FAIL', flush=True)
        report.append('')
    report.append(f'TOTAL FAIL: {total_bad}')
    open(OUT + ('CHECK.md' if not only else 'CHECK-partial.md'), 'w').write('\n'.join(report) + '\n'); print('TOTAL FAIL', total_bad)
