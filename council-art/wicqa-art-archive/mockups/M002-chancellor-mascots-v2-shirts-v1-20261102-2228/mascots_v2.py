"""Council bot mascots v2 (t743u): our own inline SVG, no outside assets, no outside fonts.
Drop-in for mascots.py e738a6b7: same svg(name, state, mode, i, w) and inner(...) signatures,
same viewBox 0 0 80 108 with the desk, same CSS hooks (.bb .act .lid .arm) and SMIL / still modes.
Look: soft Play-Doh forms, radial-gradient shading, rim light, big eyes with highlights,
slight 3/4 turn, idle = gentle squash, working = stretch and lean toward the role prop.
Identity kept: QM blue cloud, Watchman orange pumpkin, Chancellor violet star + top hat,
Instructor green wedge, Auditor brown square.
mode: "css"  -> classes (.bb .act .lid .arm) animated by the page CSS
      "smil" -> SMIL <animate> children (for the private Page), "still" -> no animation at all.
"""
INK = "#2a1a3a"
ACTS = {  # role action, translate only (safe in Safari 14)
    "write": "0 0;-6 1;0 0;-3 -1;0 0", "sway": "0 0;3 0;0 0;-3 0;0 0", "toss": "0 0;0 -11;0 0",
    "page": "0 0;-9 0;-9 0;0 0", "sweep": "0 0;-9 0;0 0",
}
DUR = {"write": "1.1s", "sway": "1.6s", "toss": "1s", "page": "1.8s", "sweep": "1.8s"}

# main, light (key-lit side), dark (shadow side), rim, skin/face plate, iris
PAL = {
    "Quartermaster": dict(main="#3b82f6", light="#93c5fd", dark="#1e3a8a", rim="#dbeafe", hi="#ffffff", skin="#dcecff", skin_d="#8db6ee", iris="#1d4ed8"),
    "Watchman":      dict(main="#f97316", light="#fdba74", dark="#9a3412", rim="#ffedd5", hi="#ffd2a8", skin="#fb8a2e", skin_d="#b8410c", iris="#7c2d12"),
    "Chancellor":    dict(main="#8b5cf6", light="#c4b5fd", dark="#4c1d95", rim="#ede9fe", hi="#e4d9ff", skin="#a37efa", skin_d="#6025d0", iris="#5b21b6"),
    "Instructor":    dict(main="#22c55e", light="#86efac", dark="#14532d", rim="#dcfce7", hi="#f2fff6", skin="#a7f3c0", skin_d="#3fc46f", iris="#15803d"),
    "Auditor":       dict(main="#b45309", light="#e0a15a", dark="#5c2a06", rim="#fde7c7", hi="#f6c995", skin="#d4893f", skin_d="#8a3c0c", iris="#78350f"),
}
_n = [0]
_T = [False]  # tough shirt treatment for the current inner() call (shirts only; dashboard never sets it)

def _uid(name, state, i):
    _n[0] += 1
    return f"m{name[:2].lower()}{state[0]}{i}n{_n[0]}"

def _anim(mode, kind, state, extra=""):
    if mode != "smil" or state != "working":
        return ""
    return f'<animateTransform attributeName="transform" type="translate" values="{ACTS[kind]}" dur="{DUR[kind]}" repeatCount="indefinite"{extra}/>'

def _bob(mode, state):
    return '<animateTransform attributeName="transform" type="translate" values="0 0;0 -2;0 0" dur="2.4s" repeatCount="indefinite"/>' if mode == "smil" and state == "working" else ""

def _act(mode, kind, state, body):
    cls = f' class="act {kind}"' if mode == "css" else ""
    return f'<g{cls}>{_anim(mode, kind, state)}{body}</g>'

