# Nancy's Adventure English — v5-15 Master Build Prompt

Single source of truth. Card data comes from the companion file `nancys-adventure-english-v5-15-cards.json`, attached with this prompt and saved in the build as `cards.json`. The card file wins on all card content.

## 0. Why this exists

**You are seen, loved, and capable.** Every screen should say that to Nancy, Maxwell's Thai-speaking wife.

- Every system asks: does this make her feel capable? If not, cut it.
- Personal meaning leads: Maxwell's voice, her hotel work, her baby, her faith. The game skin is Maxwell's joy. Nancy's joy is being seen and succeeding.
- Rewards read `rewardText` ("You earned this!"), never "Unlocked."
- Rest is a gift, and a pause is mercy for a season of life. Nothing ever breaks or fails.

## 1. Rules

1. **Three-second rule:** every screen is clear in 3 seconds without Maxwell.
2. **XP is the only points.** It never goes down. Gold coins are only the visual pip meter; cosmetics are trophies earned automatically (section 11).
3. **Flow:** the challenge sits just above her skill, with clear goals and instant feedback.
4. **One new thing per level and per screen.** A level gives at most one new zone, boss, or feature, plus one small reward (a cosmetic or a talent point).
5. **No voice recognition.** She speaks aloud on the honor system.
6. **Pregnancy safe:** no shake, nothing flashing more than 3 times a second, no sudden loud sounds.
7. **Thai on every instruction and label,** shown the moment it appears. Every on-screen label comes from the file's strings (`uiText`, `rewardText`, `wrongText`, `welcomeBack`, `restScreen`, `gotItText`, zone and trophy names); Build never hardcodes label text.
8. **Text hierarchy** wherever English and Thai appear together: English on top, bold and larger; Thai underneath, regular, about 75% size, secondary color. Exception: the question screen hides the English answer (6.4).
9. **Nothing red or alarming** anywhere.
10. **Maxwell is in the room during play.** The app has no phone links and no contact features.
11. **No orphans:** nothing references a removed system, every `cards.json` field and `uiText` key is used, and every field this spec names exists in the file.

## 2. Privacy (public web app)

- No personal contact info (phone numbers, addresses, emails) and no phone links are ever in any publicly deployed version: source, `cards.json`, service worker cache, or manifest.
- Card text holds no surnames, addresses, birth or due dates, phone numbers or emails. The first names Max and Maxwell are allowed.
- Personal progress lives on the device only, in IndexedDB. The app makes no network calls except fetching its own files.

## 3. Look: chunky cartoon strategy-game style

Original SVG/CSS art in a bright, cel-shaded mobile-strategy style ("Clash of Clans feel"), with no copied assets, characters, logos, or fonts. No online images. Put `<!-- Private family use. Original art. -->` at the top of `index.html`. Match any attached mockups.

- **Cel-shaded:** flat fills, one hard shadow tone, one highlight band; no airbrush gradients on objects.
- **Outlines:** 3–4 px Ink `#10170F` on every button, tile, panel, and drawn icon.
- **Metal buttons** (every button, tab, switch, and zone tile; original CSS, no copied assets):
  - **Face:** brushed iron, `linear-gradient(180deg, #8A939C, #5E6770 45%, #4A525A 55%, #6B747D)` plus `repeating-linear-gradient(90deg, rgba(255,255,255,.04) 0 1px, transparent 1px 3px)`.
  - **Rim:** 3 px bevel (light top `#B9C2CA`, dark bottom `#2C3238`), 4 corner rivets (6 px radial-gradient dots `#D9DEE3`→`#4A525A`, 8 px in), 4 px Ink outline, 18 px radius, 6 px drop edge `#23282D`. On press it sinks 4 px (edge to 2 px) in 80 ms and pops back.
  - **Label plate:** text always sits on a dark inset plate (`#1A1F24` at 85%, 10 px radius) so the texture never touches letters.
  - **English:** Lilita One, Hero Yellow `#FFD100`, 3 px Ink stroke (`paint-order: stroke fill`), drop shadow `0 2px 0 #000`, at least 18 px.
  - **Thai:** under it, Kanit, Cream, at least 15 px.
  - **Variants:** Gold-plated (`#FFE07A`→`#C9971A`) for Got it; locked tiles use dark iron with Stone-light `#C9CED3` text and a lock.
