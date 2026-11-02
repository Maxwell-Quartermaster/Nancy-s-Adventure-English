# Auditor gate 2b29ce71: the 7.1 flaw is also in CURRENT v5-37 ("Tap the Wash the baby."). Before = v5-37 rule (tapPrompt "Tap the {word}" for a 1-3 word en)
# on bh-12; after = the B1 rule (v6-08): a sentence shows its own en. Both drawn in today's Home Lake template; CURRENT is not touched.
import sys, json; sys.path.insert(0, '/workspace/v608build/screens'); sys.argv = ['x']
import play_v608 as P
from PIL import Image, ImageDraw, ImageFont
V = json.load(open('/workspace/nancys-adventure-english-v5-37-cards.json')); tp = V['uiText']['tapPrompt']; c = [c for c in V['cards'] if c['id'] == 'bh-12'][0]
before = [P.tx(tp['en'].replace('{word}', c['en']), 'e22'), P.tx(tp['th'].replace('{word}', c['th']), 't17', 'line-height:1.7')]
after = [P.tx(c['en'], 'e22', 'margin-bottom:10px'), P.tx(c['th'], 't17', 'line-height:1.7')]
for nm, ln in (('before', before), ('after', after)):
    b, g = P.base('lake'); doc = P.page(390, 844, b + P.top('lake') + P.Z.qcard2(390, 844, ln)); open(nm + '.html', 'w').write(doc); P.S.shot(doc, nm + '.png', 390, 844, 'v537wb-' + nm)
F = lambda s: ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', s)
S = Image.new('RGB', (840, 844 + 110), '#F4ECD8'); d = ImageDraw.Draw(S)
d.text((20, 12), 'bh-12 ask card: v5-37 rule | B1 rule (v6-08). CURRENT v5-37 unchanged.', fill='#3A2410', font=F(19))
d.text((20, 40), 'Fix this in CURRENT too, or leave v5-37 as is until v6-08 ships?', fill='#7A1E12', font=F(16))
for i, (nm, t) in enumerate((('before', 'v5-37: "Tap the Wash the baby."'), ('after', 'B1: "Wash the baby."'))):
    d.text((20 + i*410, 70), t, fill='#3A2410', font=F(15)); S.paste(Image.open(nm + '.png').convert('RGB').resize((390, 844)), (20 + i*410, 94))
S.save('v537-wash-the-baby-before-after.png'); print('ok')
