# Read-only scene inventory (t508u). Scans renders, classifies region/location/time-of-day/size/status. Writes nothing outside council-tools.
import os, re, json, hashlib, sys
from PIL import Image
W = '/workspace'
ROOTS = [d for d in sorted(os.listdir(W)) if d.startswith(('screens-v6', 'mocks-', 'mock-t')) or d in ('v608build', 'polish-r1')]
MAN = W + '/v608build/snap-r2h-0021MDT/renders-MANIFEST.md5'
man = {}
for ln in open(MAN):
    p = ln.split(None, 1)
    if len(p) == 2: man[p[1].strip()] = p[0]
man_md5 = {}
for k, v in man.items(): man_md5.setdefault(v, []).append(k)
TINT = {'rgba(255,170,110,.12)': 'm', 'rgba(255,255,255,.16)': 'd', 'rgba(255,196,80,.16)': 'a', 'rgba(255,130,60,.16)': 'e', 'rgba(11,27,51,.45)': 'n'}
STOP = {'#7FA7DE': 'm', '#58ABF4': 'd', '#3F86D9': 'a'}
def md5(p):
    h = hashlib.md5()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''): h.update(b)
    return h.hexdigest()
def pair_html(png):
    d, b = os.path.split(png); s = b[:-4]
    for c in (os.path.join(d, s + '.html'), os.path.join(os.path.dirname(d), 'html', s + '.html'), os.path.join(os.path.dirname(d), s + '.html')):
        if os.path.exists(c): return c
    return None
def tod_of(s, loc):
    for k, v in TINT.items():
        if f"background:{k};pointer-events:none" in s: return v, 'tint'
    if 'linear-gradient(#4F64A8 0%,#F4A862' in s: return 'e', 'evening-overlay'
    m = re.search(r"data-tod='([a-z])'", s)
    if m:
        t = m.group(1)
        st = re.findall(r'(?<!\] )#sk stop\{stop-color:(#[0-9A-Fa-f]+)\}', s)
        if st and st[0] in STOP and t in 'ma': return STOP[st[0]], 'data-tod+stops'
        return t, 'data-tod'
    return None, 'none'
def loc_of(s, fn):
    N = set(re.findall(r"data-(?:name|pn)='([^']*)'", s)); D = set(re.findall(r"data-deco='([^']*)'", s))
    f = fn.lower()
    if N & {'row-r1', 'dot-r1'}: return 'MAP'
    if 'open-from-home' in f: return 'TITLE'
    if re.search(r'main-menu|menu-gemtag|welcome-back', f): return 'MENU'
    if 'rest-screen' in f or 'restNow' in N or 'keepGoing' in N: return 'REST'
    if 'letsGo' in N or re.search(r'title', f) and 'map' not in f: return 'TITLE'
    if N & {'tent', 'bridge', 'mushroom', 'owl', 'lantern'}: return 'forest-woods'
    if 'corn' in D or N & {'cow', 'gate'}: return 'fields-farm'
    if N & {'keys', 'truck'}: return 'lake-front-desk'
    lakeish = N & {'crib', 'towel', 'tie', 'disc', 'desk', 'sundae', 'spaghetti', 'eggs', 'croissant'}
    if lakeish:
        if N & {'sundae', 'spaghetti', 'eggs', 'croissant'} or ("stroke-width='6' stroke='#8E5730'" in s and 'crib' not in N) or 'kitchen' in f: return 'lake-kitchen'
        return 'lake-home'
    if 'swing set' in D:
        return 'meadow-pond' if N & {'ship', 'rock', 'rain', 'shop', 'water'} else 'meadow-park'
    return None
def loc_from_name(f):
    f = f.lower()
    if 'title' in f or 'open-from-home' in f: return 'TITLE'
    if re.search(r'main-menu|menu-gemtag|welcome-back', f): return 'MENU'
    if 'rest-screen' in f: return 'REST'
    if re.search(r'(^|[-_/])map', f): return 'MAP'
    if 'pond' in f: return 'meadow-pond'
    if 'front-desk' in f: return 'lake-front-desk'
    if 'kitchen' in f or 'night-table' in f: return 'lake-kitchen'
    if 'forest' in f or 'duel' in f: return 'forest-woods'
    if 'fields' in f or 'farm' in f: return 'fields-farm'
    if 'lake' in f or 'home' in f: return 'lake-home'
    if 'meadow' in f or 'park' in f: return 'meadow-park'
    return None
def tod_from_name(f):
    f = os.path.basename(f).lower().replace('night-table', 'tbl')
    m = re.search(r'step([1-5])', f)
    if m: return 'mdaen'[int(m.group(1)) - 1]
    for k, v in (('morning', 'm'), ('dawn', 'm'), ('midday', 'd'), ('afternoon', 'a'), ('evening', 'e'), ('dusk', 'e'), ('night', 'n')):
        if k in f: return v
    m = re.search(r'-([mdaen])-(320|390)', f)
    return m.group(1) if m else None