def _defs(u, p):
    """Shared gradients for one mascot instance (ids unique per call so many inline SVGs can share a page)."""
    if _T[0]:  # tough: hard cel-shaded steps instead of soft falloff
        b = f'<stop offset="0" stop-color="{p["light"]}"/><stop offset=".3" stop-color="{p["light"]}"/><stop offset=".3" stop-color="{p["main"]}"/><stop offset=".72" stop-color="{p["main"]}"/><stop offset=".72" stop-color="{p["dark"]}"/>'
        sk = f'<stop offset="0" stop-color="{p["hi"]}"/><stop offset=".22" stop-color="{p["hi"]}"/><stop offset=".22" stop-color="{p["skin"]}"/><stop offset=".7" stop-color="{p["skin"]}"/><stop offset=".7" stop-color="{p["skin_d"]}"/>'
    else:
        b = f'<stop offset="0" stop-color="{p["light"]}"/><stop offset=".55" stop-color="{p["main"]}"/><stop offset="1" stop-color="{p["dark"]}"/>'
        sk = f'<stop offset="0" stop-color="{p["hi"]}"/><stop offset=".45" stop-color="{p["skin"]}"/><stop offset="1" stop-color="{p["skin_d"]}"/>'
    return (f'<defs>'
            f'<radialGradient id="{u}b" cx="36%" cy="30%" r="75%">{b}</radialGradient>'
            f'<radialGradient id="{u}s" gradientUnits="userSpaceOnUse" cx="33" cy="19" r="36" fx="31" fy="16">{sk}</radialGradient>'
            f'<radialGradient id="{u}i" cx="45%" cy="35%" r="70%"><stop offset="0" stop-color="{p["light"]}"/><stop offset=".6" stop-color="{p["iris"]}"/><stop offset="1" stop-color="#140a1e"/></radialGradient>'
            f'<radialGradient id="{u}w" cx="40%" cy="30%" r="75%"><stop offset=".6" stop-color="#ffffff"/><stop offset="1" stop-color="#dfe3ee"/></radialGradient>'
            f'<radialGradient id="{u}h" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#000" stop-opacity=".55"/><stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient>'
            f'<radialGradient id="{u}k" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#ff7aa2" stop-opacity=".75"/><stop offset="1" stop-color="#ff7aa2" stop-opacity="0"/></radialGradient>'
            f'<linearGradient id="{u}d" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#d79a5c"/><stop offset="1" stop-color="#a0663a"/></linearGradient>'
            f'<linearGradient id="{u}f" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8f5a30"/><stop offset="1" stop-color="#5e3819"/></linearGradient>'
            f'<radialGradient id="{u}g" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#fff3b0" stop-opacity=".95"/><stop offset=".4" stop-color="#fcd34d" stop-opacity=".45"/><stop offset="1" stop-color="#fcd34d" stop-opacity="0"/></radialGradient>'
            f'<radialGradient id="{u}o" cx="35%" cy="30%" r="75%"><stop offset="0" stop-color="#fff7c2"/><stop offset=".5" stop-color="#facc15"/><stop offset="1" stop-color="#a16207"/></radialGradient>'
            f'</defs>')

