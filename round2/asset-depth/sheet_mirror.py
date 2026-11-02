# Sheet (b): Word Meadow at 390, current vs mirrored (park and pond layouts). Usage: python3 sheet_mirror.py
from PIL import Image, ImageDraw, ImageFont
F = lambda s: ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', s)
O = '/workspace/v608build/round2/asset-depth/'
cols = [('Park: now', 'mirror-B-meadow-listen-and-find-now-390x844.png'), ('Park: mirrored (odd runs)', 'mirror-B-meadow-listen-and-find-mirrored-390x844.png'),
        ('Pond: now', 'mirror-A-meadow-evening-pond-now-390x844.png'), ('Pond: mirrored (odd runs)', 'mirror-A-meadow-evening-pond-mirrored-390x844.png')]
w, h = 390, 844; S = Image.new('RGB', (20 + 4*(w + 20), h + 150), '#F4ECD8'); d = ImageDraw.Draw(S)
d.text((20, 12), 'Word Meadow at 390: mirrored scene art on odd runs (council idea, Watchman; +146 chars with the glyph rule, no new art)', fill='#3A2410', font=F(20))
d.text((20, 42), 'Show the scene art mirrored on every other run in a zone?', fill='#7A1E12', font=F(17))
d.text((20, 70), 'Only the scene art flips. Sam, the words, Thai, emoji, digits, svg pictures and the wall clock stay the right way round.', fill='#3A2410', font=F(14))
for i, (t, p) in enumerate(cols):
    d.text((20 + i*(w + 20), 104), t, fill='#3A2410', font=F(15)); S.paste(Image.open(O + p).convert('RGB').resize((w, h), Image.LANCZOS), (20 + i*(w + 20), 130))
S.save(O + 'mirror-word-meadow-390-now-vs-mirrored.png'); print('ok')
