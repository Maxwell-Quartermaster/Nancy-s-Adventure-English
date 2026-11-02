# v6-08 build (Quartermaster). Times in MDT. v6-07 is frozen at the Auditor gate; nothing here touches v6-07 files.
## Running total (PASTE chars, ceiling 188,200; 188,200-188,500 is the Thai reserve, never used). Rows = qm_v608.py --dry, 4:04 PM MDT.
| step | delta | PASTE |
|---|---|---|
| v6-07 base | | 181,850 |
| B1 ask-card rule (Auditor + Instructor `pic` not null) | +175 | |
| A2 ask-card Thai wraps | +37 | |
| VP1-VP10 verse pop-up B + daily gift, O1 folded into VP3 (spec) | +1,063 | |
| H1 hand emoji rule :243 + svg note (spec) | +68 | |
| E1 happy eyes: #rE = Nancy's exact arcs (cards) | -133 | |
| H1 ms-31 choices 🙏/🙌 (cards) | -25 | |
| VP uiText.dailyGift (Thai อัญมณีประจำวัน: 1 เม็ด) + uiTextEntries (cards) | +70 | 183,105 (snap-1554MDT) |
| P1 reveal pictures C/A (t423u, spec :243) | +169 | |
| SC scenes in 7.1: time by level, pond, front desk, kitchen table, listen, count, big or small (spec) | +1,858 | |
| G picture pairs, section 12 + check 3 (spec) | +72 | |
| VP10/SC uiText count 93 -> 97 | 0 | |
| G1 tunic-rose meaning (cards) | -2 | |
| SC 4 uiText keys + meta.sizeSort + 6 pair pics (cards) | +409 | |
| = v6-08 now | +3,761 | 185,611 (banked 2,589) |
**Ledger fix (council 3:55 PM MDT):** the old row "182,944" was measured at 3:44 PM before three later edits: B1 replaced the A1 sketch (+175 vs +42 = +133), O1 added to VP3 (+34), dailyGift Thai shortened (-6). 133 + 34 - 6 = +161 = 183,105 - 182,944. The old table also left out the H1 spec rows (+68) and showed E1 at -172 (before the shared #rE, now -133), so its rows did not add up to its own +1,094.
**Patches:** (4:04 PM MDT none existed.) Applied in order through fixes_v608/qm_v608 to PASTE, FINAL and spec: 1. watchman-state-hero.py (8e75b04d, +6) folded into K1; 2. watchman-weapon-slot-ids.py (e08b0fbd, +66) reconciled with Auditor K2 into one scheme `<type>-t<t>`; 3. auditor-u1-uitext-count.py (863deae1, 0: 91 -> 97).
Title file: 19,136 -> 19,057 (-79; Sam's profile eye is one of Nancy's arcs).
## Log
- 3:28 PM MDT: started v6-08 (Maxwell's "Go").
- 3:39 PM MDT: E1 happy eyes, A1/A2, VP verse pop-up B in qm_v608; checks_v608 on v6-08: 309 True / 0 live False / 67 SUPERSEDED.
- 3:40 PM MDT: t408u: Sam's eyes = Nancy's exact eyes (path, 1.6, Ink) via shared #rE; Nancy's own snippet unchanged.
- 3:44 PM MDT: H1 (t406u hand emoji on plates) in qm_v608; eyes re-shot on 42 screens (38 app + 4 scene-variety); checks_v608: 303 True / 0 live False / 75 SUPERSEDED. Reported eyes to the parent.
## Eyes deliverables
- eyes/pairs/eyes-*.png (25 before/after crops), eyes/contact-eyes-v608.png, eyes/contact-all-sam-after-v608.png
- screens-v608/{html,png} (app screens), eyes/scene-variety/{html,png} (mock screens), eyes/eyes-manifest.json

## Oct 31, 2026, 3:54 PM MDT: t411u + gate HOLD items + Instructor Thai (snapshot snap-1554MDT, read-only)
- Eye-weight sheet: eyes/eye-weight-A-B.png (1055ab92). A = Nancy's exact arcs (current), B = stroke 2.2 Ink arc. Render-only.
- B1 (+175 incl. Instructor "and `pic` is not null"): 7.1 rule text at PASTE/FINAL :226, spec :217. Live check walks every card: 44 get "Where is the ...?", 0 bad outputs.
- O1: folded into VP3 (spec "over the main menu (never the title, t404u)"); old render 02 moved to screens-v608/superseded-O1/.
- dailyGift Thai = อัญมณีประจำวัน: 1 เม็ด (Instructor 7057dde4, NEEDS NANCY).
- m1: 24/25 plate gap 10 px at 390. m2: decisions/m2-sound-duel-speaker-A-B-390-relabel.png. m3: .get() on tapPrompt/playAgain (P2 mutation now fails cleanly, rc 0). n1: W path. n2: 4 SUPERSEDED reasons refreshed.
- v5-37 flaw pair: b1/v537-wash-the-baby-before-after.png. CURRENT untouched (b653ffb2).
- t411u: screen 10 v6-06 rhythm; 320 m1 revert (104 px plates, 140 px button) + 44 pt speaker in its own slot; 46 Backup readable, labels inside at 390/320. Pairs in polish-r1/t411u/.
- Emoji: decisions/emoji12-now-A-B-C-390.png, decisions/emoji-17-18-19-390.png (harness 17-19 now hand emoji on plates, H1).
- Verse pop-up renders: screens-v608/png/02-*, 02b-*, 03-* (390check/320x568); sheet verse-popup/verse-popup-menu-before-after.png.
- Decision queue: polish-r1/QUEUE.md. PASTE 183,105 (+1,255 vs v6-07), banked 5,095. Checks v6-08 308 True / 0 False.
- Not started: scene E, A-H, level 1-5 time-of-day strip.

## Oct 31, 2026, 4:04 PM MDT: council items + t421u/t422u/t423u + scene work
- Ledger fixed (above). Render 30 "A gift from the Word Guardian"; sv-now-10 re-shot with "kite อยู่ที่ไหน"; G1 tunic-rose meaning; gem tag menu before/after the verse (390/320, English tag exactly "Daily gift: +1 gem").
- t421u: Watchman fix1-4 copies and the v6-07 m2 sheet removed from the queue; m2 re-shot from v6-08. t422u eyes = A (no change). t423u: P1 rule + check; 12 C, 20/21 C, 24-27 A.
- Pure bug fixed on the way: 21 at 390 had Replay/Got it 6 px apart (rule >= 8); now 8.
- Scenes E, A-H, Level 1-5 strip (Word Meadow) in scenes/; spec + cards + checks in qm_v608/fixes_v608. Checks v6-08: 315 True / 0 False.

## Oct 31, 2026, 4:21 PM MDT: fix snapshot snap-1621MDT (gate candidate, t434u)
| Row | Delta | PASTE |
|---|---|---|
| snap-1604MDT | | 185,611 |
| K1 hero + zoneRuns in state, restore keys (incl. Watchman S1 +6), K2 tier-slot ids (incl. Watchman G1), K3 time of day = 1 + zoneRuns[zone] mod 5, M1 reconcile drops unknown ids (no refund), M2 Big or small as a scene card, U1 count, F2-F4 rows, F5 welcome-back before verse | +590 | 186,201 (banked 1,999) |
- Checks (NAE_VERSION set): v6-08 313 True / 0 live False / 74 SUPERSEDED; v6-07 292 / 0 / 57; v6-06 283 / 0 / 55. Grace-word check: clean.
- Render bugs: scene targets A, C, D, E, F all 44 pt+, 8 px apart, no overlap (scenery carries no tap; truck sits partly behind the hill); 19 Done 8 px from speaker; 08 'Coming next' inside its plate, Home Lake bubble opens upward clear of the hero strip (polish-r1/council/before-after-08.png).
- scenes/before-after-E.png re-shot (t426u confirmation).
- t435u: M1 refund pick dropped from QUEUE; reconcile rule stays.
- CURRENT-v6-08.md drafted (e325f46f); CURRENT.md untouched (b653ffb2).
- Not done yet: 320 renders for scenes A-H and L1-L5; Watchman sweep P1-P4, P7, P8, P10-P14; missing renders 14, 15, 16, 40-43, 45, 47 and the phrase ask card; new-feature mocks (walk A/B, phrasings, letter game, gem-tag timing) for the next snapshot.

## Oct 31, 2026, 5:00 PM MDT: snapshot snap-1700MDT (read-only). PASTE 7374cc6f, 187,074 chars, banked 1,126. CURRENT.md not flipped (v5-37 b653ffb2).
Ledger since snap-1621MDT (a077a328, 186,201), in build order (qm_v608.py R loop: ... + AG + IN_SPEC + CH_SPEC + WG; cards: IN_CARDS + CH_CARDS):
- AG Auditor glitch hunt 47d0b89c: g1-g9 (+334 as scripts) + R1 resume +47 + A1 run id date +13 / +21.
- IN Instructor sweep 2 9a7e52d9 (verified by Instructor on c7632e33 = QM's working PASTE at 4:29:34 PM MDT after AG, 186,616; not a frozen snapshot): ask-en-both +26, kitchen-tap +19 (later replaced by WG W10), color-ask +48, cards cs-07/sw-11 (NEEDS NANCY)/guardianLast/ms-04 + CH C4 tex +58.
- CH Chancellor 5da6f734: newcap 0 (cap 8), firstrun -16, arrowtie +38 (pairs with A1), cssdefaults (cards); plain fixes a (a miss keeps every coin: -79/-50/-23/-64), b (+25 fewest words first), c (+23 recap ends like a round), d (+61/+11 ring text).
  Coin vs G4: ONE edit. Chancellor (a) applied; G4 kept for its scene rule, only its now-doubled "no coin off, " clause trimmed (-13).
- WG Watchman glitch hunt 73b6d48f (checked on 476f0b65), parent ruling 4:42 PM MDT: welcomeback-key -7, region-once +28, level20-bar +24, tod-steps +47, bigsmall-card +50, frontdesk-scene +38 (scripts as written);
  W1 scene-apart lean +143 (was +186: "Never in one scene (one waits): <9 groups>"; "one waits" covers Baby's 5-card group); W2 count-prop lean +82 (was +103);
  W10 Kitchen say-it cards are scene targets (:226 wins) -36 (removes the picture-first sentence incl. its uiText.continue mention; uiText.continue is still used by Audio wake and pause, so no orphan); restore keeps hero/giftGems/zoneRuns when a backup lacks them +25.
  Total WG +394. Render 20 (Kitchen picture-first) moved to screens-v608/superseded-W10/.
- Render fixes (0 chars): R1 bar fill = zone tint, Sound Duel shows the Echo Knight name plate only (no bar); R2 hint button (72 pt, 64 at 568, Aqua, metal rim, leaf-heart) beside the speaker on every scene ask card and Count it; R3 Pantry (stars in header, Thai under names, wearIt EN+TH, tinted shirts, only the worn item glows); R4 33 reply (crib out, 320 buttons under the text); R5 22 speaker inside, table for crib, room scenery; R6 mushroom/bridge/tent scenery in Sound Duel; R7 tod steps 1-3 distinct (sky stop swap + tint); R8 no star dots at dawn (H and forest steps 1-2, dawn-mist ground); R9 scenes A-H at 320 (scenes/s320/, incl. C10 = ten cows); R10 E shows ms-21's own en/th (what the PASTE builds).
  Also: 17-19 disc hidden (2 pt from Pray), duel first line beside the speaker (tiles 8 pt+ clear), menu 320 button spacing, Z.screen at 320 now gets W,H (10/11/13 at 320 were 390 crops before).
- Not built at 320 (out of scope, no layout rule yet): play screens 11-19, 23-32, 37, 44, 48 and gear 40/41 (their 320 files were removed rather than shown broken).
- Checks (NAE_VERSION set): v6-08 311 True / 0 live False / 80 SUPERSEDED; v6-07 292/0/57; v6-06 284/0/55. checks_v608_block.py is stale (checks_v608.py is the authority).

## Oct 31, 2026, 5:31 PM MDT: STAGED working copy (not frozen). PASTE 95a4d0fc, 187,208 chars, banked 992. snap-1700MDT stays frozen under Auditor's recheck. CURRENT.md not flipped (v5-37 b653ffb2).
Ledger since snap-1700MDT (7374cc6f, 187,074), Watchman re-walk 1700 (b365ef8f) + Auditor recheck (43b4b669), parent 5:12 / 5:17 PM MDT:
| Row | Delta | PASTE |
|---|---|---|
| snap-1700MDT | | 187,074 |
| H1 watchman-scene-apart-r2 (5feae868, required): 7 more look-alike groups in the W1 list | +69 | 187,143 |
| watchman-frontdesk-r2 (9ef100e1): "(only them in that scene, repeats filling it)" | +8 | 187,151 |
| W2 auditor-r1-countit-wording (7cfa3a7f): "Scenery copies of the prop hide; Count it, Big or small: never the spoken target." (count-prop-r2 58c7de76 DROPPED) | 0 | 187,151 |
| F1 :268 `run:<local date>:<zone>:<runId>` (+7); :174 "(today's `run:` ids; a Sound Duel round writes one too)" (+35; Auditor estimated +33, the clause is 35 chars) | +42 | 187,193 |
| F2 :268 `region:<id>` added to the ledger id list | +15 | 187,208 |
- How: r2 + countit are b-string edits inside WG (fixes_v608._wg2 reads EDITS from patches/); F1/F2 are b-string edits inside AG A1 (fixes_v608._rc), so the final text equals the patch text and every pin follows it. Diffs: staged/diff-PASTE-snap1700-to-staged-1731.diff, staged/diff-spec-...
- Unchanged from snap-1700MDT: cards 149dfc59, verses 81295c9f (byte-identical), title bab91ec9, qm 420d5166. FINAL d467d659, spec 351a4ce6.
- Checks (NAE_VERSION set): v6-08 312 True / 0 live False / 80 SUPERSEDED; v6-07 292/0/57; v6-06 284/0/55. checks_v608.py ffe4cf47 (AG pin now needs `<zone>`, `region:<id>` and the Sound Duel clause; WG r2 pin uses the Auditor wording).
- F6: patch_checks_v608.py (098ded60) now refuses to run (exit 1) while checks_v608_block.py is the stale 2761acae; v520/checks_v608.py is the source of truth. freeze_v608.sh (d35e7d65, not run for real) copies v608build/patches/ and README.md into every new snapshot; MANIFEST.md5 is built with `find . -type f ! -name MANIFEST.md5` (Auditor H1). Scratch test (SNAP_DIR=/tmp/freeze-scratch/snap-test): 47 files, `md5sum -c` all OK, manifest does not list itself.
- Renders (0 chars): V1-V6 as reported at 5:12 (V1 Sound Duel Thai title clear of the speaker at 320; V2 Thai lh 1.7 on 33/45/25; V3 16 pt margins at 320 incl. the bridge; V4 Echo Forest tod renders are Sound Duel; V5 Count it cows untapped, only plates tappable; V6 Pantry 320 scroll panel + gold thumb).
  XP bar fill = XP Purple #6D3CC9 (spec :80/:95; Auditor said :89) on every play HUD, incl. zone-*-ask-320x568 (re-shot 5:47 PM MDT, Auditor H2); no live render keeps a #5DBB63 XP fill (left only in superseded-*/, b1/ (v5-37 look) and eyes/scene-variety (decided t422u)). Thai lh 1.7 on 14, 23 and 46 at 390/390check (46 also 320) (Auditor R2). The map's Level plate bar (approved t306u/t346u mock, yellow #FFCC33) was NOT changed: Maxwell approved those screens pixel-identical (t385u); flagged for a call.
  Screen 07/08 choosers (:174): while a chooser is open the region rows behind it are inert (no tap) under a soft parchment veil; Back closes it. DOM check: 70 files, only the known Pantry-320 scroll clip.
- Scene E (:227 full-height door, wall key rack, truck far behind the hill): Maxwell t426u, Oct 31, 2026. His exact words are not in any file on the box; the memory record reads: "approved scene E (front desk) with changes: keys on a wall rack, not floating by Nancy's hand; the truck smaller and lower so it reads as outside; the door full height to the floor; the clock fine. General rule: every prop sits where it really would be, at a sensible scale, never floating." (paraphrase, not verbatim).
- Sheets (decisions/b2b/, all looked at): TG1 + D1 (re-shot), B1 + D2 (re-shot), TG2, TG3, TG4, bloodtide-name, night-title-line, coin-rule, letter-game-A-B, state-pairs-lean. Batch 2 walk24 / phrasings and scenes/before-after-* re-shot with XP Purple.

## Oct 31, 2026, 5:47 PM MDT: Auditor staged recheck (f46d83b1, HOLD) fixes, all 0 PASTE chars. PASTE still 95a4d0fc (187,208). Not frozen.
- H1 freeze_v608.sh manifest + README copy (above). H2 zone-*-ask-320x568 re-shot purple. R2 Thai lh 1.7 on 14/23/46. R1 QUEUE Pair 4 split (max 2 per round). R3 bloodtide sheet asks "two other names" (5882d53c). R4 stale comments: checks_v608.py :102 (picture-first reason now cites W10) and :1480 IN label, fixes_v608.py :155 (countit, not count-prop-r2).
- Also re-shot with XP Purple: decisions/m2-sound-duel-speaker-A-B-390-v608.png (e9fbea94), emoji12-now-A-B-C-390.png (f9758c8d), emoji-17-18-19-390.png (c4f767f6, script emoji171819_v608.py).
- Checks: v6-08 312/0/80, v6-07 292/0/57, v6-06 284/0/55. DOM check: 70 files, only the known Pantry-320 scroll clip.
