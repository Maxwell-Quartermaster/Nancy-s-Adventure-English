# t411u (Maxwell): screen 10 v6-06 rhythm, 320 m1 revert + centred speaker, 24/25 gap 10 at 390 (m1 gate). Pre-patch copy: play_v608.pre-t411u.py
# play_v608.py: copied from v607build/screens/play_v607.py (63310d10) by mk_play_v608.py; v6-08 cards, happy eyes (eyes_v608.apply) on every page from v604build/screens/play_v604.py (approved t385u). 390x844 code path unchanged; NAE_SE=1 renders 320x568 with clip-only fixes.
# v6-04 play-family screens (t378u): every screen is built FROM the approved t328u mock code (mock-t328u/find_t328u.py and the
# t320u/t312u/t308u helpers it imports, all read-only): scene (outdoor()/room()), hero() at the mock scale, obj(), hud() top-bar plates,
# P.stop_pill() zone chip, qcard()/qcard2() parchment ask card with the speaker, plus_pop(), P.burst(). Strings come from the v6-04 cards.
# Approved screens call find_t328u.screen() itself; extrapolated screens add only parchment cards/ribbons built with the same fr()/tx() frame.
import sys, json, re, os; sys.dont_write_bytecode = True
sys.path.insert(0, '/workspace/mock-t328u'); sys.path.insert(0, '/workspace/mock-t320u')
import find_t328u as Z, find_t320u as Q
from find_t328u import P, S, tx, obj, hud, qcard2, plus_pop, page, room, L320, L390, DR
from find_t320u import fr, qcard
sys.path.insert(0, '/workspace/v608build/eyes'); import eyes_v608 as EY
_page0 = page
# Watchman sweep P11 (:68): top bar 16 pt from both edges; Back, stars and flame shrink 4-8 pt each so the Level plate keeps its room
import find_t312u as F12
def hud16(w, stars=64, xp=.6):
    c = w == 320; bh = 62 if c else 74; m = 16
    bw, sw_, fd = (56, 62, 48) if c else (60, 76, 56)
    out = fr(m, 8, bw, bh, tx('Back', 'e15 nw' if c else 'e17 nw'), 'gs6', face='#D9D2C2', tap=True, st=(), name='back')
    out += fr(m+bw+8, 8, sw_, bh, tx(f'★ {stars}', ('e17' if c else 'e22') + ' nw'), 'gs6', face='#FFF0B8', st=(), name='stars')
    xx = m+bw+8+sw_+8; xw = w-m-fd-8-xx
    lab = (f"<div style='display:flex;gap:6px;align-items:baseline'>{tx('Lv 3', 'e17 nw')}</div>" if c else
           f"<div style='display:flex;gap:6px;align-items:baseline'>{tx('Level 3', 'e17 nw')}{tx('เลเวล 3', 't17 nw')}</div>")
    bar = (f"<div style='height:10px;border:2px solid #10170F;border-radius:6px;background:#E4DCC8;overflow:hidden;margin-top:2px'>"
           f"<div style='height:100%;width:{xp*100:.0f}%;background:#6D3CC9'></div></div>")   # Auditor recheck: XP Purple #6D3CC9 (spec :89)
    out += fr(xx, 8, xw, bh, f"<div style='width:100%;padding:0 8px;box-sizing:border-box'>{lab}{bar}</div>", 'gs6', face='#F6E9C8', st=(), name='level')
    return out + F12.flame_btn(w-m-fd, 8+(bh-fd)/2, fd)
F12.hud = Q.hud = Z.hud = hud = hud16
# Watchman re-walk V3 (5:12 PM MDT): 16 pt side margins at 320 (fields cow/gate/bicycle, forest tent/bridge) and the 390 footbridge
_m16 = {('fields', 'cow'): 204, ('fields', 'gate'): 16, ('fields', 'bicycle'): 208, ('forest', 'tent'): 16, ('forest', 'bridge'): 184}
for _k in ('fields', 'forest'):
    _hx, _kk, _ft, _ob = Z.STOP320[_k]; Z.STOP320[_k] = (_hx, _kk, _ft, [(o[0], _m16.get((_k, o[0]), o[1])) + tuple(o[2:]) for o in _ob])
Z.STOP390_BRIDGE = ('bridge', 224) + tuple(Z.STOP390_BRIDGE[2:])
# Watchman sweep P13 (:68): room desk and crib 16 pt from the screen edges (window, pot and shelf stay)
L390['objs'][:] = [('desk', 16, o[2], o[3], o[4]) if o[0] == 'desk' else ('crib', 238, o[2], o[3], o[4]) if o[0] == 'crib' else o for o in L390['objs']]
L320['objs'][:] = [('desk', 16, o[2], o[3], o[4]) if o[0] == 'desk' else o for o in L320['objs']]
def page(*a, **k): return EY.apply(_page0(*a, **k))[0]
_TPC = json.load(open('/workspace/nancys-adventure-english-v6-08-cards.json'))['uiText']['tapPrompt']   # instructor ccf506dc: {word} stays English in both
def _ask_lines(c, en, th):   # every ask card shows the real tapPrompt (en + th) and no "Thai draft" chip
    w_ = re.match(r'Where is the (.+)\?$', en).group(1)
    return [tx(_TPC['en'].replace('{word}', w_), 'e20' if c else 'e22', 'margin-bottom:%dpx' % (2 if c else 10)), tx(_TPC['th'].replace('{word}', w_), 't17', 'line-height:1.7;overflow-wrap:anywhere')]   # t411u: v6-06 10 rhythm; A2: Thai wraps