def _eye(u, cx, cy, r, st, mode, i, lidfill, sx=1.0, look=(0, 0)):
    """Big Pixar-ish eye: shaded sclera, glossy iris, pupil, two highlights, upper lid line.
    sx < 1 narrows the far eye for the 3/4 turn."""
    rx, ry = r * sx, r * 1.12
    lx, ly = look
    ix, iy = cx + lx * r * 0.28 * sx, cy + ly * r * 0.3
    s = (f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx:.2f}" ry="{ry:.2f}" fill="url(#{u}w)"/>'
         f'<ellipse cx="{ix:.1f}" cy="{iy:.1f}" rx="{r*0.7*sx:.2f}" ry="{r*0.76:.2f}" fill="url(#{u}i)"/>'
         f'<ellipse cx="{ix:.1f}" cy="{iy+r*0.04:.1f}" rx="{r*0.38*sx:.2f}" ry="{r*0.42:.2f}" fill="#120818"/>'
         f'<circle cx="{ix-r*0.26*sx:.1f}" cy="{iy-r*0.3:.1f}" r="{r*0.27:.2f}" fill="#fff"/>'
         f'<circle cx="{ix+r*0.26*sx:.1f}" cy="{iy+r*0.26:.1f}" r="{r*0.12:.2f}" fill="#fff" opacity=".9"/>')
    if False:  # (v2a had a half lid on idle; read as sleepy/smug, removed)
        s += f'<path d="M{cx-rx-.3:.1f} {cy-ry*0.2:.1f}Q{cx:.1f} {cy-ry*1.35:.1f} {cx+rx+.3:.1f} {cy-ry*0.2:.1f}Q{cx:.1f} {cy-ry*0.72:.1f} {cx-rx-.3:.1f} {cy-ry*0.2:.1f}z" fill="{lidfill}"/>'
    s += f'<path d="M{cx-rx-.4:.1f} {cy-ry*0.35:.1f}Q{cx:.1f} {cy-ry*1.27:.1f} {cx+rx+.4:.1f} {cy-ry*0.35:.1f}" fill="none" stroke="{INK}" stroke-width="1.3" stroke-linecap="round"/>'
    a = ""
    if mode == "smil":
        dur = "4.2s" if st == "working" else "7s"
        a = f'<animate attributeName="opacity" values="0;0;1;0" keyTimes="0;0.9;0.94;1" dur="{dur}" begin="{i*0.7:.1f}s" repeatCount="indefinite"/>'
    cls = ' class="lid"' if mode == "css" else ""
    s += f'<ellipse{cls} cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx+.7:.2f}" ry="{ry+.7:.2f}" fill="{lidfill}" opacity="0">{a}</ellipse>'
    return s

def _face(u, cx, cy, r, gap, st, mode, i, lidfill, look, mouth_dy=None, brows=True, mood="smile"):
    """Two eyes with a 3/4 turn (face shifted toward the viewer's right, far eye narrower)."""
    e1, e2 = cx - gap, cx + gap
    s = _eye(u, e1, cy, r, st, mode, i, lidfill, 0.88, look) + _eye(u, e2, cy, r, st, mode, i, lidfill, 1.0, look)
    md = mouth_dy if mouth_dy is not None else r * 1.75
    my, mx = cy + md, cx + 1.2
    # cheeks (soft dashboard look only; the tough shirt version drops them)
    s += "" if _T[0] else (f'<ellipse cx="{e1-r*0.6:.1f}" cy="{cy+r*1.35:.1f}" rx="{r*0.75:.1f}" ry="{r*0.45:.1f}" fill="url(#{u}k)"/>'
          f'<ellipse cx="{e2+r*0.7:.1f}" cy="{cy+r*1.35:.1f}" rx="{r*0.85:.1f}" ry="{r*0.5:.1f}" fill="url(#{u}k)"/>')
    if _T[0]:
        by = cy - r * 1.12 - 1.2
        for e, sgn in ((e1, 1), (e2, -1)):  # straight, low, slight inward angle
            s += f'<path d="M{e-r*0.95:.1f} {by-sgn*0.9:.1f}L{e+r*0.95:.1f} {by+sgn*0.9:.1f}" stroke="{INK}" stroke-width="2.3" stroke-linecap="round"/>'
        for e, sx in ((e1, .88), (e2, 1.0)):  # steady upper lid
            rx, ry = r * sx, r * 1.12
            s += f'<path d="M{e-rx-.5:.1f} {cy-ry*0.15:.1f}Q{e:.1f} {cy-ry*1.4:.1f} {e+rx+.5:.1f} {cy-ry*0.15:.1f}Q{e:.1f} {cy-ry*0.55:.1f} {e-rx-.5:.1f} {cy-ry*0.15:.1f}z" fill="{lidfill}" stroke="{INK}" stroke-width="1.3"/>'
        s += f'<path d="M{mx-3.2:.1f} {my+.6:.1f}Q{mx+.5:.1f} {my+2.2:.1f} {mx+3.6:.1f} {my-1.2:.1f}" fill="none" stroke="{INK}" stroke-width="1.7" stroke-linecap="round"/>'
        return s
    if brows:
        by = cy - r * 1.12 - 2.2
        if st == "working":  # determined, inner ends down
            s += (f'<path d="M{e1-r*0.8:.1f} {by-1:.1f}Q{e1:.1f} {by-1.8:.1f} {e1+r*0.8:.1f} {by+.9:.1f}" fill="none" stroke="{INK}" stroke-width="1.7" stroke-linecap="round"/>'
                  f'<path d="M{e2-r*0.85:.1f} {by+.9:.1f}Q{e2:.1f} {by-1.8:.1f} {e2+r*0.85:.1f} {by-1:.1f}" fill="none" stroke="{INK}" stroke-width="1.7" stroke-linecap="round"/>')
        else:  # soft, lifted
            s += (f'<path d="M{e1-r*0.7:.1f} {by:.1f}Q{e1:.1f} {by-2.2:.1f} {e1+r*0.7:.1f} {by-.4:.1f}" fill="none" stroke="{INK}" stroke-width="1.4" stroke-linecap="round" opacity=".85"/>'
                  f'<path d="M{e2-r*0.75:.1f} {by-.4:.1f}Q{e2:.1f} {by-2.4:.1f} {e2+r*0.75:.1f} {by:.1f}" fill="none" stroke="{INK}" stroke-width="1.4" stroke-linecap="round" opacity=".85"/>')
    if st == "working":
        if mood == "hmm":  # Auditor: small pursed "o", checking
            s += f'<ellipse cx="{mx:.1f}" cy="{my+.6:.1f}" rx="1.6" ry="1.9" fill="#4a1022"/>'
        else:  # open, eager mouth with tongue
            s += (f'<path d="M{mx-3.6:.1f} {my-.4:.1f}Q{mx:.1f} {my+5.4:.1f} {mx+3.6:.1f} {my-.4:.1f}Q{mx:.1f} {my+.6:.1f} {mx-3.6:.1f} {my-.4:.1f}z" fill="#4a1022"/>'
                  f'<path d="M{mx-1.9:.1f} {my+2.5:.1f}Q{mx:.1f} {my+1.2:.1f} {mx+1.9:.1f} {my+2.5:.1f}Q{mx:.1f} {my+4.4:.1f} {mx-1.9:.1f} {my+2.5:.1f}z" fill="#ff7a9a"/>')
    else:
        s += f'<path d="M{mx-3:.1f} {my:.1f}Q{mx:.1f} {my+2.8:.1f} {mx+3:.1f} {my-.5:.1f}" fill="none" stroke="{INK}" stroke-width="1.5" stroke-linecap="round"/>'
    return s

