# Renders gear-family screens from v604build/screens/gear_v604.py (read-only) with the v6-08 cards into screens-v608/ (-390check, or -320x568 with NAE_SE=1).
# t411u (Maxwell): 46 Backup view kept, text easier to read (Ink, heavier, 15-16 px EN, 17 px Thai lh 1.7, nothing cut), Backup/Restore labels stacked EN over TH fully inside the buttons at 390 and 320.
import sys, os, json
s = open('/workspace/v604build/screens/gear_v604.py', encoding='utf-8').read()
SE = os.environ.get('NAE_SE') == '1'; SUF = '-320x568' if SE else '-390check'
for a, b in [("OUT = '/workspace/v604build/screens/'", "OUT = '/workspace/screens-v608/'"), ("nancys-adventure-english-v6-04-cards.json", "nancys-adventure-english-v6-08-cards.json"),
             ("w, h = 390, 844", "w, h = (320, 568) if %r else (390, 844)" % SE),
             ("{txt(t['en'][:16], 'mc', 'font-size:12px;color:#3A2410;white-space:normal;line-height:14px')}", "{txt(t['en'], 'mc', 'font-size:12px;color:#3A2410;white-space:normal;line-height:14px')}"),   # full theme names, 2 lines, no cut
             ("txt('Yours after 3 boss wins · ได้รับเมื่อชนะบอส 3 ครั้ง', 'mc', 'font-size:13px;color:#F6E9C8')", "txt('Yours after 3 boss wins', 'mc', 'font-size:13px;color:#F6E9C8') + txt('ได้รับเมื่อชนะบอส 3 ครั้ง', 'th', 'color:#F6E9C8')"),   # Thai 17 px on its own line
             ("tip(h-12-56-8-92, 84, [txt('Green meadow'", "tip(h-12-56-8-118, 110, [txt('Green meadow'"),
             ("out += tip(h-12-56-8-80, 72, [txt(U['nextWeapon']['en'].replace('{n}', '4') + ' · 2 more gems to the next gear bonus', 'mc', 'font-size:14px;color:#9BE08F')", "out += tip(h-12-56-8-96, 88, [txt(U['nextWeapon']['en'].replace('{n}', '4') + ' · 2 more gems to the next gear bonus', 'mc', 'font-size:14px;color:#9BE08F;white-space:normal;line-height:17px')"),   # wraps inside the tip
             ("height:96px;padding:8px 12px;box-sizing:border-box'>\"\n                f\"{txt(v['ref']", "height:{96 if len(v['en']) < 110 else 132}px;padding:8px 12px;box-sizing:border-box'>\"\n                f\"{txt(v['ref']"),
             ("line-height:17px')}</div>\"); y += 106", "line-height:17px')}</div>\"); y += (106 if len(v['en']) < 110 else 142)")]:   # long verses get a taller card, nothing cut
    assert s.count(a) == 1, a; s = s.replace(a, b)
s = s[:s.index("if __name__ == '__main__':")]
sys.path.insert(0, '/workspace/v604build/screens'); sys.path.insert(0, '/workspace/v608build/eyes'); import eyes_v608 as EY
g = {'__name__': 'gear_v608'}; exec(compile(s, 'gear_v608', 'exec'), g)
w, h, U, D, txt, head = g['w'], g['h'], g['U'], g['D'], g['txt'], g['head']
INK = '#10170F'
def btn2(en, th, wd):   # EN over TH, both inside the button (t411u)
    return (f"<div data-tap=1 role='button' style='width:{wd}px;height:68px;flex:none;box-sizing:border-box;border-radius:8px;background:linear-gradient(#FFE08A,#E8B84A);"
            f"border:2px solid {INK};box-shadow:inset 0 0 0 1px #FFF3C4,0 3px 0 #000;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:0 6px'>"
            f"{txt(en, 'cz', f'font-size:15px;line-height:1.2;color:{INK}')}{txt(th, 'th', f'color:{INK};line-height:1.5')}</div>")
