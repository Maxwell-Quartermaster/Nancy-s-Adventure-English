# t439u (6:11 PM MDT): its 320 scene LAYOUTS are superseded (superseded-t439u/s320); stage_v608.py still imports this file for the approved 320x568 HUD and ask cards only.
# Watchman glitch hunt R9 (4:42 PM MDT): scenes A-H at 320x568 on the approved 320 zone layouts (Z.STOP320 / L320: hero hx 100, feet 446, k .8,
# five targets on the approved 3+2 slots), plus C at N = 10 (the most Count it can ask, :229) to prove ten cows fit above the card.
# Same strings and rules as the 390 scenes (scenes_v608.py); only the coordinates change. Targets 44 pt+, 8 px apart, clear of the hero and card.
import os, sys, re, json
os.environ['NAE_SE'] = '1'; sys.argv = ['x']
sys.path.insert(0, '/workspace/v608build/screens'); import play_v608 as PV
Z, tx, obj, fr, W, H, S = PV.Z, PV.tx, PV.obj, PV.fr, PV.W, PV.H, PV.S
assert (W, H) == (320, 568)
D = json.load(open('/workspace/nancys-adventure-english-v6-08-cards.json')); C = {c['id']: c for c in D['cards']}; U = D['uiText']
OUT = '/workspace/v608build/scenes/s320/'
def emo(ch, x, y, sz, name, shadow=True, water=False, tap=True, fs=None):
    s = ''
    if shadow: s = f"<div class='abs' style='left:{x+sz*.18:.0f}px;top:{y+sz-7:.0f}px;width:{sz*.64:.0f}px;height:10px;border-radius:50%;background:rgba(16,23,15,.22)'></div>"
    if water: s = f"<div class='abs' style='left:{x+sz*.05:.0f}px;top:{y+sz-8:.0f}px;width:{sz*.9:.0f}px;height:10px;border-radius:50%;border:2px solid #CFE6F5;box-sizing:border-box'></div>"
    t = "data-tap=1 role='button' " if tap else ''
    return s + (f"<div class='abs' {t}data-name='{name}' aria-label='{name}' style='left:{x}px;top:{y}px;width:{sz}px;height:{sz}px;"
                f"display:flex;align-items:flex-end;justify-content:center;font-size:{fs or int(sz*.86)}px;line-height:1'>{ch}</div>")
def svg(b): return PV.P.svg(W, H, b)
def deco(h): return h.replace("data-tap=1 role='button' ", '', 1).replace("data-tap='1' role='button' ", '', 1)
def ask(en, th): return Z.qcard2(W, H, [tx(en, 'e20'), tx(th, 't17', 'line-height:1.7')])
def tp(cid): w_ = C[cid]['en']; return U['tapPrompt']['en'].replace('{word}', w_), U['tapPrompt']['th'].replace('{word}', w_)
def tag(x, y, en, w=88): return f"<div class='abs' style='left:{x}px;top:{y}px;z-index:3'>{fr(None, None, w, 48, '<div style=text-align:center>' + tx(en, 'e17 nw') + '</div>', 'gs6', face='#F6E9C8', tap=True, st=(), name='tag-'+en)}</div>"
ALL = ('kite', 'bus stop', 'bench', 'book', 'flower', 'cow', 'hat', 'gate', 'basket', 'bicycle', 'disc', 'tie', 'towel', 'desk', 'crib', 'owl', 'lantern', 'tent', 'mushroom', 'bridge')
def scene(key, tod=None, sun=(-100, 70)):
    _s = Z.sky
    if tod: Z.sky = lambda w_, h_, t_, s_: _s(w_, h_, tod, sun)
    try: b, g = PV.base(key, 'ask', hide=ALL)
    finally: Z.sky = _s
    return b
def A():   # Word Meadow, evening park by a pond (ship, rock, bread on the bench, rain, shop)
    b = scene('meadow', 'e')
    b += svg("<ellipse cx='52' cy='346' rx='42' ry='14' fill='#5C8FC4' stroke='#3F6F9E' stroke-width='2'/><path d='M28 344h14M58 350h16' stroke='#CFE6F5' stroke-width='2'/>")
    b += emo('🚢', 28, 300, 48, 'ship', shadow=False, water=True) + emo('🌧️', 232, 120, 52, 'rain', shadow=False) + emo('🏪', 252, 232, 48, 'shop')
    b += deco(obj('bench', 196, 380, 96, 58)) + emo('🍞', 222, 340, 44, 'bread', shadow=False) + emo('🪨', 24, 396, 48, 'rock')
    return b + PV.top('meadow') + ask(*tp('ph-22'))
