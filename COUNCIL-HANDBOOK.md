**Quartermaster:** # COUNCIL HANDBOOK: Nancy's Adventure English v6-08 build (one page; written Nov 1, 2026 for Maxwell t540u/t541u)
**Quartermaster:** Load the shared skill `council-build-playbook` at the start of every build or council turn. Playbook SKILL.md md5 df9a61e8 (df9a61e864634c9209d114c13fd92fe6). If you see a different md5, flag it to QM in the Council room before you rely on it.
**Quartermaster:** ## Bots and ids (Maxwell t499u relay; QM is build lead, t482u relay)
**Quartermaster:** Grok 1: Watchman, research, UX, sweeps, cleanup list: dcb35cfa-6fcf-45ae-9dc0-b74b8b00d7ba
**Quartermaster:** Grok 2: Instructor, English content, question wording, Thai, visual copy sweep: 47fc00ab-ae8d-437c-9ac2-e909bd5a2a60
**Quartermaster:** Grok 3: Chancellor, scope, cost, deadlines, screenshot pipeline, sole editor of council-tools: 966e4586-0136-4ebb-b178-af61227c0805
**Quartermaster:** Grok 4: Quartermaster, build lead and source of truth; owns the pointer, the freeze, ASKS-LEDGER, SETTLED-RULINGS, STATUS.
**Quartermaster:** Grok 5: Auditor, code verification, paste gates, quote checks: dc4c33fd-9f0f-448b-8b71-6614ff4b38dc
**Quartermaster:** Council room: c6e948a1-05c2-4e2f-9c2b-1c8213aedac0
**Quartermaster:** ## Before you ask Maxwell anything (Maxwell t542u, Council room)
**Quartermaster:** Step 1, lookup: `python3 /workspace/v608build/council-tools-incoming/ask_lookup.py "your question"` (moves to council-tools after Auditor's gate; Chancellor installs). ALREADY ANSWERED: use the quote, do not ask. MAYBE: QM asks him one line, "does this still apply?". NEW: go to step 2.
**Quartermaster:** Step 2, QM: post the ask to QM. QM adds one ASKS-LEDGER row naming ONE asker, so he is never asked twice.
**Quartermaster:** Step 3, Maxwell: only the named asker asks, with numbered side-by-side pictures (1A/1B) and a tap card. His answer goes into the ledger verbatim the same turn.
**Quartermaster:** Files: ASKS-LEDGER.md (open and closed asks), SETTLED-RULINGS.md (every past ruling, labelled), STATUS.md (one row per bot). All in /workspace/v608build/.
**Quartermaster:** Labels: **Maxwell (tN, chat):** only for his own typed words. A line that talks about Maxwell in the third person is a relay: **Ara (relay, tN, X DM):**. A summary is **<Bot> (paraphrase):** with NO VERBATIM ON RECORD. t-numbers are per chat; always name the chat.
**Quartermaster:** Relays are cut at 3,999 chars (t472u, t473u, t495u were lost). Keep relays under 3,500 chars, or send anything long to a bot directly.
**Quartermaster:** ## Pointer (read before every post)
**Quartermaster:** Pointer: /workspace/v608build/CURRENT-SNAP.txt (now f6dac2d0: snap-r2h-0021MDT, MANIFEST 7b7c357f, renders 62e41535, paste_1b 317e91ce at r2h-build/nancys-adventure-english-v6-08-1B-v32-PASTE.md, 188,116 chars, bank 84). Read it with `python3 -c "import sys; sys.path.insert(0,'/workspace/council-tools'); import current_snap as c; d=c.read(); print(d['snap'], d['pointer_md5'][:8], c.verify(d) or 'OK')"`. Never edit it by hand; only freeze.py moves it.
**Quartermaster:** live_current is v5-37 PASTE acc534a5 (the live app, not the build base).
**Quartermaster:** Freeze tool: /workspace/v608build/freeze/freeze.py; commands and steps in freeze/README.md (dry run first; --hold, --release, --status). Any bot: `python3 /workspace/v608build/freeze/hold_check.py` (exit 1 = HOLD, stop work).
**Quartermaster:** ## Stages (unfrozen; do not edit, send patches to QM)
**Quartermaster:** /workspace/v608build/r2h-rerun-stage/: MANIFEST ac0582ca, renders-MANIFEST 1089c48e, trial pointer reports/STAGE-POINTER-trial.txt 32e9e360 (for send_guard on the stage only).
**Quartermaster:** /workspace/v608build/scene-fill-20261101/: MANIFEST 6848a5e0, renders-MANIFEST 08be71de.
**Quartermaster:** Items parked out of a stage go to /workspace/v608build/r2h-rerun-stage-excluded/ (never /tmp), logged in the FIXLOG with md5.
**Quartermaster:** ## Patches and tools
**Quartermaster:** Patches and diffs go to /workspace/council-tools/incoming/ (tools) or to QM (build). Chancellor applies tool diffs after Auditor's gate; QM applies build patches.
**Quartermaster:** ground_check f46a2d29 (council-tools/ground-check/ground_check.py); text_check 9c433cba (council-tools/text-check/text_check.py; v3 diff d8094f48 pending); send_guard 80615576 (council-tools/send-guard/send_guard.py); fill_batch_check 78c071f0 (council-tools/chancellor-ext/fill_batch_check.py); tuft_check b19579ac (watchman/checker/tuft_check.py). Re-hash before you quote a result; a changed md5 means re-run.
**Quartermaster:** ## Gates before any send to Maxwell
**Quartermaster:** 1. The build it shows is frozen and named by the pointer (no stale or old-news images, t421u, t502u relay).
**Quartermaster:** 2. send_guard exit 0 on every attached PNG against the current pointer; reference sheets with "-before" tiles (e.g. sheets-ref r2h-before-after.png) never go.
**Quartermaster:** 3. text_check clear on the sheet and its captions; Instructor's copy and Thai check for anything with words.
**Quartermaster:** 4. Auditor pre-check (eye check of captions if they can't be traced).
**Quartermaster:** 5. A ledger row with one named asker; numbered 1A/1B images side by side with a tap card; a few sheets at a time.
**Quartermaster:** ## Schedule
**Quartermaster:** Content freeze Fri Nov 6, 11:59 PM PT (moved from Nov 4 on Nov 1, t583u); Auditor gate Nov 7-9; Nancy's Thai pass Nov 7; paste Nov 10; bug fixes only Dec 10 to mid-January.
**Quartermaster:** Why the freeze moved: Sat Oct 31 went entirely to building tools, not the game, and that tool-building day had not been counted against the game schedule.
**Quartermaster:** ## Char budget
**Quartermaster:** PASTE ceiling 188,200 chars; 300-char reserve (README and must-do only, not in the spec); bank now 84 (317e91ce, 188,116). Every PASTE change is measured by Chancellor's fit_sheet_check before it goes in, and goes to Maxwell as a 1A/1B with its char cost.
**Quartermaster:** ## Nancy content rules (never break)
**Quartermaster:** Verses are free gifts, never purchasable, byte-identical to the PASTE, and get no new verse moments (t493u relay).
**Quartermaster:** No 911, no "Call Max", no "Show the Nurse".
**Quartermaster:** Grace wording: no timers, no energy, no fail words; a wrong tap is never called wrong.
**Quartermaster:** Older emoji only (Emoji 13.0 or earlier).
**Quartermaster:** Thai at 17 px or larger with line-height 1.7.
**Quartermaster:** Must run in Safari 14 at 320 pt.
**Quartermaster:** No real surnames and no Elk Refuge Inn in card data. The due date appears only in bh-11. No personal contact info hardcoded (no phone, email or street address).
**Quartermaster:** ## Post format (every Council post)
**Quartermaster:** Every line starts with a bold prefix: **Watchman:**, **Instructor:**, **Chancellor:**, **Quartermaster:**, **Auditor:**; **Maxwell (tN, chat):** only for his own words.
**Quartermaster:** Base line: `Based on: <snap>, pointer <8>, PASTE <8>` plus any stage MANIFESTs you used.
**Quartermaster:** Last line: `Ready to paste: none yet. CURRENT stays v5-37, nancys-adventure-english-v5-37-PASTE.md (acc534a51a922102ee37844e04d17955).` or the exact files in order with md5s.
**Quartermaster:** Update your STATUS.md row when you start or finish a task.
