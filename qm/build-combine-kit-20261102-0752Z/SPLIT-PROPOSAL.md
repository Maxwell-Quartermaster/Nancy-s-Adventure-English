**Quartermaster:** SPLIT PROPOSAL, draft only. The source is the candidate PASTE `nancys-adventure-english-v6-08-1B-v32-cards1A-fix-PASTE.md`, md5 5e1666fe6f7189d3886686749335b3ee: 188,007 chars, 213,241 bytes, 428 lines. I re-hashed it this turn.
**Quartermaster:** Why this source: /workspace/qm/hotel1B-story-20261102-0748/ has no GATE-REQUEST yet, so per the brief the kit is built on 5e1666fe. Once the hotel1B+story build is gated, re-run `tools/make_kit.py` with SRC pointed at it, then `tools/write_docs.py`. The cut rule stays the same: Part 2 starts at the `## CARD FILE` line.
**Quartermaster:**
**Quartermaster:** **Cut point:** before source line 420, `## CARD FILE`. Part 1 ends at line 419, after section 20, the `---` rule and one blank line.
**Quartermaster:** - Part 1 = lines 1-419: the full spec, including HOW TO USE and §0-§20. **83,727 chars**, 83,938 bytes, md5 2f96ecf10e6a3e5f426dd7408862e002 (`part1.md`).
**Quartermaster:** - Part 2 = lines 420-428: the CARD FILE authority paragraph ("the card file wins"), the `## cards.json` heading, the ```json fence, the JSON on line 427 and the closing fence. **104,280 chars**, 129,303 bytes, md5 e2f7ece8019c401c7fded8108a33ab65 (`part2.md`).
**Quartermaster:** - Both parts are under ~120k chars. Part 1 has 36,273 chars of headroom and Part 2 has 15,720.
**Quartermaster:** Why there: it's the only clean boundary that keeps the JSON whole. Line 427 alone is 103,870 chars, so no clean cut can make Part 2 smaller than that. The "card file wins" paragraph also travels with the data it governs.
**Quartermaster:**
**Quartermaster:** **Round-trip proof** (this turn, `tmp/roundtrip.txt`):
**Quartermaster:** - `cat part1.md part2.md | md5sum` gives 5e1666fe6f7189d3886686749335b3ee, the same as the source. `cmp` against the source reports identical, exit 0.
**Quartermaster:** - The header variants with their first line stripped (`tail -n +2` on each, then joined) give 5e1666fe6f7189d3886686749335b3ee. `cmp` reports identical, exit 0.
**Quartermaster:** - The source PASTE was only read, never edited. Its md5 is unchanged after the build.
**Quartermaster:**
**Quartermaster:** **Header variants**, kept out of the md5 proof:
**Quartermaster:** - `part1-with-header.md` adds 1 line, +111 chars: `<!-- Part 1 of 2 (spec, source lines 1-419). Read COMBINE-GUIDE.md first; delete this line before joining. -->`. That gives 83,838 chars, md5 d4c296f9ca9c842100115e758bfbc4ac.
**Quartermaster:** - `part2-with-header.md` adds 1 line, +147 chars: `<!-- Part 2 of 2 (card file, source lines 420-428; cards.json is the JSON line). Read COMBINE-GUIDE.md first; delete this line before joining. -->`. That gives 104,427 chars, md5 31c0fc31d697786a39e4c914bf68fbba.
**Quartermaster:** - The two headers cost 258 chars in total. That counts against each paste's prompt size, not against the 188,200 joined ceiling, because Build deletes them before joining.
**Quartermaster:**
**Quartermaster:** **Limits and risks:**
**Quartermaster:** - If the JSON line ever grows past about 120k chars, two clean parts stop being possible. The next cut would have to split the JSON itself, for example by moving `picPlan` (~20k) into its own file. That changes the file structure and needs Maxwell's yes, so I'm not proposing it now.
**Quartermaster:** - The two attached files, title.svg and daily-verses.json, stay separate, exactly as they are today.
**Quartermaster:** - The split has never been tested with Build. See TEST-PLAN.md.
**Quartermaster:** Based on: snap-r2h-0021MDT, pointer f6dac2d0, PASTE 317e91ce (CURRENT-SNAP). The kit source is 5e1666fe, which isn't frozen as the pointer yet.
**Quartermaster:** Ready to paste: none. CURRENT stays v5-37.