Z.ask_lines = Q.ask_lines = Q.F.ask_lines = _ask_lines
DR = ''
for _M in (Z, Q, Q.F): _M.DR = ''   # council t402u: no "Thai draft" chip anywhere in the renders
OUT = '/workspace/screens-v608/'
D = json.load(open('/workspace/nancys-adventure-english-v6-08-cards.json')); U = D['uiText']
C = {c['id']: c for c in D['cards']}
G = json.load(open('/workspace/v604build/screens/guardians.json'))   # dumped from mock-t346u/map_t346u.guardian() by dump_guardians.py
def u(k, **kw):
    en, th = U[k]['en'], U[k]['th']
    for a, b in kw.items(): en = en.replace('{%s}' % a, str(b)); th = th.replace('{%s}' % a, str(b))
    return en, th
SE = os.environ.get('NAE_SE') == '1'
W, H = (320, 568) if SE else (390, 844)   # 320x568: iPhone SE; every SE branch below fixes a clip only
SC = {'meadow': Z.STOP['meadow'], 'fields': Z.STOP['fields'], 'forest': Z.STOP['forest'], 'lake': Z.STOP['lake']}
WEAP_FIX = {'forest': 'sword1'}   # drift fix: the t328u forest mock gave Nancy a dagger; Option B (t360u) removed daggers
def base(key, pose='ask', objs=True, hide=(), shift=0, stars=64, xp=.6, hero=True):
    hn, wk, hx, k, feet, reach, target, ob, en, th, thok = SC[key]
    wk = WEAP_FIX.get(key, wk)
    if key == 'lake':
        L = L320 if SE else L390; k, hx, feet, ob = L['k'], L['hx'], L['feet'], L['objs']; body = room(W, H, L)
    else:
        if SE: hx, k, feet, ob = Z.STOP320[key]
        elif key == 'forest': ob = [o if o[0] != 'bridge' else Z.STOP390_BRIDGE for o in ob]
        body = Z.outdoor(W, H, key)
    hy = feet - 177*k - (6 if pose == 'cheer' else 0) + shift
    if hero: body += Z.hero(hn, k, hx, hy, wk, pose, happy=(pose == 'ask' and hn == 'sam'))
    if objs:
        for (nm, x, y, ow, oh) in ob:
            if nm not in hide: body += obj(nm, x, y, ow, oh)
    return body, dict(k=k, hx=hx, feet=feet, hn=hn, ob=ob)
def top(key, stars=64, xp=.6): return hud(W, stars, xp) + P.stop_pill(key, 78 if SE else 90)
def gbtn(en, th, wd=150, green=False, name='btn'):
    face = '#2E7D32' if green else '#FFE08A'; col = '#FFF8E1' if green else '#10170F'
    return fr(None, None, wd, 56, f"<div style='text-align:center'>{tx(en, 'e17 nw', 'color:'+col)}{tx(th, 't17 nw', 'color:'+col) if th else ''}</div>", 'gs6', face=face, tap=True, st=(), name=name)
def card(lines, ch, btns=(), glow=False, speaker=False, hint=False):
    m = 16; y = H - 8 - ch
    row = f"<div style='display:flex;gap:10px;justify-content:center;margin-top:8px'>{''.join(btns)}</div>" if btns else ''
    d_ = 64 if SE else 72; sp = (Q.F.speaker(8, 8) + (hintb(68, 8, d_) if hint else '')) if speaker else ''
    if speaker and not hint and lines: lines = [f"<div style='min-height:60px;padding:0 60px;display:flex;flex-direction:column;justify-content:center'>{lines[0]}</div>"] + list(lines[1:])   # the first line sits beside the speaker; nothing under it
    inner = f"<div style='padding:6px {12 + (68 + d_) if hint else 12}px 6px 12px;box-sizing:border-box;width:100%;text-align:center'>{''.join(lines)}{row}</div>{sp}"
    extra = 'box-shadow:0 0 0 4px #FFE27A,0 0 22px 8px rgba(255,204,51,.55),0 4px 0 #10170F;' if glow else ''
    return fr(m, y, W - 2*m, ch, inner, 'gs', face='#FFF0B8' if glow else '#F6E9C8', st=('top', 'bottom'), name='card', extra=extra).replace("class='face' style='", "class='face' style='display:block;position:relative;", 1)
# Watchman glitch hunt R2 (spec :227 + rule 5): the hint button sits in the scene card row beside the speaker: a 72 pt Aqua round button
# (64 pt at 568), thick metal rim, soft Aqua glow, leaf-heart icon, Ink; accessible label uiText.hintButton. 8 pt from the speaker, inside the margins.
_UH = json.load(open('/workspace/nancys-adventure-english-v6-08-cards.json'))['uiText']['hintButton']['en']
def hintb(right, top, d):
    ic = d * .5
    return (f"<div class='abs' data-tap=1 role='button' data-name='hint' aria-label='{_UH}' style='right:{right}px;top:{top:.0f}px;width:{d}px;height:{d}px;box-sizing:border-box;border-radius:50%;"
            f"background:#7FE0D0;border:4px solid #8C8F94;box-shadow:inset 0 0 0 2px #3A9C8F,0 0 10px 3px rgba(127,224,208,.55),0 3px 0 #10170F;display:flex;align-items:center;justify-content:center'>"
            f"<svg width='{ic:.0f}' height='{ic:.0f}' viewBox='0 0 32 32' fill='none' stroke='#10170F' stroke-width='2.6' stroke-linejoin='round' stroke-linecap='round'>"
            f"<path d='M16 28L5 17Q0 11 5 6.5T16 9q6-7 11-2.5t0 10.5z' fill='#FFF8E1'/><path d='M16 9q2-6 8-7-1 6-8 7z' fill='#5DBB63'/></svg></div>")