def B():   # listen and find: the standard park, the word not shown
    b, g = PV.base('meadow', 'ask')
    return b + PV.top('meadow') + Z.qcard2(W, H, [tx(U['listenFind']['en'], 'e20'), tx(U['listenFind']['th'], 't17 nw')])
def _count(n):
    b = scene('fields')
    spots = [(172, 128), (224, 128), (176, 184), (228, 184), (172, 240), (224, 240), (260, 296), (16, 128), (16, 184), (16, 240)][:n]
    for i, (x, y) in enumerate(spots): b += emo('🐄', x, y, 44, 'cow', shadow=True, fs=36, tap=False)
    pl = ''.join(fr(None, None, 80, 48, tx(C[c]['en'], 'e20 nw'), 'gs6', face='#F6E9C8', tap=True, st=(), name='plate') for c in (('nm-11', 'nm-10', 'nm-12') if n == 3 else ('nm-14', 'nm-15', 'nm-17')))
    pl = pl.replace("class='fr", "style='flex:none' class='fr") if False else pl
    lines = [tx(U['howManyCows']['en'], 'e20'), tx(U['howManyCows']['th'], 't17 nw'), f"<div style='display:grid;grid-template-columns:repeat(3,80px);gap:8px;margin-top:10px'>{pl}</div>"]
    return b + PV.top('fields') + PV.card(lines, 150, speaker=True, hint=True).replace('padding:6px 148px 6px 12px', 'padding:6px 12px 6px 12px;text-align:left')
def C3(): return _count(3)
def C10(): return _count(10)
def Dz():   # big or small: Sam holds the egg; a big and a small basket with word plates
    b = scene('fields'); k = .8; hx = 110; hy = 446 - 177 * k
    b += emo('🥚', int(hx + 86 * k - 22), int(hy + 64 * k - 44), 44, 'egg', shadow=False, tap=False)
    b += deco(obj('basket', 204, 352, 100, 88)) + deco(obj('basket', 30, 394, 52, 46))
    b += tag(210, 296, C['cs-23']['en']) + tag(16, 336, C['cs-24']['en'], 80)
    return b + PV.top('fields') + Z.qcard2(W, H, [tx(U['bigOrSmall']['en'], 'e20'), tx(U['bigOrSmall']['th'], 't17 nw')])
def E():   # front desk: door, key rack above it, truck on the road in the window, book on the shelf, counter at the right
    L = dict(PV.L320); L['objs'] = []; L['shelf'] = (226, 240, 80); L['pegs'] = []
    b = Z.room(W, H, L); base = L['base']; dh = 150; dy = base - dh
    a = (f"<path d='M14 {dy}h60v{dh}H14z' fill='#8E5730' stroke-width='3'/><path d='M21 {dy+9}h46v{dh*.42:.0f}H21zM21 {dy+dh*.5:.0f}h46v{dh*.44:.0f}H21z' fill='#A8653A' stroke='#6E4224' stroke-width='2'/>"
         f"<circle cx='64' cy='{dy+dh*.52:.0f}' r='3.5' fill='#FFCC33' stroke-width='2'/><path d='M32 {dy+14}h24v16H32z' fill='#FFCC33' stroke-width='2'/>"
         "<path d='M16 222h58v10H16z' fill='#8E5730' stroke-width='2.2'/><path d='M30 232v6q0 3 3 3M45 232v6q0 3 3 3M60 232v6q0 3 3 3' stroke-width='2.2' fill='none'/>"
         "<path d='M112 322q30-10 50-4t46-6v34H112z' fill='#5E9E4A' stroke='none'/><path d='M112 326h96v9H112z' fill='#C9B48A' stroke='none'/>"
         "<path d='M200 360h104v60H200z' fill='#B9733F' stroke-width='3'/><path d='M196 352h112v10H196z' fill='#8E5730' stroke-width='3'/>")
    b += svg(a) + f"<div class='abs' style='left:34px;top:{dy+13}px;width:20px;text-align:center;font:400 13px/18px \"Lilita One\";color:#10170F'>13</div>"
    b += emo('🔑', 22, 238, 44, 'keys', shadow=False, fs=22) + emo('🛻', 162, 286, 44, 'truck', shadow=False, fs=22) + emo('📖', 244, 196, 44, 'book', shadow=False)
    b += Z.hero('nancy', .8, 100, 446 - 177 * .8, 'sword1', 'ask')
    return b + PV.top('lake') + ask(C['ms-21']['en'], C['ms-21']['th'])
