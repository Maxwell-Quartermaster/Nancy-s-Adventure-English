# v6-08 scene renders (Maxwell approved t401u A-H; council 3:55 PM MDT): built from mocks-scene-variety-t401u/src/mocks.py (read-only) on the v6-08 harness
# (play_v608: v6-08 cards, Sam = Nancy's happy eyes, no Thai draft chip). All new Thai comes from the v6-08 uiText (Instructor 7057dde4, NEEDS NANCY).
import sys, os, json
s = open('/workspace/mocks-scene-variety-t401u/src/mocks.py', encoding='utf-8').read()
s = s[:s.index("if __name__ == '__main__':")]
U8 = json.load(open('/workspace/nancys-adventure-english-v6-08-cards.json'))['uiText']
for a, b in [("sys.path.insert(0, '/workspace/v604build/screens')", "sys.path.insert(0, '/workspace/v608build/screens'); sys.argv = ['x']"),
             ("import play_v604 as PV\nfrom play_v604 import", "import play_v608 as PV\nfrom play_v608 import"),
             ("nancys-adventure-english-v6-07-cards.json", "nancys-adventure-english-v6-08-cards.json"),
             ("OUT = '/workspace/mocks-scene-variety-t401u/'", "OUT = '/workspace/v608build/scenes/'"),
             ("TP = {'en': D['uiText']['tapPrompt']['en'], 'th': '{word} อยู่ที่ไหน'}", "TP = D['uiText']['tapPrompt']"),
             ("tx('Listen. Where is it?', 'e22'), tx('ฟังแล้วหาดูนะ' + DR, 't17 nw')", "tx(D['uiText']['listenFind']['en'], 'e22'), tx(D['uiText']['listenFind']['th'], 't17 nw')"),
             ("tx('How many cows?', 'e22'), tx('มีวัวกี่ตัว' + DR, 't17 nw')", "tx(D['uiText']['howManyCows']['en'], 'e22'), tx(D['uiText']['howManyCows']['th'], 't17 nw')"),
             ("[tx('Big or small?', 'e22'), tx('ใหญ่หรือเล็ก' + DR, 't17 nw')]", "[tx(D['uiText']['bigOrSmall']['en'], 'e22'), tx(D['uiText']['bigOrSmall']['th'], 't17 nw')]"),
             # Instructor sweep 2 #2: {word} is the card's en in BOTH lines (patch instructor-ask-en-both), never th
             ("TP['th'].replace('{word}', C[cid]['th'])", "TP['th'].replace('{word}', C[cid]['en'])"),
             # sweep 2 #12: the D plates are the cs-23/cs-24 words only
             ("tag(34, 516, 'big', C['cs-23']['th']) + tag(264, 556, 'small', C['cs-24']['th'])", "tag(34, 516, C['cs-23']['en'], '') + tag(264, 556, C['cs-24']['en'], '')")]:
    assert s.count(a) == 1, a; s = s.replace(a, b)
