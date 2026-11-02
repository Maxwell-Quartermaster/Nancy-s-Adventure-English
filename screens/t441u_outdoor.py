# t441u outdoor fixes, moved out of play_v608.py (Auditor S2, 7:03 PM MDT): applied ONLY inside the stage pipeline (new staged scenes),
# so screens approved at t385u keep their old backgrounds. Usage: import t441u_outdoor; t441u_outdoor.apply(P, Z)
def apply(P, Z):
    global grass_y, tuft
    _G = {'w': 390, 'y': 420}
    _ground0 = P.ground
    def _ground(w, y, c, far):   # also: the grass reaches the screen bottom (it stopped at y+400, so 820-844 showed sky under the card's corners at 390)
        _G.update(w=w, y=y); return _ground0(w, y, c, far).replace(f'V{y+400}H0z', f'V{y+700}H0z')
    P.ground = _ground
    def _qy(x, x0, y0, cx, cy, x1, y1):   # y on a quadratic bezier at x (bisection on t)
        lo, hi = 0.0, 1.0
        for _ in range(40):
            t = (lo + hi) / 2; xt = (1-t)**2*x0 + 2*t*(1-t)*cx + t*t*x1
            lo, hi = (t, hi) if xt < x else (lo, t)
        t = (lo + hi) / 2; return (1-t)**2*y0 + 2*t*(1-t)*cy + t*t*y1
    def grass_y(x, w=None, y=None):   # top of the grass at x: the higher of the far and near hills drawn by P.ground
        w = w or _G['w']; y = y or _G['y']; x = min(max(x, 0), w)
        def hill(x0y, c, p1, e):   # q c p1 then t e (reflected control)
            (x0, y0), (cx, cy), (x1, y1), (x2, y2) = x0y, c, p1, e
            if x <= x1: return _qy(x, x0, y0, cx, cy, x1, y1)
            return _qy(x, x1, y1, 2*x1 - cx, 2*y1 - cy, x2, y2)
        far = hill((0, y-30), (w*.3, y-70), (w*.6, y-50), (w, y-56)); near = hill((0, y), (w*.35, y-30), (w*.7, y-14), (w, y-10))
        return min(far, near)
    _tree0 = P.tree
    def _tree(x, yb, s, base):
        g = max(grass_y(x - 6*s), grass_y(x + 4*s)) + 3   # trunk spans x-6s .. x+4s; its foot sits 3 pt into the grass
        return _tree0(x, max(yb, round(g, 1)), s, base)
    P.tree = _tree
    def tuft(x, y, col='#0F3A14'):   # S1: #0F3A14 on grass #36A13D is about 3.9:1   # a miniature grass tuft (replaces the dot flowers and pebbles)
        return f"<path d='M{x-6} {y}q1-7 -2-10M{x-1} {y}q-1-9 1-14M{x+4} {y}q0-7 4-10' stroke='{col}' stroke-width='2.5' fill='none' stroke-linecap='round' data-deco='tuft'/>"
    _outdoor0 = Z.outdoor
    def _outdoor(w, h, key):
        o = _outdoor0(w, h, key)
        if key == 'meadow':
            c = w == 320
            for x, y, cc in ([(90, 440, '#FFE27A'), (300, 448, '#F2A0A8')] if c else [(110, 690, '#FFE27A'), (230, 680, '#FFF8E1'), (350, 660, '#F2A0A8')]):
                a = f"<circle cx='{x}' cy='{y}' r='3' fill='{cc}' stroke-width='1.5'/>"; assert o.count(a) == 1, a; o = o.replace(a, '')   # S1: the dots go; tufts are placed per scene on open grass above the card (stage_v608 TUFTS)
            a, b = (("<path d='M118 568q14-120 96-170' stroke='#E8D9A8' stroke-width='20' opacity='.85'/>", "<path d='M96 568q20-50 120-84' stroke='#E8D9A8' stroke-width='20' opacity='.85'/>") if c else
                    ("<path d='M140 844q20-140 120-250' stroke='#E8D9A8' stroke-width='26' opacity='.85'/>", "<path d='M118 844q26-70 170-128' stroke='#E8D9A8' stroke-width='26' opacity='.85'/>"))
            assert o.count(a) == 1; o = o.replace(a, b)
        return o
    Z.outdoor = _outdoor
    P.grass_y = grass_y; P.tuft = tuft