- **Panels, CSS only:** stone plates (gray gradients plus rivet dots) and metal trim (steel gradient, 1 px light top edge). No wood surfaces.
- **Layout:** each screen has a thin top bar, one main area, and a bottom bar; no modal on a modal. Everything she taps sits in the lower 60%.
- **Motion:** slide-and-pulse transitions, not flips. A bouncing Gold arrow (1.2 s, 8 px) marks the next step. Calm Motion, or `prefers-reduced-motion`, swaps every move for a 150 ms fade or brightness flash.
- **Opaque layers:** nothing behind a moving element shows through.
- **Screen title banner** on every screen except the sword screen: a metal-and-gold ribbon at the top, English in Hero Yellow (24 px), Thai under it (16 px). Titles: Map `uiText.titleMap` (the Map is the main menu; there is no separate menu screen), My Stuff `uiText.myStuff` (the one name for the trophy case), Scrolls `uiText.scrolls`, Talents `uiText.talents`, Sound Duel `uiText.soundDuel`, Settings `uiText.titleSettings`, weekly verse `uiText.verseOfWeek`, character `uiText.forestRanger`; a zone run shows the zone `name`/`nameTh`; a boss run shows `zones[].boss.name`.

**Menu palette** (Map, My Stuff, Scrolls, Talents, Settings, reward and verse screens; AA-checked):

| Token | Hex | Use |
|---|---|---|
| Forest | `#0E3B22` | app background (grass gradient to `#145A32`) |
| Meadow | `#17633A` | panels, top bar |
| Grass | `#2FA84F` | highlight bands; dark text only |
| Gold | `#FFCC33` | coins, trophies, arrow, right-answer glow |
| Gold Edge | `#B7860B` | coin rim |
| Hero Yellow | `#FFD100` | English on buttons and title banners |
| XP Track | `#2B1752` | XP bar trough |
| XP Purple | `#6D3CC9` | XP bar fill |
| XP Lilac | `#B79BFF` | XP fill top highlight band |
| Cream | `#FFF8E1` | text on dark, Thai on buttons, picture frame |
| Stone | `#5B6670` / `#D9DEE3` | locked tiles, Settings plates |
| Moonstone | `#9DB4CC` | soft "missed" glow |
| Ink | `#10170F` | outlines, text on light plates |

Contrast: Hero Yellow on the label plate 9.1 over iron, 7.5 over polished steel, 8.9 over gold; Cream Thai on the plate 10.3 or more; locked text 8.4; Cream on Forest 11.9, on Meadow 6.9; Ink on Cream 17.2; white XP label on XP Purple 6.7. Never white text on Grass (3.1). High Contrast makes the label plate solid Ink (Hero Yellow 12.5).

**Fonts** (self-hosted in `/fonts/`, never a CDN): English display and buttons in **Lilita One** (OFL). Thai in **Kanit** (Thai subset); fallback `Kanit, "Sukhumvit Set", Thonburi, "Noto Sans Thai", sans-serif`. Respellings in Kanit 500, Gold.

**XP bar and coin meter:**

- **XP bar:** XP Track trough, XP Purple fill with an XP Lilac highlight band, Ink outline, label "Level N" in white bold.
- **Coin meter (the ten pips),** directly under the XP bar and never merged with it: 10 original SVG gold coins (`svg:coin`). Each coin is round Gold with a thick Gold Edge rim, a simple embossed star-and-leaf mark in the center, a bright white highlight crescent at top-left, and a 3 px Ink outline. Empty: dim outline only (Gold Edge at 35%, no fill). Filled: the shiny coin with a 250 ms pop (scale 1→1.2→1).
- **Glow pulse:** when all ten coins fill, and on every level-up, the whole XP bar area glows a soft purple-gold for about 1 s, then returns to normal. With reduced motion, a simple 1 s brightness flash.

