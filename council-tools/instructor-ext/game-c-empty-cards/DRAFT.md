**Instructor:** # Game priority (c): drafts for the 4 empty personal cards bh-30, ms-28, ms-29, ms-30 (DRAFT ONLY, no PASTE, live or snap file touched)
**Instructor:** Assigned by QM (Council, Nov 1, after Maxwell's t581u game-first direction). Written Nov 1, 2026 (MST). Nothing here is ready to paste.
**Instructor:** Base checked this turn: CURRENT-SNAP.txt f6dac2d0 (snap-r2h-0021MDT), PASTE `r2h-build/nancys-adventure-english-v6-08-1B-v32-PASTE.md` 317e91ce, 188,116 chars, bank 84 (ceiling 188,200). All 4 cards are empty on line 427: `"en":"","th":"","respell":""`, `fill:true`, `slot` baby / hotel / husband / faith, `personal:true` (ms-30 also has `faith:true`).
**Instructor:** ## Rules these drafts follow
**Instructor:** Spec section 17: these are the 4 personal say-it slots that "wait for Maxwell" (bh-30 the baby, ms-28 the hotel, ms-29 Maxwell, her husband, ms-30 faith). All 4 are on `needsMaxwell` (7), and must-do.md item 2 says Maxwell writes them by Nov 7. So each card below is a 1A/1B proposal for Maxwell to confirm or edit, not a final.
**Instructor:** Say-it schema (section 8/16): `type:"say-it"`, `en`, `th`, `respell`; no choices, no pic, no hint. `thStatus` is left out because the default is NEEDS NANCY (`meta.cardThStatusDefault`), which costs 0 chars.
**Instructor:** 6 words or fewer (ms-06 and bh-14 are the only approved 7-word exceptions). Every draft is 3 to 5 words.
**Instructor:** Speaker convention: bh is Nancy (ค่ะ). In ms, Maxwell speaks (ครับ, ผม), except that Nancy speaks the hotel lines (ms-03 to ms-06) and ms-32 (ค่ะ). These drafts follow that.
**Instructor:** No surnames, no Elk Refuge Inn, no due date (it appears only in bh-11), no contact info, no 911 or Call Max, no pic, so no emoji-version risk. No scripture is quoted and there's no new verse moment.
**Instructor:** 17px rule (Thai 17px+, line-height 1.7, zero scroll at 320x568): the longest new Thai is 27 chars (1B ms-28) and the longest English is 24 chars. Existing say-it cards already render at 17px with longer text (ms-02 and nm-09 Thai are 34 chars, bh-10 English is 28). PASS by comparison only. These cards aren't rendered anywhere yet, so text_check hasn't run on them (UNVERIFIED on a render).
**Instructor:** ## Char cost: how it was measured
**Instructor:** fit_table.py e95adcd6 (costs.json fea5bd8e), run on a copy in `scratch/`: `--selftest` gave PASS, rc 0. A real run REFUSES with rc 1, because costs.json's manifest is 3bee8d98 (r2g) and the pointer's is 7b7c357f (r2h), and the costs.json bank is a stale 403. fit_table also only lists R2 combinations and has no per-card cost mode.
**Instructor:** So I measured with fit_table's own metric, which is `len(PASTE text)` in Python chars with bank = ceiling 188,200 minus length (`fit_table.check_bank` imported, pinned bank switched off), on scratch copies of 317e91ce. Script: `scratch/measure.py` and `scratch/measure_spec.py`. Every variant's line 427 parses as JSON, and the 4 cards read back exactly as drafted.
**Instructor:** "min" = fill `en`/`th`/`respell` only and keep `fill:true` and `slot`. "lean" = also drop `"fill":true,` and `"slot":"…",` from these 4. That's safe in the data: once `en` is written the run order no longer skips the card, and ms-04 to ms-06 keep `fill`. But `slot` then exists on no card, which orphans the spec's `slot?` field and its line 353 under rule 11, so lean needs the spec edits below.
**Instructor:** ## bh-30 (the baby), zone Baby and Hospital, Nancy speaking
**Instructor:** 1A English: The baby is kicking. / respell: thuh BAY-bee iz KIK-ing / 4 words
**Instructor:** 1A Thai: ลูกดิ้นค่ะ [NEEDS NANCY] (new string, built byte-for-byte from bh-09 ลูกไม่ดิ้นค่ะ with ไม่ removed)
**Instructor:** 1A JSON (min): `{"id":"bh-30","type":"say-it","en":"The baby is kicking.","th":"ลูกดิ้นค่ะ","respell":"thuh BAY-bee iz KIK-ing","fill":true,"slot":"baby","personal":true}` = +53 chars
**Instructor:** 1A JSON (lean): `{"id":"bh-30","type":"say-it","en":"The baby is kicking.","th":"ลูกดิ้นค่ะ","respell":"thuh BAY-bee iz KIK-ing","personal":true}` = +27 chars
**Instructor:** 1A reason: it's the happy opposite of the bh-09 nurse phrase "The baby is not moving.", so she can tell a nurse that everything is fine, and it reuses words she already knows.
**Instructor:** 1B: My baby is healthy. / ลูกของฉันแข็งแรงดีค่ะ [NEEDS NANCY] (new; ลูกของฉัน reused from bh-15/bh-16) / mai BAY-bee iz HEL-thee / min +63, lean +37
**Instructor:** ## ms-28 (the hotel), zone Maxwell Says, Nancy at the front desk
**Instructor:** 1A English: Here is your key. / respell: HEER iz yor KEE / 4 words
**Instructor:** 1A Thai: นี่กุญแจของคุณค่ะ [NEEDS NANCY] (new string, using the frame of sw-01 นี่บัตรของคุณค่ะ with กุญแจ from ms-21)
**Instructor:** 1A JSON (min): `{"id":"ms-28","type":"say-it","en":"Here is your key.","th":"นี่กุญแจของคุณค่ะ","respell":"HEER iz yor KEE","fill":true,"slot":"hotel","personal":true}` = +49 chars
**Instructor:** 1A JSON (lean): `{"id":"ms-28","type":"say-it","en":"Here is your key.","th":"นี่กุญแจของคุณค่ะ","respell":"HEER iz yor KEE","personal":true}` = +22 chars
**Instructor:** 1A reason: she'd really say this at check-in. It uses the "your" possessive and matches sw-01 "Here is your card." with no inn name. Note: "Here is your key." is already a wrong choice in nm-04, so it shows up there as a distractor too. That isn't a conflict, but QM should know.
**Instructor:** 1B: Do you need more towels? / ต้องการผ้าเช็ดตัวเพิ่มไหมคะ [NEEDS NANCY] (new; ต้องการ from bh-01, ผ้าเช็ดตัว from ph-05, ไหมคะ from sw-03) / doo yoo NEED mor TOW-elz / min +75, lean +48
**Instructor:** ## ms-29 (Maxwell, her husband), zone Maxwell Says, Nancy speaking
**Instructor:** 1A English: This is my husband. / respell: THIS iz mai HUZ-bund / 4 words
**Instructor:** 1A Thai: นี่สามีของฉันค่ะ [NEEDS NANCY] (new string: นี่ from sw-01, with สามีของฉันค่ะ byte-identical to the tail of sw-04 and bh-06)
**Instructor:** 1A JSON (min): `{"id":"ms-29","type":"say-it","en":"This is my husband.","th":"นี่สามีของฉันค่ะ","respell":"THIS iz mai HUZ-bund","fill":true,"slot":"husband","personal":true}` = +55 chars
**Instructor:** 1A JSON (lean): `{"id":"ms-29","type":"say-it","en":"This is my husband.","th":"นี่สามีของฉันค่ะ","respell":"THIS iz mai HUZ-bund","personal":true}` = +26 chars
**Instructor:** 1A reason: it's how she introduces Maxwell at church, the clinic or the desk. It practises "my" without putting a name in the data, and it's different from sw-04 "He is my husband."
**Instructor:** 1B (Maxwell speaking): You are my wife. / คุณเป็นภรรยาของผมครับ [NEEDS NANCY] (new; ภรรยา from ph-06, ของผมครับ from ms-14) / yoo ar mai WAIF / min +52, lean +23
**Instructor:** ## ms-30 (faith), zone Maxwell Says, Maxwell speaking, faith:true
**Instructor:** 1A English: God is good. / respell: GOD iz GUD / 3 words
**Instructor:** 1A Thai: พระเจ้าทรงดีครับ [NEEDS NANCY] (new string: พระเจ้าทรงดี is byte-identical to the jesusWordsFallback[0] Thai, plus ครับ)
**Instructor:** 1A JSON (min): `{"id":"ms-30","type":"say-it","en":"God is good.","th":"พระเจ้าทรงดีครับ","respell":"GOD iz GUD","fill":true,"slot":"faith","faith":true,"personal":true}` = +38 chars
**Instructor:** 1A JSON (lean): `{"id":"ms-30","type":"say-it","en":"God is good.","th":"พระเจ้าทรงดีครับ","respell":"GOD iz GUD","faith":true,"personal":true}` = +11 chars
**Instructor:** 1A reason: it's short and warm, A1 level, and echoes the existing grace line "because God is good". It isn't presented as a verse (it's not a scripture quote, so no ESV/THSV text is involved), which keeps the no-new-verse-moment rule.
**Instructor:** 1B: God takes care of us. / พระเจ้าทรงดูแลเราครับ [NEEDS NANCY] (new; พระเจ้าทรง from cs-05/sw-07/bh-17, ดูแล from the John 10:11 thGloss, เรา from bh-17) / GOD tayks KAIR uv us / min +62, lean +35
**Instructor:** ## Totals (measured on copies of 317e91ce, bank 84)
**Instructor:** 1A min (fill 3 fields only): +195, bank left -111. DOES NOT FIT.
**Instructor:** 1A lean (drop fill and slot on the 4): +86, bank left -2. DOES NOT FIT, and it orphans `slot`.
**Instructor:** 1A lean + meta (`emptySlots:[]`; writtenCards 207 to 211, sayItWritten 33 to 37, personalWritten 76 to 80, same length): +55, bank left 29. Fits, but it still orphans the `slot` spec text.
**Instructor:** 1A lean + meta + spec cleanup (5 prose edits, below): -129, bank left 213. The PASTE gets smaller. scratch md5 55e277dc.
**Instructor:** 1B min +252 (-168), 1B lean +143 (-59), 1B lean + meta +112 (-28, does not fit), 1B lean + meta + spec -72 (bank left 156). scratch md5 198c286e.
**Instructor:** ## Spec cleanup measured (QM's text, proposal only, -184 chars total)
**Instructor:** :236 `…"english-first"`: 70 written plus the 4 empty slots (section 17).` becomes `…"english-first"`.` (-48)
**Instructor:** :350 `…in `cards.json`: 207 written plus 4 empty personal slots. Format:` becomes `…in `cards.json`. Format:` (-41)
**Instructor:** :352 `, personal, slot?, prompts?` becomes `, personal, prompts?` (-7). :353 delete ` `slot` names an empty slot's topic.` (-36)
**Instructor:** :369 `Four empty say-it cards wait for Maxwell (`fill:true`, `personal:true`, empty `en`, `th`, `respell`), skipped until written, then sorted first:` becomes `Four personal say-it cards, Instructor drafts for Maxwell to confirm or edit, sorted first:` (-52)
**Instructor:** Not measured, for QM: :223 and :385 still say unwritten cards are skipped, which stays valid as general logic because ms-04 to ms-06 keep `fill`. Section 18 says "any slot Maxwell fills", and `needsMaxwell` keeps all 7 if Maxwell is still to confirm.
**Instructor:** ## Open questions (via QM and the ledger, one asker)
**Instructor:** Q1: These 4 are Maxwell's own personal cards (section 17, needsMaxwell, must-do item 2). Auditor's task (d) builds the needsMaxwell 1A/1B sheet for the same 7 cards, so this file should feed that sheet rather than become a second ask.
**Instructor:** Q2: Zero-char route: section 17 lets Maxwell fill these in cards.json after the build, or through the Backup view list, which costs 0 PASTE chars. Does he want them in the Nov 10 PASTE, or after it?
**Instructor:** Q3: Should the baby or husband card be more personal (the baby's name, whether it's a boy or a girl, Maxwell's name)? First names are allowed and surnames aren't. Any such fact must come from Maxwell, not a bot.
**Instructor:** Q4: Lean vs min, and the spec cleanup, are QM's build call, and fit_sheet_check has to measure them before any PASTE change.
**Instructor:** Ready to paste: none yet. CURRENT stays v5-37, nancys-adventure-english-v5-37-PASTE.md (acc534a51a922102ee37844e04d17955).
**Instructor:** Based on: snap-r2h-0021MDT, pointer f6dac2d0, PASTE 317e91ce.
