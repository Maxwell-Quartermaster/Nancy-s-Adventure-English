# Council 3:55 PM MDT item 5: main menu with the daily gem tag, (a) before the verse is seen (tag above the verse pop-up) and
# (b) on a day the verse is already seen (spec VP4: the tag sits alone). English tag stays exactly "Daily gift: +1 gem" (Maxwell's pick).
import sys
sys.argv = ['x']; exec(open('/workspace/v608build/verse-popup/votd_v608.py', encoding='utf-8').read().split("M = g['M']")[0])
M = g['M']; WK = g['WK']; OUT = '/workspace/screens-v608/'
sys.path.insert(0, '/workspace/v608build/screens'); import menufix_v608; menufix_v608.apply(M)   # Watchman sweep P1/P2: hearth top-right, 320 buttons 288 wide
assert g['T']['dailyGift']['en'] == 'Daily gift: +1 gem'
def alone(se):   # tag alone: same flat dashed strip, same spot above where the card would sit; information only (never a button)
    return (f"<div style='position:absolute;z-index:80;left:{16 if se else 20}px;right:{16 if se else 20}px;top:{78 if se else 132}px;display:flex;justify-content:center;pointer-events:none'>{g['giftrow'](se)}</div>")
for se in (False, True):
    g['setsize'](se); sz = '-320x568' if se else '-390check'
    def inert_hub(e):   # Auditor r2b-2051 occlusion (3): the menu under the verse pop-up is inert (aria-hidden, no taps), as 02/02b (0 chars)
        d = M.hub(e); i = d.index(e[:80]); return d[:i].replace("<div data-tap=1 ", "<div data-inert=1 aria-hidden='true' ") + d[i:]
    for n, doc in (('02c-menu-gemtag-before-verse', inert_hub(g['OPTS']['B'](WK[0], se))), ('02d-menu-gemtag-after-verse', M.hub(alone(se)))):
        doc = EY.apply(doc)[0]; open(OUT + f'html/{n}{sz}.html', 'w').write(doc); M.shot(doc, OUT + f'png/{n}{sz}.png'); print(n + sz, flush=True)
