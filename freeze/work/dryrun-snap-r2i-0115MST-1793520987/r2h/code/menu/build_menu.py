# r2h main-menu concepts M1/M2/M3 and the extended Adventure Map (Maxwell t487u/t504u/t505u, pt505u), 390x844 and 320x568.
# Built from pieces of the approved map render (parts.py), so frames, plates, heroes and art match the map's look. Text: existing uiText only.
import re, sys, os
sys.path.insert(0, os.path.dirname(__file__)); import parts as P
OUT = '/workspace/v608build/r2h-rerun-stage/r2h/html/'   # stage-only edit (1:36 AM: only r2h-rerun-stage); round2/r2h copy not changed
U = dict(gear=('Gear', 'อุปกรณ์'), shop=('Shop', 'ร้านดาวทอง'), map=('Adventure Map', 'แผนที่ผจญภัย'), choose=('Choose your hero', 'เลือกฮีโร่ของคุณ'), greet=('Good morning!', 'สวัสดีตอนเช้า!'))
STUDS = "<i class='stud' style='top:2px;left:2px'><b></b></i><i class='stud' style='top:2px;right:2px'><b></b></i><i class='stud' style='bottom:2px;left:2px'><b></b></i><i class='stud' style='bottom:2px;right:2px'><b></b></i>"
def place(h, x, y, w=None, hh=None):   # move/resize the OUTER element only
    m = re.search(r"style='([^']*)'", h); st = m.group(1)
    st = re.sub(r'left:[-\d.]+px', f'left:{x}px', st, 1); st = re.sub(r'top:[-\d.]+px', f'top:{y}px', st, 1)
    if w is not None: st = re.sub(r'width:[-\d.]+px', f'width:{w}px', st, 1)
    if hh is not None: st = re.sub(r'height:[-\d.]+px', f'height:{hh}px', st, 1)
    return h[:m.start(1)] + st + h[m.end(1):]
def frame(bb, x, y, w, h, inner, face='#F6E9C8', tap=False, cls='f9', extra=''):
    t = " data-tap=1 role=button" if tap else ''
    return (f"<div class='{cls}' data-bb='{bb}'{t} style='left:{x}px;top:{y}px;width:{w}px;height:{h}px;{extra}'>{STUDS}<div class='r'>"
            f"<div class='face' data-bb='{bb}-inner' style='background:{face};display:flex;align-items:center;justify-content:center;position:relative'>{inner}</div></div></div>")
def label(en, th, align='center', size=20): return (f"<div style='text-align:{align}'><div class='en' data-txt=1 style='font-size:{size}px'>{en}</div><div class='th' data-txt=1>{th}</div></div>")
ICON = {   # small emblems drawn for the menu (originals; same stroke rules as the map dots)
 'gear': "<svg width='40' height='40' viewBox='-20 -20 40 40' stroke='#10170F' stroke-linejoin='round' stroke-linecap='round' fill='none'><path d='M-2-16h4v20h-4z' fill='#C9D1D8' stroke-width='2'/><path d='M-9 4h18v4h-18z' fill='#E8B84A' stroke-width='2'/><path d='M-2 8h4v8h-4z' fill='#8A5A34' stroke-width='2'/></svg>",
 'shop': "<svg width='40' height='40' viewBox='-20 -20 40 40' stroke='#10170F' stroke-linejoin='round' stroke-linecap='round' fill='none'><path d='M0-15l4.4 9 9.9 1.4-7.2 7 1.7 9.8L0 7.6l-8.8 4.6 1.7-9.8-7.2-7 9.9-1.4z' fill='#FFCC33' stroke-width='2'/></svg>",
 'map': "<svg width='40' height='40' viewBox='-20 -20 40 40' stroke='#10170F' stroke-linejoin='round' stroke-linecap='round' fill='none'><path d='M-14-10l9-4 10 4 9-4v24l-9 4-10-4-9 4z' fill='#F6E9C8' stroke-width='2'/><path d='M-5-14v24M5-10v24' stroke-width='1.5'/><path d='M-10 2q6-8 18-4' stroke='#A3211A' stroke-width='1.8' stroke-dasharray='3 3'/></svg>"}
