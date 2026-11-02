import sys; sys.path.insert(0, '.'); from sheetkit import sheet, r2tp
O = '/workspace/v608build/round2/sky-options/'
A = 'A, sky safe band: the kite, owl and lantern move down below the HUD at every size, so the 390 screen changes. PASTE +67; leaves 569 (544 with trim 1B).'
B = 'B, the fix for targets hidden on small phones: the crop stops at the highest target and the scene shrinks to fit. 390 unchanged. PASTE +79, plus +41 for the 16 pt edge rule; leaves 516 (491 with trim 1B).'
t = []
for row, n, lab in (('10-word-meadow-scene', 1, 'Word Meadow, screen 10'), ('zone-forest-ask', 2, 'Echo Forest zone')):
    for o, cap in (('A', A), ('B', B)):
        for wh in ((390, 844), (320, 568)):
            t.append((f'{n}{o}' if wh[0] == 390 else None, f'{lab}, {wh[0]} × {wh[1]}. ' + (cap if wh[0] == 390 else ('Same option at 320.' if o == 'A' else 'Same option at 320: scale 0.59 (meadow) / 0.58 (forest), parchment at the sides.')),
                      r2tp(O + f'{o}/html/{row}-{wh[0]}x{wh[1]}.html', *wh), wh))
sheet('/workspace/v608build/round2/sheets/sky-A-vs-B-meadow10-forest.png',
      'Sky targets on small phones: two ways to keep the kite, owl and lantern in view',
      'Which do you want: A (move the sky targets down everywhere) or B (shrink the scene at 320 so nothing is cut)?',
      t, 'A: 390 changes on 10, 11, 13, 15, 48 and the tod meadow strip; desk, towel, crib, tent and bridge move in 2-4 pt to stay 16 pt from the edge. '
         'B: 390 is byte-identical to the 6:09 PM baseline; at 320 meadow and forest show parchment bars at the sides; the lake rooms scale 0.80. '
         'Asks shown in the round 2 wording (sheet copies). Both: 0 targets under the HUD and 0 edges under 16 pt at 320, 375 × 812 and 390 (DOM check). Staged build only; nothing frozen changed.', cols=4)
print('ok')
