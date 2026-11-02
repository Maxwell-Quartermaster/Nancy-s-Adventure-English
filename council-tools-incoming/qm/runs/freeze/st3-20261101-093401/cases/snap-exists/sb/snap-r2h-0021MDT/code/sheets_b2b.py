# Batch 2b decision sheets (one question each), from the staged v6-08 renders (/workspace/screens-v608, XP Purple) and this folder's mocks.
import textwrap
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
V = '/workspace/screens-v608/png/'
BF = lambda s: ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', s)
RF = lambda s: ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', s)
INK, RED, GOLD, BG = '#3A2410', '#7A1E12', '#8A6A10', '#F4ECD8'
def im(p, w=390): i = Image.open(p).convert('RGB'); return i.resize((w, round(i.height * w / i.width)))
def wrap(d, xy, text, font, fill, width_px):
    x, y = xy; cw = font.getlength('n'); lines = []
    for para in text.split('\n'): lines += textwrap.wrap(para, max(10, int(width_px / cw))) or ['']
    for ln in lines: d.text((x, y), ln, fill=fill, font=font); y += int(font.size * 1.35)
    return y
def sheet(out, title, question, panels, notes=(), pw=390, foot=None):
    # panels: list of (label, image or path, cost, caption)
    import sys as _s; _s.path.insert(0, '/workspace/v608build/round2/asset-depth'); import round_totals as _RT; _l = _RT.for_sheet(out)   # Chancellor 8:20 PM MDT: round total on every pick sheet
    if _l: foot = (foot + ' ' if foot else '') + _l
    n = len(panels); Wd = 20 + n * (pw + 20)
    imgs = [p[1] if isinstance(p[1], Image.Image) else im(p[1], pw) for p in panels]; ih = max(i.height for i in imgs)
    Hd = 200 + ih + 150 + 26 * 6 + (sum(40 + 24 * (len(t) // max(1, int(Wd / 9.5)) + t.count('\n') + 1) for t in notes) if notes else 0)
    S = Image.new('RGB', (Wd, Hd + 800), BG); d = ImageDraw.Draw(S)   # Auditor eb2674be: room for long footers (state pairs was cut off), cropped below
    y = wrap(d, (20, 14), title, BF(20), INK, Wd - 40) if title else 14; y = wrap(d, (20, y + 4), question, BF(18), RED, Wd - 40)
    y0 = y + 10
    for k, (lab, _, cost, cap) in enumerate(panels):
        x = 20 + k * (pw + 20); d.text((x, y0), lab, fill=INK, font=BF(16)); S.paste(imgs[k], (x, y0 + 26))
        yy = y0 + 26 + ih + 10; d.text((x, yy), cost, fill=GOLD, font=BF(18)); wrap(d, (x, yy + 28), cap, RF(14), INK, pw)
    y = y0 + 26 + ih + 150
    for t in notes: y = wrap(d, (20, y), t, RF(15), INK, Wd - 40) + 12
    if foot: y = wrap(d, (20, y + 4), foot, RF(13), '#5A4A3A', Wd - 40) + 8
    S = S.crop((0, 0, Wd, y + 12)); S.save(out); return out
OUT = []
SRC = 'Built from the staged v6-08 renders (screens-v608, XP Purple) and this folder\'s mocks (mocks_b2b.py); Oct 31, 2026, MDT.'
# --- Pair 1: TG1 (+ D1) ---
def strip(slots, w=390):
    S = Image.new('RGB', (w, 300), '#F6E9C8'); d = ImageDraw.Draw(S); pal = {}
    cols = ['#E8B84A', '#7FB8F5', '#F5A3C7', '#7FD38B', '#B79BFF', '#FFC48A', '#F2B8A0', '#C9CED6', '#E3D06B', '#9AD0C2', '#D7A6E8']
    for r, row in enumerate(slots):
        d.text((8, 10 + r * 56), f'scene {r+1}' if row and row[0] != 'T' else 'cards', fill=INK, font=BF(12))
        for c, s in enumerate(row):
            x, yy = 70 + c * 62, 6 + r * 56
            if s == 'T': d.rounded_rectangle((x, yy, x + 56, yy + 46), 8, fill='#FFFFFF', outline='#10170F', width=2); d.text((x + 8, yy + 15), 'text', fill='#5A4A3A', font=RF(12)); continue
            pal.setdefault(s, cols[len(pal) % len(cols)]); d.rounded_rectangle((x, yy, x + 56, yy + 46), 8, fill=pal[s], outline='#10170F', width=2); d.text((x + 6, yy + 15), s, fill='#10170F', font=BF(12))
    return S
A8 = ['01', '02', '06', '15', '17', '18', '19', '24']; B11 = A8 + ['11', '12', '16']
seqA = [A8[i % 8] for i in range(25)]; seqB = [B11[i % 11] for i in range(25)]
stA = strip([seqA[i*5:i*5+5] for i in range(5)]); stC = strip([A8[0:5], A8[5:8] + A8[0:2]] + [['T'] * 5] * 3)
pA = Image.new('RGB', (390, 844 + 310), BG); pA.paste(im(V + '15-say-it-sight-words.png').crop((0, 0, 390, 844)) if False else im('tg1-now-sw01.png'), (0, 0)); pA.paste(stA, (0, 854))
pB = Image.new('RGB', (390, 844 + 310), BG)
for k, f in enumerate(('tg1-sw16', 'tg1-sw12', 'tg1-sw11')): pB.paste(im(f + '.png', 194).crop((0, 0, 194, 420)), ((k % 2) * 196, (k // 2) * 424))
pB.paste(strip([seqB[i*5:i*5+5] for i in range(5)]), (0, 854))
pC = Image.new('RGB', (390, 844 + 310), BG); pC.paste(im('tg1-now-sw01.png'), (0, 0)); pC.paste(stC, (0, 854))
OUT.append(sheet('TG1-sight-words-repeats.png', 'TG1  Sight Words: 25 scene targets, 8 of its cards have pictures (sw-01, 02, 06, 15, 17, 18, 19, 24)',
    'Which one for Sight Words: A as now, B three more pictures, C fewer scenes, or B and C together?',
    [('A  As now', pA, '0 chars', 'Each of the 8 pictures comes back about 3 times a run (5 scenes x 5 targets).'),
     ('B  3 honest pictures (Instructor)', pB, 'about +9 chars', 'sw-16 "I want it." (reaching for a cake), sw-12 "This is yours." (key handed across the desk), sw-11 "It is mine." (hugging a mug). 11 pictures, each about 2 times a run. Emoji pairs here; drawn art would cost more.'),
     ('C  Fewer scenes (Auditor)', pC, 'about +45 chars', 'One scene per 5 picture cards, at least 2: Sight Words gets 2 scenes, the rest are its text cards. B and C together: 3 scenes, about +54 chars.')],
    ['In every option, his, her, this, where, now, it, there, come, grace and faith stay text-only (no picture).'], foot=SRC + ' Screens in B are cropped to the top half; the full cards match A.'))
# D1 re-shot (Watchman 5a77fd3b; only the XP bar colour changes)
c12 = Image.new('RGB', (390, 844), BG); c12.paste(im('wreshoot/D1-A-cardth.png', 192), (0, 30)); c12.paste(im('wreshoot/D1-B-readfind.png', 192), (198, 30))
dd = ImageDraw.Draw(c12); dd.text((0, 6), 'steps 1-2', fill=INK, font=BF(14)); dd.text((198, 6), 'steps 3-5', fill=INK, font=BF(14))
OUT.append(sheet('D1-sentence-ask-thai-A-B-C-staged.png', 'D1  The Thai line under a sentence ask (86 of the 130 picture cards).',
    'As the PASTE builds it today it is the card\'s full Thai, so she can find the picture from the Thai alone and skip the English. What should the Thai under it say?',
    [('A  As in the PASTE now', 'wreshoot/D1-A-cardth.png', '0 chars', "The Thai under it is ms-21's own Thai, 'where are the keys', so the Thai gives the answer."),
     ("B  Thai says 'read, then find'", 'wreshoot/D1-B-readfind.png', 'about +104 chars', 'New uiText.readFind, Thai only (Instructor drafts, NEEDS NANCY). The full Thai still shows on the reveal.'),
     ("C  B from that zone's step 3 on", c12, 'about +128 chars', 'Steps 1-2 (morning, midday) look like A; steps 3-5 (afternoon to night) like B. A ramp in each zone.')],
    foot="Watchman's D1 (5a77fd3b), re-shot from its own html with the staged XP Purple bar; text and options unchanged. Taps, reveal and grace are the same in all three."))
# --- Pair 2: B1 (+ D2) ---
import b1sim
def timeline(mode, w=600):
    o = b1sim.run(mode); S = Image.new('RGB', (w, 250), '#F6E9C8'); d = ImageDraw.Draw(S); n = 34; cw = (w - 40) / n
    for i, (dd_, z, xp, L, pf, st, ev) in enumerate(o[:n]):
        x = 20 + i * cw; h = min(len(ev), 8) * 14
        d.rectangle((x + 2, 180 - h, x + cw - 3, 180), fill='#E8B84A', outline='#10170F')
        if any('bloodtide' in e for e in ev): d.text((x - 10, 186), 'Bloodtide', fill=RED, font=BF(12)); d.line((x + cw / 2, 180 - h - 4, x + cw / 2, 30), fill=RED, width=3)
        if any('dragonbane' in e for e in ev): d.text((x - 10, 204), 'Dragonbane', fill=RED, font=BF(12)); d.line((x + cw / 2, 180 - h - 4, x + cw / 2, 30), fill=RED, width=3)
        if i % 5 == 0: d.text((x, 222), f'run {i+1}', fill=INK, font=RF(11))
    d.text((20, 6), 'new reward screens per run, one run a day', fill=INK, font=RF(13)); return S
pa = Image.new('RGB', (600, 844 * 600 // 390 // 2 + 260), BG)
for k, mode in enumerate('AB'):
    pass
tA, tB = timeline('A'), timeline('B')
gift = im('name-keep.png', 290)
def b1panel(t):
    P_ = Image.new('RGB', (600, 260 + gift.height + 10), BG); P_.paste(t, (0, 0)); P_.paste(gift, (155, 265)); return P_
OUT.append(sheet('B1-reward-pacing.png', 'B1  Reward pacing: when the two "final" blades arrive (Chancellor sim, staged cards)',
    'When should Bloodtide and Dragonbane arrive: A at her 4th and 5th guardian wins (runs 4 and 6), or B at levels 12 and 16 (runs 13 and 23)?',
    [('A  Guardian milestones (now)', b1panel(tA), '0 chars', 'Both blades in the first week (runs 4 and 6), next to 5-6 other reward screens; their Hint2/Retry2 help switches on early.'),
     ('B  Level 12 and level 16', b1panel(tB), 'about -11 chars', 'Fills two quiet stretches (runs 13 and 23) and keeps the help for later. Side effect: their rank trim goes 4 to 2 unless pinned.')],
    pw=600, foot='Bars: reward screens per run from chancellor/v608sim/sim.py run on the staged cards (one run a day, every card answered right in the end). The card under each chart is the Bloodtide gift card (screen 30\'s card with the blade and name swapped, mock).'))
OUT.append('(D2 below)')
# D2 re-shot
def d2grid(spoken):
    G = Image.new('RGB', (5 * 120 + 40, 3 * 300 + 60), BG); d = ImageDraw.Draw(G)
    for r, (lv, nm) in enumerate(((1, 'step 1 (morning)'), (3, 'step 3 (afternoon)'), (5, 'step 5 (night)'))):
        d.text((0, r * 300 + 4), nm, fill=INK, font=BF(13))
        for t in range(5):
            sp = (t + 1) in spoken[lv]; G.paste(im(f'wreshoot/L{lv}-{"listen" if sp else "written"}.png', 116), (t * 124, r * 300 + 40))
            d.text((t * 124, r * 300 + 22), f'target {t+1}' + (' (spoken)' if sp else ''), fill=INK, font=RF(11))
    return G
OUT[-1] = sheet('D2-listen-ramp-A-B-C-staged.png', "D2  How many of a scene's 5 targets are spoken only (uiText.listenFind), by the zone's time-of-day step. Today it never rises.",
    'How many spoken-only targets as she plays a zone more: A one, B two from step 3, or C a steady ramp?',
    [('A  3rd target spoken only, every run (now)', d2grid({1: {3}, 3: {3}, 5: {3}}), '0 chars', ''),
     ("B  From that zone's step 3: 3rd and 5th spoken", d2grid({1: {3}, 3: {3, 5}, 5: {3, 5}}), '+40 chars', ''),
     ('C  Steps 1-2: 3rd; 3-4: 3rd+5th; 5 (night): 2nd+3rd+5th', d2grid({1: {3}, 3: {3, 5}, 5: {2, 3, 5}}), '+63 chars', '')],
    pw=640, foot="Watchman's D2 (141a0297), re-shot from its own html with the staged XP Purple bar; options and costs unchanged. Same taps, reveal and grace (the speaker replays the word; the hint still shows letters).")
# --- Pair 3: TG2, TG3 ---
mp = im(V + '09-map-later.png'); vp = Image.open(V + '02-main-menu-verse-popup.png').convert('RGB')
crop = vp.crop((int(vp.width * .05), int(vp.height * .20), int(vp.width * .95), int(vp.height * .775))).resize((round(390 * .9), round(844 * .575)))
mpB = ImageEnhance.Brightness(mp).enhance(.6); mpB.paste(crop, (round(390 * .05), round(844 * .20)))
OUT.append(sheet('TG2-verse-after-run.png', 'TG2  A run ends on the Map. If she always stops mid-run, she never reaches the menu, so she never sees the daily verse or gift.',
    'Should the verse pop-up also open over the Map at the end of a run, when she has not seen it today?',
    [('A  Menu only (t404u, now)', V + '09-map-later.png', '0 chars', 'The run ends on the Map; the verse and gift wait on the menu.'),
     ('B  Not seen today: opens over the Map', mpB, 'about +60 chars', 'Same pop-up as the menu one (screen 02), once a day at most.')], foot=SRC + ' B is screen 02\'s pop-up laid over screen 09.'))
OUT.append(sheet('TG3-guardian-recap.png', 'TG3  After a guardian is won, every later run in that zone still ends with the same 10 guardian cards (10 of 35 cards, 29%).',
    'After the win, should the guardian recap run every time (A), or only when she taps the gold Boss! ribbon on the Map (B)?',
    [('A  Recap every run (now)', V + '24-guardian-run-entry.png', '0 chars', 'Every Phonics, Colors, Numbers, Sight Words and Baby run adds the same 10 cards.'),
     ('B  Offered by the gold ribbon', V + '09-map-later.png', 'about +55 chars', 'The run ends after its scenes; the gold Boss! ribbon on the zone row starts the recap when she wants it.')], foot=SRC))
# --- Pair 4: TG4, Bloodtide name, night title ---
OUT.append(sheet('TG4-tier3-buy.png', '',
    'One tap buys and equips (:292). One tap (A), or ask once first (B)?',
    [('A  One tap', V + '39-character-gear-rows.png', '0 chars', '"Get it for 200 ★" buys and equips on the same tap; nothing asks first.'),
     ('B  Ask once (Pantry getFor)', 'tg4-B-confirm.png', 'about +35 chars', 'One more tap on each Star-tier buy; Crystal stays one tap, Oak is free (:292).')], foot=SRC))
OUT.append(sheet('bloodtide-name.png', 'Bloodtide Cleaver: your name for the 4th-guardian blade (t258u). Same tier style as Dragonbane Greatsword and Sunforged Sword.',
    'Bloodtide Cleaver (now), Dawntide Cleaver or Brightwater Cleaver?',
    [('A  Bloodtide Cleaver (now)', 'name-keep.png', '0 chars', 'The name you gave it (t258u).'),
     ('B  Dawntide Cleaver', 'name-alt1.png', '-1 char', 'Same "-tide" shape, morning light.'),
     ('C  Brightwater Cleaver', 'name-alt2.png', '+2 chars', 'Echoes the lake; same two-part style.')], foot=SRC + ' The card is screen 30\'s gift card with the blade and name swapped (mock).'))
OUT.append(sheet('night-title-line.png', 'Night title (level 5 sky): the banner greeting over "Start your day".',
    'At night, should the banner say "Good night!" (A) or "Good evening!" (B)?',
    [('A  Good night! (now)', V + '52-title-night.png', '0 chars', '"Good night!" over the Start your day button.'),
     ('B  Good evening!', 'title-night-B.png', 'about -60 chars', 'Night uses greetEvening; greetNight is dropped.')], foot=SRC))
# --- Coin rule ---
cb = Image.open('coins-before.png').convert('RGB'); ca = Image.open('coins-A.png').convert('RGB'); cB = Image.open('coins-B.png').convert('RGB')
def cpanel(after):
    P_ = Image.new('RGB', (390, 530), BG); d = ImageDraw.Draw(P_)
    d.text((10, 6), 'before the miss', fill=INK, font=RF(13)); P_.paste(cb.crop((170, 660, 610, 940)).resize((370, 235)), (10, 26))
    d.text((10, 270), 'after the miss', fill=INK, font=RF(13)); P_.paste(after.crop((170, 660, 610, 940)).resize((370, 235)), (10, 290)); return P_
coin_quotes = ['Maxwell, Oct 30, 2026 (build-history.md log entry, about 5:40 PM MDT; his own message text is not on file): "Maxwell\'s final calls applied: coins stay full bright (a wrong answer removes one filled coin, no dimming, incl. Baby and Hospital and Sound Duel)"',
               'Maxwell, Oct 31, 2026 (t432u): "Keep in mind Nancy is tough and won\'t get frustrated easily and you won\'t offend me if the game is hard enough to teach well."']
OUT.append(sheet('coin-rule.png', 'Coin meter: what a wrong answer does (the ten coins under her gem count).',
    'A miss costs nothing (A), or a wrong answer removes one filled coin (B)?',
    [('A  A miss costs nothing (now)', cpanel(ca), '0 chars', 'Six filled coins stay six.'),
     ('B  A wrong answer removes one filled coin', cpanel(cB), 'about +80 chars', 'Six filled coins become five; no dimming.')], coin_quotes, foot=SRC + ' Coin close-ups are drawn to the spec (:124) on plain sky.'))
# --- Mocks ---
OUT.append(sheet('letter-game-A-B.png', 'Letter game (t430u), grace-safe: no lives, nothing lost; used letters just go grey.',
    'When she gets a letter right: does the picture grow (A), or uncover tile by tile (B)?',
    [('A  The picture grows', 'letters-A-grows.png', '+413 lean, +523 full (either way)', 'A small cake on the grass grows with each right letter; full size when the word is done.'),
     ('B  The picture is revealed', 'letters-B-tiles.png', '+413 lean, +523 full (either way)', 'A 3x3 cover lifts one tile per right letter; the whole picture shows when the word is done.')], foot=SRC + ' Mock only, not in the build. Thai line is a draft for Instructor.'))
OUT.append(sheet('state-pairs-lean.png', 'State pairs (t428u/t429u), lean version: two of the same object in a scene, the ask names the state.',
    'Is this the right shape for "Can you find the open book?" and the other pairs?',
    [('Lean mock', 'state-pair-open-book.png', '+367 chars', 'One open and one closed book on the grass, beside her; "Can you find the open book?" with the speaker. The lean version adds the rule and the pair list; the full version (more objects, own art) is +885.')],
    foot=SRC + ' Mock only, not in the build. Thai line is a draft for Instructor.'))
print('\n'.join(OUT))
