# Nancy's Adventure English — FINAL Build Prompt

## HOW TO USE THIS PROMPT

1. Paste this entire document into Grok Build. It holds the full spec; the card data is in the attached `nancys-adventure-english-v5-20-cards.json`.
2. Do not generate Thai. Every Thai string is a NEEDS NANCY draft; use it exactly as written. The 16 Bible verses are verified ESV and THSV11 text, and the 6 Jesus words are bible.com ESV and THSV11 text; show them exactly as written.
3. Pictures: each picture card's `pic` is an emoji (render it), `svg:<id>`, or `null` (zone-emblem fallback). Draw 47 SVGs: `picPlan.svg` (29 of 37; 8 are supplied in `picPlan.inlineSvg`), `picPlan.trophySvg` (17 of 21; 4 are supplied in `picPlan.trophyInlineSvg`), `picPlan.uiSvg` (the gold coin).
4. Build in the four stages of section 19; each must print `PASS` before the next.

---

Single source of truth. Card data comes from the companion file `nancys-adventure-english-v5-20-cards.json`, attached with this prompt and saved in the build as `cards.json`. The card file wins on all card content.

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

## 2. Permanent standards (public web app)

These two rules carry equal weight and are never traded off.

- **No personal info:** no personal contact info (phone numbers, addresses, emails) and no phone links are ever in any publicly deployed version: source, `cards.json`, service worker cache, or manifest.
- Card text holds no surnames, addresses, birth or due dates, phone numbers or emails. The first names Max and Maxwell are allowed.
- Personal progress lives on the device only, in IndexedDB. The app makes no network calls except fetching its own files.
- **Scripture is never purchasable:** Bible verses are NEVER purchasable. No shop item, coin/gem/currency cost, or unlock gate that requires spending anything to read scripture. Verses are free gifts (grace): given by week, boss win, or rest, never as purchases. (`verses.graceRule`)
  - A verse arrives as a gift (weekly verse, boss scroll, rest verse), framed with `uiText.verseGift` ("A gift for you"), never "You earned this!".
  - No verse is given by level. Once given, a verse stays on the Scrolls shelf free to reread forever: never locked, hidden, removed, or reset (restore and reconcile keep it).
  - No shop, currency, or spending anywhere: coins are only the pip meter; nothing is ever deducted for a verse; no verse has a `cost` or `price` field.
- **Never list:** no countdowns or wait timers, energy or lives, withering, stock or offers, pay-to-skip, leaderboards, push notifications, app-icon badges, or reminder prompts.

## 3. Look: chunky cartoon strategy-game style

Original SVG/CSS art in a bright, cel-shaded mobile-strategy style ("Clash of Clans feel"); no copied assets, logos, or fonts; no online images. Put `<!-- Private family use. Original art. -->` at the top of `index.html`. Match any attached mockups.

- **Cel-shaded:** flat fills, one hard shadow tone, one highlight band; no airbrush gradients on objects.
- **Outlines:** 3–4 px Ink `#10170F` on every button, tile, panel, and drawn icon.
- **Metal buttons** (every button, tab, switch, and zone tile; original CSS, no copied assets):
  - **Face:** brushed iron, `linear-gradient(180deg, #8A939C, #5E6770 45%, #4A525A 55%, #6B747D)` plus `repeating-linear-gradient(90deg, rgba(255,255,255,.04) 0 1px, transparent 1px 3px)`.
  - **Rim:** 3 px bevel (light top `#B9C2CA`, dark bottom `#2C3238`), 4 corner rivets (6 px radial-gradient dots `#D9DEE3`→`#4A525A`, 8 px in), 4 px Ink outline, 18 px radius, 6 px drop edge `#23282D`. On press it sinks 4 px (edge to 2 px) in 80 ms and pops back.
  - **Label plate:** text always sits on a dark inset plate (`#1A1F24` at 85%, 10 px radius) so the texture never touches letters.
  - **English:** Lilita One, Hero Yellow `#FFD100`, 3 px Ink stroke (`paint-order: stroke fill`), drop shadow `0 2px 0 #000`, at least 20 px.
  - **Thai:** under it, Kanit, Cream, at least 17 px.
  - **Press sound:** only these yellow-text metal plate buttons (iron buttons, tabs, zone tiles, choice plates, Got it) play a soft low metal thud on press: original Web Audio synthesis, never a recorded or game file; a sine thump gliding 90 to 55 Hz plus a faint metallic ring (1.8 and 2.6 kHz partials), 5 ms attack, gone by 160 ms, peak gain 0.25 (moderate, pregnancy safe). The gear button and everything in Settings are silent; other taps keep only the sounds this spec names.
  - **Variants:** Gold-plated (`#FFE07A`→`#C9971A`) for Got it; locked tiles use dark iron with Stone-light `#C9CED3` text and a lock.
- **Panels, CSS only:** stone plates and steel trim; no wood surfaces.
- **Layout:** a thin top bar, one main area, a bottom bar; no modal on a modal. Everything she taps sits in the lower 60%. Only tappable things look like buttons; titles, labels, and the HUD are flat.
- **4-across rows** (My Stuff grid and tabs, and any other): `display:grid; grid-template-columns:repeat(4,1fr); gap:6pt; padding-inline:max(6pt,env(safe-area-inset-left)) max(6pt,env(safe-area-inset-right))`: every four-across row fills the full width with equal small gutters; no max-width, no centering, no extra side margin.
- **Main button spot:** Got it, Continue, Keep going, and next round share one spot: fills the row beside the hint button, at least 64 pt tall, bottom third.
- **Motion:** slide-and-pulse transitions, not flips. A bouncing Gold arrow (1.2 s, 8 px) marks the next step (after a pause, Continue). Calm Motion, or `prefers-reduced-motion`, swaps every move for a 150 ms fade or brightness flash.
- **Opaque layers:** nothing behind a moving element shows through.
- **Back control:** a small metal `uiText.toMap` button at top-left on every screen except the sword screen, the Map, reward screens (every `rewardQueue` entry, including a boss scroll), and the weekly verse; those leave only by Got it, so the queue always drains first (section 10). Mid-run it keeps the run; tapping that zone again (or the next launch) resumes it.
- **Screen title banner** on every screen except the sword screen: a flat gold ribbon at the top (no bevel, rivets, plate, shadow, or press state; never looks tappable), English in Hero Yellow (26 px), Thai under it (18 px). Titles: Map `uiText.titleMap` (the Map is the main menu; there is no separate menu screen), My Stuff `uiText.myStuff` (the one name for the trophy case), Scrolls `uiText.scrolls`, Talents `uiText.talents`, Sound Duel `uiText.soundDuel`, Settings `uiText.titleSettings`, weekly verse `uiText.verseOfWeek`, a scroll opened from the shelf `uiText.scrolls`, reward and unlock screens `rewardText` (a verse screen given as a gift uses `uiText.verseGift`), rest screen `restScreen`, character `uiText.classGuardian` (her starting class); a zone run shows the zone `name`/`nameTh`; a boss run shows `zones[].boss.name`.

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
| Stone | `#5B6670` / `#D9DEE3` | Settings plates, frame rims |
| Moonstone | `#9DB4CC` | soft "missed" glow |
| Ink | `#10170F` | outlines, text on light plates |