**Arena theme (gameplay screens only: card runs, boss runs, Sound Duel).** Clearly different from the menus:

| Token | Hex | Use |
|---|---|---|
| Arena Night | `#0B1B33` | background top, radial vignette at the edges |
| Arena Teal | `#0F3B4A` | background bottom, a soft grass-horizon silhouette `#123F35` |
| Star | Cream at 35% | 20–30 tiny static CSS dots in the top third |
| Panel Stone | `#5B6670` rim, parchment `#F3E6C4` inside | question panel framing the picture |
| Polished Steel | `#E3E8EC`→`#B8C1C9` with a bright specular band | choice plates: lighter than menu iron, same rim, rivets, label plate, Hero Yellow English |
| Aqua | `#7FE0D0` / edge `#3A9C8F` | hint button (Ink icon) |
| Zone tint | Phonics `#7FD38B`, Colors and Shapes `#F5A3C7`, Numbers `#7FB8F5`, Sight Words `#F5D06B`, Baby and Hospital `#F2B8A0`, Maxwell Says `#B79BFF` | arena banner and panel top stripe, Ink text |

Contrast: Cream on Arena Night 16.2 and on Arena Teal 11.3, Hero Yellow on the steel plate's label plate 7.5, Ink on parchment 14.7, Ink on Aqua 11.7, Gold on Arena Night 11.4, Ink on every zone tint at least 7.9. The XP bar keeps its purple; coins sit on a dark Arena Night strip with empty coins at Gold Edge 45%. Got it is the Gold-plated variant. Menu iron tiles never appear in the arena.

- **Enter a run (about 400 ms):** the menu slides down and fades out, then the zone-tinted arena banner swoops in from the top with the zone name (English bold, Thai under it) and settles into the top bar. **Exit** reverses it. Reduced motion: a 200 ms crossfade.
- The `<body>` carries `data-theme="menu"` or `data-theme="arena"`; all theme colors come from CSS variables under those two selectors.

## 4. Tech

- **App:** a PWA in vanilla HTML/CSS/JS with `manifest.json` (`display: standalone`, theme and background `#0E3B22`), `apple-mobile-web-app-capable`, `viewport-fit=cover`, and `env(safe-area-inset-*)` insets.
- **Thai:** `lang="th"` and `line-height: 1.7` on every Thai string.
- **Storage:** IndexedDB object store `kv`, key `state` (one record, section 10), mirrored to localStorage after each commit. Call `navigator.storage.persist()`.
- **Home screen:** the icon avoids Safari's 7-day wipe (iOS may still clear data when storage is low). In plain Safari, show only `uiText.openFromHome`.
- **Service worker:** cache-first, versioned. Core files (HTML, JS, CSS, fonts, SVGs, sound effects, `cards.json`) go through `cache.addAll`; each voice clip in `/audio/` is cached on its own, failures ignored. Never reload mid-run or while a reward screen is open; show a `uiText.updateReady` chip on the Map.
- **Audio:** Web Audio API; decode each clip on first play; a missing or failed clip is skipped silently. English `speechSynthesis` at 0.85 (0.6 in Slow Mode); no Thai voice means Thai audio is skipped.
- **Audio wake:** the sword tap on each launch and every `uiText.continue` tap resume the AudioContext and play a silent buffer. Nothing waits on audio.
- **Locks:** one answer per card; Got it locks until the next screen renders.
- **Auto-pause:** on `visibilitychange` to hidden and on `pagehide`, pause the run, stop audio and the play timer. On return show `uiText.continue`, then the exact screen she left.

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

- Only the sword and `uiText.pickUpSword`. The tap wakes audio.
- Then follow the launch order (section 10): first launch goes to card 1; an unfinished run resumes at its exact card or reveal; otherwise the Map (or the next Phonics run before the Map is earned).
- The XP bar fades in after card 1, the coin meter after card 3.

### 6.2 Character

After card 5, one panel with the Forest Ranger preselected. One tap on `uiText.go` keeps it. Cosmetic only.

### 6.3 Map (main menu, earned at level 2)

