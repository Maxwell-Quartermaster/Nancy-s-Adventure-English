# Batch 2b mocks rendered from the staged v6-08 play code (play_v608.py, XP purple). Each output is a single 390x844 screen.
import sys, re, json; sys.path.insert(0, '/workspace/v608build/screens'); sys.argv = ['x']
import play_v608 as P
W, H = 390, 844; C = P.C; D = P.D; tx = P.tx
def shot(name, inner):
    doc = P.page(W, H, inner); open(name + '.html', 'w').write(doc); P.S.shot(doc, name + '.png', W, H, 'b2b-' + name); print(name, flush=True)
def piccard(cid, pic):
    b, g = P.base('meadow', 'ask', objs=False); c = C[cid]
    return b + P.tplate(pic) + P.top('meadow') + P.card([tx(c['th'], 't17 nw'), P.plates(c['choices'], wd=160, cls='e15')], 196)
which = sys.argv_real if hasattr(sys, 'argv_real') else None
# TG1: now (sw-01, one of the 8 pictures) and Instructor's three honest pictures (mock emoji pairs; final art would be one SVG each)
shot('tg1-now-sw01', piccard('sw-01', C['sw-01']['pic']))
shot('tg1-sw16', piccard('sw-16', "<span style='font-size:44px;white-space:nowrap;letter-spacing:-4px'>" + '🤲🎂' + "</span>"))
shot('tg1-sw12', piccard('sw-12', "<span style='font-size:44px;white-space:nowrap;letter-spacing:-4px'>" + '🫴🔑' + "</span>"))
shot('tg1-sw11', piccard('sw-11', "<span style='font-size:44px;white-space:nowrap;letter-spacing:-4px'>" + '🤗☕' + "</span>"))
# Bloodtide name: the boss-milestone gift card, same card as screen 30, three names
SW = "<svg width='84' height='84' viewBox='-30 -60 60 80'><path d='M-3 18v-14h6v14z' fill='#B07A42' stroke='#10170F' stroke-width='2.5'/><path d='M-14 4h28v5h-28z' fill='#E8B84A' stroke='#10170F' stroke-width='2.5'/><path d='M-9 4v-52q9-12 18 0v52z' fill='#C9CED6' stroke='#10170F' stroke-width='2.5'/></svg>"
def gift(name):
    b, g = P.base('meadow', 'cheer', objs=False)
    return (b + P.top('meadow') + P.ribbon(*P.u('weaponNew')) + P.card(["<div style='display:flex;justify-content:center'>" + SW + "</div>", tx(name, 'e22')], 200, [P.gbtn(*P.u('weaponUse'), 150), P.gbtn(*D['gotItText'].values(), 110)]))
for k, n in (('keep', 'Bloodtide Cleaver'), ('alt1', 'Dawntide Cleaver'), ('alt2', 'Brightwater Cleaver')): shot('name-' + k, gift(n))
# State pairs (t428u/t429u), lean mock: two copies of one object in the scene, the ask names the state
def state_pair():
    b, g = P.base('meadow', 'ask', objs=False)
    return (b + P.big('📖', 236, 560, 64) + P.big('📕', 312, 560, 64) + P.top('meadow') +
            P.card([tx('Can you find the open book?', 'e22'), tx('หาหนังสือที่เปิดอยู่เจอไหม', 't17')], 150, speaker=True))
shot('state-pair-open-book', state_pair())
# Letter game (t430u), grace-safe: no lives, no lost state. A: the picture grows with each right letter. B: the picture is revealed tile by tile.
def letters(mode):
    b, g = P.base('meadow', 'ask', objs=False)
    word = 'CAKE'; got = {'C', 'K'}
    blanks = ''.join(f"<span style='display:inline-block;width:40px;margin:0 4px;border-bottom:3px solid #10170F;text-align:center'>{ch if ch in got else '&nbsp;'}</span>" for ch in word)
    keys = ''.join(P.fr(None, None, 52, 52, tx(ch, 'e20 nw'), 'gs6', face=('#E9E2D2' if ch in 'CKS' else '#F6E9C8'), tap=ch not in 'CKS', st=(), name='key') for ch in 'ACEKST')
    if mode == 'A':
        pic = P.big('🎂', 262, 560, 56)
    else:
        cells = ''.join(f"<div style='width:52px;height:52px;box-sizing:border-box;border:1px solid #10170F;background:{'transparent' if i in (0, 4, 5, 7) else '#E8B84A'}'></div>" for i in range(9))
        pic = ("<div class='abs' style='left:115px;top:190px;width:160px;height:160px;border:3px solid #10170F;border-radius:14px;overflow:hidden;background:#F6E9C8'>"
               "<div style='position:absolute;left:0;top:0;width:156px;height:156px;display:flex;align-items:center;justify-content:center;font:400 120px/1 sans-serif'>🎂</div>"
               f"<div style='position:absolute;left:0;top:0;display:grid;grid-template-columns:52px 52px 52px'>{cells}</div></div>")
    return (b + pic + P.top('meadow') + P.card([tx("<span style='font-size:28px;letter-spacing:2px'>" + blanks + "</span>", 'e22'), tx('สะกดคำว่า เค้ก', 't17'),
            f"<div style='display:flex;gap:8px;justify-content:center;margin-top:8px'>{keys}</div>"], 210, speaker=True))
