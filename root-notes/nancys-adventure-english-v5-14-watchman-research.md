# Watchman research for v5-14: recommended fixes (Oct 30, 2026)

Already in the spec, so no change: free hints, missed cards return 3-5 cards later, streak never resets, no Sound Duel timers, 5-minute active-play rest, one new thing per level, pause on background, big targets, XP never drops, picture-first cards.

1a Spaced review: give each card a box (0-4) and a dueDate. A right answer moves it up a box; a miss resets it to box 1, quietly. Gaps: box 1 = 1 day, 2 = 3 days, 3 = 7 days, 4 = 14 days. Run order: easy opener, then personal cards, then up to 3 due cards (most overdue first), then new cards. Never show "overdue". Source: Kang 2016 https://www.teachinghowtolearn.veritytest.com.au/verity/uploads/2021/08/Policy-Insights-from-the-Behavioral-and-Brain-Sciences-2016-Kang-12-9.pdf
1b Mixing zones: after level 6, 2 of every 10 cards in a non-boss run come from her other open zones, chosen from due cards. Source: Kang 2016.
1c Sound Duel voices: rotate up to 4 English voices from speechSynthesis.getVoices(), changing on each pair. Replay uses the same voice. Maxwell's recordings count as one voice. Source: https://doi.org/10.1017/s0272263125100879
1d Sound Duel answers are word tiles with the respelling (light / LAIT), not pictures. Source: same meta-analysis (word choices g 0.90-1.03 vs image choices 0.47).
1e Add 6 word-ending pairs (trap "final consonant"): fine/file, mine/mile, leave/leaf, save/safe, rice/right, bus/but. Sources: http://sutir.sut.ac.th:8080/jspui/bitstream/123456789/1234/1/warisara_fulltext.pdf https://so05.tci-thaijo.org/index.php/tgt/article/view/273223
2a maxNewPerRun = 3 until Feb 1, 2027, then 5. Sources: https://www.mja.com.au/journal/2018/208/1/cognitive-impairment-during-pregnancy-meta-analysis https://pubmed.ncbi.nlm.nih.gov/21409694/
2b Resume: when she comes back, show the same card again with the pips, "Card 4 of 10" / "การ์ดที่ 4 จาก 10", and a big gold arrow on Continue. Replay the audio after she taps it. Source: https://escholarship.org/content/qt18b4r661/qt18b4r661.pdf
2c Reach: Got it is full-width minus the HELP gap, at least 64pt tall, centered in the bottom third. Continue, Keep going and Close go in the same spot. The map's next-run button is 96pt bottom-right, with HELP bottom-left and the gear top-right. No diagonal reach to the top corner is needed in any flow. Source: http://www.cs.umd.edu/hcil/trs/2006-02/2006-02.pdf
2d No push notifications, badges, or reminder prompts in v1. Source: https://developer.apple.com/design/human-interface-guidelines/notifications.md
3a Red dot: Shop, Scrolls and Talents each get one dot, only when there's real news (something affordable, an unread scroll, an unspent talent point). It clears when she opens the screen. No counts, and at most 2 dots at once. Source: https://supercell.com/en/games/clashofclans/blog/news/weve-revamped-the-clash-of-clans-user-interface/
3b Tapping a locked gate shows a 2-second parchment: "Opens at Level 6. You're doing great!" / "เปิดที่เลเวล 6 เก่งมาก!" (Thai marked NEEDS NANCY). Then the arrow points back to her next step.
3c First Shop visit: highlight only the cheapest item she can afford (a 10-gem cape). Arrow to the item, then Buy, then Wearing, then the whole shop unlocks. Source: https://www.supercheats.com/clash-of-clans/walkthrough/tutorial
3d Never list: no real-time timers, no energy or lives, no withering, no limited or rotating stock, no "one-time offer", no pay-to-skip, no leaderboards. Source: https://diva-portal.org/smash/get/diva2:1043332/FULLTEXT01.pdf

Note: no Thai-specific study compares picture cues with translation cues. General research supports picture plus Thai, which the cards already use.
Note: FINAL.md was being edited during this review (line 19 changed from "The WoW skin" to "The game skin").
Maxwell decides: nothing is a true 50/50. Default new-word cap is 3 (gentler); 5 would mean faster progress.

