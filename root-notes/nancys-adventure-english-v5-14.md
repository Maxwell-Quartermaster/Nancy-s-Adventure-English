# Nancy's Adventure English — v5-14 Master Build Prompt

Single source of truth. Card data comes from the companion file `nancys-adventure-english-v5-14-cards.json`, attached with this prompt and saved in the build as `cards.json`. The card file wins on all card content.

## 0. Why this exists

**You are seen, loved, and capable.** Every screen should say that to Nancy, Maxwell's Thai-speaking wife.

- Every system asks: does this make her feel capable? If not, cut it.
- Personal meaning leads: Maxwell's voice, her hotel work, her baby, her faith. The game skin is Maxwell's joy. Nancy's joy is being seen and succeeding.
- Rewards read "You earned this!" / "เก่งมาก! รางวัลนี้เป็นของคุณ", never "Unlocked."
- Rest is a gift, and a pause is mercy for a season of life. Nothing ever breaks or fails.

## 1. Rules

1. **Three-second rule:** every screen is clear in 3 seconds without Maxwell.
2. **XP is the only points.** It never goes down. No currency, prices, or spending. Gold coins are only the visual pip meter; cosmetics are trophies earned automatically (section 11).
3. **Flow:** the challenge sits just above her skill, with clear goals and instant feedback.
4. **One new thing per level and per screen.** A level gives at most one new zone, boss, or feature, plus one small reward (a cosmetic or a talent point).
5. **No voice recognition.** She speaks aloud on the honor system.
6. **Pregnancy safe:** no shake, nothing flashing more than 3 times a second, no sudden loud sounds.
7. **Thai on every instruction and label,** shown the moment it appears.
8. **Text hierarchy** wherever English and Thai appear together: English on top, bold and larger; Thai underneath, regular, about 75% size, secondary color. Exception: the question screen hides the English answer (6.4).
9. **Nothing red or alarming** anywhere.
10. **Maxwell is in the room during play.** The app has no phone links and no contact features.

## 2. Privacy (public web app)

- No personal contact info (phone numbers, addresses, emails) and no phone links are ever in any publicly deployed version: source, `cards.json`, service worker cache, or manifest.
- Card text holds no real names, addresses, birth or due dates, or phone numbers.
- Personal progress lives on the device only, in IndexedDB. The app makes no network calls except fetching its own files.

## 3. Look: chunky cartoon strategy-game style

Original SVG/CSS art in a bright, cel-shaded mobile-strategy style ("Clash of Clans feel"), with no copied assets, characters, logos, or fonts. No online images. Put `<!-- Private family use. Original art. -->` at the top of `index.html`. Match any attached mockups.

- **Cel-shaded:** flat fills, one hard shadow tone, one highlight band; no airbrush gradients on objects.
- **Outlines:** 3–4 px Ink `#10170F` on every button, tile, panel, and drawn icon.
- **Chunky buttons:** 18 px radius, a 6 px darker bottom bevel, a top highlight band. On press they sink 4 px (bevel to 2 px) in 80 ms and pop back.
- **Materials, CSS only:** stone plates (gray gradients plus 2–3 rivet dots), metal trim (steel gradient with a 1 px light top edge), plank trim only on frame edges and signposts (never a large brown surface).
- **Layout:** each screen has a thin top bar, one main area, and a bottom bar; no modal on a modal. Everything she taps sits in the lower 60%.
- **Motion:** slide-and-pulse transitions, not flips. A bouncing Gold arrow (1.2 s, 8 px) marks the next step. Calm Motion, or `prefers-reduced-motion`, swaps every move for a 150 ms fade or brightness flash.
- **Opaque layers:** nothing behind a moving element ever shows through.

**Palette (AA-checked):**

| Token | Hex | Use |
|---|---|---|
| Forest | `#0E3B22` | app background (grass gradient to `#145A32`) |
| Meadow | `#17633A` | panels, top bar |
| Grass | `#2FA84F` | highlight bands; dark text only |
| Grass Deep | `#1B7A37` | primary button face, white text |
| Grass Edge | `#0F5726` | green bevel |
| Gold | `#FFCC33` | coins, trophies, arrow, right-answer glow |
| Gold Edge | `#B7860B` | gold bevel and coin rim |
| XP Track | `#2B1752` | XP bar trough |
| XP Purple | `#6D3CC9` | XP bar fill |
| XP Lilac | `#B79BFF` | XP fill top highlight band |
| Cream | `#FFF8E1` | text on dark, choice plates, picture frame |
| Mint | `#8EE0B5` / edge `#4FA37D` | hint button |
| Stone | `#5B6670` / `#D9DEE3` | locked tiles, Settings plates |
| Moonstone | `#9DB4CC` | soft "missed" glow |
| Ink | `#10170F` | outlines, text on light plates |