def _arms(u, mode, state, pts):
    """Chunky Play-Doh arms (capsules); class arm l/r keeps the dashboard tap animation."""
    out = ""
    for k, (x, y, w, h) in enumerate(pts):
        cls = f' class="arm {"l" if k == 0 else "r"}"' if mode == "css" else ""
        a = f'<animateTransform attributeName="transform" type="translate" values="0 0;0 -2;0 0" dur="0.5s" begin="{k*0.25}s" repeatCount="indefinite"/>' if mode == "smil" and state == "working" else ""
        out += f'<rect{cls} x="{x}" y="{y}" width="{w}" height="{h}" rx="{w/2:.1f}" fill="url(#{u}b)">{a}</rect>'
    return out

def _star(cx, cy, R, r):
    import math
    pts = []
    for k in range(10):
        a = math.radians(-90 + 36 * k)
        rr = R if k % 2 == 0 else r
        pts.append(f"{cx + rr*math.cos(a):.1f},{cy + rr*math.sin(a):.1f}")
    return " ".join(pts)

def _desk(u):
    return (f'<g><ellipse cx="40" cy="105" rx="36" ry="2.6" fill="url(#{u}h)"/>'
            f'<rect x="9" y="76" width="8" height="28" rx="3" fill="url(#{u}f)"/><rect x="63" y="76" width="8" height="28" rx="3" fill="url(#{u}f)"/>'
            f'<rect x="8" y="76" width="64" height="8" rx="2.5" fill="#7a4a24"/>'
            f'<rect x="2.5" y="68.5" width="75" height="10" rx="4.5" fill="url(#{u}d)"/>'
            f'<rect x="4" y="69.2" width="72" height="1.6" rx=".8" fill="#f1c591" opacity=".7"/>'
            f'<path d="M9 73.5h18M33 75h15M55 73h15" stroke="#8a5a2f" stroke-width=".7" stroke-linecap="round" opacity=".55"/></g>')

