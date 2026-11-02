# QM flex-gap (Nov 2 2026, candidate; Auditor fix320 F1): Safari 14.0 (iOS 14.0-14.4) ignores `gap` on flex boxes, so every inline
# `display:flex` box loses its gap and each element child after the first gets the same space as a leading margin (margin-left in a row,
# margin-top in a column). Grid gap stays (Safari 14 supports it). Page 30 is HELD and is left as it was. 0 PASTE chars.
_FGTAG = re.compile(r"<(/?)([A-Za-z][A-Za-z0-9]*)((?:[^>'\"]|'[^']*'|\"[^\"]*\")*?)(/?)>")
_FGVOID = {'br', 'img', 'input', 'meta', 'link', 'hr', 'source', 'wbr', 'area', 'base', 'col', 'embed', 'param', 'track'}
_FGSTY = re.compile(r"(\sstyle=)(['\"])(.*?)\2", re.S)
def _fg_style(attrs):
    m = _FGSTY.search(attrs); return (m, m.group(3)) if m else (None, None)
def flexgap(doc):
    out = []; pos = 0; st = []   # stack: [tag, gap px or None, column?, element children seen]
    for m in _FGTAG.finditer(doc):
        out.append(doc[pos:m.start()]); pos = m.end(); cl, tag, attrs, sc = m.group(1), m.group(2).lower(), m.group(3), m.group(4)
        if cl:
            while st and st[-1][0] != tag: st.pop()
            assert st, ('unmatched close', tag); st.pop(); out.append(m.group(0)); continue
        sm, sty = _fg_style(attrs); new = attrs
        if st and st[-1][1] is not None:
            par = st[-1]; par[3] += 1
            if par[3] > 1:
                prop = 'margin-top' if par[2] else 'margin-left'
                if sty is not None:
                    assert not re.search(r'(^|;)\s*(margin|' + prop + r')\s*:', sty), ('child already sets margin', sty[:80])
                    new = new[:sm.start(3)] + f'{prop}:{par[1]}px;' + new[sm.start(3):]
                else: new = new + f" style='{prop}:{par[1]}px'"
        gap = None; col = False
        sm2, sty2 = _fg_style(new)
        if sty2 is not None and re.search(r'(^|;)display:(inline-)?flex(;|$)', sty2):
            g = re.search(r'(^|;)gap:(\d+)px(;|$)', sty2)
            if g:
                assert not re.search(r'(^|;)(row-gap|column-gap|flex-wrap)\s*:', sty2), sty2[:80]
                gap = int(g.group(2)); col = bool(re.search(r'(^|;)flex-direction:column(;|$)', sty2))
                s3 = sty2[:g.start()] + g.group(1) + sty2[g.end():] if not g.group(3) else sty2[:g.start() + len(g.group(1))] + sty2[g.end():]
                new = new[:sm2.start(3)] + s3 + new[sm2.end(3):]
        out.append('<' + m.group(2) + new + sc + '>')
        if not sc and tag not in _FGVOID:
            if tag in ('script', 'style'):
                e = doc.index('</' + tag, pos); out.append(doc[pos:e]); pos = e
            st.append([tag, gap, col, 0])
    out.append(doc[pos:]); return ''.join(out)
for _n in list(SCR):
    if _n != 30:
        _s, _st, _sr, _fn = SCR[_n]; SCR[_n] = (_s, _st, _sr, (lambda f: lambda: flexgap(f()))(_fn))
_CHIP = re.compile(r"<div class='abs' style='left:8px;top:([0-9.]+)px;border-radius:10px;background:rgba\(255,248,225,\.92\);border:2px solid (#[0-9A-F]{6});padding:0 10px;display:flex;align-items:center'>.*?</div></div>")
_gchip0 = guardian_chip
def guardian_chip(doc, n): return flexgap(_gchip0(doc, n))
