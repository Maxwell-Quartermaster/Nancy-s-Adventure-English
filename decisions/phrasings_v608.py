# Batch 2 (t427u): ask-card phrasings on the current v6-08 Word Meadow scene at 390 (snap-1700MDT harness). Instructor Thai 8b765b95 (NEEDS NANCY).
import sys; sys.path.insert(0, '/workspace/v608build/screens'); sys.path.insert(0, '/workspace/v608build'); sys.argv = ['x']
import play_v608 as P, fixes_v608 as X
from PIL import Image, ImageDraw, ImageFont
base = P.page(390, 844, P.Z.screen('meadow', 'ask', 390, 844))
assert base.count('Where is the kite?') == 1 and base.count('kite อยู่ที่ไหน') == 1
ph = X.TPV_PHRASES[:4]
for i, (e, t) in enumerate(ph, 1):
    doc = base.replace('Where is the kite?', e.replace('{word}', 'kite'), 1).replace('kite อยู่ที่ไหน', t.replace('{word}', 'kite'), 1)
    open(f'phrasing-{i}.html', 'w').write(doc); P.S.shot(doc, f'phrasing-{i}.png', 390, 844, f'phr{i}')
F = lambda s: ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', s)
S = Image.new('RGB', (20 + 4*410, 844 + 150), '#F4ECD8'); d = ImageDraw.Draw(S)
d.text((20, 12), 'Ask card wording at 390 (v6-08 staged): one phrasing now, or rotate them in a run?', fill='#3A2410', font=F(19))
d.text((20, 42), 'A: keep "Where is the ...?" only (0 chars)   B: rotate all five + "Where are the ...?" for plurals (about +462 chars, leaves about 530)   C: plural line only (about +150)', fill='#7A1E12', font=F(15))
d.text((20, 68), "Phrase 5 \"Where's the ...?\" reads like 1. Thai drafts by Instructor, NEEDS NANCY.", fill='#3A2410', font=F(14))
for i, (e, t) in enumerate(ph):
    d.text((20 + i*410, 100), f'{i+1}: {e}', fill='#3A2410', font=F(15)); S.paste(Image.open(f'phrasing-{i+1}.png').convert('RGB').resize((390, 844)), (20 + i*410, 130))
S.save('ask-phrasings-1-4-390.png'); print('ok')
