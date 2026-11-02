# Batch 9 sheet: screens 17-19 at 390 (t406u hand emoji on the bordered plates), from the current screens-v608 renders.
from PIL import Image, ImageDraw, ImageFont
F = lambda s: ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', s); V = '/workspace/screens-v608/png/'
S = Image.new('RGB', (1250, 954), '#F4ECD8'); d = ImageDraw.Draw(S)
d.text((20, 12), '17-19 at 390 (t406u): hand emoji on the same bordered plates', fill='#3A2410', font=F(19))
d.text((20, 42), 'Do 17, 18 and 19 look consistent with hand emoji on the plates?', fill='#7A1E12', font=F(15))
for i, (f, t) in enumerate((('17-two-answer-pray-high-five', '17 ask'), ('18-two-answer-wrong-tap', '18 wrong tap'), ('19-two-answer-right-done', '19 right, Done'))):
    d.text((20 + i * 410, 76), t, fill='#3A2410', font=F(14)); S.paste(Image.open(V + f + '.png').convert('RGB').resize((390, 844)), (20 + i * 410, 98))
S.save('emoji-17-18-19-390.png')