_qc2 = Q.qcard2
def qcard2(w, h, lines, btn='speaker', glow=False):
    s = _qc2(w, h, lines, btn, glow)
    if btn != 'speaker': return s
    c = w == 320; d = 64 if c else 72; ch = 104 if c else 112
    old = "<div class='abs' style='left:8px;top:50%;transform:translateY(-50%);right:68px'>"
    assert s.count(old) == 1
    return s.replace(old, hintb(68, (ch - 18 - d) / 2, d) + old.replace('right:68px', 'right:%dpx' % (68 + d + 8)), 1)
Q.qcard2 = Z.qcard2 = qcard2
def _spk(st):   # compact 44 pt speaker for 320 (t411u)
    return Q.F.speaker(0, 0).replace('right:0px;top:0px;width:52px;height:52px', st + ';width:44px;height:44px').replace("width='26' height='26'", "width='22' height='22'")
def _spk_slot(): return f"<div style='flex:1;min-width:60px;display:flex;justify-content:center;align-items:center'>{_spk('position:relative;flex:none')}</div>"
def ccard(lines, btns=(), speaker=False, ch=128):
    m = 16; y = H - 8 - ch
    col = f"<div style='display:flex;flex-direction:column;gap:8px;margin-left:8px'>{''.join(btns)}</div>" if btns else ''
    inner = f"<div style='display:flex;align-items:center;width:100%;padding:0 {4 if SE and speaker else 8}px;box-sizing:border-box'><div style='flex:1'>{''.join(lines)}</div>{col}{_spk_slot() if speaker and SE else (Q.F.speaker(0, 0).replace('right:0px;top:0px', 'position:relative;flex:none;margin-left:8px') if speaker else '')}</div>"
    return fr(m, y, W - 2*m, ch, inner, 'gs', face='#F6E9C8', st=('top', 'bottom'), name='card').replace("class='face' style='", "class='face' style='display:block;position:relative;", 1)
def sbtn(en, th, wd=118): return fr(None, None, wd, 54, f"<div style='text-align:center;line-height:1'>{tx(en, 'e15 nw')}{tx(th, 't17 nw', 'line-height:1.7')}</div>", 'gs6', face='#FFE08A', tap=True, st=(), name='btn')
def ribbon(en, th, y=150):   # same parchment toast as mock-t346u toast(), centred under the zone chip
    return (f"<div class='abs' data-txt=1 style='left:50%;transform:translateX(-50%);top:{y}px;white-space:nowrap;box-sizing:border-box;text-align:center;background:#FFF0B8;border:2px solid #10170F;"
            f"border-radius:12px;box-shadow:inset 0 0 0 2px #E8B84A,0 3px 0 #10170F;padding:2px 16px;z-index:5'>"
            f"<div style=\"font:400 22px/1.15 'Lilita One',sans-serif;color:#3A2410\">{en}</div><div style='font:400 17px/1.7 Kanit,Thonburi,sans-serif;color:#3A2410'>{th}</div></div>")
def tplate(pic, sz=104):   # t423u option A: framed 124 pt plate at the top right, clear of the hero (people / pictures that cannot stand)
    x, y = W - sz - 24, 234 if not SE else 150
    return (f"<div class='abs' data-pic='plate' style='left:{x}px;top:{y}px;width:{sz}px;height:{sz}px;display:flex;align-items:center;justify-content:center;box-sizing:border-box;background:#F6E9C8;border:3px solid #10170F;border-radius:18px;box-shadow:inset 0 0 0 3px #E8B84A,0 3px 0 #10170F;font:400 {int(sz*.6)}px/1 sans-serif'>{pic}</div>")
def gprop(pic, x, y, sz=64): return big(pic, x, y, sz).replace("<div class='abs'", "<div class='abs' data-pic='prop'", 1)   # t423u option C: a 64 pt prop standing on the ground with a contact shadow
def on_desk(pic, sz=56):   # t425u: food and objects stand on furniture (the room's desk top), a prop with a small shadow, never on the floor
    L = L320 if SE else L390; dx, dy, dw, dh = next((o[1], o[2], o[3], o[4]) for o in L['objs'] if o[0] == 'desk'); sz = 44 if SE else sz
    return gprop(pic, int(dx + (dw - sz)/2), int(dy + .19*dh - sz + 3), sz)   # the desk art's top surface sits 19% down its box
def big(inner, x, y, sz=120):   # an object drawn in the scene (no tile): emoji or svg, with a soft contact shadow
    return (f"<div class='abs' style='left:{x}px;top:{y}px;width:{sz}px;height:{sz}px;display:flex;align-items:center;justify-content:center;font-size:{int(sz*.78)}px;line-height:1'>{inner}</div>"
            f"<div class='abs' style='left:{x+sz*.15:.0f}px;top:{y+sz-6:.0f}px;width:{sz*.7:.0f}px;height:12px;border-radius:50%;background:rgba(16,23,15,.18)'></div>")