def _plinth(u):
    return (f'<g><ellipse cx="40" cy="83" rx="36" ry="3" fill="url(#{u}h)"/>'
            '<rect x="4" y="68.5" width="72" height="12" rx="6" fill="#5b21b6"/>'
            '<rect x="4" y="68.5" width="72" height="7" rx="3.5" fill="#7c3aed"/>'
            '<rect x="7" y="69.3" width="66" height="1.5" rx=".75" fill="#c4b5fd" opacity=".7"/>'
            '<rect x="6" y="78.2" width="68" height="1.4" rx=".7" fill="#39ff14" opacity=".9"/></g>')

def _body(u, p, x=21, y=50, w=38, h=28):
    """Soft rounded bean torso, mostly behind the desk."""
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{w*0.42:.1f}" fill="url(#{u}b)"/>'
            f'<path d="M{x+w-4:.1f} {y+5}q4 6 3 16" fill="none" stroke="{p["rim"]}" stroke-width="1.4" stroke-linecap="round" opacity=".55"/>')

def _pose(st, lean):
    """Squash (idle) or stretch-and-lean (working) about the seat point (40, 74)."""
    if st == "working":
        return f"translate(40 74) rotate({lean}) scale(.965 1.035) translate(-40 -74)"
    return "translate(40 74) scale(1.05 .955) translate(-40 -74)"