def hd(en, th): return (f"<div style='display:flex;flex-wrap:wrap;align-items:baseline;column-gap:8px;margin:4px 4px 0'>{txt(en.upper(), 'cz', f'font-size:16px;color:{INK}')}{txt(th, 'th', 'color:#3A2410')}</div>")
def row(inner, mh=40): return f"<div class='paper' style='min-height:{mh}px;padding:6px 12px;box-sizing:border-box;display:flex;align-items:center;gap:8px'>{inner}</div>"
_backup0 = g['backup']
def backup(step2=False):
    if step2: return _backup0(True)
    bw = (w - 24 - 24 - 10) // 2; C = {c['id']: c for c in D['cards']}
    out = f"<div style='display:flex;gap:10px;justify-content:center'>{btn2(*g['u']('backup'), bw)}{btn2(*g['u']('restore'), bw)}</div>"
    out += hd(*g['u']('needsMaxwell'))
    for cid in D['needsMaxwell'][:4 if not SE else 2]:
        c = C[cid]; t = c.get('en') or c.get('th') or ('______' if c.get('fill') else '')
        out += row(txt(cid + ' · ' + t, 'mc' if c.get('en') else 'th', f'font-size:16px;font-weight:700;color:{INK};white-space:normal;line-height:1.3' if c.get('en') else f'color:{INK};white-space:normal'))
    out += hd(*g['u']('thaiReview'))
    for t in [U['tapPrompt']['th'], U['playAgain']['th'], U['giftFrom']['th'], U['dailyGift']['th']][:4 if not SE else 2]:   # sweep 2: only file strings in the Thai queue
        out += row(f"{txt(t, 'th', f'color:{INK};white-space:normal')}<div style='flex:1'></div>{txt('✓', 'cz', 'font-size:22px;color:#1F5A1F')}{txt('✎', 'cz', 'font-size:22px;color:#5A3A10')}", 44)
    panel = (82, h - 82 - 80)
    return g['shell'](g['u']('backup'), f"<div style='position:absolute;left:24px;right:24px;top:{panel[0]+12}px;height:{panel[1]-24}px;overflow:hidden;display:flex;flex-direction:column;gap:8px'>{out}</div>", panel=panel)
# Instructor sweep 2 #7: no strings that are not in the file (hand words, draft Thai type names); the tooltip shows the selected tier's bonus (a Retry row's tier 2 = bonusRetry2)
GM = g['GM']; GM.TH_TYPE.clear(); GM.W.HAND.update({k: '' for k in GM.W.HAND})
def _tier_tip(kind, t_sel, owned):
    b0 = GM.BONUS[kind]
    if t_sel == 1 and not b0.endswith('2'): GM.BONUS[kind] = b0 + '2'
    try: return GM.screen(w, h, kind, t_sel, owned)
    finally: GM.BONUS[kind] = b0
g['backup'] = backup; SCR = dict(g['SCR'])
SCR[38] = (SCR[38][0], SCR[38][1], SCR[38][2], lambda: _tier_tip('mace1', 1, (0, 1))); SCR[39] = (SCR[39][0], SCR[39][1], SCR[39][2], lambda: _tier_tip('axe1', 0, (0,))); SCR[46] = ('backup-view', 'extrapolated', 't349u frame/band/paper; t411u readability', backup)
if __name__ == '__main__':
    only = [int(x) for x in sys.argv[1:]]
    for n, (slug, st, src, fn) in sorted(SCR.items()):
        if only and n not in only: continue
        doc = EY.apply(g['page'](w, h, fn()))[0]; open(g['OUT'] + f'html/{n:02d}-{slug}{SUF}.html', 'w').write(doc)
        g['shot'](doc, g['OUT'] + f'png/{n:02d}-{slug}{SUF}.png', w, h, f'v608g-{n}{SUF}'); print(n, slug, flush=True)