Contrast: Cream on Forest 11.9, Cream on Meadow 6.9, white on Grass Deep 5.4, Ink on Cream 17.2, Ink on Gold 12.1, Ink on Mint 11.7, white XP label on XP Purple 6.7, Cream on XP Track 14.7. Never white text on Grass (3.1). High Contrast raises all text to 7:1.

**Fonts** (self-hosted in `/fonts/`, never a CDN): English display and buttons in **Lilita One** (OFL) with a 2 px Ink text stroke on colored buttons. Thai in **Kanit** (Thai subset); fallback `Kanit, "Sukhumvit Set", Thonburi, "Noto Sans Thai", sans-serif`. Respellings in Kanit 500, Gold.

**XP bar and coin meter:**

- **XP bar:** XP Track trough, XP Purple fill with an XP Lilac highlight band, Ink outline, label "Level N" in white bold.
- **Coin meter (the ten pips),** directly under the XP bar and never merged with it: 10 original SVG gold coins (`svg:coin`). Each coin is round Gold with a thick Gold Edge rim, a simple embossed star-and-leaf mark in the center, a bright white highlight crescent at top-left, and a 3 px Ink outline. Empty: dim outline only (Gold Edge at 35%, no fill). Filled: the shiny coin with a 250 ms pop (scale 1→1.2→1).
- **Glow pulse:** when all ten coins fill, and on every level-up, the whole XP bar area glows a soft purple-gold for about 1 s, then returns to normal. With reduced motion, a simple 1 s brightness flash.

## 4. Tech

- **App:** a PWA in vanilla HTML/CSS/JS with `manifest.json` (`display: standalone`, theme and background `#0E3B22`), `apple-mobile-web-app-capable`, `viewport-fit=cover`, and `env(safe-area-inset-*)` insets.
- **Thai:** `lang="th"` and `line-height: 1.7` on every Thai string.
- **Storage:** IndexedDB object store `kv`, key `state` (one record, section 10), mirrored to localStorage after each commit. Call `navigator.storage.persist()`.
- **Home screen:** the icon avoids Safari's 7-day wipe (iOS may still clear data when storage is low). In plain Safari, show only "Open from your home screen icon" / "เปิดจากไอคอนบนหน้าจอโฮม".
- **Service worker:** cache-first, versioned. Core files (HTML, JS, CSS, fonts, SVGs, sound effects, `cards.json`) go through `cache.addAll`; each voice clip in `/audio/` is cached on its own, failures ignored. Never reload mid-run or while a reward screen is open; show an "Update ready" chip on the Map.
- **Audio:** Web Audio API; decode each clip on first play; a missing or failed clip is skipped silently. English `speechSynthesis` at 0.85 (0.6 in Slow Mode); no Thai voice means Thai audio is skipped.
- **Audio wake:** the sword tap on each launch and every "Continue" tap resume the AudioContext and play a silent buffer. Nothing waits on audio.
- **Locks:** one answer per card; Got it locks until the next screen renders.
- **Auto-pause:** on `visibilitychange` to hidden and on `pagehide`, pause the run, stop audio and the play timer. On return show "Continue", then the exact screen she left.

## 5. Pictures

- **Picture recall applies to the 119 `mode: "picture-recall"` cards.** Each shows one picture of its answer from `pic`:
  - **Emoji** (an emoji string, sometimes two like "👶💤"): Apple Color Emoji at 120 pt, centered. 75 cards.
  - **SVG** (`svg:<id>`): draw the 29 ids in `picPlan.svg` in the section 3 style. Color cards use flat swatches; size cards show two objects with the target outlined in Gold. 30 cards (`svg:hungry` is shared).
  - **Fallback** (`null`): the zone emblem at 40% opacity, with the Thai line moved into the frame at 28 pt as the prompt. 14 abstract cards.
