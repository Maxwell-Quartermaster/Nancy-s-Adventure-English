# Council 8:43 PM MDT: ONE combined pick sheet for Maxwell: trim 1A/1B, Maxwell's lean ask (letter game / state pairs), and the long verse at 320 (A scroll / B shorter
# verses), each with its own cost, plus every combination with the chars left after the ramp (40). Neutral: no default, no leaning labels. Numbers from round_totals.py.
import sys; sys.path.insert(0, '/workspace/v608build/round2/asset-depth'); sys.path.insert(0, '/workspace/v608build/round2/sheets')
import round_totals as RT; from sheetkit import r2tp
from PIL import Image, ImageDraw, ImageFont
BF = lambda s: ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', s); RF = lambda s: ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', s)
INK, RED, GOLD, BG = '#3A2410', '#7A1E12', '#8A5F16', '#F4ECD8'
import textwrap
import sys as _s0; _s0.path.insert(0, '/workspace/v608build/round2/r2d'); import r2_fit_table as FT0   # r2e: the under-20 note and the Thai reserve line come from the fit table
def wrap(d, x, y, t, f, chars, fill=INK):
    for l in textwrap.wrap(t, chars): d.text((x, y), l, fill=fill, font=f); y += f.size + 5
    return y
H = '/workspace/v608build/round2/ceiling-cap/home-lake/'; V = '/workspace/screens-v608/'; B = '/workspace/v608build/decisions/b2b/'
PICKS = [('Trim (Maxwell t444u, QM-relayed)', [('1A', 'All rooms, never over a target', '+%d' % RT.TRIM['1A'], r2tp(H + 'html/54-phrase-ask-card-390x844.html', 390, 844)),
                                               ('1B', 'Front desk and kitchen only', '+%d' % RT.TRIM['1B'], r2tp(V + 'html/54-phrase-ask-card.html', 390, 844))]),
         ("Maxwell's ask, lean (+ ramp 40)", [('Letter game', 'The picture grows with each right letter', '+%d' % RT.ASK['letter game'], B + 'letters-A-grows.png'),
                                                         ('State pairs', '"Can you find the open book?"', '+%d' % RT.ASK['state pairs'], B + 'state-pair-open-book.png')])]
tw = 170; Wd = 40 + 3 * (2 * (tw + 16) + 40) - 40; S = Image.new('RGB', (Wd, 1900), BG); d = ImageDraw.Draw(S)
y = wrap(d, 30, 18, 'Two picks together: the ceiling trim and Maxwell\'s ask', BF(26), 90)
y = wrap(d, 30, y + 4, 'Which trim, which ask? Each option shows its own cost; the tables show every combination and the savings Maxwell could choose.', BF(18), 110, RED) + 14
x0 = 30
for title, opts in PICKS:
    d.text((x0, y), title, fill=INK, font=BF(17))
    for k, (lab, cap, cost, png) in enumerate(opts):
        x = x0 + k * (tw + 16); im = Image.open(png).convert('RGB'); im = im.resize((tw, round(im.height * tw / im.width)), Image.LANCZOS)
        d.rectangle((x, y + 30, x + 56, y + 62), fill=INK); d.text((x + 6, y + 33), lab if len(lab) <= 3 else lab[0], fill='#FFF8E1', font=BF(22))
        d.text((x + 64, y + 36), cost + ' chars', fill=GOLD, font=BF(17)); S.paste(im, (x, y + 70)); wrap(d, x, y + 76 + im.height, (lab + ': ' if len(lab) > 3 else '') + cap, RF(13), 26)
    x0 += 2 * (tw + 16) + 40
