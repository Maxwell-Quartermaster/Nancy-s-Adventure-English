# Nancy's Adventure English — FINAL Build Prompt

## HOW TO USE THIS PROMPT

1. Paste this entire document into Grok Build. It holds the full spec; the card data is in the attached `nancys-adventure-english-v5-29-cards.json`.
2. Do not generate Thai. Every Thai string is a NEEDS NANCY draft; use it exactly as written. The 16 Bible verses are verified ESV and THSV11 text, and the 6 Jesus words are bible.com ESV and THSV11 text; show them exactly as written.
3. Pictures: each picture card's `pic` is an emoji (render it), `svg:<id>`, or `null` (zone-emblem fallback). Draw 49 SVGs: `picPlan.svg` (30 of 38; 8 are supplied in `picPlan.inlineSvg`), `picPlan.trophySvg` (18 of 22; 4 are supplied in `picPlan.trophyInlineSvg`), `picPlan.uiSvg` (the gold coin).
4. Build in the four stages of section 19; each must print `PASS` before the next.

---

Single source of truth. Card data comes from the companion file `nancys-adventure-english-v5-29-cards.json`, attached with this prompt and saved in the build as `cards.json`. The card file wins on all card content.

## 0. Why this exists

**You are seen, loved, and capable.** Every screen should say that to Nancy, Maxwell's Thai-speaking wife.

- Every system asks: does this make her feel capable? If not, cut it.
- Personal meaning leads: Maxwell's voice, her hotel work, her baby, her faith. The game skin is Maxwell's joy. Nancy's joy is being seen and succeeding.
- Rewards read `rewardText` ("You earned this!"), never "Unlocked."
- Rest is a gift, and a pause is mercy for a season of life. Nothing ever breaks or fails.

## 1. Rules

1. **Three-second rule:** every screen is clear in 3 seconds without Maxwell.
2. **XP is the only points.** It never goes down. Gold coins are only the visual pip meter; cosmetics are earned trophies or Pantry items (11.4; Gold Stars are the one counter that is spent).
3. **Flow:** the challenge sits just above her skill, with clear goals and instant feedback.
4. **One new thing per screen.** A level gives at most one small reward (a cosmetic). Nothing opens by level or by day: every zone and Sound Duel are open from her first launch. One event never gives a reward twice (`ledger`), and two goals met by one answer show as two separate queued screens.
5. **No voice recognition.** She speaks aloud on the honor system.
6. **Pregnancy safe:** no shake, nothing flashing more than 3 times a second, no sudden loud sounds.
7. **Thai on every instruction and label,** shown the moment it appears. Every on-screen label comes from the file's strings (`uiText`, `rewardText`, `wrongText`, `welcomeBack`, `restScreen`, `gotItText`, zone and trophy names); Build never hardcodes label text.
8. **Text hierarchy** wherever English and Thai appear together: English on top, bold and larger; Thai underneath, regular, about 75% size, secondary color. Exception: the question screen hides the English answer (6.4).
9. **Nothing red or alarming** anywhere.
10. **Maxwell is in the room during play.** The app has no phone links and no contact features.
11. **No orphans:** nothing references a removed system, every `cards.json` field and `uiText` key is used, and every field this spec names exists in the file.
12. **Zero scroll (t235u):** at 320 × 568 pt every screen fits with no scrolling; only the Character pane (6.6) scrolls. A long verse drops its English to 18 px; Thai stays 17 px+.

## 2. Permanent standards (public web app)

These two rules carry equal weight and are never traded off.

- **No personal info:** no personal contact info (phone numbers, addresses, emails) and no phone links are ever in any publicly deployed version: source, `cards.json`, service worker cache, or manifest.
- Card text holds no surnames, addresses, birth dates, phone numbers or emails; the one due date is Maxwell's `bh-11` `reply` (his override, 7:54 PM). The first names Max and Maxwell are allowed.
- Personal progress lives on the device only, in IndexedDB. The app makes no network calls except fetching its own files.
- **Scripture is never purchasable:** Bible verses are NEVER purchasable. No shop item, coin/gem/currency cost, or unlock gate that requires spending anything to read scripture. Verses are free gifts (grace): given by day, boss win, or rest, never as purchases. (`verses.graceRule`)
  - A verse arrives as a gift (daily verse, boss scroll, rest verse), framed with `uiText.verseGift` ("A gift for you"), never "You earned this!".
  - No verse is given by level. Once given, a verse stays on the Scrolls shelf free to reread forever: never locked, hidden, removed, or reset (restore and reconcile keep it).
  - Golden Pantry sells cosmetics only for Gold Stars; trophies stay earned and never sold; verses never sold. Coins are only the pip meter; nothing is ever deducted for a verse; no verse has a `cost` or `price` field.
- **Never list:** no countdowns or wait timers, energy or lives, withering, stock or offers, pay-to-skip, leaderboards, push notifications, app-icon badges, or reminder prompts.

## 3. Look: rugged, serious hand-inked adventure style

Original SVG/CSS art: flat cel-shaded fills, thick Ink line, serious, no comedy; no copied assets, logos, or fonts; no online images. Put `<!-- Private family use. Original art. -->` at the top of `index.html`. Spec text beats any mockup.

- **Cel-shaded:** flat fills, one hard shadow tone, one highlight band; no airbrush gradients on objects.
- **Outlines:** 3–4 px Ink `#10170F` on every button, tile, panel, and drawn icon.
- **Metal buttons** (every button, tab, switch, and zone tile):
  - **Face:** brushed iron, `linear-gradient(180deg, #8A939C, #5E6770 45%, #4A525A 55%, #6B747D)` plus `repeating-linear-gradient(90deg, rgba(255,255,255,.04) 0 1px, transparent 1px 3px)`.
  - **Rim:** 3 px bevel (light top `#B9C2CA`, dark bottom `#2C3238`), 4 corner rivets (6 px radial-gradient dots `#D9DEE3`→`#4A525A`, 8 px in), 4 px Ink outline, 18 px radius, 6 px drop edge `#23282D`. On press it sinks 4 px (edge to 2 px) in 80 ms and pops back.
  - **Label plate:** text always sits on a dark inset plate (`#1A1F24` at 85%, 10 px radius) so the texture never touches letters.
  - **English:** Lilita One, Hero Yellow `#FFD100`, 3 px Ink stroke (`paint-order: stroke fill`), drop shadow `0 2px 0 #000`, at least 20 px.
  - **Thai:** under it, Kanit, Cream, 17 px+, no stroke.
  - **Press sound:** only these yellow-text metal plate buttons (iron buttons, tabs, zone tiles, choice plates, Got it) play a soft low metal thud on press: original Web Audio synthesis, never a recorded or game file; a sine thump gliding 90 to 55 Hz plus a faint metallic ring (1.8 and 2.6 kHz partials), 5 ms attack, gone by 160 ms, peak gain 0.25 (moderate, pregnancy safe). Other taps keep only the sounds this spec names.
  - **Variants:** Gold-plated (`#FFE07A`→`#C9971A`) for Got it.