- **Picture frame:** Cream plate, 4 px Ink outline, 18 px radius, stone-and-metal rim, about 200 pt square. Never blank or broken; an emoji that renders as an empty box uses the fallback.
- **Drawings Build makes: 42** = 29 card ids (`picPlan.svg`) + 12 trophy ids (`picPlan.trophySvg`) + 1 coin (`picPlan.uiSvg`). Plus 6 zone emblems, the avatar, and UI icons (gear, leaf hint, trophy, lock, check, scroll, flame, book).
- **Say-it cards** are `mode: "english-first"` (section 8): no picture, no hidden word.

## 6. Screens

### 6.1 Sword screen (every launch)

- Only the sword and "Pick up the sword." / "หยิบดาบขึ้นมา". The tap wakes audio.
- Then follow the launch order (section 10): first launch goes to card 1; an unfinished run resumes at its exact card or reveal; otherwise the Map (or the next Phonics run before the Map is earned).
- The XP bar fades in after card 1, the coin meter after card 3.

### 6.2 Character

After card 5, one panel with the Forest Ranger preselected. One tap on "Go" keeps it. Cosmetic only.

### 6.3 Map (main menu, earned at level 2)

- **Top bar:** the avatar button (opens My Stuff, 11.1) with the featured jewel on its frame and the jewel shelf beside it, a Gold trophy counter (earned of 17), the "Days with English" flame, the Talents book (from level 5), and the gear.
- **Zone grid:** 2 columns × 4 rows of identical tiles, 12 pt gaps, 16 pt side margins: Phonics, Colors and Shapes / Numbers, Sight Words / Baby and Hospital, Maxwell Says / Sound Duel, Scrolls.
- **Tile:** about 164 × 120 pt on a 375 pt screen; a chunky Grass Deep button with the zone emblem (48 pt), the English name bold in Cream, Thai smaller beneath.
- **Closed tiles:** Stone gray with a lock and a level plate ("Level 6" / "เลเวล 6"). Sound Duel stays locked until level 3.
- **Boss ready:** a Gold ribbon across the tile corner, "Boss!" / "บอส!". One bouncing Gold arrow points at the next step.
- **Before level 2:** only two big tiles, Baby and Hospital and Maxwell Says, in the same style.

### 6.4 Question screen (picture-recall cards)

Top to bottom:

1. Top bar: the XP bar, the coin meter under it, the gear.
2. Picture frame (section 5). The English answer is never shown here.
3. **Thai line** directly above the choices (Kanit 18 pt, Cream 80%): `thDef` if present, else `th`. The 15 abstract cards carry `thDef`, a 2–4 word Thai hint rather than a translation.
4. **Choices:** a 2×2 grid of Cream text plates (Lilita One, Ink text, Grass Edge bevel), at least 96 pt tall, shuffled every card. The only English she reads before answering.
5. **Hint button:** bottom-left in the safe area, a 56 pt Mint round button with a leaf-heart icon, at least 16 pt from the choices.

### 6.5 Reveal screen (after every picture-card answer)

- **Header:** `rewardText` on a right answer, `wrongText` ("Now you know it") on a miss.
- **Body:** the picture, the English answer bold (Lilita One 34 pt), the respelling in Gold, the Thai under it. The English is spoken once automatically.
- **Prompt:** "Say it out loud" / "พูดออกเสียงดังๆ" on the first 10 reveals.
- **Buttons:** 🔊 Replay, Say-it-to-Maxwell (full-screen card to read to him, +2 XP once per card), and a big Grass Deep **Got it** (`gotItText`).
- **Never auto-advances.** Only Got it moves on. The hint button here gives encouragement only.

### 6.6 Talents

A stone tablet with 3 nodes. A lit node means she owns it; tapping one previews it.

### 6.7 Settings (the gear)

- Four switches with Thai: High Contrast / คอนทราสต์สูง; Calm Motion / ภาพเคลื่อนไหวน้อย (on automatically with iOS Reduce Motion); Slow Mode / โหมดช้า; Rest weeks / สัปดาห์พัก.
- Maxwell section: Backup/Restore as JSON, the "Needs Maxwell" list, and the Thai Review Queue.

## 7. Core loop

A **run** is 10 cards from one zone, each `picture` or `say-it`.

