# Maxwell t425u: screen 24 (guardian run, sw-15 "walk"): A = framed plate top right (current v6-08) vs B = a small walking figure woven into the park, on the ground with a shadow.
import sys; sys.path.insert(0, '/workspace/v608build/screens'); sys.argv = ['x']
import play_v608 as P
from PIL import Image, ImageDraw, ImageFont
a = P.page(390, 844, P.grun('sw-15', 1.0))
b = a.replace(P.tplate('🚶'), P.gprop('🚶', 96, 446, 40), 1)
assert a != b
for k, doc in (('A', a), ('B', b)): open(f'walk24-{k}.html', 'w').write(doc); P.S.shot(doc, f'walk24-{k}.png', 390, 844, 'walk24' + k)
F = lambda s: ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', s)
S = Image.new('RGB', (20 + 2*410, 844 + 110), '#F4ECD8'); d = ImageDraw.Draw(S)
d.text((20, 12), 'Screen 24 "walk" at 390 (v6-08): A framed plate | B walker in the park', fill='#3A2410', font=F(19))
d.text((20, 42), 'For people pictures like "walk": A plate or B small figure in the scene?', fill='#7A1E12', font=F(16)); d.text((20, 62), 'A: 0 chars (spec now)   B: about +72 chars', fill='#3A2410', font=F(14))
for i, (k, t) in enumerate((('A', 'A: framed plate, top right (now)'), ('B', 'B: small walker on the far grass, with a shadow'))):
    d.text((20 + i*410, 80), t, fill='#3A2410', font=F(14)); S.paste(Image.open(f'walk24-{k}.png').convert('RGB').resize((390, 844)), (20 + i*410, 96))
S.save('walk24-A-B-390.png'); S.crop((420, 380, 840, 700)).save('_w_prev.png')
