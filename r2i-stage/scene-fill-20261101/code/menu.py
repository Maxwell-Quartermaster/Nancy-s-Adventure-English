# Menu at evening + night from snapshot copies of the r2h M1/M3 concepts (current layout). Morning = M1/M3 as-is (not re-rendered).
import os, re, json, hashlib, sys
sys.dont_write_bytecode = True; sys.path.insert(0, '/workspace/v608build/round2/r2h'); import fix_r2h as F   # read-only: F.tuft, the walk-24 / t441u three-blade tuft
B = '/workspace/v608build/scene-fill-20261101/'; V = '/workspace/v608build/'
md5 = lambda p: hashlib.md5(open(p, 'rb').read()).hexdigest()
PTR, PASTE = md5(V + 'CURRENT-SNAP.txt'), md5(V + 'r2h-build/nancys-adventure-english-v6-08-1B-v32-PASTE.md')
assert PTR.startswith('f6dac2d0') and PASTE.startswith('317e91ce'), (PTR, PASTE)
SKY = dict(e=('#4F64A8', '#B9879A', '#F4A862'), n=('#0B1B3A', '#1C2E55', '#2E4370'))   # title skies (spec :121 'menus take the title's four skies')
TINT = dict(e='rgba(255,130,60,.16)', n='rgba(11,27,51,.45)')
GREET = dict(e=('Good evening!', 'สวัสดีตอนเย็น!'), n=('Good night!', 'ราตรีสวัสดิ์!'))   # uiText greetEvening / greetNight (night = A)
STOPS = "<stop stop-color='#3D8FE6'/><stop offset='.5' stop-color='#9FD0F5'/><stop offset='1' stop-color='#FFF1C9'/>"
FLW = re.compile(r"<g data-bb='flowers'>((?:<g stroke='none'>(?:<circle [^>]*/>)+</g>)+)</g>")
def tufts(doc):   # Maxwell t527u: no circle dots on grass; the 4 five-petal circle flowers become three-blade tufts at the same spots (390 only; 320 has no scene panel)
    m = FLW.search(doc)
    if not m: return doc, 0
    cs = re.findall(r"<circle cx='([0-9.]+)' cy='([0-9.]+)' r='1.8' fill='#FFD54F'/>", m.group(1)); assert len(cs) == 4, cs
    g = "<g data-bb='tufts'>" + ''.join(F.tuft(float(x), float(y) + 5) for x, y in cs) + '</g>'
    return doc[:m.start()] + g + doc[m.end():], len(cs)
def menu(doc, t):
    d, nt = tufts(doc); a, b, c = SKY[t]
    n = d.count(STOPS); assert n >= 1; d = d.replace(STOPS, f"<stop stop-color='{a}'/><stop offset='.5' stop-color='{b}'/><stop offset='1' stop-color='{c}'/>")
    assert d.count('Good morning!</div>') == 1 and d.count('สวัสดีตอนเช้า!</div>') == 1
    d = d.replace('Good morning!</div>', GREET[t][0] + '</div>').replace('สวัสดีตอนเช้า!</div>', GREET[t][1] + '</div>')
    sun = "<circle data-bb='sun' cx='195' cy='228' r='14' fill='#FFE27A' stroke='#E0A21A' stroke-width='1.5'/>"
    if sun in d: d = d.replace(sun, sun.replace("#FFE27A' stroke='#E0A21A", "#FF9F45' stroke='#D9762A" if t == 'e' else "#FFF3C4' stroke='#C9C2A0"))
    out, i, k = [], 0, 0
    for m in re.finditer(r"url\(#sk[2m]\)", d):
        j = d.find('</svg>', m.start()); assert '<svg' not in d[m.start():j]
        out.append(d[i:j] + f"<rect x='-500' y='-500' width='1500' height='2000' fill='{TINT[t]}' stroke='none' pointer-events='none' data-tod='{t}'/>"); i = j; k += 1
    out.append(d[i:]); return ''.join(out), n, (k, nt)
J = []
for v in ('M1', 'M3'):
    for b, (w, h) in (('390x844', (390, 844)), ('320x568', (320, 568))):
        src = B + f'src-snapshot/{v}-main-menu-{b}.html'
        for t in 'en':
            tag = f'menu-{v}-{t}-{b}'; d, n, k = menu(open(src).read(), t)
            p = B + f'html/{tag}.html'; open(p, 'w').write(d)
            J.append(dict(tag=tag, src=src, src_orig=V + f'round2/r2h/html/{v}-main-menu-{b}.html', src_md5=md5(src), html_md5=md5(p), w=w, h=h, loc='MENU', tod=t,
                          fixes=[f'sky-stops x{n}', f'sky-tint x{k[0]}', f'flowers -> tufts x{k[1]}', 'greeting', 'sun recolour' if '228' in d else 'no sun at this size'],
                          note=f'{v} concept (unpicked) at {"evening" if t=="e" else "night (greeting A: Good night!)"}'))
json.dump(dict(pointer_md5=PTR, paste_md5=PASTE, jobs=J), open(B + 'code/jobs-menu.json', 'w'), indent=1, ensure_ascii=False)
print(len(J), 'menu pages')
