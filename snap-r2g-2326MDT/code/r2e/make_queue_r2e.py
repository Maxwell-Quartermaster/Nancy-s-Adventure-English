# r2e (11:00 PM MDT brief + steering): copy of make_queue_r2d.py with the r2e lines (C' head note, timing, under-20 note, Thai reserve). Was: r2d (10:07 PM MDT): 26 line now A-D from the staged r2d sheet, 26-B worded 'scroll covers 🤔'. Regenerates v608build/polish-r1/QUEUE.md from the files as they are now (Auditor r2b-2051 gate: QUEUE was a stale 8:01 PM list).
# Usage: python3 make_queue.py <snapshot name> <written time>
import sys, os, hashlib
sys.path.insert(0, '/workspace/v608build/round2/asset-depth'); import round_totals as RT
SNAP, NOW = sys.argv[1], sys.argv[2]; B = '/workspace/v608build/'
def m(p):
    f = p if p.startswith('/') else B + p
    return hashlib.md5(open(f, 'rb').read()).hexdigest()[:8] if os.path.exists(f) else 'MISSING'
def it(p, q): return f'- {p} ({m(p)}): {q}'
P1A, P1B = m('round2/staged/nancys-adventure-english-v6-08-PASTE.md'), m('round2/trim-1B/staged/nancys-adventure-english-v6-08-PASTE.md')
L = [f"# v6-08 decision queue for Maxwell (regenerated {NOW}, Oct 31, 2026, from {SNAP}; neutral: every option shows its cost, none is the default)", '',
 f"Build: candidate snap-1748MDT (PASTE 95a4d0fc). Round 2 staged in {SNAP}: PASTE 1A {P1A} / 1B {P1B}, both 187,797 chars, {RT.STAGED['1A']} banked. Verses unchanged (81295c9f).",
 'Provenance: t440u, t441u, t444u, t445u, t446u and the 7:53 / 8:08 PM MDT relays are QM-relayed and unverified.', '',
 '## Decided',
 '- eyes = A (t422u). Screen 12 = C, A elsewhere (t423u).',
 "- walk 24 = B with changes (t441u, QM-relayed); staged in round 2.",
 "- one ask phrasing 'Can you find the {word}?' / 'หา {word} เจอไหม' (t440u, QM-relayed; Thai NEEDS NANCY); staged in round 2.",
 '- Fixed, not picks: sky B crop floor, 16 pt edges, Guardian name on the chip line, walk scene shrinks below the banner, sw-19 three, long verses scroll in their card (+52).', '',
 '## Open now (round 2 picks; costs from round_totals.py)',
 it('round2/sheets/pick-combined-trim-ask-verse.png', f"Which trim (1A all rooms, never over a target +{RT.TRIM['1A']} / 1B front desk and kitchen +{RT.TRIM['1B']}) and which ask (letter game {RT.ASK['letter game']} / state pairs {RT.ASK['state pairs']}, each + ramp 40)? " + RT.BUDGET),
 it('round2/r2d/sheets/jesus-words-26-320-A-B-C-D.png', "Screen 26 (Words of Jesus hint; each covers its part only until tapped or 6 s, :220): A (bubble above the card covers Sam, 0, 403 left), B (bubble under the banner, scrolls, covers 🤔, +36, 367 left), C' (chip 'Words of Jesus' + its Thai from uiText.jesusWords; the opened verse covers the heroes' heads and 🤔, the only option besides A that covers a head; +82, 321 left; a new chip entry with new Thai would be +142, 261 left, NEEDS NANCY) or D (bubble under the banner beside 🤔, above Sam's head, covers scenery only, Thai scrolls; +36, 367 left; two full Thai lines do not fit above Sam at 320 or 375 x 667)? Every R2 combination that fits is on the sheet (r2_fit_table.py, matches Chancellor f6fdf5c7)."),
 it('round2/sheets/trim-pick-1A-vs-1B-390.png', 'Context for the trim: 1A or 1B, both +89, 403 left.'),
 it('round2/sheets/home-lake-trim-before-after-390.png', 'Context strip: the home-lake rooms before and after the trim (17-19 keep their ceiling under 1A).'),
 it('round2/sheets/front-desk-t444u-320-vs-390.png', 'Context: the front desk at 320 and 390 (3A or 3B look).'),
 it('decisions/b2b/letter-game-A-B.png', 'Letter game: picture grows, or picture revealed tile by tile? (lean +413, full +523)'),
 it('decisions/b2b/state-pairs-lean.png', 'State pairs: is this the right shape for "Can you find the open book?"? (lean +367, full +885)'), '',
 "- Timing: Maxwell's R2 pick and screen 26 pick need to land by Nov 2 (freeze Nov 4, 11:59 PM). If they slip past Nov 3, there is no R2 ask in this paste and v6-09 picks it up. Writing and Thai-checking time (Instructor): state pairs about 1 hour, letter game about 2 hours.",
 "- chars left = room for later changes, English or new Thai; Nancy's Nov 7 Thai sign-off fixes use the separate 300-char reserve (188,200 to 188,500).", '',
 '## Open picks (decisions/b2b, sent in pairs)',
 it('decisions/b2b/TG1-sight-words-repeats.png', 'A 0, B 3 honest pictures about +9, C fewer scenes about +45, B+C about +54.'),
 it('decisions/b2b/D1-sentence-ask-thai-A-B-C-staged.png', 'A 0, B +104, C +128.'),
 it('decisions/b2b/B1-reward-pacing.png', 'A 0, B about -11.'),
 it('decisions/b2b/D2-listen-ramp-A-B-C-staged.png', 'A 0, B +40, C +63.'),
 it('decisions/b2b/TG2-verse-after-run.png', 'A 0, B about +60.'),
 it('decisions/b2b/TG3-guardian-recap.png', 'A 0, B about +55.'),
 it('decisions/b2b/TG4-tier3-buy.png', 'One tap (A, 0), or ask once first (B, about +35)?'),
 it('decisions/b2b/bloodtide-name.png', 'Bloodtide Cleaver (now, 0), Dawntide Cleaver (-1) or Brightwater Cleaver (+2)? Waiting on Maxwell (t258u, his own name).'),
 it('decisions/b2b/night-title-line.png', 'A 0, B about -60.'),
 it('decisions/b2b/coin-rule.png', 'A a miss costs nothing (0), B a wrong answer removes one filled coin (about +80).'), '',
 '## Other open questions',
 it('/workspace/watchman/playtest-v608/decision/daily-gem-A-B.png', 'Which gem tag, A or B? (Watchman)'),
 it('scenes/tod/strip-meadow-steps-390.png', 'Does the sky follow her runs the way you want (K3: 1 + zoneRuns mod 5)?'),
 it('decisions/m2-sound-duel-speaker-A-B-390-v608.png', 'Which speaker spot for Sound Duel at 390: A or B?'),
 it('decisions/emoji-17-18-19-390.png', 'Do 17, 18 and 19 look consistent with hand emoji on the plates?'),
 '- b1/v537-wash-the-baby-before-after.png: Fix this in CURRENT too, or leave v5-37 as is until v6-08 ships?', '',
 '## To see before the phone test (no question)',
 '- Showcase tour: ' + ', '.join(f'round2/showcase/showcase-{k}.png ({m(f"round2/showcase/showcase-{k}.png")})' for k in ('1-opening', '2-zones', '3-asking', '4-walk-guardian', '5-rewards-pause')),
 '- Screens 24-28 at 320 x 568 and 375 (screens-v608/png/2[4-8]-guardian-*-{320x568,375x667,375x812}.png; Auditor asked that Maxwell see the 320 renders).', '',
 '## Queued for v6-09 (not this paste; 0 PASTE chars)',
 "- Code/comment fix: screens/play_v608.py tplate() draws the plate at sz=104 pt, but its comment says 'framed 124 pt plate' (PASTE :246 says 124 pt). Make the two agree in v6-09 (decide which number is meant); no render or PASTE change now.",
 "- Latent risk, not a hold: in the B-meadow listen scene the moved-down kite (design 296-368 x 306-378) would sit under the top-right reveal plate spot (:246, design 262-366 x 234-338, 32 pt overlap) if that plate were ever drawn on a zone scene. Today no zone scene draws it.", '',
 '## Set aside (not sent)',
 '- round2/sheets/aside-not-sent/: sky A-vs-B (decided: B is a fix), the clinic idea. Verse option B (shorter verses) is out: it breaks the verse guard (Instructor 42ecfd0a).',
 '- Dropped: M1 refund pick (t435u). The old front-desk 98926d6b / trim-pick 91dd33bb ("night table", +93) and "Find the open book." sheets are replaced by the files above.']
open(B + 'polish-r1/QUEUE.md', 'w').write('\n'.join(L) + '\n'); print('QUEUE written', m('polish-r1/QUEUE.md'))
