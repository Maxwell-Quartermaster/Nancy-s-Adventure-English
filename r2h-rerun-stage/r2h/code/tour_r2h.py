# Showcase tour rebuilt from r2h renders only (Watchman 2d: tiles from round2/r2h, not screens-v608). Same tile list and captions as round2/showcase/tour.py.
import sys, os, hashlib
sys.path.insert(0, '/workspace/v608build/round2/sheets'); from sheetkit import sheet
R = '/workspace/v608build/r2h-rerun-stage/r2h/'; O = '/workspace/v608build/r2h-rerun-stage/showcase/'; P, S = (390, 844), (320, 568)   # stage-only (1:43 AM)
def png(tag):   # the r2h render: the fixed copy if fix() changed it, else the as-is render of the same source
    for p in (R + f'png/{tag}.png', R + f'png/{tag}-before.png'):
        if os.path.exists(p): return p
    raise SystemExit(f'no r2h render for {tag}')
SHEETS = [
 ('1-opening', 'Opening the game', [('Title screen.', '01-title-390x844', P), ('Verse of the day pops up over the menu.', '02-main-menu-verse-popup-390x844', P),
   ('Main menu (current; the M1/M2/M3 concepts are on sheets/r2h-M-menus.png).', '03-main-menu-390x844', P), ('The map on day 1.', '05-map-day1-390x844', P), ('She taps Word Meadow: the zone chooser.', '07-map-word-meadow-chooser-390x844', P)]),
 ('2-zones', "Each zone's first scene", [('Word Meadow, first ask.', '10-word-meadow-scene-390x844', P), ('Word Meadow at 320 × 568.', '10-word-meadow-scene-320x568', S),
   ('Golden Fields.', '31-golden-fields-scene-390x844', P), ('Home Lake.', '32-home-lake-scene-390x844', P), ('Echo Forest, first ask.', 'zone-forest-ask-390x844', P), ('Echo Forest at 320 × 568.', 'zone-forest-ask-320x568', S)]),
 ('3-asking', 'Asking and answering', [('An ask card with a phrase.', '54-phrase-ask-card-390x844', P), ('A right answer.', '11-word-meadow-scene-right-390x844', P),
   ('The reveal: a hug card to say out loud.', '12-reveal-right-390x844', P), ('A gentle miss on a two-answer card.', '18-two-answer-wrong-tap-390x844', P),
   ('After a miss: "Now you know it."', '14-reveal-gentle-retry-390x844', P), ('Say it: a sight-word card.', '15-say-it-sight-words-390x844', P)]),
 ('4-walk-guardian', 'The walk and the Word Guardian', [('The walk (screen 24, staged; approved tile, unchanged).', 'stage-W24-walk-B-390x844', P), ('The walk at 320 × 568.', 'stage-W24-walk-B-320x568', S),
   ("The Guardian's hint: words of Jesus (red bar 7/10).", '26-guardian-hint-jesus-words-390x844', P), ('The Guardian kneels (bar empty).', '27-guardian-kneels-390x844', P), ('Sam wins: the Guardian gives the scroll.', '28-guardian-win-390x844', P)]),
 ('5-rewards-pause', 'Rewards, gear, pause and the end of a level', [('A verse scroll as a gift.', '29-verse-scroll-gift-390x844', P), ('Level up.', '23-level-up-reward-390x844', P),
   ('End of a Sound Duel round.', '36-sound-duel-round-done-390x844', P), ('Character gear.', '38-character-gear-mmo-tooltip-390x844', P), ('The Shop.', '45-character-golden-pantry-390x844', P),
   ('Back after a pause: one Continue button.', '48-continue-after-pause-390x844', P)])]
n = 0; idx = ["# Nancy's eyes: showcase tour, r2h re-run", '', 'Every tile is an r2h render (r2h/png, CDP Chrome, DPR 2) with a sidecar JSON next to it. paste_1b 317e91ce, pointer f6dac2d0. Tile 16/16S is the approved stage png, unchanged.', '']
src = []
for key, title, tiles in SHEETS:
    rows = []
    for cap, tag, wh in tiles:
        if wh == S and rows: num = f'{n}s'
        else: n += 1; num = str(n)
        p = png(tag); rows.append((num, cap, p, wh)); src.append((key, num, p))
    out = O + f'showcase-{key}.png'
    sheet(out, f"Nancy's eyes, sheet {key[0]}: {title}", 'Reply with a tile number to fix it (for example "fix 13" or "9s").', rows,
          'r2h re-run (post-cleanup), paste_1b 317e91ce, pointer f6dac2d0. Every tile is an r2h render. Nov 1, 2026, MDT.', cols=3)
    # sources sidecar (1:45 AM): one md5 line per tile render, then the sheet title and one line per tile caption, exact text as drawn
    open(out + '.sources.txt', 'w', encoding='utf-8').write(''.join(f'{hashlib.md5(open(r[2], "rb").read()).hexdigest()}  {r[2]}\n' for r in rows)
        + f"caption Nancy's eyes, sheet {key[0]}: {title}\n" + ''.join(f'caption {r[1]}\n' for r in rows))
    idx.append(f'## Sheet {key[0]}: {title}  ({os.path.basename(out)}, md5 {hashlib.md5(open(out, "rb").read()).hexdigest()})')
    idx += [f'- **{r[0]}**: {r[1]} (r2h/png/{os.path.basename(r[2])}, md5 {hashlib.md5(open(r[2], "rb").read()).hexdigest()})' for r in rows]; idx.append(''); print(out, flush=True)
open(O + 'INDEX.md', 'w').write('\n'.join(idx) + '\n')
open(O + 'tiles.txt', 'w').write('\n'.join(f'{k}\t{num}\t{p}' for k, num, p in src) + '\n')