- **Panels, CSS only:** stone plates and steel trim; no wood surfaces except the Map's header logs (6.3).
- **Layout:** a thin top bar, one main area, a bottom bar; no modal on a modal. Everything she taps sits in the lower 60%. Only tappable things look like buttons; titles, labels, and the HUD are flat.
- **Compartment grid (the three-bar rule, whole UI):** every screen is built from equal modular blocks: 12 pt side margins (or the safe-area inset if larger) and 8 pt gaps between blocks, never an odd gap. Rows split into equal columns (3 in the top bars, 2 for the choices, 3 or 4 in Character): `display:grid; grid-template-columns:repeat(N,1fr); gap:8pt; padding-inline:max(12pt,env(safe-area-inset-left)) max(12pt,env(safe-area-inset-right))`. Rows fill the full width; no max-width or centering.
- **Main button spot:** Got it, Continue, Keep going, and next round share one spot: fills the row beside the hint button, at least 64 pt tall, bottom third.
- **Motion:** slide-and-pulse transitions, not flips. A bouncing Gold arrow (1.2 s, 8 px) marks the next step (after a pause, Continue). iOS Reduce Motion (`prefers-reduced-motion`) swaps every move for a 150 ms fade or opacity flash.
- **Opaque layers:** nothing behind a moving element shows through.
- **Back control:** a small metal `uiText.toMap` button at top-left on every screen except the sword screen, the main menu, the Map, Character (these two have `uiText.back` at bottom-left, always back to the main menu), reward screens (every `rewardQueue` entry, including a boss scroll), and the daily verse; those leave only by Got it, so the queue always drains first (section 10). Mid-run it keeps the run; tapping that zone again (or the next launch) resumes it.
- **Screen title banner** on every screen except the sword screen and the main menu: a flat gold ribbon at the top (no bevel, rivets, plate, shadow, or press state; never looks tappable), English in Hero Yellow (26 px), Thai under it (18 px). Titles: Map `uiText.titleMap`, Character `uiText.character` (its panes keep their tab names), Sound Duel `uiText.soundDuel`, daily verse `uiText.verseOfDay`, a scroll opened from the shelf `uiText.scrolls`, reward screens `rewardText` (a verse screen given as a gift uses `uiText.verseGift`), rest screen `restScreen`; a zone run shows the zone `name`/`nameTh`; a boss run shows `zones[].boss.name`.

- **Game feel:** chunky buttons, bold colors, icon counters (gem cluster, gold star) that count up with a pop, thick rounded bars that fill with a pop and end sparkle, gear bonus pips that light like an upgrade (stone, badge, pop); no timers or pressure; Thai labels keep their size, plate and space.
- **Sam:** the hero, a young Thai American boy with glasses (thin round Ink frames), never Nancy. Athletic build: broad shoulders, V-taper, lean arms; slim, long tapered legs, small boots; small dot eyes (never giant), short brows, a calm serious face. Rugged: scuffed boots, patched tunic, slightly uneven Ink line. Zero comedy. One figure: sword screen, HUD, Map emblem, Character.

**Menu palette** (main menu, Map, Character, reward and verse screens; AA-checked):

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
| Stone | `#5B6670` / `#D9DEE3` | Backup view plates, frame rims |
| Log | `#6B4423`, grain `#3E2612`, end cut `#C8A26A` | Map header logs |
| Paper | `#E9D9AE`, edge `#8A6A3A` | Map sheet |
| Moonstone | `#9DB4CC` | soft "missed" glow |
| Ink | `#10170F` | outlines, text on light plates |

AA contrast: Hero Yellow on label plates 7.5–9.1, Cream Thai 10.3+, Cream on Forest 11.9 and Meadow 6.9. Never white on Grass (3.1). Gold only on label plates (10.0; never on bare Paper, 1.08), Hero Yellow on a plate over Paper 7.7, Ink on Paper 13.0. `prefers-contrast: more` makes label plates solid Ink.

**Fonts** (self-hosted in `/fonts/`, never a CDN): English display and buttons in **Lilita One** (OFL). Thai in **Kanit** (Thai subset); fallback `Kanit, "Sukhumvit Set", Thonburi, "Noto Sans Thai", sans-serif`. Respellings in Kanit 500, Gold.

**XP bar and coin meter:**

- **XP bar:** 28 pt tall, XP Track trough, XP Purple fill with an XP Lilac highlight band, Ink outline, label "Level N" in Gold bold on a label plate.
- **Coin meter (the ten pips),** under the gem count in the three-bar's left compartment, never merged with the XP bar: 10 original SVG gold coins (`svg:coin`, 18 pt, two rows of 5, 4 pt gaps): Gold face, thick Gold Edge rim, embossed star-and-leaf mark, white highlight crescent, 3 px Ink outline. Empty: outline only (Gold Edge 35%). Filled: shiny, with a 250 ms pop; filled coins always stay full bright.
- **Glow pulse:** when all ten coins fill and on every level-up, the XP bar area glows soft purple-gold for about 1 s (reduced motion: an opacity flash).

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
- **HUD (the three-bar, every arena screen, just under the safe area):** three equal compartments on the grid above. LEFT: her gem count (a 28 pt gem and its number) with the coin meter under it. CENTER: Sam's 96 pt portrait in all equipped gear, weapon in hand, with the class line under it. RIGHT: "Level N" and the XP bar. Flat, not tappable, no buttons; redraws on the same frame as any change.
- **Cheer and nod (with aura):** on a right answer, a soft glowing aura (rising light rings and motes) rises around Sam inside the 96 pt portrait compartment, never past its edge, while Sam lifts his equipped weapon (sword raised, sling twirled overhead, staffs lifted, hammer held high, bow raised, shield lifted), then settles back to the low open stance; the only in-run time the weapon rises. Aura color: warm Gold for the 4 Bible weapons, the sword's own glint color for swords, leaf-green for the bow, a soft comfort shimmer for the shield. Gift rings: owning 3, 6 and all 9 weapons each adds one faint ring to every aura (derived from `owned`; nothing to buy, no timer, no stat). On a wrong one, a small encouraging nod (head tilts up; never a droop). Both about 600 ms, CSS transform and opacity only on the arm, head, weapon and aura groups; gentle, never mocking; reduced motion: none. The animated Map hero is v6.
- The `<body>` carries `data-theme="menu"` or `data-theme="arena"`; all theme colors come from CSS variables under those two selectors.

## 4. Tech

- **App:** a PWA in vanilla HTML/CSS/JS with `manifest.json` (`display: standalone`, theme and background `#0E3B22`), `apple-mobile-web-app-capable`, `viewport-fit=cover`, and `env(safe-area-inset-*)` insets.
- **Thai:** `lang="th"` and `line-height: 1.7` on every Thai string.
- **Storage:** IndexedDB object store `kv`, key `state` (one record, section 10), mirrored to localStorage after each commit. Call `navigator.storage.persist()`.
- **Home screen:** the icon avoids Safari's 7-day wipe (iOS may still clear data when storage is low). In plain Safari, show only `uiText.openFromHome`.
- **Service worker:** cache-first, versioned. Core files (HTML, JS, CSS, fonts, SVGs, sound effects, `cards.json`) go through `cache.addAll`; each voice clip in `/audio/` is cached on its own, failures ignored. When a new version is cached, show a `uiText.updateReady` chip on the Map only; tapping it saves state, then reloads into the new version. Never reload mid-run, mid-card, or on a reward screen. Mid-run means on an arena screen; on the Map, tapping the chip reloads, and the run resumes.
- **Audio:** Web Audio API; decode each clip on first play; a missing or failed clip is skipped silently. English `speechSynthesis` at 0.85 (0.6 with `uiText.slowMode` on); no Thai voice means Thai audio is skipped. Verses are never spoken in Thai (section 15).
- **Audio wake:** the title tap on each launch and every `uiText.continue` tap resume the AudioContext and play a silent buffer. Continue resumes audio and replays the English of the screen she left (a reveal, say-it card, or verse); a question screen speaks nothing, so nothing replays there; on Sound Duel, Continue replays the current pair. Nothing waits on audio.
- **Locks:** one answer per card; Got it locks until the next screen renders.
- **Auto-pause:** on `visibilitychange` to hidden and on `pagehide`, pause the run and stop audio. On return show `uiText.continue`, then the exact screen she left.

## 5. Pictures