def inner(name, state, mode="css", i=0, desk=True, bare=False, tough=False):
    """desk=False swaps the wooden desk for a soft purple plinth (shirt art); dashboard keeps the default.
    bare=True: neutral front-on figure only (no desk, props or lean), for the small shirt-front mark."""
    _T[0] = tough
    if bare:
        state = "idle"
    st = state if state in ("working", "idle") else "idle"
    name = name if name in PAL else "Auditor"
    p = PAL[name]
    u = _uid(name, st, i)
    look = (0.9, 0.75) if st == "working" else ((0, 0) if bare else (0.35, -0.05))
    lean = 3
    shadow = f'<ellipse cx="40" cy="70.5" rx="25" ry="3" fill="url(#{u}h)"/>'  # contact shadow on the desk top
    if name == "Quartermaster":  # cloud head (avatar: cloud/blue), shield chest, ledger + pen
        body = (_body(u, p)
                + f'<path d="M40 54.5l7.5 2.6v5c0 4.6-3.6 7.3-7.5 9.2-3.9-1.9-7.5-4.6-7.5-9.2v-5z" fill="#f4f8ff"/><path d="M40 57.5v10M35.5 61h9" stroke="{p["main"]}" stroke-width="1.8" stroke-linecap="round"/>'
                # cloud: puffs around a rounded core, one gradient
                + f'<g fill="url(#{u}s)"><circle cx="21" cy="33" r="9"/><circle cx="59" cy="33" r="9"/><circle cx="27" cy="20" r="9.5"/><circle cx="40" cy="15.5" r="10.5"/><circle cx="53" cy="20" r="9.5"/>'
                  f'<rect x="16" y="19" width="48" height="31" rx="15"/></g>'
                + f'<path d="M59 19q7 4 7 13" fill="none" stroke="#fff" stroke-width="1.6" stroke-linecap="round" opacity=".75"/>'
                + f'<ellipse cx="34" cy="13.5" rx="4.5" ry="2.2" fill="#fff" opacity=".7"/>'
                + _face(u, 41, 34, 6.2, 8.8, st, mode, i, p["skin"], look, mouth_dy=9.6))
        arms = _arms(u, mode, st, [(15, 57, 9, 15), (56, 57, 9, 15)])
        prop = ('<rect x="20" y="64.5" width="25" height="7.5" rx="1.5" fill="#f7efdc" stroke="#9a6a3a" stroke-width=".8"/><path d="M32.5 64.5v7.5" stroke="#9a6a3a" stroke-width=".8"/>'
                '<path d="M23 67h6.5M23 69.2h5M35.5 67h6.5" stroke="#9ca3af" stroke-width=".8" stroke-linecap="round"/>'
                + _act(mode, "write", st, '<path d="M50 58.5l-5.4 10.5" stroke="#facc15" stroke-width="2.8" stroke-linecap="round"/><path d="M44.6 69l-.7 1.7" stroke="#2a1a3a" stroke-width="1.3" stroke-linecap="round"/>'))
    elif name == "Watchman":  # pumpkin head (avatar: pumpkin/orange), lantern
        lean = 4
        body = (_body(u, dict(p, rim="#ffedd5"), 22, 51, 36, 27)
                + f'<path d="M30 55q10 5 20 0" fill="none" stroke="{p["dark"]}" stroke-width="2" stroke-linecap="round" opacity=".6"/>'
                + f'<path d="M40 14q-1-6 2-8.5" fill="none" stroke="#15803d" stroke-width="3.8" stroke-linecap="round"/><path d="M42 8.5q6-4 9.5 1q-5 0-7.5 3" fill="#22c55e"/>'
                # ribbed pumpkin: overlapping lobes under one light, creases between them
                + f'<g fill="url(#{u}s)"><ellipse cx="28" cy="32" rx="13" ry="17"/><ellipse cx="52" cy="32" rx="13" ry="17"/><ellipse cx="40" cy="31.5" rx="15" ry="18.5"/></g>'
                + f'<path d="M30.5 15.5q-6 16 0 32.5M49.5 15.5q6 16 0 32.5" fill="none" stroke="{p["dark"]}" stroke-width="1.5" stroke-linecap="round" opacity=".5"/>'
                + f'<path d="M58 19q7 6 6.5 17" fill="none" stroke="{p["rim"]}" stroke-width="1.6" stroke-linecap="round" opacity=".7"/>'
                + f'<ellipse cx="34" cy="19" rx="4.5" ry="2.2" fill="#fff" opacity=".45"/>'
                + _face(u, 41, 33, 6.0, 8.6, st, mode, i, p["skin"], look, mouth_dy=9.4))
        arms = _arms(u, mode, st, [(17, 57, 9, 15)])
        prop = _act(mode, "sway", st,
                    f'<circle cx="62" cy="59" r="11" fill="url(#{u}g)"/>'
                    '<path d="M55 46q7-5 14 0" fill="none" stroke="#64748b" stroke-width="1.6"/>'
                    '<rect x="56" y="50" width="12" height="2.6" rx="1.3" fill="#475569"/><rect x="57" y="52.5" width="10" height="13" rx="3" fill="#1f2937"/>'
                    '<rect x="58.8" y="54.3" width="6.4" height="9.4" rx="2" fill="#fde68a"/><ellipse cx="62" cy="60" rx="1.6" ry="2.4" fill="#fb923c"/>'
                    '<rect x="56" y="65" width="12" height="2.4" rx="1.2" fill="#475569"/>'
                    f'<rect x="50" y="53" width="9" height="13" rx="4.5" fill="url(#{u}b)"/>')
    elif name == "Chancellor":  # rounded star head (avatar: star/violet), top hat, monocle, coin toss
        lean = 3
        star = _star(40, 33, 22.5, 11.8)
        body = (_body(u, p)
                + '<path d="M40 50l-7.5 9 7.5 5 7.5-5z" fill="#f5f3ff"/><path d="M36.5 56.5l3.5 3 3.5-3-3.5-2z" fill="#db2777"/>'
                + '<path d="M28 61l1.4 2.8 3.1.5-2.3 2.1.6 3.1-2.8-1.5-2.8 1.5.6-3.1-2.3-2.1 3.1-.5z" fill="#facc15"/>'
                + f'<polygon points="{star}" fill="url(#{u}s)" stroke="url(#{u}s)" stroke-width="6" stroke-linejoin="round"/>'
                + f'<path d="M57 25q6 1 8 4" fill="none" stroke="#fff" stroke-width="1.5" stroke-linecap="round" opacity=".7"/>'
                # tipped top hat on the top point
                + f'<g transform="translate(0 1.5) rotate(-10 40 13)"><rect x="32" y="3.5" width="16" height="10" rx="2.5" fill="#2a2036"/><ellipse cx="40" cy="13" rx="12" ry="2.8" fill="#1c1426"/>'
                  f'<rect x="32" y="9" width="16" height="2.8" fill="#facc15"/><rect x="33.6" y="4.4" width="2.6" height="4" rx="1.3" fill="#fff" opacity=".25"/></g>'
                + _face(u, 41, 32, 5.4, 7.6, st, mode, i, p["skin"], look, mouth_dy=8.6)
                + f'<circle cx="48.6" cy="32" r="7.4" fill="none" stroke="#facc15" stroke-width="1.6"/><path d="M55.8 35q3 5 0 10" fill="none" stroke="#facc15" stroke-width="1"/>')
        arms = _arms(u, mode, st, [(14, 56, 9, 15), (57, 56, 9, 15)])
        prop = _act(mode, "toss", st, f'<circle cx="65" cy="62" r="5.4" fill="url(#{u}o)" stroke="#a16207" stroke-width="1.2"/><path d="M65 59.3v5.4" stroke="#a16207" stroke-width="1.3" stroke-linecap="round"/><circle cx="63.3" cy="60.4" r="1.1" fill="#fff" opacity=".8"/>')
    elif name == "Instructor":  # rounded wedge head (avatar: wedge/green), big glasses, book
        lean = -3
        look = (0.1, 0.95) if st == "working" else look
        body = (_body(u, p)
                + f'<path d="M33 53q7 5 14 0" fill="none" stroke="{p["dark"]}" stroke-width="1.8" stroke-linecap="round" opacity=".7"/>'
                + f'<path d="M40 8C56 10 65 24 65 36C65 47 54 51 40 51C26 51 15 47 15 36C15 24 24 10 40 8Z" fill="url(#{u}s)"/>'
                + f'<path d="M40 8q5-5 10-2" fill="none" stroke="{p["dark"]}" stroke-width="2" stroke-linecap="round"/>'
                + f'<path d="M56 16q8 8 7 20" fill="none" stroke="#fff" stroke-width="1.6" stroke-linecap="round" opacity=".7"/>'
                + _face(u, 41, 34, 5.8, 8.4, st, mode, i, p["skin"], look, mouth_dy=9.4)
                + f'<g fill="none" stroke="#9a3412" stroke-width="1.7"><ellipse cx="32.6" cy="34" rx="7.8" ry="8.2"/><ellipse cx="49.4" cy="34" rx="8.6" ry="8.6"/><path d="M40.2 33.5q1-1 1.4 0"/></g>'
                + f'<ellipse cx="47" cy="30" rx="2.4" ry="1.2" fill="#fff" opacity=".35"/>')
        arms = _arms(u, mode, st, [(15, 58, 9, 14), (56, 58, 9, 14)])
        prop = ('<path d="M22 70.5l17-1.6v-8.4L22 62z" fill="#fef3c7" stroke="#b45309" stroke-width=".9"/><path d="M58 70.5l-17-1.6v-8.4l17 1.5z" fill="#fef3c7" stroke="#b45309" stroke-width=".9"/>'
                '<path d="M25 64.5h10M25 66.5h9M44.5 64.5h10M44.5 66.5h8" stroke="#d6a76a" stroke-width=".7"/>'
                + _act(mode, "page", st, '<path d="M41 60.6l13 1.2v6.6l-13-.6z" fill="#fde68a" opacity=".95"/>'))
    else:  # Auditor: rounded square head (avatar: square/brown), magnifier, clipboard
        lean = 3
        body = (_body(u, p)
                + f'<path d="M30 52l10 6 10-6" fill="none" stroke="{p["dark"]}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>'
                + f'<rect x="35" y="7" width="10" height="8" rx="3" fill="{p["dark"]}"/>'
                + f'<rect x="17" y="12" width="46" height="37" rx="13" fill="url(#{u}s)"/>'
                + f'<path d="M59 18q4 8 2 22" fill="none" stroke="#fff" stroke-width="1.6" stroke-linecap="round" opacity=".55"/>'
                + f'<ellipse cx="29" cy="16" rx="5" ry="2.2" fill="#fff" opacity=".35"/>'
                + _face(u, 41, 32, 6.0, 8.6, st, mode, i, p["skin"], look, mouth_dy=9.4, mood="hmm"))
        arms = _arms(u, mode, st, [(15, 57, 9, 15), (56, 57, 9, 15)])
        prop = ('<rect x="9.5" y="57" width="16" height="14" rx="1.6" fill="#e2c49a" stroke="#78350f" stroke-width=".9"/><rect x="14" y="55.2" width="7" height="3.4" rx="1.2" fill="#475569"/>'
                '<path d="M15 61.5h8M15 64.2h6.5M15 66.9h7.5" stroke="#78350f" stroke-width=".8" stroke-linecap="round"/><path d="M11.6 61.4l.9.9 1.5-1.8" stroke="#15803d" stroke-width="1" fill="none" stroke-linecap="round"/>'
                + _act(mode, "sweep", st, '<path d="M63 64l5.5 5.5" stroke="#6b4423" stroke-width="3.6" stroke-linecap="round"/>'
                       '<circle cx="58.5" cy="59.5" r="6.4" fill="#bae6fd" fill-opacity=".35" stroke="#e5e7eb" stroke-width="2.4"/><path d="M55.5 57q2-2 4.5-1.6" stroke="#fff" stroke-width="1.2" fill="none" stroke-linecap="round"/>'))
    if bare:
        if name == "Watchman":  # lantern hand is a prop; give the neutral figure its second arm
            arms += _arms(u, mode, st, [(54, 57, 9, 15)]).replace('arm l', 'arm r')
        return _wrap(u, f'{_defs(u, p)}<g>{body}{arms}</g>', tough)
    bb_cls = ' class="bb"' if mode == "css" else ""
    return _wrap(u, f'{_defs(u, p)}<g{bb_cls}>{_bob(mode, st)}<g transform="{_pose(st, lean)}">{body}</g></g>'
            f'{_desk(u) if desk else _plinth(u)}{shadow}<g transform="{_pose(st, lean)}">{arms}</g>{prop}', tough)

