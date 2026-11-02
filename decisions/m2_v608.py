# m2 re-shot from the current v6-08 harness (Maxwell t421u: latest version only): Sound Duel 34/35 at 390, A = speaker top-right (approved v6-04 look), B = speaker at the card's bottom-right.
import sys; sys.path.insert(0, '/workspace/v608build/screens'); sys.argv = ['x']
import play_v608 as P
from PIL import Image, ImageDraw, ImageFont
out = []
for st, n in ((None, '34'), ('right', '35')):
    a = P.page(390, 844, P.duel(st)); b = P.page(390, 844, P.duel(st).replace("right:8px;top:8px", "right:8px;bottom:6px", 1))   # S2 (Auditor 1748 gate): 8 pt from the tiles
    for k, doc in (('A', a), ('B', b)): open(f'm2-{k}-{n}-v608.html', 'w').write(doc); P.S.shot(doc, f'm2-{k}-{n}-v608.png', 390, 844, f'm2{k}{n}'); out.append((k, n))
F = lambda s: ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', s)
S = Image.new('RGB', (20 + 4*410, 844 + 110), '#F4ECD8'); d = ImageDraw.Draw(S)
d.text((20, 12), 'Sound Duel speaker at 390 (v6-08 renders): A = top right, over the tile corner (v6-04 look); B = speaker at the card\'s bottom-right', fill='#3A2410', font=F(18))
d.text((20, 42), 'Which speaker spot for Sound Duel at 390: A or B?', fill='#7A1E12', font=F(17))
for i, (k, n) in enumerate(out):
    d.text((20 + i*410, 72), ('A  top right - ' if k == 'A' else "B  speaker at the card's bottom-right - ") + n, fill='#3A2410', font=F(14))
    S.paste(Image.open(f'm2-{k}-{n}-v608.png').convert('RGB').resize((390, 844)), (20 + i*410, 96))
S.save('m2-sound-duel-speaker-A-B-390-v608.png'); print('ok')