x1 = x0; d.text((x1, y), 'Long verse at 320', fill=INK, font=BF(17))
im = Image.open(V + 'png/02b-main-menu-verse-popup-longest-320x568-scrolled.png').convert('RGB'); im = im.resize((tw, round(im.height * tw / im.width)), Image.LANCZOS); S.paste(im, (x1, y + 70))
wrap(d, x1, y + 34, 'Not a pick', BF(15), 30, GOLD); wrap(d, x1, y + 76 + im.height, RT.VERSE_FIX[0].upper() + RT.VERSE_FIX[1:] + '.', RF(13), 26)
y += 70 + 370 + 120
y = wrap(d, 30, y, 'Every combination (limit 188,200; read from the staged PASTEs: %s banked on both paths)' % RT.fmt(RT.STAGED['1A']), BF(18), 120) + 10
cols = [30, 160, 420, 640, 860]; hdr = ['Trim', 'Ask (lean)', 'Ask + ramp', 'Banked', 'Result']
for c, t in zip(cols, hdr): d.text((c, y), t, fill=INK, font=BF(15))
y += 26; d.line((30, y - 4, Wd - 30, y - 4), fill=INK, width=2)
for t, a_, left in RT.COMBOS:
    row = [f"{t} (+{RT.TRIM[t]})", f'{a_} {RT.ASK[a_]}', RT.fmt(RT.ASK[a_] + RT.RAMP), RT.fmt(RT.bank(t)), RT.verdict(left)]
    for cx, s_ in zip(cols, row): d.text((cx, y), s_, fill=(RED if left < 0 and cx == cols[-1] else INK), font=RF(15))
    y += 24
y += 18
y = wrap(d, 30, y, 'Savings Maxwell could choose himself (each row is the same under 1A and 1B)', BF(18), 120) + 10
cols = [30, 230, 520, 740, 960]; hdr = ['Ask (lean)', 'Saving', 'Ask + ramp, net', 'Banked', 'Result']
for c, t in zip(cols, hdr): d.text((c, y), t, fill=INK, font=BF(15))
y += 26; d.line((30, y - 4, Wd - 30, y - 4), fill=INK, width=2)
SV = {sv: (c, keep) for sv, c, keep in RT.SAVES}
for a_, sv, left in RT.CHOICES:
    c, keep = SV[sv]; net = RT.ASK[a_] + (RT.RAMP - c if keep else 0)
    row = [f'{a_} {RT.ASK[a_]}', f'{sv} (-{c})', RT.fmt(net) + ('' if keep else ' (no ramp)'), RT.fmt(RT.STAGED['1A']), RT.verdict(left)]
    for cx, s_ in zip(cols, row): d.text((cx, y), s_, fill=(RED if left < 0 and cx == cols[-1] else INK), font=RF(15))
    y += 24
    if sv == RT.SAVES[-1][0]: d.line((30, y - 2, Wd - 30, y - 2), fill='#C9B48A', width=1); y += 6
y += 14
y = wrap(d, 30, y, FT0.RESERVE, RF(15), 140) + 10   # r2e
DEADLINE = ("Timing: Maxwell's R2 pick and screen 26 pick need to land by Nov 2 (freeze Nov 4, 11:59 PM). If they slip past Nov 3, there is no R2 ask in this paste and v6-09 picks it up. "
            "Writing and Thai-checking time (Instructor): state pairs about 1 hour, letter game about 2 hours. Every new string goes on Nancy's Nov 7 list either way.")
y = wrap(d, 30, y, DEADLINE, BF(15), 130, RED) + 12   # r2e (brief task 5)
import sys as _s3; _s3.path.insert(0, '/workspace/v608build/round2/r2d'); import r2_fit_table as FT   # r2d (Auditor r2c H7): the screen 26 pick spends the same 403
J26 = 'The screen 26 pick spends the same %d: ' % RT.STAGED['1A'] + '; '.join(f"{o} (+{FT.COST[o]}) fits in {len(FT.fits(o))} of 16 R2 combinations" for o in FT.COST) + ' (full list on the screen 26 sheet).'
foot = ('The other R3 open picks (coin B 80, TG2 B 60, TG3 B 55, TG1 B+C 54, TG4 B 35, Echo recap 22, Bloodtide +2: 308) all together fit in no row. ' + J26 + ' '
        + RT.BUDGET + ' Staged PASTEs: 1A and 1B both %s chars. Verses unchanged (daily-verses.json 81295c9f). Oct 31, 2026, MDT.' % RT.fmt(RT.LIMIT - RT.STAGED['1A']) + RT.snap_line())
y = wrap(d, 30, y, foot, RF(14), 150, '#5A4A3A')
S = S.crop((0, 0, Wd, y + 20)); S.save('/workspace/v608build/round2/sheets/pick-combined-trim-ask-verse.png'); print('ok', S.size)