def size_of(png, f):
    m = re.search(r'(\d{3})x(\d{3})', os.path.basename(f))
    if m: return f'{m.group(1)}x{m.group(2)}'
    try: w, h = Image.open(png).size
    except Exception: return '?'
    for k in (1, 2, 3):
        if (w // k, h // k) in ((390, 844), (320, 568), (375, 667), (375, 812), (414, 896), (430, 932)): return f'{w//k}x{h//k}'
    if re.search(r'-390(check)?(\.|$|-)', os.path.basename(f)): return '390x844'
    return f'{w}x{h}px'
def look_reasons(s, loc):
    if s is None or loc is None: return None
    r = []
    if (loc.startswith('meadow') or loc == 'REST') and re.search(r"stroke='#(E8D9A8|D8C99A)' stroke-width='26'", s): r.append('meadow walkway (removed in r2h)')
    if (loc.startswith('meadow') or loc == 'REST') and "r='3' fill='#FFE27A'" in s: r.append('ground dots (tufts in r2h)')
    if loc.startswith('lake') and '#D9663F;padding:0 10px' in s: r.append('Home Lake chip #D9663F (r2h #F05A00)')
    if re.search(r'>Where is the [^<?]*\?<', s) or re.search(r"Where is the [a-z ]+\?</div", s): r.append('old ask wording "Where is the ...?" (P1 t440u tapPrompt "Can you find the {word}?")')
    return r
def look(s, loc):
    r = look_reasons(s, loc)
    return None if r is None else (len(r) == 0)
rows = []
HIDX = {}
for r in ROOTS:
    for dp, dn, fs in os.walk(os.path.join(W, r)):
        for fn in fs:
            if fn.endswith('.html'): HIDX.setdefault(fn[:-5], []).append(os.path.join(dp, fn))
def classify_html(h, rel):
    s = open(h, errors='ignore').read(); loc = loc_of(s, rel) or loc_from_name(rel)
    tod, how = tod_of(s, loc)
    if tod is None and loc and loc.startswith('lake'): tod, how = 'base', 'indoor-untinted'
    if loc in ('TITLE', 'MENU'):
        m = re.findall(r"data-tod='([a-z])'", s); g = re.findall(r'Good (morning|afternoon|evening|night)!', s)
        tod = m[0] if m else ({'morning': 'm', 'afternoon': 'a', 'evening': 'e', 'night': 'n'}[g[0]] if len(set(g)) == 1 else tod_from_name(rel))
    return s, loc, tod, how
for r in ROOTS:
    for dp, dn, fs in os.walk(os.path.join(W, r)):
        if '/agent-tools' in dp or '__pycache__' in dp: continue
        for fn in fs:
            if not fn.lower().endswith('.png'): continue
            p = os.path.join(dp, fn); rel = os.path.relpath(p, W)
            h = pair_html(p); via = 'pair' if h else None
            if not h:
                c = HIDX.get(fn[:-4], [])
                cl = set()
                for x in c:
                    _, l_, t_, _ = classify_html(x, rel); cl.add((l_, t_))
                if c and len(cl) == 1: h = c[0]; via = 'stem(%d)' % len(c)
            s = open(h, errors='ignore').read() if h else None
            loc = (loc_of(s, rel) if s else None) or loc_from_name(rel)
            sheet = bool(re.search(r'(strip-|sheet|contact|before-after|showcase-|pick|-vs-|heatmap|/sheets?/|/pick-sheets)', rel.lower()))
            if s:
                tod, how = tod_of(s, loc)
                if tod is None and loc and loc.startswith('lake'): tod, how = 'base', 'indoor-untinted'
                if loc in ('TITLE', 'MENU'):
                    m = re.findall(r"data-tod='([a-z])'", s); g = re.findall(r'Good (morning|afternoon|evening|night)!', s)
                    tod = m[0] if m else ({'morning': 'm', 'afternoon': 'a', 'evening': 'e', 'night': 'n'}[g[0]] if len(set(g)) == 1 else tod_from_name(rel))
            else:
                tod, how = tod_from_name(rel), 'filename'
                if tod is None and loc and not sheet: tod = 'unknown'
            m5 = md5(p)
            inman = rel in man or m5 in man_md5
            before = '-before' in fn
            lk = look(s, loc) if via == 'pair' else None
            if before: st = 'BEFORE'
            elif inman: st = 'CURRENT' if lk is not False else 'CURRENT-LISTED-STALE-LOOK'
            else: st = 'OLD'
            kind = 'sheet' if sheet else ('ask' if s and ("data-name='question'" in s or "data-name='listen'" in s) and re.search(r"data-pn='", s) else ('overlay' if loc and loc not in ('MAP', 'TITLE') else 'screen'))
            if loc in ('MAP', 'TITLE', 'MENU', 'REST'): kind = 'screen'
            rows.append(dict(stale=(look_reasons(s, loc) if via == 'pair' else None), html_via=via, path=rel, md5=m5, html=os.path.relpath(h, W) if h else None, loc=loc, tod=tod, tod_src=how, size=size_of(p, rel), status=st, in_manifest=inman, look_ok=lk, kind=kind,
                             rest=('rest' in fn.lower())))
G = {}
for x in rows: G.setdefault(x['md5'], []).append(x)
for g in G.values():
    src = next((x for x in g if x['html_via'] == 'pair'), None) or next((x for x in g if x['html']), None)
    if src:
        for x in g:
            if (not x['html'] or (x['html_via'] or '').startswith('stem')) and x is not src: x.update(loc=src['loc'], tod=src['tod'], tod_src=src['tod_src'] + ' (md5 copy)', look_ok=src['look_ok'], stale=src['stale'], kind=src['kind'], html=src['html'], html_via='md5')
    inm = any(x['in_manifest'] for x in g)
    for x in g:
        x['in_manifest'] = inm
        if x['status'] != 'BEFORE': x['status'] = ('CURRENT' if x['look_ok'] is not False else 'CURRENT-LISTED-STALE-LOOK') if inm else 'OLD'
for x in rows:
    x['in_progress'] = x['path'].startswith('v608build/round2/r2h/') and not x['in_manifest']
json.dump(rows, open('/tmp/inv/rows.json', 'w'), indent=0)
print(len(rows))