def dot(x, y, kind, bg):
    return (f"<div data-bb='dot-{kind}' style='position:absolute;left:{x}px;top:{y}px;width:44px;height:44px;box-sizing:border-box;border-radius:50%;border:2px solid #10170F;background:{bg};"
            f"box-shadow:inset 0 0 0 3px #E8B84A,inset 0 0 0 4px #10170F;overflow:hidden'>{ICON[kind]}</div>")
ARROW = "<svg width='44' height='28' viewBox='0 0 44 28'><path d='M2 9h24V2l16 12-16 12v-7H2z' fill='#FFCC33' stroke='#10170F' stroke-width='3' stroke-linejoin='round'/></svg>"
def button(kind, x, y, w, h=72, cue=False):
    en, th = U[kind]; ic = f"<div style='position:absolute;left:8px;top:50%;margin-top:-20px'>{ICON[kind]}</div>"
    cu = f"<div data-bb='cue' style='position:absolute;right:8px;top:50%;margin-top:-14px;width:44px;height:28px'>{ARROW}</div>" if cue else ''
    inner = ic + f"<div style='position:absolute;left:58px;top:50%;transform:translateY(-50%);white-space:nowrap'><div class='en' data-txt=1>{en}</div><div class='th' data-txt=1>{th}</div></div>" + cu
    return frame(f'btn-{kind}', x, y, w, h, inner, tap=True)
def hearth(x, y, s=44):
    return (f"<div data-tap=1 role=button data-name='hearth' aria-label='A gift for you' style='position:absolute;left:{x}px;top:{y}px;width:{s}px;height:{s}px;box-sizing:border-box;border-radius:50%;background:#F6E9C8;border:3px solid #10170F;box-shadow:inset 0 0 0 3px #E8B84A,0 3px 0 #10170F;display:flex;align-items:center;justify-content:center'>"
            "<svg width='26' height='26' viewBox='-13 -13 26 26'><path d='M-10 10v-9a10 10 0 0 1 20 0v9z' fill='#8E959C' stroke='#10170F' stroke-width='2'/><path d='M0 6c-6-4-7-8-4-10 2-1 3 0 4 2 1-2 2-3 4-2 3 2 2 6-4 10z' fill='#FFCC33' stroke='#10170F' stroke-width='1.6'/></svg></div>")