- **Top bar:** the avatar button (opens My Stuff) with featured jewel, title, and jewel shelf; a Gold trophy counter (earned of 32); the `uiText.daysWithEnglish` flame; the Talents book (from level 5); the gear.
- **Zone grid:** 2 columns × 4 rows of identical tiles, 12 pt gaps, 16 pt side margins: Phonics, Colors and Shapes / Numbers, Sight Words / Baby and Hospital, Maxwell Says / Sound Duel, Scrolls.
- **Tile:** about 164 × 120 pt on a 375 pt screen; a metal button with a zone-tint stripe on top, the zone emblem (48 pt), and the label plate with the English name and Thai.
- **Closed tiles:** Stone gray with a lock and a level plate (`uiText.levelN`). Sound Duel stays locked until level 3.
- **Boss ready:** a Gold ribbon across the tile corner, `uiText.boss`. One bouncing Gold arrow points at the next step.
- **Before level 2:** only two big tiles, Baby and Hospital and Maxwell Says, in the same style.

### 6.4 Question screen (picture-recall cards)

Top to bottom:

1. Top bar: the XP bar, the coin meter under it, the gear.
2. Question panel: the picture frame (section 5) inside the stone-and-parchment panel with the zone-tint stripe. The English answer is never shown here.
3. **Thai line** directly above the choices (Kanit 18 pt, Cream 80%): `thDef` if present, else `th`. 15 cards carry `thDef` (the 14 fallback cards plus ph-17 "they"): a 2–4 word Thai hint rather than a translation.
4. **Choices:** a 2×2 grid of polished-steel plates (section 3), at least 96 pt tall, shuffled every card. The only English she reads before answering.
5. **Hint button:** on every question screen, bottom-left in the safe area, a 56 pt Aqua round button with a metal rim and a leaf-heart icon (`uiText.hintButton` as its accessible label), at least 16 pt from the choices. There is no HELP button on any screen; this soft hint button replaces it, by Maxwell's decision.

### 6.5 Reveal screen (after every picture-card answer)

- **Header:** `rewardText` on a right answer, `wrongText` on a miss.
- **Body:** the picture, the English answer bold (Lilita One 34 pt), the respelling in Gold, the Thai under it; after a miss, the card's `trapNote` (Thai tip) under that. `faith` cards get a small gold leaf mark. The English is spoken once automatically.
- **Prompt:** `uiText.sayItOutLoud` on the first 10 reveals.
- **Buttons:** 🔊 `uiText.replay`, `uiText.sayItToMaxwell` (full-screen card to read to him, +2 XP once per card), and a big Gold-plated **Got it** (`gotItText`).
- **Never auto-advances.** Only Got it moves on. The hint button here gives encouragement only.

### 6.6 Talents

A stone tablet with 3 nodes. A lit node means she owns it; tapping one previews it.

### 6.7 Settings (the gear)

- Four metal switches: `uiText.highContrast`, `calmMotion` (on automatically with iOS Reduce Motion), `slowMode`, `restWeeks`.
- Maxwell section: `backup`/`restore` as JSON, the `needsMaxwell` list (cards and unpasted verses), and the `thaiReview` queue.

### 6.8 Scrolls

A shelf of earned boss scrolls and past weekly verses, newest first. Tapping one opens its verse screen (section 15).

## 7. Core loop

A **run** is 10 cards from one zone, each `picture` or `say-it`.

1. A soft cue plays. The question screen shows the picture and Thai line; nothing is spoken, so she recalls the word herself.
2. She taps one of the four text choices. Near-miss traps stay (play/pray, crib/rib, thirteen/thirty).
3. **Right:** the plate pulses Gold, +10 XP is committed, one coin fills, then the reveal.
4. **Wrong:** the tapped plate glows Moonstone, the right one glows Gold, a soft chime plays, one filled coin dims quietly, then the reveal with `wrongText`. The card returns 3 to 5 cards later, at most twice.
5. **Coin meter:** when all ten coins are filled, the glow pulse plays, `pipFills` +1 is committed, and the coins reset.
6. **Hint:** always free; a right answer after it still earns +10.
   - First tap on a question: shows `hint.letters` (for example "p___" or "P_____ w___ h___.") and speaks `uiText.itStartsWith` plus `hint.sound` ("ขึ้นต้นด้วยเสียง /p/").
   - Further taps, and taps anywhere else: the next line from `encouragement` ("I love you.") in a soft bubble for 3 s.