1. A soft cue plays. The question screen shows the picture and Thai line; nothing is spoken, so she recalls the word herself.
2. She taps one of the four text choices. Near-miss traps stay (play/pray, crib/rib, thirteen/thirty).
3. **Right:** the plate pulses Gold, +10 XP is committed, one coin fills, then the reveal.
4. **Wrong:** the tapped plate glows Moonstone, the right one glows Gold, a soft chime plays, one filled coin dims quietly, then the reveal with `wrongText`. The card returns 3 to 5 cards later, at most twice.
5. **Coin meter:** when all ten coins are filled, the glow pulse plays, `pipFills` +1 is committed, and the coins reset.
6. **Hint:** always free; a right answer after it still earns +10.
   - First tap on a question: shows `hint.letters` (for example "p___" or "P_____ w___ h___.") and speaks "It starts with" plus `hint.sound` ("ขึ้นต้นด้วยเสียง /p/").
   - Further taps, and taps anywhere else: the next line from `encouragement` (for example "I love you." / "ผมรักคุณนะ") in a soft bubble for 3 s.
7. **Review:** cards missed in her most recent completed session, even days ago.
8. **Run order:** skip unwritten cards (`fill:true`, empty `en`); open with one `easy:true` card (every zone has at least 2), preferring her zone; then written `personal:true` cards; then up to 3 review cards; then the rest.

## 8. Say-it cards

37 cards are `type: "say-it"`, `mode: "english-first"`: 33 written (16 Baby and Hospital, 9 Maxwell Says, 5 Sight Words, 2 Numbers, 1 Colors) plus the 4 empty slots (section 17), so 17 are in Baby and Hospital. They include the hospital phrases `bh-01` to `bh-10` (`nursePhrase: true`).

- English bold on top, respelling, Thai underneath; the English is spoken. She says it aloud and taps **Got it**.
- No choices, no picture, no wrong answer. +10 XP and one coin; never dims a coin.
- Hint replays the phrase slowly. Never in boss runs.

## 9. XP, levels, rewards

- **No health in v1.** XP to reach level 2: 60 (her first run); level 3: 250 total (day 1); after that 100 + 60 × (L − 3) more per level. Cap: level 20.
- **Levels 2 to 4 focus on Phonics on purpose.** Baby and Hospital and Maxwell Says stay open; Colors and Numbers open at 6 and 8.

| Zone | Opens | Focus levels | Boss at |
|---|---|---|---|
| Phonics | 1 | 1–4 | 4 |
| Baby and Hospital | 1 | 1–7 | 7 |
| Colors and Shapes | 6 | 6–9 | 9 |
| Numbers | 8 | 8–13 | 13 |
| Sight Words | 10 | 10–16 | 16 |
| Maxwell Says | 1 | none | none |

- **Boss:** exactly the 10 picture cards in `zones[].boss.cards`, ready at the top level of the zone's focus range. A stone guardian's bar drops on each right answer; a boss can't be lost.
- **Boss win (once per zone):** the guardian kneels, a "You earned this!" banner, `bossesWon` adds the zone, the scroll unrolls (section 15), Maxwell's boss clip plays (visuals play even if it's missing). Replays give card XP only.
- **Rewards by level:** 2 the Map + green jewel trophy; 3 Sound Duel + purple cape trophy; 4 Phonics boss + oak card border; 5 Talents + first talent point; 6 Colors and Shapes + title "Brave Learner"; 7 Baby and Hospital boss + talent point; 8 Numbers + blue lantern flames; 9 Colors boss + silver card border; 10 Sight Words + title "Word Ranger"; 11 leaf trail on the map arrow; 12 talent point; 13 Numbers boss + moonlit Map; 14 title "Sound Hunter"; 15 gold card border; 16 Sight Words boss + owl on the Map; 17 starry rest-screen sky; 18 title "Voice of the Inn"; 19 golden sword splash; 20 title "Champion of English" with a crown frame.
- **Talents** (levels 5, 7, 12): a smoother slide, a wider XP flash, a correct-answer glow.
- **Reward screens:** a Cream-and-Gold panel with the picture, English bold, Thai under it, and Got it. Never auto-advance.

## 10. State, awards, resume