def topbar(W, y, h, back=True, hearth_slot=False):
    if W == 390: bw, sw, lw = 84, 150, 108
    else: bw, sw, lw = 64, 120, 88
    x = 16; out = ''
    if back: out += place(P.el('back'), x, y, bw, h); x += bw + 8
    else: sw += bw + 8
    if hearth_slot: sw -= 52; out += hearth(W - 16 - 44, y + (h - 44) // 2); lw0 = lw
    if hearth_slot: x0 = x; out += place(P.el('stats'), x, y, sw, h) + place(P.el('level'), x + sw + 8, y, lw, h); return out
    out += place(P.el('stats'), x, y, sw, h); x += sw + 8
    out += place(P.el('level'), x, y, lw, h)
    return out
def banner(W, y, h, en, th): return place(re.sub(r"<div class='en' data-txt=1>[^<]*</div><div class='th' data-txt=1>[^<]*</div>", f"<div class='en' data-txt=1>{en}</div><div class='th' data-txt=1>{th}</div>", P.el('banner')), 16, y, W - 32, h)
def sheet(bb, x, y, w, h): return frame(bb, x, y, w, h, '', face='transparent', extra='background:transparent;box-shadow:inset 0 0 0 3px #8E959C,inset 1px 1px 0 #B9BFC5,0 3px 0 #10170F;').replace("background:transparent;display:flex", "background:transparent;box-shadow:inset 0 0 0 3px #E8B84A,inset 1px 1px 0 #FFE08A,inset 0 0 0 4px #10170F;border:0;display:flex")
ART_BODY = re.search(r"<g clip-path='url\(#([^)]+)\)'>(.*)</g></svg>$", P.ART, re.S)
def art_window(x, y, w, h, dx, dy, show_guardians=True):   # the map's sky sheet art, shown in a window (no scaling): art point (ax, ay) lands at (ax+dx, ay+dy)
    sky = P.ART[:P.ART.index('<clipPath')] if '<clipPath' in P.ART else ''
    body = re.sub(r"<path d='M55 322V592'[^>]*/>", '', ART_BODY.group(2))
    s = (f"<div style='position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;overflow:hidden;border-radius:6px'>"
         f"<svg xmlns='http://www.w3.org/2000/svg' width='{w}' height='{h}' viewBox='{-dx + x} {-dy + y} {w} {h}' stroke='#10170F' stroke-width='3' stroke-linejoin='round' stroke-linecap='round' fill='none' style='display:block'>"
         f"<rect x='-500' y='-500' width='1500' height='2000' fill='url(#skm)' stroke='none'/><defs><linearGradient id='skm' x2='0' y2='1'><stop stop-color='#3D8FE6'/><stop offset='.5' stop-color='#9FD0F5'/><stop offset='1' stop-color='#FFF1C9'/></linearGradient></defs>{body}")
    if show_guardians: s += re.search(r"<g clip-path='url\(#wc\)'>(.*)</g></svg>$", P.WASH, re.S).group(1)
    return s + '</svg></div>'
def hero_band(W, x, y, w, h, compact=False, big=False):
    sam, nan = P.el('btn-sam'), P.el('btn-nancy')
    i = P.D.find("left:25px;top:672px;width:340px;height:155px"); s0 = P.D.rfind('<div', 0, i); band_art = P.D[s0:P.div_end(P.D, s0)]
    lab = P.D[P.D.rfind('<div', 0, P.D.find("data-bb='t-choose'")):]; lab = lab[:P.div_end(lab, 0)]
    out = sheet('band', x, y, w, h)
    if not compact:   # 390: the approved band, moved as one piece (art, label, cards, sword)
        dy = y + 9 - 672 + 0; ax = x + 9
        out += place(band_art, ax, y + 9, w - 18, h - 18).replace("viewBox='25 672 340 155'", f"viewBox='25 672 {w-18} {h-18}'").replace("width='340' height='155'", f"width='{w-18}' height='{h-18}'", 1)
        out += lab.replace('top:680px', f'top:{y + 17}px')
        cw, ch = 126, 100; cy = y + h - 9 - ch - 8
        if big:   # M2: taller band, art zoomed (slice), hero cards 126x170 with the figure 1.5x over the name
            out = out.replace(f"viewBox='25 672 {w-18} {h-18}'", f"viewBox='25 672 340 155' preserveAspectRatio='xMidYMax slice'")
            cw, ch = 124, 172; cy = y + h - 9 - ch - 10
            def bigc(c):
                c = re.sub(r"(data-fig='[a-z]+' style='left:)[\d.]+px;top:[\d.]+px;([^']*?)transform:scale\(1\.0000\)", r"\g<1>32.8px;top:4px;\2transform:scale(1.3);transform-origin:0 0", c)
                c = re.sub(r"<svg style='position:absolute;left:0.0px;top:68.8px'", "<svg style='position:absolute;left:31.5px;top:86px'", c)
                return re.sub(r"left:47px;top:50%;transform:translateY\(-50%\)", "left:0;right:0;bottom:4px;text-align:center", c)
            sam, nan = bigc(sam), bigc(nan)
        out += place(sam, x + 17, cy, cw, ch) + place(nan, x + w - 17 - cw, cy, cw, ch)
    else:            # 320: compact hero strip, heroes 40 pt, no sword or rays (6.3 / t290u)
        out += place(band_art, x + 9, y + 9, w - 18, h - 18).replace("viewBox='25 672 340 155'", f"viewBox='60 672 {w-18} {h-18}'").replace("width='340' height='155'", f"width='{w-18}' height='{h-18}'", 1)
        out = re.sub(r"<g data-bb='sword'.*?</g></svg>", '</svg>', out, flags=re.S)
        out += lab.replace('top:680px', f'top:{y + 13}px')
        cw, ch = 128, 72; cy = y + h - 9 - ch - 8
        def compactc(c):
            c = re.sub(r"(data-fig='[a-z]+' style='left:)[\d.]+px;top:[\d.]+px;([^']*?)transform:scale\(1\.0000\)", r"\g<1>8px;top:6px;\2transform:scale(0.5714);transform-origin:0 0", c)
            return re.sub(r"left:47px;top:50%", "left:34px;top:50%", c)
        out += place(compactc(sam), x + 12, cy, cw, ch) + place(compactc(nan), x + w - 12 - cw, cy, cw, ch)
    return out
def page(W, H, body, title):
    return P.HEAD.rstrip() + P.BODY_OPEN + P.DEFS.replace("id='scr' style='position:relative;width:390px;height:844px;", f"id='scr' style='position:relative;width:{W}px;height:{H}px;") + f"<div style='position:relative;width:{W}px;height:{H}px;overflow:hidden;background:#24303A' data-page='{title}'>" + body + "</div></div></body></html>"
from flowers import FLOWER, tuft, FLOG, deflower   # t527u: five-petal circle flowers -> three-blade tufts (shared with fix_r2h)
def wr(name, doc): open(OUT + name + '.html', 'w').write(deflower(name, doc)); return name
names = []
SAFE = {390: 34, 320: 0}   # bottom inset kept clear of taps (home indicator at 390x844)
for W, H in ((390, 844), (320, 568)):
    c = W == 320; tag = f'{W}x{H}'; bot = H - SAFE[W] - 16
    bh, ty, th_ = (70, 84, 64) if c else (89, 109, 80); hdr = banner(W, 8 if c else 12, bh, *U["greet"])
    BAND = 140 if c else 173; BH = 72; btop = bot - (3 * BH + 2 * 8); hy = 8 if c else 12
    # ---------- M1: header and top bar, the hero band right under them, a scenery window, three stacked buttons ----------
    b = hdr + topbar(W, ty, th_, back=False, hearth_slot=True)
    by = ty + th_ + 8; b += hero_band(W, 16, by, W - 32, BAND, compact=c)
    sy = by + BAND + 8; sh = btop - 8 - sy
    if sh > 40: b += sheet('scene', 16, sy, W - 32, sh) + art_window(25, sy + 9, W - 50, sh - 18, -70 if c else 0, sy + sh - 9 - 376, show_guardians=False)
    for k, kind in enumerate(('gear', 'shop', 'map')): b += button(kind, 16, btop + k * (BH + 8), W - 32, BH, cue=(kind == 'map'))
    names.append(wr(f'M1-main-menu-{tag}', page(W, H, b, 'M1')))
    # ---------- M2: lower ceiling (no title log; top bar only), sky window, band low over the buttons ----------
    b = topbar(W, 8, th_, back=False, hearth_slot=True)
    B2 = BAND if c else 268; sy = 8 + th_ + 8; by = btop - 8 - B2; sh = by - 8 - sy
    if sh > 30: b += sheet('scene', 16, sy, W - 32, sh) + art_window(25, sy + 9, W - 50, sh - 18, -70 if c else 0, sy + sh - 9 - 330, show_guardians=False)
    b += hero_band(W, 16, by, W - 32, B2, compact=c, big=not c)
    for k, kind in enumerate(('gear', 'shop', 'map')): b += button(kind, 16, btop + k * (BH + 8), W - 32, BH, cue=(kind == 'map'))
    names.append(wr(f'M2-main-menu-{tag}', page(W, H, b, 'M2')))
    # ---------- M3: trail board: band, then a parchment board where Gear, Shop, Map are stops (dot + plate) on one dashed path ----------
    b = hdr + topbar(W, ty, th_, back=False, hearth_slot=True)
    rows_h = 3 * BH + 2 * 10; boardh = rows_h + 24; boy = bot + 16 - 8 - boardh if c else bot - boardh + 8
    by = boy - 8 - BAND; sy = ty + th_ + 8
    if by - 8 - sy > 40: b += sheet('scene', 16, sy, W - 32, by - 8 - sy) + art_window(25, sy + 9, W - 50, by - 8 - sy - 18, -70 if c else 0, by - 8 - 9 - 376, show_guardians=False)
    else: by = sy
    b += hero_band(W, 16, by, W - 32, BAND, compact=c)
    b += frame('board', 16, boy, W - 32, boardh, '', face='#EADBB4')
    px = 16 + (10 if c else 14); plx = px + 44 + (6 if c else 8); plw = W - 16 - (10 if c else 14) - plx; r0 = boy + 12
    b += f"<svg style='position:absolute;left:0;top:0' width='{W}' height='{H}'><path d='M{px+22} {r0+BH//2}V{r0+2*(BH+10)+BH//2}' stroke='#10170F' stroke-width='4' stroke-dasharray='8 6' fill='none'/></svg>"
    for k, (kind, bg) in enumerate((('gear', '#C9D1D8'), ('shop', '#FFE08A'), ('map', '#5DBB63'))):
        yy = r0 + k * (BH + 10); b += dot(px, yy + (BH - 44) // 2, kind, bg)
        en, th = U[kind]; cue = f"<div data-bb='cue' style='position:absolute;right:6px;top:50%;margin-top:-14px;width:44px;height:28px'>{ARROW}</div>" if kind == 'map' else ''
        b += frame(f'btn-{kind}', plx, yy, plw, BH, f"<div style='position:absolute;left:8px;top:50%;transform:translateY(-50%);white-space:nowrap'><div class='en' data-txt=1>{en}</div><div class='th' data-txt=1>{th}</div></div>" + cue, tap=True, cls='r9')
    names.append(wr(f'M3-main-menu-{tag}', page(W, H, b, 'M3')))
    # ---------- extended Adventure Map: hero select moved off, sheet down to the bottom, rows at the bottom ----------
    if not c:
        d = P.D
        for bb in ('strip', 'btn-sam', 'btn-nancy'): d = d.replace(P.el(bb, d), '')
        lab = d[d.rfind('<div', 0, d.find("data-bb='t-choose'")):]; d = d.replace(lab[:P.div_end(lab, 0)], '')
        i = d.find("left:25px;top:672px;width:340px;height:155px"); s0 = d.rfind('<div', 0, i); d = d[:s0] + d[P.div_end(d, s0):]
        DY = 172; d = d.replace("data-bb='sheet' style='left:16px;top:197px;width:358px;height:458px;", "data-bb='sheet' style='left:16px;top:197px;width:358px;height:639px;")
        for k in range(4):
            for bb in (f'row{k}', f'dot{k}'):
                e = P.el(bb, d); m = re.search(r'top:([\d.]+)px', e); d = d.replace(e, e.replace(m.group(0), f'top:{float(m.group(1)) + DY:g}px', 1))
        d = d.replace("<rect x='25' y='206' width='340' height='440' rx='8'/>", "<rect x='25' y='206' width='340' height='621' rx='8'/>")
        for sv in re.findall(r"<g clip-path='url\(#[^)]+\)'>", d): d = d.replace(sv, sv + f"<g transform='translate(0 {DY})'>")
        d = re.sub(r"</g></svg>(?=<svg width='390' height='666')", "</g></g></svg>", d, 1)   # close the art translate
        d = d.replace("<svg width='390' height='666' style='position:absolute;left:0;top:0' fill='none'>", "<svg width='390' height='844' style='position:absolute;left:0;top:0' fill='none'>")
        d = re.sub(r"(<svg width='390' height='844' style='position:absolute;left:0;top:0' fill='none'>.*?)</g></svg>", lambda m: m.group(1) + '</g></g></svg>', d, 1, flags=re.S)
        names.append(wr(f'map-extended-{tag}', d))
    else:
        b = banner(W, 8, bh, *U['map']) + topbar(W, ty, th_, back=True); sy = ty + th_ + 8; b += sheet('sheet', 16, sy, W - 32, H - 8 - sy)
        rows_top = H - 8 - 9 - 12 - (4 * 82 + 3 * 8); b += art_window(25, sy + 9, W - 50, H - 8 - sy - 18, -70, rows_top - 286 + 4)
        b += f"<svg style='position:absolute;left:0;top:0' width='{W}' height='{H}'><path d='M48 {rows_top+41}V{rows_top+3*90+41}' stroke='#10170F' stroke-width='4' stroke-dasharray='8 8' fill='none'/></svg>"
        for k in range(4):
            y = rows_top + k * 90; b += place(P.el(f'dot{k}'), 26, y + 19) + place(P.el(f'row{k}'), 78, y, 210, 82)
        names.append(wr(f'map-extended-{tag}', page(W, H, b, 'map')))
print('\n'.join(names)); print('\n'.join(FLOG))