7. **Review:** cards missed in her most recent completed session, even days ago.
8. **Run order:** at most 2 `faith:true` cards per run; skip unwritten cards (`fill:true`, empty `en`); open with one `easy:true` card (every zone has at least 2), preferring her zone; then written `personal:true` cards; then up to 3 review cards; then the rest.

## 8. Say-it cards

37 cards are `type: "say-it"`, `mode: "english-first"`: 33 written plus the 4 empty slots (section 17). They include the hospital phrases `bh-01` to `bh-10` (`nursePhrase: true`).

- English bold on top, respelling, Thai underneath; the English is spoken. She says it aloud and taps **Got it**.
- No choices, no picture, no wrong answer. +10 XP and one coin; never dims a coin.
- Hint replays the phrase slowly. Never in boss runs.

## 9. XP, levels, rewards

- XP to reach level 2: 60 (her first run); level 3: 250 total (day 1); after that 100 + 60 × (L − 3) more per level. Cap: level 20.
- **Levels 2 to 4 focus on Phonics on purpose.** Baby and Hospital and Maxwell Says stay open; Colors and Numbers open at 6 and 8.

| Zone | Opens | Focus levels | Boss at |
|---|---|---|---|
| Phonics | 1 | 1–4 | 4 |
| Baby and Hospital | 1 | 1–7 | 7 |
| Colors and Shapes | 6 | 6–9 | 9 |
| Numbers | 8 | 8–13 | 13 |
| Sight Words | 10 | 10–16 | 16 |
| Maxwell Says | 1 | none | none |

- **Boss:** exactly the 10 picture cards in `zones[].boss.cards`, ready at the top level of the zone's focus range. Its guardian (`boss.name`) has a bar that drops on each right answer; a boss can't be lost.
- **Boss win (once per zone):** the guardian kneels, a "You earned this!" banner, `bossesWon` adds the zone, the scroll unrolls (section 15), Maxwell's boss clip plays (visuals play even if it's missing). Replays give card XP only.
- **Level features:** 2 the Map; 3 Sound Duel; 5 Talents; zones open at 6, 8, 10; bosses at 4, 7, 9, 13, 16; talent points at 5, 7, 12. **Level cosmetics:** each is the `trophies` entry with `unlock: {type: "level", n}` (17, levels 2–20; level 20 gives a title and its crown frame). Rule 4 holds: at most one feature plus one small reward per level.
- **Talents:** Smooth Slide, Big XP Flash, Right-Answer Glow (`uiText.talent*`).
- **Reward screens:** a Cream-and-Gold panel with the picture, English bold, Thai under it, and Got it. Never auto-advance.

## 10. State, awards, resume

- **One state record** `kv/state`: `{xp, level, pipFills, daysPlayed, bossesWon[], owned[], equipped{}, ledger{}, rewardQueue[], scrolls[], run{id, cards, index, phase}, pips, streak, settings}`. Every change is one readwrite transaction on it. Counters only go up.
- **Idempotent awards:** each award has an id, recorded in `ledger` in the same transaction; a repeated id is skipped. Ids: `card:<runId>:<index>`, `say:<runId>:<index>`, `tell:<runId>:<index>` (Say it to Maxwell), `pips:<n>`, `duel:<roundId>:<pair>`, `round:<roundId>`, `level:<N>`, `talent:<N>`, `boss:<zone>`, `day:<local date>`, `verse:<week>`, `unlock:<trophyId>`.
- **Answer awards** commit at the answer tap, before the reveal shows.
- **Level-ups:** after any XP award, in the same transaction, handle every level crossed (one award can cross several): apply each level's reward and talent once and push one `rewardQueue` entry per level, in order. Then run the trophy check (11.2).
- **Derived on every render, never stored:** zone locks, boss ribbons, Sound Duel lock.
- **Scrolls and `bossesWon`** are sets; adding twice does nothing.
- **Reward queue:** shown after the current Got it (or at run, round, or boss end), one entry per screen; each Got it removes its entry in one transaction. It drains before the rest screen or the Map.
- **Resume:** `run.phase` is `question` or `reveal`. A kill on a reveal resumes on that reveal with no new award.
- **Launch order:** sword tap → reconcile (11.3) → `rewardQueue` → weekly verse if due → run or Map.
- **Restore** replaces the whole record in one transaction, then reconciles.