def F():   # Home Lake at night, the table set
    L = dict(PV.L320); L['objs'] = [('desk', 16, 343.9, 84, 84)]; L['shelf'] = (14, 240, 100); L['pegs'] = []
    b = Z.room(W, H, L).replace("fill='#F4A862'", "fill='#2B3A6B'").replace('#FFE27A', '#FFF3C4')
    b = deco(b) if "data-tap" in b else b
    b += svg("<path d='M196 380h108v8H196z' fill='#8E5730' stroke-width='3'/><path d='M206 388v32M294 388v32' stroke='#8E5730' stroke-width='6'/><path d='M192 376h116v5H192z' fill='#FFF8E1' stroke-width='2'/>")
    b += emo('🥐', 200, 332, 44, 'croissant') + emo('🍝', 256, 332, 44, 'spaghetti')
    b += emo('🍞', 16, 196, 44, 'bread', shadow=False) + emo('🥚', 68, 196, 44, 'eggs', shadow=False) + deco(obj('desk', 16, 343.9, 84, 84)) + emo('🍨', 30, 300, 44, 'sundae')
    b += Z.hero('nancy', .8, 100, 446 - 177 * .8, 'sword1', 'ask')
    return b + PV.top('lake') + ask(*tp('fd-08'))
def _duel(pics, dawn=False):
    b, g = PV.base('forest', 'ask', hide=('owl', 'lantern'))
    for n in ('mushroom', 'bridge', 'tent'): b = b.replace(f"data-tap=1 role='button' data-name='{n}'", f"data-name='{n}'")
    if dawn:
        mk = Z.mk
        for a_, c_ in ((mk(255, .34, .30), mk(130, .32, .42)), (mk(258, .26, .28), mk(150, .26, .52)), (mk(250, .30, .30), mk(140, .34, .30)), (mk(250, .34, .30), mk(140, .36, .34))): b = b.replace(a_, c_)
        b = re.sub(r"<circle cx='[0-9.]+' cy='[0-9.]+' r='2.4' fill='#FFF3A8' stroke='none'/>", '', b).replace("data-tod='n'", "data-tod='m'", 1)
    out = b + PV.guardian('echo', W - 120, g['feet']) + PV.top('forest') + PV.nameplate(*PV.u('echoKnight'), PV.TINT['echo'])
    t = lambda w_, ch: fr(None, None, 116, 60, f"<div style='display:flex;align-items:center;gap:4px'>{f'<div style=font-size:28px;line-height:1>{ch}</div>' if ch else ''}{tx(w_, 'e20 nw')}</div>", 'gs6', face='#F6E9C8', tap=True, st=(), name='tile')
    return out + PV.card([tx(PV.u('soundDuel')[0] + ' · ' + PV.u('soundDuel')[1], 't17', 'line-height:1.7'), f"<div style='display:flex;gap:10px;justify-content:center;margin:4px 0'>{''.join(t(w_, ch) for w_, ch in pics)}</div>"], 196, [PV.gbtn(*PV.u('hearItAgain'), 170)], speaker=True).replace('padding:6px 12px;box-sizing', 'padding:0 8px 6px;box-sizing')
def G(): return _duel([('ship', '🚢'), ('sheep', '🐑')])
def Hd(): sd = D['soundDuel']['pairs'][4]; return _duel([(sd['a'], ''), (sd['b'], '')], dawn=True)
M = {'A-meadow-evening-pond': A, 'B-meadow-listen-and-find': B, 'C-fields-count-it': C3, 'C10-fields-count-it-ten': C10, 'D-fields-big-or-small': Dz,
     'E-lake-front-desk': E, 'F-lake-night-table': F, 'G-forest-picture-duel': G, 'H-forest-dawn': Hd}
if __name__ == '__main__':
    only = sys.argv[1:] if len(sys.argv) > 1 else []
    for n, fn in M.items():
        doc = PV.page(W, H, fn()); assert 'Thai draft' not in doc
        f = f'{n}-320x568'; open(OUT + f'html/{f}.html', 'w').write(doc); S.shot(doc, OUT + f'png/{f}.png', W, H, 's320-' + n[:3]); print(f, flush=True)
