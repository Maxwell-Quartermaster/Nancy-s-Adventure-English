**Auditor:** # GATE: QM cards 1A (P) + Safari 14.0 flex-gap fix (R). Sun Nov 1 2026, ~10:55 PM MST. Lean, read-only gate; every md5 came from md5sum this turn.
**Auditor:** Based on: snap-r2h-0021MDT, pointer CURRENT-SNAP.txt f6dac2d0e7b391436a160eab1bbf17fe, PASTE 317e91ce86f073c961f8169183d2bbd3 (both re-hashed unchanged after all runs). df /: 32% before and after.
**Auditor:** VERDICT (P) PASTE 55e277dc: NOT SECONDED, confidence 0.90. Blocker P-B1, plus a must-fix P-B2 that costs 0 chars.
**Auditor:** VERDICT (R) renderer 70b5fbc9: SECONDED, confidence 0.90. No blockers; advisories R-A1 to R-A4.
**Auditor:** ## Inputs
**Auditor:** GATE-REQUEST.md 6c6c5bfdb1fa98bd0d652edc034ab111, MD5SUMS 21ba5c4a04427927edbe6872cc2928a4: md5sum -c 459/459 OK, re-run OK after my runs.
**Auditor:** Candidate PASTE 55e277dc77a3a1079d6c2f019a5a652f; candidate renderer 70b5fbc9d526fa83028e664981efc36d.
**Auditor:** ## P1. Diff 317e91ce -> 55e277dc (p/, tools/jdiff.py, out/p-jdiff.txt)
**Auditor:** Byte identity: cmp-identical to instructor-ext/game-c-empty-cards/scratch/variant-1A-lean-meta-spec.md (55e277dc). Both files have 429 lines; only lines 236, 350, 352, 353, 369 and 427 differ.
**Auditor:** Spec edit 1 (:236): ': 70 written plus the 4 empty slots (section 17)' is removed.
**Auditor:** Spec edit 2 (:350): ': 207 written plus 4 empty personal slots' is removed.
**Auditor:** Spec edit 3 (:352): 'slot?' is removed from the card field list.
**Auditor:** Spec edit 4 (:353): the sentence 'slot names an empty slot's topic.' is removed.
**Auditor:** Spec edit 5 (:369): 'Four empty say-it cards wait for Maxwell (...) skipped until written' becomes 'Four personal say-it cards, Instructor drafts for Maxwell to confirm or edit'.
**Auditor:** All 5 match DRAFT.md 5f3f2184 :50-53 and are consistent with the data. No card keeps 'slot'; fill:true remains only on ms-04/05/06; :223/:385 skip logic stays valid for those 3; needsMaxwell (:371 and the JSON) still lists all 7.
**Auditor:** Line 427 deep diff: only cards[155-158] (bh-30, ms-28, ms-29, ms-30) changed. For each, en/th/respell went from empty to filled, and fill and slot were removed.
**Auditor:** The only meta changes are emptySlots 4 -> [], writtenCards 207 -> 211, sayItWritten 33 -> 37 and personalWritten 76 -> 80.
**Auditor:** verses, jesusWords and jesusWordsFallback are equal (Python ==). ms-04/05/06 and nm-04 are unchanged. No boss data, rule 9 or red wording changed (no other line differs).
**Auditor:** New cards vs DRAFT 1A lean JSON: bh-30 'The baby is kicking.' ลูกดิ้นค่ะ, ms-29 'This is my husband.' นี่สามีของฉันค่ะ and ms-30 'God is good.' พระเจ้าทรงดีครับ (faith:true) all match DRAFT 1A and SHEET-v5 (e53b55dc) 6A/8A/9A byte-for-byte.
**Auditor:** P-B1 BLOCKER: ms-28 is 'Here is your key.' / นี่กุญแจของคุณค่ะ / 'HEER iz yor KEE' (DRAFT 1A). SHEET-v5 :42 tile 7A is 'Your room is ready.' / ห้องของคุณพร้อมแล้วค่ะ / 'yor ROOM iz RED-ee'.
**Auditor:** The sheet chose 7A because 'Here is your key.' is already a wrong choice on nm-04 (SHEET-v5 :58; nm-04 choices confirmed in the data). '1A' means different lines in the two documents, so 'Maxwell picked 1A' does not settle ms-28.
**Auditor:** Fix: QM confirms with Maxwell which line he picked, or swaps in the sheet's 7A. Measured in memory: the swap is exact-once, +10 chars, length 187,997, bank 203, so it still fits.
**Auditor:** P-B2 MUST-FIX (0 chars): spec :375 still says 'Everything starts NEEDS NANCY: 201 of the 207 written cards'. The data now has 211 written, 205 of them NEEDS NANCY (recounted). '205 of the 211' is the same length, so the bank is unchanged.
**Auditor:** ## P2. Integrity
**Auditor:** Length 187,987 Python chars (213,211 bytes), bank 213 = 188,200 - len. The JSON line parses. 211 cards, 211 unique ids.
**Auditor:** Recount matches meta: written 211, sayItWritten 37, personalWritten 80, emptySlots [].
**Auditor:** New Thai: no thStatus key, so meta.cardThStatusDefault = 'NEEDS NANCY' applies to all 4 (spec :352). They're also NEEDS NANCY in both DRAFT and SHEET. That covers the Nov 7 sign-off marking.
**Auditor:** ## P3. Content rules on the 4 new cards and the 5 spec edits (out/p-rules.txt)
**Auditor:** 0 contact info / phone / email / url; 0 '911', 'Call Max' or 'Show the Nurse'; 0 emoji (no non-Thai non-ASCII chars); 0 brand names; 0 '(?<', 0 '\p{', 0 /s. Word counts are 4/4/4/3 (6 or fewer).
**Auditor:** ## R4. Renderer
**Auditor:** Chain: acf48ca2 (my fix320 gate copy, cmp = QM base) + flexgap.diff c8d4f19af12e9c5230ffc1354a66b4e1 = 70b5fbc9, patch exit 0, cmp-identical. +45/-0, all after duel()/guardian_chip, before the end.
**Auditor:** Diff review: flexgap() removes 'gap:Npx' only from inline display:flex boxes and adds margin-left (row) or margin-top (column) to element children 2..n.
**Auditor:** It asserts the child has no margin of its own, and that the box has no wrap, row-gap or column-gap. It wraps every SCR page except 30, plus guardian_chip; _CHIP is re-matched to the gap-less chip. Grid untouched; no other behavior change.
**Auditor:** Rebuild (tools/build.py 0257c990, PASTE 317e91ce): 6/6 runs with 0 errors, 0 writes and 0 other events. New vs base: page 30 byte-identical at 390/375/320; the other 30 differ, as expected.
**Auditor:** My new runs equal QM runs/build-new-* at all 3 sizes. Page 26/37 md5s match the request: 390 8f7d02c4/c0f02e8c, 375 379ce22e/92bbd8d1, 320 e0503594/d7d90b72.
**Auditor:** The new renderer gives the same 31 page md5s at 320 with PASTE 55e277dc as with 317e91ce, so the PASTE change doesn't move any showcase page.
**Auditor:** My own render (tools/cdp3.mjs: CDP, DPR 2, animations and SVG paused at t=0 on both sides): 320 pages 12, 14, 24, 25, 30, 34, 37 and 390 pages 16, 26, 28, 35. That's 11/11 pairs with 0 differing pixels and every element rect identical.
**Auditor:** Chrome finds 0 flex boxes with gap on the new versions of those pages, except page 30 (3, HELD). scrollWidth = viewport.
**Auditor:** QM evidence spot-check: I recomputed all 96 of QM's png before/after pairs (31 x 3 sizes + fit320 x 3) with PIL: 0 differ, matching runs/pixdiff-*.txt (TOTAL_DIFF_PX 0).
**Auditor:** Output grep (out/flexgap-grep.txt): across all 31 new pages at 390 and 320, inline flex-with-gap appears only on 30-new-weapon-gift (3), and there's no gap in any <style> block.
**Auditor:** Animation pause at t=0 is acceptable evidence: it's the same freeze on both sides, and page 30 (byte-identical HTML) is the control.
**Auditor:** Page-level byte change on 26/37: acceptable. The verse strings are unchanged (QM S3), and my render shows 0 pixel/rect change on 26 and 37.
**Auditor:** R-A1: page 30 (HELD) keeps 3 flex gaps (HUD label, zone chip, button row), so on Safari 14.0 they lose spacing until the HOLD lifts. That's Maxwell's call (QM B8).
**Auditor:** R-A2: flexgap() counts element children only, so a flex item that is a bare text node, or an absolutely positioned child, would be mis-spaced. There are none today (0 pixel / 0 rect diff), but a future page could hit it unseen.
**Auditor:** R-A3 (delete flag): QM tools/cdp.mjs:5 still calls fs.unlinkSync(DevToolsActivePort) in its scratch profile, which is outside the 'delete nothing' rule.
**Auditor:** My cdp3.mjs never deletes. When a reused profile left a stale port file (my first 390 run failed with ECONNREFUSED), I used a second profile dir, render/prof390, instead of deleting it.
**Auditor:** R-A4: PASTE :289 'Safari 14 CSS: no aspect-ratio, :has(), color-mix() or container queries' doesn't ban flex gap. The real game is built from the PASTE, so it could still use flex gap. Adding 'or flex gap' (about 12 chars) is a PASTE edit for Maxwell, not part of this gate.
**Auditor:** ## Rulings
**Auditor:** (1) cards.json: in the shipped game, cards.json IS the PASTE's JSON block (PASTE :5, :12, :424), so P delivers the 4 cards.
**Auditor:** (1, cont.) /workspace/nancys-adventure-english-v6-08-cards.json (149dfc59, unchanged, still 4 empty fill slots) only feeds play_v608 showcase renders and patch tools (freeze.py uses the snap trim-1B copy). NOT needed now; resync it at RESUME before any showcase render of these cards.
**Auditor:** (2) The unswept stage_v608 snap screens DO contain inline flex gaps: 02b 3, 02c 3, 18 2, 23 3, 29 3, 30 3, 36 3, 52 1 (0 in style blocks).
**Auditor:** (2, cont.) NOT a blocker for R: they're showcase renders, not the game, and R doesn't touch them. They must not be cited as Safari-14-safe until swept; the real-game risk is R-A4.
**Auditor:** (3) Chrome-only for R is ACCEPTABLE: margin-left/top on flex items is supported by every Safari, and Blink shows 0 pixel / 0 rect change. The remaining risk is only what R-A1/R-A4 leave open. Not a blocker.
**Auditor:** ## Side effects and rules
**Auditor:** I worked only in this folder (161M, including 2 Chrome profiles); TMPDIR=./tmp. Nothing was deleted and no live file touched. CURRENT-SNAP, PASTE 317e91ce and the local cards.json 149dfc59 were unchanged; the QM folder still md5sum -c OK.
**Auditor:** Mistakes: one failed 390 render run (stale DevToolsActivePort in a reused profile), re-run with a fresh profile dir and nothing deleted. No other known mistakes.
**Auditor:** Ready to paste: none yet.
