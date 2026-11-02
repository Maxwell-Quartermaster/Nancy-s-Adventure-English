# Asset depth costs, Maxwell's asks and the ledger (QM, Oct 31, 2026, 7:23 PM MDT)
Measured on the post-HOLD staged PASTE 19321a59 (187,446 chars; **754 banked** under 188,200; Thai reserve 188,200-188,500 untouched). Nothing here is applied or staged.
Unit sizes from the staged cards: one-word card 209 avg (181-275); a drawn SVG = svgNotes entry ~82 + id in picPlan.svg ~11 = ~93; a supplied inline SVG 194-3,718 (front-desk 663, crib 713).

## (a) All-in costs (art included)
| Item | Text (len, exact) | Art | All-in |
|---|---|---|---|
| Mirror on odd zoneRuns (Watchman Idea 1) with the glyph rule | 146: " When `zoneRuns[zone]` is odd, the scene art is mirrored left-right; text, digits, `svg:` pictures, the wall clock, emoji and the hero never flip." | 0 | **+146** |
| Clinic room (Idea 2) | 352 (Watchman's sentence) | props in words 0 / 4 svgNotes ~372 / supplied inline like the mock ~1,391 (my one-piece furniture SVG 1,371 + key) | **352 / ~724 / ~1,743** |
| Market counter (Idea 3; ids now fd-13/17/18/19/21, cv-05/07) | 300 | 0 / ~372 / ~2,000 | **300 / ~672 / ~2,300** |
| Push., Breathe., milk 🥛 (Instructor as first asked) | 3 x 209 = 627 | Push and Breathe need SVG: 2 x 93 | **~813** |
| milk 🥛 + eggs 🥚 (Instructor revised) | 2 x 209 | none | **~418** (joins the tapPrompt group: 44 -> 46) |
| Other "needs svg" items (car seat, burp, Sunday) | 209 each | +93 each | **~302 each** |
| P3 fit-to-width rewording (now staged, D2) | "…scaled as one piece to the screen width, bottom pinned, sky cropped; the HUD, card and 44 pt tap areas stay full size." | 0 | **+98 over the old P3** (P3 total +160) |

## Maxwell's own asks (t428u-t432u), drafted and measured (ledger_r2.py)
| Ask | Lean | Full |
|---|---|---|
| Letter game (t430u) | **413** (spec line 366 + uiText.spellIt 46 + newline; picture grows, 6 plates, grace) | **523** (+ step-3 ramp to 8 plates, letter sounds, Sight Words runs) |
| State pairs (t428u/t429u) | **367** (spec line 254 + uiText.findState 72 + meta.states 40; one pair, book 📖/📕; 📕 is a new emoji) | **885** (6 pairs + state words + 4 drawn second states x 93) |
| Difficulty ramp (t432u) | **40** (D2 B) | **191** (D2 C 63 + D1 C 128) |
| Total | **820** | **1,599** |

## Ledger from the post-HOLD bank (754)
| Step | Cost | Left |
|---|---|---|
| Bank after round 2 + HOLD fixes (P1 +7, P2 +71, P3 +160) | | 754 |
| Maxwell's asks, lean | 820 | **-66** |
| Costliest open picks (coin B 80, TG2 B 60, TG3 B 55, TG1 B+C 54, TG4 B 35, Echo recap 22, Bloodtide +2; B1 and night title can only save) | 308 | -374 |
| Mirror with the glyph rule | 146 | -520 |
| milk + eggs | 418 | -938 |
Combinations that fit 754: letter lean + ramp lean + mirror = 599 (155 left); state lean + ramp lean + all picks = 715 (39 left); letter lean + ramp lean + picks = 761 (7 over). Maxwell's full asks alone are 845 over. The clinic and market do not fit beside any of his asks: v6-09.

## (d) A 4th art file (note only; depends on Maxwell's three-file phone test)
Scene backgrounds are prose, not SVG, so the scene SVG a 4th file could take is small: crib 713 + front-desk 663 = **~1,390** with keys. All supplied art in the PASTE (picPlan.inlineSvg 2,492 + uiInlineSvg 10,189 incl. tex 3,718 and title pointer, + trophyInlineSvg 1,270) is **~13,950**. A pointer line ("load ...-art.json with cards.json") costs about +90, so the net saving is ~1,300 (scene only) to ~13,860 (all supplied art). It adds a 4th paste or upload, which is exactly what the three-file test is checking.

## Round2b ledger (Auditor 48295eae; council update, 7:47 PM MDT)
Staged PASTE 5a52f40c (snap-r2-2010MDT; r2b: 4b744c52), 187,684 chars; 516 banked of 188,200 (Thai reserve 188,200-188,500 untouched).

| Step | Chars | Left |
|---|---|---|
| Post-HOLD bank (PASTE 19321a59) | | 754 |
| Bug fix: sky B, the crop never puts a target under the HUD (scene shrinks to fit) | -79 | 675 |
| Bug fix: targets keep 16 pt from the screen edge | -41 | 634 |
| Bug fix: guardian chip, "; on guardian runs the zone chip shows `boss.name`" (Maxwell t445u (QM-relayed)) | -50 | **584** |
| Letter game lean 413 + listen ramp (D2 B) 40 | -453 | 131 |
| Front desk 390 trim (t444u (QM-relayed)), "; on taller phones a room crops its ceiling to the 320 × 568 framing" | -68 | **63** |
| Costliest open picks (coin B 80, TG2 B 60, TG3 B 55, TG1 B+C 54, TG4 B 35, Echo recap 22, Bloodtide +2) | 308 | **245 short** |

- Scoped trim wording ("the front desk and night table", +93) instead of +68 leaves 38 (270 short of 308).
- Bug fixes 79 + 41 + 50 = 170 come off first; the three steps above are staged in round2.py (P4 +188 incl. the t444u (QM-relayed) +68, P5 +50).

## Trim pick and the two lean asks, side by side (8:01 PM MDT; neutral, no default)
After the bug fixes (B 79 + edge 41 + guardian chip 50, Maxwell t445u (QM-relayed)): 584 left.

| Trim | PASTE | Left | Letter game lean 413 + ramp 40 (453) | State pairs lean 367 + ramp 40 (407) | Costliest open picks (308) |
|---|---|---|---|---|---|
| 1A all rooms, +68 (staged/ 5a52f40c (snap-r2-2010MDT; r2b: 4b744c52)) | 187,684 | 516 | 63 left | 109 left | do not fit either way |
| 1B front desk and night table, +93 (trim-1B/staged/ 46d39ffd (snap-r2-2010MDT; r2b: 2eebff94)) | 187,709 | 491 | 38 left | 84 left | do not fit either way |

## SUPERSEDED: Round totals for every pick round (8:23 PM MDT; Chancellor; neutral, no default)

> SUPERSEDED (Auditor r2b-2051 gate 679dd6d5; marked 9:27 PM MDT): this section used the r2-2010 sizes (bank 584, 1B "front desk and night table" +93, "> 516"). Current numbers: the snap-r2c section at the end.
Bank after the bug fixes: 584. Paths after R1 + R2 lean: 1A + letter game 63, 1A + state pairs 109, 1B + letter game 38, 1B + state pairs 84. Shared table: round_totals.py (the pick sheet footers read the same one).

| Round | Picks | Combined (cheapest to costliest) | Left before | Worst case | Flag |
|---|---|---|---|---|---|
| R0 round2b bug fixes (taken) | sky B 79, 16 pt edges 41, guardian chip 50 (Maxwell t445u, QM-relayed) | 170 | post-HOLD bank 754 | 170 | fits (584 left) |
| R1 ceiling trim (t444u (QM-relayed)) | 1A all rooms +68 or 1B front desk and night table +93 | 68 to 93 | all paths 584 | 93 | fits on every path |
| R2 Maxwell's asks + ramps (t428u-t432u; D1, D2) | letter game lean 413 or state pairs lean 367, each + D2 B ramp 40; full: letter game 523, state pairs 885, ramps D2 C 63 + D1 C 128 | 407 to 1,599 | 1A 516, 1B 491 | 1,599 (one ask full: 1,076) | **OVERRUN**: short by 1,083 (1A), 1,108 (1B) |
| R3 open picks (coin, TG1-TG4, Echo recap, Bloodtide, B1, night title) | coin B 80, TG2 B 60, TG3 B 55, TG1 B+C 54, TG4 B 35, Echo recap 22, Bloodtide +2; B1 B -11 and night title B -60 only save | -71 to 308 | 1A + letter game 63, 1A + state pairs 109, 1B + letter game 38, 1B + state pairs 84 | 308 | **OVERRUN**: short by 245 (1A + letter game), 199 (1A + state pairs), 270 (1B + letter game), 224 (1B + state pairs) |
| R4 extras (Watchman, Instructor) | mirror 146, milk + eggs 418, clinic room 352 / ~724 / ~1,743, market counter 300 / ~672 / ~2,300 | 146 to 4,607 | 1A + letter game 63, 1A + state pairs 109, 1B + letter game 38, 1B + state pairs 84 | 4,607 | **OVERRUN**: short by 4,544 (1A + letter game), 4,498 (1A + state pairs), 4,569 (1B + letter game), 4,523 (1B + state pairs); even the cheapest overruns |

Whole-round worst case (every round at its costliest, 1B): 6,607 chars against 584: **OVERRUN by 6,023**.
R2 lean only fits: letter game lean + ramp 453 or state pairs lean + ramp 407, not both (413 + 367 + 40 = 820 > 516). R3 fits only at the cheap end: the 0-char A options, or B1 B / night title B, which save chars.

## SUPERSEDED: snap-r2b sizes (Auditor eb2674be, Council 8:43 PM MDT; 8:51 PM MDT; neutral, no default)

> SUPERSEDED by the snap-r2c section at the end (1A +89 with ", never over a target"; verse scroll is a fix; verse option B is out).
PASTE 1A 187,776 (md5 4b744c529fba24626630ffc24116e41c), 1B 187,797 (md5 2eebff944f7c30ac2e13fdc8e888d398); verses unchanged (81295c9f). 1748 base 187,208.

| Step | Chars | 1A left | 1B left |
|---|---|---|---|
| Post-HOLD bank | | 754 | 754 |
| Bug fix: sky B | -79 | 675 | 675 |
| Bug fix: 16 pt edges | -41 | 634 | 634 |
| Bug fix: guardian chip (Maxwell t445u, QM-relayed) | -50 | 584 | 584 |
| Bug fix: walk scene shrinks below the banner (eb2674be H2) | -38 | 546 | 546 |
| Bug fix: sw-19 three (eb2674be H1) | -2 | 544 | 544 |
| Trim (Maxwell t444u, QM-relayed): 1A all rooms / 1B front desk and kitchen | -68 / -89 | 476 | 455 |
| Verse at 320, A scroll in its card (staged in both) | -52 | 424 | 403 |

Every combination, chars left after the lean ask + ramp 40 (fits / over by N):

| Trim | Verse | Letter game 413 + 40 | State pairs 367 + 40 |
|---|---|---|---|
| 1A | A (scroll in its card, all 30 verses kept, +52) | over by 29 | fits (17 left) |
| 1A | B (swap the long verses for shorter ones, 0 chars, some peace verses replaced, needs a new Thai check and Nancy's sign-off) | fits (23 left) | fits (69 left) |
| 1B | A (scroll in its card, all 30 verses kept, +52) | over by 50 | over by 4 |
| 1B | B (swap the long verses for shorter ones, 0 chars, some peace verses replaced, needs a new Thai check and Nancy's sign-off) | fits (2 left) | fits (48 left) |

Only one lean ask fits beside the ramp: 820 vs 424 (1A) / 403 (1B) with the verse scroll staged (476 / 455 without it); with the scroll, letter game + ramp (453) fits neither trim and state pairs + ramp (407) fits 1A only.
R3 open picks B1 B (-11) and night title B (-60) would free up to 71 more chars on any row; the costliest open picks (308) fit on no row.

| Round | Picks | Combined | Left before | Worst case | Flag |
|---|---|---|---|---|---|
| R0 bug fixes (taken) | sky B 79, 16 pt edges 41, guardian chip (Maxwell t445u, QM-relayed) 50, walk scene shrinks below the banner (eb2674be H2) 38, sw-19 three (eb2674be H1) 2 | 210 to 210 | post-HOLD bank 754 | 210 | fits |
| R1 ceiling trim (Maxwell t444u, QM-relayed) | 1A all rooms +68 or 1B front desk and kitchen +89 | 68 to 89 | bank 544 | 89 | fits |
| RV long verse at 320 | A scroll in its card +52 or B shorter verses 0 | 0 to 52 | 1A 476, 1B 455 | 52 | fits |
| R2 Maxwell's asks + ramp (t428u-t432u, QM-relayed) | letter game lean 413 or state pairs lean 367, each + D2 B ramp 40; full: letter game 523, state pairs 885, ramps D2 C 63 + D1 C 128 | 407 to 1,599 | 1A/A 424, 1A/B 476, 1B/A 403, 1B/B 455 | 1,599 | **OVERRUN** by 1,175 (1A/A), 1,123 (1A/B), 1,196 (1B/A), 1,144 (1B/B) |
| R3 open picks (coin, TG1-TG4, Echo recap, Bloodtide, B1, night title) | coin B 80, TG2 B 60, TG3 B 55, TG1 B+C 54, TG4 B 35, Echo recap 22, Bloodtide +2; B1 B -11 and night title B -60 only save | -71 to 308 | most left after R2 69 | 308 | **OVERRUN** by 239 (most left after R2) |
| R4 extras (Watchman, Instructor) | mirror 146, milk + eggs 418, clinic room 352 / ~724 / ~1,743, market counter 300 / ~672 / ~2,300 | 146 to 4,607 | most left after R2 69 | 4,607 | **OVERRUN** by 4,538 (most left after R2) |

Note: the 8:23 PM MDT round-totals table above used the r2-2010 sizes (bank 584, trim 1B +93); this section supersedes it.

## SUPERSEDED: Working copy after snap-r2b-2051MDT (follow-up 9:05 PM MDT, QM-relayed; staged, not frozen; written 9:17 PM MDT)

> SUPERSEDED by the snap-r2c section below (verse option B removed: it breaks the verse guard; the scroll is a fix).

1A trim wording gains ", never over a target" (+21): 1A is now +89 like 1B, so both trims bank the same. Supersedes the 1A +68 / 424 rows above.

| PASTE | md5 | chars | banked |
|---|---|---|---|
| 1A | 106a066103da9713220a5e7d6c4285cf | 187,797 | 403 |
| 1B | 2eebff944f7c30ac2e13fdc8e888d398 | 187,797 | 403 |

| Step | Chars | 1A left | 1B left |
|---|---|---|---|
| Bank after the bug fixes | | 544 | 544 |
| Trim: 1A all rooms, never over a target / 1B front desk and kitchen | -89 / -89 | 455 | 455 |
| Verse at 320, A scroll in its card (staged in both) | -52 | 403 | 403 |

Combinations Maxwell could choose (same under 1A and 1B; no default):

| Verse | Ask (lean) | Other picks | Banked | Result |
|---|---|---|---|---|
| A scroll (+52) | letter game 413 | as listed | 403 | over by 50 |
| A scroll (+52) | letter game 413 | night title B (-60) | 403 | fits (10 left) |
| A scroll (+52) | letter game 413 | night title B + B1 B (-71) | 403 | fits (21 left) |
| A scroll (+52) | letter game 413 | drop the ramp (-40) | 403 | over by 10 |
| A scroll (+52) | state pairs 367 | as listed | 403 | over by 4 |
| A scroll (+52) | state pairs 367 | night title B (-60) | 403 | fits (56 left) |
| A scroll (+52) | state pairs 367 | night title B + B1 B (-71) | 403 | fits (67 left) |
| A scroll (+52) | state pairs 367 | drop the ramp (-40) | 403 | fits (36 left) |
| B shorter verses (-52) | letter game 413 | as listed | 455 | fits (2 left) |
| B shorter verses (-52) | letter game 413 | night title B (-60) | 455 | fits (62 left) |
| B shorter verses (-52) | letter game 413 | night title B + B1 B (-71) | 455 | fits (73 left) |
| B shorter verses (-52) | letter game 413 | drop the ramp (-40) | 455 | fits (42 left) |
| B shorter verses (-52) | state pairs 367 | as listed | 455 | fits (48 left) |
| B shorter verses (-52) | state pairs 367 | night title B (-60) | 455 | fits (108 left) |
| B shorter verses (-52) | state pairs 367 | night title B + B1 B (-71) | 455 | fits (119 left) |
| B shorter verses (-52) | state pairs 367 | drop the ramp (-40) | 455 | fits (88 left) |

Trim costs 89 on both paths, so 1A and 1B both bank 403 with the verse scroll (455 with shorter verses). As listed, state pairs + ramp (407) is over by 4 and letter game + ramp (453) is over by 50; the combined pick sheet lists the combinations that fit.

| Round | Line |
|---|---|
| R0 | Round total (R0 bug fixes (taken)): picks combined 210 chars against post-HOLD bank 754 left. Worst case 210: fits on every path. |
| R1 | Round total (R1 ceiling trim (Maxwell t444u, QM-relayed)): picks combined 89 chars against bank 544 left. Worst case 89: fits on every path. |
| RV | Round total (RV long verse at 320): picks combined 0 to 52 chars against 1A 455, 1B 455 left. Worst case 52: fits on every path. |
| R2 | Round total (R2 Maxwell's asks + ramp (t428u-t432u, QM-relayed)): picks combined 407 to 1,599 chars against 1A/A 403, 1A/B 455, 1B/A 403, 1B/B 455 left. Worst case 1,599 (both asks full; one ask full at most 1,076): OVERRUN, short by 1,196 (1A/A), 1,144 (1A/B), 1,196 (1B/A), 1,144 (1B/B). |
| R3 | Round total (R3 open picks (coin, TG1-TG4, Echo recap, Bloodtide, B1, night title)): picks combined -71 to 308 chars against most left after R2 48 left. Worst case 308: OVERRUN, short by 260 (most left after R2). |
| R4 | Round total (R4 extras (Watchman, Instructor)): picks combined 146 to 4,607 chars against most left after R2 48 left. Worst case 4,607: OVERRUN, short by 4,559 (most left after R2). Even the cheapest pick (146) overruns every path. |

## snap-r2c (Auditor r2b-2051 gate 679dd6d5, Instructor 42ecfd0a, council 9:19 PM MDT, QM-relayed; written 9:27 PM MDT)

1A :227 gains ", never over a target" (+21), so 1A and 1B both cost 89. The verse scroll (+52) is a bug fix, not a pick; verse option B is out (it breaks the verse guard). No default.

| PASTE | md5 | chars | banked |
|---|---|---|---|
| 1A | 106a066103da9713220a5e7d6c4285cf | 187,797 | 403 |
| 1B | 2eebff944f7c30ac2e13fdc8e888d398 | 187,797 | 403 |

| Step | Chars | Left |
|---|---|---|
| Post-HOLD bank | | 754 |
| Bug fix: sky B | -79 | 675 |
| Bug fix: 16 pt edges | -41 | 634 |
| Bug fix: guardian chip (Maxwell t445u, QM-relayed) | -50 | 584 |
| Bug fix: walk scene shrinks below the banner (eb2674be H2) | -38 | 546 |
| Bug fix: sw-19 three (eb2674be H1) | -2 | 544 |
| Bug fix: long verses scroll in their card (eb2674be H4; council 9:19 PM MDT, QM-relayed: a fix, not a pick) | -52 | 492 |
| Trim: 1A all rooms, never over a target / 1B front desk and kitchen | -89 / -89 | 403 / 403 |

| Trim | Ask (lean) + ramp 40 | Result |
|---|---|---|
| 1A | letter game 413 + 40 | over by 50 |
| 1A | state pairs 367 + 40 | over by 4 |
| 1B | letter game 413 + 40 | over by 50 |
| 1B | state pairs 367 + 40 | over by 4 |

Savings Maxwell could choose himself (same under 1A and 1B):

| Ask (lean) | Saving | Result |
|---|---|---|
| letter game 413 | night title B | fits (10 left) |
| letter game 413 | B1 B | over by 39 |
| letter game 413 | night title B + B1 B | fits (21 left) |
| letter game 413 | drop the ramp | over by 10 |
| state pairs 367 | night title B | fits (56 left) |
| state pairs 367 | B1 B | fits (7 left) |
| state pairs 367 | night title B + B1 B | fits (67 left) |
| state pairs 367 | drop the ramp | fits (36 left) |

Trim costs 89 on both paths, so 1A and 1B both bank 403 (the verse scroll is a fix, already counted). State pairs + ramp (407) is over by 4; letter game + ramp (453) is over by 50. Savings Maxwell could choose: night title B -60, B1 B -11, dropping the ramp -40.

| Round | Line |
|---|---|
| R0 | Round total (R0 bug fixes (taken)): picks combined 262 chars against post-HOLD bank 754 left. Worst case 262: fits on every path. |
| R1 | Round total (R1 ceiling trim (Maxwell t444u, QM-relayed)): picks combined 89 chars against bank 492 left. Worst case 89: fits on every path. |
| R2 | Round total (R2 Maxwell's asks + ramp (t428u-t432u, QM-relayed)): picks combined 407 to 1,599 chars against 1A 403, 1B 403 left. Worst case 1,599 (both asks full; one ask full at most 1,076): OVERRUN, short by 1,196 (1A), 1,196 (1B). Even the cheapest pick (407) overruns every path. |
| R3 | Round total (R3 open picks (coin, TG1-TG4, Echo recap, Bloodtide, B1, night title)): picks combined -71 to 308 chars against most left after R2 -4 left. Worst case 308: OVERRUN, short by 312 (most left after R2). |
| R4 | Round total (R4 extras (Watchman, Instructor)): picks combined 146 to 4,607 chars against most left after R2 -4 left. Worst case 4,607: OVERRUN, short by 4,611 (most left after R2). Even the cheapest pick (146) overruns every path. |
