**Quartermaster:** I wrote this guide for Build. It is a draft kit for a two-part paste of Nancy's Adventure English, made from PASTE 5e1666fe on 2026-11-02 (UTC 07:52).

# COMBINE GUIDE — for Build

**If you can reach Quartermaster, ask. Otherwise follow this guide.**

You have been given the game prompt in two parts because it is long. Join them back into one document, then build from the joined document exactly as if it had come as one paste. Nothing in the game changes because of the split.

## 1. What the two parts are

| Part | What it holds | Source lines | Characters | Bytes (UTF-8) | md5 (no header) |
|---|---|---|---|---|---|
| Part 1 (`part1.md`) | The full spec: HOW TO USE, sections 0 to 20 | 1-419 | 83,727 | 83,938 | `2f96ecf10e6a3e5f426dd7408862e002` |
| Part 2 (`part2.md`) | The CARD FILE: authority paragraph, heading, and the `cards.json` block (one JSON line, line 427) | 420-428 | 104,280 | 129,303 | `e2f7ece8019c401c7fded8108a33ab65` |
| Joined | The original single prompt | 1-428 | 188,007 | 213,241 | `5e1666fe6f7189d3886686749335b3ee` |

Also attached, as before, and **not** part of either part: `nancys-adventure-english-v6-08-title.svg` (the title picture) and `nancys-adventure-english-v6-08-daily-verses.json` (30 daily verses). Part 1 names both.

The JSON line on its own (Part 2, the line between ` ```json ` and ` ``` `): 103,870 characters, 128,893 bytes, md5 `8d209ec5d2701b4d1f77e73457dd8fcb` (with one trailing newline: `12d973cf0af5c6edc7dbbffa828bd481`), SHA-256 `0d4abf2d603a0b8ceeffac18515e2c0162b038a9657ab5f1438f768e0f0b3480`. Save it as `cards.json` exactly, byte for byte.

## 2. Read order

1. This guide.
2. Part 1 in full. Do not start coding.
3. Part 2 in full. Parse the JSON and confirm it is valid.
4. Join (section 3), then run the checks in section 4 of this guide.
5. Only then build, in the four stages of Part 1 section 19.

If the parts come with a first line that starts `<!-- Part N of 2`, that line is a label from Quartermaster. Delete it before joining. It is not part of the game.

## 3. Join into one logical spec before coding

- Joined text = Part 1 + Part 2, in that order, with nothing added or removed between them. Part 1 already ends with `---` and a blank line, and Part 2 starts at `## CARD FILE`.
- After joining, every place in Part 1 that says "this prompt", "this document", "the JSON block at the end of this prompt", "Paste this entire document" or "one paste" means the joined document. The split does not change the build order: still four stages, each printing `PASS` (section 19).
- Treat every name Part 1 gives in backticks as a pointer into Part 2. Section 5 lists all of them.
- Never build from Part 1 alone, and never treat Part 2 as optional. If Part 2 has not arrived, stop and ask for it.

## 4. Join checks (run before stage 1)

1. `cards.json` parses as JSON. It has 22 top-level keys: `version`, `rewardText`, `wrongText`, `welcomeBack`, `restScreen`, `needsMaxwell`, `zones`, `soundDuel`, `cards`, `rewardClips`, `gotItText`, `meta`, `trophies`, `trophyRules`, `picPlan`, `uiText`, `encouragement`, `verses`, `jesusWords`, `jesusWordsFallback`, `mapLayout`, `pantry`.
2. The md5 of `cards.json` is `8d209ec5d2701b4d1f77e73457dd8fcb` (or `12d973cf0af5c6edc7dbbffa828bd481` if you saved it with one trailing newline). SHA-256 without newline: `0d4abf2d603a0b8ceeffac18515e2c0162b038a9657ab5f1438f768e0f0b3480`.
3. `cards` has 211 entries with 211 unique ids, matching "**211 cards**" in Part 1 section 16 and `meta.totalCards` = 211.
4. Every name in section 5 resolves. The scan below found **0** names in Part 1 that point at a card id missing from Part 2.
5. If you can hash the joined text, it should be md5 `5e1666fe6f7189d3886686749335b3ee`. If your input box trimmed whitespace and the joined md5 differs, the build is still fine as long as checks 1 to 3 pass. Tell Quartermaster or Maxwell the md5 you got.

## 5. Rules that override

1. **The card file wins on all card content** (Part 1 line 12 and Part 2 line 422): text, Thai, respellings, answers, pictures, hints, zones, bosses, trophies, labels, verses and slots. If Part 1 and Part 2 disagree on card content, Part 2 wins.
2. **File strings win over any Thai here** (Part 1 line 358). Any Thai quoted in Part 1 is only for reference. Use the Thai in Part 2.
3. **Do not generate, write or edit Thai** (lines 6 and 361). Every Thai string is a `NEEDS NANCY` draft. Use it exactly as written.
4. **Verse text is exact** (lines 6, 344, 345, 404, 410). The 16 verses, the 6 Jesus words and `verses.attribution` must be byte-identical to the file. Never trim, capitalize, re-punctuate, or add or remove a quote mark. `\n` is a line break.
5. **Supplied art is exact** (line 147). Inline `picPlan.inlineSvg`, `picPlan.trophyInlineSvg` and `picPlan.uiInlineSvg` as given. Never redraw them.
6. **Labels come from the file** (rule 7, line 30). Never hardcode label text. Take it from `uiText` and the other string keys.
7. **No orphans** (rule 11, line 34). Every `cards.json` field and every `uiText` key gets used, and every field the spec names exists in the file. This includes the four `uiText` keys that Part 1 covers only through the pattern `uiText.bonus<word>`: `bonusHint2`, `bonusRetry2`, `bonusStar2`, `bonusStreak2`.
8. **Spec text beats any mockup** (line 52).
9. **Defaults fill absent fields** (line 352). A field missing from a card takes `meta.cardDefaults`, `meta.modeByType`, `meta.typeByZone`, `meta.cardThStatusDefault` or `meta.thStatusDefault`. A missing field is not an error when a default covers it. See the "defaulted" and "derived" tables in section 7.

