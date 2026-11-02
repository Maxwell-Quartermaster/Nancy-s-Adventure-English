# r2d staged copy of the screen 26 sheet: Watchman's 26-D rebuilt with the plate kept (Instructor, 10:18 PM MDT, QM-relayed); A's 6 s line; every fitting R2 combination from r2_fit_table.py.
# Neutral: no default; each option shows its cost, what is left from the staged bank, and which R2 ask + saving combinations fit. Nothing is applied to the PASTE.
import sys; sys.path.insert(0, '/workspace/v608build/round2/sheets'); from sheetkit import wrap, F, INK, GOLD, BG, RED
from PIL import Image, ImageDraw
sys.path.insert(0, '/workspace/v608build/round2/asset-depth'); import round_totals as RT
G = '/workspace/v608build/round2/r2d/g26d/png/'; L = RT.STAGED['1A']   # 1A and 1B both bank the same
sys.path.insert(0, '/workspace/v608build/round2/r2d'); import r2_fit_table as FT   # the fit list is built by script (every ask x ramp x night title B x B1 B)
COST = FT.COST
def cap(k, desc, scale):
    l = L - COST[k]; f = FT.fits(k)
    return (f"{desc} +{COST[k]} chars, {l} left. Scale {scale}.", [f'Fits ({len(f)} of 16):'] + ['- ' + FT.label(r) for r in f] if f else ['Nothing fits (0 of 16).'])
U6 = 'until tapped or 6 s (:220)'
T = [('A', *cap('A', f'Bubble above the card: it covers Sam {U6}.', '0.816'), G + '26-A-320x568.png'),
     ('B', *cap('B', f'Bubble under the banner, scrolls: it covers the picture plate {U6}. At 320 two full Thai lines show before scrolling.', '0.816'), G + '26-B-320x568.png'),
     ("C'", *cap("C'", 'Chip under the banner, label "Words of Jesus" + its Thai (uiText.jesusWords, already checked); at rest it covers nothing and the scene sits below it.', '0.687'), G + '26-C-rest-320x568.png'),
     (None, (f"C' after a tap on the chip: the verse opens over the scene and covers the heroes' heads {U6}. Once the chip is tapped, C' is the only option besides A that covers the heroes' heads.", []), G + '26-C-open-320x568.png'),
     ('D', *cap('D', f'Bubble under the banner beside the picture plate, ending above Sam\'s head: it covers scenery only, {U6}. Thai scrolls inside. Two full Thai lines do not fit above Sam at 320 (37 pt short; about 1 Thai line shows before scrolling) or at 375 x 667 (22 pt short); they fit at 375 x 812.', '0.816'), G + '26-D-320x568.png'),
     (None, ("D at 375 x 667: the same layout (bubble beside the plate, above Sam's head, Thai scrolls; scale 0.803).", []), G + '26-D-375x667.png')]
T = [(t[0], t[1], t[2], t[3]) if t[0] else (None, t[1][0], t[1][1], t[2]) for t in T]
w, h, colw, caph = 320, 568, 360, 470
_d0 = ImageDraw.Draw(Image.new('RGB', (10, 10)))
def _caph(num, c1, lines):
    yy = wrap(_d0, 0, 2, c1, F(14, False), 30 if num else 40); yy = max(yy, 58) + 4
    for ln in lines: yy = wrap(_d0, 0, yy, ln, F(13, False), 50) + 3
    return yy
caph = max(caph, max(_caph(*t[:3]) for t in T) + 16)   # r2e: never let a caption run into its picture
W = 30 + len(T) * colw; footer = ('Each option shows its own cost, what is left from %d (both trims), and every round 2 combination that fits (ask: letter game %d / state pairs %d; ramp kept +%d; '
     'night title B -60; B1 B -11; full table by r2_fit_table.py, cross-checked with Chancellor f6fdf5c7: all four lists match). Nothing here is in the PASTE. '
     'A: spec :220 already says a soft bubble until tapped or 6 s (0). B and D: spec 1.12 needs " A Jesus word scrolls in its bubble." (+36); the spec does not fix where the bubble sits, so D needs no other words. '
     "C': spec :220 needs \"; at 320 pt it rests as a chip under the banner (`uiText.jesusWords`) until tapped\" (+82; no scroll icon, spec :344 keeps Jesus words off Scrolls). "
     'A new chip entry instead (uiText.jesusChip, new Thai NEEDS NANCY by meta.thStatusDefault, 61 + a clause of 81) would be +142, 261 left. '
     "C' chip with a line break between the English and the Thai (0 chars) was rendered too: the opened verse would cover more of Sam (51 pt of 150 at 320, 24 of 147 at 375 x 667, against 47 of 154 and 20 of 151 as shown), so the chip is shown as frozen. "
     + FT.RESERVE + ' Oct 31, 2026, MDT.') % (L, RT.ASK['letter game'], RT.ASK['state pairs'], RT.RAMP) + RT.snap_line()
H = 150 + caph + h + 40 + 22 * (2 + len(footer) // 150)
S = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(S)
y = wrap(d, 30, 16, 'Screen 26: the Words of Jesus hint (320 x 568; D also at 375 x 667)', F(24), 120); y = wrap(d, 30, y + 4, "Which one, A, B, C' or D?", F(18), 120, RED) + 10
for i, (num, c1, lines, png) in enumerate(T):
    x = 30 + i * colw
    if num: d.rounded_rectangle((x, y, x + 64, y + 50), 10, fill=INK); d.text((x + 12 - (6 if len(num) > 1 else 0), y + 6), num, fill='#FFF8E1', font=F(34))
    yy = wrap(d, x + (80 if num else 0), y + 2, c1, F(14, False), 30 if num else 40); yy = max(yy, y + 58) + 4
    for ln in lines: yy = wrap(d, x, yy, ln, F(13, False), 50) + 3
    im = Image.open(png).convert('RGB').resize((w, h), Image.LANCZOS); S.paste(im, (x, y + caph)); d.rectangle((x - 1, y + caph - 1, x + w, y + caph + h), outline=GOLD, width=2)
wrap(d, 30, y + caph + h + 20, footer, F(14, False), 260)
out = '/workspace/v608build/round2/r2d/sheets/jesus-words-26-320-A-B-C-D.png'; S.save(out); print(out)
for t in T: print(t[0], t[1][:60], t[2])
