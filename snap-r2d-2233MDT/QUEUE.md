# v6-08 decision queue for Maxwell (regenerated 10:33 PM MDT, Oct 31, 2026, from snap-r2d-2233MDT; neutral: every option shows its cost, none is the default)

Build: candidate snap-1748MDT (PASTE 95a4d0fc). Round 2 staged in snap-r2d-2233MDT: PASTE 1A 106a0661 / 1B 2eebff94, both 187,797 chars, 403 banked. Verses unchanged (81295c9f).
Provenance: t440u, t441u, t444u, t445u, t446u and the 7:53 / 8:08 PM MDT relays are QM-relayed and unverified.

## Decided
- eyes = A (t422u). Screen 12 = C, A elsewhere (t423u).
- walk 24 = B with changes (t441u, QM-relayed); staged in round 2.
- one ask phrasing 'Can you find the {word}?' / 'หา {word} เจอไหม' (t440u, QM-relayed; Thai NEEDS NANCY); staged in round 2.
- Fixed, not picks: sky B crop floor, 16 pt edges, Guardian name on the chip line, walk scene shrinks below the banner, sw-19 three, long verses scroll in their card (+52).

## Open now (round 2 picks; costs from round_totals.py)
- round2/sheets/pick-combined-trim-ask-verse.png (7440f94a): Which trim (1A all rooms, never over a target +89 / 1B front desk and kitchen +89) and which ask (letter game 413 / state pairs 367, each + ramp 40)? Trim costs 89 on both paths, so 1A and 1B both bank 403 (the verse scroll is a fix, already counted). State pairs + ramp (407) is over by 4; letter game + ramp (453) is over by 50. Savings Maxwell could choose: night title B -60, B1 B -11, dropping the ramp -40.
- round2/r2d/sheets/jesus-words-26-320-A-B-C-D.png (333ef49e): Screen 26 (Words of Jesus hint; each covers its part only until tapped or 6 s, :220): A (bubble above the card covers Sam, 0, 403 left), B (bubble under the banner, scrolls, covers 🤔, +36, 367 left), C' (chip 'Words of Jesus' + its Thai from uiText.jesusWords; the opened verse covers the heroes' heads; +82, 321 left; a new chip entry with new Thai would be +142, 261 left, NEEDS NANCY) or D (bubble under the banner beside 🤔, above Sam's head, covers scenery only, Thai scrolls; +36, 367 left; two full Thai lines do not fit above Sam at 320 or 375 x 667)? Every R2 combination that fits is on the sheet (r2_fit_table.py, matches Chancellor f6fdf5c7).
- round2/sheets/trim-pick-1A-vs-1B-390.png (2aa8e7c4): Context for the trim: 1A or 1B, both +89, 403 left.
- round2/sheets/home-lake-trim-before-after-390.png (90c4c920): Context strip: the home-lake rooms before and after the trim (17-19 keep their ceiling under 1A).
- round2/sheets/front-desk-t444u-320-vs-390.png (56e60380): Context: the front desk at 320 and 390 (3A or 3B look).
- decisions/b2b/letter-game-A-B.png (c6089384): Letter game: picture grows, or picture revealed tile by tile? (lean +413, full +523)
- decisions/b2b/state-pairs-lean.png (f2ec52d3): State pairs: is this the right shape for "Can you find the open book?"? (lean +367, full +885)

## Open picks (decisions/b2b, sent in pairs)
- decisions/b2b/TG1-sight-words-repeats.png (a469bfb4): A 0, B 3 honest pictures about +9, C fewer scenes about +45, B+C about +54.
- decisions/b2b/D1-sentence-ask-thai-A-B-C-staged.png (9d3e0b71): A 0, B +104, C +128.
- decisions/b2b/B1-reward-pacing.png (6b737d08): A 0, B about -11.
- decisions/b2b/D2-listen-ramp-A-B-C-staged.png (bf5a0220): A 0, B +40, C +63.
- decisions/b2b/TG2-verse-after-run.png (2d503ebb): A 0, B about +60.
- decisions/b2b/TG3-guardian-recap.png (1317998d): A 0, B about +55.
- decisions/b2b/TG4-tier3-buy.png (d7c9f70d): One tap (A, 0), or ask once first (B, about +35)?
- decisions/b2b/bloodtide-name.png (7eee863f): Bloodtide Cleaver (now, 0), Dawntide Cleaver (-1) or Brightwater Cleaver (+2)? Waiting on Maxwell (t258u, his own name).
- decisions/b2b/night-title-line.png (3709c41b): A 0, B about -60.
- decisions/b2b/coin-rule.png (1361e3e3): A a miss costs nothing (0), B a wrong answer removes one filled coin (about +80).

## Other open questions
- /workspace/watchman/playtest-v608/decision/daily-gem-A-B.png (501e982f): Which gem tag, A or B? (Watchman)
- scenes/tod/strip-meadow-steps-390.png (47492118): Does the sky follow her runs the way you want (K3: 1 + zoneRuns mod 5)?
- decisions/m2-sound-duel-speaker-A-B-390-v608.png (bfd8e4f1): Which speaker spot for Sound Duel at 390: A or B?
- decisions/emoji-17-18-19-390.png (c4f767f6): Do 17, 18 and 19 look consistent with hand emoji on the plates?
- b1/v537-wash-the-baby-before-after.png: Fix this in CURRENT too, or leave v5-37 as is until v6-08 ships?

## To see before the phone test (no question)
- Showcase tour: round2/showcase/showcase-1-opening.png (8dcce473), round2/showcase/showcase-2-zones.png (923bacf2), round2/showcase/showcase-3-asking.png (f4a8453e), round2/showcase/showcase-4-walk-guardian.png (dc0939b8), round2/showcase/showcase-5-rewards-pause.png (f1a2e8d0)
- Screens 24-28 at 320 x 568 and 375 (screens-v608/png/2[4-8]-guardian-*-{320x568,375x667,375x812}.png; Auditor asked that Maxwell see the 320 renders).

## Set aside (not sent)
- round2/sheets/aside-not-sent/: sky A-vs-B (decided: B is a fix), the clinic idea. Verse option B (shorter verses) is out: it breaks the verse guard (Instructor 42ecfd0a).
- Dropped: M1 refund pick (t435u). The old front-desk 98926d6b / trim-pick 91dd33bb ("night table", +93) and "Find the open book." sheets are replaced by the files above.