## 6. If something is missing or does not match

- **Stop and ask. Never invent.** Don't invent a card, a Thai string, a verse, a key, an id or a count to make something fit.
- Ask Quartermaster if you can reach him. If not, ask Maxwell, and name the exact item, for example: "Part 1 line 371 names `ms-28` but I can't find it in Part 2."
- A missing `title.svg`: stop and ask for it. Never redraw it (line 157).
- A missing voice clip is skipped silently (lines 135 and 365). That one is by design, not an error.
- Never build from only one part. If Part 2 looks cut off, for example the JSON doesn't parse or doesn't end with `}`, ask for it to be pasted again.

## 7. Every cross-reference from Part 1 into Part 2

I produced this list by scanning every backticked name, and every card id written as plain text, in Part 1 (lines 1-426) and resolving each one against the JSON in Part 2.

**401 unique names, 711 mentions.** By kind: data key 111, uiText key 94, data path 76, card id 57, data value 21, attached file 10, trophy id 10, derived 7, svg id 6, defaulted field 4, id pattern 3, must-not-exist 2. Missing from Part 2: **0**.

Every one of them crosses the split: the rule lives in Part 1 and the data lives in Part 2.

Not listed here: 176 backticked items that are not data. They are CSS, HTML, colors, regexes, browser APIs, and runtime `state` or ledger names such as `state.hero`, `naeState` and `region:<id>`. Part 1 defines those, and you create them. There are also 49 section cross-references inside Part 1 (for example "section 10" and "(6.4)"). They stay inside Part 1 and don't cross the split.

### Zones at a glance (`zones[]`, Part 2)

| order | key | name | prefix | cards | boss |
|---|---|---|---|---|---|
| 1 | `phonics` | Phonics | `ph` | 26 | yes, 10 cards, scroll Genesis 1:1 |
| 2 | `colors-shapes` | Colors and Shapes | `cs` | 24 | yes, 10 cards, scroll Genesis 9:13 |
| 3 | `numbers` | Numbers | `nm` | 24 | yes, 10 cards, scroll John 6:9 |
| 4 | `sight-words` | Sight Words | `sw` | 24 | yes, 10 cards, scroll 1 Samuel 17:45 |
| 5 | `baby-hospital` | Baby and Hospital | `bh` | 31 | yes, 10 cards, scroll Isaiah 40:11 |
| 6 | `maxwell-says` | Maxwell Says | `ms` | 32 | none |
| 7 | `kitchen` | Nancy's Kitchen | `fd cv` | 50 | none |

Region order (`mapLayout.regions`): r1 Word Meadow = phonics, sight-words; r2 Golden Fields = colors-shapes, numbers; r3 Home Lake = maxwell-says, kitchen, baby-hospital; r4 Echo Forest = soundDuel. `startZone` = `phonics`.

### Card ids (cards[] in Part 2) (57)

| Spec names | Lives in Part 2 at | Part 1 lines | Sections |
|---|---|---|---|
| `bh-11` | cards[] id=bh-11 | 42,238 | §2 §8 |
| `ms-22` | cards[] id=ms-22 | 143 | §5 |
| `nm-04` | cards[] id=nm-04 | 143 | §5 |
| `ph-06` | cards[] id=ph-06 | 143 | §5 |
| `ph-07` | cards[] id=ph-07 | 143,226 | §5 §7.1 |
| `ph-12` | cards[] id=ph-12 | 143 | §5 |
| `ms-31` | cards[] id=ms-31 | 144,244,375,390,411 | §5 §8.1 §18 §19 |
| `ms-32` | cards[] id=ms-32 | 144,375 | §5 §18 |
| `ph-01` | cards[] id=ph-01 | 185 | §6.4 |
| `ph-03` | cards[] id=ph-03 | 185 | §6.4 |
| `ph-17` | cards[] id=ph-17 | 185,226 | §6.4 §7.1 |
| `sw-06` | cards[] id=sw-06 | 185 | §6.4 |
| `bh-12` | cards[] id=bh-12 | 226 | §7.1 |
| `cs-01` | cards[] id=cs-01 | 226 | §7.1 |
| `cs-02` | cards[] id=cs-02 | 226 | §7.1 |
| `cs-04` | cards[] id=cs-04 | 226 | §7.1 |
| `cs-08` | cards[] id=cs-08 | 226 | §7.1 |
| `cs-11` | cards[] id=cs-11 | 226 | §7.1 |
| `cs-15` | cards[] id=cs-15 | 226 | §7.1 |
| `cs-22` | cards[] id=cs-22 | 226 | §7.1 |
| `cs-23` | cards[] id=cs-23 | 226,230 | §7.1 |
| `cs-24` | cards[] id=cs-24 | 226,230 | §7.1 |
| `fd-02` | cards[] id=fd-02 | 226 | §7.1 |
| `ms-19` | cards[] id=ms-19 | 226 | §7.1 |
| `nm-02` | cards[] id=nm-02 | 226 | §7.1 |
| `nm-05` | cards[] id=nm-05 | 226 | §7.1 |
| `nm-06` | cards[] id=nm-06 | 226 | §7.1 |
| `nm-14` | cards[] id=nm-14 | 226 | §7.1 |
| `ph-02` | cards[] id=ph-02 | 226 | §7.1 |
| `ph-08` | cards[] id=ph-08 | 226 | §7.1 |
| `ph-11` | cards[] id=ph-11 | 226 | §7.1 |
| `ph-21` | cards[] id=ph-21 | 226 | §7.1 |
| `ph-24` | cards[] id=ph-24 | 226 | §7.1 |
| `sw-15` | cards[] id=sw-15 | 226 | §7.1 |
| `sw-18` | cards[] id=sw-18 | 226 | §7.1 |
| `sw-19` | cards[] id=sw-19 | 226 | §7.1 |
| `sw-24` | cards[] id=sw-24 | 226 | §7.1 |
| `ms-03` | cards[] id=ms-03 | 227 | §7.1 |
| `ms-06` | cards[] id=ms-06 | 227,363,364,371 | §7.1 §16 §17 |
| `ms-21` | cards[] id=ms-21 | 227 | §7.1 |
| `ms-23` | cards[] id=ms-23 | 227 | §7.1 |
| `fd-29` | cards[] id=fd-29 | 254 | §8.2 |
| `fd-38` | cards[] id=fd-38 | 254 | §8.2 |
| `bh-01` | cards[] id=bh-01 | 357 | §16 |
| `bh-10` | cards[] id=bh-10 | 357 | §16 |
| `ms-04` | cards[] id=ms-04 | 363,371 | §16 §17 |
| `ms-05` | cards[] id=ms-05 | 363,371 | §16 §17 |
| `bh-14` | cards[] id=bh-14 | 364 | §16 |
| `bh-30` | cards[] id=bh-30 | 369,371 | §17 |
| `ms-28` | cards[] id=ms-28 | 369,371 | §17 |
| `ms-29` | cards[] id=ms-29 | 369,371 | §17 |
| `ms-30` | cards[] id=ms-30 | 369,371 | §17 |
| `bh-31` | cards[] id=bh-31 | 375 | §18 |
| `fd-01` | cards[] id=fd-01 | 375 | §18 |
| `fd-06` | cards[] id=fd-06 | 375 | §18 |
| `ph-25` | cards[] id=ph-25 | 375 | §18 |
| `ph-26` | cards[] id=ph-26 | 375 | §18 |

