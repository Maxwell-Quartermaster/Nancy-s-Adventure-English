# Round 2 P1 (Maxwell t440u): one ask card with the staged phrasing, screen 10 (Word Meadow ask, kite) at 390x844 and 320x568.
# The tapPrompt comes from round2/staged cards.json (not the build). Usage: python3 render_phrasing.py ; NAE_SE=1 python3 render_phrasing.py
import sys, os, json; sys.argv = ['x']; sys.path.insert(0, '/workspace/v608build/screens')
import play_v608 as P
TP = json.load(open('/workspace/v608build/round2/staged/nancys-adventure-english-v6-08-cards.json'))['uiText']['tapPrompt']
assert TP == {'en': 'Can you find the {word}?', 'th': 'หา {word} เจอไหม'}
P._TPC.clear(); P._TPC.update(TP)
slug, st, src, fn = P.SCR[10]; f = '/workspace/v608build/round2/renders/ask-can-you-find-' + ('320x568' if P.SE else '390x844')
doc = P.page(P.W, P.H, fn()); assert 'Can you find the kite?' in doc and 'หา kite เจอไหม' in doc
open(f + '.html', 'w').write(doc); P.S.shot(doc, f + '.png', P.W, P.H, 'r2ask' + str(P.W)); print(f)
