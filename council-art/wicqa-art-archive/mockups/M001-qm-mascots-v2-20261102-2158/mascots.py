"""Council bot mascots: our own inline SVG, no outside assets (t734u).
Colors and a shape motif come from each bot's avatar setting in its profile.json (read only):
QM cloud/blue, Watchman pumpkin/orange, Chancellor star/violet, Instructor wedge/green, Auditor square/brown.
mode: "css"  -> classes (.bb .act .lid .arm) animated by the page CSS
      "smil" -> SMIL <animate> children (for the private Page), "still" -> no animation at all.
"""
INK = "#1b1b2f"
ACTS = {  # role action, translate only (safe in Safari 14)
    "write": "0 0;-6 1;0 0;-3 -1;0 0", "sway": "0 0;3 0;0 0;-3 0;0 0", "toss": "0 0;0 -11;0 0",
    "page": "0 0;-9 0;-9 0;0 0", "sweep": "0 0;-9 0;0 0",
}
DUR = {"write": "1.1s", "sway": "1.6s", "toss": "1s", "page": "1.8s", "sweep": "1.8s"}

def _anim(mode, kind, state, extra=""):
    if mode != "smil" or state != "working":
        return ""
    return f'<animateTransform attributeName="transform" type="translate" values="{ACTS[kind]}" dur="{DUR[kind]}" repeatCount="indefinite"{extra}/>'

def _bob(mode, state):
    return '<animateTransform attributeName="transform" type="translate" values="0 0;0 -2;0 0" dur="2.4s" repeatCount="indefinite"/>' if mode == "smil" and state == "working" else ""

def _lid(mode, x, y, w, h, fill, i, state):
    a = ""
    if mode == "smil":
        dur = "4.2s" if state == "working" else "7s"
        a = f'<animate attributeName="opacity" values="0;0;1;0" keyTimes="0;0.9;0.94;1" dur="{dur}" begin="{i*0.7:.1f}s" repeatCount="indefinite"/>'
    cls = ' class="lid"' if mode == "css" else ""
    return f'<rect{cls} x="{x}" y="{y}" width="{w}" height="{h}" rx="{min(w,h)/2:.1f}" fill="{fill}" opacity="0">{a}</rect>'

def _eye(cx, cy, r, state, skin, mode, i):
    dy = 1.1 if state == "working" else 0  # working: looking down at the task
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#fff"/>'
            f'<circle cx="{cx}" cy="{cy+dy:.1f}" r="{r*0.62:.1f}" fill="{INK}"/>'
            f'<circle cx="{cx-r*0.28:.1f}" cy="{cy+dy-r*0.32:.1f}" r="{r*0.26:.1f}" fill="#fff"/>'
            f'<circle cx="{cx+r*0.22:.1f}" cy="{cy+dy+r*0.2:.1f}" r="{r*0.12:.1f}" fill="#fff"/>'
            + _lid(mode, cx - r - .6, cy - r - .6, 2 * r + 1.2, 2 * r + 1.2, skin, i, state))

