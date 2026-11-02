# Round 2 (STAGED, not frozen), Oct 31, 2026, 6:40 PM MDT; Auditor HOLD e5129779 fixes 7:23 PM MDT
Base: snap-1748MDT (gate CLEAR b8e3ba68), PASTE 95a4d0fc 187,208. Nothing here touches qm_v608.py, the build output or any snapshot. CURRENT.md stays v5-37 (b653ffb2).
`python3 round2.py` rewrites staged/ from snap-1748MDT and writes diff-PASTE/-spec/-cards-snap-1748MDT-to-round2.diff.

| Patch | Ask | PASTE delta | PASTE |
|---|---|---|---|
| snap-1748MDT | | | 187,208 |
| P1 maxwell-t440u-ask-phrasing | tapPrompt "Can you find the {word}?" / "หา {word} เจอไหม" (Thai NEEDS NANCY via thStatusDefault); :226 example 'Can you find red?' | +7 | 187,215 |
| P2 maxwell-t441u-walk24-B | :246 an emoji person picture is a 52 pt prop, centred between the screen edge and the hero (D4 'an emoji person', +7 measured) | +71 | 187,286 |
| P3 maxwell-t439u-scene-one-layout | :227 drops the 320 hero numbers; one 390 x 844 layout scaled as one piece to the screen width, bottom pinned, sky cropped; the HUD, card and 44 pt tap areas stay full size (D2, +98 over the old +62). ', each on its furniture or ground' (+33) is the t426u rule (D3), written in with P3 | +160 | 187,446 |
| D1 | spec :417 banked line = 754 / 187,446 (spec only, same digits) | 0 | 187,446 |
Total +238; PASTE 19321a59, banked left 754 (of 992). Thai reserve 188,200-188,500 untouched.

- P1 scope (parent 6:16 PM MDT, narrow): only the 44 cards that already use tapPrompt (:226 filter, exclusion list and colour rule kept). The 86 sentence cards keep their own en/th asks; no plural line. ask-walk-44.md lists all 44.
  The tapPrompt json is in the PASTE and cards.json only; FINAL/spec carry only the :226 example. listenFind ("Listen. Where is it?") is the spoken-only card, not a word ask: unchanged.
- D5: checks/checks_v608.py is the staged checks: a round 2 layer reads every pinned v6-08 literal through round2.py's own edits (no new literals); B1 template, colour example, fd-08 and the :1367 guard regex come from uiText.tapPrompt; diff-only undoes round 2 first; the generator length check subtracts the round 2 delta; scene renders point at the t439u stage. Run: cd /workspace/v520 && NAE_W=<scratch with staged files> NAE_VERSION=v6-08 python3 /workspace/v608build/round2/checks/checks_v608.py -> 0 live False on the staged copy AND on the build. (:1106/:1322 read v6-04/v6-07 files, unaffected.) The live v520/checks_v608.py is untouched; it has 1 live False on the build (scene renders path, since the t439u move).
- Renders: renders/ask-can-you-find-390x844 and -320x568 are now stage scene A ('Can you find the ship?') at both sizes on the fit-to-width stage (NAE_R2TP=1 stage_v608.py); render_phrasing.py (screen 10) is superseded because the kite crops under the HUD at 320 under D2. Scenes: v608build/scenes/stage/ (stage_v608.py, CHECK.md). Sheets: sheets/.

## Auditor HOLD e5129779 fixes (7:23 PM MDT)
- S1 tufts: per scene, on open grass above the card (A, B, W24), #0F3A14 2.5 px, 3.9:1 on grass #36A13D. S2: the t441u outdoor block moved out of play_v608.py into screens/t441u_outdoor.py, applied only in stage_v608 (approved screens are byte-identical to the 18:09 baseline again, 10-13, 15, 23-31, 34-37, 44, 48 and the tod 390 strips).
- D2 stage: s = 390-fit to the width, bottom pinned (oy = card - card390 x s), sky cropped; sky targets in the new scenes come down (B kite, bus stop; A rain cloud). S3: the Word Guardian label sits on the HUD chip line at every size (stage_v608.guardian_on_hud).
- S5: screens-v608 320 scene renders (10, 14, 21, 22, 23, 33-36, 54, zone x4) and tod 320 x 20 rebuilt on the fit-to-width stage (screens/stage320_play.py, scenes/tod_stage320.py). D2 consequence on approved layouts at 320: kite (10, meadow zone, meadow tod) and owl/lantern (forest zone) crop under the HUD; lake desk/towel/crib come within 13-15 pt of the edge. Moving them changes t385u 390 screens: a decision, not done.
- Screen 48: the scene is inert under the pause card (aria-hidden, pointer-events none, no data-tap): DOM taps = Continue only. 0 chars.
- Asset depth: asset-depth/COSTS-and-LEDGER.md, mirror and clinic mocks and sheets.

## Round2b (7:51 PM MDT; Auditor 48295eae + council updates)
- round2.py P4 +188 (sky B "; the crop never puts a target under the HUD (the scene shrinks to fit instead)" +79, "; targets keep 16 pt from the screen edge" +41, t444u "; on taller phones a room crops its ceiling to the 320 × 568 framing" +68) and P5 +50 ("; on guardian runs the zone chip shows `boss.name`", Maxwell t445u, QM-relayed). PASTE 187,684 bfb0392b, 516 banked.
- Render-level: stage_v608.fit_capped (B) used by screens/stage320_play.py and scenes/tod_stage320.py (320 scene renders + tod 320); 390 unchanged. Screen 33 scene inert under the say-it card (png unchanged). Ceiling trim: round2/ceiling-cap (E, F at 390 / 375).
- checks: round2.py via NAE_W; 5 independent R2b lines (328 True, 0 live False, 80 SUPERSEDED).
- 8:09 PM MDT: P6 sw-19 choices run -> ten (0 chars, owner's yes). Trim pick staged both ways: 1A all rooms (+68) in staged/, 1B front desk and night table (+93) in trim-1B/staged/ (NAE_TRIM=1B python3 round2.py). Guardian name on the chip line for 24-28; menu inert under the verse pop-up; 3B trim renders in ceiling-cap/ and ceiling-cap/home-lake/.
- 8:35 PM MDT (snap-r2b): walk 24 at 320 scales down (stage_v608 fit_whole: the swing set, trees, walker and heroes clear the Guardian banner; 390 byte-identical; t445u). Instructor gate fixes, render only: screen 18 glow on Pray (the right answer) with the X on High five; screen 23 card Level 3 like its HUD; screen 36 roundDone ribbon under the Echo Knight plate (390) / heading the card (320). Sky-B renders re-shot with the round 2 ask (sky-options/B/png-r2ask/). Round totals (round_totals.py) on the ledger and every pick sheet. Showcase footers name the snapshot; tile 19 "The Guardian is beaten."
