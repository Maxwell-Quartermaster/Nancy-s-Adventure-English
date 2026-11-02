# Happy eyes (Maxwell t408u): every Sam figure uses Nancy's happy eyes exactly: her path M32.6 21q2.4-2.8 4.8 0M42.6 21q2.4-2.8 4.8 0,
# stroke 1.6, Ink #10170F by inheritance, in the shared head frame (scaled with Sam's head). In the build this is the shared #rE (cards).
NANCY = "<path d='M32.6 21q2.4-2.8 4.8 0M42.6 21q2.4-2.8 4.8 0' stroke-width='1.6'/>"
PROF = "<path d='M46 21q2.4-2.8 4.8 0' stroke-width='1.6'/>"      # title Sam in profile: one of her arcs, centred in his lens (48.4)
SUBS = [
    ("<use href='#rE'/>", NANCY),                                                                  # rig open eyes -> her arcs (Sam, and the guardians drawn from his rig)
    ("<path d='M33.1 20.7q1.9-2.4 3.8 0M43.1 20.7q1.9-2.4 3.8 0'/>", NANCY),                        # map Sam plate's thinner, smaller arcs
    ("<g stroke='none'><ellipse cx='48.6' cy='20' rx='1.1' ry='.9' fill='#FFF8E1'/><circle cx='49.1' cy='20' r='.6' fill='#10170F'/></g>", PROF),   # v6-06+ title Sam
    ("<ellipse cx='48' cy='20' rx='2.6' ry='4' fill='none' stroke-width='2.2'/>", "<ellipse cx='48' cy='20' rx='2.6' ry='4' fill='none' stroke-width='2.2'/>" + PROF.replace('M46 ', 'M45.6 ')),  # v6-04 title Sam (49)
]
# t328u fields HAPPY ("<g stroke-width='1.6'><path d='M32.6 21q2.4-2.8 4.8 0M42.6 21q2.4-2.8 4.8 0'/></g>") is already her exact eyes: kept.
OLD = ["<use href='#rE'/>", "M33.1 20.7q1.9-2.4 3.8 0", "<ellipse cx='48.6' cy='20' rx='1.1' ry='.9' fill='#FFF8E1'/>", "M32.8 21.4q2.2-3.2"]
def apply(html):
    n = {}
    for a, b in SUBS:
        c = html.count(a)
        if c: n[a[:24]] = c; html = html.replace(a, b)
    return html, n