- **Picture recall** (the 126 `mode: "picture-recall"` cards) shows one picture of the answer from `pic`:
  - **Emoji** (an emoji string, sometimes two or three like "👶💤" or "☀️👶🛏️", scaled together to fit the frame): Apple Color Emoji at 120 pt, centered. 73 cards. The newest emoji used are Emoji 13.0 (🫂 `ph-07`, 🪨 `ph-12`, 🪙 `nm-04`, 🛻 `ms-22`, trophy 🪵 `frame-oak`, and the ZWJ sequence 👰‍♀️ `ph-06`; iOS 14.2+); no skin tones. If a glyph does not render (canvas width test on first launch), that card uses the null fallback.
  - **SVG** (`svg:<id>`): the 38 ids in `picPlan.svg` (30 drawn in the section 3 style, 8 supplied; `high-five` and `pray-kneel` are also `ms-31`'s two buttons). Color cards use flat swatches; size cards show one object at its size, nothing else. 39 cards (`svg:hungry` and `svg:pray-kneel` are shared; `svg:tie` is ms-32); clock times are digital.
  - **Fallback** (`null`): the zone emblem at 40% opacity, with the Thai line moved into the frame at 28 pt as the prompt. 14 abstract cards.
- **At a glance (Maxwell's rule):** Every picture card must be unambiguous at a glance on a phone screen. If the image could fit two choices, or two choices look or sound alike (e.g., crib/rib), swap the wrong choice or redraw the image. Draw the ids in `picPlan.svgNotes` exactly as noted. **Clip art (t235u):** tight and realistic: true-to-life proportions and silhouettes, real detail (seams, grain, folds) in flat shade tones, one 3 px Ink outline, no faces on objects, no cartoon squash; the object fills about 85% of its frame. Emoji 13.0 or older; animate only transform and opacity.
- **Supplied art:** `picPlan.inlineSvg` holds 8 ready SVGs: crib, front-desk, towel, towel-white, tie from Openclipart (CC0 public domain, so no credit line) and the original pray-kneel (`ph-08`, `ms-11`, `ms-31`), pray-meal (`ms-12`) and high-five (`ms-31`); `picPlan.trophyInlineSvg` holds 4 original trophy icons: the brown bow for `bow-oak`, the silver and gold card borders, and the blue-flame lantern. Every id inside a supplied SVG is prefixed with its asset name, so inlined SVGs never collide. Inline them exactly as given; never redraw them.
- **Picture frame:** Cream plate, 4 px Ink outline, 18 px radius, stone-and-metal rim, 150–200 pt square; on a 320 pt screen insets trim at most 6 pt and only the picture shrinks, never the Thai. Never blank or broken; an emoji that renders as an empty box uses the fallback.
- **Drawings Build makes: 49** = 30 card ids (`picPlan.svg` minus `picPlan.inlineSvg`; `svgDrawnCount`) + 18 trophy ids (`picPlan.trophySvg` minus `picPlan.trophyInlineSvg`; `trophySvgDrawnCount`) + 1 coin (`picPlan.uiSvg`). Plus 7 zone emblems (6 drawn; Nancy's Kitchen reuses `svg:chef-hat` via `zones[].emblem`), Sam, and UI icons (leaf hint, trophy, gift, check, scroll, flame).
- **Say-it cards** are `mode: "english-first"` (section 8): no picture, no hidden word.

## 6. Screens

### 6.1 Sword screen (every launch)

- **Title (t238u):** a static shot, flat fills, sky `#4FA3FF`, Heroic trim, in a `.cam`: `picPlan.uiInlineSvg` `title`, Sam (section 3; x 30–110, y 290–470), `sword` in `stone` filling the foreground, and the iron button `uiText.letsGo` between rock and front grass (Hero Yellow 24 px+, 11.0; Thai Cream). `.ti svg{stroke:#10170F;stroke-width:3;stroke-linejoin:round}.ti svg *{transform-box:fill-box}.ti{touch-action:manipulation}`. No other words or emoji; no tassel. Wind on `.w` only: `@keyframes sy{50%{transform:rotate(6deg)}}` 3 s.
- **Tap** (button or sword): speak `uiText.letsGo` once; wind stops; Sam dips 3 px and rises (200 ms, no squash); `.cam` pans into the sun (origin at the sun, `translate` to center, `scale(3)`), ease-in, 1.2 s (0.6 s once a card is `seen`), fading to Cream from 80%; transform/opacity only. A 2nd tap skips, never passed on. Reduced motion: no wind or pan, a 150 ms fade.
- Then follow the launch order (section 10): first launch goes to card 1 of a Phonics run (`startZone`); an unfinished run resumes at its exact card or reveal; otherwise the main menu.
- The XP bar fades in after card 1, the coin meter after card 3.

### 6.2 Main menu (the hub)

Exactly two buttons plus one cue: a Gold arrow bobbing beside the Map button (transform only; still with reduced motion), a cue, not a button. No banner, HUD, counters, chip or art; Forest background: `uiText.titleMap` (opens the Map) over `uiText.character` (opens Character, 6.6). Each is a full-width iron button 96 pt tall, 8 pt apart, in the lower 60%. Back from the Map or Character returns here.

### 6.3 Map (linear path, zero scroll)

- **Header logs:** the title banner (`uiText.titleMap`) over the top bar. A 12 pt wood log lies across the yellow-to-green seam, and an 8 pt log frames the whole header (top, sides, bottom): Log bark with static 1 px grain, a light top band (end cut, Ink on it 7.7), end-cut rings at the corners, 3 px Ink outline. CSS only, not tappable.
- **Top bar (the three-bar):** LEFT: one icon column on the 12 pt margin, on a label plate: gem count, Gold trophy (earned of 40), the `uiText.daysWithEnglish` flame (`picPlan.trophyStyle.streakFlame`), the `uiText.goldStars` star. Each row: a 20 pt icon and its count in Gold `#FFCC33` (no white), 22 pt rows 4 pt apart, icons on one left edge. CENTER: the avatar button (opens Character): Sam's 72 pt portrait on a round Stone plate, weapon in hand, featured gem, title and class line. RIGHT: "Level N" and the XP bar. SE height: header 214 pt (status 20, logs 28, banner 62, top bar 104) + margins 24 + rows 264 + bottom bar 44 = 546 ≤ 568.
- **Sheet:** the map area is one rugged Paper sheet: static dot speckle (1 px dots, `radial-gradient`), torn-edge SVG border, a 3D look from a 6 pt Paper-edge drop and a static inset bevel; no animation, `overflow:hidden`.
- **Path:** `mapLayout.regions` in one straight column, bottom to top in file order (Word Meadow first). Each row is 60 pt tall, 8 pt apart, inside the 12 pt margins: a 44 pt region dot (emblem) on one left column, then its label plate (8 pt gap), English in Hero Yellow over Cream Thai 17 px+. One straight dashed path (`pathStyle`) joins the dot centers. Rows start in the lower 60%; on taller screens the spare height goes evenly between rows.
- **No overlaps:** every tap target is its own grid cell, 44 × 44 pt or more and 8 pt from any other; nothing is placed over a row. Each plate has one 56 pt slot at its right end: the Gold `uiText.boss` ribbon when that region's boss is ready, else the bouncing Gold arrow on the next-step row (the region with the fewest runs today; ties: lowest row); never both. Bottom bar (44 pt, 2 columns): `uiText.back` at left, the `uiText.updateReady` chip at right.
- **Taps:** a row opens its zone, or a chooser with one plate per zone (zone `name`/`nameTh`) when it holds two or three; Echo Forest opens Sound Duel.
- **Sam emblem:** each dot keeps its region emblem; on the row she last played (Word Meadow at first), a 20 pt Sam head (glasses, Ink silhouette) sits at the plate's left end. Not tappable.
- **Re-render:** the Sam emblem and the Map slots (`mapTheme`, `mapLanterns`, `mapPet`, `arrowTrail`) update on the same frame a trophy is worn (11.2); slot art stays on the sheet, never over a dot or plate.

### 6.4 Question screen (picture-recall cards)

Top to bottom:

1. The three-bar HUD (gems and coins | portrait | level and XP).
2. Question panel: the picture frame (section 5) inside the stone-and-parchment panel with the zone-tint stripe. The English answer is never shown here.
3. **Thai line** directly above the choices (Kanit 20 pt, Cream 80%): `thDef` if present, else `th`. 18 cards carry `thDef` (the 14 fallback cards, ph-17 "they", and the crib/bed pair ph-01, ph-03, sw-06): a 2–4 word Thai hint rather than a translation.
4. **Choices:** a 2×2 grid of polished-steel plates (section 3), at least 96 pt tall, shuffled every card. The only English she reads before answering. Every picture card uses this one layout on the grid: three-bar, picture, Thai line, the 2×2 plates, then the hint and main-button row, 8 pt apart. A choice may wrap to three lines inside its plate; if one needs more, all four drop to 18 px. The 2×2 never stacks. Strings never carry doubled or trailing spaces.
5. **Hint button:** on every question screen, bottom-left in the safe area, a 72 pt Aqua round button (tap area at least 80 pt) with a thick metal rim, a soft Aqua glow, and a leaf-heart icon, with `uiText.wordsForYou` under it (`uiText.hintButton` as its accessible label), at least 16 pt from the choices. There is no HELP button on any screen; this soft hint button replaces it, by Maxwell's decision.

### 6.5 Reveal screen (after every picture-card answer)

- **Header:** the next `encouragement` line on a right answer, `wrongText` on a miss. `rewardText` ("You earned this!") never shows here; it appears only as the banner of reward screens (section 9).
- **Body:** the picture, the English answer bold (Lilita One 36 pt), the respelling in Gold, the Thai under it; after a miss, the card's `trapNote` (Thai tip) under that. `faith` cards get a small gold leaf mark. The English is spoken once automatically.
- **Prompt:** `uiText.sayItOutLoud` on the first 10 reveals.
- **Buttons:** 🔊 `uiText.replay` and a Gold-plated **Got it** (`gotItText`) in the main button spot.
- **Never auto-advances.** Only Got it moves on. The hint button here gives encouragement only.

### 6.6 Character

The only screen that scrolls. From the main menu or the Map's avatar button; title `uiText.character`; bottom bar: `uiText.back` at left, `uiText.backup` at right. Fixed, never scrolled: Sam's panel (`uiText.yourHero` over `uiText.heroName`, 96 pt portrait in all gear, class line, title, featured gem, gem count, gear bonus pips, 11.1; at its right two plain switches, `uiText.slowMode` and `uiText.restWeeks`), the `uiText.earnedShelf` row, then 6 tabs, 3 across in two rows: `uiText.gems`, `gear`, `themes` / `titles` (`trophies[].cat`), `uiText.scrolls` (6.8), `uiText.pantry` (11.4). It opens on her newest trophy's tab. Only the pane under the tabs scrolls (`overflow-y:auto`; 120 pt+ of it shows on the SE).

### 6.7 Backup view (for Maxwell)

Opened only by `uiText.backup`, outside the pane; silent Stone, no red: `backup` saves her record as JSON; the `needsMaxwell` list (7 cards); the `thaiReview` queue. **Restore, two steps:** 1) `uiText.restore` picks a backup and checks it; 2) `uiText.useBackup` names both (its level and days, and hers now), with `uiText.restore` (a second, separate tap) and `uiText.back`. Before step 2 replaces anything, her current save is copied to the localStorage key `naeState.bak`. A corrupt, partial or empty backup changes nothing: her days, stars and given verses stay. Turning Slow Mode or Rest mode (section 13) off never costs a streak, star or coin. No Settings screen or gear: motion follows iOS Reduce Motion, contrast `prefers-contrast`.

### 6.8 Scrolls

The `uiText.scrolls` pane of Character: a shelf of the boss scrolls and daily verses she has been given, and the rest verse once seen, newest first, each free to reread any time; tapping one opens its verse screen (section 15). Empty shelf: `uiText.scrollsEmpty`. The `verses.attribution` credit line sits small at the bottom of the shelf.

## 7. Core loop

A **run** is 10 cards from one zone, each `picture`, `say-it`, `two-answer` or `server-talk`. After the 10th card's Got it, the reward queue drains, then the rest screen (every 3rd run, section 14) or the Map.

1. A soft cue plays. The question screen shows the picture and Thai line; nothing is spoken, so she recalls the word herself.
2. She taps one of the four text choices. Near-miss traps stay (play/pray, thirteen/thirty) only where the picture rules them out (section 5).
3. **Right:** within 150 ms of the tap (state and glow on the same frame; sounds preloaded; the save never delays it), the plate pulses Gold, +10 XP is committed, one coin fills, then the reveal.
4. **Wrong:** within 150 ms of the tap (same rule), the tapped plate glows Moonstone, the right one glows Gold, a soft chime plays, the meter removes one filled coin if any are filled (none in Baby and Hospital; at 0 nothing changes; no dimming; the rest stay full bright), then the reveal with `wrongText`. The card returns 3 to 5 cards later, at most twice, except in boss runs (section 9). The two-answer card is the exception: a wrong tap there never removes a coin or XP (section 8.1).
5. **Coin meter:** when all ten coins are filled, the glow pulse plays, `pipFills` +1 is committed, and the coins reset.
6. **Hint:** always free; a right answer after it still earns +10.
   - First tap on a question: shows `hint.letters` (for example "p___" or "P_____ w___ h___.") and speaks `uiText.itStartsWith` plus `hint.sound` ("ขึ้นต้นด้วยเสียง /p/").
   - Further taps, and taps anywhere else, alternate in a soft bubble: the next `encouragement` line ("I love you.", 3 s), then her next Jesus word (`jesusWords`, section 15; first while a Bible weapon is equipped, 11.1; until tapped or 6 s): the `ref` and `uiText.jesusWords` small, English bold, Thai, `thGloss` small. On the question screen, Jesus words are shown, not spoken; on the reveal, encouragement only. She has all 6 from the start (`given.type: "start"`); no gear, level or coin brings one. Once she has seen all of hers this visit (session memory only), one `uiText.jesusAllHeard` bubble; the next tap starts them over. No timer or countdown. An empty entry shows a `jesusWordsFallback` line instead.
7. **Review queue:** a missed card's id goes into the small localStorage key `naeReviewQueue` (unique ids, oldest first, at most 20; a right answer on that card removes it). On her next visit (a new app open), up to 2 queued cards missed on an earlier visit appear within the first 3 cards of her first run (right after the easy opener): cards from that zone first, then from any open zone; never in boss runs. No new UI, label, timer, or penalty; they score like any card. Only picture-recall misses enter it (say-it and two-answer cards never do). If the key is missing or not valid JSON, the queue is empty and is rewritten; an empty queue simply adds no cards. The key sits outside `state` and is not in backups; losing it loses nothing. Full Leitner boxes stay in v6.
8. **Run order:** at most 2 `faith:true` cards per run; skip unwritten cards (`fill:true`, empty `en`); open with one `easy:true` card (every zone has at least 2), preferring her zone; then, on a new visit, up to 2 review-queue cards (step 7); then written `personal:true` cards; then the rest, at most 3 never-seen (`seen`) once the zone has 7 seen, the rest seen longest ago. Never 4 say-it cards in a row while a choice card is left; this rule wins over the order above.

## 8. Say-it cards

74 cards are `type: "say-it"`, `mode: "english-first"`: 70 written plus the 4 empty slots (section 17). They include the hospital phrases `bh-01` to `bh-10` (`nursePhrase: true`).

- English bold on top, respelling, Thai underneath; the English is spoken. She says it aloud and taps **Got it**. A `reply` (only `bh-11`) shows small under it, English then Thai, never spoken; no countdown.
- No choices, no wrong answer, no picture unless it has `pic`. A Kitchen say-it card with `pic` opens picture-first: picture and Thai; one tap shows the English. Got it is a right answer: +10 XP, one coin, Gold Stars, `rightByZone`; never removes a coin.
- Hint replays the phrase slowly. Never in boss runs. A `faith:true` card never repeats when she taps Got it without speaking; no prompt to say it again.

### 8.1 Two-answer card (pray or high five)

`ms-31` (`type`/`mode` `"two-answer"`) breaks the normal formula: no reveal, no auto-advance, and a wrong tap costs nothing.

- **Prompt:** each time, one of its 2 `prompts` at random: English bold, Thai under it, English spoken once. The card's `en`/`th` are the Thai Review Queue summary only.
- **Buttons:** two big picture buttons from `choices` (`svg:pray-kneel`, a small kneeling person with folded hands, `uiText.pray`; `svg:high-five`, two hands slapping with a burst, `uiText.highFive`; both supplied in `picPlan.inlineSvg`, never emoji), at least 120 pt, no press sound; the prompt's `answer` is the right `key`.
- **Right tap:** Gold glow, +10 XP and one coin (once per card), then `uiText.done` in the main button spot; only Done advances, one card.
- **Wrong tap:** a soft Moonstone X fades over that button: no red, no buzzer, thud, or any sound, no shake, no `wrongText`, no droop (the small encouraging nod is fine). No coin is removed and no XP is lost (the exception to section 7's coin rule). Then the right one glows Gold; tapping it still earns +10 XP and one coin.
- Hint replays the prompt slowly; never in boss runs; counts as `faith:true`. Fits the iPhone SE without scrolling.

### 8.2 Server Talk (`type: "server-talk"`, Nancy's Kitchen)

`fd-29`–`fd-38`: `uiText.serverAsks`, then a server's question (`en` bold, spoken once, `th` under it) and 4 reply plates (`choices`, the 2×2 of 6.4); she taps the reply that fits (`answer`; `trap` is a near sound). No picture; hint, scoring, reveal and review as a picture card (section 7).

## 9. XP, levels, rewards

- XP to reach level 2: 60 (her first run); level 3: 250 total; after that 100 + 60 × (L − 3) more per level. Cap: level 20.

- **Boss:** exactly the 10 picture cards in `zones[].boss.cards`, ready after 30 right answers in that zone (`boss.readyAfter`, counted in `state.rightByZone`). **Intro:** the Map's `uiText.boss` ribbon (in its row's slot) plus the arena banner showing `boss.name` on entry; no separate intro screen. **Run:** each card answered right drops the guardian's bar by one tenth; a missed card returns after the others, again until right. When all 10 are right the bar is empty and the guardian kneels. No failure state; `uiText.toMap` keeps progress.
- **Boss win (once per zone):** boss win commits before its animation; the scroll waits in the queue. The commit (`boss:<zone>` ledger, `bossesWon`, scroll pushed to `rewardQueue`) happens in one transaction when all 10 are right; a kill mid-animation loses nothing and shows the scroll on relaunch. Then, after the kneel, a boss-win screen shows the `rewardText` banner once (`bossesWon` already committed) with Got it; then, as its own separate screen, the scroll unrolls as a gift (section 15) under `uiText.verseGift` (the scroll screen never shows `rewardText`), Maxwell's boss clip plays (visuals play even if it's missing). Then the reward queue (scroll first). Replays give card XP and Gold Stars only.
- **Level cosmetics:** each is the `trophies` entry with `unlock: {type: "level", n}` (17, levels 2–20; level 20 gives a title and its crown frame). Rule 4 holds: one small reward per level; levels never open anything. Bosses are in Phonics, Baby and Hospital, Colors and Shapes, Numbers and Sight Words; Maxwell Says and Kitchen have none.
- **Celebration** (level-up and new-zone reward screens): CSS-only ribbon drop and one fall of soft confetti, about 1.5 s; nothing flashes more than 3 times a second; no new sound; reduced motion: a 150 ms fade, no confetti.
- **Reward screens:** a Cream-and-Gold panel with the picture, English bold, Thai under it, and Got it; never auto-advance. `rewardText` shows once per screen, as the title banner, in English once and Thai once; never repeated in the body.

