import sys; sys.path.insert(0, '.'); from sheetkit import sheet, r2tp
from PIL import Image, ImageDraw, ImageFont
V = '/workspace/screens-v608/html/'; H = '/workspace/v608build/round2/ceiling-cap/home-lake/'; C = '/workspace/v608build/round2/ceiling-cap/'
# 1) the pick: 1A all rooms vs 1B front desk and kitchen only (Auditor eb2674be H3: "night table" named no PASTE scene; F is the kitchen meal room)
t = [('1A', 'All rooms, never over a target (+89): every Home Lake room takes the 320-frame ceiling trim unless it would cut a target; the two-answer screens 17-19 keep their ceiling. PASTE 187,797, 403 left.', r2tp(H + 'html/54-phrase-ask-card-390x844.html', 390, 844), (390, 844)),
     ('1B', 'Front desk and kitchen only (+89): the front desk, the kitchen meal room and kitchen screens 20-22 trim; the other Home Lake rooms stay as approved. PASTE 187,797, 403 left.', r2tp(V + '54-phrase-ask-card.html', 390, 844), (390, 844)),
     (None, 'Front desk at 390 in both 1A and 1B (the ceiling strip under the HUD). The ask is ms-21\'s own sentence, which round 2 keeps (P1).', C + 'png/E-lake-front-desk-390x844-wallup.png', (390, 844)),
     (None, 'Screen 18 at 390 under 1A: the Pray and High five plates sit in the trim band, so the room keeps its ceiling (never over a target). Under 1B 17-19 also stay as approved.', r2tp(H + 'html/18-two-answer-wrong-tap-390x844.html', 390, 844), (390, 844))]
sheet('/workspace/v608build/round2/sheets/trim-pick-1A-vs-1B-390.png', 'Ceiling trim at 390: which rooms?', 'Which one, 1A or 1B?', t,
      'Home Lake room (screen 54) shown at 390. 320 renders are the same in both. Both PASTEs carry the verse scroll (+52); the combined pick sheet lists every combination. Maxwell t444u (QM-relayed). Staged only. Oct 31, 2026, MDT.', cols=4)
# 2) before/after strip of the affected rooms (390)
rooms = ['14-reveal-gentle-retry', '16-say-it-maxwell-says-day1', '17-two-answer-pray-high-five', '18-two-answer-wrong-tap', '19-two-answer-right-done', '20-kitchen-say-it-picture-first', '21-kitchen-say-it-shown', '22-kitchen-server-talk', '32-home-lake-scene', '33-say-it-baby-hospital-reply', '54-phrase-ask-card', 'zone-lake-ask'] + [f'lake-step{i}' for i in range(1, 6)]
F = lambda s: ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', s); w, h = 195, 422
import textwrap; sys.path.insert(0, '/workspace/v608build/round2/asset-depth'); import round_totals as RT
FOOT = textwrap.wrap('+89 with 1A (all rooms, never over a target: 17-19 keep their ceiling); +89 with 1B (front desk and kitchen 20-22 only). 320 renders unchanged. Trim-clip check: 0 targets above the trim band. Staged only. Oct 31, 2026, MDT. ' + RT.for_sheet('home-lake-trim'), 250)
S = Image.new('RGB', (30 + len(rooms) * (w + 12), 2 * h + 150 + 22 * len(FOOT)), '#F4ECD8'); d = ImageDraw.Draw(S)
d.text((30, 14), 'Home-lake rooms at 390, before and after the 320-frame ceiling trim (extends t444u to the other rooms)', fill='#3A2410', font=F(22))
d.text((30, 46), 'Top: as approved (20: the same layout untrimmed; it has no approved 390 render). Bottom: 1A. 14 does not change; 17-19 keep their ceiling (the trim would cut Pray / High five). Under 1B only 20, 21 and 22 (kitchen) trim.', fill='#3A2410', font=F(15))
for i, r in enumerate(rooms):
    x = 30 + i * (w + 12)
    if r.startswith('lake-step'): before = '/workspace/v608build/scenes/tod/' + r + '-390.html'
    elif r.startswith('zone'): before = '/workspace/v608build/round2/sky-options/B/html/zone-lake-ask-390x844.html'
    elif r.startswith('20-'): before = H + 'html/20-kitchen-say-it-picture-first-390x844-before.html'
    else: before = V + r + '.html'
    for j, p in enumerate((r2tp(before, 390, 844), r2tp(H + f'html/{r}-390x844.html', 390, 844))):
        S.paste(Image.open(p).convert('RGB').resize((w, h), Image.LANCZOS), (x, 110 + j * (h + 10)))
    d.text((x, 84), r.split('-')[0] if not r.startswith(('zone', 'lake')) else r.replace('-ask', ''), fill='#3A2410', font=F(14))
for i, t in enumerate(FOOT): d.text((30, 2 * h + 140 + 22 * i), t, fill='#3A2410', font=F(14))
S.save('/workspace/v608build/round2/sheets/home-lake-trim-before-after-390.png'); print('ok')