### Trophy ids (trophies[]) (10)

| Spec names | Lives in Part 2 at | Part 1 lines | Sections |
|---|---|---|---|
| `frame-oak` | trophies[] id=frame-oak | 143 | §5 |
| `cleaver-bloodtide` | trophies[] id=cleaver-bloodtide | 293 | §11.1 |
| `greatsword-dragonbane` | trophies[] id=greatsword-dragonbane | 293 | §11.1 |
| `sword-iron` | trophies[] id=sword-iron | 293,295 | §11.1 |
| `sword-sunforged` | trophies[] id=sword-sunforged | 293,304 | §11.1 |
| `shield-sunrise` | trophies[] id=shield-sunrise | 299 | §11.1 |
| `sparkle` | trophies[] id=sparkle | 302 | §11.1 |
| `hammer-builder` | trophies[] id=hammer-builder | 303 | §11.1 |
| `sling-shepherd` | trophies[] id=sling-shepherd | 303 | §11.1 |
| `staff-shepherd` | trophies[] id=staff-shepherd | 303 | §11.1 |

### SVG / picture ids (picPlan, cards[].pic) (6)

| Spec names | Lives in Part 2 at | Part 1 lines | Sections |
|---|---|---|---|
| `svg:coin` | picPlan / cards[].pic svg:coin | 105 | §3 |
| `high-five` | picPlan / cards[].pic high-five | 144 | §5 |
| `svg:hungry` | picPlan / cards[].pic svg:hungry | 144 | §5 |
| `svg:pray-kneel` | picPlan / cards[].pic svg:pray-kneel | 144 | §5 |
| `svg:tie` | picPlan / cards[].pic svg:tie | 144 | §5 |
| `svg:chef-hat` | picPlan / cards[].pic svg:chef-hat | 150 | §5 |

### uiText keys (labels; Build never hardcodes label text) (94)

