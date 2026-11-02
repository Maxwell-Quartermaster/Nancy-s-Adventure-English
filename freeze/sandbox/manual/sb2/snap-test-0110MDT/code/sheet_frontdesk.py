import sys; sys.path.insert(0, '.'); from sheetkit import sheet
S = '/workspace/v608build/scenes/stage/png/'; C = '/workspace/v608build/round2/ceiling-cap/png/'
t = [('1', '320 × 568 AFTER (fit to width). The framing asked for at every size.', S + 'E-lake-front-desk-320x568.png', (320, 568)),
     ('2', '390 × 844 now: same layout and width fit; the room shows 181 pt more ceiling above the shelf line. No text.', S + 'E-lake-front-desk-390x844.png', (390, 844)),
     ('3A', '390 × 844 trimmed: the art above the 320 framing line is cropped; plain parchment fills the band under the HUD. PASTE +89 (1A or 1B).', C + 'E-lake-front-desk-390x844.png', (390, 844)),
     ('3B', '390 × 844 trimmed: the 320 ceiling strip sits under the HUD; plain wall fills down to the molding. PASTE +89 (1A or 1B), same look.', C + 'E-lake-front-desk-390x844-wallup.png', (390, 844))]
sheet('/workspace/v608build/round2/sheets/front-desk-t444u-320-vs-390.png', 'Front desk: the 320 framing at 390',
      'At 390: 2 (as now), 3A or 3B?', t,
      'Maxwell t444u (QM-relayed): the 320 × 568 AFTER is the target composition at every size. Props, hook, shelf, clock, window, HUD, card and taps are the same size and the same distance from the card in 2, 3A and 3B. '
      'Text (1A): "; on taller phones a room crops its ceiling to the 320 × 568 framing, never over a target" +89. Also applied to the kitchen meal room (same layout). '
      'With all rooms (1A, +89) the home-lake rooms at 390 (14, 16, 20-22, 32, 33, 54, zone lake, tod lake 1-5) take the same trim and 17-19 keep their ceiling (never over a target); '
      'with the front desk and kitchen only (1B, +89) only the kitchen 20-22 trim and the rest stay as approved (see the 1A/1B trim sheet). DOM check (390, 375 × 667, 375 × 812) on the front desk: 0 targets hidden, 0 edges under 16 pt. The ask is ms-21\'s own sentence (P1 keeps sentence cards).', cols=4)
print('ok')