AA contrast: Hero Yellow on label plates 7.5–9.1, Cream Thai 10.3+, locked text 8.4, Cream on Forest 11.9 and Meadow 6.9, white on XP Purple 6.7. Never white on Grass (3.1). High Contrast makes label plates solid Ink.

**Fonts** (self-hosted in `/fonts/`, never a CDN): English display and buttons in **Lilita One** (OFL). Thai in **Kanit** (Thai subset); fallback `Kanit, "Sukhumvit Set", Thonburi, "Noto Sans Thai", sans-serif`. Respellings in Kanit 500, Gold.

**XP bar and coin meter:**

- **XP bar:** 28 pt tall, XP Track trough, XP Purple fill with an XP Lilac highlight band, Ink outline, label "Level N" in white bold.
- **Coin meter (the ten pips),** under the XP bar, never merged: 10 original SVG gold coins (`svg:coin`, 30 pt): Gold face, thick Gold Edge rim, embossed star-and-leaf mark, white highlight crescent, 3 px Ink outline. Empty: outline only (Gold Edge 35%). Filled: shiny, with a 250 ms pop; filled coins always stay full bright.
- **Glow pulse:** when all ten coins fill and on every level-up, the XP bar area glows soft purple-gold for about 1 s (reduced motion: a brightness flash).

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

AA contrast: Cream on Arena Night 16.2 and Teal 11.3, Ink on parchment 14.7, on Aqua 11.7, on zone tints 7.9+. Coins sit on a dark strip (empty coins at Gold Edge 45%). Got it is Gold-plated. Menu iron tiles never appear in the arena.

- **Enter a run (about 400 ms):** the menu slides down and fades out, then the zone-tinted arena banner (a flat title ribbon, never button-styled) swoops in with the zone name (or boss name) and settles into the top bar. **Exit** means leaving the arena for the Map, either by `uiText.toMap` or after a run's last Got it and reward queue; it plays the same transition reversed. Reduced motion: a 200 ms crossfade.
- **HUD** (in-game bar, every arena screen, in the top bar inside the safe area): her small, cute 40 pt corner portrait in all equipped gear, her jewel count, and her equipped weapon and cape icons. Flat, not tappable, no button styling; never overlaps the picture, choices, hint, or main button spot; redraws on the same frame as any change.
- **Cheer and nod:** the HUD portrait raises its arms on a right answer and on a wrong one gives a small encouraging nod (head tilts up, about 600 ms; never a droop): about 600 ms, CSS transform only on the avatar's arm and head groups, gentle, never mocking; reduced motion: none. The animated Map hero is v6.
- The `<body>` carries `data-theme="menu"` or `data-theme="arena"`; all theme colors come from CSS variables under those two selectors.

## 4. Tech

- **App:** a PWA in vanilla HTML/CSS/JS with `manifest.json` (`display: standalone`, theme and background `#0E3B22`), `apple-mobile-web-app-capable`, `viewport-fit=cover`, and `env(safe-area-inset-*)` insets.
- **Thai:** `lang="th"` and `line-height: 1.7` on every Thai string.
- **Storage:** IndexedDB object store `kv`, key `state` (one record, section 10), mirrored to localStorage after each commit. Call `navigator.storage.persist()`.
- **Home screen:** the icon avoids Safari's 7-day wipe (iOS may still clear data when storage is low). In plain Safari, show only `uiText.openFromHome`.
- **Service worker:** cache-first, versioned. Core files (HTML, JS, CSS, fonts, SVGs, sound effects, `cards.json`) go through `cache.addAll`; each voice clip in `/audio/` is cached on its own, failures ignored. When a new version is cached, show a `uiText.updateReady` chip on the Map only; tapping it saves state, then reloads into the new version. Never reload mid-run, mid-card, or on a reward screen. Mid-run means on an arena screen; on the Map, tapping the chip reloads, and the run resumes.
- **Audio:** Web Audio API; decode each clip on first play; a missing or failed clip is skipped silently. English `speechSynthesis` at 0.85 (0.6 in Slow Mode); no Thai voice means Thai audio is skipped. Verses are never spoken in Thai (section 15).
- **Audio wake:** the sword tap on each launch and every `uiText.continue` tap resume the AudioContext and play a silent buffer. Continue resumes audio and replays the English of the screen she left (a reveal, say-it card, or verse); a question screen speaks nothing, so nothing replays there; on Sound Duel, Continue replays the current pair. Nothing waits on audio.
- **Locks:** one answer per card; Got it locks until the next screen renders.
- **Auto-pause:** on `visibilitychange` to hidden and on `pagehide`, pause the run, stop audio and the play timer. On return show `uiText.continue`, then the exact screen she left.

## 5. Pictures