def _wrap(u, s, tough):
    """Tough shirt treatment: ink outline on every body/head shape + a bold purple sticker keyline."""
    _T[0] = False
    if not tough:
        return s
    return (f'<style>.{u}t [fill$="b)"]:not(polygon),.{u}t [fill$="s)"]:not(polygon){{stroke:#0a0a0c;stroke-width:1.6}}.{u}t g[fill]{{stroke:none}}</style>'
            f'<filter id="{u}x" x="-15%" y="-15%" width="130%" height="130%"><feMorphology in="SourceAlpha" operator="dilate" radius="1.1" result="a"/>'
            f'<feFlood flood-color="#0a0a0c"/><feComposite in2="a" operator="in" result="ink"/>'
            f'<feMorphology in="SourceAlpha" operator="dilate" radius="2.3" result="b"/><feFlood flood-color="#8b5cf6"/><feComposite in2="b" operator="in" result="key"/>'
            f'<feMerge><feMergeNode in="key"/><feMergeNode in="ink"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
            f'<g class="{u}t" filter="url(#{u}x)">{s}</g>')

def svg(name, state, mode="css", i=0, w=None, desk=True, bare=False, tough=False):
    size = f' width="{w}" height="{round(w*1.35)}"' if w else ""
    return f'<svg viewBox="0 0 80 108"{size} aria-hidden="true">{inner(name, state, mode, i, desk, bare, tough)}</svg>'