TINT = {'word': '#F5D06B', 'number': '#7FB8F5', 'gentle': '#F2B8A0', 'echo': '#7FE0D0'}
def guardian(kind, x, feet, k=1.1*1.2, kneel=False):
    # spec (t377u): an original armored figure in the hero rig, 1.2 H, in its zone tint with a round shield. Built from the mock hero rig.
    s = Q.A['sam'].replace("color='#3B689B'", f"color='{TINT[kind]}'").replace('#E3AE7E', '#A9B2BC').replace('#1F1A17', '#6F7A86').replace('#4A2E16', '#6F7A86').replace('#4E311B', '#6F7A86')
    s = s.replace("<g class='wp'/>", '').replace('<svg ', f"<svg width='{80*k:.1f}' height='{180*k:.1f}' style='overflow:visible;display:block' ", 1)
    helm = f"<svg class='abs' width='{80*k:.0f}' height='{60*k:.0f}' viewBox='0 0 80 60' style='left:0;top:{-6*k:.0f}px;overflow:visible'><path d='M22 30q0-26 18-26t18 26v6H22z' fill='#8E99A6' stroke='#10170F' stroke-width='3'/><path d='M24 26h32' stroke='#10170F' stroke-width='3'/><path d='M40 4v-6' stroke='{TINT[kind]}' stroke-width='5'/></svg>"
    shield = f"<svg class='abs' width='{40*k:.0f}' height='{40*k:.0f}' viewBox='-20 -20 40 40' style='left:{-8*k:.0f}px;top:{78*k:.0f}px'><circle r='17' fill='{TINT[kind]}' stroke='#10170F' stroke-width='3'/><circle r='9' fill='none' stroke='#E8B84A' stroke-width='3'/><circle r='3' fill='#E8B84A'/></svg>"
    y = feet - 177*k
    sh = f"<div class='abs' style='left:{x+14*k:.0f}px;top:{feet-6:.0f}px;width:{52*k:.0f}px;height:12px;border-radius:50%;background:rgba(16,23,15,.22)'></div>"
    tf = f"transform:scaleX(-1){' translateY(%dpx) scaleY(.82)' % (18*k) if kneel else ''};"
    return sh + f"<div class='abs' style='left:{x:.0f}px;top:{y:.0f}px;width:{80*k:.0f}px;height:{180*k:.0f}px;{tf}'>{s}{helm}{shield}</div>"
def hpbar(name_en, name_th, frac, tint, y=150):
    return (f"<div class='abs' style='left:{W-196}px;top:{y}px;width:180px;z-index:4'>"
            f"<div data-txt=1 style='background:{tint};border:2px solid #10170F;border-radius:10px 10px 0 0;padding:0 8px;text-align:center'>{tx(name_en, 'e15 nw')}{tx(name_th, 't17 nw')}</div>"
            f"<div style='height:14px;border:2px solid #10170F;border-top:0;border-radius:0 0 8px 8px;background:#E4DCC8;overflow:hidden'><div style='height:100%;width:{frac*100:.0f}%;background:{tint}'></div></div></div>")   # Watchman R1: the zone tint, nothing red (rule 9)
def nameplate(name_en, name_th, tint, y=150):   # R1: Sound Duel has no health bar (section 12); the Echo Knight's name plate only
    return hpbar(name_en, name_th, 0, tint, y).replace("border-radius:10px 10px 0 0", "border-radius:10px").split("<div style='height:14px")[0] + '</div>'
def plates(ch, wrong=None, right=None, h=52, wd=160, cls=None):   # 2x2 answer plates inside the parchment card (6.4 plates, parchment, Ink)
    out = ''
    for c in ch:
        f = '#FFF0B8' if c == right else ('#E9E2D2' if c == wrong else '#F6E9C8')
        out += fr(None, None, wd, h, (tx(c, cls, 'text-align:center;padding:0 6px;line-height:1.15') if cls else tx(c, 'e20 nw' if wd > 150 else 'e15 nw')), 'gs6', face=f, tap=True, st=(), name='plate')
    return f"<div style='display:grid;grid-template-columns:{wd}px {wd}px;gap:{8 if SE else 10}px;justify-content:center;margin-top:6px'>{out}</div>"
SCR = {}
def add(n, slug, status, src, fn): SCR[n] = (slug, status, src, fn)
# ---------------- approved mocks (t328u screen() itself) ----------------
def approved(key, mode):
    b = Z.screen(key, mode, W, H)
    if key == 'forest': b = Z.screen.__wrapped__(key, mode) if hasattr(Z.screen, '__wrapped__') else b
    return b
def meadow_ask(): return Z.screen('meadow', 'ask', W, H)
def meadow_right():
    hn, wk, hx, k, feet, reach, target, objs, en, th, thok = Z.STOP['meadow']
    old = Z.qcard2(W, H, [tx(f'Yes! That is the {target}.', 'e22'), tx('You got a star.', 'e17'), tx(thok + DR, 't17 nw')], btn='next')
    doc = Z.screen('meadow', 'correct', W, H); assert doc.count(old) == 1
    return doc.replace(old, Z.qcard2(W, H, Z.ask_lines(SE, en, th)))
def fields_ask(): return Z.screen('fields', 'ask', W, H)
def lake_ask(): return Z.screen('lake', 'ask', W, H)
add(10, 'word-meadow-scene', 'approved mock', 'Q-shot-t328u-meadow-ask-390x844.png', meadow_ask)
add(11, 'word-meadow-scene-right', 'approved mock', 'Q-shot-t328u-meadow-correct-390x844.png', meadow_right)
add(31, 'golden-fields-scene', 'approved mock', 'Q-shot-t328u-fields-ask-390x844.png', fields_ask)
add(32, 'home-lake-scene', 'approved mock', 'Q-shot-t328u-lake-ask-390x844.png', lake_ask)
# ---------------- extrapolated from the same components ----------------
def reveal_right():
    b, g = base('meadow', 'cheer', hide=('kite',))
    c = C['ph-07']; e = D['encouragement'][0]
    return (b + gprop(c['pic'], 262, 452) + top('meadow', 65, .68) + ribbon(e['en'], e['th']) +
            card([tx(c['en'].upper(), 'e22'), tx(c['respell'], 'e15', 'color:#8A6200'), tx(c['th'], 't17 nw'), tx(u('sayItOutLoud')[0] + ' · ' + u('sayItOutLoud')[1], 'e15', 'font-family:Kanit,Thonburi,sans-serif;font-size:17px;line-height:1.7')], 214,
                 [gbtn(*u('replay'), 130), gbtn(*D['gotItText'].values(), 130)]))
