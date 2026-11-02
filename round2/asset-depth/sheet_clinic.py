import sys; sys.path.insert(0, '/workspace/v608build/round2/sheets'); from sheetkit import r2tp
# Sheet (c): a council idea for v6-09 answering t442u. Today = the approved screen 32 render (Baby and Hospital plays in this home room).
from PIL import Image, ImageDraw, ImageFont
F = lambda s: ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', s)
O = '/workspace/v608build/round2/asset-depth/'
cols = [('Today: the home room (its towel ask)', r2tp('/workspace/screens-v608/html/32-home-lake-scene.html', 390, 844)),
        ('Idea: a calm check-up room', O + 'clinic-checkup-room-idea-390x844.png')]
import textwrap; sys.path.insert(0, '/workspace/v608build/round2/asset-depth'); import round_totals as RT
FOOT = textwrap.wrap('Render only; nothing staged. The bathroom needs a door this mock does not show. Oct 31, 2026, MDT. ' + RT.for_sheet('clinic-idea'), 130)
w, h = 390, 844; S = Image.new('RGB', (20 + 2*(w + 20) + 260, h + 130 + 20 * len(FOOT)), '#F4ECD8'); d = ImageDraw.Draw(S)
d.text((20, 12), 'A council idea for v6-09 answering t442u (not in v6-08)', fill='#3A2410', font=F(20))
d.text((20, 42), 'Should Baby and Hospital get its own check-up room in v6-09?', fill='#7A1E12', font=F(17))
for i, (t, p) in enumerate(cols):
    d.text((20 + i*(w + 20), 76), t, fill='#3A2410', font=F(14)); S.paste(Image.open(p).convert('RGB').resize((w, h), Image.LANCZOS), (20 + i*(w + 20), 100))
notes = ['In the room:', '- exam bed with a paper sheet', '- cabinet with a baby scale', '- sink, curtain on a rail', '- the same window', '', 'Plays only: blanket, water,', 'bathroom, pill, "I am hungry"', '(bh-18/23/24/26/27).', 'Baby-care cards stay', 'by the crib at home.', '', 'No signs or names.', '', 'Cost (staged PASTE):', '352 with props in words,', 'about 724 with 4 drawn', 'props. 516 are left and', 'your own asks need about', '820 at their leanest.', 'So: v6-09.']
for i, t in enumerate(notes): d.text((20 + 2*(w + 20), 104 + i*22), t, fill='#3A2410', font=F(13))
for i, t in enumerate(FOOT): d.text((20, h + 112 + 20 * i), t, fill='#5A4A30', font=F(13))
S.save(O + 'clinic-idea-v609-today-vs-checkup-390.png'); print('ok')