- **One state record** `kv/state`: `{xp, level, pipFills, daysPlayed, bossesWon[], owned[], equipped{}, ledger{}, rewardQueue[], scrolls[], run{id, cards, index, phase}, pips, streak, settings}`. Every change is one readwrite transaction on it. Counters only go up.
- **Idempotent awards:** each award has an id, recorded in `ledger` in the same transaction; a repeated id is skipped. Ids: `card:<runId>:<index>`, `say:<runId>:<index>`, `pips:<n>`, `duel:<roundId>:<pair>`, `level:<N>`, `talent:<N>`, `boss:<zone>`, `day:<local date>`, `verse:<week>`, `unlock:<trophyId>`.
- **Answer awards** commit at the answer tap, before the reveal shows.
- **Level-ups:** after any XP award, in the same transaction, handle every level crossed (one award can cross several): apply each level's reward and talent once and push one `rewardQueue` entry per level, in order. Then run the trophy check (11.2).
- **Derived on every render, never stored:** zone locks, boss ribbons, Sound Duel lock.
- **Scrolls and `bossesWon`** are sets; adding twice does nothing.
- **Reward queue:** shown after the current Got it (or at run, round, or boss end), one entry per screen; each Got it removes its entry in one transaction. It drains before the rest screen or the Map.
- **Resume:** `run.phase` is `question` or `reveal`. A kill on a reveal resumes on that reveal with no new award.
- **Launch order:** sword tap → reconcile (11.3) → `rewardQueue` → weekly verse if due → run or Map.
- **Restore** replaces the whole record in one transaction, then reconciles.

## 11. My Stuff and the trophy case

No shop and no spending. Every cosmetic in `trophies` (17) is earned automatically.

### 11.1 My Stuff (the avatar button)

- **Tabs:** Jewels, Gear, Themes (`trophies[].cat`), chunky tab buttons, English bold over Thai.
- **"You earned this!" shelf** across the top with her newest trophies.
- **Grid:** 3 columns of square trophy cards (Cream plate, Ink outline, Stone rim): big picture, English name bold, Thai under it.
  - **Earned:** full color; the equipped one has a Gold glow and a ✓.
  - **Not yet:** greyed, with its goal from `uiText` ("Unlocks at level 6", "Fill the coins 10 times", "Play on 5 days", "Win 2 boss battles") and a Gold progress bar.
- **Tap an earned trophy:** equips it instantly with a live avatar preview. Free, reversible, no confirm; it never changes XP, level, counters, or `owned`. One per `slot`; tapping the equipped sparkle or jewel again unequips it. A locked trophy only shows its goal.
- **Jewels:** every earned jewel sits on the jewel shelf by her avatar on the Map; the `featuredJewel` also sits on the avatar frame.
- **Gear is visual only:** sword, cape, tunic tint, and the right-answer sparkle (400 ms on the chosen plate). Nothing makes a question easier.
- **Defaults** (`unlock.type: "start"`) are owned from first launch. `state.equipped` persists choices.

### 11.2 Unlocks

- **Goals** (`trophies[].unlock`): `level`, `pipFills`, `daysPlayed` (distinct days played), `bossesWon`. Early ones land on day 1–2; the gold jewel needs all 5 bosses.
- **Trophy check:** inside the same transaction as every XP, coin, day, or boss award. Each trophy whose goal is met and whose `unlock:<id>` isn't in the ledger is added to `owned`, ledgered, and queued as a "You earned this!" screen (picture, `rewardText`, name, "Wear it", Got it).

### 11.3 Reconcile on launch

- Recompute every goal from the counters; grant any met-but-missing trophy through the trophy check. Never remove an earned trophy.
- Drop duplicate `owned` ids and any `equipped` id not owned (fall back to the default).

## 12. Sound Duel (level 3)

- The Echo Knight plays two similar words (light/right, three/tree, thirteen/thirty); she taps the one she heard. Rounds of 8 pairs, untimed, no score, can't be lost.
- +10 XP per right answer, +30 per round. Free "Hear it again" replays both slowly. Right answers fill coins; misses never dim them.

## 13. Day streak

- A "Days with English" flame in the Map top bar. A missed day pauses it and never resets it. On return: `welcomeBack` ("Welcome back! Your streak waited for you." / "ยินดีต้อนรับกลับ! วันเรียนของคุณยังอยู่ครบ"). With Rest weeks on, the flame shows a moon.

## 14. Daily rest (five minutes)

- The timer counts active play only: it stops when paused, backgrounded, or after 60 s without a tap.
- After 5 active minutes she finishes the current run, then sees `restScreen` ("Great work, come back tomorrow." / "เก่งมาก พรุ่งนี้มาเล่นต่อนะ") with Matthew 11:28. No clock or countdown.
- "Keep going" always works; Settings and both real-life zones stay reachable.

## 15. Bible verses