---
# v5-20 Conversations category: Watchman review (Oct 30, 2026, 4:30 PM MT)
Source of the design: build-history.md, 4:28 PM entry, item 2 (a single line; there's no full spec yet). Research basis: /workspace/nancy-phrasebook-research-note.md (R1.x, R3.x).

C1 One scenario is one run. Each scenario has at most 10 player turns, and each turn fills one pip, so the run fits the existing 10-pip run and the 5-minute rest. Limits: at most 12 nodes, at most 3 choices per node (2 forward plus 1 grace), and every branch rejoins a gather node within 2 steps (note R3.2, Ink weave).
C2 Use the node schema in note R3.1: {id, speaker, en, th, picture, choices:[{en, th, next | grace}]}. A choice has either next or grace, never both. A node with no choices auto-advances after its audio.
C3 Grace redirect (note R1.4/R3.4): the other speaker says "Oh, did you mean…?" and the node replays with the grace choice dimmed to 40%. After 2 grace picks the right choice glows gold. No red X, no XP loss, no damage.
C4 Every line is a usable chunk of at most 8 words with a chunkId. Reuse chunks across scenarios. Design judgment, not sourced: put one repair chunk in all three scenarios, "Sorry, can you say that slowly?", because it's the phrase she'll use most in real life.
C5 Scenario contents for the launch, with no emergency features (the game rule stands):
   - Grocery checkout: greeting, "Paper or plastic?", card or cash, "Do you need a receipt?", thank you.
   - Clinic check-in: name, "I have an appointment at 2," handing over her insurance card, "Can I have a Thai interpreter, please?" The interpreter line is a request, not an emergency, so it fits the rule. Federal rule 45 CFR 92.201 makes the interpreter free.
   - Asking for help in a store: "Excuse me, where is the…?", "Do you have this in…?", the repair chunk.
   Keep labor and medical content in Baby-and-Hospital so the two don't overlap.
C6 Turn format default (still Maxwell's 50/50 from the note; act-don't-ask default applied): she hears the English line, taps the reply tile (English, with the Thai underneath and a picture), then says it aloud on the honor system. No voice recognition.
C7 Every node picture must pass Maxwell's at-a-glance rule from the 4:22 PM flag. One object per node, nothing abstract.
C8 Resume: save {scenarioId, nodeId, graceCount} to IndexedDB after every node. An interruption resumes on the same node, the same as auto-pause.
C9 Validator: window.__test() prints PASS only if every node is reachable, every path ends within 10 turns, there are no dead ends, no choice has both next and grace, and the node and choice limits hold.
C10 Spacing for launch: chunks she missed come back as a short replay in her next session. The scenario-level due boxes (note R1.2) move to v6, matching Chancellor's deferral of spaced boxes.

Gaps for Quartermaster and Chancellor (not my call):
G1 The Map grid is already full at 2x4 (spec line 136, 8 tiles). A fourth category needs a tile slot or a grid change.
G2 Unlock level: rule 4 allows one new feature per level. Conversations needs its own level (suggestion: 6, moving the zone opening) or it breaks the rule.
G3 Thai review load: about 3 scenarios x up to 12 nodes is roughly 36 new Thai lines, all marked NEEDS NANCY, on top of the hospital review due Nov 7. That needs a scope check against the Nov 10 paste and the Dec 10 freeze.

STATUS (4:31 PM MT, Oct 30): Chancellor's scope call moves the Conversations category to v6, after the freeze. Items C1-C10 and G1-G3 above are now v6 input, and Quartermaster is keeping the drafts in /workspace/v6-addons.md.

V6 CALLS (Chancellor, 4:32 PM MT, Oct 30):
G1 Conversations takes the Scrolls tile, and Scrolls moves into My Stuff. The grid stays at 8 tiles.
G2 Conversations opens at level 6, the same level as Colors, so it lands as a reward and not as homework.
G3 The roughly 36 Thai lines get reviewed in January at the earliest, after the baby comes, and stay out of the Nov 7 review.

## LEAF SAYINGS OPTION TWO (Oct 30, 5 PM MT)

Research only (Watchman). Quartermaster builds, Auditor verifies, Instructor and Nancy own the Thai. Maxwell's call: whole short verses only, no excerpts, no excerpt labels, John 10:11 complete, 6 sayings max, ESV (bible.com 59) and THSV11 (bible.com 174). All are free gifts: no cost, never bought, no "unlock" wording.

Live check: I fetched all 10 candidates from bible.com at 5:02 PM MT. ESV and THSV11 were each pulled from the verse page, and the page text matched the page's own data exactly. Raw pages and results are in `v520/jw/opt2/` (`live.json`). Quartermaster's in-progress `v520/jw/leaf6.json` matches live text exactly for all 6 of its refs.

State found at 5:03 PM MT: Quartermaster is already rebuilding item 8 in `v520/build_cards.py` lines 106-125. That build has 6 whole verses: John 15:9 and Luke 12:7 at start, then John 14:27, John 10:11, John 8:12 and John 15:11 with 4 gear gifts. No excerpt is left in that build. The line numbers below are as of 5:03 PM MT and will shift while he works, so match on the quoted text.

### Test for each candidate (whole verse, about 25 ESV words or fewer, Jesus speaking, comforting, readable)

John 10:11, 15 words: passes, and it is complete. "I am the good shepherd. The good shepherd lays down his life for the sheep."

John 15:9, 15 words: passes.

Luke 12:7, 20 words: passes, and "Fear not" is in the whole verse.

John 14:1, 13 words: passes. It has an opening quote mark that is never closed (in both ESV and THSV11), so keep it as printed.

John 14:18, 12 words: passes (reserve). Orphan opening mark, keep as printed.

Luke 12:32, 16 words: passes (reserve). Orphan opening mark.

John 15:11, 21 words: passes. No quote marks.

John 8:12, 28 words: slightly over the guide, but kept because Maxwell asked for its gloss to be restored. The words of Jesus are 20 of the 28. It includes the narrator ("Again Jesus spoke to them, saying,") and quote marks, so it is NOT whole-verse speech: keep the marks exactly as printed.

John 14:27, 32 words: fails the length guide (it is two long sentences). Drop it.

Matthew 11:29, 25 words: borderline, and "yoke" is hard for her. Leave it out.

Mark 5:36, Mark 6:50, Matthew 28:20: the old excerpts. Their whole verses are narration or start mid-sentence, so they fail.

Quote marks: none of the 6 picks is whole speech with marks, so nothing gets stripped. All are shown exactly as printed, under the existing rule at spec line 289 ("never add or remove a quote mark").

### The 6 picks (6 qualify, so no affirmations are needed)

1. John 15:9 (start gift)
ESV: As the Father has loved me, so have I loved you. Abide in my love.
THSV11: พระบิดาทรงรักเราอย่างไร เราก็รักพวกท่านอย่างนั้น จงติดสนิทอยู่กับความรักของเรา
Gloss (restores "as the Father loved me"): พระบิดารักพระเยซูอย่างไร พระเยซูก็รักคุณอย่างนั้น อยู่ในความรักของพระองค์นะ
thGlossStatus: NEEDS NANCY

2. Luke 12:7 (start gift)
ESV: Why, even the hairs of your head are all numbered. Fear not; you are of more value than many sparrows.
THSV11: ถึงผมของพวกท่านก็ทรงนับไว้แล้วทุกเส้น อย่ากลัวเลย ท่านก็มีค่ามากกว่านกกระจาบหลายตัว
Gloss (restores the counted hairs, "Fear not" and the sparrows): พระเจ้านับเส้นผมของคุณไว้ทุกเส้น ไม่ต้องกลัว คุณมีค่ามากกว่านกตัวเล็กๆ หลายตัว
thGlossStatus: NEEDS NANCY

3. John 14:1 (replaces John 14:27; gear gift sling-shepherd)
ESV: “Let not your hearts be troubled. Believe in God; believe also in me.
THSV11: “อย่าให้ใจของพวกท่านเป็นทุกข์เลย พวกท่านวางใจในพระเจ้า จงวางใจในเราด้วย
Gloss: ไม่ต้องกังวลใจ วางใจในพระเจ้า และวางใจในพระเยซูด้วย
thGlossStatus: NEEDS NANCY
Note: the opening quote mark has no closing mark. It is kept as printed under the spec rule (never add or remove a quote mark). Whether to keep the marks on John 3:16, Joshua 1:9 and 1 Samuel 17:45 is still Maxwell's open call.

4. John 10:11, complete (gear gift staff-shepherd)
ESV: I am the good shepherd. The good shepherd lays down his life for the sheep.
THSV11: เราเป็นผู้เลี้ยงที่ดี ผู้เลี้ยงที่ดีย่อมสละชีวิตของตนเพื่อฝูงแกะ
Gloss: keep Instructor's line, which already covers both halves: พระเยซูดูแลคุณเหมือนคนเลี้ยงแกะ และยอมตายเพื่อคุณ
thGlossStatus: NEEDS NANCY

5. John 8:12 (gear gift staff-lantern)
ESV: Again Jesus spoke to them, saying, “I am the light of the world. Whoever follows me will not walk in darkness, but will have the light of life.”
THSV11: พระเยซูตรัสกับพวกเขาอีกครั้งหนึ่งว่า “เราเป็นความสว่างของโลก คนที่ตามเรามาจะไม่ต้องเดินในความมืด แต่จะมีความสว่างแห่งชีวิต”
Gloss (keeps "of the world", the condition, and "but will have the light of life"): พระเยซูเป็นแสงสว่างของโลก ใครตามพระองค์จะไม่เดินในความมืด แต่จะมีแสงสว่างแห่งชีวิต
thGlossStatus: NEEDS NANCY

6. John 15:11 (gear gift hammer-builder)
ESV: These things I have spoken to you, that my joy may be in you, and that your joy may be full.
THSV11: เราบอกสิ่งเหล่านี้กับพวกท่านแล้ว เพื่อให้ความยินดีของเราอยู่ในท่าน และให้ความยินดีของท่านเต็มเปี่ยม
Gloss (restores "my joy in you"): พระเยซูอยากให้ความสุขของพระองค์อยู่ในใจคุณ และให้คุณมีความสุขเต็มหัวใจ
thGlossStatus: NEEDS NANCY

Reserves, not used, live-checked at 5:02 PM MT:

John 14:18: “I will not leave you as orphans; I will come to you. / “เราจะไม่ละทิ้งพวกท่านไว้ให้เป็นลูกกำพร้า เราจะมาหาท่าน / gloss พระเยซูจะไม่ทิ้งคุณไว้คนเดียว พระองค์จะมาหาคุณ (NEEDS NANCY)

Luke 12:32: “Fear not, little flock, for it is your Father’s good pleasure to give you the kingdom. / “ฝูงแกะเล็กน้อยเอ๋ย อย่ากลัวเลย เพราะว่าพระบิดาของพวกท่านชอบพระทัยจะประทานแผ่นดินนั้นให้แก่ท่าน

Reserve affirmations, not scripture, only if a verse is ever dropped (all thStatus NEEDS NANCY):

"You are loved because God is good, not because you did well." / คุณเป็นที่รัก เพราะพระเจ้าดี ไม่ใช่เพราะคุณทำเก่ง

"Grace is a gift. You never have to earn it." / พระคุณเป็นของขวัญ คุณไม่ต้องทำอะไรเพื่อให้ได้มา

### Fix list for Quartermaster (line numbers as of 5:03 PM MT)

1. `v520/build_cards.py` line 110: change the John 14:27 row to John 14:1, with the same gear gift. Old: `('John 14:27',{'type':'gear','id':'sling-shepherd'},'พระเยซูให้สันติสุขกับคุณ ไม่ต้องกังวล ไม่ต้องกลัว','Quartermaster draft'),` New: `('John 14:1',{'type':'gear','id':'sling-shepherd'},'ไม่ต้องกังวลใจ วางใจในพระเจ้า และวางใจในพระเยซูด้วย','Watchman draft'),` Also add John 14:1 to `leaf6.json`; the live text is in `v520/jw/opt2/live.json`.

2. `v520/build_cards.py` line 108, John 15:9 gloss. Old: `พระเยซูรักคุณมาก อยู่ในความรักนั้นนะ` New: `พระบิดารักพระเยซูอย่างไร พระเยซูก็รักคุณอย่างนั้น อยู่ในความรักของพระองค์นะ`

3. `v520/build_cards.py` line 109, Luke 12:7 gloss. Old: `ไม่ต้องกลัว คุณมีค่ามากสำหรับพระเจ้า` New: `พระเจ้านับเส้นผมของคุณไว้ทุกเส้น ไม่ต้องกลัว คุณมีค่ามากกว่านกตัวเล็กๆ หลายตัว`

4. `v520/build_cards.py` line 111, John 10:11: no change. The verse is complete and the gloss is Instructor's full line.

5. `v520/build_cards.py` line 112, John 8:12 gloss. Old: `พระเยซูเป็นแสงสว่าง คนที่ตามพระองค์จะไม่อยู่ในความมืด` New: `พระเยซูเป็นแสงสว่างของโลก ใครตามพระองค์จะไม่เดินในความมืด แต่จะมีแสงสว่างแห่งชีวิต`

6. `v520/build_cards.py` line 113, John 15:11 gloss. Old: `พระเยซูอยากให้คุณมีความสุขเต็มหัวใจ` New: `พระเยซูอยากให้ความสุขของพระองค์อยู่ในใจคุณ และให้คุณมีความสุขเต็มหัวใจ`

7. Optional, your call: `v520/build_cards.py` lines 122-123 (`uiText.jesusAllHeard` and `jesusAllHeardFull`) call these "affirmations". They are Jesus' words, and affirmations are now a separate filler category. A possible English line: "You've heard all of Jesus' words for now." The Thai would be Instructor's to write, marked NEEDS NANCY.

8. Spec `nancys-adventure-english-v5-20.md` line 196 / FINAL line 205, built from `v520/build_spec.py` line 38. Old: "She has the 2 with `given.type: "start"` plus one per boss win, up to 7." New: "She has the 2 with `given.type: "start"` plus one with each of 4 gear gifts (`given.type: "gear"`), up to 6."

9. Spec line 290 / FINAL line 299, built from `build_spec.py` line 57. Old: "(`jesusWords`, 7; ..." New: "(`jesusWords`, 6; ...". Keep "full verses". Add: "Quote marks stay exactly as printed (John 14:1's opening mark; John 8:12's narrator words and marks). No excerpt labels."

10. Spec line 289 / FINAL line 298, the quote-mark rule. Under Option Two no leaf excerpt sentence is needed, and there is none in the current v5-20 files, so there is nothing to remove. Do not add the old line-283 sentence ("Leaf sayings are excerpts; quote marks at the cuts are removed"). Leave the rule unscoped: "never add or remove a quote mark" now covers the 16 verses and the 6 Jesus words.

11. Spec line 317 / FINAL line 326, built from `build_spec.py` line 65. Old: "the 7 Jesus-word `thGloss`" New: "the 6 Jesus-word `thGloss`"

12. FINAL line 6, built from `build_spec.py` line 83. Old: "The 16 Bible verses and 7 Jesus words" New: "The 16 Bible verses and 6 Jesus words"

13. `v520/checks.py` line 41. Old: '`jesusWords`, 7' New: '`jesusWords`, 6'

14. Cards: `nancys-adventure-english-v5-20-cards.json` is regenerated by `build_cards.py`, so edit the script rather than the JSON. After the rebuild, `meta.jesusWords` must be 6, `meta.notes.jesusWords` must say 6 whole verses, and no entry may have "excerpt", cost, price or unlock wording.

15. Instructor's files (Instructor's to change, not Quartermaster's): `v520/instructor-thai-check.md` lines 3-4 still say "Leaf sayings: all 8 verified / These are exact excerpts...", and the table at lines 11-18 still lists the 8 old refs. `thai-corrections-log.md` line 71 still points to `v520/jw/picks.json`, the old 8-excerpt file, which should now count as superseded.

### Not confirmed live

The fit of the Thai glosses. They are my drafts, NEEDS NANCY, and need Instructor's review.

Whether 2 start gifts plus 4 gear gifts is the final schedule. I took it from Quartermaster's in-progress build; it is not a decision of mine.

Auditor has not yet verified the John 14:1 swap.