| Spec names | Lives in Part 2 at | Part 1 lines | Sections |
|---|---|---|---|
| `uiText.comingNext` | uiText.comingNext | 27 | §1 |
| `uiText.guardianLast` | uiText.guardianLast | 27 | §1 |
| `uiText.regionOpen` | uiText.regionOpen | 27 | §1 |
| `uiText` | uiText | 30,34,358,375 | §1 §16 §18 |
| `uiText.verseGift` | uiText.verseGift | 45,73,166,261,333,341,342,411 | §2 §3 §6.2 §9 §14 §15 §19 |
| `uiText.back` | uiText.back | 72,171,199,203,227 | §3 §6.3 §6.6 §6.7 §7.1 |
| `uiText.toMap` | uiText.toMap | 72,123,260,325,396,399 | §3 §9 §12 §19 |
| `uiText.character` | uiText.character | 73,199 | §3 §6.6 |
| `uiText.scrolls` | uiText.scrolls | 73,199,207 | §3 §6.6 §6.8 |
| `uiText.soundDuel` | uiText.soundDuel | 73 | §3 |
| `uiText.titleMap` | uiText.titleMap | 73,164,170 | §3 §6.2 §6.3 |
| `uiText.chooseHero` | uiText.chooseHero | 76 | §3 |
| `uiText.heroName` | uiText.heroName | 76,176,199 | §3 §6.3 §6.6 |
| `uiText.heroNancy` | uiText.heroNancy | 76,176 | §3 §6.3 |
| `uiText.useBackup` | uiText.useBackup | 131,203 | §4 §6.7 |
| `uiText.openFromHome` | uiText.openFromHome | 133 | §4 |
| `uiText.updateReady` | uiText.updateReady | 134,174 | §4 §6.3 |
| `uiText.slowMode` | uiText.slowMode | 135,199 | §4 §6.6 |
| `uiText.continue` | uiText.continue | 136,138 | §4 |
| `greetAfternoon` | uiText.greetAfternoon | 157 | §6.1 |
| `greetEvening` | uiText.greetEvening | 157 | §6.1 |
| `greetNight` | uiText.greetNight | 157 | §6.1 |
| `uiText.greetMorning` | uiText.greetMorning | 157 | §6.1 |
| `uiText.letsGo` | uiText.letsGo | 157,388 | §6.1 §19 |
| `uiText.gear` | uiText.gear | 164,293,295,298 | §6.2 §11.1 |
| `uiText.pantry` | uiText.pantry | 164,199,319 | §6.2 §6.6 §11.4 |
| `uiText.daysWithEnglish` | uiText.daysWithEnglish | 171,329 | §6.3 §13 |
| `uiText.goldStars` | uiText.goldStars | 171 | §6.3 |
| `uiText.boss` | uiText.boss | 174,260 | §6.3 §9 |
| `uiText.playAgain` | uiText.playAgain | 174 | §6.3 |
| `uiText.echoKnight` | uiText.echoKnight | 175,323 | §6.3 §12 |
| `chooseHero` | uiText.chooseHero | 176 | §6.3 |
| `uiText.hintButton` | uiText.hintButton | 187 | §6.4 |
| `uiText.wordsForYou` | uiText.wordsForYou | 187 | §6.4 |
| `uiText.sayItOutLoud` | uiText.sayItOutLoud | 193 | §6.5 |
| `uiText.replay` | uiText.replay | 194,227,342 | §6.5 §7.1 §15 |
| `uiText.backup` | uiText.backup | 199,203 | §6.6 §6.7 |
| `uiText.earnedShelf` | uiText.earnedShelf | 199,285 | §6.6 §11.1 |
| `uiText.gems` | uiText.gems | 199 | §6.6 |
| `uiText.restWeeks` | uiText.restWeeks | 199,329 | §6.6 §13 |
| `uiText.yourHero` | uiText.yourHero | 199 | §6.6 |
| `backup` | uiText.backup | 203 | §6.7 |
| `thaiReview` | uiText.thaiReview | 203 | §6.7 |
| `uiText.backupCompare` | uiText.backupCompare | 203 | §6.7 |
| `uiText.restore` | uiText.restore | 203 | §6.7 |
| `uiText.scrollsEmpty` | uiText.scrollsEmpty | 207,404 | §6.8 §19 |
| `uiText.itStartsWith` | uiText.itStartsWith | 219 | §7 |
| `uiText.jesusAllHeard` | uiText.jesusAllHeard | 220,386 | §7 §19 |
| `uiText.jesusWords` | uiText.jesusWords | 220 | §7 |
| `uiText.tapPrompt` | uiText.tapPrompt | 226 | §7.1 |
| `uiText.listenFind` | uiText.listenFind | 228 | §7.1 |
| `uiText.howMany` | uiText.howMany | 229 | §7.1 |
| `uiText.howManyCows` | uiText.howManyCows | 229 | §7.1 |
| `uiText.bigOrSmall` | uiText.bigOrSmall | 230 | §7.1 |
| `uiText.spellIt` | uiText.spellIt | 231 | §7.1 |
| `uiText.highFive` | uiText.highFive | 247 | §8.1 |
| `uiText.pray` | uiText.pray | 247 | §8.1 |
| `uiText.done` | uiText.done | 248,390 | §8.1 §19 |
| `uiText.serverAsks` | uiText.serverAsks | 254 | §8.2 |
| `goldStars` | uiText.goldStars | 268 | §10 |
| `uiText.wearing` | uiText.wearing | 287 | §11.1 |
| `uiText.unlocksAtLevel` | uiText.unlocksAtLevel | 288 | §11.1 |
| `unlocksBosses` | uiText.unlocksBosses | 288 | §11.1 |
| `unlocksPips` | uiText.unlocksPips | 288 | §11.1 |
| `unlocksZoneRight` | uiText.unlocksZoneRight | 288 | §11.1 |
| `uiText.wearIt` | uiText.wearIt | 292,310,319 | §11.1 §11.2 §11.4 |
| `getFor` | uiText.getFor | 293 | §11.1 |
| `uiText.getFor` | uiText.getFor | 293,295,319 | §11.1 §11.4 |
| `uiText.nextWeapon` | uiText.nextWeapon | 293 | §11.1 |
| `uiText.weaponEarnAt` | uiText.weaponEarnAt | 293 | §11.1 |
| `uiText.weaponInShop` | uiText.weaponInShop | 293 | §11.1 |
| `uiText.weaponInUse` | uiText.weaponInUse | 293 | §11.1 |
| `uiText.weaponNew` | uiText.weaponNew | 293,296 | §11.1 |
| `uiText.weaponUse` | uiText.weaponUse | 293 | §11.1 |
| `bonusHint` | uiText.bonusHint | 294 | §11.1 |
| `bonusRespell` | uiText.bonusRespell | 294 | §11.1 |
| `bonusRetry` | uiText.bonusRetry | 294 | §11.1 |
| `bonusSlow` | uiText.bonusSlow | 294 | §11.1 |
| `bonusStar` | uiText.bonusStar | 294 | §11.1 |
| `bonusStreak` | uiText.bonusStreak | 294 | §11.1 |
| `uiText.weapon` | uiText.weapon | 294 | §11.1 |
| `uiText.giftFrom` | uiText.giftFrom | 296 | §11.1 |
| `uiText.classDefender` | uiText.classDefender | 301 | §11.1 |
| `uiText.weaponGift` | uiText.weaponGift | 303,395 | §11.1 §19 |
| `uiText.secretCaption` | uiText.secretCaption | 304 | §11.1 |
| `uiText.secretReveal` | uiText.secretReveal | 304 | §11.1 |
| `uiText.hearItAgain` | uiText.hearItAgain | 324 | §12 |
| `uiText.roundDone` | uiText.roundDone | 325 | §12 |
| `uiText.keepGoing` | uiText.keepGoing | 333 | §14 |
| `uiText.restNow` | uiText.restNow | 333 | §14 |
| `uiText.askMax` | uiText.askMax | 341 | §15 |
| `uiText.verseOfDay` | uiText.verseOfDay | 342 | §15 |
| `uiText.dailyGift` | uiText.dailyGift | 343 | §15 |
| `uiText.example` | uiText.example | 353 | §16 |

### Dotted data paths (picPlan.*, verses.*, meta.*, zones[].*, trophyRules.*, mapLayout.*) (76)