## 11. My Stuff (the trophy case)

Every cosmetic is one of the 32 `trophies`, earned automatically: 5 jewels, 9 gear, 13 themes, 5 titles; 17 of them unlock by level.

### 11.1 My Stuff screen (from the avatar button)

- **Tabs:** `uiText.jewels`, `gear`, `themes`, `titles` (`trophies[].cat`), chunky tab buttons, English bold over Thai.
- **`uiText.earnedShelf` shelf** across the top with her newest trophies.
- **Grid:** 3 columns of square trophy cards (Cream plate, Ink outline, Stone rim): big picture, English name bold, Thai under it.
  - **Earned:** full color; the equipped one has a Gold glow, a ✓, and `uiText.wearing`.
  - **Not yet:** greyed, with its goal from `uiText` ("Unlocks at level 6", "Fill the coins 10 times", "Play on 5 days", "Win 2 boss battles") and a Gold progress bar.
- **Tap an earned trophy:** equips it instantly with a live avatar preview. Free, reversible, no confirm; it never changes XP, level, counters, or `owned`. One per `slot` (`trophyRules.slots`); `cardFrame` holds one of oak, silver, gold, or hearts; `title` shows under her avatar. Tapping an equipped optional item (sparkle, jewel, frame, title, map extras) again unequips it. A locked trophy only shows its goal.
- **Jewels:** every earned jewel sits on the jewel shelf by her avatar on the Map; the `featuredJewel` also sits on the avatar frame.
- **Where slots render:** `sword`, `cape`, `tunic`, `avatarFrame`, `featuredJewel`, `title` on the avatar; `mapTheme`, `mapLanterns`, `mapPet`, `arrowTrail` on the Map; `cardFrame` around the question panel; `restSky` on the rest screen; `swordSplash` on the sword screen; `sparkle` on right answers.
- **Gear is visual only:** sword, cape, tunic tint, and the right-answer sparkle (400 ms on the chosen plate). Nothing makes a question easier.
- **Defaults** (`unlock.type: "start"`) are owned from first launch. `state.equipped` persists choices.

### 11.2 Unlocks

- **Goals** (`trophies[].unlock`): `start`, `level`, `pipFills`, `daysPlayed` (distinct days played), `bossesWon`. Early ones land on day 1–2; the gold jewel needs all 5 bosses.
- **Trophy check:** inside the same transaction as every XP, coin, day, or boss award. Each trophy whose goal is met and whose `unlock:<id>` isn't in the ledger is added to `owned`, ledgered, and queued as a "You earned this!" screen (picture, `rewardText`, name, `uiText.wearIt`, Got it).

### 11.3 Reconcile on launch

- Recompute every goal from the counters; grant any met-but-missing trophy through the trophy check. Never remove an earned trophy.
- Drop duplicate `owned` ids and any `equipped` id not owned (fall back to the default).

## 12. Sound Duel (level 3)

- The Echo Knight (`uiText.echoKnight`) plays two similar words (light/right, three/tree, thirteen/thirty); she taps the one she heard. Rounds of 8 pairs, untimed, no score, can't be lost.
- +10 XP per right answer, +30 per round. Free `uiText.hearItAgain` replays both slowly. Right answers fill coins; misses never dim them.

## 13. Day streak

- The `uiText.daysWithEnglish` flame in the Map top bar. A missed day pauses it and never resets it. On return: `welcomeBack`. With Rest weeks on, the flame shows a moon.

