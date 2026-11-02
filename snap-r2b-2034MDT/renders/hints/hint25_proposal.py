# Proposal only (council 7:56 PM MDT vs the owner's 7:53 PM "don't change hints on 13 or 25"): sw-19 "think" choices eat/sink/run/think
# -> eat/sink/ten/think, so "t____" fits two choices. 0 PASTE chars ("run" -> "ten", nm-15's own word; choices are English only, no new Thai).
# NOT applied to round2.py, the staged PASTE or screens-v608. Usage: python3 hint25_proposal.py
import sys; sys.argv = ['x']; sys.path.insert(0, '/workspace/v608build/screens')
import play_v608 as PV
c = PV.C['sw-19']; assert c['choices'] == ['eat', 'sink', 'run', 'think'], c['choices']; c['choices'] = ['eat', 'sink', 'ten', 'think']
slug, st, src, fn = PV.SCR[25]; O = '/workspace/v608build/round2/hints/'
doc = PV.guardian_chip(PV.page(PV.W, PV.H, fn()), 25); open(O + f'25-{slug}-ten-390x844.html', 'w').write(doc); PV.S.shot(doc, O + f'25-{slug}-ten-390x844.png', PV.W, PV.H, 'h25'); print('ok')
