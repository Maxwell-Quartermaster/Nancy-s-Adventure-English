# Neutral side-by-side sheets for the main-menu concepts and the extended map. Every tile = a current r2h render (md5 listed in the .md).
import hashlib, os
from PIL import Image, ImageDraw, ImageFont
R = '/workspace/v608build/round2/r2h/'; PNG = R + 'png/'; OUT = R + 'sheets/'
LF = '/usr/share/fonts/truetype/sand-box/google/Lilita One/LilitaOne-Regular.ttf'; DF = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
STAMP = 'paste_1b 317e91ce · pointer f6dac2d0 · r2h renders (CDP, DPR 2) · sidecar JSON per tile'
md5 = lambda p: hashlib.md5(open(p, 'rb').read()).hexdigest()
def wrap(dr, t, f, w):
    out, line = [], ''
    for word in t.split():
        if dr.textlength((line + ' ' + word).strip(), font=f) > w: out.append(line); line = word
        else: line = (line + ' ' + word).strip()
    return out + [line]
def sheet(name, title, cols, rows, notes):
    # cols: list of (label, [png per row]); notes: per col text lines (same facts for each)
    S = 0.5; lab = ImageFont.truetype(LF, 44); f = ImageFont.truetype(DF, 19); tf = ImageFont.truetype(LF, 34)
    cw = 390 * 2 * S + 60; heights = [max(Image.open(PNG + c[1][r]).height for c in cols) * S for r in range(rows)]
    Wd = int(60 + len(cols) * cw); Hd = int(130 + sum(h + 40 for h in heights) + 380)
    im = Image.new('RGB', (Wd, Hd), '#FFFFFF'); dr = ImageDraw.Draw(im)
    dr.text((60, 30), title, font=tf, fill='#222222'); y0 = 110; src = []
    for i, (lb, files) in enumerate(cols):
        x = int(60 + i * cw); dr.text((x, y0 - 10), lb, font=lab, fill='#222222'); y = y0 + 50
        for r in range(rows):
            p = PNG + files[r]; t = Image.open(p).convert('RGB'); t = t.resize((int(t.width * S), int(t.height * S)), Image.LANCZOS)
            im.paste(t, (x, y)); dr.rectangle((x - 1, y - 1, x + t.width, y + t.height), outline='#999999')
            dr.text((x, y + t.height + 6), files[r].replace('.png', ''), font=ImageFont.truetype(DF, 14), fill='#555555'); y += int(heights[r]) + 40
            src.append((files[r], md5(p)))
        yy = y
        for ln in notes[i]:
            for w in wrap(dr, ln, f, cw - 40): dr.text((x, yy), w, font=f, fill='#222222'); yy += 25
    dr.text((60, Hd - 36), STAMP, font=ImageFont.truetype(DF, 15), fill='#555555')
    im.save(OUT + name + '.png')
    md = [f'# {title}', '', STAMP, '', 'PASTE for this sheet: 317e91ce86f073c961f8169183d2bbd3', '', '| tile | source render | md5 |', '|---|---|---|']
    md += [f'| {lb} | round2/r2h/png/{fn} | {h} |' for (lb, _), (fn, h) in zip([(c[0], None) for c in cols for _ in range(rows)], src)]
    md += ['', '## Notes per option (cost / what it leaves; no default)'] + [f'- **{c[0]}**: ' + ' '.join(notes[i]) for i, c in enumerate(cols)]
    open(OUT + name + '.md', 'w').write('\n'.join(md) + '\n'); return OUT + name + '.png'
M = lambda m: (m, [f'{m}-main-menu-390x844.png', f'{m}-main-menu-320x568.png'])
notes = [
 ['Order: title log, top bar (hearth at its right end), hero band, scenery window, Gear, Shop, Adventure Map.',
  'Cost: buttons 72 pt tall (6.2 says 60 pt; EN 20 px over TH 17 px/1.7 needs 51 pt of face).',
  'Leaves: 390 scenery window 176 pt; 320 no scenery window (band 140 pt, buttons from y 320).'],
 ['Order: top bar (hearth at its right end), scenery window, hero band, Gear, Shop, Adventure Map.',
  'Cost: no title log (6.2 says "Map\'s look ... header logs"); buttons 72 pt tall (6.2 says 60 pt).',
  'Leaves: 390 hero band 268 pt, cards 124 x 172 pt, heroes 1.3x; scenery window 182 pt (390), 84 pt (320).'],
 ['Order: title log, top bar (hearth at its right end), scenery window, hero band, then Gear, Shop, Adventure Map as stops (44 pt dot + plate) on one dashed path on a parchment board.',
  'Cost: plates 72 pt tall (6.2 says 60 pt); three new dot emblems (gear, star, map) not in picPlan.',
  'Leaves: 390 scenery window 156 pt; 320 no scenery window; plates 278 pt (390) / 218 pt (320) wide.']]
a = sheet('r2h-M-menus', 'Main menu concepts M1 / M2 / M3  (390 x 844 top, 320 x 568 below)', [M('M1'), M('M2'), M('M3')], 2, notes)
b = sheet('r2h-map-extended', 'Adventure Map: hero select moved to the main menu, sheet extended down', [('Map now (r2h)', ['05-map-day1-390x844.png', None]), ('Map extended', ['map-extended-390x844.png', 'map-extended-320x568.png'])][:0] or
          [('Map now (r2h) 390', ['05-map-day1-390x844.png']), ('Map extended 390', ['map-extended-390x844.png']), ('Map extended 320', ['map-extended-320x568.png'])], 1,
          [['Hero band (173 pt) at the bottom; rows 286-638.', 'No 320 render of the current map exists in r2h.'],
           ['Hero band removed; sheet 197-836; rows moved down 172 pt to 458-810 (16 pt above the 34 pt safe area); art strips moved with the rows; spare sky above.'],
           ['Native 320 build: rows 82 pt (as 390), 4 rows 196-548; art shifted 70 left; dashed path redrawn; Back 64, stats 120, level 88.']])
print(a, md5(a)); print(b, md5(b))