| Spec names | Lives in Part 2 at | Part 1 lines | Sections |
|---|---|---|---|
| `picPlan.inlineSvg` | picPlan.inlineSvg | 7,147,149,150 | HOW TO USE THIS PROMPT §5 |
| `picPlan.svg` | picPlan.svg | 7,144,150 | HOW TO USE THIS PROMPT §5 |
| `picPlan.trophyInlineSvg` | picPlan.trophyInlineSvg | 7,147,150 | HOW TO USE THIS PROMPT §5 |
| `picPlan.trophySvg` | picPlan.trophySvg | 7,150 | HOW TO USE THIS PROMPT §5 |
| `picPlan.uiSvg` | picPlan.uiSvg | 7,150 | HOW TO USE THIS PROMPT §5 |
| `rewardText` | rewardText | 19,30,73,191,261,264,285,310,358,375,411 | §0 §1 §3 §6.5 §9 §11.1 §11.2 §16 §18 §19 |
| `boss.name` | zones[].boss.name | 27,121,227,260,296 | §1 §3 §7.1 §9 §11.1 |
| `mapLayout` | mapLayout | 27,227,272,358 | §1 §7.1 §10 §16 |
| `gotItText` | gotItText | 30,194,342,358,375 | §1 §6.5 §15 §16 §18 |
| `restScreen` | restScreen | 30,73,333,358,375 | §1 §3 §14 §16 §18 |
| `welcomeBack` | welcomeBack | 30,121,329,342,358,375 | §1 §3 §13 §15 §16 §18 |
| `wrongText` | wrongText | 30,191,216,232,249,260,358,375 | §1 §6.5 §7 §7.1 §8.1 §9 §16 §18 |
| `verses.graceRule` | verses.graceRule | 44 | §2 |
| `picPlan.uiInlineSvg.tex` | picPlan.uiInlineSvg.tex | 54 | §3 |
| `picPlan` | picPlan | 57,358 | §3 §16 |
| `zones[].boss.name` | zones[].boss.name | 73 | §3 |
| `picPlan.uiInlineSvg.aura` | picPlan.uiInlineSvg.aura | 76 | §3 |
| `picPlan.uiInlineSvg.sam` | picPlan.uiInlineSvg.sam | 76,176 | §3 §6.3 |
| `encouragement` | encouragement | 121,166,191,220,358 | §3 §6.2 §6.5 §7 §16 |
| `picPlan.svgNotes` | picPlan.svgNotes | 146,247 | §5 §8.1 |
| `zones[].emblem` | zones[].emblem | 150 | §5 |
| `picPlan.uiInlineSvg.nancy` | picPlan.uiInlineSvg.nancy | 157 | §6.1 |
| `picPlan.uiInlineSvg.title` | picPlan.uiInlineSvg.title | 157 | §6.1 |
| `verses` | verses | 166,358 | §6.2 §16 |
| `picPlan.trophyStyle.streakFlame` | picPlan.trophyStyle.streakFlame | 171 | §6.3 |
| `mapLayout.regions` | mapLayout.regions | 173 | §6.3 |
| `trophies[].cat` | trophies[].cat | 199 | §6.6 |
| `needsMaxwell` | needsMaxwell | 203,358,371 | §6.7 §16 §17 |
| `verses.attribution` | verses.attribution | 207,346,375 | §6.8 §15 §18 |
| `jesusWords` | jesusWords | 220,345,358 | §7 §15 §16 |
| `jesusWordsFallback` | jesusWordsFallback | 220,358,375 | §7 §16 §18 |
| `meta.outings` | meta.outings | 222 | §7 |
| `meta.sizeSort` | meta.sizeSort | 230 | §7.1 |
| `zones[].boss.cards` | zones[].boss.cards | 260 | §9 |
| `trophies` | trophies | 262,281,315,358,395 | §9 §11 §11.3 §16 §19 |
| `zones` | zones | 272,358 | §10 §16 |
| `picPlan.trophyStyle` | picPlan.trophyStyle | 286 | §11.1 |
| `unlock.type` | trophies[].unlock.type | 288,289,296,304 | §11.1 |
| `meta.bonusGems` | meta.bonusGems | 293 | §11.1 |
| `meta.weaponTiers` | meta.weaponTiers | 293 | §11.1 |
| `trophyRules.tierStars` | trophyRules.tierStars | 293 | §11.1 |
| `meta.weaponBonus` | meta.weaponBonus | 294 | §11.1 |
| `trophyRules.theme` | trophyRules.theme | 294 | §11.1 |
| `trophyRules.rows` | trophyRules.rows | 295 | §11.1 |
| `trophyRules.giftOf` | trophyRules.giftOf | 296 | §11.1 |
| `picPlan.weaponParts` | picPlan.weaponParts | 299 | §11.1 |
| `trophyRules.hands` | trophyRules.hands | 299 | §11.1 |
| `trophyRules.classes` | trophyRules.classes | 301 | §11.1 |
| `trophies[].unlock` | trophies[].unlock | 309 | §11.2 |
| `pantry.items` | pantry.items | 315,319 | §11.3 §11.4 |
| `pantry.earn` | pantry.earn | 319 | §11.4 |
| `verses.rest` | verses.rest | 333 | §14 |
| `zones[].boss.scroll` | zones[].boss.scroll | 338 | §15 |
| `meta.dailyVerses` | meta.dailyVerses | 339 | §15 |
| `verses.rotation` | verses.rotation | 339 | §15 |
| `verses.weekly` | verses.weekly | 339 | §15 |
| `verses.weeklyStart` | verses.weeklyStart | 339 | §15 |
| `verses[]` | verses | 339 | §15 |
| `verses.decided` | verses.decided | 344 | §15 |
| `verses.textRule` | verses.textRule | 344 | §15 |
| `verses.ttsRule` | verses.ttsRule | 344 | §15 |
| `verses.attribution.esvTag` | verses.attribution.esvTag | 346 | §15 |
| `meta.typeByZone` | meta.typeByZone | 351 | §16 |
| `zones[]` | zones | 351 | §16 |
| `meta.cardDefaults` | meta.cardDefaults | 352 | §16 |
| `meta.cardThStatusDefault` | meta.cardThStatusDefault | 352 | §16 |
| `meta.modeByType` | meta.modeByType | 352 | §16 |
| `meta.thStatusDefault` | meta.thStatusDefault | 352 | §16 |
| `pantry` | pantry | 352 | §16 |
| `cards` | cards | 358 | §16 |
| `meta` | meta | 358 | §16 |
| `rewardClips` | rewardClips | 358 | §16 |
| `soundDuel.pairs` | soundDuel.pairs | 358 | §16 |
| `trophyRules` | trophyRules | 358 | §16 |
| `.thsv11` | verses.attribution.thsv11 | 410 | §19 |
| `verses.attribution.esv` | verses.attribution.esv | 410 | §19 |