## 14. Daily rest (five minutes)

- The timer counts active play only: it stops when paused, backgrounded, or after 60 s without a tap.
- After 5 active minutes she finishes the current run, then sees `restScreen` with `verses.rest`. No clock or countdown.
- `uiText.keepGoing` always works; Settings and both real-life zones stay reachable.

## 15. Bible verses

- **Boss scrolls** (`zones[].boss.scroll`): Phonics Genesis 1:1; Colors and Shapes Genesis 9:13; Numbers John 6:9; Sight Words 1 Samuel 17:45; Baby and Hospital Isaiah 40:11. Saved to Scrolls (6.8).
- **Weekly verse** (`verses.weekly`, 10, from `verses.weeklyStart`): on her first open each week (Monday to Sunday), titled `uiText.verseOfWeek`, marked seen only on Got it. Rotation from Monday, Nov 2, 2026: Psalm 23:1; Philippians 4:13; Isaiah 41:10; Proverbs 3:5; John 3:16; Psalm 139:14; Joshua 1:9 (week of Dec 14); Luke 2:11 (Dec 21); Romans 8:28 (Dec 28); Psalm 46:1 (Jan 4).
- **Verse screen (scrolls and weekly):** a cream parchment panel with a Gold and metal frame: the reference, the English verse bold, **the Thai verse directly under the English**, tap to hear, then at the bottom one small line `uiText.askMax` ("If you don't know the meaning, ask Max and he can help you."), then Got it.
- **Verse text is never generated.** Maxwell pastes the English (`en`, his chosen translation) and the Thai Standard Version (`th`) word for word over the `[PASTE-EN: ref]` and `[PASTE-TSV: ref]` placeholders (16 verses). Never display a placeholder: until pasted, show the reference, any pasted half, and the askMax line.

## 16. Cards

- **156 cards** in `cards.json`: 152 written plus 4 empty personal slots. Format:
  `{id, zone, type, mode, en, th, thDef?, thDefStatus?, respell, pic, choices:[{en}×4], answer, hint{letters, sound, word}, trap, trapNote, fill, tag, easy, faith, personal, slot?, nursePhrase, thStatus}`.
  - `hint.word` (the word `hint.sound` comes from) is underlined in `hint.letters`. `trapNote` shows on a miss. `tag: "Example"` shows `uiText.example`. `slot` names an empty slot's topic.
  - `picture` cards: `mode: "picture-recall"`, with `pic` and `hint`; `answer` and `trap` are among the choices.
  - `say-it` cards: `mode: "english-first"`, `choices: []`, `answer: null`.
  - `nursePhrase: true` marks `bh-01` to `bh-10` for the Thai Review Queue.
- **Top-level data:** `zones` (`key`, `name`, `nameTh`, `order`, `startZone`, `openLevel`, `zoneClip`, `cardIds`, `boss` with `appearsAtLevel`, `cards`, `clip`, `name`, `scroll`), `soundDuel.pairs`, `verses`, `picPlan`, `trophies`, `trophyRules`, `uiText` (48), `encouragement` (7), `rewardText`, `wrongText`, `welcomeBack`, `restScreen`, `gotItText`, `rewardClips`, `needsMaxwell`, `meta`. File strings win over any Thai in this spec.
- **Traps** are sound-alikes for Thai speakers (R/L, TH, V/W, dropped endings).
- **Thai:** Build never writes or edits Thai. Every Thai string is a `NEEDS NANCY` draft and still shows, with a tiny dot only the Backup view explains.
- **Personal cards:** 75 are `personal:true` (71 written plus the 4 slots). Written ones sort first (7.8).
- **Inn examples:** `ms-04`, `ms-05`, `ms-06` are hypothetical (Example tag, `fill:true`) until Maxwell confirms them.
- **Approved 7-word exceptions:** `ms-06` and `bh-14` ("Is it a boy or a girl?").
- **Maxwell's voice, 16 clips, each skipped if missing:** 6 zone clips (`maxwell-<zone>.m4a`, first visit), 5 reward clips (`maxwell-reward-1..5.m4a`, random on rewards), 5 boss clips (`maxwell-boss-<zone>.m4a`).