assert U8['tapPrompt']['th'] == '{word} อยู่ที่ไหน'
# Auditor gate 1975f0b8 + Watchman sweep P15 render bugs: tap targets 44 pt+, 8 px apart, no overlap; scenery that is not a target carries no tap
def _deco(h): return h.replace("data-tap=1 role='button' ", "", 1).replace("data-tap='1' role='button' ", "", 1)
for a_, b_ in [("obj('bench', 248, 606, 120, 72) + emo('🍞', 284, 572, 46, 'bread')", "_deco(obj('bench', 248, 606, 120, 72)) + emo('🍞', 284, 572, 46, 'bread')"),   # A: bench is the surface, bread the target
               ("obj('cow', 214, 312, 96, 69) + obj('cow', 300, 350, 84, 60) + obj('cow', 250, 520, 120, 86)", "obj('cow', 214, 312, 96, 69) + obj('cow', 290, 400, 84, 60) + obj('cow', 250, 520, 120, 86)"),   # C: no cow overlap, 16 pt from the edge
               ("f\"<div style='display:flex;gap:8px;margin-top:6px'>{plates}</div>\"", "f\"<div style='display:flex;gap:8px;margin-top:16px'>{plates}</div>\""),   # C: plates clear of the speaker
               ("body += obj('cow', 250, 330, 120, 86) + obj('gate', 24, 450, 90, 70)", "body += _deco(obj('cow', 250, 330, 120, 86)) + _deco(obj('gate', 24, 436, 90, 70))"),   # D: scenery, gate clear of the big plate
               ("body += emo('🥚', int(hx + 86*k - 20), int(hy + 64*k - 40), 40, 'egg', shadow=False)", "body += emo('🥚', int(hx + 86*k - 22), int(hy + 64*k - 44), 44, 'egg', shadow=False)"),
               ("body += obj('basket', 22, 572, 120, 105) + obj('basket', 280, 616, 64, 56)", "body += _deco(obj('basket', 22, 572, 120, 105)) + _deco(obj('basket', 280, 616, 64, 56))"),   # D: the plates are the targets
               ("body += emo('🥐', 246, 542, 46, 'croissant') + emo('🍝', 298, 540, 48, 'spaghetti') + emo('🥚', 348, 548, 38, 'eggs')", "body += emo('🥐', 250, 542, 44, 'croissant') + emo('🍝', 312, 542, 44, 'spaghetti')"),   # F: 44 pt, 8 px+ apart
               ("body += obj('desk', 8, 558.5, 112, 112) + emo('🍨', 34, 514, 46, 'sundae')", "body += _deco(obj('desk', 16, 558.5, 112, 112)) + emo('🍨', 16, 536, 44, 'sundae') + emo('🥚', 74, 536, 44, 'eggs')")]:   # F: eggs move onto the desk
    assert s.count(a_) == 1, a_[:60]; s = s.replace(a_, b_)
s = s.replace('mk = Z.mk\n', 'mk = Z.mk\ndef _deco(h): return h.replace("data-tap=1 role=\'button\' ", "", 1).replace("data-tap=\'1\' role=\'button\' ", "", 1)\n', 1); assert '_deco(h)' in s
g = {'__name__': 'scenes_v608'}; exec(compile(s, 'scenes_v608', 'exec'), g)
PV, page, S, W, H = g['PV'], g['page'], g['S'], g['W'], g['H']
# Maxwell t426u (front desk, approved with changes): key on a wall key rack, truck small and far behind the hill line in the window,
# a full-height door to the floor line sized to Nancy (gold 13 kept), clock kept; every prop on a surface, hook, shelf or the ground.
def mock_E():
    Z, svg, emo, hero, ask, C_ = g['Z'], g['svg'], g['emo'], g['hero'], g['ask'], g['C']
    L = dict(Z.L390); L['objs'] = []; L['win'] = (232, 407, 140, 150); L['shelf'] = (122, 474, 84); L['pegs'] = []
    body = Z.room(W, H, L); base = L['base']
    b = "<circle cx='176' cy='402' r='20' fill='#FFF8E1' stroke-width='3'/><path d='M176 402v-13M176 402l-6-7' stroke-width='3'/><circle cx='176' cy='402' r='2.2' fill='#10170F'/>"   # wall clock (kept)
    # far hill inside the window, drawn after the truck so the truck sits partly behind it
    hill = "<path d='M235 548v-40q40-14 70-6t64-8v54z' fill='#5E9E4A' stroke='none'/><path d='M235 508q40-14 70-6t64-8' stroke-width='2.4' fill='none'/>"
    # front desk counter across the right (hip high)
    desk = "<path d='M196 560h186v100H196z' fill='#B9733F' stroke-width='3'/><path d='M190 550h198v14H190z' fill='#8E5730' stroke-width='3'/>"
    desk += ''.join(f"<path d='M{x} 576h40v70h-40z' fill='#A8653A' stroke='#7E4A26' stroke-width='2'/>" for x in (210, 262, 314))
    desk += "<ellipse cx='290' cy='662' rx='88' ry='4' fill='#10170F' opacity='.22' stroke='none'/>"
    # full-height room door on the left wall, bottom on the floor line, about 1.1x Nancy's height
    dh = 214; dy = base - dh
    door = (f"<path d='M14 {dy}h92v{dh}H14z' fill='#8E5730' stroke-width='3'/><path d='M24 {dy+12}h72v{dh*.42:.0f}H24zM24 {dy+dh*.5:.0f}h72v{dh*.44:.0f}H24z' fill='#A8653A' stroke='#6E4224' stroke-width='2'/>"
            f"<circle cx='92' cy='{dy+dh*.52:.0f}' r='4.5' fill='#FFCC33' stroke-width='2'/><path d='M44 {dy+20}h32v20H44z' fill='#FFCC33' stroke-width='2'/>")
    # key rack: a wood strip with three hooks on the wall above the door, away from her hand
    rack = "<path d='M20 386h80v12H20z' fill='#8E5730' stroke-width='2.4'/><circle cx='27' cy='392' r='2' fill='#FFCC33' stroke='none'/><circle cx='93' cy='392' r='2' fill='#FFCC33' stroke='none'/><path d='M38 398v7q0 3 3 3M57 398v7q0 3 3 3M76 398v7q0 3 3 3' stroke-width='2.4' fill='none'/>"   # rack on the wall above the door, away from her hand
    road = "<path d='M235 524h134v12H235z' fill='#C9B48A' stroke='none'/><path d='M235 524h134M235 536h134' stroke-width='2' fill='none'/>"   # a road across the window, in front of the far hill
    body += svg(b + door + rack + hill + road)
    body += emo('🛻', 300, 494, 44, 'truck', shadow=False).replace('font-size:37px', 'font-size:28px', 1)      # small truck on the road outside; 44 pt tap area
    body += svg(desk)
    body += f"<div class='abs' style='left:47px;top:{dy+20}px;width:26px;text-align:center;font:400 15px/20px \"Lilita One\";color:#10170F'>13</div>"
    body += emo('🔑', 28, 393, 44, 'keys', shadow=False).replace('font-size:37px', 'font-size:26px', 1)   # hangs on the middle hook; 44 pt tap area
    body += emo('📖', 130, 430, 44, 'book', shadow=False)      # stands on the shelf (top 474)
    body += hero('lake', 'nancy', 1.1, 112, 700, 'sword1')
    return body + PV.top('lake') + ask(en='Where are the keys?', th='keys อยู่ที่ไหนบ้าง')   # parent 4:30 PM MDT + Instructor plural template (8b765b95, NEEDS NANCY); keys stays English