### Field names (resolve inside the object the sentence is about) (111)

| Spec names | Lives in Part 2 at | Part 1 lines | Sections |
|---|---|---|---|
| `pic` | cards[].choices[].pic / cards[].pic / pantry.items[].pic / trophies[].pic | 7,142,226,231,239,354,356 | HOW TO USE THIS PROMPT §5 §7.1 §8 §16 |
| `reply` | cards[].reply | 42,238 | §2 §8 |
| `tex` | picPlan.uiInlineSvg.tex | 55,146 | §3 §5 |
| `title` | picPlan.uiInlineSvg.title / trophyRules.defaults.title | 55,301,302 | §3 §11.1 |
| `name` | zones[].boss.name / zones[].name | 73,358 | §3 §16 |
| `nameTh` | zones[].nameTh | 73,375 | §3 §18 |
| `color` | mapLayout.regions[].color | 76,358 | §3 §16 |
| `nancy` | picPlan.uiInlineSvg.nancy | 76,176 | §3 §6.3 |
| `stone` | picPlan.uiInlineSvg.stone | 76,176 | §3 §6.3 |
| `sword` | picPlan.uiInlineSvg.sword | 76,176 | §3 §6.3 |
| `restSky` | trophyRules.defaults.restSky | 121,302 | §3 §11.1 |
| `svgDrawnCount` | picPlan.svgDrawnCount | 150,358 | §5 §16 |
| `trophySvgDrawnCount` | picPlan.trophySvgDrawnCount | 150,358 | §5 §16 |
| `a` | soundDuel.pairs[].a | 157,227,358 | §6.1 §7.1 §16 |
| `en` | cards[].choices[].en / cards[].en / cards[].prompts[].en / cards[].reply.en / encouragement[].en (+112 more) | 157,223,226,246,254,323,339,342,344,351,352,356,407 | §6.1 §7 §7.1 §8.1 §8.2 §12 §15 §16 §19 |
| `n` | trophies[].unlock.n | 157,227,309 | §6.1 §7.1 §11.2 |
| `th` | cards[].prompts[].th / cards[].reply.th / cards[].th / encouragement[].th / gotItText.th (+111 more) | 157,185,226,246,254,286,339,342,344,356,375,407 | §6.1 §6.4 §7.1 §8.1 §8.2 §11.1 §15 §16 §18 §19 |
| `startZone` | zones[].startZone | 159,358 | §6.1 §16 |
| `streakFlame` | picPlan.trophyStyle.streakFlame | 166 | §6.2 |
| `pathStyle` | mapLayout.pathStyle | 173,358 | §6.3 §16 |
| `bossesWon` | trophyRules.unlockTypes.bossesWon | 175,261,273,309,394,408 | §6.3 §9 §10 §11.2 §19 |
| `arrowTrail` | trophyRules.defaults.arrowTrail | 177,302 | §6.3 §11.1 |
| `mapLanterns` | trophyRules.defaults.mapLanterns | 177,302 | §6.3 §11.1 |
| `mapPet` | trophyRules.defaults.mapPet | 177,302 | §6.3 §11.1 |
| `mapTheme` | trophyRules.defaults.mapTheme | 177,302 | §6.3 §11.1 |
| `thDef` | cards[].thDef | 185,375 | §6.4 §18 |
| `faith` | cards[].faith / meta.cardDefaults.faith | 192,352 | §6.5 §16 |
| `trapNote` | cards[].trapNote / meta.cardDefaults.trapNote | 192,352,353 | §6.5 §16 |
| `gear` | meta.trophiesByCat.gear / uiText.gear | 199 | §6.6 |
| `themes` | meta.trophiesByCat.themes / uiText.themes | 199 | §6.6 |
| `titles` | meta.trophiesByCat.titles / uiText.titles | 199 | §6.6 |
| `pipFills` | trophyRules.unlockTypes.pipFills | 217,309,387 | §7 §11.2 §19 |
| `ref` | jesusWords[].ref / trophies[].ref / verses.rest.ref / verses.weekly[].ref / zones[].boss.scroll.ref | 220,297,339,395 | §7 §11.1 §15 §19 |
| `thGloss` | jesusWords[].thGloss / trophies[].thGloss | 220,286,339,345,358,375 | §7 §11.1 §15 §16 §18 |
| `type` | cards[].type / jesusWords[].given.type / meta.cardDefaults.type / trophies[].unlock.type | 244,351,352 | §8.1 §16 |
| `prompts` | cards[].prompts | 246,356,390 | §8.1 §16 §19 |
| `answer` | cards[].answer / cards[].prompts[].answer / meta.cardDefaults.answer | 247,254,352,354,356,382 | §8.1 §8.2 §16 §19 |
| `choices` | cards[].choices / meta.cardDefaults.choices | 247,254,352,356 | §8.1 §8.2 §16 |
| `key` | cards[].choices[].key / cards[].prompts[].key / zones[].key | 247,356 | §8.1 §16 |
| `trap` | cards[].trap / meta.cardDefaults.trap | 254,352,354,382 | §8.2 §16 §19 |
| `wt` | trophies[].wt | 281,301 | §11 §11.1 |
| `enlarged` | picPlan.trophyStyle.enlarged | 286 | §11.1 |
| `gems` | meta.trophiesByCat.gems / picPlan.trophyStyle.gems / uiText.gems | 286 | §11.1 |
| `cardFrame` | trophyRules.defaults.cardFrame | 292,302 | §11.1 |
| `slot` | pantry.items[].slot / trophies[].slot | 292,319 | §11.1 §11.4 |
| `2` | meta.weaponTiers.2 | 294 | §11.1 |
| `tier` | trophies[].tier | 295 | §11.1 |
| `tierColor` | trophyRules.tierColor | 295 | §11.1 |
| `typeNames` | trophyRules.typeNames | 295 | §11.1 |
| `weaponParts` | picPlan.weaponParts | 295 | §11.1 |
| `guardian` | trophyRules.unlockTypes.guardian | 296,309 | §11.1 §11.2 |
| `word` | trophies[].word | 297,351,375 | §11.1 §16 §18 |
| `one` | trophyRules.hands.one | 299 | §11.1 |
| `two` | trophyRules.hands.two | 299 | §11.1 |
| `classKnight` | trophyRules.classes.classKnight / uiText.classKnight | 301 | §11.1 |
| `classWarrior` | trophyRules.classes.classWarrior / uiText.classWarrior | 301 | §11.1 |
| `auraRing` | trophyRules.defaults.auraRing | 302 | §11.1 |
| `avatarFrame` | trophyRules.defaults.avatarFrame | 302 | §11.1 |
| `cape` | trophyRules.defaults.cape | 302 | §11.1 |
| `featuredGem` | trophyRules.defaults.featuredGem | 302 | §11.1 |
| `swordSplash` | trophyRules.defaults.swordSplash | 302 | §11.1 |
| `tunic` | trophyRules.defaults.tunic | 302 | §11.1 |
| `weapon` | trophyRules.defaults.weapon / uiText.weapon | 302 | §11.1 |
| `secret` | trophyRules.unlockTypes.secret | 304,309 | §11.1 §11.2 |
| `level` | trophyRules.unlockTypes.level | 309 | §11.2 |
| `start` | trophyRules.unlockTypes.start | 309 | §11.2 |
| `zone` | meta.audioClips.zone / trophies[].unlock.zone | 309 | §11.2 |
| `zoneRight` | trophyRules.unlockTypes.zoneRight | 309 | §11.2 |
| `stars` | pantry.items[].stars | 319 | §11.4 |
| `tint` | pantry.items[].tint | 319 | §11.4 |
| `pics` | meta.pics / soundDuel.pairs[].pics | 323,400 | §12 §19 |
| `enUrl` | jesusWords[].enUrl / verses.rest.enUrl / verses.weekly[].enUrl / zones[].boss.scroll.enUrl | 339,344 | §15 |
| `rule` | picPlan.rule | 339 | §15 |
| `thUrl` | jesusWords[].thUrl / verses.rest.thUrl / verses.weekly[].thUrl / zones[].boss.scroll.thUrl | 339,344 | §15 |
| `verifiedBy` | jesusWords[].verifiedBy | 339,345 | §15 |
| `enSource` | jesusWords[].enSource / verses.rest.enSource / verses.weekly[].enSource / zones[].boss.scroll.enSource | 344 | §15 |
| `esv` | verses.attribution.esv | 346 | §15 |
| `esvSource` | verses.attribution.esvSource | 346 | §15 |
| `tagRule` | verses.attribution.tagRule | 346 | §15 |
| `thsv11` | verses.attribution.thsv11 | 346 | §15 |
| `thsv11Source` | verses.attribution.thsv11Source | 346 | §15 |
| `thsv11Tag` | verses.attribution.thsv11Tag | 346 | §15 |
| `hint` | cards[].hint | 351,354 | §16 |
| `id` | cards[].id / mapLayout.regions[].id / pantry.items[].id / trophies[].id | 351 | §16 |
| `picture` | meta.modeByType.picture | 351,352,354 | §16 |
| `prefix` | zones[].prefix | 351,358 | §16 |
| `easy` | cards[].easy / meta.cardDefaults.easy | 352 | §16 |
| `fill` | cards[].fill / meta.cardDefaults.fill | 352 | §16 |
| `nursePhrase` | cards[].nursePhrase / meta.cardDefaults.nursePhrase | 352,375 | §16 §18 |
| `personal` | cards[].personal / meta.cardDefaults.personal | 352 | §16 |
| `tag` | cards[].tag / meta.cardDefaults.tag | 352 | §16 |
| `say-it` | meta.modeByType.say-it | 355 | §16 |
| `respell` | cards[].prompts[].respell / cards[].respell | 356 | §16 |
| `two-answer` | meta.modeByType.two-answer | 356 | §16 |
| `accent` | mapLayout.regions[].accent | 358 | §16 |
| `b` | soundDuel.pairs[].b | 358 | §16 |
| `boss` | meta.audioClips.boss / uiText.boss / zones[].boss | 358 | §16 |
| `clip` | zones[].boss.clip | 358 | §16 |
| `emblem` | zones[].emblem | 358 | §16 |
| `given` | jesusWords[].given | 358 | §16 |
| `inlineSvg` | picPlan.inlineSvg | 358 | §16 |
| `paths` | mapLayout.paths | 358 | §16 |
| `regions` | mapLayout.regions / trophies[].unlock.regions | 358 | §16 |
| `scroll` | zones[].boss.scroll | 358 | §16 |
| `thGlossBy` | jesusWords[].thGlossBy | 358 | §16 |
| `thGlossStatus` | jesusWords[].thGlossStatus | 358 | §16 |
| `trophyInlineSvg` | picPlan.trophyInlineSvg | 358 | §16 |
| `uiInlineSvg` | picPlan.uiInlineSvg | 358 | §16 |
| `zoneClip` | zones[].zoneClip | 358 | §16 |
| `syl` | cards[].syl | 360 | §16 |
| `instructorChecked` | uiText.done.instructorChecked / uiText.earnedShelf.instructorChecked / uiText.highFive.instructorChecked / uiText.jesusAllHeard.instructorChecked / uiText.jesusWords.instructorChecked (+2 more) | 375 | §18 |