add(12, 'reveal-right', 'extrapolated', 'Q-shot-t328u-meadow-correct (scene, cheer pose, hud, chip) + qcard frame', reveal_right)
def retry():
    hn, wk, hx, k, feet, reach, target, ob, en, th, thok = SC['meadow']
    b = Z.screen('meadow', 'try', W, H).replace(Z.qcard2(W, H, [tx(en, 'e22'), tx('Almost! Look up in the sky.', 'e17'), tx('เกือบแล้ว! ลองมองขึ้นไปบนฟ้า' + DR, 't17 nw')], btn=None, glow=True), '')
    w_ = D['wrongText']; e = D['encouragement'][3]
    kb = next(o for o in ob if o[0] == 'kite'); hint = f"<div class='abs' style='left:{kb[1]-8}px;top:{kb[2]-8}px;width:{kb[3]+16}px;height:{kb[4]+16}px;border-radius:50%;box-shadow:0 0 0 3px #FFE27A,0 0 18px 6px rgba(255,204,51,.55);opacity:.85;pointer-events:none'></div>"
    return b + hint + qcard2(W, H, [tx(e['en'], 'e20'), tx(e['th'], 't17 nw'), tx(u('tapPrompt', word='kite')[0], 'e17'), tx(u('tapPrompt', word='kite')[1], 't17 nw')], btn=None, glow=True)
add(13, 'word-meadow-scene-retry', 'extrapolated', "t328u screen('meadow','try'): wiggle + glow card; grace line = encouragement 'Take your time.' (gap 3)", retry)
def miss_reveal():   # R2 (Auditor staged recheck): the trapNote ribbon line carries Thai, so 17 px / lh 1.7
    b, g = base('lake', 'ask', hide=('crib',)); b = b.replace("data-tap=1 role='button' ", ''); b += kit_table(); c = C['fd-29']; w_ = D['wrongText']
    return (b + top('lake') + ribbon(w_['en'], w_['th'], 116 if SE else 150) + ribbon(c['trapNote'], c['th'], 186 if SE else 236).replace("font:400 22px/1.15","font:400 17px/1.7").replace('white-space:nowrap', 'white-space:normal;width:%dpx' % (W - 32) if SE else 'white-space:nowrap') +
            ccard([tx(c['en'], 'e15'), tx(c['answer'], 'e20')], [sbtn(*u('replay')), sbtn(*D['gotItText'].values())]))
add(14, 'reveal-gentle-retry', 'extrapolated', 'lake template (room, Nancy ask, hud, chip) + parchment card', miss_reveal)
def kit_table():   # spec :229: a Kitchen run swaps the crib for a small table (Instructor sweep 2 #8)
    L = L320 if SE else L390; cx, cy, cw, ch_ = next((o[1], o[2], o[3], o[4]) for o in L['objs'] if o[0] == 'crib'); ty = cy + ch_ * .45; tw = cw * .8; tx0 = cx + cw * .1
    return (f"<svg class='abs' style='left:0;top:0' width='{W}' height='{H}'><g stroke='#10170F' stroke-width='3' stroke-linejoin='round'>"
          f"<ellipse cx='{tx0+tw/2:.0f}' cy='{cy+ch_:.0f}' rx='{tw/2:.0f}' ry='4' fill='#10170F' opacity='.2' stroke='none'/>"
          f"<path d='M{tx0+8:.0f} {ty+10:.0f}v{cy+ch_-ty-12:.0f}M{tx0+tw-8:.0f} {ty+10:.0f}v{cy+ch_-ty-12:.0f}' stroke-width='6' stroke='#8E5730'/><path d='M{tx0+8:.0f} {ty+10:.0f}v{cy+ch_-ty-12:.0f}M{tx0+tw-8:.0f} {ty+10:.0f}v{cy+ch_-ty-12:.0f}' fill='none'/>"
          f"<path d='M{tx0:.0f} {ty:.0f}h{tw:.0f}v12h-{tw:.0f}z' fill='#B9733F'/></g></svg>")
def sayit(cid, key, shown=True, reply=False):
    kit = cid.startswith('fd-'); b, g = base(key, 'ask', hide=('crib',) if (kit or reply) else ()); c = C[cid]   # R4: the reply card needs the room; the crib steps out (no overlap with the buttons)
    if kit: b += kit_table()
    pic = c.get('pic') if c.get('pic') and not str(c.get('pic')).startswith('svg:') else None
    out = b + (on_desk(pic) if pic else '') + top(key)
    lines = ([tx(c['en'], 'e22'), tx(c['respell'], 'e15'), tx(c['th'], 't17')] if shown else [tx(c['th'], 't17')])
    if reply: lines += [tx(c['reply']['en'], 'e15', 'margin-top:6px'), tx(c['reply']['th'], 't17')]   # the answer, small, under the question; no speaker label (sweep 2 #5)
    if reply and SE: return out + card(lines, 262, [sbtn(*u('replay'), 118), sbtn(*D['gotItText'].values(), 118)])   # R4: at 320 the buttons go under the text so the reply Thai is never cut
    if key == 'lake': return out + ccard(lines, [sbtn(*u('replay'), 100 if SE else 118), sbtn(*D['gotItText'].values(), 100 if SE else 118)] if shown else [sbtn(*u('continue'), 100 if SE else 118)], speaker=not shown, ch=(250 if reply else 176 if SE and len(c['en']) > 16 else 128))
    return out + card(lines, 196, [gbtn(*u('replay'), 110), gbtn(*D['gotItText'].values(), 110)] if shown else [], speaker=True)
