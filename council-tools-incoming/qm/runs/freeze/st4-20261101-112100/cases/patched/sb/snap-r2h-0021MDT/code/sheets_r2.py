# Round 2 sheets for Maxwell (render-only). Each panel is shown 390 wide; a 320x568 screen is scaled up to 390 wide and keeps its own shape.
from PIL import Image, ImageDraw, ImageFont
F = lambda s: ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', s)
def sheet(out, title, sub, cols, foot):
    import sys as _s; _s.path.insert(0, '/workspace/v608build/round2/asset-depth'); import round_totals as _RT; _l = _RT.for_sheet(out)   # Chancellor 8:20 PM MDT
    if _l: foot = foot + ' ' + _l
    hs = [int(390 * Image.open(p).size[1] / Image.open(p).size[0]) for _, p in cols]; H = max(hs)
    import textwrap as _tw; _fl = _tw.wrap(foot, (len(cols) * 410) // 8); S = Image.new('RGB', (20 + len(cols) * 410, H + 130 + 20 * len(_fl)), '#F4ECD8'); d = ImageDraw.Draw(S)
    d.text((20, 12), title, fill='#3A2410', font=F(20)); d.text((20, 42), sub, fill='#7A1E12', font=F(16))
    for i, ((t, p), h) in enumerate(zip(cols, hs)):
        d.text((20 + i * 410, 74), t, fill='#3A2410', font=F(14)); S.paste(Image.open(p).convert('RGB').resize((390, h)), (20 + i * 410, 98))
    for _i, _t in enumerate(_fl): d.text((20, H + 112 + 20 * _i), _t, fill='#5A4A30', font=F(13))
    S.save(out); print(out)
ST = '/workspace/v608build/scenes/stage/png/'; SC = '/workspace/v608build/scenes/superseded-t439u/'
sheet('/workspace/v608build/round2/sheets/E-front-desk-one-layout-390.png', 'Front desk (scene E): one layout for every phone (t439u)',
      'Small phones get the same scene, scaled to the screen width. The keys hang on the hook; the book stands on the shelf.',
      [('320 x 568 BEFORE (its own layout)', SC + 's320/png/E-lake-front-desk-320x568.png'), ('320 x 568 AFTER (same layout, fit to width)', ST + 'E-lake-front-desk-320x568.png'),
       ('390 x 844 AFTER', ST + 'E-lake-front-desk-390x844.png')],
      'Render only. Spec line: round 2 P3, +160 PASTE chars (fit to width; HUD, card, taps full size), already in the staged PASTE (1A and 1B 187,797, 403 banked); not a pick. stage/CHECK.md: 0 FAIL. Oct 31, 2026, MDT.')
sheet('/workspace/v608build/round2/sheets/walk24-B-t441u-before-after-390.png', 'Screen 24 "walk", option B with your changes (t441u)',
      'Walker bigger, left of Sam; path behind the card; dark tufts on open grass; trees on the grass; Guardian name up top.',
      [('390 BEFORE (B as shown at t425u)', '/workspace/v608build/decisions/walk24-B.png'), ('390 AFTER', ST + 'W24-walk-B-390x844.png'), ('320 x 568 AFTER (scaled to 390 framing)', ST + 'W24-walk-B-320x568.png')],
      'Staged in round 2: P2 +71 ("an emoji person: 52 pt"); Guardian name on the zone-chip line +50 ("; on guardian runs the zone chip shows `boss.name` and the scene shrinks to sit below it", +50 +38, Maxwell t445u, QM-relayed; Auditor eb2674be H2). Same layout at 390 and 320; at 320 the scene scales down so the swing set, trees and walker sit below the Guardian banner (t445u). Oct 31, 2026, MDT.')