- **Boss scrolls:** Phonics Genesis 1:1; Colors and Shapes Genesis 9:13; Numbers John 6:9; Sight Words 1 Samuel 17:45; Baby and Hospital Isaiah 40:11. Saved to the Scrolls tile.
- **Weekly verse:** on her first open each week (Monday to Sunday), marked seen only on Got it. Rotation from Monday, Nov 2, 2026: Psalm 23:1; Philippians 4:13; Isaiah 41:10; Proverbs 3:5; John 3:16; Psalm 139:14; Joshua 1:9 (week of Dec 14); Luke 2:11 (Dec 21); Romans 8:28 (Dec 28); Psalm 46:1 (Jan 4).
- **Verse screen (scrolls and weekly):** a cream parchment panel with a Gold and metal frame: the reference, the English verse bold, **the Thai verse directly under the English**, tap to hear, then at the bottom one small line `uiText.askMax` ("If you don't know the meaning, ask Max and he can help you." / Thai, NEEDS NANCY), then Got it.
- **Thai verse text** is pasted word for word from the Thai Standard Version, never generated. Until then the data holds `[PASTE-TSV: reference]`: never display it; show English plus the askMax line.

## 16. Cards

- **156 cards** in `cards.json`: 152 written plus 4 empty personal slots. Format:
  `{id, zone, type, mode, en, th, thDef?, thDefStatus?, respell, pic, choices:[{en}×4], answer, hint{letters, sound, word}, trap, trapType, trapNote, fill, tag, easy, faith, personal, nursePhrase, thStatus}`.
  - `picture` cards: `mode: "picture-recall"`, with `pic` and `hint`; `answer` and `trap` are among the choices.
  - `say-it` cards: `mode: "english-first"`, `choices: []`, `answer: null`.
  - `nursePhrase: true` marks `bh-01` to `bh-10` for the Thai Review Queue.
- **Top-level data:** `zones` (`order`, `path`, `openLevel`, `zoneClip`, `boss` with `appearsAtLevel`, `cards`, `clip`, `scroll`), `soundDuel`, `picPlan`, `trophies`, `trophyRules`, `uiText`, `encouragement` (7), `rewardText`, `wrongText`, `welcomeBack`, `restScreen`, `gotItText`, `rewardClips`, `needsMaxwell`, `meta`. File strings win over any Thai in this spec.
- **Traps** are sound-alikes for Thai speakers (R/L, TH, V/W, dropped endings).
- **Thai:** Build never writes or edits Thai. Every Thai string is a draft with `thStatus: "NEEDS NANCY"` and still shows, with a tiny dot only Maxwell's Backup view explains. A card with no Thai shows English and respelling only.
- **Personal cards:** 75 are `personal:true` (71 written plus the 4 slots), such as "crib" and "Welcome to our hotel." Written ones sort first (7.8); unwritten ones are skipped.
- **Inn examples** in Maxwell Says carry an "Example" tag and `fill:true`: ms-04 "Check-out is at eleven." / "เช็คเอาท์ 11 โมงค่ะ"; ms-05 "Breakfast is at seven thirty." / "อาหารเช้าเจ็ดโมงครึ่งค่ะ"; ms-06 "One night is one hundred twenty dollars." / "คืนละ 120 ดอลลาร์ค่ะ".
- **Approved 7-word exceptions:** `ms-06` and `bh-14` ("Is it a boy or a girl?").
- **Maxwell's voice, 16 clips, each skipped if missing:** 6 zone clips (`maxwell-<zone>.m4a`, first visit), 5 reward clips (`maxwell-reward-1..5.m4a`, random on rewards), 5 boss clips (`maxwell-boss-<zone>.m4a`).

## 17. Personal card slots

Four empty say-it cards wait for Maxwell (`fill:true`, `personal:true`, empty `en`, `th`, `respell`), skipped until written, then sorted first: `bh-30` the baby; `ms-28` the hotel; `ms-29` Maxwell, her husband; `ms-30` faith.

**Needs Maxwell list** (`needsMaxwell`): `ms-04`, `ms-05`, `ms-06`, `bh-30`, `ms-28`, `ms-29`, `ms-30`. He fills them in `cards.json` or through the Backup view's list.

## 18. Thai Review Queue