shot('letters-A-grows', letters('A')); shot('letters-B-tiles', letters('B'))
# TG4: tier 3+ buy, B = the Pantry's getFor ask-once over screen 39
g39 = open('/workspace/screens-v608/html/39-character-gear-rows.html', encoding='utf-8').read()
gf = D['uiText']['getFor']
# S1 (Auditor 1748 gate): as the :174 07/08 chooser fix: the screen behind is inert (no tap) under a soft parchment veil; the dialog sits over the hero panel, clear of the weapon tabs.
# Buttons reuse uiText.getFor (confirms) and uiText.back (closes); no new strings.
bk = D['uiText']['back']; gn = {k: v.replace('{n}', '200 ★') for k, v in gf.items()}
TH = "font:400 17px/1.7 Kanit,Thonburi,sans-serif"
btn = lambda en, th, face, w: (f"<div data-tap=1 role='button' style='width:{w}px;min-height:56px;box-sizing:border-box;padding:4px 6px;background:{face};border:2px solid #10170F;border-radius:12px;"
                               f"display:flex;flex-direction:column;justify-content:center'><div style='font-size:18px;line-height:1.15'>{en}</div><div style='{TH}'>{th}</div></div>")
dlg = ("<div style='position:absolute;z-index:90;left:0;top:0;width:390px;height:844px;background:rgba(246,233,200,.55)'></div>"
       "<div data-frame=9 style='position:absolute;z-index:91;left:32px;top:190px;width:326px;box-sizing:border-box;background:#F6E9C8;border:2px solid #10170F;border-radius:14px;"
       "box-shadow:inset 0 0 0 3px #E8B84A,inset 0 0 0 4px #10170F,0 4px 0 #10170F;padding:16px 14px;text-align:center;font-family:Lilita One,sans-serif;color:#10170F'>"
       "<div style='font-size:22px'>Star Axe</div>"
       "<div style='display:flex;gap:10px;justify-content:center;margin-top:12px'>" + btn(gn['en'], gn['th'], '#FFE08A', 168) + btn(bk['en'], bk['th'], '#E9E2D2', 112) + "</div></div>")
g39 = g39.replace(" data-tap=1 role='button'", ' aria-hidden=true'); assert 'data-tap' not in g39
i = g39.rindex('</body>'); g39b = g39[:i] + dlg + g39[i:]
open('tg4-B-confirm.html', 'w').write(g39b); P.S.shot(g39b, 'tg4-B-confirm.png', W, H, 'b2b-tg4b'); print('tg4-B-confirm')
# Night title B: "Good evening!" on the night banner
t52 = open('/workspace/screens-v608/html/52-title-night.html', encoding='utf-8').read(); assert t52.count('Good night!') == 1
t52b = t52.replace('Good night!', D['uiText']['greetEvening']['en'])
open('title-night-B.html', 'w').write(t52b); P.S.shot(t52b, 'title-night-B.png', W, H, 'b2b-t52b'); print('title-night-B')
# Coin meter close-ups (the HUD's left compartment, spec :124): 6 filled before a miss; A keeps 6, B shows 5
def coins(n):
    one = lambda f: (f"<svg width='26' height='26' viewBox='0 0 20 20'><circle cx='10' cy='10' r='8.5' fill='{'#FFCC33' if f else 'none'}' stroke='{'#B8860B' if f else 'rgba(184,134,11,.45)'}' stroke-width='2.4'/>"
                     + ("<circle cx='10' cy='10' r='8.5' fill='none' stroke='#10170F' stroke-width='1'/><path d='M10 5l1.5 3.2 3.4.4-2.5 2.3.7 3.4L10 12.6 6.9 14.3l.7-3.4-2.5-2.3 3.4-.4z' fill='#E8B84A' stroke='#8A6A10' stroke-width='.6'/><path d='M5.5 7a5 5 0 0 1 3-2.5' stroke='#fff' stroke-width='1.2' fill='none'/>" if f else '') + "</svg>")
    rows = ''.join(f"<div style='display:flex;gap:4px'>{''.join(one(k + 5*r < n) for k in range(5))}</div>" for r in range(2))
    return (f"<div style='position:absolute;left:95px;top:340px;width:200px;box-sizing:border-box;background:#F6E9C8;border:2px solid #10170F;border-radius:14px;box-shadow:inset 0 0 0 3px #E8B84A,0 4px 0 #10170F;padding:12px;display:flex;flex-direction:column;align-items:center;gap:4px'>"
            f"<div style='font:400 26px/1 Lilita One,sans-serif;color:#10170F'>💎 5</div>{rows}</div>")
for k, n in (('before', 6), ('A', 6), ('B', 5)):
    inner = (f"<div style='position:absolute;left:0;top:0;width:390px;height:844px;background:#9FD0F0'></div>" + coins(n))
    doc = P.page(W, H, inner).replace("</body>", "</body>"); P.S.shot(doc, f'coins-{k}.png', W, H, 'b2b-c' + k); print('coins', k)
