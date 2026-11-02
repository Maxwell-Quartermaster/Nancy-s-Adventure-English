**Watchman:** # Practice card sets: README
**Watchman:** PRACTICE ONLY. This is not game content. Nothing here is applied to the game or the PASTE.
**Watchman:** INSTRUCTOR FLAG: ALL Thai in these files (every "th" and every Thai "trapNote") is UNREVIEWED and needs Instructor review before any use.
**Watchman:** INSTRUCTOR FLAG: every "respell" is UNREVIEWED and needs Instructor review too.
**Watchman:** Made by Watchman on Monday Nov 2, 2026 (Mountain time), from Maxwell t655u via Quartermaster.
**Watchman:** Based on: snap-r2h-0021MDT, pointer f6dac2d0, PASTE 317e91ce
**Watchman:** Files: clinic.json (9), hospital.json (9), grocery.json (8), cooking.json (9), eating.json (9), home-day.json (10). Total 54 cards.
**Watchman:** Card shape copied from cards.json in nancys-adventure-english-v6-08-1B-v32-cards1A-fix-PASTE.md line 427: id, en, th, respell, choices (4), trap, trapNote, hint, type, personal, pic.
**Watchman:** Each file wraps its cards as {"practiceOnly": true, "location": "...", "cards": [...]}. That wrapper is not part of the game format.
**Watchman:** Ids are placeholders (prac-<location>-NN). They follow the step order in ../RESEARCH.md.
**Watchman:** type: "say-it" for Nancy's SAY lines, "picture" for single things with a clear emoji. HEAR lines have no cards, because only say-it and picture were allowed. The game's "server-talk" type would fit them if Maxwell wants that later.
**Watchman:** pic: emoji on picture cards, null on say-it cards (same as existing say-it cards, which have no pic).
**Watchman:** hint: a letter string for one-word cards, and [pattern, letters, key word] for phrases, same as the game.
**Watchman:** personal is set true on all cards. That is a guess, so please check it.
**Watchman:** Thai particle: statements end in ค่ะ. Questions end in คะ, as existing game cards do ("ห้องคลอดอยู่ที่ไหนคะ"). Soft requests end in นะคะ (cooking-02, cooking-06, eating-02, eating-06, home-day-09, hospital-08). Instructor should confirm these.
**Watchman:** Generator scripts are in ../tools/ (build_research.py, build_cards.py). Re-running them overwrites these files.