### Field = value statements (21)

| Spec names | Lives in Part 2 at | Part 1 lines | Sections |
|---|---|---|---|
| `mode: "english-first"` | meta.modeByType (from type) = "english-first" | 151,236,355 | §5 §8 §16 |
| `given.type: "start"` | jesusWords[].given.type = "start" | 220 | §7 |
| `easy:true` | cards[].easy / meta.cardDefaults.easy = true | 223 | §7 |
| `faith:true` | cards[].faith / meta.cardDefaults.faith = true | 223,240,250 | §7 §8 §8.1 |
| `fill:true` | cards[].fill / meta.cardDefaults.fill = true | 223,363 | §7 §16 |
| `personal:true` | cards[].personal / meta.cardDefaults.personal = true | 223,362 | §7 §16 |
| `type: "say-it"` | cards[].type / jesusWords[].given.type / meta.cardDefaults.type / trophies[].unlock.type = "say-it" | 236 | §8 |
| `"two-answer"` | cards[].type = "two-answer" (ms-31) | 244 | §8.1 |
| `type: "server-talk"` | cards[].type / jesusWords[].given.type / meta.cardDefaults.type / trophies[].unlock.type = "server-talk" | 252 | §8.2 |
| `unlock: {type: "level", n}` | trophies[].unlock = {type: "level", n} | 262 | §9 |
| `unlock.type: "start"` | trophies[].unlock.type = "start" | 305 | §11.1 |
| `status: "VERIFIED"` | jesusWords[].status / verses.attribution.status / verses.rest.status / verses.weekly[].status / zones[].boss.scroll.status = "VERIFIED" | 344,345,375 | §15 §18 |
| `thSource: "THSV11"` | jesusWords[].thSource / verses.rest.thSource / verses.weekly[].thSource / zones[].boss.scroll.thSource = "THSV11" | 344 | §15 |
| `NEEDS NANCY` | meta.cardThStatusDefault / meta.thStatusDefault = "NEEDS NANCY" | 352,361,375 | §16 §18 |
| `tag: "Example"` | cards[].tag / meta.cardDefaults.tag = "Example" | 353 | §16 |
| `mode: "picture-recall"` | meta.modeByType (from type) = "picture-recall" | 354 | §16 |
| `answer: null` | cards[].answer / cards[].prompts[].answer / meta.cardDefaults.answer = null | 355,356 | §16 |
| `choices: []` | cards[].choices / meta.cardDefaults.choices = [] | 355 | §16 |
| `mode: "two-answer"` | meta.modeByType (from type) = "two-answer" | 356 | §16 |
| `nursePhrase: true` | cards[].nursePhrase / meta.cardDefaults.nursePhrase = true | 357 | §16 |
| `thStatus: "SIGNED OFF"` | cards[].thStatus (6 SIGNED OFF) else meta.cardThStatusDefault = "SIGNED OFF" | 375 | §18 |