add(15, 'say-it-sight-words', 'extrapolated', 'meadow template + parchment card with speaker', lambda: sayit('sw-03', 'meadow'))
add(16, 'say-it-maxwell-says-day1', 'extrapolated', 'lake template + parchment card with speaker', lambda: sayit('ms-01', 'lake'))
add(20, 'kitchen-say-it-picture-first', 'extrapolated', 'lake template; picture in the scene, card shows Thai first', lambda: sayit('fd-02', 'lake', shown=False))
add(21, 'kitchen-say-it-shown', 'extrapolated', 'lake template + parchment card', lambda: sayit('fd-02', 'lake'))
add(33, 'say-it-baby-hospital-reply', 'extrapolated', "lake template + card with Maxwell's reply", lambda: sayit('bh-11', 'lake', reply=True))
def svgpic(fn):
    t = open('/workspace/asset-library/assets/card-pictures/' + fn, encoding='utf-8').read(); t = re.sub(r'<\?xml[^>]*>', '', t)
    return re.sub(r'<svg\b', "<svg width='100' height='100'", t, count=1)
def picplate(fn, x, y, sz=124, emo=None):
    return (f"<div class='abs' style='left:{x}px;top:{y}px;width:{sz}px;height:{sz}px;display:flex;align-items:center;justify-content:center;box-sizing:border-box;background:#F6E9C8;border:3px solid #10170F;border-radius:18px;box-shadow:inset 0 0 0 3px #E8B84A,0 3px 0 #10170F;line-height:1'>{svgpic(fn) if fn else f'<span style=\"font:400 76px/1 sans-serif\">{emo}</span>'}</div>"
            f"<div class='abs' style='left:{x+sz*.15:.0f}px;top:{y+sz-6:.0f}px;width:{sz*.7:.0f}px;height:12px;border-radius:50%;background:rgba(16,23,15,.18)'></div>")
def twoans(state):
    b, g = base('lake', 'cheer' if state == 'right' else 'ask', hide=('disc',)); c = C['ms-31']   # the disc sat 2 pt from the Pray plate; scenery only here
    pr = picplate(None, 63, 202, emo=c['choices'][0]['pic'] if isinstance(c['choices'][0], dict) else '🙏'); hf = picplate(None, 243, 202, emo=c['choices'][1]['pic'] if isinstance(c['choices'][1], dict) else '🙌')   # H1 (t406u): hand emoji on the same bordered plate
    glow = "<div class='abs' style='left:%dpx;top:202px;width:124px;height:124px;border-radius:18px;box-shadow:0 0 0 4px #FFE27A,0 0 26px 10px rgba(255,204,51,.6);z-index:2'></div>"
    x = ''
    if state == 'wrong': x = glow % 243 + "<div class='abs' style='z-index:2;left:280px;top:238px;font:400 60px/1 sans-serif;color:#9AA7B5;opacity:.8'>✕</div>"
    if state == 'right': x = glow % 63
    lines = [tx(c['en'].split(' / ')[0], 'e22'), tx(c['th'].split(' / ')[0], 't17')]
    btns = [] if state != 'right' else [gbtn(*u('done'), 120, True)]
    lab = lambda xx, k_: f"<div class='abs' style='left:{xx}px;top:334px;z-index:3'>{fr(None, None, 120, 48, tx(*[u(k_)[0]], 'e17 nw') , 'gs6', face='#F6E9C8', tap=True, st=(), name=k_)}</div>"
    return b + x + pr + hf + lab(65, 'pray') + lab(245, 'highFive') + top('lake') + ccard(lines, btns, speaker=True)
add(17, 'two-answer-pray-high-five', 'extrapolated', 'lake template; the two answers drawn in the scene + parchment card', lambda: twoans('ask'))
add(18, 'two-answer-wrong-tap', 'extrapolated', 'as 17, Moonstone X + Gold glow', lambda: twoans('wrong'))
add(19, 'two-answer-right-done', 'extrapolated', 'as 17, cheer pose, Done in the green main spot', lambda: twoans('right'))
def server():
    b, g = base('lake', 'ask', hide=('crib',)); b = b.replace("data-tap=1 role='button' ", ''); b += kit_table(); c = C['fd-29']
    return (b + top('lake') + ribbon(u('serverAsks')[0] + ': ' + c['en'], u('serverAsks')[1] + ' ' + c['th'], 150).replace("font:400 22px","font:400 18px").replace('white-space:nowrap', 'white-space:normal;width:%dpx' % (W - 32 if SE else 340)) +
            ccard([plates(c['choices'], h=48, wd=128, cls='e15') if not SE else plates(c['choices'], h=48, wd=104, cls='e15')], speaker=True, ch=(140 if SE else 128)))
add(22, 'kitchen-server-talk', 'extrapolated', 'lake template + parchment card with the 4 reply plates', server)
def levelup():   # resweep flag: the gem's centre facet had no fill (drew black); now a light green facet
    b, g = base('meadow', 'cheer', objs=False)
    return (b + P.svg(W, H, (P.burst(236, 252, 56) if SE else P.burst(270, 330, 80)).replace("data-behind='hero'", "data-behind='all'")) + big("<svg width='96' height='96' viewBox='0 0 40 40' stroke='#10170F' stroke-width='2.2' stroke-linejoin='round'><path d='M10 8h20l7 9-17 18L3 17z' fill='#2FAF5A'/><path d='M3 17h34M14 8l-4 9 10 18 10-18-4-9' fill='#7FD38B' stroke-width='1.3'/></svg>", *((196, 212, 80) if SE else (222, 280, 110)))   # 320 (gate nit): gem and burst clear of the edge and the card
            + top('meadow', 66, .05) + ribbon(D['rewardText']['en'], D['rewardText']['th']) + card([tx('Level 2 · เลเวล 2', 'e22', 'line-height:1.7'), tx('Green gem · อัญมณีสีเขียว', 't17')], 184 if SE else 200, [gbtn(*u('wearIt'), 120), gbtn(*D['gotItText'].values(), 120)]))
