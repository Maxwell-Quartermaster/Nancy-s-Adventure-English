# "Nancy's eyes" showcase tour (Maxwell t446u, QM-relayed): the main path from the staged round 2 build (round2b: sky B at 320, 16 pt edges,
# guardian on the chip line, screen 33 inert, round 2 ask wording). 390 renders, plus a 320 copy where the layout differs. Sheets of 4-6.
import sys, os, re, json, subprocess, hashlib
sys.path.insert(0, '/workspace/v608build/round2/sheets'); from sheetkit import sheet, r2tp
V = '/workspace/screens-v608/html/'; ST = '/workspace/v608build/scenes/stage/html/'; B = '/workspace/v608build/round2/sky-options/B/html/'
O = '/workspace/v608build/round2/showcase/'; TL = O + 'tiles/'
P, S = (390, 844), (320, 568)
SHEETS = [
 ('1-opening', 'Opening the game', [
   ('1', 'Title screen.', V + '01-title.html', P),
   ('2', 'Verse of the day pops up over the menu.', V + '02-main-menu-verse-popup.html', P),
   ('3', 'Main menu.', V + '03-main-menu.html', P),
   ('4', 'The map on day 1.', V + '05-map-day1.html', P),
   ('5', 'She taps Word Meadow: the zone chooser.', V + '07-map-word-meadow-chooser.html', P)]),
 ('2-zones', "Each zone's first scene", [
   ('6', 'Word Meadow, first ask.', V + '10-word-meadow-scene.html', P),
   ('6s', 'Word Meadow at 320 × 568: the scene shrinks so the kite stays below the top bar.', V + '10-word-meadow-scene-320x568.html', S),
   ('7', 'Golden Fields.', V + '31-golden-fields-scene.html', P),
   ('8', 'Home Lake.', V + '32-home-lake-scene.html', P),
   ('9', 'Echo Forest, first ask.', B + 'zone-forest-ask-390x844.html', P),
   ('9s', 'Echo Forest at 320 × 568: the owl and lantern stay below the top bar.', V + 'zone-forest-ask-320x568.html', S)]),
 ('3-asking', 'Asking and answering', [
   ('10', 'An ask card with a phrase.', V + '54-phrase-ask-card.html', P),
   ('11', 'A right answer.', V + '11-word-meadow-scene-right.html', P),
   ('12', 'The reveal: a hug card to say out loud.', V + '12-reveal-right.html', P),
   ('13', 'A gentle miss on a two-answer card.', V + '18-two-answer-wrong-tap.html', P),
   ('14', 'After a miss: "Now you know it."', V + '14-reveal-gentle-retry.html', P),
   ('15', 'Say it: a sight-word card.', V + '15-say-it-sight-words.html', P)]),
 ('4-walk-guardian', 'The walk and the Word Guardian', [
   ('16', 'The walk (screen 24, staged): the Guardian name sits on the zone-chip line.', ST + 'W24-walk-B-390x844.html', P),
   ('16s', 'The walk at 320 × 568.', ST + 'W24-walk-B-320x568.html', S),
   ('18', "The Guardian's hint: words of Jesus.", V + '26-guardian-hint-jesus-words.html', P),
   ('19', 'The Guardian kneels.', V + '27-guardian-kneels.html', P),
   ('20', 'The Guardian is won.', V + '28-guardian-win.html', P)]),
 ('5-rewards-pause', 'Rewards, gear, pause and the end of a level', [
   ('21', 'A verse scroll as a gift.', V + '29-verse-scroll-gift.html', P),
   ('22', 'Level up.', V + '23-level-up-reward.html', P),
   ('23', 'End of a Sound Duel round.', V + '36-sound-duel-round-done.html', P),
   ('24', 'Character gear.', V + '38-character-gear-mmo-tooltip.html', P),
   ('25', 'The golden pantry.', V + '45-character-golden-pantry.html', P),
   ('26', 'Back after a pause: one Continue button.', V + '48-continue-after-pause.html', P)]),
]
_n = 0   # tiles numbered in order; an 's' tile is the 320 copy of the tile before it
for _i, (_k, _t, _tl) in enumerate(SHEETS):
    _new = []
    for num, cap, html, wh in _tl:
        if num.endswith('s'): _new.append((f'{_n}s', cap, html, wh))
        else: _n += 1; _new.append((str(_n), cap, html, wh))
    SHEETS[_i] = (_k, _t, _new)