## 17. Personal card slots

Four empty say-it cards wait for Maxwell (`fill:true`, `personal:true`, empty `en`, `th`, `respell`), skipped until written, then sorted first: `bh-30` the baby; `ms-28` the hotel; `ms-29` Maxwell, her husband; `ms-30` faith.

**Needs Maxwell list** (`needsMaxwell`): `ms-04`, `ms-05`, `ms-06`, `bh-30`, `ms-28`, `ms-29`, `ms-30`, plus the 16 unpasted verses. He fills them in `cards.json` or through the Backup view's list.

## 18. Thai Review Queue

Everything starts `NEEDS NANCY`: the 152 written cards, the 15 `thDef` hints, `gotItText`, all 48 `uiText` entries (labels, screen titles, settings, talents), the 5 boss names, the 7 encouragement lines, the 32 trophy names, and any slot Maxwell fills. The Backup view lists them; Nancy taps ✓ (confirm) or ✎ (Maxwell edits). Review the `nursePhrase` cards and the `thDef` hints first.

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
   - No red fills anywhere. Every button label sits on a label plate, English Hero Yellow at least 18 px, Thai at least 15 px.
   - Card, boss, and Sound Duel screens render with `data-theme="arena"` (Arena Night background, polished-steel plates); Map, My Stuff, Scrolls, and Settings render with `data-theme="menu"` and no arena colors. Entering and leaving a run plays the banner transition (crossfade with reduced motion).
2. **Map, levels, rewards:**
   - The Map appears at level 2 as a 2×4 grid of identical tiles.
   - Colors closed below 6, Numbers below 8, Sight Words below 10, Sound Duel below 3.
   - Boss ribbons at levels 4, 7, 9, 13 and 16, each with 10 cards.
   - One award crossing two levels grants both levels' rewards once and queues two screens.
   - Winning a boss twice gives its scroll and `bossesWon` entry once.
   - Every level reward cosmetic exists in `trophies`; a met trophy goal unlocks once, in the award's transaction, with one "You earned this!" screen.
   - Killing the app with 2 queued rewards shows both on relaunch, then none.
   - Every screen except the sword screen shows its title banner from the file (Map, My Stuff, Scrolls, Talents, Sound Duel, Settings, weekly verse, character, each zone run, each boss run).
3. **Sound Duel:** no timer; misses never dim coins.
4. **Offline, Settings, My Stuff, trophies, Talents, streak, rest, verses:**
   - Works in airplane mode with Thai showing. Later launches resume correctly, with audio.
   - The timer stops in the background and after 60 s idle. A missed day pauses the streak.
   - A missed Monday still delivers that week's verse; verse screens show Thai under English (English only while the TSV placeholder remains) plus the askMax line.
   - Trophies: a forced transaction failure during an award leaves XP, counters, and trophies unchanged; killing on an unlock screen shows it once on relaunch; a trophy removed from a test state comes back on reconcile; none is granted twice.
   - My Stuff: equipping persists across reload and never changes XP, level, counters, or `owned`; a locked trophy can't be equipped.
   - Privacy scan of every shipped file (HTML, JS, CSS, JSON, manifest, service worker): no telephone-scheme links (`tel` URLs), no phone numbers (`/(?<!\d)(\+?1[\s.-]?)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}(?!\d)/`), no email addresses (`/[\w.+-]+@[\w-]+\.[\w.]+/`).

## 20. Maxwell's iPhone checks

- Mid-transition screenshots show no bleed-through. Contrast holds in daylight; yellow button text reads without squinting. Thai tone marks aren't clipped. Every emoji picture renders. The coins look like gold coins at arm's length. Airplane mode works. Audio plays on the second launch.

## 21. Dry-run fixes (applied above)

Earned-only cosmetics; awards, level-ups, and unlocks in one ledgered transaction; launch reconcile; persisted `rewardQueue`; Got it lock; 60 s idle timer stop; resume without re-award; Continue resumes audio; verse seen only on Got it; one launch order.
