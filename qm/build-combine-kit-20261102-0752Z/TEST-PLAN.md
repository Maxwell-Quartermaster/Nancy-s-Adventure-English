**Quartermaster:** TEST PLAN: Maxwell's one-time two-file test with Build, after the Nov 10 paste. Draft only, and nothing runs until Maxwell says go.
**Quartermaster:** Owner's words (t665u): "Build app can invoke you while he's building. Keep this in mind and prepare the work for it. This should solve the gap when he summons you. If you can't communicate, leave something for him to help him combine the text for the game."
**Quartermaster:** Goal: prove that Build, given the prompt as two parts plus COMBINE-GUIDE.md, generates the same game as the single paste.
**Quartermaster:**
**Quartermaster:** **Before the test** (Quartermaster):
**Quartermaster:** 1. Use the PASTE frozen as the pointer after Nov 10. Re-run `tools/make_kit.py` and `tools/write_docs.py` with SRC pointed at it, re-prove the round trip (cat gives the source md5, cmp exit 0), and refresh MD5SUMS. Never test with a kit built on an older PASTE.
**Quartermaster:** 2. Auditor re-hashes every kit file against MD5SUMS and confirms the round trip before Maxwell pastes.
**Quartermaster:** 3. Run it in a new, throwaway Build project. It must never replace the live game or the Nov 10 build.
**Quartermaster:**
**Quartermaster:** **Paste steps** (Maxwell, about 10 minutes):
**Quartermaster:** 1. Message 1: attach or paste `COMBINE-GUIDE.md` with one line: "Two-part prompt coming. Read this guide first and don't start building until Part 2 arrives."
**Quartermaster:** 2. Message 2: paste `part1-with-header.md`.
**Quartermaster:** 3. Message 3: paste `part2-with-header.md`, and attach the same `nancys-adventure-english-v6-08-title.svg` and `nancys-adventure-english-v6-08-daily-verses.json` as the single-paste build.
**Quartermaster:** 4. Message 4: "Join Part 1 + Part 2 as COMBINE-GUIDE section 3 says, run its section 4 join checks and tell me the results, then build in the four stages and run SELF-CHECK.md." Attach `SELF-CHECK.md`.
**Quartermaster:** 5. If Build asks a question, Maxwell forwards it to Quartermaster, or Build invokes Quartermaster directly. Quartermaster answers only from the kit and the PASTE, and the answer gets logged.
**Quartermaster:** 6. Maxwell drops the generated files (index.html, JS, CSS, cards.json, sw.js, manifest.json) into /workspace or the Council thread.
**Quartermaster:**
**Quartermaster:** **Auditor compares the generated game to the spec:**
**Quartermaster:** - A. `cards.json` byte-identical to the JSON line: the md5 from COMBINE-GUIDE section 1 (or the same md5 with one trailing newline).
**Quartermaster:** - B. Every SELF-CHECK.md row (A1-E3) holds, with numbers recomputed from the generated files, not taken from Build's report.
**Quartermaster:** - C. Spec-vs-code: Auditor's usual post-paste check against the joined spec. Every COMBINE-GUIDE section 7 cross-reference has to be used in code, especially `needsMaxwell`, `meta.outings`, the zone prefixes `fd cv`, all 98 `uiText` keys including bonus*2, and `picPlan.*InlineSvg` inlined exactly.
**Quartermaster:** - D. Diff against the single-paste build: the same cards.json, the same list of uiText keys used, and the same four stage tests printing PASS. Code doesn't have to match line for line, but behavior and data do.
**Quartermaster:** - E. Play-flow walk plus the 320 × 568 render, the same gates as a normal paste. No `<!-- Part N of 2` text ships.
**Quartermaster:**
**Quartermaster:** **Pass:** A, B, C and E all pass, and D shows no data or behavior difference. The split becomes an approved paste method, so Quartermaster can use two files for the location work once Maxwell says yes.
**Quartermaster:** **Fail:** Auditor names the exact missed link, with its file and line. Quartermaster adds it to COMBINE-GUIDE, and the test runs once more. Until a pass, the default stays one paste whenever it fits.
**Quartermaster:** Based on: snap-r2h-0021MDT, pointer f6dac2d0, PASTE 317e91ce (CURRENT-SNAP). The kit draft is on 5e1666fe.
**Quartermaster:** Ready to paste: none. CURRENT stays v5-37.
