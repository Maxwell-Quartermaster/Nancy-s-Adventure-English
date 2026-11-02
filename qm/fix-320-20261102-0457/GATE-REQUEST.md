**Quartermaster:** # GATE-REQUEST: 320px game-screen fix (1B), Echo Knight plate off the helmet on screens 34-36 at 320x568. Sun Nov 1 2026, 10:07 PM MST. Maxwell t584u: "fix a game screen at 320px width (not the checking tool)"; t629u: "Ok go for it". Quick Auditor check asked.
**Quartermaster:** Based on: snap-r2h-0021MDT, pointer f6dac2d0, PASTE 317e91ce
**Quartermaster:** ## Source of the item
**Quartermaster:** ASKS-LEDGER.md :22 (1B CLOSED, t584u); SETTLED-RULINGS.md :178 names the known candidate: snap-r2c-2159MDT/showcase/INDEX.md :52 "at 320, screen 36 (and the 34/35 duel screens that share it) the Echo Knight plate overlaps the knight's helmet". Page 30 (the other candidate) stays HELD. Instructor sweep I8 (instructor/v608/boss-nameplate-healthbar-sweep-20261101.md :47) also lists it.
**Quartermaster:** Measured on the shipped 320 renders (snap-r2h-0021MDT/renders/screens/34-36-*-320x568.html, the stage320_play fit-to-width docs): plate box 124,122-304,171.4; helmet dome top 165.4 and plume tip 159 on 34/35 (12.4 pt into the plate), plume 167.9 on 36 (3.5 pt into it). The r2b "plate top 122" move did not clear it.
**Quartermaster:** ## Files (md5 hashed on disk this turn; full list in MD5SUMS)
**Quartermaster:** base/play_v608.py a2871d0a755f1ae8297ad20f8bfaeb22 = byte copy of qm/verse-split-b1-20261101-2124/new/play_v608.py (SECONDED 0.90 tonight).
**Quartermaster:** new/play_v608.py acf48ca244a1419311dba03dbc62af78 = CANDIDATE. play_v608.fix320.diff 57e4e352: 2 lines added in duel() (:320-321), 0 removed.
**Quartermaster:** ## What changed
**Quartermaster:** At 320 only (if SE), the Echo Knight nameplate's left moves from W-196 (124) to 16 pt (the 16 pt edge rule). Same top 122, same 180 width, same text, tint and style. The swap asserts it matches exactly once. 390 and 375 code paths are untouched. 0 PASTE chars, 0 non-ASCII bytes in the added lines, no verse text, no names.
**Quartermaster:** ## Self-checks
**Quartermaster:** 1. Rebuild PASS (tools/build.py 0257c990, Watchman harness, Python only): 31 pages x 390/375/320 for base and new, 6/6 runs exit 0, 0 errors (runs/build-*.json). base matches the a2871d0a gate runs 93/93.
**Quartermaster:** 2. Scope PASS: new vs a2871d0a: 390 31/31 and 375 31/31 byte-identical; 320 28/31, the only differences are 34, 35 and 36.
**Quartermaster:** 3. Verses and page 30 PASS: pages 26 and 37 (verse pages) and 30 (HELD) are byte-identical to qm/verse-split-b1-20261101-2124/html/ at all 3 sizes (cmp), so the verse bytes Auditor checked 12/12 are unchanged. Page md5s 390 26c1d9ce/dfad68d3/c0835bac, 375 51ac07b1/4860981c/287bffca, 320 11c59779/57cac786/da5c587c (26/30/37).
**Quartermaster:** 4. Baseline PASS: CURRENT-SNAP.txt f6dac2d0 (current_snap verify OK), PASTE 317e91ce, both re-hashed after the runs. No writes outside this folder (build.py audit hook: 0 outside writes, 0 other events); no /tmp; Chrome TMPDIR and profile in scratch/.
**Quartermaster:** 5. Shipped 320 docs: tools/fit320.py takes each snap 320 doc and swaps its 320 UI layer for the candidate's. With base it reproduces the snap docs byte-for-byte (cmp, 3/3), so the swap equals the stage320 pipeline output (compose's fit reads only the HUD and card, not the plate). Candidate docs: html/34 7a2de5c7, 35 99878e39, 36 ae8e65f7.
**Quartermaster:** 6. Real 320x568 render (headless Chrome via CDP, tools/cdp.mjs + tools/measure.js, DPR 2): runs/measure-*-fit320.jsonl. After: plate 16,122-196,171.4; helmet gap 21.7 pt on 34/35/36 (before: -12.4/-12.4/-3.5); chip gap 18.6 pt (unchanged); Thai min 17 px, min line-height 1.7, 0 Thai lines at "normal"; scrollWidth 320, no horizontal overflow.
**Quartermaster:** 6a. Open detail: the knight's two figure svg boxes (left edge 193.6/194) still cross the plate's right edge (196) by about 2 pt across, 1.3-10.3 pt down (34/35: tops 161.1 and 167.7; 36: top 170.1). That corner of the boxes is empty (the drawn helmet starts at x 217.7, 21.7 pt away); on the PNGs nothing drawn touches the plate. Nancy's svg does not cross it (runs/measure-new-fit320.jsonl plateHits).
**Quartermaster:** 6b. Render engine is Chrome (Blink), not Safari 14 WebKit; Safari 14 is UNVERIFIED (no WebKit driver here). The change is plain absolute left/top, as the old plate used.
**Quartermaster:** PNGs (640x1136): png/34-*.png 7bbfcefd, 35 262fb2a7, 36 7376a601; before: png/before/34 f3b2810d, 35 a3292e3b, 36 043b1d8f.
**Quartermaster:** ## Auditor, please verify
**Quartermaster:** a. md5s in MD5SUMS (md5sum -c); new = base + only play_v608.fix320.diff.
**Quartermaster:** b. Re-run tools/build.py on new at 390/375/320 (NAE_SE=1 for 320): 93 pages, only 320 34/35/36 differ from a2871d0a.
**Quartermaster:** c. Page 26/30/37 bytes unchanged at all sizes; page 30 HOLD untouched.
**Quartermaster:** d. Look at png/ vs png/before/: the plate is off the helmet, clear of Nancy and the chip; rule whether the 6a box overlap matters.
**Quartermaster:** e. Design call for Maxwell (not a gate blocker): at 320 the knight's name now sits on the left over the tent, not above the knight. The other options are a smaller one-line gold chip (Instructor I3, t496u, needs about +21 PASTE chars) or the knight's name on the HUD chip line like the guardians (guardian_on_hud style).
**Quartermaster:** Ready to paste: none yet.
