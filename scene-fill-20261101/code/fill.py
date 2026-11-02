# Scene fill (Maxwell t511s1901 "Yes, fill every gap"). Render-only staging; never edits PASTE, build, snapshots or r2h outputs.
# Sources are read-only HTML already in the snapshot manifest (scenes/tod, scenes/stage, screens-v608); fixes come from round2/r2h/fix_r2h.py (imported, not edited).
import os, sys, re, json, hashlib, shutil
sys.dont_write_bytecode = True
B = '/workspace/v608build/scene-fill-20261101/'
sys.path.insert(0, '/workspace/v608build/round2/r2h'); import fix_r2h as F
V = '/workspace/v608build/'; TOD_D = V + 'scenes/tod/'; STG = V + 'scenes/stage/html/'; SCR = '/workspace/screens-v608/html/'
PASTE = V + 'r2h-build/nancys-adventure-english-v6-08-1B-v32-PASTE.md'; PTR = V + 'CURRENT-SNAP.txt'
md5f = lambda p: hashlib.md5(open(p, 'rb').read()).hexdigest()
md5s = lambda s: hashlib.md5(s.encode()).hexdigest()
TINT = {'m': 'rgba(255,170,110,.12)', 'd': 'rgba(255,255,255,.16)', 'a': 'rgba(255,196,80,.16)', 'e': 'rgba(255,130,60,.16)', 'n': 'rgba(11,27,51,.45)'}
STOPS = {'m': ('#7FA7DE', '#F9CFA4'), 'd': ('#58ABF4', '#F2F8FF'), 'a': ('#3F86D9', '#F6D98E')}   # tod_v608 R7 stops; e/n use the title palette CSS
STEP = dict(m=1, d=2, a=3, e=4, n=5)
TINT_RE = re.compile(r"<div class='abs'(?: data-tod='[a-z]')? style='left:0;top:0;width:\d+px;height:\d+px;background:rgba\([^)]*\);pointer-events:none'></div>")
STOP_RE = re.compile(r"<style>#sk stop\{stop-color:#[0-9A-Fa-f]+\}#sk stop\+stop\{stop-color:#[0-9A-Fa-f]+\}[^<]*</style>")
def tint_in(doc, tod, w, h, attr=True):
    doc = TINT_RE.sub('', doc)
    ov = f"<div class='abs'{(' data-tod=' + repr(tod)) if attr else ''} style='left:0;top:0;width:{w}px;height:{h}px;background:{TINT[tod]};pointer-events:none'></div>"
    k = doc.index("data-name='back'"); k = doc.rindex('<div', 0, k)
    return doc[:k] + ov + doc[k:]
def outdoor(doc, tod, w, h):
    n = len(re.findall(r"data-tod='[a-z]'", doc)); assert n == 1, n
    doc = re.sub(r"data-tod='[a-z]'", f"data-tod='{tod}'", doc)   # spec :227: midday is its own state 'd'
    doc = STOP_RE.sub('', doc)
    css = ''
    if tod in STOPS: css += f"#sk stop{{stop-color:{STOPS[tod][0]}}}#sk stop+stop{{stop-color:{STOPS[tod][1]}}}"
    if tod == 'd': css += "[data-tod=d] .su{transform:translate(-50px,-40px)}"   # midday: the a sun spot, lighter sky (spec: 'the a sky lighter')
    if css:
        i = doc.index("<div class='abs ti' data-tod=") if "<div class='abs ti' data-tod=" in doc else doc.index("data-tod='")
        i = doc.rindex('<', 0, i); doc = doc[:i] + f'<style>{css}</style>' + doc[i:]
    return tint_in(doc, tod, w, h, attr=False)
