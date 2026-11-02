# r2h before/after sheet: every PNG is an r2h render from round2/r2h/png (send rule: no stale renders). Neutral labels.
from PIL import Image, ImageDraw, ImageFont
import hashlib, os
R = '/workspace/v608build/r2h-rerun-stage/r2h/'; ST = '/workspace/v608build/r2h-rerun-stage/';   # stage-only (1:43 AM)
F = lambda s: ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', s)
B = lambda s: ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', s)
T = [('6', 'Word Meadow scene (screen 10): tree rooted, walkway off, dots -> tufts (t467u/t473u)', ['10-word-meadow-scene-390x844', '10-word-meadow-scene-320x568']),
     ('8', 'Home Lake home room (screen 32 / zone ask): tie hangs straight (t472u); wall unchanged under 1B', ['32-home-lake-scene-390x844', 'zone-lake-ask-320x568']),
     ('9', 'Echo Forest (zone ask, sky B): moon to the sky centre (t471u)', ['zone-forest-ask-390x844', 'zone-forest-ask-320x568', 'zone-forest-ask-375x812']),
     ('10', 'Phrase ask (screen 54): bed 8 pt forward, tie straight (t472u); wall unchanged under 1B', ['54-phrase-ask-card-390x844', '54-phrase-ask-card-320x568']),
     ('11', 'Right answer (screen 11): tree, walkway, tufts (t473u)', ['11-word-meadow-scene-right-390x844']),
     ('12', 'Reveal (screen 12): tree, walkway, tufts (t473u)', ['12-reveal-right-390x844']),
     ('15', 'Say it, sight words (screen 15): tree, walkway, tufts (t476u)', ['15-say-it-sight-words-390x844']),
     ('K', 'Kitchen (screen 21): taller wall, 1B (t470u/t492u); tie straight', ['21-kitchen-say-it-shown-390x844', '21-kitchen-say-it-shown-320x568']),
     ('M', 'Map (screen 05): Home Lake colour #D9663F -> #F05A00 (t474u)', ['05-map-day1-390x844']),
     ('14', 'Screen 14 gentle retry: Home Lake colour (t474u) and tie (t474u item 2)', ['14-reveal-gentle-retry-390x844', '14-reveal-gentle-retry-320x568']),
     ('G', 'Guardian 24-27: red boss bar (boss step); 390 nameplate + bar, 375/320 bar under the zone chip', ['24-guardian-run-entry-390x844', '25-guardian-hint-letters-320x568', '26-guardian-hint-jesus-words-375x667', '27-guardian-kneels-390x844']),
     ('W', 'Watchman 2a-2c: ask wording (r2tp), walkway strokes M118/M330 removed, zone-meadow-ask 320 and sky-B', ['zone-meadow-ask-320x568', 'zone-meadow-ask-390x844-skyB', 'stage-A-meadow-evening-pond-390x844', 'stage-B-meadow-listen-and-find-390x844'])]
import sys as _sys; AFTER = 'after-only' in _sys.argv
TH = 300; rows = []; used = []; caps = []
for num, lab, names in T:
    ims = []
    for n in names:
        for v in ((n,) if AFTER else (n + '-before', n)):
            p = R + f'png/{v}.png'; im = Image.open(p).convert('RGB'); im = im.resize((int(im.width * TH / im.height), TH)); ims.append((v, im)); used.append(p)
    w = sum(i.width + 12 for _, i in ims) + 20; row = Image.new('RGB', (max(w, 1180), TH + 64), 'white'); d = ImageDraw.Draw(row)
    d.text((10, 6), f'{num}  {lab}', fill='#10170F', font=B(16)); x = 10; caps.append(f'{num}  {lab}')
    for v, i in ims:
        cap = ('before ' if v.endswith('-before') else 'after ') + v.replace('-before', '').split('-')[-1]; caps.append(cap); d.text((x, 30), cap, fill='#333', font=F(12)); row.paste(i, (x, 50)); x += i.width + 12
    rows.append(row)
W = max(r.width for r in rows); H = sum(r.height for r in rows) + 120; S = Image.new('RGB', (W, H), 'white'); d = ImageDraw.Draw(S)
TITLE = ('r2h fixes, after only' if AFTER else 'r2h before/after') + ', base trim 1B (Maxwell t492u). Every image is an r2h render (r2h/png). paste_1b 317e91ce, pointer f6dac2d0.'
d.text((10, 10), TITLE, fill='#10170F', font=B(18)); y = 44
for r in rows: S.paste(r, (0, y)); y += r.height
d.text((10, y + 8), 'Render-only fixes, 0 PASTE chars. PASTE costs are in COSTS-r2h.md.', fill='#333', font=F(13))
out = ST + 'sheets/r2h-after.png' if AFTER else R + 'sheets-ref/r2h-before-after.png'; S.save(out)
SRC = ''.join(f'{hashlib.md5(open(p,"rb").read()).hexdigest()}  {p}\n' for p in used) + f'caption {TITLE}\n' + ''.join(f'caption {c}\n' for c in caps)
for sc in (out + '.sources.txt', out[:-4] + '.sources.txt'): open(sc, 'w', encoding='utf-8').write(SRC)   # <png>.sources.txt (1:45 AM) and the older <name>.sources.txt, same content
print(out, S.size, hashlib.md5(open(out, 'rb').read()).hexdigest())
