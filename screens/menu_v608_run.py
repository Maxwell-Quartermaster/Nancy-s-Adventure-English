# 03/04/49/50/51 main-menu family at 390 and 320 with the menufix_v608 layout (Watchman sweep P1-P4) and Sam's happy eyes.
import sys
sys.argv = ['x']; exec(open('/workspace/v608build/verse-popup/votd_v608.py', encoding='utf-8').read().split("M = g['M']")[0])
M = g['M']; sys.path.insert(0, '/workspace/v608build/screens'); import menufix_v608; menufix_v608.apply(M)
C, T, E = M.C, M.T, M.E; V = g['WK'][0]; en_, th_ = M.en_, M.th_
C8 = json.load(open('/workspace/nancys-adventure-english-v6-08-cards.json'))
OUT = '/workspace/screens-v608/'
for se in (False, True):
    g['setsize'](se); sz = '-320x568' if se else '-390check'
    for n, fn in (('03-main-menu', lambda: M.hub()),
                  ('04-main-menu-hearth', lambda: M.hub(M.hbubble(en_(C8['encouragement'][0]['en']) + th_(C8['encouragement'][0]['th']), 196 if se else 220))),
                  ('49-welcome-back', lambda: M.hub(M.bubble(en_(C8['welcomeBack']['en'], 18 if se else 20) + th_(C8['welcomeBack']['th']), 112 if se else 24, 72 if se else 200, 192 if se else 342))),
                  ('50-open-from-home-screen', lambda: M.page('a', M.bubble(en_(C8['uiText']['openFromHome']['en'], 22) + th_(C8['uiText']['openFromHome']['th']), 16 if se else 24, 120 if se else 160, M.w - 32 if se else 342))),
                  ('51-main-menu-hearth-verse', lambda: M.hub(M.hbubble(en_(V['en'], 17 if se else 20) + th_(V['th']) + en_(V['ref'], 15), 196 if se else 300)))):
        doc = EY.apply(fn())[0]; open(OUT + f'html/{n}{sz}.html', 'w').write(doc); M.shot(doc, OUT + f'png/{n}{sz}.png'); print(n + sz, flush=True)