def indoor(doc, tod, w, h): return TINT_RE.sub('', doc) if tod is None else tint_in(doc, tod, w, h, attr=True)
WALL = ('E-', 'F-')   # 1B (Maxwell t492u): front desk and kitchen get the taller wall
F.WALL_ROOMS = lambda tag: tag.startswith(WALL) or tag[:3] in ('20-', '21-', '22-')
WSKY = dict(m='#F9CFA4', d='#9CCBF2', a='#F6D98E', e='#F4A862', n='#2B3A6B')   # window sky follows the scene step (indoor = sky/ground/light tint only)
WIN_RE = re.compile(r"(<path d='M\d+ 407h\d+v\d+H\d+z' fill=')#(?:F4A862|2B3A6B)(' stroke-width='4'/>)")
DISC_RE = re.compile(r"(<circle cx='[\d.]+' cy='45\d(?:\.\d+)?' r='[\d.]+' fill=')#(?:FFE27A|FFF3C4)(' stroke='none'/>)")
def window(doc, tod):
    if tod is None: return doc
    d, n1 = WIN_RE.subn(lambda m: m.group(1) + WSKY[tod] + m.group(2), doc)
    d, n2 = DISC_RE.subn(lambda m: m.group(1) + ('#FFF3C4' if tod == 'n' else '#FFE27A') + m.group(2), d)
    assert n1 == 1 and n2 == 1, ('window', n1, n2); return d
def asks(doc):   # sentence cards keep their own card ask from the PASTE (ms-21 keys: 'Where are the keys?' / 'กุญแจอยู่ไหนครับ', as bh-24); only word cards take tapPrompt (fix_r2h)
    return doc
NW_OLD = "<div class='t17' data-txt=1 style='line-height:1.7'>หา croissant เจอไหม</div>"
def r2h(doc, tag, w):
    r = F.fix(asks(doc), tag, w); d = r[0] if isinstance(r, tuple) else r
    if w == 320 and NW_OLD in d:   # kitchen 320: the longer r2h ask wrapped 'เจอ|ไหม' onto a 4th card line (clipped); keep the Thai on one line (17px, lh 1.7 unchanged)
        d = d.replace(NW_OLD, NW_OLD.replace("'t17'", "'t17 nw'")); r = (d,) + tuple(r[1:]) if isinstance(r, tuple) else d
    assert 'Where is the' not in d or tag.startswith('E-'), tag; return r
J = []
def job(tag, src, w, h, loc, tod, fn, note=''): J.append(dict(tag=tag, src=src, w=w, h=h, loc=loc, tod=tod, fn=fn, note=note))
SZ = [(390, 844, '390', '390x844'), (320, 568, '320x568', '320x568')]
for t in 'dhaen'.replace('h', ''):
    for w, h, a, b in SZ: job(f'park-{t}-{b}', TOD_D + f'meadow-step{STEP[t]}-{a}.html', w, h, 'meadow-park', t, 'outdoor')
PONDE = os.path.exists(V + 'round2/r2h/png/stage-A-meadow-evening-pond-390x844.png') and os.path.exists(V + 'round2/r2h/png/stage-A-meadow-evening-pond-320x568.png')
for t in ('mdan' if PONDE else 'mdaen'):
    for w, h, a, b in SZ: job(f'pond-{t}-{b}', STG + f'A-meadow-evening-pond-{b}.html', w, h, 'meadow-pond', t, 'outdoor')
for t in 'mdaen':
    for w, h, a, b in SZ: job(f'home-{t}-{b}', TOD_D + f'lake-step{STEP[t]}-{a}.html', w, h, 'lake-home', t, 'indoor')
for t in 'mdaen':
    for w, h, a, b in SZ: job(f'F-kitchen-{t}-{b}', STG + f'F-lake-night-table-{b}.html', w, h, 'lake-kitchen', t, 'indoor')
for t in ['base'] + list('mdaen'):
    for w, h, a, b in SZ: job(f'E-front-desk-{t}-{b}', STG + f'E-lake-front-desk-{b}.html', w, h, 'lake-front-desk', t, 'indoor')
for t in 'mden':
    for w, h, a, b in SZ: job(f'farm-{t}-{b}', TOD_D + f'fields-step{STEP[t]}-{a}.html', w, h, 'fields-farm', t, 'outdoor')
# ---- title (spec :157; greetings from uiText) ----
G = dict(m='Good morning!', a='Good afternoon!', e='Good evening!', n='Good night!')
def pq_block(doc):
    i = doc.index("<g class='pq'>"); j = i; depth = 0
    for m in re.finditer(r'<g[ >]|</g>', doc[i:]):
        depth += 1 if m.group(0) != '</g>' else -1
        if depth == 0: j = i + m.end(); break
    return i, j