g['M']['E-lake-front-desk'] = mock_E
# t426u sweep (A): the shop sat in the sky above the far hill; stand it on the hill line
g['M']['A-meadow-evening-pond'] = (lambda f: (lambda: f().replace("data-name='shop' aria-label='shop' style='left:186px;top:344px", "data-name='shop' aria-label='shop' style='left:186px;top:372px", 1)))(g['M']['A-meadow-evening-pond'])
# time of day by level (spec 7.1): the title's sky palette + a light tint over the scene (CSS var swap); props, layout, taps unchanged
TOD = {1: ('m', ''), 2: ('a', 'rgba(255,255,255,.10)'), 3: ('a', 'rgba(255,190,110,.08)'), 4: ('e', 'rgba(255,130,60,.16)'), 5: ('n', 'rgba(11,27,51,.45)')}
def meadow_level(lv):
    tod, tint = TOD[lv]; Z = g['Z']
    b, gg = PV.base('meadow', 'ask')
    if tod != 'm': b = b.replace(Z.sky(W, H, 'm', (-170, 120)), Z.sky(W, H, tod, (-170, 120) if tod != 'n' else (60, 70)), 1)
    if tint: b += f"<div class='abs' style='left:0;top:0;width:{W}px;height:{H}px;background:{tint};pointer-events:none'></div>"
    return b + PV.top('meadow') + g['ask']('ph-07' if False else None, 'Where is the kite?', 'kite อยู่ที่ไหน')
if __name__ == '__main__':
    only = sys.argv[1:]
    for n, fn in g['M'].items():
        if only and n[0] not in only: continue
        doc = page(W, H, fn()); assert 'Thai draft' not in doc and 'แตะเลย' not in doc and 'นะ</div>' not in doc
        open(f'html/{n}.html', 'w').write(doc); S.shot(doc, f'png/{n}.png', W, H, 'v608sc-' + n[0]); print(n, flush=True)
    if not only or 'L' in only:
        for lv in range(1, 6):
            doc = page(W, H, meadow_level(lv)); open(f'html/L{lv}-meadow.html', 'w').write(doc); S.shot(doc, f'png/L{lv}-meadow.png', W, H, f'v608L{lv}'); print('L', lv, flush=True)