def _face(cx1, cx2, cy, r, state, skin, mode, i, mouth_y, brow=True, blush=True):
    s = _eye(cx1, cy, r, state, skin, mode, i) + (_eye(cx2, cy, r, state, skin, mode, i) if cx2 else "")
    xs = [cx1] + ([cx2] if cx2 else [])
    if brow:
        for x in xs:
            if state == "working":  # focused, a little determined
                s += f'<path d="M{x-r} {cy-r-2.2:.1f}l{2*r} {1.2 if x == xs[0] else -1.2}" stroke="{INK}" stroke-width="1.6" stroke-linecap="round"/>' if len(xs) == 2 else f'<path d="M{x-r} {cy-r-3:.1f}q{r} -2.4 {2*r} 0" fill="none" stroke="{INK}" stroke-width="1.6" stroke-linecap="round"/>'
            else:
                s += f'<path d="M{x-r*0.8:.1f} {cy-r-2.4:.1f}q{r*0.8:.1f} -1.6 {r*1.6:.1f} 0" fill="none" stroke="{INK}" stroke-width="1.4" stroke-linecap="round" opacity=".8"/>'
    mid = (cx1 + (cx2 or cx1)) / 2
    if blush:
        for x in xs if len(xs) == 2 else [mid - r - 3, mid + r + 3]:
            off = -r - 1.5 if (len(xs) == 2 and x == xs[0]) else (r + 1.5 if len(xs) == 2 else 0)
            s += f'<ellipse cx="{x+off:.1f}" cy="{cy+r+1.5:.1f}" rx="3" ry="1.8" fill="#fb7185" opacity=".55"/>'
    if state == "working":
        s += f'<path d="M{mid-3.2:.1f} {mouth_y}q3.2 3.6 6.4 0z" fill="#7f1d1d"/><path d="M{mid-1.6:.1f} {mouth_y+1.6:.1f}q1.6 1 3.2 0" fill="#fb7185"/>'
    else:
        s += f'<path d="M{mid-2.4:.1f} {mouth_y}q2.4 1.8 4.8 0" fill="none" stroke="{INK}" stroke-width="1.4" stroke-linecap="round"/>'
    return s

def _arms(mode, state, color, pts):
    out = ""
    for k, (x, y, w, h) in enumerate(pts):
        cls = f' class="arm {"l" if k == 0 else "r"}"' if mode == "css" else ""
        a = f'<animateTransform attributeName="transform" type="translate" values="0 0;0 -2;0 0" dur="0.5s" begin="{k*0.25}s" repeatCount="indefinite"/>' if mode == "smil" and state == "working" else ""
        out += f'<rect{cls} x="{x}" y="{y}" width="{w}" height="{h}" rx="{w/2:.1f}" fill="{color}">{a}</rect>'
    return out

def _act(mode, kind, state, body):
    cls = f' class="act {kind}"' if mode == "css" else ""
    return f'<g{cls}>{_anim(mode, kind, state)}{body}</g>'

DESK = ('<g><rect x="8" y="78" width="7" height="28" fill="#7a4a24"/><rect x="65" y="78" width="7" height="28" fill="#7a4a24"/>'
        '<rect x="8" y="78" width="64" height="7" fill="#946036"/>'
        '<rect x="3" y="69" width="74" height="9" fill="#b07945"/><rect x="3" y="76" width="74" height="2" fill="#8a5a2f"/>'
        '<path d="M7 72h22M35 74.5h17M57 71.5h16M14 75h9" stroke="#8a5a2f" stroke-width=".8" opacity=".75"/></g>')