NT = "<path class='nt' d='M-20 0h430v844H-20z' fill='url(#nf)' stroke='none'/>"
def title(doc, tod, greet):
    assert doc.count("class='ti' data-tod='m'") == 1 and doc.count('Good morning!</text>') == 1
    doc = doc.replace("class='ti' data-tod='m'", f"class='ti' data-tod='{tod}'").replace('Good morning!</text>', greet + '</text>')
    if tod == 'n':   # as 52-title-night: the plane + banner painted above the night tint
        i, j = pq_block(doc); g = doc[i:j]; doc = doc[:i] + doc[j:]
        k = doc.index(NT) + len(NT) if NT in doc else None
        if k is None:
            m = re.search(r"<path class='nt' d='[^']*' fill='url\(#nf\)' stroke='none'/>", doc); k = m.end()
        doc = doc[:k] + g.replace("<g class='pq'>", "<g data-name='night-banner' class='pq'>", 1) + doc[k:]
    return doc
TT = {'390x844': SCR + '01-title.html', '320x568': SCR + '01-title-320x568.html'}
for b, src in TT.items():
    w, h = map(int, b.split('x'))
    job(f'title-a-{b}', src, w, h, 'TITLE', 'a', 'title', 'clean afternoon (no home-screen hint card)')
    job(f'title-e-{b}', src, w, h, 'TITLE', 'e', 'title', 'evening greeting uiText.greetEvening')
job('title-n-A-320x568', TT['320x568'], 320, 568, 'TITLE', 'n', 'title', 'night A: uiText.greetNight "Good night!" (PASTE 317e91ce)')
job('title-n-B-320x568', TT['320x568'], 320, 568, 'TITLE', 'n', 'titleB', 'INTERNAL night B: "Good evening!" (instructor-night-b1-picks.py --night, addf7973; not in PASTE 317e91ce)')
def make(j):
    d = open(j['src']).read(); fn = j['fn']; t = j['tod']; w, h = j['w'], j['h']
    if fn == 'outdoor':
        d = outdoor(d, t, w, h)
        if j['loc'] == 'meadow-pond' and t in 'mda':   # stage A pins a setting sun at the right edge (evening art); use the meadow tod placement (steps 1-4) instead
            o = "[data-tod] .su{transform:translate(60px,70px)!important}"; assert d.count(o) == 1, j['tag']
            d = d.replace(o, "[data-tod] .su{transform:translate(-170px,120px)!important}")
    elif fn == 'indoor': d = window(indoor(d, None if t == 'base' else t, w, h), None if t == 'base' else t)
    elif fn == 'title': return title(d, t, G[t]), []
    elif fn == 'titleB': return title(d, 'n', 'Good evening!'), []
    return r2h(d, j['tag'], w)
def selftest():   # the night transform must reproduce the approved 52 at 390 byte for byte
    a = title(open(SCR + '01-title.html').read(), 'n', 'Good night!'); b = open(SCR + '52-title-night.html').read()
    return a == b
if __name__ == '__main__':
    os.makedirs(B + 'html', exist_ok=True)
    print('night selftest 01->52 identical:', selftest())
    ptr = md5f(PTR); pm = md5f(PASTE); assert ptr == 'f6dac2d0e7b391436a160eab1bbf17fe' and pm == '317e91ce86f073c961f8169183d2bbd3', (ptr, pm)
    meta = []; LOG = []
    for j in J:
        doc, lg = make(j); LOG += lg
        hp = B + f"html/{j['tag']}.html"; open(hp, 'w').write(doc)
        meta.append(dict(tag=j['tag'], loc=j['loc'], tod=j['tod'], w=j['w'], h=j['h'], src=j['src'], src_md5=md5f(j['src']), html_md5=md5s(doc), note=j['note'], fixes=lg))
    json.dump(dict(pointer_md5=ptr, paste_md5=pm, pond_evening_skipped=PONDE, jobs=meta), open(B + 'code/jobs.json', 'w'), indent=1, ensure_ascii=False)
    open(B + 'code/fixlog-fill.txt', 'w').write('\n'.join(LOG) + '\n')   # FIXLOG.md is composed by code/fixlog.py (attribution prefix on every line)
    print(len(J), 'pages; pond evening skipped (r2h has it):', PONDE)
