# Scene before/after sheets from the t439u stage renders (one layout scaled as one piece): Now = current v6-08 screen, After 390 and After 320 = stage/png. Replaces the superseded-t439u sheets under the same names.
from PIL import Image, ImageDraw, ImageFont
F = lambda s: ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', s)
def sheet(out, title, q, cols, w=390, h=844):
    S = Image.new('RGB', (20 + len(cols)*(w + 20), h + 110), '#F4ECD8'); d = ImageDraw.Draw(S)
    d.text((20, 12), title, fill='#3A2410', font=F(20)); d.text((20, 42), q, fill='#7A1E12', font=F(17))
    for i, (t, p) in enumerate(cols):
        d.text((20 + i*(w + 20), 72), t, fill='#3A2410', font=F(14)); S.paste(Image.open(p).convert('RGB').resize((w, int(w * 568 / 320)) if '320x568' in p else (w, h)), (20 + i*(w + 20), 96))   # 320 keeps its own shape
    S.save(out); print(out)
V = '/workspace/screens-v608/png/'
# K3: the old L1-L5 strip is superseded by tod/strip-<zone>-steps-<390|320x568>.png (tod_v608.py)
S = [('E', 'Front desk (t426u: key rack, far truck, full door)', 'Confirmation: front desk with your changes.', V + '32-home-lake-scene-390check.png', 'E-lake-front-desk'),
     ('A', 'Word Meadow: park by the pond (second layout)', 'Does the pond layout work as a second park?', V + '10-word-meadow-scene.png', 'A-meadow-evening-pond'),
     ('B', 'Listen and find (3rd target spoken only)', 'Is the spoken-only card clear?', V + '10-word-meadow-scene.png', 'B-meadow-listen-and-find'),
     ('C', 'Golden Fields: count it (cow scene)', 'Does count it read well?', V + '31-golden-fields-scene-390check.png', 'C-fields-count-it'),
     ('D', 'Golden Fields: big or small?', 'Do the two baskets read well?', V + '31-golden-fields-scene-390check.png', 'D-fields-big-or-small'),
     ('F', 'Home Lake: room set for a meal (Kitchen runs)', 'Does the meal table fit the room?', V + '32-home-lake-scene-390check.png', 'F-lake-night-table'),
     ('G', 'Echo Forest: picture pairs (6 pairs)', 'Do pictures in the tiles help?', V + '34-echo-forest-sound-duel.png', 'G-forest-picture-duel'),
     ('H', 'Echo Forest at dawn (zone steps 1-2)', 'Does the dawn forest look right?', V + '34-echo-forest-sound-duel.png', 'H-forest-dawn')]
for k, t, q, now, n in S: sheet('before-after-%s.png' % k, t, q, [('Now (v6-08)', now), ('After at 390: ' + k, 'stage/png/%s-390x844.png' % n), ('After at 320 (same layout, fit to width)', 'stage/png/%s-320x568.png' % n)])