## 10. State, awards, resume

- **One state record** `kv/state`: `{xp, level, pipFills, goldStars, pantryOwned[], rightByZone{}, bossesWon[], owned[], equipped{}, ledger{}, rewardQueue[], scrolls[], seen[], run{id, cards, index, phase}, pips, streak, settings{slowMode, restWeeks}}`. Every change is one readwrite transaction on it. Counters only go up, except `goldStars` (Pantry). The record carries one version field, `schema: 5020`. On launch, if `schema` is missing or different, the saved playtest data is reset to a fresh start (Nancy has never installed an earlier version, so there is no migration code). Build never changes `schema` on its own: once Nancy has real progress, a version that changes it must ship a migration first (v6 list).
- **Idempotent awards:** each award has an id, recorded in `ledger` in the same transaction; a repeated id is skipped. Ids: `card:<runId>:<index>`, `say:<runId>:<index>`, `pips:<n>`, `duel:<roundId>:<pair>`, `round:<roundId>`, `level:<N>`, `boss:<zone>`, `day:<local date>`, `verse:<local date>`, `unlock:<trophyId>`.
- **Answer awards** commit at the answer tap, before the reveal shows.
- **Level-ups:** after any XP award, in the same transaction, handle every level crossed (one award can cross several): apply each level's reward once and push one `rewardQueue` entry per level, in order. Then run the trophy check (11.2); gear bonuses follow the gem count (11.1) and are never stored.
- **Derived on every render, never stored or cached:** every Map row, dot, path and emblem (rebuilt from `zones` and `mapLayout` on each return and tab switch; never reuse old DOM or a one-time animation state), boss ribbons, the HUD.
- **Scrolls and `bossesWon`** are sets; adding twice does nothing.
- **Reward queue:** shown after the current Got it (or at run, round, or boss end), one entry per screen; each Got it removes its entry in one transaction. It drains before the rest screen or the Map.
- **Resume:** `run.phase` is `question` or `reveal`. A kill on a reveal resumes on that reveal with no new award.
- **Launch order:** sword tap → reconcile (11.3) → `rewardQueue` → daily verse if due → run or main menu.
- **Restore** (6.7 step 2) replaces the whole record in one transaction, then reconciles.

