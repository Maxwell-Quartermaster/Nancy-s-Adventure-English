**Auditor:** # GATE: QM 320 fix, Echo Knight plate on 34-36, candidate new/play_v608.py acf48ca244a1419311dba03dbc62af78 (base a2871d0a). Sun Nov 1 2026, ~10:30 PM MST. Lean, read-only gate; every md5 came from md5sum this turn.
**Auditor:** Based on: snap-r2h-0021MDT, pointer CURRENT-SNAP.txt f6dac2d0e7b391436a160eab1bbf17fe, PASTE 317e91ce86f073c961f8169183d2bbd3 (both re-hashed unchanged after all runs).
**Auditor:** VERDICT: SECONDED, confidence 0.92. Blockers: none. Rulings: Safari 14 unverified is NOT a blocker for this change, and the 2 pt box overlap does NOT matter (it touches no text and no drawn pixel). One separate pre-existing Safari 14.0 finding (F1) is below.
**Auditor:** ## Inputs
**Auditor:** GATE-REQUEST.md 82f01fa8c2f0f26d3ab86180af67cff0, MD5SUMS 84f247b1de29e17a38f319bbf379aa37, diff 57e4e35222781f70eeb86b461fb0ed53: all match. md5sum -c MD5SUMS: 29/29 OK, re-run OK after my runs.
**Auditor:** ## 1. Chain (chain/)
**Auditor:** base = my gated a2871d0a copy, cmp-identical to QM base/. Base + play_v608.fix320.diff (patch exit 0) = acf48ca244a1419311dba03dbc62af78, cmp-identical to the candidate. The change is 2 added lines at :320-321 in duel() and 0 removed.
**Auditor:** The added lines are ASCII only (0 non-ASCII), run only under 'if SE', and assert that the plate string appears exactly once before swapping left:{W-196}px for left:16px.
**Auditor:** ## 2. Rebuild (tools/build.py 0257c990; out/*.json)
**Auditor:** 390: 31/31 byte-identical to a2871d0a. 375: 31/31 identical. 320: 28/31 identical; only 34, 35 and 36 differ. My base 320 equals my earlier a2871d0a gate run, and my new runs equal QM runs/build-new-* at all 3 sizes.
**Auditor:** Pages 26/30/37: 390 26c1d9ce/dfad68d3/c0835bac, 375 51ac07b1/4860981c/287bffca, 320 11c59779/57cac786/da5c587c. 320 html is cmp-identical to my a2871d0a gate html, so the verse bytes (12/12) and the page 30 HOLD are unchanged.
**Auditor:** Diff scope (tools/dump.py, out/dump-*): in 34/35/36 at 320 the single difference is in the Echo Knight plate div, where 'left:124px' becomes 'left:16px'. Top 122, width 180, text and tint are unchanged.
**Auditor:** QM's fit-to-width docs html/34-36 differ from the snap-r2h-0021MDT 320 docs (f35d4136/e4226262/354d95d3) by that one edit only, which I checked with a char diff.
**Auditor:** ## 3. Render (my own tools/cdp2.mjs via CDP, 320x568, DPR 2, Chrome/Blink; render/measure-after.jsonl, render/png/, render/pixel-check.txt)
**Auditor:** First try: chrome --dump-dom with --window-size timed out (exit 124) on 5 of 6 docs, and the one that finished laid out at innerWidth 500, not 320. Discarded. The CDP device-metrics run then worked first time (exit 0).
**Auditor:** Plate 16,122-196,171.4. Helmet paths start at x 217.7, so the helmet gap is 21.7 pt on 34/35/36. The leftmost knight pixel actually drawn within the plate's rows is x 222 (34/35) and x 234 (36).
**Auditor:** Thai: every Thai node is 17 px with line-height 1.7, and none uses 'normal'. scrollWidth 320 = innerWidth 320: no horizontal scroll.
**Auditor:** 2 pt overlap: the knight svg boxes start at x 194 / 193.6 (34/35) and 193.6 (36), crossing the plate's right edge (196) by 2.0-2.4 pt.
**Auditor:** The plate's text boxes end at x 186, so the overlap sits only in padding/border, 7.6+ pt from any text.
**Auditor:** Pixel test: plate hidden vs plate + knight svgs hidden gives 0 differing pixels in x 186-197, y 122-172. The corner of the boxes is empty, so nothing drawn touches the plate. RULING: not an issue.
**Auditor:** Visual (png/34): the plate sits left over the tent area, clear of the helmet and the chip, with Nancy's head below it. Where the knight's name sits is QM's item e design call for Maxwell, not a gate item.
**Auditor:** ## 4. ES2017 / Safari 14 (out/es2017-css.txt)
**Auditor:** Added lines: 0 '(?<', 0 '\p{', 0 /s, 0 script, 0 inset, 0 aspect-ratio, 0 :is/:where, 0 gap. The emitted change is one integer in an existing absolute 'left:' value, so it adds no new CSS feature.
**Auditor:** The 34-36 320 docs have 0 script blocks, 0 '(?<', 0 '\p{', 0 inset, 0 aspect-ratio and 0 :is/:where, both before and after.
**Auditor:** RULING: 'Safari 14 unverified' is NOT a blocker for this change. It changes no property, only a pixel value of 'left', which every browser supports.
**Auditor:** F1 (pre-existing, not from this change, outside this gate): each 34-36 doc has 3 'display:flex;gap:' uses: the zone chip (dot + Echo Forest + Thai, gap 8px), the light/right answer row (gap 12px) and the HUD level label (one child at 320, so harmless).
**Auditor:** Flex 'gap' arrived in Safari 14.1, so iOS 14.2 (Safari 14.0) ignores it there: the chip items and the two answer buttons would lose their spacing. This needs its own ticket and ruling, not this candidate.
**Auditor:** ## Side effects and rules
**Auditor:** I worked only in this folder. TMPDIR, the Chrome profile and the copies are all here (folder 58M), and tmp/ holds 7 Chrome entries.
**Auditor:** I deleted nothing myself; my cdp2.mjs has no unlink. Chrome may manage its own profile and temp files inside this folder.
**Auditor:** Note for QM: tools/cdp.mjs:5 unlinkSync()s DevToolsActivePort in its own scratch profile. That's a small delete, outside the 'nothing deleted' rule as written.
**Auditor:** The snap 34-36 docs, PASTE, CURRENT-SNAP and QM folder were all unchanged after my runs. df /: 32% before and after.
**Auditor:** Mistakes: (1) one wasted render pass with --dump-dom, which timed out and also ran at the wrong width. (2) render/after/ and render/before/ each also hold 3 copies with my measuring script injected (from that failed pass). They're labeled by the lack of the -320x568 suffix and aren't evidence.
**Auditor:** Ready to paste: none yet.
