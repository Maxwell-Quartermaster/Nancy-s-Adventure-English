# t411u pairs: screen 10 (v6-06 | v6-08), 320 m1 screens 22/33/34/35 (v6-06 | v6-08), and the m1 gate pair 24/25 at 390 (v6-07 8 px | v6-08 10 px)
from PIL import Image, ImageDraw, ImageFont
F = lambda s: ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', s)
A = '/workspace/screens-v606/png/'; B = '/workspace/screens-v608/png/'; C7 = '/workspace/screens-v607/png/'
def pair(out, l, r, lt, rt, w, h, title, q):
    S = Image.new('RGB', (2*w + 60, h + 110), '#F4ECD8'); d = ImageDraw.Draw(S)
    d.text((20, 12), title, fill='#3A2410', font=F(20)); d.text((20, 40), q, fill='#7A1E12', font=F(16))
    for i, (p, t) in enumerate(((l, lt), (r, rt))):
        d.text((20 + i*(w + 20), 70), t, fill='#3A2410', font=F(15)); S.paste(Image.open(p).convert('RGB').resize((w, h)), (20 + i*(w + 20), 94))
    S.save(out); print(out)
pair('10-v606-v608.png', A+'10-word-meadow-scene.png', B+'10-word-meadow-scene.png', 'v6-06', 'v6-08 (t402u wording, v6-06 card rhythm)', 390, 844,
     'Screen 10 at 390: v6-06 layout back, t402u wording, no Thai draft chip', 'Does v6-08 10 match the v6-06 10 you liked?')
for n in ('22-kitchen-server-talk', '33-say-it-baby-hospital-reply', '34-echo-forest-sound-duel', '35-sound-duel-right'):
    pair(n[:2] + '-320-v606-v608.png', A+n+'-320x568.png', B+n+'-320x568.png', 'v6-06', 'v6-08 (v6-06 buttons, speaker 44 pt in its own slot)', 320, 568,
         'Screen %s at 320x568' % n[:2], 'Speaker centred in its own space, at least 8 px from the buttons?')
for n in ('24-guardian-run-entry', '25-guardian-hint-letters'):
    pair(n[:2] + '-390-m1-gap.png', C7+n+'-390check.png', B+n+'.png', 'v6-07 (8 px gap, unclaimed)', 'v6-08 (approved 10 px gap back)', 390, 844,
         'Screen %s at 390: plate gap (Auditor m1)' % n[:2], 'Render-only fix, no decision needed.')