add(23, 'level-up-reward', 'extrapolated', 'meadow template, cheer pose, burst + ribbon + parchment card', levelup)
z_sw = next(z for z in D['zones'] if z['key'] == 'sight-words'); BN = z_sw['boss']['name']
def grun(cid, frac, hint=None, kneel=False):
    b, g = base('meadow', 'cheer' if kneel else 'ask', objs=False)
    c = C[cid]
    out = b + guardian('word', 236, 625, kneel=kneel) + tplate(c['pic']) + top('meadow') + hpbar(BN['en'], BN['th'], frac, TINT['word'])
    if kneel:
        return out + ribbon(D['encouragement'][2]['en'], D['encouragement'][2]['th'], 290) + card([tx(c['en'].upper(), 'e22'), tx(c['th'], 't17')], 200, [gbtn(*D['gotItText'].values(), 130)])
    lines = [tx(c['th'], 't17 nw'), plates(c['choices'])]
    if hint == 'letters': lines = [tx(c['en'][:1] + '_' * (len(c['en']) - 1) + ' /th/', 'e20'), tx(u('itStartsWith')[1], 't17', 'line-height:1.7')] + lines   # V2: Thai on its own 1.7 line
    if hint == 'jesus':
        j = D['jesusWords'][0]
        out += (f"<div class='abs' style='left:16px;top:250px;width:250px;z-index:6;box-sizing:border-box;background:#FFF0B8;border:2px solid #10170F;border-radius:14px;box-shadow:inset 0 0 0 3px #E8B84A,inset 0 0 0 4px #10170F,0 4px 0 #10170F;padding:10px 12px'>"
                + tx(u('jesusWords')[0] + ' · ' + j['ref'], 'e15') + tx(j['en'], 'e15') + tx(j['th'], 't17') + '</div>')
    return out + card(lines, 196 if hint != 'letters' else 228)
add(24, 'guardian-run-entry', 'extrapolated', 'meadow template + guardian (hero rig, 1.2 H, zone tint, round shield; gap 1) + bar + 2x2 plates in the card', lambda: grun('sw-15', 1.0))
add(25, 'guardian-hint-letters', 'extrapolated', 'as 24 + letters hint line', lambda: grun('sw-19', .6, 'letters'))
add(26, 'guardian-hint-jesus-words', 'extrapolated', 'as 24 + Words of Jesus parchment bubble', lambda: grun('sw-19', .6, 'jesus'))
add(27, 'guardian-kneels', 'extrapolated', 'as 24, bar empty, guardian kneels, cheer pose', lambda: grun('sw-19', 0, kneel=True))
def gwin():
    b, g = base('meadow', 'cheer', objs=False)
    return (b + guardian('word', 236, 625, kneel=True) + top('meadow') + ribbon(D['rewardText']['en'], D['rewardText']['th']) +
            card([tx(BN['en'], 'e22'), tx(BN['th'], 't17')], 180, [gbtn(*D['gotItText'].values(), 130)]))
add(28, 'guardian-win', 'extrapolated', 'gap 2: kneeling guardian + boss.name, then the scroll', gwin)
def scroll(reopen=False):
    b, g = base('meadow', 'cheer', objs=False); s = z_sw['boss']['scroll']
    rb = u('scrolls') if reopen else u('verseGift')
    btn = [gbtn(*u('toMap'), 140)] if reopen else []
    return (b + top('meadow') + ribbon(*rb) + card([tx(s['ref'], 'e20'), tx(s['en'], 'e15', 'font-size:18px;line-height:1.35'), tx(s['th'], 't17'), tx('ESV · THSV11', 'e15'), tx(u('askMax')[0], 'e15'), tx(u('askMax')[1], 't17')], 540, btn + [gbtn(*D['gotItText'].values(), 120)]))
add(29, 'verse-scroll-gift', 'extrapolated', 'meadow template + tall parchment card', scroll)
add(44, 'scroll-reopened', 'extrapolated', 'as 29 with Scrolls banner + Back to Map', lambda: scroll(True))
def weapon_gift():
    b, g = base('meadow', 'cheer', objs=False)
    ax = "<svg width='110' height='110' viewBox='-30 -60 60 80'><path d='M-3 18v-72h6v72z' fill='#B07A42' stroke='#10170F' stroke-width='2.5'/><path d='M3-56c16-6 27 4 27 24c-9-6-18-6-27 0z' fill='#C9CED6' stroke='#10170F' stroke-width='2.5'/><path d='M-3-50l-11 6 11 6z' fill='#8A939C' stroke='#10170F' stroke-width='2.5' stroke-linejoin='round'/></svg>"
    return (b + top('meadow') + ribbon(*u('weaponNew')) +
            card(["<div style='display:flex;justify-content:center'>" + ax.replace("width='110' height='110'", "width='84' height='84'") + "</div>", tx('Oak Axe', 'e22'), tx(u('giftFrom', g=re.sub(r'^The ', 'the ', BN['en']))[0], 'e15'), tx(u('giftFrom', g=BN['th'])[1], 't17'), tx('Steadfast · Isaiah 41:10', 'e15')], 290, [gbtn(*u('weaponUse'), 150), gbtn(*D['gotItText'].values(), 110)]))
