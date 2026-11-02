# v6-08 VP renders (Maxwell t399u option B, 3:35 PM MT): the daily verse pops up over the main menu (never the title, t404u/O1).
# Built from mocks-verse-popup-t399u/mock_votd_menu.py (read-only) with the v6-08 cards: dailyGift tag from uiText (Instructor 7057dde4 Thai), Sam's happy eyes (eyes_v608).
import sys, json, os
s = open('/workspace/mocks-verse-popup-t399u/mock_votd_menu.py', encoding='utf-8').read()
s = s[:s.index("if __name__ == '__main__':")]
for a, b in [("nancys-adventure-english-v6-06-cards.json", "nancys-adventure-english-v6-08-cards.json"),
             ("GIFT_EN, GIFT_TH = 'Daily gift: +1 gem', 'ของขวัญวันนี้: อัญมณี 1 เม็ด'", "GIFT_EN, GIFT_TH = T['dailyGift']['en'], T['dailyGift']['th']")]:
    assert s.count(a) == 1, a; s = s.replace(a, b)
g = {'__name__': 'votd_v608'}; exec(compile(s, 'votd_v608', 'exec'), g)
sys.path.insert(0, '/workspace/v608build/eyes'); import eyes_v608 as EY
M = g['M']; WK = g['WK']; OUT = '/workspace/screens-v608/'
sys.path.insert(0, '/workspace/v608build/screens'); import menufix_v608; menufix_v608.apply(M)   # Watchman sweep P1/P2: hearth top-right, 320 buttons 288 wide
L = max(range(len(WK)), key=lambda i: len(WK[i]['en']) + len(WK[i]['th']))
for se in (False, True):
    g['setsize'](se); sz = '-320x568' if se else '-390check'
    def inert_hub(e):   # council 7:53 PM MDT: the menu under the verse pop-up is inert (aria-hidden, no taps), as 33 and 48 (0 chars)
        d = M.hub(e); i = d.index(e[:80]); return d[:i].replace("<div data-tap=1 ", "<div data-inert=1 aria-hidden='true' ") + d[i:]
    for n, doc in (('03-main-menu', M.hub()), ('02-main-menu-verse-popup', inert_hub(g['OPTS']['B'](WK[0], se))), ('02b-main-menu-verse-popup-longest', inert_hub(g['OPTS']['B'](WK[L], se)))):
        doc = EY.apply(doc)[0]
        SA = "<div style='flex:1 1 auto;min-height:0;overflow-y:auto;-webkit-overflow-scrolling:touch'>"
        if se and n.startswith('02b') and SA in doc:   # P7 (Auditor eb2674be H4): at 320 a verse too long for the card scrolls inside it (the verse box was already a scroll box); a soft inner shadow marks more below
            doc = doc.replace(SA, "<div data-scroll='verse' style='flex:1 1 auto;min-height:0;overflow-y:auto;-webkit-overflow-scrolling:touch;box-shadow:inset 0 -14px 10px -12px rgba(58,36,16,.45)'>", 1)
        open(OUT + f'html/{n}{sz}.html', 'w').write(doc); M.shot(doc, OUT + f'png/{n}{sz}.png'); print(n + sz, flush=True)
        if se and n.startswith('02b'):   # the same card scrolled to the end: the whole Thai verse and the ESV · THSV11 line
            d2 = doc.replace('</body>', "<script>addEventListener('load',()=>{const e=document.querySelector('[data-scroll]');e.scrollTop=e.scrollHeight})</script></body>")
            open(OUT + f'html/{n}{sz}-scrolled.html', 'w').write(d2); M.shot(d2, OUT + f'png/{n}{sz}-scrolled.png'); print(n + sz + '-scrolled', flush=True)
print('longest verse index', L, WK[L]['ref'])
