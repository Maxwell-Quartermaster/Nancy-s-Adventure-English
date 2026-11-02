# Screen 26 at 320 x 568: where the Words of Jesus hint goes (council 9:49 PM MDT, QM-relayed; Instructor's chip proposal). Neutral, no default.
# Costs measured against the staged PASTE (403 banked); none of them is applied to the PASTE.
import sys; sys.path.insert(0, '.'); from sheetkit import sheet
sys.path.insert(0, '/workspace/v608build/round2/asset-depth'); import round_totals as RT
G = '/workspace/v608build/round2/r2c/g26/png/'; L = RT.STAGED['1A']
COST = {'A': 0, 'B': 36, 'C': 81 + 88}
t = [('A', f"Bubble over Sam (as staged). Mock only: 0 chars, {L - COST['A']} left. Scale 0.816.", G + '26-A-320x568.png', (320, 568)),
     ('B', f"Bubble under the banner, scrolls; covers the picture. +{COST['B']} chars, {L - COST['B']} left. Scale 0.816.", G + '26-B-320x568.png', (320, 568)),
     ('C', f"Chip under the banner, covers nothing; scene smaller. +{COST['C']} chars, {L - COST['C']} left. Scale 0.669. Chip Thai: NEW, NEEDS NANCY.", G + '26-C-rest-320x568.png', (320, 568)),
     (None, "C after a tap on the chip: the verse opens over the scene; any tap closes it.", G + '26-C-open-320x568.png', (320, 568))]
sheet('/workspace/v608build/round2/sheets/jesus-words-26-320-A-B-C.png', 'Screen 26 at 320 x 568: the Words of Jesus hint', 'Which one, A, B or C?', t,
      'Each option shows its own cost and what is left from %d; nothing here is in the PASTE. A: the spec (:220) already says a soft bubble, until tapped or 6 s. '
      'B: spec 1.12 lets only the Character pane, Backup lists and long verses scroll, so it needs " A Jesus word scrolls in its bubble." (+36). '
      'C: spec :220 needs "; at 320 pt it rests as a chip under the banner (`uiText.jesusChip`) until tapped" (+81) and a new uiText.jesusChip entry with its Thai marked NEEDS NANCY (+88). '
      'C could reuse the existing uiText.jesusWords label instead (Thai already checked by Instructor): +82, %d left, no new Thai. Oct 31, 2026, MDT.' % (L, L - 82), cols=4)
print('ok')
