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
Staged PASTE bfb0392b, 187,684 chars; 516 banked of 188,200 (Thai reserve 188,200-188,500 untouched).

| Step | Chars | Left |
|---|---|---|
| Post-HOLD bank (PASTE 19321a59) | | 754 |
| Bug fix: sky B, the crop never puts a target under the HUD (scene shrinks to fit) | -79 | 675 |
| Bug fix: targets keep 16 pt from the screen edge | -41 | 634 |
| Bug fix: guardian chip, "; on guardian runs the zone chip shows `boss.name`" (Maxwell t445u (QM-relayed)) | -50 | **584** |
| Letter game lean 413 + listen ramp (D2 B) 40 | -453 | 131 |
| Front desk 390 trim (t444u), "; on taller phones a room crops its ceiling to the 320 × 568 framing" | -68 | **63** |
| Costliest open picks (coin B 80, TG2 B 60, TG3 B 55, TG1 B+C 54, TG4 B 35, Echo recap 22, Bloodtide +2) | 308 | **245 short** |

- Scoped trim wording ("the front desk and night table", +93) instead of +68 leaves 38 (270 short of 308).
- Bug fixes 79 + 41 + 50 = 170 come off first; the three steps above are staged in round2.py (P4 +188 incl. the t444u +68, P5 +50).

## Trim pick and the two lean asks, side by side (8:01 PM MDT; neutral, no default)
After the bug fixes (B 79 + edge 41 + guardian chip 50, Maxwell t445u (QM-relayed)): 584 left.

| Trim | PASTE | Left | Letter game lean 413 + ramp 40 (453) | State pairs lean 367 + ramp 40 (407) | Costliest open picks (308) |
|---|---|---|---|---|---|
| 1A all rooms, +68 (staged/ bfb0392b) | 187,684 | 516 | 63 left | 109 left | do not fit either way |
| 1B front desk and night table, +93 (trim-1B/staged/ 797b941b) | 187,709 | 491 | 38 left | 84 left | do not fit either way |