PH = re.compile(r'_{3,}|\(word\)|\{word\}|NEEDS NANCY|TODO|lorem|\?\?\?|TH:')
def visible(h): return re.sub(r'<[^>]+>', ' ', re.sub(r'<(script|style)[^>]*>.*?</\1>', ' ', h, flags=re.S))
index = ["# Nancy's eyes: showcase tour (Maxwell t446u, QM-relayed)", '', 'From the staged round 2 build (round2b, PASTE bfb0392b): round 2 ask wording on every ask, sky B at 320, 16 pt edges, Guardian on the chip line, screens 33 and 48 inert. '
         '390 renders; a 320 copy (tile "s") only where the scene layout differs. Answer with a tile number ("fix 13", "9s").', '']
dom = []
for key, title, tiles in SHEETS:
    rows = []
    for num, cap, html, wh in tiles:
        png = r2tp(html, *wh, outdir=TL)
        src = TL + os.path.basename(os.path.dirname(os.path.dirname(html))) + '--' + os.path.basename(html) if png.startswith(TL) else html
        txt = visible(open(src).read()); ph = PH.findall(txt); old = re.findall(r'Where is the [a-z]+\?|อยู่ที่ไหน', txt)
        dom.append((num, src, ph, old)); rows.append((num, cap, png, wh))
    out = O + f'showcase-{key}.png'
    sheet(out, f"Nancy's eyes, sheet {key[0]}: {title}", 'Reply with a tile number to fix it (for example "fix 13" or "9s").', rows,
          'Staged round 2 build (round2b, not frozen). Every word ask reads "Can you find the …?" with its Thai line (uiText, NEEDS NANCY). Maxwell t446u, QM-relayed. Oct 31, 2026, MDT.', cols=3)
    index.append(f'## Sheet {key[0]}: {title}  ({os.path.basename(out)}, md5 {hashlib.md5(open(out, "rb").read()).hexdigest()})')
    index += [f'- **{n}**: {c} ({os.path.basename(h)}{", 320 × 568" if w == S else ""})' for n, c, h, w in tiles]; index.append('')
    print(out, flush=True)
r = subprocess.run([sys.executable, '/tmp/dc1.py'] + [d[1] for d in dom], capture_output=True, text=True).stdout.splitlines()
issues = {dom[i][0]: r[2 * i + 1].split('issues: ', 1)[1] for i in range(len(dom))}
index += ['## Checks on every tile', '- DOM check (domcheck_r2: Thai 17 px+, Thai line height 1.7+, clipping, overlap, 44 pt, 16 pt edges): ' +
          ('all clean' if all(v == '[]' for v in issues.values()) else '; '.join(f'{k}: {v}' for k, v in issues.items() if v != '[]')),
          '- Placeholder text (___, (word), {word}, NEEDS NANCY, TODO): ' + (', '.join(f'{d[0]} {d[2]}' for d in dom if d[2]) or 'none'),
          '- Old ask wording left ("Where is the …?" / "อยู่ที่ไหน"): ' + (', '.join(f'{d[0]} {d[3]}' for d in dom if d[3]) or 'none'), '']
index += ['## Left out, and notes for Auditor (sending waits on Auditor)',
  '- Settings: no settings screen is rendered in v6-08 (46 backup view is not settings and shows a "(word) อยู่ไหน" review-queue line and a "bh-30 · ______" blank), so it is not in the tour.',
  '- 13 (meadow retry: the kite glows after a wrong tap, with "Take your time"): this is the after-miss grace hint the spec allows (PASTE :231 "Another tap: that object wiggles, the right one glows as a hint, then `wrongText` and a grace line; she tries again"). It already shows the after-miss state; unchanged, not in the tour.',
  '- 25 (guardian letters "t____/th/"): staged (round2.py P6, owner\'s yes 8:08 PM MDT, council ruling): sw-19 choices run -> ten (nm-15\'s own word), 0 chars, so two choices start with t. Screens 25 and 26 re-rendered; 25 is not a tour tile, 26 is tile 17.',
  '- 24-28 now carry the Guardian name on the zone-chip line (P5); 24 itself is replaced on the path by the staged walk (tile 16).',
  '- Tile 2: the menu under the verse pop-up is now inert (aria-hidden, no taps), 0 chars; png unchanged.',
  '- Home-lake rooms (tiles 8, 10, 14) are shown as approved: the 390 ceiling trim is still Maxwell\'s 1A/1B pick (round2/sheets/trim-pick-1A-vs-1B-390.png).',
  '- Near-duplicates skipped: 52 night title, 04/51 hearth menus, 06/08/09/53 maps, 11-13 meadow variants, 16/20/21 say-it, 19, 35, 37-47 other character pages.', '']
open(O + 'INDEX.md', 'w').write('\n'.join(index) + '\n'); print('\n'.join(index[-5:]))