add(30, 'new-weapon-gift', 'extrapolated', 'meadow template + weapon in the scene + parchment card', weapon_gift)
def duel(state):
    b, g = base('forest', 'cheer' if state else 'ask', hide=('owl', 'lantern'))
    sd = D['soundDuel']['pairs'][0]
    for n_ in ('mushroom', 'bridge', 'tent'): b = b.replace(f"data-tap=1 role='button' data-name='{n_}'", f"data-name='{n_}'")   # R6: Sound Duel scenery is not a target
    out = b + (guardian('echo', W - 120, g['feet']) if SE else guardian('echo', 236, 640)) + top('forest') + nameplate(*u('echoKnight'), TINT['echo'])
    if state == 'done':
        return out + ribbon(*u('roundDone')) + card([tx('+30 XP', 'e22')], 170, [gbtn(*D['gotItText'].values(), 130)])
    t = lambda w_, on: fr(None, None, 116 if SE else 150, 64, tx(w_, 'e22 nw'), 'gs6', face='#FFF0B8' if on else '#F6E9C8', tap=True, st=(), name='tile', extra='box-shadow:0 0 0 4px #FFE27A,0 0 18px 6px rgba(255,204,51,.6);' if on else '')
    if SE:   # t411u: v6-06 button width (140) and a compact 44 pt speaker centred in its own slot right of the button row, >= 8 px clear
        row = f"<div style='display:flex;align-items:center;margin:8px -8px 0'><div style='flex:1'></div>{gbtn(*u('hearItAgain'), 140)}<div style='flex:1;display:flex;justify-content:center'>{_spk('position:relative;flex:none')}</div></div>"
        return out + card([tx(u('soundDuel')[0] + ' · ' + u('soundDuel')[1], 't17', 'line-height:1.7'), f"<div style='display:flex;gap:12px;justify-content:center;margin:6px 0'>{t(sd['a'], state == 'right')}{t(sd['b'], False)}</div>", row], 220)
    return out + card([tx(u('soundDuel')[0] + ' · ' + u('soundDuel')[1], 't17', 'line-height:1.7'), f"<div style='display:flex;gap:12px;justify-content:center;margin:6px 0'>{t(sd['a'], state == 'right')}{t(sd['b'], False)}</div>"], 220, [gbtn(*u('hearItAgain'), 170)], speaker=True).replace('right:8px;top:8px', 'right:8px;bottom:8px' if SE else 'right:8px;top:8px', 1)
add(34, 'echo-forest-sound-duel', 'extrapolated', 'Q-shot-t328u-forest scene (night woods, Nancy, sword not dagger) + Echo Knight (gap 1) + parchment card', lambda: duel(None))
add(35, 'sound-duel-right', 'extrapolated', 'as 34, cheer pose, Gold glow tile', lambda: duel('right'))
add(36, 'sound-duel-round-done', 'extrapolated', 'as 34, roundDone ribbon + card', lambda: duel('done'))
def rest():
    b = Z.outdoor(W, H, 'meadow')
    ev = "<div class='abs' style='left:0;top:0;width:390px;height:844px;background:linear-gradient(#4F64A8 0%,#F4A862 45%,rgba(244,168,98,0) 60%);opacity:.72'></div>"   # t288u evening sky (gap 17)
    hn, wk, hx, k, feet, *_ = SC['meadow']
    b += ev + Z.hero(hn, k, hx, feet - 177*k, wk, 'cheer')
    v = D['restScreen']
    return (b + top('meadow') + ribbon(v['en'], v['th'], 150).replace('white-space:nowrap', 'white-space:normal;width:340px') +
            card([tx('Matthew 11:28', 'e20'), tx('“Come to me, all who labor and are heavy laden, and I will give you rest.”', 'e15', 'font-size:18px'), tx('ESV · THSV11', 'e15')], 260, [gbtn(*u('keepGoing'), 140), gbtn(*u('restNow'), 140)]))
add(37, 'rest-screen', 'extrapolated', 'gap 17: the evening sky (t288u palette) over the meadow scene + parchment card', rest)
def paused():
    b = Z.screen('meadow', 'ask', W, H)
    dim = "<div class='abs' style='left:0;top:0;width:390px;height:844px;background:rgba(16,23,15,.45);z-index:20'></div>"
    btn = f"<div class='abs' style='left:95px;top:390px;z-index:21'>{gbtn(*u('continue'), 200)}</div>"
    return b + dim + btn
add(48, 'continue-after-pause', 'extrapolated', "t328u meadow ask under a dim layer + one Continue button", paused)
# Phrase/sentence ask card (B1 sentence path; Watchman missing render): a card whose en is a phrase shows its own en and th, never the template
def phrase_ask():
    b, g_ = base('lake', 'ask'); c = C['cs-03']
    return b + top('lake') + Z.qcard2(W, H, [tx(c['en'], 'e22'), tx(c['th'], 't17 nw')])
SCR[54] = ('phrase-ask-card', 'extrapolated', 'lake template; cs-03 "a white towel" shows its own text (B1 rule: starts with "a ")', phrase_ask)
if __name__ == '__main__':
    only = [int(x) for x in sys.argv[1:]]
    for n, (slug, st, src, fn) in sorted(SCR.items()):
        if only and n not in only: continue
        doc = page(W, H, fn()); open(OUT + f'html/{n:02d}-{slug}' + ('-320x568' if SE else '-390check') + '.html', 'w').write(doc)
        S.shot(doc, OUT + f'png/{n:02d}-{slug}' + ('-320x568' if SE else '-390check') + '.png', W, H, f'v608-{n}')
        print(n, slug, st, flush=True)


def se_zone():   # the t376u zone template at 320x568: the mock's own screen() at SE size, all 4 zones
    for key in ('meadow', 'fields', 'lake', 'forest'):
        doc = page(320, 568, Z.screen(key, 'ask', 320, 568)); open(OUT + f'html/zone-{key}-ask-320x568.html', 'w').write(doc)
        S.shot(doc, OUT + f'png/zone-{key}-ask-320x568.png', 320, 568, f'v608-zone-{key}'); print('zone', key, flush=True)
