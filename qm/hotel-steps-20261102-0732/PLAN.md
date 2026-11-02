**Quartermaster:** # Hotel cards: guest-stay step order (DRAFT ONLY, not gated, nothing pasted)
**Quartermaster:** Written Mon Nov 2, 2026, 12:3x AM MST. Folder stamp 20261102-0732 is UTC. Source: cards1A-fix PASTE 5e1666fe6f7189d3886686749335b3ee (188,007 chars, cap 188,200, bank 193), copied unchanged to src/ (md5 re-checked).
**Quartermaster:** Maxwell (card answer, relayed by QM): "She is a guest and can be alone". Maxwell t646u/t647u (abridged, via QM brief): normal hotel procedures in order, very simple phrases, loose guide not hard rules, hotel only tonight.
**Quartermaster:** ## Research (guest cycle)
**Quartermaster:** Front-office texts split a stay into pre-arrival (reservation), arrival (welcome, registration, room and key), occupancy (requests, problems, a courtesy call from the desk), departure (bill, payment, key back). Sources: slithm.edu.lk front office management tutorial; inflibnet "Guest cycle"; dbpolytech front office curriculum; Eclat Hospitality courtesy call process.
**Quartermaster:** ## 1) Step order (guest side, 6 steps)
**Quartermaster:** S1 Reserve: call or book, ask the price for one night.
**Quartermaster:** S2 Arrive and check in: say she has a reservation (her first name only), wait in line.
**Quartermaster:** S3 Room and key: room is ready, key card, room number, floor.
**Quartermaster:** S4 During the stay: a problem or a request (towels, wifi), or the desk calls to ask how the room is.
**Quartermaster:** S5 Breakfast: what time.
**Quartermaster:** S6 Check out: check-out time, cash or card, change.
**Quartermaster:** ## 2) Mapping (SAY = Nancy says it, say-it card; HEAR = staff line she recognizes, picture card)
**Quartermaster:** S1: ms-06 "One night is one hundred twenty dollars." HEAR (Example). Gap: Nancy's own ask ("One room, please.").
**Quartermaster:** S2: ms-03 "Welcome to our hotel." staff voice in a say-it card, does not fit a guest. sw-02 "Please wait here." HEAR. cs-04 "a long line" vocab. ph-04 "desk" vocab. sw-03 "Can I help you?" staff voice (sight words zone).
**Quartermaster:** S3: ms-28 "Your room is ready." staff voice in a say-it card (Maxwell accepted t642u). sw-01 "Here is your card." HEAR. nm-01 "Room thirteen." HEAR. nm-02 "Fourth floor." HEAR.
**Quartermaster:** S4: Gap: nothing Nancy says. Vocab: ph-05 towel, cs-03 a white towel, cs-01 a white blanket, ph-03 bed.
**Quartermaster:** S5: ms-05 "Breakfast is at seven thirty." HEAR (Example).
**Quartermaster:** S6: ms-04 "Check-out is at eleven." HEAR (Example). nm-03 "Cash or card?" HEAR. nm-04 "Here is your change." HEAR.
**Quartermaster:** How order works in play: card order is computed, not file order (spec :223: easy opener, review cards, written personal cards, then fewest-words never-seen, then seen longest ago). Hotel cards sit in several zones (ph, cs, nm, sw and ms, so 5), so only the Maxwell Says ones can share a run. Spec :227 already puts ms-03 to ms-06 and ms-21 to ms-23 in the front-desk scene. Renumbering ids would break needsMaxwell, outings (ms-05) and spec refs, so the plan adds one spec sentence instead.
**Quartermaster:** ## 3) Options
**Quartermaster:** 1A (minimal, wording unchanged): append to spec :363 "Hotel cards in one run keep stay order: `ms-06`, `ms-03`, `ms-28`, `ms-05`, `ms-04`." No card changes.
**Quartermaster:** 1B (guest side, 3 cards): same order rule plus ms-33; ms-03 and ms-06 reworded; ms-33 added. ms-04, ms-05, ms-28 unchanged (HEAR cards). Pics unchanged, so no new art.
**Quartermaster:** 1B ms-03 SAY: "I have a reservation." / ฉันจองห้องไว้ค่ะ [NEEDS NANCY, Instructor review] / ai HAV uh rez-er-VAY-shun / syl res·er·va·tion (hard-word tier rule) / 4 words, say-it.
**Quartermaster:** 1B ms-06 HEAR: "One hundred twenty dollars a night." / Thai unchanged คืนละ 120 ดอลลาร์ค่ะ / WUN HUN-dred TWEN-tee DOL-erz uh NAIT / 6 words, so the ms-06 7-word exception is dropped from :364 / choices: One hundred twelve / Two hundred twenty / One hundred twenty / One hundred dollars a night. / trap "One hundred twelve dollars a night." (twelve vs twenty), trapNote unchanged / pic svg:money-120 unchanged / hint O__ h______ t_____ d______ a n____. Example tag and fill kept.
**Quartermaster:** 1B ms-33 SAY (new, S4): "I need more towels." / ขอผ้าเช็ดตัวเพิ่มค่ะ [NEEDS NANCY, Instructor review] / ai NEED mor TOW-ulz / 4 words, say-it, personal. Counts updated: meta totalCards/writtenCards 211 to 212, sayIt 37 to 38, personal 80 to 81; spec :236 74 to 75, :350 211 to 212, :362 80 to 81, :375 "206 of the 212".
**Quartermaster:** ## 4) Char cost (Python len, cap 188,200)
**Quartermaster:** 1A: +85, total 188,092, bank 108.
**Quartermaster:** 1B: +185, total 188,192, bank 8. Pieces: order rule +94, ms-06 -39, :364 -13, ms-03 +9, ms-33 +134.
**Quartermaster:** Too tight? Trims: drop the backticks in the order rule (-12), drop ms-03 syl (-25), or skip ms-33 (1B without ms-33: +51, bank 142).
**Quartermaster:** ## 5) Built candidates (copies, NOT gated)
**Quartermaster:** 1A: 1A/nancys-adventure-english-v6-08-1B-v32-hotel1A-PASTE.md 322fb1207fdc0d282d2a5795db636028; diff 78aa971b; p-diff b496e6ee.
**Quartermaster:** 1B: 1B/nancys-adventure-english-v6-08-1B-v32-hotel1B-PASTE.md 7c178da0280285de147569e7f094398e; diff 97704401; p-diff 19bdd9c5.
**Quartermaster:** Tools: build.py 3cec4953, selfcheck.py 0617c7ee (rc 0).
**Quartermaster:** Self-check, both: line 427 parses as JSON; 428 lines like the source; ids unique; meta counts match cards; verses, jesusWords, jesusWordsFallback and boss scrolls equal to the source; no other top-level key changed; no inn name, email or phone pattern.
**Quartermaster:** 1A changes only :363. 1B changes :236 :350 :362 :363 :364 :375 :427; changed cards ms-03, ms-06, ms-33 only; ms-06 has 4 unique choices with answer and trap in them and a valid hint.
**Quartermaster:** NOT run: checks_v608.py, text_check or any 320 render (UNVERIFIED). The 1B count edits may trip check lines that pin 211 or 80.
**Quartermaster:** ## Open questions for Maxwell (one asker, via QM and the ledger)
**Quartermaster:** Q1 Spec :18 still says "her hotel work", and Instructor's DRAFT convention calls ms-03 to ms-06 Nancy's lines at the desk. Keep :18 (her real life) or reword it to guest-side? Not changed here.
**Quartermaster:** Q2 ms-04/05/06 numbers (11:00, 7:30, $120) stay Example placeholders. Keep them as examples, or does he have real ones?
**Quartermaster:** Q3 ms-28 "Your room is ready." is a staff line in a say-it card. Keep it (t642u), or swap it for a line Nancy says, like "Where is my room?"
**Quartermaster:** Q4 1A or 1B, and if 1B, with or without ms-33. Should ms-33 join needsMaxwell (not added; costs chars and count edits)?
**Quartermaster:** Q5 sw-03 "Can I help you?" is staff voice too, but it's outside the hotel set and left alone.
**Quartermaster:** Based on: snap-r2h-0021MDT, pointer f6dac2d0, PASTE 317e91ce
**Quartermaster:** Ready to paste: none yet. CURRENT stays v5-37, `nancys-adventure-english-v5-37-PASTE.md` (acc534a51a922102ee37844e04d17955)