Everything starts `NEEDS NANCY`: the 152 written cards (`ph-01`–`ph-24`, `cs-01`–`cs-24`, `sw-01`–`sw-24`, `nm-01`–`nm-24`, `bh-01`–`bh-29`, `ms-01`–`ms-27`), the 15 `thDef` hints, `gotItText`, every `uiText` entry, the 7 encouragement lines, the 17 trophy names, and any slot Maxwell fills. The Backup view lists them; Nancy taps ✓ (confirm) or ✎ (Maxwell edits). Review the `nursePhrase` cards and the `thDef` hints first.

## 19. Build order: one paste, four stages

After each stage, `window.__test()` must print `PASS` before the next. Never rewrite an earlier stage unless its test fails.

1. **Core loop:** sword screen, 3 cards, question and reveal screens, Hint, XP bar, coin meter, review.
   - The question screen never shows the English answer: `pic` (or fallback) plus the Thai line above 4 text choices.
   - Every picture card's `answer` and `trap` are among its choices.
   - The reveal shows English, respelling, and Thai, and is still there after 10 s.
   - A hint earns +10; a miss dims only 1 coin. First hint tap shows `hint.letters`; the next shows an encouragement line.
   - Review opens with one easy card and caps at 3. Personal cards sort first; unwritten cards are skipped.
   - Say-it cards show Got it and no choices.
   - Killing the app on a reveal resumes on that reveal with XP unchanged. Double-tapping Got it advances one card.
   - Filling ten coins plays the glow pulse and adds 1 to `pipFills`.
   - No red fills anywhere.
2. **Map, levels, rewards:**
   - The Map appears at level 2 as a 2×4 grid of identical tiles.
   - Colors closed below 6, Numbers below 8, Sight Words below 10, Sound Duel below 3.
   - Boss ribbons at levels 4, 7, 9, 13 and 16, each with 10 cards.
   - One award crossing two levels grants both levels' rewards once and queues two screens.
   - Winning a boss twice gives its scroll and `bossesWon` entry once.
   - A met trophy goal unlocks once, in the award's transaction, with one "You earned this!" screen.
   - Killing the app with 2 queued rewards shows both on relaunch, then none.
3. **Sound Duel:** no timer; misses never dim coins.
4. **Offline, Settings, My Stuff, trophies, Talents, streak, rest, verses:**
   - Works in airplane mode with Thai showing. Later launches resume correctly, with audio.
   - The timer stops in the background and after 60 s idle. A missed day pauses the streak.
   - A missed Monday still delivers that week's verse; verse screens show Thai under English (English only while the TSV placeholder remains) plus the askMax line.
   - Trophies: a forced transaction failure during an award leaves XP, counters, and trophies unchanged; killing on an unlock screen shows it once on relaunch; a trophy removed from a test state comes back on reconcile; none is granted twice.
   - My Stuff: equipping persists across reload and never changes XP, level, counters, or `owned`; a locked trophy can't be equipped.
   - Privacy scan of every shipped file (HTML, JS, CSS, JSON, manifest, service worker): no telephone-scheme links (`tel` URLs), no phone numbers (`/(\+?1[\s.-]?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}/`), no email addresses (`/[\w.+-]+@[\w-]+\.[\w.]+/`).

## 20. Maxwell's iPhone checks

- Mid-transition screenshots show no bleed-through. Contrast holds in daylight on the green screens. Thai tone marks aren't clipped. Every emoji picture renders. The coins look like gold coins at arm's length. Airplane mode works. Audio plays on the second launch.

## 21. Safety rules from the dry run (all applied above)

1. No spending anywhere; trophies unlock automatically (fixes the old shop eating currency).
2. Trophy check runs inside the award transaction; ledger `unlock:<id>`.
3. Launch reconcile grants met-but-missing trophies.
4. Rest timer stops after 60 s idle (reveal no longer auto-advances).
5. Answer awards commit at the tap with an id; resume re-shows the reveal without re-awarding.
6. Got it locks until the next screen.
7. Level-ups and unlocks go to the persisted `rewardQueue`, shown after Got it.
8. Every crossed level is processed, then the trophy check.
9. Boss win, scrolls, and `bossesWon` are once per zone.
10. Boss win commits before its animation; the scroll waits in the queue.
11. Continue resumes the AudioContext and replays the English.
12. `daysPlayed` counts once per local date.
13. No reload while a reward screen is open.
14. Weekly verse is marked seen only on Got it.
15. One launch order (section 10).
16. The hint button gives encouragement only on the reveal.
17. Equip checks `owned`; reconcile clears bad `equipped` ids.