### Fields that are often ABSENT in the file and take a default (4)

| Spec names | Lives in Part 2 at | Part 1 lines | Sections |
|---|---|---|---|
| `mode` | meta.modeByType (from type) | 244,352 | §8.1 §16 |
| `nameThStatus` | meta.thStatusDefault (absent in file = default) | 352,358,375 | §16 §18 |
| `thDefStatus` | meta.thStatusDefault (absent in file = default) | 352 | §16 |
| `thStatus` | cards[].thStatus (6 SIGNED OFF) else meta.cardThStatusDefault | 352 | §16 |

### Derived values (computed from other data, not stored) (7)

| Spec names | Lives in Part 2 at | Part 1 lines | Sections |
|---|---|---|---|
| `hint.letters` | cards[].hint (compact: string=sound, list=[letters,sound,word]) | 219,294,384 | §7 §11.1 §19 |
| `hint.sound` | cards[].hint (compact) | 219,353 | §7 §16 |
| `tierNames[t]` | trophyRules.tierNames | 295 | §11.1 |
| `classTitle` | derived: trophyRules.classes by weapon wt -> uiText.class* | 301,358 | §11.1 §16 |
| `letters` | cards[].hint (compact) | 351 | §16 |
| `sound` | cards[].hint (compact) | 351 | §16 |
| `hint.word` | cards[].hint (compact; data only) | 353 | §16 |

### Id patterns (3)

| Spec names | Lives in Part 2 at | Part 1 lines | Sections |
|---|---|---|---|
| `svg:<id>` | cards[].pic / picPlan.svg ids | 7,144 | HOW TO USE THIS PROMPT §5 |
| `uiText.bonus<word>` | uiText.bonus* (10 keys) | 294 | §11.1 |
| `<type>-t<t>` | trophies[].id pattern | 295 | §11.1 |

### Attached files and clip paths (outside the two parts) (10)

| Spec names | Lives in Part 2 at | Part 1 lines | Sections |
|---|---|---|---|
| `cards.json` | Part 2 JSON line (save as cards.json) | 5,12,34,41,134,350,371,411,422 | HOW TO USE THIS PROMPT §1 §2 §4 §16 §17 §19 CARD FILE |
| `/audio/` | zones[].zoneClip, boss.clip, rewardClips paths | 134 | §4 |
| `nancys-adventure-english-v6-08-title.svg` | 3rd attached file | 157 | §6.1 |
| `title.svg` | 3rd attached file nancys-adventure-english-v6-08-title.svg | 157 | §6.1 |
| `daily-verses.json` | 2nd attached file nancys-adventure-english-v6-08-daily-verses.json | 339 | §15 |
| `enGloss` | daily-verses.json verses[] (optional) | 339 | §15 |
| `nancys-adventure-english-v6-08-daily-verses.json` | 2nd attached file | 339 | §15 |
| `maxwell-<zone>.m4a` | zones[].zoneClip | 365 | §16 |
| `maxwell-boss-<zone>.m4a` | zones[].boss.clip | 365 | §16 |
| `maxwell-reward-1..5.m4a` | rewardClips | 365 | §16 |

### Names that must NOT exist anywhere (2)

| Spec names | Lives in Part 2 at | Part 1 lines | Sections |
|---|---|---|---|
| `cost` | must NOT exist anywhere (grace check) | 47,411 | §2 §19 |
| `price` | must NOT exist anywhere (grace check) | 47,411 | §2 §19 |