def inner(name, state, mode="css", i=0):
    st = state if state in ("working", "idle") else "idle"
    if name == "Quartermaster":  # sturdy boxy, cloud cap (avatar: cloud/blue), shield, ledger + pen
        c, d, skin = "#3b82f6", "#1e40af", "#bfdbfe"
        body = (f'<rect x="19" y="45" width="42" height="26" rx="3" fill="{c}"/><rect x="19" y="45" width="42" height="5" fill="{d}"/>'
                f'<path d="M40 52l7 2.6v4.4c0 4.4-3.5 7-7 8.8-3.5-1.8-7-4.4-7-8.8v-4.4z" fill="#eef3ff"/><path d="M40 55.5v9" stroke="{c}" stroke-width="1.6"/>'
                f'<circle cx="27" cy="13" r="6.5" fill="#dbeafe"/><circle cx="36" cy="9.5" r="8" fill="#dbeafe"/><circle cx="46" cy="10.5" r="7" fill="#dbeafe"/><circle cx="54" cy="14" r="5.5" fill="#dbeafe"/>'
                f'<rect x="17" y="13" width="46" height="31" rx="5" fill="{skin}" stroke="{d}" stroke-width="2"/>'
                + _face(31, 49, 26, 5, st, skin, mode, i, 35)
                + _arms(mode, st, d, [(14, 52, 7, 15), (59, 52, 7, 15)]))
        prop = ('<rect x="22" y="63" width="24" height="7" rx="1" fill="#f5ecd7" stroke="#8a5a2f" stroke-width=".8"/><path d="M34 63v7" stroke="#8a5a2f" stroke-width=".8"/>'
                '<path d="M25 65.5h6M25 67.5h5M37 65.5h6" stroke="#9ca3af" stroke-width=".7"/>'
                + _act(mode, "write", st, '<path d="M48 58l-5 10" stroke="#facc15" stroke-width="2.4" stroke-linecap="round"/><path d="M43 68l-.6 1.6" stroke="#1b1b2f" stroke-width="1.2"/>'))
    elif name == "Watchman":  # tall slim sentinel, pumpkin head (avatar: pumpkin/orange), one big eye, lantern
        c, d, skin = "#f97316", "#c2410c", "#fed7aa"
        body = (f'<rect x="32" y="36" width="16" height="36" rx="6" fill="{c}"/><rect x="32" y="44" width="16" height="3" fill="{d}"/>'
                f'<rect x="38.5" y="3" width="3" height="6" rx="1" fill="#16a34a"/><path d="M41 5q5-3 7 1" fill="none" stroke="#16a34a" stroke-width="1.6"/>'
                f'<ellipse cx="40" cy="21" rx="17" ry="13.5" fill="{c}"/><path d="M30 10q-4 11 0 23M50 10q4 11 0 23M40 8v26" fill="none" stroke="{d}" stroke-width="1.2" opacity=".6"/>'
                f'<ellipse cx="40" cy="21" rx="11" ry="9" fill="{skin}"/>'
                + _face(40, None, 20, 6.4, st, skin, mode, i, 27.5, brow=True)
                + _arms(mode, st, d, [(26, 44, 6, 16)]))
        prop = _act(mode, "sway", st, '<path d="M50 46h8v4" fill="none" stroke="#475569" stroke-width="1.6"/><rect x="53.5" y="50" width="9" height="12" rx="2" fill="#1f2937"/>'
                    '<rect x="55" y="52" width="6" height="8" rx="1.5" fill="#fde68a"/><circle cx="58" cy="56" r="7" fill="#fde68a" opacity=".22"/>'
                    '<rect x="52" y="48" width="12" height="2.5" rx="1" fill="#475569"/><rect x="48" y="44" width="6" height="12" rx="3" fill="#c2410c"/>')
    elif name == "Chancellor":  # wide and dapper, top hat, monocle, star badge (avatar: star/violet), coin toss
        c, d, skin = "#8b5cf6", "#5b21b6", "#ddd6fe"
        body = (f'<rect x="9" y="38" width="62" height="33" rx="15" fill="{c}"/><path d="M40 38l-7 12 7 4 7-4z" fill="#f5f3ff"/><path d="M37 49l3 4 3-4-3-2z" fill="#be185d"/>'
                f'<path d="M24 52l1.5 3 3.3.5-2.4 2.3.6 3.3-3-1.6-3 1.6.6-3.3-2.4-2.3 3.3-.5z" fill="#facc15"/>'
                f'<rect x="15" y="15" width="50" height="25" rx="11" fill="{skin}" stroke="{d}" stroke-width="2"/>'
                f'<rect x="22" y="12" width="36" height="4" rx="2" fill="#111827"/><rect x="29" y="0" width="22" height="13" rx="2" fill="#111827"/><rect x="29" y="8.5" width="22" height="2.5" fill="{c}"/>'
                + _face(31, 49, 26, 4.6, st, skin, mode, i, 34.5)
                + f'<circle cx="49" cy="26" r="7" fill="none" stroke="#facc15" stroke-width="1.4"/><path d="M55 30q3 6 0 10" fill="none" stroke="#facc15" stroke-width=".9"/>'
                + _arms(mode, st, d, [(6, 48, 7, 16), (67, 48, 7, 16)]))
        prop = _act(mode, "toss", st, '<ellipse cx="64" cy="64" rx="5" ry="5" fill="#facc15" stroke="#a16207" stroke-width="1.4"/><path d="M64 61.5v5" stroke="#a16207" stroke-width="1.2"/>')
    elif name == "Instructor":  # soft rounded, wedge head (avatar: wedge/green), big glasses, book
        c, d, skin = "#4ade80", "#15803d", "#dcfce7"
        body = (f'<ellipse cx="40" cy="60" rx="21" ry="14" fill="{c}"/><path d="M33 47q7 5 14 0" fill="none" stroke="{d}" stroke-width="1.6"/>'
                f'<path d="M40 7Q63 10 65 33Q65 45 40 45Q15 45 15 33Q17 10 40 7Z" fill="{skin}" stroke="{d}" stroke-width="2"/>'
                f'<path d="M40 7q6 -4 9 -1" fill="none" stroke="{d}" stroke-width="1.6"/>'
                + _face(31, 49, 28, 5, st, skin, mode, i, 37.5)
                + f'<g fill="none" stroke="#9a3412" stroke-width="1.5"><circle cx="31" cy="28" r="7.6"/><circle cx="49" cy="28" r="7.6"/><path d="M38.6 28h2.8"/></g>'
                + _arms(mode, st, d, [(16, 54, 7, 14), (57, 54, 7, 14)]))
        prop = ('<path d="M24 69l14-1.5V61L24 62z" fill="#fef3c7" stroke="#b45309" stroke-width=".8"/><path d="M56 69l-14-1.5V61l14 1z" fill="#fef3c7" stroke="#b45309" stroke-width=".8"/>'
                + _act(mode, "page", st, '<path d="M42 61.3l11 1v5.4l-11-.4z" fill="#fde68a" opacity=".9"/>'))
    else:  # Auditor: angular and compact, square motif (avatar: square/brown), magnifier, clipboard
        c, d, skin = "#b45309", "#78350f", "#fde7c7"
        body = (f'<path d="M22 47h36l3 24H19z" fill="{c}"/><path d="M28 47l12 7 12-7" fill="none" stroke="{d}" stroke-width="1.6"/>'
                f'<path d="M24 20h32l4 4v20l-4 3H24l-4-3V24z" fill="{skin}" stroke="{d}" stroke-width="2"/><rect x="36" y="13" width="8" height="7" fill="{d}"/>'
                + _face(32, 48, 31, 4.6, st, skin, mode, i, 40)
                + _arms(mode, st, d, [(14, 52, 7, 15), (59, 52, 7, 15)]))
        prop = ('<rect x="11" y="57" width="15" height="13" rx="1" fill="#d6b48a" stroke="#78350f" stroke-width=".8"/><rect x="15" y="55.5" width="7" height="3" rx="1" fill="#475569"/>'
                '<path d="M14 61.5h9M14 64h7M14 66.5h8" stroke="#78350f" stroke-width=".8"/><path d="M13 61.5l.8.8 1.4-1.6" stroke="#15803d" stroke-width=".9" fill="none"/>'
                + _act(mode, "sweep", st, '<circle cx="58" cy="60" r="5.5" fill="#bae6fd" fill-opacity=".35" stroke="#e5e7eb" stroke-width="2.2"/><path d="M62 64l5 5" stroke="#e5e7eb" stroke-width="3" stroke-linecap="round"/>'))
    bb_cls = ' class="bb"' if mode == "css" else ""
    return f'<g{bb_cls}>{_bob(mode, st)}{body}</g>{DESK}{prop}'

def svg(name, state, mode="css", i=0, w=None):
    size = f' width="{w}" height="{round(w*1.35)}"' if w else ""
    return f'<svg viewBox="0 0 80 108"{size} aria-hidden="true">{inner(name, state, mode, i)}</svg>'