## 11. Character

Every earned cosmetic is one of the 40 `trophies`, earned automatically (Pantry items, 11.4, are separate): 5 gems, 15 gear, 14 themes, 6 titles; 17 unlock by level. Gear (9 held items: 3 swords, sling, bow, 2 staffs, hammer, shield; gentle, never gory) comes only at start, by level, or by boss win, never bought; every name is unique and shows under the item in Character and on its reward screen.

### 11.1 Character screen (6.6)

- **`uiText.earnedShelf` shelf** ("My newest trophies") in the fixed row above the tabs (6.6); it never repeats `rewardText`.
- **Grid:** 3 across at 320 pt (4 across at 375 pt+) trophy cards (Cream plate, Ink outline, Stone rim): near-square art area on top, picture about 80% of it (sizes may vary a little); the card grows taller so the 17 px Thai never clips; name bold, Thai under it (`th`; wherever a trophy's Thai shows, gear uses `thGloss`). Colors and sizes per `picPlan.trophyStyle` (`gems`, `enlarged`).
  - **Earned:** full color; the equipped one has a Gold glow, a ✓, and `uiText.wearing`.
  - **Not yet:** full color, never grey or dim (only its rank rings sit at 60% opacity, 5:1+ on Ink), a small gift icon at top-right, no 'locked' wording, and its goal from `uiText.unlocksAtLevel`, `unlocksPips`, `unlocksZoneRight`, or `unlocksBosses` (by `unlock.type`) in a gifting tone ("Yours at level 6", "Yours after 2 boss wins") and a Gold progress bar.
- **Rank trim (CSS only, no new SVG):** a trophy's rank comes from `unlock.type`: start 1, level 2, pipFills or zoneRight 3, bossesWon 4. Rank shows by count, never by color alone: rank 1 is the Stone rim alone; 2 adds one 3 px inset ring; 3 adds two; 4 adds two plus 2 Gold studs at the bottom corners (the button rivet dots). Ring colors: 2 emerald `#00D26A`, 3 sky `#4FA3FF`, 4 Gold `#FFCC33` (6.9:1+ on Ink). Rings sit just inside the Ink outline (inset box-shadow) and take at most 6 pt total; the picture shrinks, never the name, Thai or plate padding. No rank words on screen; Pantry items have no rank. Safari 14 CSS: no aspect-ratio, :has(), color-mix() or container queries.
- **Heroic trim:** the title ribbon, verse card and hero panel get a 2 px Gold inner line on Stone, Dark Gold `#8A6200` on parchment, with the existing bevel and rivets; no new art.
- **Juice:** one pop per event (600 ms or less, transform and opacity only, never box-shadow or filter animation; the glow pulse, ribbon and confetti keep their times, and every glow fades a layer's opacity); no combo meters, lives, move limits, boosters or near-miss screens.
- **Tap an earned trophy** (or `uiText.wearIt`): applies instantly: state and UI update on the same frame (avatar, HUD, ✓), then it commits to IndexedDB and the localStorage mirror; a Gold glow and soft chime of 300 ms or less never block input; repeat taps while applying are ignored. All trophy art is preloaded at launch in fixed-size cells, so nothing shifts or flickers; free, reversible, no confirm, and it never changes XP, level, counters, or `owned`. One per `slot` (`cardFrame`: oak, silver, gold, or hearts). Tapping an equipped optional item again unequips it. A not-yet trophy only shows its goal.
- **Gear bonuses:** gems are earned, never spent and never go down; nothing to buy, no timer. Her gem total turns on and upgrades her gear bonuses by itself at set thresholds (`meta.bonusGems`): 1 gem adds the right-answer glow, 2 a wider halo, 4 a smooth slide to the next card; they work on every weapon and show as up to 3 Gold pips in Sam's panel. Under the pips, a gentle progress line names the next bonus and the gems left (`uiText.nextBonus`, a Gold bar; a string's `enOne` is used when n is 1); with all 3 it shows nothing. Visual only: no stat, nothing makes a question easier. Gold Stars stay Pantry cosmetics only (11.4).
- **Hero pose:** an open, ready stance (feet apart, free hand open). The equipped weapon is drawn in Sam's hand in both portraits and Character, held low at his side, never across his face; a weapon change redraws it on the same frame.
- **Class line:** under Sam's portrait (HUD, Character; never on the Map emblem), the equipped weapon's `classTitle` (Maxwell's mapping; only weapons set the class): sling `uiText.classWarrior`, staffs `uiText.classMage`, hammer `uiText.classKnight`, the brown `bow-oak` `uiText.forestRanger`, swords `uiText.classDefender`. The shield has no `classTitle`: with it equipped, the class line is hidden. Words only; no stats. Earned titles (`title` slot) still show on the avatar.
- **Where slots render:** `weapon`, `cape`, `tunic`, `avatarFrame`, `featuredGem`, `title` on the avatar; `mapTheme`, `mapLanterns`, `mapPet`, `arrowTrail` on the Map; `cardFrame` around the question panel; `restSky` on the rest screen; `auraRing` on the cheer aura (the Golden Spoon adds one soft gold ring); `swordSplash` on the sword screen; `sparkle` on right answers.
- **Weapon flourishes (visual only; no stat, XP, coin, timer or penalty; nothing makes a question easier):** the 4 Bible weapons (`sling-shepherd`, `staff-shepherd`, `staff-lantern`, `hammer-builder`) show `uiText.weaponGift` under them in Character once she has them (never on a not-yet card, so scripture never reads as a goal); while one is equipped, her next hint bubble shows her Jesus word before the encouragement line (the same free gift she already has; never earned or bought). Swords: the right-answer glint in the sword's color (iron white, gold, ice blue). `bow-oak`: a leaf-green trail on the right plate. `shield-sunrise`: a soft sunrise shimmer on Got it after a miss. The `sparkle` gear is a 400 ms glint on the chosen plate.
- **Defaults** (`unlock.type: "start"`) are owned from first launch. `state.equipped` persists choices.

### 11.2 Unlocks

- **Goals** (`trophies[].unlock`): `start`, `level`, `pipFills`, `zoneRight` (`n` right answers in `zone`; Golden Chef: 25 in Kitchen), `bossesWon`. All come from play, never from days or sessions; the gold gem needs all 5 bosses.
- **Trophy check:** inside the same transaction as every XP, coin, day, or boss award. Each trophy whose goal is met and whose `unlock:<id>` isn't in the ledger is added to `owned`, ledgered, and queued as a reward screen: picture, name, `uiText.wearIt`, Got it, under the `rewardText` banner. rewardText shows once, as the banner; never repeated in the body.

### 11.3 Reconcile on launch

- Recompute every goal from the counters; grant any met-but-missing trophy through the trophy check. Never remove an earned trophy.
- Drop duplicate `owned` ids and any `equipped` id not owned (fall back to the default).

### 11.4 Golden Pantry

The `uiText.pantry` tab shows a chunky stone-and-Gold shelf of `pantry.items` (cosmetics only, never trophies or verses): each tile shows its picture, name, Thai, and a gold-star price (owned: ✓ and `uiText.wearIt`); `uiText.getFor` asks once, then a soft thud, the stars go down by `stars`, and the item is hers to equip in its `slot` (state `pantryOwned[]`, ledger `buy:<id>`). She earns `pantry.earn` Gold Stars per right answer and finished run (ledger as the card or run). No timer, sale, stock limit, offer or real money; stars never drop any other way.

## 12. Sound Duel

- The Echo Knight (`uiText.echoKnight`) shows two similar word tiles (light/right, fine/file, thirteen/thirty) and speaks ONE of them at random; she taps the word she heard (English, no pictures). Each pair uses the next on-device English voice (`speechSynthesis.getVoices()` with `lang` starting `en`, up to 4, in turn; one voice if that is all there is; load voices on `voiceschanged`, and if none arrive, use the default voice). Rounds of 8 pairs, untimed, no score, can't be lost.
- +10 XP per right answer. Free `uiText.hearItAgain` replays that one word slowly, same voice. Right answers fill coins; misses never remove or dim a coin.
- **Round end:** `uiText.roundDone` with +30 XP, then Got it, then the reward queue, then a choice of the next round or `uiText.toMap`.

## 13. Day streak

- The `uiText.daysWithEnglish` flame in the Map top bar. A missed day pauses it and never resets it. On return: `welcomeBack`. With `uiText.restWeeks` on, the flame shows a moon (a resting season; nothing else changes).

## 14. Rest screen (optional victory lap)

- After every 3rd finished run since she opened the app, once the reward queue drains: a celebration shows `restScreen` with `verses.rest` (framed with `uiText.verseGift` the first time; once seen it joins the Scrolls shelf, section 2) with a soft Gold burst and two buttons: `uiText.keepGoing` (primary, Gold) starts her next run in the same zone; `uiText.restNow` and the back control go to the Map. Nothing waits; the app never closes itself.
- No session length, daily cap, play timer or forced rest; the whole game can be finished in one sitting.

## 15. Bible verses

- **Boss scrolls** (`zones[].boss.scroll`): Phonics Genesis 1:1; Colors and Shapes Genesis 9:13; Numbers John 6:9; Sight Words 1 Samuel 17:45; Baby and Hospital Isaiah 40:11. Saved to Scrolls (6.8).
- **Daily verse** (Maxwell 7:38 PM PT): one memory verse a day on her first open each day, titled `uiText.verseOfDay`, seen on Got it (ledger `verse:<local date>`), else shown again next launch (section 10). Day d = whole local days since `verses.weeklyStart`; the 40-day cycle (`meta.dailyVerses`) is the 10 `verses.weekly`, then the 30 in `daily-verses.json`, a second file given with this prompt (`nancys-adventure-english-v5-29-daily-verses.json`; `rule`, `verses[]`: `ref`, `en`, `th`, `enUrl`, `thUrl`; optional `enGloss`/`thGloss` show small under the Thai, never spoken); index ((d mod 40)+40) mod 40; as `verses.rotation`. Free, never sold; a missed day costs nothing; given verses stay on Scrolls. Daily texts are VERIFIED (see the file's `verifiedBy`). Same text rules.
- **Verse card style:** chunky rounded card, bold saturated Gold and parchment frame, a reward-pop entrance (about 600 ms; none with reduced motion), a chunky Gold Got it. Visual only.
- **Verse screen (scrolls and daily):** a cream parchment panel with a Gold and metal frame: when newly given, `uiText.verseGift` ("A gift for you") at the top; the reference, the English verse bold, **the Thai verse directly under the English**, tap to hear (English only), then at the bottom one small line `uiText.askMax` ("Don't know a word? Ask Max."), then Got it.
- **Verse text is filled and verified (16 verses).** English is the ESV (`enSource`, bible.com version 59); Thai is the Thai Standard Version 2011, ฉบับมาตรฐาน, Thailand Bible Society (`thSource: "THSV11"`, bible.com version 174, Maxwell's choice). Each verse has `status: "VERIFIED"` and its `enUrl`/`thUrl`. Build never generates, edits, trims, capitalizes, or re-punctuates verse text; show it exactly as in the file. **Decided by Maxwell:** Isaiah 41:10 starts with a lowercase "fear not", exactly as the ESV prints it; shown exactly as printed, honesty over formatting (`verses.decided`). The unmatched quote marks in John 3:16, Joshua 1:9, and 1 Samuel 17:45 (including the orphan opening mark) also stay exactly as printed; never add or remove a quote mark. A `\n` in `en` or `th` is a poetry line break: render it as a line break, speak it as a pause (`verses.textRule`). Verse tap-to-hear speaks en only; never speak th. (`verses.ttsRule`) (The Thai is for her to read; no verse is ever spoken in Thai, even if a Thai voice exists.) If a half is ever empty, hide it and never speak it.
- **Jesus words** (`jesusWords`, 6; hint bubble only, never on Scrolls, never purchasable): whole verses of Jesus speaking, from the same bible.com versions, under the same text rules: never add or remove a quote mark (John 14:1 opens with one; John 8:12 keeps its narrator words and marks). `status: "VERIFIED"` (`verifiedBy`); Build shows them exactly as written. `thGloss` is separate helper text, never part of the verse or spoken.
- **Credits:** `verses.attribution` shows small on the Scrolls shelf, each line word for word from its publisher: `esv` is Crossway's official copyright notice for digital works quoting more than one translation (crossway.org/permissions), and `thsv11` is the Thailand Bible Society's own credit for THSV11 as published with bible.com version 174 (four lines: Thai, then English; keep the `\n` breaks). Sources are in `esvSource` and `thsv11Source`. Never shorten or translate either. Per Crossway, each English verse carries a small `verses.attribution.esvTag` ("(ESV)") after it and each Thai verse a small `thsv11Tag` ("(THSV11)"). Show the tags as separate small text; never speak them or join them to the verse text. (`tagRule`)

## 16. Cards

- **211 cards** in `cards.json`: 207 written plus 4 empty personal slots. Format:
  `{id, zone, type, mode, en, th, thDef?, thDefStatus?, respell, pic, choices:[{en}×4], answer, hint{letters, sound, word}, trap, trapNote, fill?, tag?, easy?, faith?, personal, slot?, prompts?, reply?, syl?, nursePhrase?, thStatus?}`. A missing field takes `meta.cardDefaults` (`fill`, `easy`, `faith`, `nursePhrase`, `personal` false; `tag`, `answer`, `trap`, `trapNote` null; `type` `picture`); a missing `mode` follows `meta.modeByType`; a missing `thStatus` is `meta.cardThStatusDefault` (`NEEDS NANCY`). A missing `thDefStatus`, and outside verses, Jesus words, scrolls and `pantry` a missing `thStatus`/`nameThStatus`, is `meta.thStatusDefault`.
  - `hint.word` is data only (the word `hint.sound` comes from); never display it. `trapNote` shows on a miss. `tag: "Example"` shows `uiText.example`. `slot` names an empty slot's topic.
  - `picture` cards: `mode: "picture-recall"`, with `pic` and `hint`; `answer` and `trap` are among the choices.
  - `say-it` cards: `mode: "english-first"`, `choices: []`, `answer: null`.
  - `two-answer` cards (section 8.1): `mode: "two-answer"`, `choices` [{`en`, `key`, `pic`}]×2, `prompts` [{`key`, `en`, `th`, `respell`, `answer`}]×2, card `answer: null`.
  - `nursePhrase: true` marks `bh-01` to `bh-10` for the Thai Review Queue.
- **Top-level data:** `zones` (with `emblem`, `zoneClip`, `nameThStatus`, `startZone` = Phonics, `cardIds`, and `boss` with `readyAfter`, `name`, `cards`, `clip`, `scroll`), `soundDuel.pairs` (`a`, `b`; 30), `verses`, `jesusWords` (`given`, `thGloss`, `thGlossStatus`, `thGlossBy`), `jesusWordsFallback`, `picPlan` (with `inlineSvg`, `trophyInlineSvg`, `uiInlineSvg`, `svgDrawnCount`, `trophySvgDrawnCount`), `trophies` (weapons carry `classTitle`), `trophyRules`, `mapLayout` (`regions` with `zones`, `color`, `accent`, in path order; `paths`; `pathStyle`), `uiText` (63), `encouragement` (7), `rewardText`, `wrongText`, `welcomeBack`, `restScreen`, `gotItText`, `rewardClips`, `needsMaxwell`, `meta`. File strings win over any Thai here.
- **Traps** are the nearest wrong choice: a sound-alike for Thai speakers (R/L, TH, V/W, dropped endings) only where the picture rules it out (section 5).
- **Tiers:** a very simple word (pizza, taco, cake, corn dog) is never a bare card; it sits in a phrase ("A slice of pizza, please."). A hard word carries `syl` (`spa·ghet·ti`): the reveal and say-it card show it under the respelling, and 🔊 first plays it at Slow Mode speed. The six Thai dish names may stand alone. No tier label, score or timer.
- **Thai:** Build never writes or edits Thai. Every Thai string is a `NEEDS NANCY` draft and still shows, with a tiny dot only the Backup view explains.
- **Personal cards:** 80 are `personal:true` (76 written plus the 4 slots). Written ones sort first (7.8).
- **Inn examples:** `ms-04`, `ms-05`, `ms-06` are hypothetical (Example tag, `fill:true`) until Maxwell confirms them.
- **Approved 7-word exceptions:** `ms-06` and `bh-14` ("Is it a boy or a girl?").
- **Maxwell's voice, 17 clips, each skipped if missing:** 7 zone clips (`maxwell-<zone>.m4a`, first visit), 5 reward clips (`maxwell-reward-1..5.m4a`, random on rewards), 5 boss clips (`maxwell-boss-<zone>.m4a`).

## 17. Personal card slots

Four empty say-it cards wait for Maxwell (`fill:true`, `personal:true`, empty `en`, `th`, `respell`), skipped until written, then sorted first: `bh-30` the baby; `ms-28` the hotel; `ms-29` Maxwell, her husband; `ms-30` faith.

**Needs Maxwell list** (`needsMaxwell`, 7): `ms-04`, `ms-05`, `ms-06`, `bh-30`, `ms-28`, `ms-29`, `ms-30`. He fills them in `cards.json` or through the Backup view's list. The 16 verses are already filled and verified.

## 18. Thai Review Queue

Everything starts `NEEDS NANCY`: 201 of the 207 written cards, the 17 `thDef` hints, `gotItText`, `rewardText`, `wrongText`, `welcomeBack`, `restScreen`, the 7 zone `nameTh` (`nameThStatus`), all 63 `uiText` entries, the 4 map region names (`instructorChecked` marks Instructor's), the 5 boss names, the 7 encouragement lines, 25 trophy names, the 15 gear `thGloss`, the 6 Jesus-word `thGloss`, the 2 `jesusWordsFallback` lines, and any slot Maxwell fills. The 6 Thai dish names (`fd-01`–`fd-06`, `thStatus: "SIGNED OFF"`) are Maxwell's recorded exception (8:01 PM MT), `th` only; Nancy may still review them. Not in the queue: the 16 verses, the Jesus-word verse text, and `verses.attribution`, which are verified THSV11/ESV text (`status: "VERIFIED"`), never drafts. The Backup view lists the drafts; Nancy taps ✓ (confirm) or ✎ (Maxwell edits). Review the 10 `nursePhrase` cards first, then the `thDef` hints; gear and Jesus-word glosses go in Instructor's nightly batches after launch. The 3 sleepy and nap cards (`ph-25`, `ph-26`, `bh-31`) and the two-answer card `ms-31` are new drafts for Instructor's nightly batches after launch, not the first review. The tie card `ms-32` joins the same after-launch nightly batch; the Thai fixes from Instructor's 6:31 PM audit stay `NEEDS NANCY` too.

## 19. Build order: one paste, four stages

After each stage, `window.__test()` must print `PASS` before the next. Never rewrite an earlier stage unless its test fails.

1. **Core loop** (sword, 3 cards, question, reveal, Hint, XP bar, coins, review):
   - Question screens never show the English answer; `answer` and `trap` are among the choices.
   - The reveal is still there after 10 s; double-tapping Got it advances one card.
   - A hint earns +10; first tap shows `hint.letters`, the next an encouragement line; a miss removes one filled coin if any (none in Baby and Hospital; at 0 nothing changes); no dimming.
   - A run opens with one easy card; on a new visit, up to 2 cards missed on an earlier visit appear by card 3 (never more than 2 per visit); right and wrong feedback starts within 150 ms of the tap; personal cards first; unwritten cards skipped; at most 3 never-seen cards once the zone has 7 seen; say-it cards show Got it and no choices.
   - Hint taps alternate encouragement (3 s) and her given Jesus words (6 s or tap; shown, never spoken); a new player has all 6; after all are seen, `uiText.jesusAllHeard` once, then they start over; the HUD portrait cheers on right (aura rises, weapon lifts, then settles) and gives a small encouraging nod on wrong (head tilts up, about 600 ms; never a droop).
   - A kill on a reveal resumes there with XP unchanged. Ten coins play the glow pulse and add 1 to `pipFills`.
   - No red fills. Button labels sit on label plates: English Hero Yellow 20 px+ (`uiText.letsGo` 24 px+), Thai 17 px+; on iPhone SE nothing clips.
   - Card, boss, and Sound Duel screens use `data-theme="arena"`; menus use `data-theme="menu"` with no arena colors; enter and exit play the banner transition; the HUD sits in the top bar, flat, covering nothing.
   - Two-answer card `ms-31`: each showing picks one of its 2 `prompts` at random; right tap: Gold, +10 XP and one coin once, `uiText.done`; wrong tap: soft Moonstone X, no sound, coins and XP unchanged, then the right one glows Gold; only Done advances.
2. **Map, levels, rewards:**
   - From her first launch every region, zone and Sound Duel is open at any level, with no locks; a zone's boss ribbon shows after 30 right answers there, each boss with 10 cards.
   - One award crossing two levels grants both rewards once and queues two screens; a kill with 2 queued shows both, then none.
   - A boss twice gives its scroll and `bossesWon` once; a boss with 2 misses ends only when all 10 are right, then kneel, scroll, queue; no fail screen.
   - Every level cosmetic exists in `trophies`; a met goal unlocks once, in the award's transaction, with one reward screen; gear names are unique; equipping shows on the same frame on avatar and HUD; the 4 Bible weapons carry no verse; each shows `uiText.weaponGift` and, when equipped, puts her next Jesus word first in the hint bubble.
   - Map > zone > `uiText.toMap`, five times across every zone: every row, dot, path and emblem is present each time; at 320 × 568 pt no two tap targets overlap (bounding boxes 8 pt apart), each is 44 pt or more, and the Map never scrolls.
   - The main menu shows exactly two buttons (Map, Character) and the arrow cue. Restore: one tap never replaces her record; a corrupt, partial or empty backup changes nothing; `naeState.bak` holds the old save. At 320 × 568 pt nothing scrolls except the Character pane (scrollHeight ≤ clientHeight). No Settings, gear button or talent exists anywhere.
   - Character: 4 columns fill the width with equal gutters; not-yet trophies are full color with a gift icon; a double-tap equips once.
   - `uiText.toMap` on every screen but the sword screen, main menu, Map, Character, reward screens, and the daily verse; closing the app on the daily verse shows it again on relaunch; after a run's 10th card and the queue, the app is on the Map; every screen but the sword screen and main menu shows its title banner.
3. **Sound Duel:** no timer; word tiles, no pictures; the 6 word-ending pairs appear; misses never remove or dim a coin; round end shows +30, Got it, then next round or Map.
4. **Offline and the rest:**
   - Airplane mode works with Thai; later launches resume with audio; the update chip saves state and reloads, never mid-run (on an arena screen), mid-card, or on a reward screen; tapped on the Map with a run open, the run resumes after reload.
   - A missed day pauses the streak. After 3 runs the rest screen offers Keep playing (next run, same zone) and Rest now (Map); play goes on with no wait.
   - A missed day costs nothing; day 41 shows verse 1 again; every verse shows ESV English bold with THSV11 Thai under it, `\n` as a line break, text byte-identical to the file; no verse placeholder text exists anywhere; the askMax line always shows; an empty Scrolls shelf shows `uiText.scrollsEmpty`.
   - A forced transaction failure changes nothing; a kill on an unlock screen shows it once on relaunch; reconcile restores a removed trophy; nothing is granted twice.
   - Equipping persists across reload, never changes XP, level, counters, or `owned`; not-yet trophies can't be equipped.
   - Verse audio: tap-to-hear on every verse calls `speechSynthesis` with `en` only, never `th`; the `(ESV)`/`(THSV11)` tags render as separate small elements, are never spoken, and are never part of the verse string; Continue on a reveal replays its English, on a question screen speaks nothing, on Sound Duel replays the current pair.
   - A kill during the boss-win animation shows the scroll once on relaunch with `bossesWon` already set.
   - The rest verse appears on the Scrolls shelf after it is first seen.
   - Credits: `verses.attribution.esv` and `.thsv11` render byte-identical to the file on the Scrolls shelf.
   - Grace check: no verse or scroll entry in `cards.json` or `state` has a `cost`, `price`, or currency field; no verse, scroll, or the Scrolls tab is gated on coins, XP spending, gems, or trophies; given verses reopen from Scrolls with every counter unchanged; every gift screen shows `uiText.verseGift`, never `rewardText`; the only spend flow is the Golden Pantry (cosmetics for Gold Stars; no verse, trophy, timer, offer or real money), and nothing on the Never list; Jesus words have no cost and all 6 are given at start; the two-answer card (`ms-31`, section 8.1) never removes a coin or XP on a wrong tap: a soft Moonstone X, no red, no sound, then the right one glows Gold and Done advances.
   - Privacy scan of every shipped file: no `tel` URLs, no phone numbers (`/(?<!\d)(\+?1[\s.-]?)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}(?!\d)/`, and compact `/(tel:|\+1)\d{10}/`), no emails (`/[\w.+-]+@[\w-]+\.[\w.]+/`).

## 20. Maxwell's iPhone checks

- Mid-transition screenshots show no bleed-through. Contrast holds in daylight; yellow button text reads without squinting. Thai tone marks aren't clipped. Every emoji picture renders. The coins look like gold coins at arm's length. Airplane mode works. Audio plays on the second launch. With the ring/silent switch on, iOS mutes sounds and voice: flip it to hear them.

---

## CARD FILE

All card data is in the attached `nancys-adventure-english-v5-29-cards.json` (save it in the build as `cards.json`). Treat the card file as authoritative for all card content: text, Thai, respellings, answers, pictures, hints, zones, bosses, trophies, labels, verses, and slots. If this spec and the card file disagree on card content, the card file wins.