- **Picture recall** (the 123 `mode: "picture-recall"` cards) shows one picture of the answer from `pic`:
  - **Emoji** (an emoji string, sometimes two or three like "👶💤" or "☀️👶🛏️", scaled together to fit the frame): Apple Color Emoji at 120 pt, centered. 71 cards. The newest emoji used are Emoji 13.0 (🫂 `ph-07`, 🪨 `ph-12`, 🪙 `nm-04`, 🛻 `ms-22`, and the ZWJ sequence 👰‍♀️ `ph-06`; iOS 14.2+); no skin tones. If a glyph does not render (canvas width test on first launch), that card uses the null fallback.
  - **SVG** (`svg:<id>`): the 37 ids in `picPlan.svg` (29 drawn in the section 3 style, 8 supplied; `high-five` and `pray-kneel` are also `ms-31`'s two buttons). Color cards use flat swatches; size cards show two objects with the target outlined in Gold. 38 cards (`svg:hungry` and `svg:pray-kneel` are shared; `svg:tie` is ms-32); clock times are digital.
  - **Fallback** (`null`): the zone emblem at 40% opacity, with the Thai line moved into the frame at 28 pt as the prompt. 14 abstract cards.
- **At a glance (Maxwell's rule):** Every picture card must be unambiguous at a glance on a phone screen. If the image could fit two choices, or two choices look or sound alike (e.g., crib/rib), swap the wrong choice or redraw the image. Draw the ids in `picPlan.svgNotes` exactly as noted.
- **Supplied art:** `picPlan.inlineSvg` holds 8 ready SVGs: crib, front-desk, towel, towel-white, tie from Openclipart (CC0 public domain, so no credit line) and the original pray-kneel (`ph-08`, `ms-11`, `ms-31`), pray-meal (`ms-12`) and high-five (`ms-31`) (`picPlan.inlineSvgSource`); `picPlan.trophyInlineSvg` holds 4 original trophy icons: the brown bow for `bow-oak`, the silver and gold card borders, and the blue-flame lantern (`trophyInlineSvgSource`). Every id inside a supplied SVG is prefixed with its asset name, so inlined SVGs never collide. Inline them exactly as given; never redraw them; a `picPlan.svgNotes` entry for a supplied id is ignored.
- **Picture frame:** Cream plate, 4 px Ink outline, 18 px radius, stone-and-metal rim, about 200 pt square. Never blank or broken; an emoji that renders as an empty box uses the fallback.
- **Drawings Build makes: 47** = 29 card ids (`picPlan.svg` minus `picPlan.inlineSvg`; `svgDrawnCount`) + 17 trophy ids (`picPlan.trophySvg` minus `picPlan.trophyInlineSvg`; `trophySvgDrawnCount`) + 1 coin (`picPlan.uiSvg`). Plus 6 zone emblems, the avatar, and UI icons (leaf hint, trophy, lock, check, scroll, flame, book; the gear is never drawn: it is supplied as `picPlan.uiInlineSvg.gear`).
- **Say-it cards** are `mode: "english-first"` (section 8): no picture, no hidden word.

## 6. Screens

### 6.1 Sword screen (every launch)

- Only the sword and `uiText.pickUpSword`. The tap wakes audio.
- Then follow the launch order (section 10): first launch goes to card 1 of a Phonics run (`startZone`); an unfinished run resumes at its exact card or reveal; otherwise the Map.
- The XP bar fades in after card 1, the coin meter after card 3.

### 6.2 Character

After card 5, one panel with her hero (Defender, iron sword) preselected; the class line under her reads `uiText.classGuardian`. One tap on `uiText.go` keeps it. Cosmetic only.

### 6.3 Map (main menu; full map earned at level 2)

- **Top bar:** the avatar button (opens My Stuff) with featured jewel, title, and jewel shelf; a 32 pt Gold trophy counter (earned of 38); the `uiText.daysWithEnglish` flame (`picPlan.trophyStyle.streakFlame`); the Talents book (from level 5); the gear.

`meta.mapStyle` picks the layout: `regions` (6.3a, current) or `grid` (6.3b, the v5-19 grid), so one edit swaps back. Each style is one self-contained component plus one CSS block.

#### 6.3a Region map (`mapLayout`)

- **Shape:** a static, original illustrated parchment map (section 3 style; no animation), a portrait diamond filling the main area. The 4 `mapLayout.regions` sit at `pos` (percent of the map): top Phonics + Sight Words (meadow, `color` green), left Colors and Shapes + Numbers (golden fields), right Baby and Hospital + Maxwell Says (lake and red hills), bottom Sound Duel (a gentle twilight wood with lantern gold; nothing scary).
- **Paths:** dashed Ink paths (`pathStyle`: 3 px, 8-6 dash) for each `paths` pair (top-left, top-right, left-bottom, right-bottom; none cross), each ending in an X marker at the next region's entrance.
- **Taps:** each region cluster is one tap target of at least 44 × 44 pt (about 150 × 150 pt); tapping it opens its zone, or a two-plate chooser (zone `name`/`nameTh`) when it holds two open zones; `soundDuel` opens Sound Duel. Region names (`en`/`th`) are flat labels, 17 pt or larger. The bottom region sits in thumb reach.
- **Not reached yet:** a region with no open zone is grayed (60% desaturated) with `uiText.unlocksAtLevel` for its first zone's `openLevel`; a closed zone inside an open region shows the same line on its plate. Player-facing text never says locked. Zone open levels are unchanged, so the top and right regions are in color from level 1 and the left (level 6) and bottom (level 3) start grayed. Before level 2 the grayed regions are faint outlines; level 2 (`uiText.fullMap`) draws them in full.
- **Boss ready:** the region gets the Gold `uiText.boss` ribbon. Her still hero (about 96 pt) stands by her next step, with the Gold arrow.
- **Re-render:** her hero and the Map slots (`mapTheme`, `mapLanterns`, `mapPet`, `arrowTrail`) update on the same frame a trophy is worn (11.2), in both styles.
- Scrolls is in My Stuff (11.1), not on the map.

#### 6.3b Grid (`meta.mapStyle: "grid"`)

- **Zone grid** (`mapLayout.grid`): 2 columns × 4 rows of identical tiles, 12 pt gaps, 16 pt side margins: Phonics, Colors and Shapes / Numbers, Sight Words / Baby and Hospital, Maxwell Says / Sound Duel, Scrolls.
- **Tile:** about 164 × 120 pt on a 375 pt screen; a metal button with a zone-tint stripe on top, the zone emblem (48 pt), and the label plate with the English name and Thai.
- **Closed tiles:** dark iron with a lock and a level plate (`uiText.levelN`); a tap pulses the plate and the arrow points to her next step. Sound Duel stays locked until level 3.
- **Hero:** her hero, in all equipped gear, stands still about 96 pt tall on the Map above the grid.
- **Boss ready:** a Gold ribbon across the tile corner, `uiText.boss`. One bouncing Gold arrow points at the next step.
- **Before level 2:** the Map shows only the three start zones (Phonics, Baby and Hospital, Maxwell Says) as big tiles, plus the Scrolls tile as soon as it holds a verse (scripture is never behind a level once given); the Scrolls tile is never locked; level 2 reveals the full grid (reward screen `uiText.fullMap`).

### 6.4 Question screen (picture-recall cards)

Top to bottom:

1. Top bar: the HUD, the XP bar, the coin meter under it, the gear.
2. Question panel: the picture frame (section 5) inside the stone-and-parchment panel with the zone-tint stripe. The English answer is never shown here.
3. **Thai line** directly above the choices (Kanit 20 pt, Cream 80%): `thDef` if present, else `th`. 15 cards carry `thDef` (the 14 fallback cards plus ph-17 "they"): a 2–4 word Thai hint rather than a translation.
4. **Choices:** a 2×2 grid of polished-steel plates (section 3), at least 96 pt tall, shuffled every card. The only English she reads before answering. Every picture card uses this one layout: picture centered at the top, Thai line, then the 4 plates in a 2×2 grid with an even 12 pt gap. If any choice wraps past two lines on the iPhone SE, all four stack 1×4 with the same 12 pt gap. Strings never carry doubled or trailing spaces.
5. **Hint button:** on every question screen, bottom-left in the safe area, a 72 pt Aqua round button with a thick metal rim, a soft Aqua glow, and a leaf-heart icon, with `uiText.wordsForYou` under it (`uiText.hintButton` as its accessible label), at least 16 pt from the choices. There is no HELP button on any screen; this soft hint button replaces it, by Maxwell's decision.

### 6.5 Reveal screen (after every picture-card answer)

- **Header:** the next `encouragement` line on a right answer, `wrongText` on a miss. `rewardText` ("You earned this!") never shows here; it appears only as the banner of reward screens (section 9).
- **Body:** the picture, the English answer bold (Lilita One 36 pt), the respelling in Gold, the Thai under it; after a miss, the card's `trapNote` (Thai tip) under that. `faith` cards get a small gold leaf mark. The English is spoken once automatically.
- **Prompt:** `uiText.sayItOutLoud` on the first 10 reveals.
- **Buttons:** 🔊 `uiText.replay` and a Gold-plated **Got it** (`gotItText`) in the main button spot.
- **Never auto-advances.** Only Got it moves on. The hint button here gives encouragement only.

### 6.6 Talents

A stone tablet with 3 nodes. A lit node means she owns it; tapping one previews it.

### 6.7 Settings (the gear)

- **Gear icon** (top bar, opens Settings): `picPlan.uiInlineSvg.gear` exactly: a solid, connected 8-tooth cog with a center hole; no gaps or rays; silent.
- Four metal switches: `uiText.highContrast`, `calmMotion` (on automatically with iOS Reduce Motion), `slowMode`, `restWeeks`.
- Maxwell section: `backup`/`restore` as JSON, the `needsMaxwell` list (7 cards), the `thaiReview` queue, and the small `verses.attribution` credit line.

### 6.8 Scrolls

A shelf of the boss scrolls and weekly verses she has been given, and the rest verse once seen, newest first, each free to reread any time; tapping one opens its verse screen (section 15). Empty shelf: `uiText.scrollsEmpty`. The `verses.attribution` credit line sits small at the bottom of the shelf.

## 7. Core loop

A **run** is 10 cards from one zone, each `picture`, `say-it`, or `two-answer`. After the 10th card's Got it, the reward queue drains, then the rest screen (if due) or the Map.

1. A soft cue plays. The question screen shows the picture and Thai line; nothing is spoken, so she recalls the word herself.
2. She taps one of the four text choices. Near-miss traps stay (play/pray, thirteen/thirty) only where the picture rules them out (section 5).
3. **Right:** within 150 ms of the tap (state and glow on the same frame; sounds preloaded; the save never delays it), the plate pulses Gold, +10 XP is committed, one coin fills, then the reveal.
4. **Wrong:** within 150 ms of the tap (same rule), the tapped plate glows Moonstone, the right one glows Gold, a soft chime plays, the meter removes one filled coin if any are filled (none in Baby and Hospital; at 0 nothing changes; no dimming; the rest stay full bright), then the reveal with `wrongText`. The card returns 3 to 5 cards later, at most twice, except in boss runs (section 9). The two-answer card is the exception: a wrong tap there never removes a coin or XP (section 8.1).
5. **Coin meter:** when all ten coins are filled, the glow pulse plays, `pipFills` +1 is committed, and the coins reset.
6. **Hint:** always free; a right answer after it still earns +10.
   - First tap on a question: shows `hint.letters` (for example "p___" or "P_____ w___ h___.") and speaks `uiText.itStartsWith` plus `hint.sound` ("ขึ้นต้นด้วยเสียง /p/").
   - Further taps, and taps anywhere else, alternate in a soft bubble: the next `encouragement` line ("I love you.", 3 s), then her next Jesus word (`jesusWords`, section 15; until tapped or 6 s): the `ref` and `uiText.jesusWords` small, English bold, Thai, `thGloss` small. On the question screen, Jesus words are shown, not spoken; on the reveal, encouragement only. She starts with the 2 with `given.type: "start"`; each of 4 gear pieces brings one more (`given.gear`, in that gear's unlock transaction), 6 at most. Once she has seen all of hers this visit (session memory only), one `uiText.jesusAllHeard` bubble; the next tap starts them over. No timer or countdown. An empty entry shows a `jesusWordsFallback` line instead.
7. **Review queue:** a missed card's id goes into the small localStorage key `naeReviewQueue` (unique ids, oldest first, at most 20; a right answer on that card removes it). On her next visit (a new app open), up to 2 queued cards missed on an earlier visit appear within the first 3 cards of her first run (right after the easy opener): cards from that zone first, then from any open zone; never in boss runs. No new UI, label, timer, or penalty; they score like any card. Only picture-recall misses enter it (say-it and two-answer cards never do). If the key is missing or not valid JSON, the queue is empty and is rewritten; an empty queue simply adds no cards. The key sits outside `state` and is not in backups; losing it loses nothing. Full Leitner boxes stay in v6.
8. **Run order:** at most 2 `faith:true` cards per run; skip unwritten cards (`fill:true`, empty `en`); open with one `easy:true` card (every zone has at least 2), preferring her zone; then, on a new visit, up to 2 review-queue cards (step 7); then written `personal:true` cards; then the rest, at most 3 never-seen (`seen`) once the zone has 7 seen.

## 8. Say-it cards

37 cards are `type: "say-it"`, `mode: "english-first"`: 33 written plus the 4 empty slots (section 17). They include the hospital phrases `bh-01` to `bh-10` (`nursePhrase: true`).

- English bold on top, respelling, Thai underneath; the English is spoken. She says it aloud and taps **Got it**.
- No choices, no picture, no wrong answer. +10 XP and one coin; never removes a coin.
- Hint replays the phrase slowly. Never in boss runs.

### 8.1 Two-answer card (pray or high five)

`ms-31` (`type`/`mode` `"two-answer"`) breaks the normal formula: no reveal, no auto-advance, and a wrong tap costs nothing.

- **Prompt:** each time, one of its 2 `prompts` at random: English bold, Thai under it, English spoken once. The card's `en`/`th` are the Thai Review Queue summary only.
- **Buttons:** two big picture buttons from `choices` (`svg:pray-kneel`, a small kneeling person with folded hands, `uiText.pray`; `svg:high-five`, two hands slapping with a burst, `uiText.highFive`; both supplied in `picPlan.inlineSvg`, never emoji), at least 120 pt, no press sound; the prompt's `answer` is the right `key`.
- **Right tap:** Gold glow, +10 XP and one coin (once per card), then `uiText.done` in the main button spot; only Done advances, one card.
- **Wrong tap:** a soft Moonstone X fades over that button: no red, no buzzer, thud, or any sound, no shake, no `wrongText`, no droop (the small encouraging nod is fine). No coin is removed and no XP is lost (the exception to section 7's coin rule). Then the right one glows Gold; tapping it still earns +10 XP and one coin.
- Hint replays the prompt slowly; never in boss runs; counts as `faith:true`. Fits the iPhone SE without scrolling.

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

- **Boss:** exactly the 10 picture cards in `zones[].boss.cards`, ready at the top level of the zone's focus range. **Intro:** the Map's `uiText.boss` ribbon (on the region, or the tile in grid style) plus the arena banner showing `boss.name` on entry; no separate intro screen. **Run:** each card answered right drops the guardian's bar by one tenth; a missed card returns after the others, again until right. When all 10 are right the bar is empty and the guardian kneels. No failure state; `uiText.toMap` keeps progress.
- **Boss win (once per zone):** boss win commits before its animation; the scroll waits in the queue. The commit (`boss:<zone>` ledger, `bossesWon`, scroll pushed to `rewardQueue`) happens in one transaction when all 10 are right; a kill mid-animation loses nothing and shows the scroll on relaunch. Then, after the kneel, a boss-win screen shows the `rewardText` banner once (`bossesWon` already committed) with Got it; then, as its own separate screen, the scroll unrolls as a gift (section 15) under `uiText.verseGift` (the scroll screen never shows `rewardText`), Maxwell's boss clip plays (visuals play even if it's missing). Then the reward queue (scroll first). Replays give card XP only.
- **Level features** (`meta.levelFeatures`): 2 the full Map; 3 Sound Duel; 5 Talents; zones open at 6, 8, 10; bosses at 4, 7, 9, 13, 16; talent points at 5, 7, 12. **Level cosmetics:** each is the `trophies` entry with `unlock: {type: "level", n}` (17, levels 2–20; level 20 gives a title and its crown frame). Rule 4 holds: at most one feature plus one small reward per level.
- **Talents:** Smooth Slide, Big XP Flash, Right-Answer Glow (`uiText.talentSmoothSlide`, `uiText.talentXpFlash`, `uiText.talentGlow`).
- **Celebration** (level-up and new-zone reward screens): CSS-only ribbon drop and one fall of soft confetti, about 1.5 s; nothing flashes more than 3 times a second; no new sound; reduced motion: a 150 ms fade, no confetti.
- **Reward screens:** a Cream-and-Gold panel with the picture, English bold, Thai under it, and Got it; never auto-advance. `rewardText` shows once per screen, as the title banner, in English once and Thai once; never repeated in the body. A zone or feature reward shows that tile's emblem and name (zone `name`; level 2 `uiText.fullMap` with the Map emblem; `uiText.soundDuel`; `uiText.talents`); a talent point shows `uiText.talentPoint`.

## 10. State, awards, resume

- **One state record** `kv/state`: `{xp, level, pipFills, daysPlayed, bossesWon[], owned[], equipped{}, ledger{}, rewardQueue[], scrolls[], seen[], run{id, cards, index, phase}, pips, streak, settings}`. Every change is one readwrite transaction on it. Counters only go up. The record carries one version field, `schema: 5020`. On launch, if `schema` is missing or different, the saved playtest data is reset to a fresh start (Nancy has never installed an earlier version, so there is no migration code). Build never changes `schema` on its own: once Nancy has real progress, a version that changes it must ship a migration first (v6 list).
- **Idempotent awards:** each award has an id, recorded in `ledger` in the same transaction; a repeated id is skipped. Ids: `card:<runId>:<index>`, `say:<runId>:<index>`, `pips:<n>`, `duel:<roundId>:<pair>`, `round:<roundId>`, `level:<N>`, `talent:<N>`, `boss:<zone>`, `day:<local date>`, `verse:<week>`, `unlock:<trophyId>`.
- **Answer awards** commit at the answer tap, before the reveal shows.
- **Level-ups:** after any XP award, in the same transaction, handle every level crossed (one award can cross several): apply each level's reward and talent once and push one `rewardQueue` entry per level, in order. Then run the trophy check (11.2).
- **Derived on every render, never stored or cached:** every Map region, X marker, tile, and emblem (rebuilt from `zones` and `mapLayout` on each return and tab switch; never reuse old DOM or a one-time animation state), zone locks, boss ribbons, Sound Duel lock, the HUD.
- **Scrolls and `bossesWon`** are sets; adding twice does nothing.
- **Reward queue:** shown after the current Got it (or at run, round, or boss end), one entry per screen; each Got it removes its entry in one transaction. It drains before the rest screen or the Map.
- **Resume:** `run.phase` is `question` or `reveal`. A kill on a reveal resumes on that reveal with no new award.
- **Launch order:** sword tap → reconcile (11.3) → `rewardQueue` → weekly verse if due → run or Map.
- **Restore** replaces the whole record in one transaction, then reconciles.

## 11. My Stuff (the trophy case)

Every cosmetic is one of the 38 `trophies`, earned automatically: 5 jewels, 15 gear, 13 themes, 5 titles; 17 unlock by level. Gear (9 held items: 3 swords, sling, bow, 2 staffs, hammer, shield; gentle, never gory) comes only at start, by level, or by boss win, never bought; every name is unique and shows under the item in My Stuff and on its reward screen.

### 11.1 My Stuff screen (from the avatar button)

- **Scrolls:** a full-width `uiText.scrolls` metal button above the tabs opens the shelf (6.8); always there, never locked; the tabs stay a 4-across row (section 3 rule).
- **Tabs:** `uiText.jewels`, `gear`, `themes`, `titles` (`trophies[].cat`), chunky tab buttons, English bold over Thai.
- **`uiText.earnedShelf` shelf** ("My newest trophies") across the top with her newest trophies; it never repeats `rewardText`.
- **Grid:** 4-across (section 3) square trophy cards (Cream plate, Ink outline, Stone rim): picture about 80% of the card (sizes may vary a little), name bold, Thai under it (`th`; wherever a trophy's Thai shows, gear uses `thGloss`). Colors and sizes per `picPlan.trophyStyle` (`jewels`, `enlarged`).
  - **Earned:** full color; the equipped one has a Gold glow, a ✓, and `uiText.wearing`.
  - **Not yet:** full color, never grey or dim, a small lock icon at top-right, no 'locked' wording, and its goal from `uiText.unlocksAtLevel`, `unlocksPips`, `unlocksDays`, or `unlocksBosses` (by `unlock.type`) in a gifting tone ("Yours at level 6", "Yours after 2 boss wins") and a Gold progress bar.
- **Tap an earned trophy** (or `uiText.wearIt`): applies instantly: state and UI update on the same frame (avatar, HUD, ✓), then it commits to IndexedDB and the localStorage mirror; a Gold glow and soft chime of 300 ms or less never block input; repeat taps while applying are ignored. All trophy art is preloaded at launch in fixed-size cells, so nothing shifts or flickers; free, reversible, no confirm, and it never changes XP, level, counters, or `owned`. One per `slot` (`cardFrame`: oak, silver, gold, or hearts). Tapping an equipped optional item again unequips it. A locked trophy only shows its goal.
- **Jewels:** every earned jewel sits on the Map's jewel shelf.
- **Hero pose:** the weapon is held low at her side, never across her face (sword screen, Map, HUD, My Stuff).
- **Class line:** under her portrait (HUD, My Stuff, Map hero), the equipped weapon's `classTitle` (Maxwell's mapping; only weapons set the class): sling `uiText.classWarrior`, staffs `uiText.classMage`, hammer `uiText.classKnight`, the brown `bow-oak` `uiText.forestRanger`, swords `uiText.classGuardian`. The shield has no `classTitle`: with it equipped, the class line is hidden. Words only; no stats. Earned titles (`title` slot) still show on the avatar.
- **Where slots render:** `weapon`, `cape`, `tunic`, `avatarFrame`, `featuredJewel`, `title` on the avatar; `mapTheme`, `mapLanterns`, `mapPet`, `arrowTrail` on the Map; `cardFrame` around the question panel; `restSky` on the rest screen; `swordSplash` on the sword screen; `sparkle` on right answers.
- **Visual only:** no trophy makes a question easier; the sparkle is a 400 ms glint on the chosen plate.
- **Defaults** (`unlock.type: "start"`) are owned from first launch. `state.equipped` persists choices.

### 11.2 Unlocks

- **Goals** (`trophies[].unlock`): `start`, `level`, `pipFills`, `daysPlayed` (distinct days played), `bossesWon`. Early ones land on day 1–2; the gold jewel needs all 5 bosses.
- **Trophy check:** inside the same transaction as every XP, coin, day, or boss award. Each trophy whose goal is met and whose `unlock:<id>` isn't in the ledger is added to `owned`, ledgered, and queued as a reward screen: picture, name, `uiText.wearIt`, Got it, under the `rewardText` banner. rewardText shows once, as the banner; never repeated in the body.

### 11.3 Reconcile on launch

- Recompute every goal from the counters; grant any met-but-missing trophy through the trophy check. Never remove an earned trophy.
- Drop duplicate `owned` ids and any `equipped` id not owned (fall back to the default).

## 12. Sound Duel (level 3)

- The Echo Knight (`uiText.echoKnight`) plays two similar words (light/right, fine/file, thirteen/thirty); she taps the word tile she heard (English, no pictures). Rounds of 8 pairs, untimed, no score, can't be lost.
- +10 XP per right answer. Free `uiText.hearItAgain` replays both slowly. Right answers fill coins; misses never remove or dim a coin.
- **Round end:** `uiText.roundDone` with +30 XP, then Got it, then the reward queue, then a choice of the next round or `uiText.toMap`.

## 13. Day streak

- The `uiText.daysWithEnglish` flame in the Map top bar. A missed day pauses it and never resets it. On return: `welcomeBack`. With Rest weeks on, the flame shows a moon.

## 14. Daily rest (five minutes)

- The timer counts active play only: it stops when paused, backgrounded, or after 60 s without a tap.
- After 5 active minutes she finishes the current run, then sees `restScreen` with `verses.rest`, framed with `uiText.verseGift` the first time; once seen it joins the Scrolls shelf (section 2). No clock or countdown.
- `uiText.keepGoing` always works; Settings and both real-life zones stay reachable.

## 15. Bible verses

- **Boss scrolls** (`zones[].boss.scroll`): Phonics Genesis 1:1; Colors and Shapes Genesis 9:13; Numbers John 6:9; Sight Words 1 Samuel 17:45; Baby and Hospital Isaiah 40:11. Saved to Scrolls (6.8).
- **Weekly verse** (`verses.weekly`, 10, from `verses.weeklyStart`): on her first open each week (Monday to Sunday), titled `uiText.verseOfWeek`, marked seen only on Got it (ledger `verse:<week>`). If she leaves without Got it (closes or backgrounds the app), it shows again on the next launch, in the launch order (section 10). The rotation repeats every 10 weeks (`verses.rotation`). Order from Monday, Nov 2, 2026: Psalm 23:1; Philippians 4:13; Isaiah 41:10; Proverbs 3:5; John 3:16; Psalm 139:14; Joshua 1:9; Luke 2:11 (week of Dec 21); Romans 8:28; Psalm 46:1.
- **Verse screen (scrolls and weekly):** a cream parchment panel with a Gold and metal frame: when newly given, `uiText.verseGift` ("A gift for you") at the top; the reference, the English verse bold, **the Thai verse directly under the English**, tap to hear (English only), then at the bottom one small line `uiText.askMax` ("If you don't know the meaning, ask Max and he can help you."), then Got it.
- **Verse text is filled and verified (16 verses).** English is the ESV (`enSource`, bible.com version 59); Thai is the Thai Standard Version 2011, ฉบับมาตรฐาน, Thailand Bible Society (`thSource: "THSV11"`, bible.com version 174, Maxwell's choice). Each verse has `status: "VERIFIED"` and its `enUrl`/`thUrl`. Build never generates, edits, trims, capitalizes, or re-punctuates verse text; show it exactly as in the file. **Decided by Maxwell:** Isaiah 41:10 starts with a lowercase "fear not", exactly as the ESV prints it; shown exactly as printed, honesty over formatting (`verses.decided`). The unmatched quote marks in John 3:16, Joshua 1:9, and 1 Samuel 17:45 (including the orphan opening mark) also stay exactly as printed; never add or remove a quote mark. A `\n` in `en` or `th` is a poetry line break: render it as a line break, speak it as a pause (`verses.textRule`). Verse tap-to-hear speaks en only; never speak th. (`verses.ttsRule`) (The Thai is for her to read; no verse is ever spoken in Thai, even if a Thai voice exists.) If a half is ever empty, hide it and never speak it.
- **Jesus words** (`jesusWords`, 6; hint bubble only, never on Scrolls, never purchasable): whole verses of Jesus speaking, from the same bible.com versions, under the same text rules: never add or remove a quote mark (John 14:1 opens with one; John 8:12 keeps its narrator words and marks). `status: "VERIFIED"` (`verifiedBy`); Build shows them exactly as written. `thGloss` is separate helper text, never part of the verse or spoken.
- **Credits:** `verses.attribution` shows small on the Scrolls shelf and in Settings, each line word for word from its publisher: `esv` is Crossway's official copyright notice for digital works quoting more than one translation (crossway.org/permissions), and `thsv11` is the Thailand Bible Society's own credit for THSV11 as published with bible.com version 174 (four lines: Thai, then English; keep the `\n` breaks). Sources are in `esvSource` and `thsv11Source`. Never shorten or translate either. Per Crossway, each English verse carries a small `verses.attribution.esvTag` ("(ESV)") after it and each Thai verse a small `thsv11Tag` ("(THSV11)"). Show the tags as separate small text; never speak them or join them to the verse text. (`tagRule`)

## 16. Cards

- **161 cards** in `cards.json`: 157 written plus 4 empty personal slots. Format:
  `{id, zone, type, mode, en, th, thDef?, thDefStatus?, respell, pic, choices:[{en}×4], answer, hint{letters, sound, word}, trap, trapNote, fill, tag, easy, faith, personal, slot?, prompts?, nursePhrase, thStatus?}`. A card with no `thStatus` uses `meta.cardThStatusDefault` (`NEEDS NANCY`).
  - `hint.word` is data only (the word `hint.sound` comes from); never display it. `trapNote` shows on a miss. `tag: "Example"` shows `uiText.example`. `slot` names an empty slot's topic.
  - `picture` cards: `mode: "picture-recall"`, with `pic` and `hint`; `answer` and `trap` are among the choices.
  - `say-it` cards: `mode: "english-first"`, `choices: []`, `answer: null`.
  - `two-answer` cards (section 8.1): `mode: "two-answer"`, `choices` [{`en`, `key`, `pic`}]×2, `prompts` [{`key`, `en`, `th`, `respell`, `answer`}]×2, card `answer: null`.
  - `nursePhrase: true` marks `bh-01` to `bh-10` for the Thai Review Queue.
- **Top-level data:** `zones` (with `openLevel`, `zoneClip`, `nameThStatus`, `startZone` = Phonics, `cardIds`, and `boss` with `appearsAtLevel`, `name`, `cards`, `clip`, `scroll`), `soundDuel.pairs` (`a`, `b`; 30), `verses`, `jesusWords` (`given`, `thGloss`, `thGlossStatus`, `thGlossBy`), `jesusWordsFallback`, `picPlan` (with `inlineSvg`, `inlineSvgSource`, `trophyInlineSvg`, `trophyInlineSvgSource`, `uiInlineSvg`, `svgDrawnCount`, `trophySvgDrawnCount`), `trophies` (weapons carry `classTitle`), `trophyRules`, `mapLayout` (`regions` with `zones`, `place`, `pos`, `color`, `accent`; `paths`; `pathStyle`; `grid`; style chosen by `meta.mapStyle`), `uiText` (63), `encouragement` (7), `rewardText`, `wrongText`, `welcomeBack`, `restScreen`, `gotItText`, `rewardClips`, `needsMaxwell`, `meta`. File strings win over any Thai here.
- **Traps** are the nearest wrong choice: a sound-alike for Thai speakers (R/L, TH, V/W, dropped endings) only where the picture rules it out (section 5).
- **Thai:** Build never writes or edits Thai. Every Thai string is a `NEEDS NANCY` draft and still shows, with a tiny dot only the Backup view explains.
- **Personal cards:** 80 are `personal:true` (76 written plus the 4 slots). Written ones sort first (7.8).
- **Inn examples:** `ms-04`, `ms-05`, `ms-06` are hypothetical (Example tag, `fill:true`) until Maxwell confirms them.
- **Approved 7-word exceptions:** `ms-06` and `bh-14` ("Is it a boy or a girl?").
- **Maxwell's voice, 16 clips, each skipped if missing:** 6 zone clips (`maxwell-<zone>.m4a`, first visit), 5 reward clips (`maxwell-reward-1..5.m4a`, random on rewards), 5 boss clips (`maxwell-boss-<zone>.m4a`).

## 17. Personal card slots

Four empty say-it cards wait for Maxwell (`fill:true`, `personal:true`, empty `en`, `th`, `respell`), skipped until written, then sorted first: `bh-30` the baby; `ms-28` the hotel; `ms-29` Maxwell, her husband; `ms-30` faith.

**Needs Maxwell list** (`needsMaxwell`, 7): `ms-04`, `ms-05`, `ms-06`, `bh-30`, `ms-28`, `ms-29`, `ms-30`. He fills them in `cards.json` or through the Backup view's list. The 16 verses are already filled and verified.

## 18. Thai Review Queue

Everything starts `NEEDS NANCY`: the 157 written cards, the 15 `thDef` hints, `gotItText`, `rewardText`, `wrongText`, `welcomeBack`, `restScreen`, the 6 zone `nameTh` (`nameThStatus`), all 63 `uiText` entries, the 4 map region names (`instructorChecked` marks Instructor's), the 5 boss names, the 7 encouragement lines, 23 trophy names, the 15 gear `thGloss`, the 6 Jesus-word `thGloss`, the 2 `jesusWordsFallback` lines, and any slot Maxwell fills. Not in the queue: the 16 verses, the Jesus-word verse text, and `verses.attribution`, which are verified THSV11/ESV text (`status: "VERIFIED"`), never drafts. The Backup view lists the drafts; Nancy taps ✓ (confirm) or ✎ (Maxwell edits). Review the 10 `nursePhrase` cards first, then the `thDef` hints; gear and Jesus-word glosses go in Instructor's nightly batches after launch. The 3 sleepy and nap cards (`ph-25`, `ph-26`, `bh-31`) and the two-answer card `ms-31` are new drafts for Instructor's nightly batches after launch, not the first review. The tie card `ms-32` joins the same after-launch nightly batch; the Thai fixes from Instructor's 6:31 PM audit stay `NEEDS NANCY` too.

## 19. Build order: one paste, four stages

After each stage, `window.__test()` must print `PASS` before the next. Never rewrite an earlier stage unless its test fails.

1. **Core loop** (sword, 3 cards, question, reveal, Hint, XP bar, coins, review):
   - Question screens never show the English answer; `answer` and `trap` are among the choices.
   - The reveal is still there after 10 s; double-tapping Got it advances one card.
   - A hint earns +10; first tap shows `hint.letters`, the next an encouragement line; a miss removes one filled coin if any (none in Baby and Hospital; at 0 nothing changes); no dimming.
   - A run opens with one easy card; on a new visit, up to 2 cards missed on an earlier visit appear by card 3 (never more than 2 per visit); right and wrong feedback starts within 150 ms of the tap; personal cards first; unwritten cards skipped; at most 3 never-seen cards once the zone has 7 seen; say-it cards show Got it and no choices.
   - Hint taps alternate encouragement (3 s) and her given Jesus words (6 s or tap; shown, never spoken); a new player has exactly 2; after all are seen, `uiText.jesusAllHeard` once, then they start over; the HUD portrait cheers on right and gives a small encouraging nod on wrong (head tilts up, about 600 ms; never a droop).
   - A kill on a reveal resumes there with XP unchanged. Ten coins play the glow pulse and add 1 to `pipFills`.
   - No red fills. Button labels sit on label plates: English Hero Yellow 20 px+, Thai 17 px+; on iPhone SE nothing clips.
   - Card, boss, and Sound Duel screens use `data-theme="arena"`; menus use `data-theme="menu"` with no arena colors; enter and exit play the banner transition; the HUD sits in the top bar, flat, covering nothing.
   - Two-answer card `ms-31`: each showing picks one of its 2 `prompts` at random; right tap: Gold, +10 XP and one coin once, `uiText.done`; wrong tap: soft Moonstone X, no sound, coins and XP unchanged, then the right one glows Gold; only Done advances.
2. **Map, levels, rewards:**
   - Level 2 draws all four map regions in full (with `meta.mapStyle` `grid`, the 2×4 grid); Colors closed below 6, Numbers below 8, Sight Words below 10, Sound Duel below 3; boss ribbons at 4, 7, 9, 13, 16, each with 10 cards.
   - One award crossing two levels grants both rewards once and queues two screens; a kill with 2 queued shows both, then none.
   - A boss twice gives its scroll and `bossesWon` once; a boss with 2 misses ends only when all 10 are right, then kneel, scroll, queue; no fail screen.
   - Every level cosmetic exists in `trophies`; a met goal unlocks once, in the award's transaction, with one reward screen; gear names are unique; equipping shows on the same frame on avatar and HUD; each of the 4 verse gear pieces adds one Jesus word, never more than 6.
   - Map > zone > `uiText.toMap`, five times across every zone: every region, X marker, and emblem is present each time; with `meta.mapStyle` `grid` the v5-19 grid and Scrolls tile return and nothing else changes; region taps hit at 44 pt or more on iPhone SE.
   - My Stuff: 4 columns fill the width with equal gutters; not-yet trophies are full color with a lock icon; a double-tap equips once.
   - `uiText.toMap` on every screen but the sword screen, the Map, reward screens, and the weekly verse; closing the app on the weekly verse shows it again on relaunch; after a run's 10th card and the queue, the app is on the Map; every screen but the sword screen shows its title banner.
3. **Sound Duel:** no timer; word tiles, no pictures; the 6 word-ending pairs appear; misses never remove or dim a coin; round end shows +30, Got it, then next round or Map.
4. **Offline and the rest:**
   - Airplane mode works with Thai; later launches resume with audio; the update chip saves state and reloads, never mid-run (on an arena screen), mid-card, or on a reward screen; tapped on the Map with a run open, the run resumes after reload.
   - The timer stops in the background and after 60 s idle; a missed day pauses the streak.
   - A missed Monday still delivers the verse; week 11 shows verse 1; every verse shows ESV English bold with THSV11 Thai under it, `\n` as a line break, text byte-identical to the file; no verse placeholder text exists anywhere; the askMax line always shows; an empty Scrolls shelf shows `uiText.scrollsEmpty`.
   - A forced transaction failure changes nothing; a kill on an unlock screen shows it once on relaunch; reconcile restores a removed trophy; nothing is granted twice.
   - Equipping persists across reload, never changes XP, level, counters, or `owned`; locked trophies can't be equipped.
   - Verse audio: tap-to-hear on every verse calls `speechSynthesis` with `en` only, never `th`; the `(ESV)`/`(THSV11)` tags render as separate small elements, are never spoken, and are never part of the verse string; Continue on a reveal replays its English, on a question screen speaks nothing, on Sound Duel replays the current pair.
   - A kill during the boss-win animation shows the scroll once on relaunch with `bossesWon` already set.
   - The rest verse appears on the Scrolls shelf after it is first seen.
   - Credits: `verses.attribution.esv` and `.thsv11` render byte-identical to the file on the Scrolls shelf and in Settings.
   - Grace check: no verse or scroll entry in `cards.json` or `state` has a `cost`, `price`, or currency field; no verse, scroll, or the Scrolls tile is gated on coins, XP spending, talents, or trophies; given verses reopen from Scrolls with every counter unchanged; every gift screen shows `uiText.verseGift`, never `rewardText`; the app contains no shop, buy, or spend flow, and nothing on the Never list; Jesus words have no cost and arrive only at start or with earned gear; the two-answer card (`ms-31`, section 8.1) never removes a coin or XP on a wrong tap: a soft Moonstone X, no red, no sound, then the right one glows Gold and Done advances.
   - Privacy scan of every shipped file: no `tel` URLs, no phone numbers (`/(?<!\d)(\+?1[\s.-]?)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}(?!\d)/`, and compact `/(tel:|\+1)\d{10}/`), no emails (`/[\w.+-]+@[\w-]+\.[\w.]+/`).

## 20. Maxwell's iPhone checks

- Mid-transition screenshots show no bleed-through. Contrast holds in daylight; yellow button text reads without squinting. Thai tone marks aren't clipped. Every emoji picture renders. The coins look like gold coins at arm's length. Airplane mode works. Audio plays on the second launch.


---

## CARD FILE

All card data is in the attached `nancys-adventure-english-v5-20-cards.json` (save it in the build as `cards.json`). Treat the card file as authoritative for all card content: text, Thai, respellings, answers, pictures, hints, zones, bosses, trophies, labels, verses, and slots. If this spec and the card file disagree on card content, the card file wins.
