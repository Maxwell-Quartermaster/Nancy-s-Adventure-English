# Nancy's Adventure English — FINAL Build Prompt

## HOW TO USE THIS PROMPT

1. Paste this entire document into Grok Build. It holds the full spec; the card data is in the attached `nancys-adventure-english-v6-08-cards.json`.
2. Do not generate Thai. Every Thai string is a NEEDS NANCY draft; use it exactly as written. The 16 Bible verses are verified ESV and THSV11 text, and the 6 Jesus words are bible.com ESV and THSV11 text; show them exactly as written.
3. Pictures: each picture card's `pic` is an emoji (render it), `svg:<id>`, or `null` (zone-emblem fallback). Draw 55 SVGs: `picPlan.svg` (33 of 38; 5 are supplied in `picPlan.inlineSvg`), `picPlan.trophySvg` (21 of 24; 3 are supplied in `picPlan.trophyInlineSvg`), `picPlan.uiSvg` (the gold coin).
4. Build in the four stages of section 19; each must print `PASS` before the next.

---

Single source of truth. Card data comes from the companion file `nancys-adventure-english-v6-08-cards.json`, attached with this prompt and saved in the build as `cards.json`. The card file wins on all card content.

## 0. Why this exists

**You are seen, loved, and capable.** Every screen should say that to Nancy, Maxwell's Thai-speaking wife.

- Personal meaning leads: Maxwell's voice, her hotel work, her baby, her faith. The game skin is Maxwell's joy. Nancy's joy is being seen and succeeding.
- Rewards read `rewardText` ("You earned this!"), never "Unlocked."
- Rest is a gift. Nothing ever breaks or fails.

## 1. Rules

1. **Three-second rule:** every screen is clear in 3 seconds without Maxwell.
2. **XP is the only points.** It never goes down. Gold coins are only the visual pip meter; cosmetics are earned trophies or Pantry items, and weapons follow the gear rule (11.1); Gold Stars are the one counter that is spent.
3. **Flow:** the challenge sits just above her skill, with clear goals and instant feedback.
4. **One new thing per screen.** A level gives at most one small reward (a cosmetic). Nothing opens by day; levels open only gear tiers (11.1). **Regions open in order (t334u):** Word Meadow; Golden Fields after the Word guardian (Sight Words); Home Lake after the Number guardian; Echo Forest (Sound Duel) after the Gentle guardian. Only a region's end guardian (its last zone in `mapLayout` order) opens the next, and she can face it first; the Sound (Phonics) and Rainbow (Colors) guardians are anytime bonuses, never needed. A guardian can't be lost (a miss: hint, try again). Maxwell Says and Kitchen open day one, bright on the faded Home Lake (its row opens their chooser). An unopened region shows its look softened (tint, not gray), the end guardian's silhouette and `uiText.comingNext`; a tap shows `uiText.guardianLast` over the end guardian's silhouette and `boss.name`. An opened region never closes; it opens once (ledger `region:<id>`) with `uiText.regionOpen` at the sheet top (never over a row), the guardian kneeling by its row, an 8% bounce and a sparkle. Hearth, Scrolls and rest screen: always. One event never gives a reward twice (`ledger`), and two goals met by one answer show as two separate queued screens.
5. **No voice recognition.** She speaks aloud on the honor system.
6. **Pregnancy safe:** no shake, nothing flashing more than 3 times a second, no sudden loud sounds.
7. **Thai on every instruction and label,** shown the moment it appears. Every on-screen label comes from the file's strings (`uiText`, `rewardText`, `wrongText`, `welcomeBack`, `restScreen`, `gotItText`, zone and trophy names); Build never hardcodes label text.
8. **Text hierarchy** wherever English and Thai appear together: English on top, bold and larger; Thai underneath, regular, about 75% size, secondary color. Exception: the question screen hides the English answer (6.4).
9. **Nothing red or alarming** anywhere.
10. **Maxwell is in the room during play.** The app has no phone links and no contact features.
11. **No orphans:** nothing references a removed system, every `cards.json` field and `uiText` key is used, and every field this spec names exists in the file.
12. **Zero scroll:** at 320 × 568 pt every screen fits with no scrolling; only the Character pane (6.6) and Backup lists scroll. A long verse drops its English to 18 px; Thai stays 17 px+; still too long, the verse text scrolls in its card.

## 2. Permanent standards (public web app)

These two rules carry equal weight and are never traded off.

- **No personal info:** no personal contact info (phone numbers, addresses, emails) and no phone links are ever in any publicly deployed version: source, `cards.json`, service worker cache, or manifest.
- Card text holds no surnames, addresses, birth dates, phone numbers or emails; the one due date is Maxwell's `bh-11` `reply` (his override, 7:54 PM). The first names Max and Maxwell are allowed.
- Personal progress lives on the device only, in IndexedDB. The app makes no network calls except fetching its own files.
- **Scripture is never purchasable:** Bible verses are NEVER purchasable. No shop item, coin/gem/currency cost, or unlock gate that requires spending anything to read scripture. Verses are free gifts (grace): given by day, boss win, or rest, never as purchases. (`verses.graceRule`)
  - A verse arrives as a gift (daily verse, boss scroll, rest verse), framed with `uiText.verseGift` ("A gift for you"), never "You earned this!".
  - No verse is given by level. Once given, a verse stays on the Scrolls shelf free to reread forever: never locked, hidden, removed, or reset (restore and reconcile keep it).
  - Golden Pantry sells cosmetics and level-opened weapons only for Gold Stars, never real money; other trophies stay earned and never sold; verses never sold. Coins are only the pip meter; nothing is ever deducted for a verse; no verse has a `cost` or `price` field.
- **Never list:** no countdowns or wait timers, energy or lives, withering, stock or offers, pay-to-skip, leaderboards, push notifications, app-icon badges, or reminder prompts.

## 3. Look: rugged, serious hand-inked adventure style

Original SVG/CSS art, one style in two layers. UI (buttons, bars, counters, plates): chunky, rounded, bold saturated, clean mobile patterns. World and Sam: dark bold Ink line, rugged, serious, no comedy. Both: 3–4 px Ink, flat fill, one cel shadow, one small highlight, light from top-left. No copied assets, logos, or fonts; no online images. Put `<!-- Private family use. Original art. -->` at the top of `index.html`. Spec text beats any mockup.

- **Texture and depth:** `picPlan.uiInlineSvg.tex` (once, top of `<body>`, never `display:none`) holds the shadow class `zs` and one 12% pattern per material: paper `zp`, wood `zw`, stone `zt`, cloth `zc`, foliage `zf`. Every drawing, supplied or Build's, uses them and is inline in the DOM, never `<img>`. No gradients except sky, the title night fade, and the title button shade (approved t288u mock and Maxwell's Button C pick). Per material: one hard shadow (25% darker, bluer); one flat highlight (≤5%), hard or shiny only. Muted bases, 1–2 accents. Far layers paler, no line; mid layers a 2 px line 12 to 18 HSL L below its fill (one value step = 5 L), same hue, saturation +5. No texture on skin, faces, text plates or behind dots/labels; Thai plates are front-layer UI (Ink outline, flat fill). Glows: flat 30% shapes, no blur.
- **Per-SVG limit:** 2,500 chars per SVG; exempt: `tex` (shared defs) and `title` (t371u).
- **Outlines:** Ink `#10170F`: 4 px on the hero and title sword, 3 px on all else.
- **Storybook look (#77):** warm light; panels, cards and plates get a gold-and-stone frame (6 pt; 4 pt on dense screens and at 320 pt); ornate gold-and-blue accents (`#3D7FD9` gems) on swords and frames; chunky round-crowned trees; full look on the title, Map, rewards and verse screens, lighter on question screens. No new art beyond `picPlan`.
- **Metal buttons** (every button, tab, switch, and zone tile):
  - **Face:** flat steel-blue `#3E5A7A`, a 5 px darker `#2C3F56` bottom lip, one 2 px lighter `#5A7699` top-edge line; every tile and tab the same face.
  - **Rim:** 3 px bevel (light top `#B9C2CA`, dark bottom `#2C3238`), 4 corner rivets (6 px flat `#D9DEE3` dots, 8 px in), 3 px Ink outline, radius 30–35% of height, 52 pt tall where it fits (6.4 SE sizes stay; never under 44 pt). On press `translateY(3px)` for 110 ms, then back; no squash or bounce.
  - **Label plate:** text always sits on a dark inset plate (`#1A1F24` at 85%, 10 px radius) so the texture never touches letters.
  - **English:** Lilita One, Hero Yellow `#FFD100`, 3 px Ink stroke (`paint-order: stroke fill`), drop shadow `0 2px 0 #000`, at least 20 px.
  - **Thai:** under it, Kanit, Cream, 17 px+, no stroke.
  - **Press sound:** only these yellow-text metal plate buttons (iron buttons, tabs, zone tiles, choice plates, Got it) play a soft low metal thud on press: original Web Audio synthesis, never a recorded or game file; a sine thump gliding 90 to 55 Hz plus a faint metallic ring (1.8 and 2.6 kHz partials), 5 ms attack, gone by 160 ms, peak gain 0.25 (moderate, pregnancy safe). Other taps keep only the sounds this spec names.
  - **Variants:** Gold-plated (flat `#FFCC33`, lip `#B7860B`) for Got it.
- **Panels, CSS only:** stone plates and steel trim; no wood surfaces except the Map's header logs (6.3).
- **Layout:** a thin top bar, one main area, a bottom bar; no modal on a modal. Everything she taps sits in the lower 60%. Only tappable things look like buttons; titles, labels, and the HUD are flat.
- **Compartment grid (the three-bar rule, whole UI):** every screen is built from equal modular blocks: 16 pt side margins (or the safe-area inset if larger) and 8 pt gaps between blocks, never an odd gap. Rows split into equal columns (3 in the top bars, 2 for the choices, 3 or 4 in Character): `display:grid; grid-template-columns:repeat(N,1fr); gap:8pt; padding:0 max(16pt,env(safe-area-inset-right)) 0 max(16pt,env(safe-area-inset-left))`. Rows fill the full width; no max-width or centering.
- **Main button spot:** Got it, Continue, Keep going, and next round share one spot: fills the row beside the hint button, at least 64 pt tall, bottom third.
- **Motion:** slide-and-pulse transitions, not flips. A bouncing Gold arrow (1.2 s, 8 px) marks the next step (after a pause, Continue). iOS Reduce Motion (`prefers-reduced-motion`) swaps every move for a 150 ms fade or opacity flash.
- **Opaque layers:** nothing behind a moving element shows through.
- **Back control:** a small metal `uiText.toMap` button at top-left on every screen except the sword screen, the main menu, the Map, Character, Backup (these have `uiText.back` at bottom-left, always back to the main menu), reward screens (every `rewardQueue` entry, including a boss scroll), and the daily verse; those leave only by Got it, so the queue always drains first (section 10). Mid-run it keeps the run; tapping that zone again (or the next launch) resumes it.
- **Screen title banner** on every screen except the sword screen, main menu, Backup: a flat gold ribbon at the top (no bevel, rivets, plate, shadow, or press state; never looks tappable), English in Hero Yellow (26 px), Thai under it (18 px). Titles: Map `uiText.titleMap`, Character `uiText.character` (its panes keep their tab names), Sound Duel `uiText.soundDuel`, a scroll opened from the shelf `uiText.scrolls`, reward screens `rewardText` (a verse screen given as a gift uses `uiText.verseGift`), rest screen `restScreen`; a zone run shows the zone `name`/`nameTh`; a boss run shows `zones[].boss.name`.

- **Game feel:** chunky buttons, bold colors, icon counters (gem cluster, gold star) that count up with a pop, thick rounded bars that fill with a pop and end sparkle, gear bonus pips that light like an upgrade (stone, badge, pop); no timers or pressure; a press is a short weighty dip, never a squash or bounce; Thai labels keep their size, plate and space.
- **Hero:** `state.hero` (default Sam, persists), picked on the Map (`uiText.chooseHero`): `uiText.heroName` or `uiText.heroNancy`. Every 'Sam' figure below means the chosen hero. On Character a tap pulls `sword` from `stone` (its `#au` aura on; the stone hides the blade until the fade), then `picPlan.uiInlineSvg.aura` fully envelops the hero: flame spikes at 30–60%, transform and opacity only, 1.2 s or less, still under reduced motion; hair color unchanged. Sam (`picPlan.uiInlineSvg.sam`): a young Thai American boy with glasses (thin round Ink frames; one 2 px Ink bar under 32 pt); shoulders 1.6 head-widths, waist 1.0, legs 3 heads tapering 0.5 to 0.3, no flare. Nancy (`nancy`): a woman, visibly pregnant, a loose rose-pink high-waisted tunic, belt above a gently rounded belly, upright and balanced; her weapon at her side, point down, never across or toward her belly. Both: about 6 heads tall, defined knees and elbows, soft rounded mitten hands 0.75 head long, the thumb about a third of the hand on the outer side (`#rH`, right hands mirrored), boots 0.9 head long on the ground line, Sam: small oval eyes with dot pupils (10% of head width or less), serious brows; Nancy: no glasses, warm closed-eyes smile, tiny blush (t297u); nothing behind the face; they read at 44 pt in silhouette. `color` sets the tunic, a cape goes behind, the weapon goes in `.wp`, `.ar`/`.hd` are the cheer arm and head. Rugged, zero comedy. HUD, Map emblem, Character.

**Menu palette** (main menu, Map, Character, reward and verse screens; AA-checked):

| Token | Hex | Use |
|---|---|---|
| Forest | `#0E3B22` | app background (flat) |
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

AA contrast: Hero Yellow on label plates 7.7–10.2 (4.87 on bare iron, so the plate always stays), Cream Thai 10.6+, Cream on Forest 11.9 and Meadow 6.9. Never white on Grass (3.1). Gold only on label plates (7.5+; never on bare Paper, 1.08), Hero Yellow on a plate over Paper 7.7, Ink on Paper 13.0. `prefers-contrast: more` makes label plates solid Ink.

**Fonts** (self-hosted in `/fonts/`, never a CDN): English display and buttons in **Lilita One** (OFL). Thai in **Kanit** (Thai subset); fallback `Kanit, "Sukhumvit Set", Thonburi, "Noto Sans Thai", sans-serif`. Respellings in Kanit 500, Gold.

**XP bar and coin meter:**

- **XP bar:** 28 pt tall, XP Track trough, XP Purple fill with an XP Lilac highlight band, Ink outline, label "Level N" in Gold bold on a label plate.
- **Coin meter (the ten pips),** under the gem count in the three-bar's left compartment, never merged with the XP bar: 10 original SVG gold coins (`svg:coin`, 16 pt, two rows of 5, 2 pt gaps): Gold face, thick Gold Edge rim, embossed star-and-leaf mark, white highlight crescent, 3 px Ink outline. Empty: outline only (Gold Edge 35%). Filled: shiny, with a 250 ms pop; filled coins always stay full bright.
- **Glow pulse:** when all ten coins fill and on every level-up, the XP bar area glows soft purple-gold for about 1 s (reduced motion: an opacity flash).

**Arena theme (the banner, HUD colors and Echo Forest's night; 7.1's scene is every play background).** Clearly different from the menus:

| Token | Hex | Use |
|---|---|---|
| Arena Night | `#0B1B33` | background top band |
| Arena Teal | `#0F3B4A` | background bottom, a soft grass-horizon silhouette `#123F35` |
| Star | Cream at 35% | 20–30 tiny static CSS dots in the top third |
| Parchment (MX3) | tan `#F6E9C8`, Ink text, Gold accent lines between | every gameplay button, plate, panel, question card and HUD plate; only the `#2E7D32` Next/right button and rarity rings differ |
| Aqua | `#7FE0D0` / edge `#3A9C8F` | hint button (Ink icon) |
| Zone tint | Phonics `#7FD38B`, Colors and Shapes `#F5A3C7`, Numbers `#7FB8F5`, Sight Words `#F5D06B`, Baby and Hospital `#F2B8A0`, Maxwell Says `#B79BFF`, Nancy's Kitchen `#FFC48A` | arena banner and panel top stripe, Ink text |

AA contrast: Cream on Arena Night 16.2 and Teal 11.3, Ink on parchment 15.1, on Aqua 11.7, on zone tints 7.9+. Coins sit on a dark strip (empty coins at Gold Edge 45%). Got it is Gold-plated. Menu iron tiles never appear in the arena.

**One style (t377u, extrapolated from approved looks):** Sound Duel, guardian runs and reward screens use 7.1's Home Lake template (scene, hero, parchment card at the bottom); the hub and choosers use the Map's sky sheet and scenery strips; menus take the title's four skies; Character, Pantry, trophies and scrolls sit in the gear sheet's carved frame; panels are parchment `#F6E9C8` with Gold lines; only tappables look like buttons. Each guardian, and the Echo Knight, is an original armored figure in the hero rig, 1.2 H, in its zone tint with a round shield; its silhouette is that shape in Ink at 40%. A boss win shows the guardian kneeling, `boss.name`, then the scroll. The grace line is the next `encouragement` line. `welcomeBack` is one parchment bubble on the main menu. The rest screen uses the evening sky (or the worn `restSky`).

- **Enter a run (about 400 ms):** the menu slides down and fades out, then the zone-tinted arena banner (a flat title ribbon, never button-styled) swoops in with the zone name (or boss name) and settles into the top bar. **Exit** means leaving the arena for the Map, either by `uiText.toMap` or after a run's last Got it and reward queue; it plays the same transition reversed. Reduced motion: a 200 ms crossfade.
- **HUD (the three-bar, every arena screen, just under the safe area):** three equal compartments on the grid above. LEFT: her gem count (a 28 pt gem and its number) with the coin meter under it. CENTER: Sam's 88 pt portrait (64 pt on 568 pt screens) in all equipped gear, weapon in hand, with the class line under it. RIGHT: "Level N" and the XP bar. Flat, not tappable, no buttons; redraws on the same frame as any change.
- **Cheer and nod (with aura):** on a right answer, a soft glowing aura (rising light rings and motes) rises around Sam inside the portrait compartment, never past its edge, while the hero lifts the equipped weapon (shield lifted too), then settles back to the low open stance; the only in-run time the weapon rises, never across his face. Aura color: warm Gold, or the sword's own glint color. Gift rings: owning 3, 9 and all 18 weapons each adds one faint ring to every aura (derived from `owned`; nothing to buy, no timer, no stat). On a wrong one, a small encouraging nod (head tilts up; never a droop). Both about 600 ms, CSS transform and opacity only on the arm, head, weapon and aura groups; gentle, never mocking; reduced motion: none. The animated Map hero is v6.
- The `<body>` carries `data-theme="menu"` or `data-theme="arena"`; all theme colors come from CSS variables under those two selectors.

## 4. Tech

- **App:** a PWA in vanilla HTML/CSS/JS with `manifest.json` (`display: standalone`, theme and background `#0E3B22`), `apple-mobile-web-app-capable`, `viewport-fit=cover`, and `env(safe-area-inset-*)` insets.
- **Thai:** `lang="th"` and `line-height: 1.7` on every Thai string; a box holding Thai has line-height 1.5+, no fixed height, no `overflow:hidden`, no ellipsis: it wraps (`uiText.useBackup` wraps or fits at 320 pt).
- **Storage:** IndexedDB object store `kv`, key `state` (one record, section 10), mirrored to localStorage key `naeState` after each commit; a write that throws is skipped. A missing or unreadable `kv/state` loads that mirror if its `schema` is 5020. Call `navigator.storage.persist()`.
- **Home screen:** the icon avoids Safari's 7-day wipe (iOS may still clear data when storage is low). In plain Safari, show only `uiText.openFromHome`.
- **Service worker:** cache-first, versioned. Core files (HTML, JS, CSS, fonts, SVGs, sound effects, `cards.json`) go through `cache.addAll`; each voice clip in `/audio/` is cached on its own, failures ignored. When a new version is cached, show a `uiText.updateReady` chip on the Map only; tapping it saves state, then reloads into the new version. Never reload mid-run, mid-card, or on a reward screen. Mid-run means on an arena screen; on the Map, tapping the chip reloads, and the run resumes.
- **Audio:** Web Audio API; decode each clip on first play; a missing or failed clip is skipped silently. English `speechSynthesis` at 0.85 (0.6 with `uiText.slowMode` on); no Thai voice means Thai audio is skipped. A new sound or speech first stops the one playing (`speechSynthesis.cancel()`). Verses are never spoken in Thai (section 15).
- **Audio wake:** the title tap on each launch and every `uiText.continue` tap resume the AudioContext, play a silent buffer and speak an empty utterance. Continue resumes audio and replays the English of the screen she left (a reveal, say-it card, or verse); a question screen speaks nothing, so nothing replays there; on Sound Duel, Continue replays the current pair. Nothing waits on audio.
- **Locks:** one answer per card; every button locks until the next screen renders.
- **Auto-pause:** on `visibilitychange` to hidden and on `pagehide`, pause the run and stop audio. On return show `uiText.continue`, then the exact screen she left.

## 5. Pictures

- **Picture recall** shows one picture of the answer from `pic`:
  - **Emoji** (an emoji string, sometimes two or three like "👶💤" or "☀️👶🛏️", scaled together to fit the frame): Apple Color Emoji at 120 pt, centered. 73 cards. The newest emoji used are Emoji 13.0 (🫂 `ph-07`, 🪨 `ph-12`, 🪙 `nm-04`, 🛻 `ms-22`, trophy 🪵 `frame-oak`, and the ZWJ sequence 👰‍♀️ `ph-06`; iOS 14.2+); no skin tones. If a glyph does not render (canvas width test on first launch), that card uses the null fallback.
  - **SVG** (`svg:<id>`): the 38 ids in `picPlan.svg` (33 drawn in the section 3 style, 5 supplied; `high-five` is kept in the library; `ms-31`'s buttons are hand emoji). Color cards use flat swatches; size cards show one object at its size, nothing else. 39 cards (`svg:hungry` and `svg:pray-kneel` are shared; `svg:tie` is ms-32); clock times are digital.
  - **Fallback** (`null`): the zone emblem at 40% opacity, with the Thai line moved into the frame at 28 pt as the prompt.
- **At a glance:** Every picture card must be unambiguous at a glance on a phone screen. If the image could fit two choices, or two choices look or sound alike (e.g., crib/rib), swap the wrong choice or redraw the image. Draw the ids in `picPlan.svgNotes` exactly as noted. **Clip art:** tight and realistic: true-to-life proportions and silhouettes, real detail (seams, grain, folds) in one shadow tone and the `tex` textures, one 3 px Ink outline, no faces on objects, no cartoon squash; the object fills about 85% of its frame. Emoji 13.0 or older; animate only transform and opacity.
- **Supplied art:** `picPlan.inlineSvg` holds 5 original SVGs: crib, front-desk, towel, towel-white and tie; `picPlan.trophyInlineSvg` holds 3 original trophy icons: the silver and gold card borders, and the blue-flame lantern. Every id inside a supplied SVG is prefixed with its asset name, so inlined SVGs never collide. Inline them exactly as given; never redraw them.
- **Picture frame:** Cream plate, 4 px Ink outline, 18 px radius, stone-and-metal rim, 150–200 pt square (128 on 568 pt screens); on a 320 pt screen insets trim at most 6 pt and only the picture shrinks, never the Thai. Never blank or broken; an emoji that renders as an empty box uses the fallback.
- **Props:** `asset-library/assets/props/` (crib, desk, disc, towel, tie) is reference only; a prop enters the build only as its `picPlan.inlineSvg` art when a scene uses it.
- **Drawings Build makes: 55** = 33 card ids (`picPlan.svg` minus `picPlan.inlineSvg`; `svgDrawnCount`) + 21 trophy ids (`picPlan.trophySvg` minus `picPlan.trophyInlineSvg`; `trophySvgDrawnCount`) + 1 coin (`picPlan.uiSvg`). Plus 7 zone emblems (6 drawn; Nancy's Kitchen reuses `svg:chef-hat` via `zones[].emblem`), Sam, and UI icons (leaf hint, trophy, gift, check, scroll, flame).
- **Say-it cards** are `mode: "english-first"` (section 8): no picture, no hidden word.

## 6. Screens

### 6.1 Sword screen (every launch)

- **Title (Maxwell's pick, t371u):** `.ti` gets `data-tod` from the clock each minute (`m` 5:00–11:59, `a` 12:00–16:59, `e` 17:00–20:59, `n` 21:00–4:59) and shows `title.svg`, a third file given with this prompt (`nancys-adventure-english-v6-08-title.svg`; inline it in `.ti`; `picPlan.uiInlineSvg.title` names it; its text goes in the DOM, never `<img>`, `<object>` or a CSS background; it and `.ti` fill the screen; if it is missing, stop and ask for it, never redraw it) (the t288u picture: Sam on the left hill shading his eyes, a small sword in a bush, a biplane towing a one-line banner), then the button `uiText.letsGo`. If `state.hero` is Nancy, hide `#th` and nest `picPlan.uiInlineSvg.nancy` in `#tn` (width 64, height 144). Banner text is live: `#gE` gets the `en` of `uiText.greetMorning`, `greetAfternoon`, `greetEvening` or `greetNight`; the title's `aria-label` is that `en` then `th`. Button (Maxwell's pick C, 1:37 PM PT): wide and low, English and the Thai plate on one line (two lines only if it must wrap); 84% wide (88% at 320 × 568), 60 pt tall, 24 pt (16 pt at 320 × 568) plus the safe-area inset above the bottom; `#A3211A` face with a `#B8261A` top strip, 6 px gold bevel (`#F2CF6A`, `#C9962E`, `#8A5F16`), 2 px `#5A3A0C` and 4 px Ink rings, 5 pt Ink drop, a 10 pt `#E8B84A` rivet with an Ink edge on each corner; English 22 pt (19 pt at 320 × 568) in Hero Yellow with a 3 px Ink stroke, Cream Thai on its `rgba(26,10,8,.82)` plate. Behind it, an Ink fade (0% at its top to 35% at the bottom) over the bottom 150 pt (120 pt at 320 × 568), not tappable. `.ti svg{stroke:#10170F;stroke-width:3;stroke-linejoin:round}.ti{touch-action:manipulation}.ti *{animation:none!important;transition:none!important}`. A still (t366u): one frame, shown at once, plane and banner parked on screen; no fade, delay or auto-advance.
- **Tap** (button or sword): the button press and metal thud only, then the next screen at once. A 2nd tap is ignored.
- Then follow the launch order (section 10): first launch goes to card 1 of a Phonics run (`startZone`); an unfinished run resumes at its exact card or reveal; otherwise the main menu.
- The XP bar fades in after card 1, the coin meter after card 3.

### 6.2 Main menu (the hub)

Exactly two buttons, the hearth (a corner button) and one cue: a Gold arrow bobbing at the Map button's right end (transform only; still with reduced motion), a cue, not a button. No banner, HUD, counters, chip or art; Forest background: `uiText.titleMap` (opens the Map) over `uiText.character` (opens Character, 6.6). Each is a full-width iron button 96 pt tall, 8 pt apart, in the lower 60%. Back from the Map or Character returns here.

- **Hearth leaf:** a 44 pt hearth button (a small Stone arch from `#fr` with a Gold heart; never a flame, which is `streakFlame`) at the top-right corner of the main menu and the Map, always there and free: each tap shows one soft bubble, alternating the next `encouragement` line and a `verses` line she has been given (English bold, Thai under it; until tapped or 6 s). No counter, timer, gear or level touches it. Its accessible label is `uiText.verseGift`.

### 6.3 Map (linear path, zero scroll)

- **Header logs:** the title banner (`uiText.titleMap`) over the top bar. A 12 pt wood log lies across the yellow-to-green seam, and an 8 pt log frames the whole header (top, sides, bottom): Log bark with static 1 px grain, a light top band (end cut, Ink on it 7.7), end-cut rings at the corners, 3 px Ink outline. CSS only, not tappable.
- **Top bar (the three-bar):** LEFT: `uiText.back` on a parchment plate (t306u). CENTER-LEFT: a counts plate, 2×2: gem count, Gold trophy (earned count), the `uiText.daysWithEnglish` flame (`picPlan.trophyStyle.streakFlame`), the `uiText.goldStars` star. Each: a 20 pt icon and its count in Gold `#FFCC33` (no white), 8 pt apart. RIGHT: "Level N" and the XP bar. SE height: header 214 pt (status 20, logs 28, banner 62, top bar 104) + margins 24 + rows 264 + bar or hero strip 48 = 550 ≤ 568.
- **Sheet:** the map area is one rugged sky sheet: the `zp` speckle (never under dots or labels), torn-edge SVG border, a 3D look from a 6 pt Paper-edge drop and a static inset bevel; no animation, `overflow:hidden`.
- **Path:** `mapLayout.regions` in one straight column, top to bottom in file order (Word Meadow at top, t306u). Each row is 60 pt tall, 8 pt apart, inside the 16 pt margins: a 44 pt region dot (emblem) on one left column, then its label plate (8 pt gap), English in Hero Yellow over Cream Thai 17 px+. One straight dashed path (`pathStyle`) joins the dot centers. Rows start in the lower 60%; on taller screens the spare height goes evenly between rows. Each row sits on its region's scenery strip (flowers, wheat, lake and cottage, dark trees) on one sky sheet with the sun (t306u, t346u); an unopened strip is washed soft with its guardian's silhouette standing in it.
- **No overlaps:** every tap target is its own grid cell, 44 × 44 pt or more and 8 pt from any other; nothing is placed over a row. Each plate has one 56 pt slot at its right end: the Gold `uiText.boss` ribbon once its last scene is done, else the bouncing Gold arrow on the next-step row (the open row whose end guardian she still needs, else the fewest runs today (today's `run:` ids; a Sound Duel round writes one too), with `uiText.playAgain` once all are done; ties: the next row after her last-played one, wrapping); never both. Bottom bar (44 pt): the `uiText.updateReady` chip.
- **Taps:** a row opens its zone, or a chooser with one plate per zone (zone `name`/`nameTh`) when it holds two or three; Echo Forest opens Sound Duel; after 4 rounds the Echo Knight (`uiText.echoKnight`) recaps 10 pairs, no failure, and ends like a round; not a zone guardian (no `bossesWon` or scroll).
- **Hero select (t290u):** the Map's hero band shows two parchment cards, Sam and Nancy (`picPlan.uiInlineSvg.sam`/`nancy`), each with its name in English and Thai, the `sword` in its `stone` between them (390 pt); at 320 pt a compact hero strip (heroes 40 pt, no sword or rays). Each hero is a 44 pt+ button (`uiText.heroName`, `uiText.heroNancy`; band label `chooseHero`); a tap sets `state.hero` (persists) with a bounce from the feet (scale 1.08 at 120 ms, back by 300 ms; transform only; reduced motion: instant); the chosen hero gets a gold ring under the feet and a gold name plate, the other dims to 60%. On the row she last played, a 20 pt head of the chosen hero sits at the plate's left end, not tappable.
- **Re-render:** the Sam emblem and the Map slots (`mapTheme`, `mapLanterns`, `mapPet`, `arrowTrail`) update on the same frame a trophy is worn (11.2); slot art stays on the sheet, never over a dot or plate.

### 6.4 Question screen (picture-recall cards)

Top to bottom:

1. The three-bar HUD (gems and coins | portrait | level and XP).
2. Question panel: the picture frame (section 5) inside the stone-and-parchment panel with the zone-tint stripe. The English answer is never shown here.
3. **Thai line** directly above the choices (Kanit 20 pt, Cream 80%): `thDef` if present, else `th`. 18 cards carry `thDef` (the 14 fallback cards, ph-17 "they", and the crib/bed pair ph-01, ph-03, sw-06): a 2–4 word Thai hint rather than a translation.
4. **Choices:** a 2×2 grid of parchment plates, at least 96 pt tall (72 on 568 pt screens), shuffled every card. The only English she reads before answering. Every picture card off a scene (7.1 has its own) uses this one layout on the grid: three-bar, picture, Thai line, the 2×2 plates, then the hint and main-button row, 8 pt apart (SE: status 20 + HUD 92 + frame 128 + Thai 34 + plates 152 + hint row 92 + gaps 48 = 566 ≤ 568). A choice may wrap to three lines inside its plate; if one needs more, all four drop to 18 px. The 2×2 never stacks. Strings never carry doubled or trailing spaces.
5. **Hint button:** on every question screen, bottom-left in the safe area, a 72 pt (64 on 568 pt screens) Aqua round button (tap area at least 80 pt) with a thick metal rim, a soft Aqua glow, and a leaf-heart icon, with `uiText.wordsForYou` under it (`uiText.hintButton` as its accessible label), at least 16 pt from the choices. There is no HELP button on any screen; this soft hint button replaces it.

### 6.5 Reveal screen (after every picture-card answer)

- **Header:** the next `encouragement` line on a right answer, `wrongText` on a miss. `rewardText` ("You earned this!") never shows here; it appears only as the banner of reward screens (section 9).
- **Body:** the picture, the English answer bold (Lilita One 36 pt), the respelling in Gold, the Thai under it; after a miss, the card's `trapNote` (Thai tip) under that. `faith` cards get a small gold leaf mark. The English is spoken once automatically.
- **Prompt:** `uiText.sayItOutLoud` on the first 10 reveals.
- **Buttons:** 🔊 `uiText.replay` and a Gold-plated **Got it** (`gotItText`) in the main button spot.
- **Never auto-advances.** Only Got it moves on. The hint button here gives encouragement only.

### 6.6 Character

The only screen that scrolls. From the main menu; title `uiText.character`; bottom bar: `uiText.back` at left, `uiText.backup` at right. Fixed, never scrolled: Sam's panel (`uiText.yourHero` over `uiText.heroName`, 96 pt portrait in all gear, class line, title, featured gem, gem count, gear bonus pips, 11.1; at its right two switches, `uiText.slowMode` and `uiText.restWeeks` (off: gray `#8A939C` track, knob left; on: Grass track, knob right; the knob moves by `transform` only)), the `uiText.earnedShelf` row, then 6 tabs, 3 across in two rows: `uiText.gems`, `gear`, `themes` / `titles` (`trophies[].cat`), `uiText.scrolls` (6.8), `uiText.pantry` (11.4). It opens on her newest trophy's tab. Only the pane under the tabs scrolls (`overflow-y:auto`; 120 pt+ of it shows on the SE).

### 6.7 Backup view (for Maxwell)

Opened only by `uiText.backup`, its lists scroll; silent Stone, no red: `backup` saves her record as JSON; the `needsMaxwell` list (7 cards); the `thaiReview` queue. **Restore, two steps:** 1) `uiText.restore` picks a backup and checks it (JSON, `schema` 5020, all keys but `giftGems`, `hero` and `zoneRuns`; those missing keep hers); 2) `uiText.useBackup` names both (`uiText.backupCompare`), with `uiText.restore` (a second, separate tap) and `uiText.back`. Before step 2 replaces anything, her current save is copied to the localStorage key `naeState.bak`. A corrupt, partial or empty backup changes nothing: her days, stars and given verses stay. Turning Slow Mode or Rest mode (section 13) off never costs a streak, star or coin. No Settings screen or gear: motion follows iOS Reduce Motion, contrast `prefers-contrast`.

### 6.8 Scrolls

The `uiText.scrolls` pane of Character: a shelf of the boss scrolls and daily verses she has been given, and the rest verse once seen, newest first, each free to reread any time; tapping one opens its verse screen (section 15). Empty shelf: `uiText.scrollsEmpty`. The `verses.attribution` credit line sits small at the bottom of the shelf.

## 7. Core loop

A **run** is 5 find-and-tap scenes × 5 cards from one zone (7.1), then its guardian (10). After the guardian, the reward queue drains, then the rest screen (every 3rd run, section 14) or the Map.

1. A soft cue plays. The question screen shows the picture and Thai line; nothing is spoken.
2. She taps one of the four text choices. Near-miss traps stay (play/pray, thirteen/thirty) only where the picture rules them out (section 5).
3. **Right:** within 150 ms of the tap (state and glow on the same frame; sounds preloaded; the save never delays it), the plate pulses Gold, +10 XP is committed, one coin fills, then the reveal.
4. **Wrong:** within 150 ms of the tap (same rule), the tapped plate glows Moonstone, the right one glows Gold, a soft chime plays, the meter keeps every coin (a miss costs nothing; no dimming), then the reveal with `wrongText`. The card returns 3 to 5 cards later, at most twice, except in boss runs (section 9). No miss removes a coin or XP (section 8.1 too).
5. **Coin meter:** when all ten coins are filled, the glow pulse plays, `pipFills` +1 is committed, and the coins reset.
6. **Hint:** always free; a right answer after it still earns +10.
   - First tap on a question: shows `hint.letters` (for example "p___" or "P_____ w___ h___.") and speaks `uiText.itStartsWith` plus `hint.sound` ("ขึ้นต้นด้วยเสียง /p/").
   - Further taps, and taps anywhere else, alternate in a soft bubble: the next `encouragement` line ("I love you.", 3 s), then her next Jesus word (`jesusWords`, section 15; until tapped or 6 s): the `ref` and `uiText.jesusWords` small, English bold, Thai, `thGloss` small. On the question screen, Jesus words are shown, not spoken; on the reveal, encouragement only. She has all 6 from the start (`given.type: "start"`); no gear, level or coin brings one. Once she has seen all of hers this visit (session memory only), one `uiText.jesusAllHeard` bubble; the next tap starts them over. No timer or countdown. An empty entry shows a `jesusWordsFallback` line instead.
7. **Review queue:** a missed card's id goes into the small localStorage key `naeReviewQueue` (unique ids, oldest first, at most 20; a right answer on that card removes it). On her next visit (a new app open), up to 2 queued cards missed on an earlier visit appear within the first 3 cards of her first run (right after the easy opener): cards from that zone only; never in boss runs. No new UI, label, timer, or penalty; they score like any card. Only picture-recall misses enter it (say-it and two-answer cards never do). If the key is missing or not valid JSON, the queue is empty and is rewritten; an empty queue simply adds no cards. The key sits outside `state` and is not in backups; losing it loses nothing. Full Leitner boxes stay in v6.
8. **Out in the world:** each run of 4+ cards includes one card from `meta.outings` (practical phrases for shops, the clinic, church and the restaurant) from her zone if it has one, after the opener; it scores as usual.
9. **Run order:** at most 2 `faith:true` cards per run; skip unwritten cards (`fill:true`, empty `en`); open with one `easy:true` card (every zone has at least 2), preferring her zone; then, on a new visit, up to 2 review-queue cards (step 7); then written `personal:true` cards; then the rest, at most 8 never-seen (`seen`, fewest `en` words first) once the zone has 7 seen, the rest seen longest ago. Never 4 say-it cards in a row while a choice card is left; this rule wins over the order above.

### 7.1 Find and tap (t312u/t313u, council 3:52 AM)
- A scene is the zone's #77 background holding the run's next 5 cards with a `pic` as tap objects; each in turn is the target. Cards without a `pic` play on their own screens (6.4, 8, 8.1, 8.2): at most one between scenes, never back to back; leftovers wait for her next run there. The tan question card reads `uiText.tapPrompt` ({word} = `en` in both lines, never `th`) when `en` is 1–3 lower-case words with no . , ? ! and no leading "a " and `pic` is not null (not ph-02, ph-07, ph-08, ph-11, ph-17, ph-21, ph-24, cs-22, cs-23, cs-24, sw-15, sw-18, sw-19, sw-24; colors cs-08–cs-15 drop "the": 'Can you find red?'), else the card's own `en` ('Let me fix your tie, honey.' → the tie); scene k uses object layout k of 5. If a zone has fewer than 25 `pic` cards, the run repeats those seen longest ago, never twice in one scene or as the next scene's first ask. Never in one scene (one waits): ph-02/25/26, cs-08/17/18, cs-02/09/20, cs-11/16, cs-15/19, cs-01/03, cs-04/21/22, bh-12/16/21/28/31, ms-19/20, cs-02/08/23/24, nm-02/16, nm-05/17, nm-06/07/12, nm-14/24, fd-02/11. Its Thai wraps, never cut or shrunk. Say-it cards keep Got it after the tap.
- Scene screen, one template for every zone and hero (t376u, the t328u Home Lake shot; not 6.4's frame): the scene fills the screen, no arena panel. Top: a slim bar (`uiText.back`, gems, stars, Level plate with XP bar, streak flame) and the zone chip (`mapLayout` name, en and th); on guardian runs the zone chip shows `boss.name` and the scene shrinks to sit below it. The hero stands centered, H = 195 pt tall at 390 × 844, feet on the floor or ground at y 700 with a contact shadow, the free hand palm-up at the waist (hand 18 long, thumb 6.3); eyes happy and closed on ask screens. Props scale to H: desk top 0.39 H (hip), crib rail 0.60 H (waist), window sill at chest height, window top 1.3 H above the wall base. Objects are drawn in the scene, never on tiles, each on its furniture or ground (44 pt+ tap areas, 8 px apart, no overlap); a scene is one 390 × 844 layout, scaled as one piece to the screen width, bottom pinned, sky cropped; the crop never puts a target under the HUD (the scene shrinks to fit instead); targets keep 16 pt from the screen edge; on taller phones the front desk and kitchen crop their ceiling to the 320 × 568 framing; the HUD, card and 44 pt tap areas stay full size. The parchment question card sits at the bottom, 🔊 `uiText.replay` at its right, the hint button beside it. 6.5's Reveal follows each right tap. Scenes: Word Meadow, a park (swing set, bench, bus stop, kite); Golden Fields, a farm (corn row, gate, cow, basket); Home Lake, inside the home (shelf, window, desk, crib, rug); Echo Forest, night woods in Arena Night over Teal (owl and lantern on branches, tent, footbridge), also behind Sound Duel. **Time of day (Maxwell: by level inside each zone):** each scene root gets `data-tod`, set at run start from that zone's step, 1 + `zoneRuns[zone]` mod 5 (her finished runs there, Sound Duel rounds for Echo Forest, 0 if unset; a resumed run keeps it), a CSS var swap of sky, ground and light tint (the title's palettes): step 1 `m` morning, 2 `d` midday (the `a` sky lighter), 3 `a`, 4 `e`, 5 `n` night, then `m` again; props, layout and taps never change; Echo Forest at `m`/`d` is the same woods in dawn mist. Word Meadow alternates a second layout, the park by a pond (swing set left, bench right, pond mid-right); a floating object sits on the pond with a ripple. Every object stands on a surface (ground, bench, desk, shelf, counter) with a contact shadow, sized to the hero, never floating. **Front desk (Home Lake):** Maxwell Says `ms-03`–`ms-06` and `ms-21`–`ms-23` play in a hotel front desk (only them in that scene, repeats filling it): the same wall, floor and window; a wood counter across the right (hip high, three front panels); a wall clock; a full-height room door with a gold 13 on the left wall; keys on a wall key rack; a book on a shelf; the truck small and far, half behind the hill in the window. No names or signs. Kitchen runs use the home room set for a meal: the crib makes way for a small table (cloth, 2 legs), food on the table, desk and shelf.
- **Listen and find:** in each scene the 3rd target is spoken only: the card reads `uiText.listenFind` with no word and plays it once; 🔊 replays it. Same taps, reveal and grace.
- **Count it (Numbers, once per run):** the scene shows N of one prop (cow, basket, hat), N from a picture number card 2–10; the card reads `uiText.howMany` ({thing} = cows, baskets or hats; cows use `uiText.howManyCows`) with 3 number plates: the right word and two other number words. Scenery copies of the prop hide; Count it, Big or small: never the spoken target. Right = that card's usual reward; grace as 7.1.
- **Big or small (Colors and Shapes, once per run):** the hero holds a `meta.sizeSort` picture on the open palm; two baskets with the `cs-23`/`cs-24` words as tappable plates; she taps the one that fits. `uiText.bigOrSmall`. Grace as 7.1; it awards, reveals and resumes as the scene card `cs-23` or `cs-24`, the word that fits (ledger `card:<runId>:<index>`).
- Right tap: Gold glow, star burst, the card's usual XP, coin and stars. Another tap: that object wiggles, the right one glows as a hint, then `wrongText` and a grace line; she tries again. No timer, nothing lost: no return (rule 4 is for question screens).

## 8. Say-it cards

74 cards are `type: "say-it"`, `mode: "english-first"`: 70 written plus the 4 empty slots (section 17).

- English bold on top, respelling, Thai underneath; the English is spoken. She says it aloud and taps **Got it**. A `reply` (only `bh-11`) shows small under it, English then Thai, never spoken; no countdown.
- No choices, no wrong answer, no picture unless it has `pic`. A Kitchen say-it card with `pic` is found in its scene, then shows English-first. Got it is a right answer: +10 XP, one coin, Gold Stars, `rightByZone`; never removes a coin.
- Hint replays the phrase slowly. Never in boss runs. A `faith:true` card never repeats when she taps Got it without speaking; no prompt to say it again.

### 8.1 Two-answer card (pray or high five)

`ms-31` (`type`/`mode` `"two-answer"`) breaks the normal formula: no reveal, no auto-advance, and a wrong tap costs nothing.

- **Prompt:** each time, one of its 2 `prompts` at random: English bold, Thai under it, English spoken once. The card's `en`/`th` are the Thai Review Queue summary only.
- **Buttons:** two big picture buttons from `choices`, each on a 124 pt bordered parchment plate (Ink edge, Gold inner line): 🙏 `uiText.pray`, 🙌 `uiText.highFive`. Hand-only emoji (Unicode 13.0 or earlier) are fine as emoji; people or bigger pictures (a hug) are drawn from `picPlan.svgNotes` on the same plate, never emoji; a reveal picture (t423u) that can stand is a 64 pt prop on the ground with a contact shadow (an emoji person: 52 pt, centred between the screen edge and the hero), else a 124 pt framed plate at the top right, never over or beside the hero; no press sound; the prompt's `answer` is the right `key`.
- **Right tap:** Gold glow, +10 XP and one coin (once per card), then `uiText.done` in the main button spot; only Done advances, one card.
- **Wrong tap:** a soft Moonstone X fades over that button: no red, no buzzer, thud, or any sound, no shake, no `wrongText`, no droop (the small encouraging nod is fine). No coin is removed and no XP is lost (as in section 7). Then the right one glows Gold; tapping it still earns +10 XP and one coin.
- Hint replays the prompt slowly; never in boss runs; counts as `faith:true`. Fits the iPhone SE without scrolling.

### 8.2 Server Talk (`type: "server-talk"`, Nancy's Kitchen)

`fd-29`–`fd-38`: `uiText.serverAsks`, then a server's question (`en` bold, spoken once, `th` under it) and 4 reply plates (`choices`, the 2×2 of 6.4); she taps the reply that fits (`answer`; `trap` is a near sound). No picture; hint, scoring, reveal and review as a picture card (section 7).

## 9. XP, levels, rewards

- XP to reach level 2: 60; level 3: 250 total; after that 100 + 60 × (L − 3) more per level. Cap: level 20 (its XP bar stays full).

- **Boss:** exactly the 10 picture cards in `zones[].boss.cards`, a recap after scene 5 of a run in that zone (zones without a guardian end at scene 5). **Intro:** the Map's `uiText.boss` ribbon (in its row's slot) plus the arena banner showing `boss.name` on entry; no separate intro screen. **Run:** each card answered right drops the guardian's bar by one tenth; a miss gets the hint glow, `wrongText` and a grace line, and she tries again. When all 10 are right the bar is empty and the guardian kneels; a reveal plays; when her region's end guardian kneels, the next region opens (rule 4). No failure state; `uiText.toMap` keeps progress.
- **Boss win (once per zone):** boss win commits before its animation; the scroll waits in the queue. The commit (`boss:<zone>` ledger, `bossesWon`, scroll pushed to `rewardQueue`) happens in one transaction when all 10 are right; a kill mid-animation loses nothing and shows the scroll on relaunch. Then, after the kneel, a boss-win screen shows the `rewardText` banner once (`bossesWon` already committed) with Got it; then, as its own separate screen, the scroll unrolls as a gift (section 15) under `uiText.verseGift` (the scroll screen never shows `rewardText`), Maxwell's boss clip plays (visuals play even if it's missing). Then the reward queue (scroll first). Replays give card XP and Gold Stars only.
- **Level cosmetics:** each is the `trophies` entry with `unlock: {type: "level", n}` (12, levels 2–20; level 20 gives a title and its crown frame). Rule 4 holds: one small reward per level. Bosses are in Phonics, Baby and Hospital, Colors and Shapes, Numbers and Sight Words; Maxwell Says and Kitchen have none.
- **Celebration** (level-up and new-zone reward screens): CSS-only ribbon drop and one fall of soft confetti, about 1.5 s; nothing flashes more than 3 times a second; no new sound; reduced motion: a 150 ms fade, no confetti.
- **Reward screens:** a Cream-and-Gold panel with the picture, English bold, Thai under it, and Got it; never auto-advance. `rewardText` shows once per screen, as the title banner, in English once and Thai once; never repeated in the body.

## 10. State, awards, resume

- **One state record** `kv/state`: `{xp, level, pipFills, goldStars, pantryOwned[], rightByZone{}, bossesWon[], owned[], equipped{}, ledger{}, rewardQueue[], scrolls[], seen[], run{id, cards, index, phase}, pips, streak, giftGems, hero, zoneRuns{}, settings{slowMode, restWeeks}}`. Every change is one readwrite transaction on it. Counters only go up, except `goldStars` (Pantry). `giftGems` feeds no trophy, gem count or gear bonus; missing, it reads 0 (no `schema` change). The record carries one version field, `schema: 5020`. On launch, if `schema` is missing or different, the saved playtest data is reset to a fresh start (Nancy has never installed an earlier version, so there is no migration code). Build never changes `schema` on its own: once Nancy has real progress, a version that changes it must ship a migration first (v6 list).
- **Idempotent awards:** each award has an id, recorded in `ledger` in the same transaction; a repeated id is skipped. Ids: `card:<runId>:<index>`, `say:<runId>:<index>`, `pips:<n>`, `duel:<roundId>:<pair>`, `round:<roundId>`, `run:<local date>:<zone>:<runId>`, `buy:<id>`, `region:<id>`, `level:<N>`, `boss:<zone>`, `day:<local date>`, `verse:<local date>`, `gift:<local date>`, `unlock:<trophyId>`.
- **Answer awards** commit at the answer tap, before the reveal shows.
- **Level-ups:** after any XP award, in the same transaction, handle every level crossed (one award can cross several): apply each level's reward once and push one `rewardQueue` entry per level, in order. Then run the trophy check (11.2); gear bonuses follow the gem count (11.1) and are never stored.
- **Derived on every render, never stored or cached:** every Map row, dot, path and emblem (rebuilt from `zones` and `mapLayout` on each return and tab switch; never reuse old DOM or a one-time animation state), boss ribbons, the HUD.
- **Scrolls and `bossesWon`** are sets; adding twice does nothing.
- **Reward queue:** shown after the current Got it (or at run, round, or boss end), one entry per screen; each Got it removes its entry in one transaction. It drains before the rest screen or the Map.
- **Resume:** `run.phase` is `question` or `reveal`. A kill on a reveal resumes on that reveal with no new award. A scene resumes with its earlier targets done.
- **Launch order:** sword tap → reconcile (11.3) → `rewardQueue` → run or main menu; the daily verse, if due, pops up over the main menu (first launch: her first menu visit after the Phonics run); the title never shows a pop-up.
- **Restore** (6.7 step 2) replaces the whole record in one transaction, then reconciles.

## 11. Character

Every cosmetic is one of the 42 `trophies` or a tier slot (Pantry items, 11.4, are separate): 5 gems, 17 gear, 14 themes, 6 titles; other than weapons they are earned automatically. Weapons (11, `wt` type; gentle, never gory) follow the gear rule (11.1); every name is unique and shows under the item in Character and on its reward screen.

### 11.1 Character screen (6.6)

- **`uiText.earnedShelf` shelf** ("My newest trophies") in the fixed row above the tabs (6.6): 44 pt icons, earned first, no text; it never repeats `rewardText`.
- **Grid:** 3 across at 320 pt (4 across at 375 pt+) trophy cards (Cream plate, Ink outline, Stone rim): near-square art area on top, picture about 80% of it (sizes may vary a little); the card grows taller so the 17 px Thai never clips; name bold, Thai under it (`th`; wherever a trophy's Thai shows, gear uses `thGloss`). Colors and sizes per `picPlan.trophyStyle` (`gems`, `enlarged`).
  - **Earned:** full color; the equipped one has a Gold glow, a ✓, and `uiText.wearing`.
  - **Not yet:** full color, never grey or dim (only its rank rings sit at 60% opacity, 3.3:1+ on Ink, non-text), a small gift icon at top-right, no 'locked' wording, and its goal from `uiText.unlocksAtLevel`, `unlocksPips`, `unlocksZoneRight`, or `unlocksBosses` (by `unlock.type`) in a gifting tone ("Yours at level 6", "Yours after 2 boss wins") and a Gold progress bar.
- **Rank trim (CSS only, no new SVG):** a trophy's rank comes from `unlock.type`: start 1, level 2, pipFills or zoneRight 3, bossesWon or secret 4. Rank shows by count, never by color alone: rank 1 is the Stone rim alone; 2 adds one 3 px inset ring; 3 adds two; 4 adds two plus 2 Gold studs at the bottom corners (the button rivet dots). Ring colors: 2 emerald `#00D26A`, 3 sky `#4FA3FF`, 4 Gold `#FFCC33` (7.0:1+ on Ink). Rings sit just inside the Ink outline (inset box-shadow) and take at most 6 pt total; the picture shrinks, never the name, Thai or plate padding. No rank words on screen; Pantry items have no rank. Safari 14 CSS: no aspect-ratio, :has(), color-mix() or container queries.
- **Heroic trim:** the title ribbon, verse card and hero panel get a 2 px Gold inner line on Stone, Dark Gold `#8A6200` on parchment, with the existing bevel and rivets; no new art.
- **Juice:** one pop per event (600 ms or less, transform and opacity only, never box-shadow or filter animation; the glow pulse, ribbon and confetti keep their times, and every glow fades a layer's opacity); no combo meters, lives, move limits, boosters or near-miss screens.
- **Tap an earned trophy** (or `uiText.wearIt`): applies instantly: state and UI update on the same frame (avatar, HUD, ✓), then it commits to IndexedDB and the localStorage mirror; a Gold glow and soft chime of 300 ms or less never block input; repeat taps while applying are ignored. All trophy art is preloaded at launch in fixed-size cells, so nothing shifts or flickers; free, reversible, no confirm, and it never changes XP, level, counters, or `owned`. One per `slot` (`cardFrame`: oak, silver, gold, or hearts). Tapping an equipped optional item again unequips it. A not-yet trophy only shows its goal.
- **Gear rule: levels open tiers; stars buy; guardians give types; one tap equips.** Reaching a tier's level (`meta.weaponTiers`) opens that tier's weapons in the `uiText.gear` tab (`uiText.nextWeapon`, 'Next weapon at level {n}', under the hero panel until all are open); a not-yet tile shows `uiText.weaponEarnAt`, and `uiText.weaponInShop` toasts once when a tier opens; she buys one for its tier's `trophyRules.tierStars` (tier 1 is hers free when its row opens, no `getFor`) with `uiText.getFor`, and that same tap equips it (ledger `buy:<id>`). Short of stars, the tile shows its price only; stars never go below zero and never hold back a lesson. Owned weapons swap free on Character (`uiText.weaponUse`; equipped: `uiText.weaponInUse`). Exceptions: `sword-iron` at start; the Bible sling and hammer (flourishes) are free when their tier opens (`uiText.weaponNew`); `cleaver-bloodtide` (second-to-last) and `greatsword-dragonbane` (final) are free earned rewards at their boss milestones (`uiText.weaponNew`, offered to equip); `sword-sunforged` comes only from the secret goal (11.2). Never real money, timer or offer. Gems still add the glow, halo and slide (`meta.bonusGems`), visual only.
- **Weapon bonuses (a row's tier 1 is its `trophyRules.theme` word, tier 2 its `2` form else + Hint, tier 3 that + Star, or + Hint if it has Star; `meta.weaponBonus` for the rest; each word a `uiText.bonus<word>` line; English progress and stats only):** shown on the weapon card and under the hero panel (`uiText.weapon`, English name, the bonus lines in English and Thai). `bonusRespell`: the respelling shows before her first pick. `bonusHint`/`2`: 1/2 cards per run open with `hint.letters` shown. `bonusRetry`/`2`: per run her first 1/2 misses may pick again (no coin or star lost, no XP for the retry, the card still returns). `bonusStar`/`2`: +1/+2 Gold Stars on a spoken Got it. `bonusStreak`/`2`: +1 coin per 3/2 right in a row. `bonusSlow`: Slow Mode at 0.5. A shield's bonus adds to its sword's. No bonus turns a miss into a right answer. Gear never touches verses: the hearth leaf, daily verse, scrolls and Jesus words stay free and word for word, and no gear unlocks, boosts or reorders them.
- **Shop rows (t315u; title `uiText.gear`):** one row per `trophyRules.rows` type (sword row: `sword-iron` as tier 1, then shield and sling; free gifts Bloodtide, Dragonbane and Sunforged sit beside the Greatsword row, the crook beside the Mace row), headed by its English `typeNames` name and tier 1 bonus line, then 3 slots: common, rare, legendary (MX2). Each slot is its named trophy (`tier`), else `tierNames[t]` + type name with the type's `weaponParts` art and id `<type>-t<t>` (e.g. `axe1-t2`), kept in `owned`/`equipped` like a trophy id. Rarity has no words: rings by rank (common 1, rare 3, legendary 5 + glint; untiered Bloodtide, Dragonbane, Sunforged ring as legendary) plus `tierColor` as `--b`. Uncommon and epic come as a Dec–Jan drip. Legendary (tier 3) is a `.sil` silhouette with only `uiText.getFor` and the star icon until tier 3 opens and her stars reach its price; then an 8% bounce and one sparkle reveal it, and one tap buys and equips it. Never 'locked' or 'not enough'. At 320 pt a row scrolls sideways (`transform`, reduced-motion safe), 44 pt cards. Pacing targets her 2–3 favorite types by Dec 5; the rest are optional.
- **Gifts from guardians (t360u):** Sword and Greatsword from the start; a `trophyRules.giftOf` row opens when that zone's guardian is won (its own `uiText.weaponNew` screen after the scroll; if tier 1 is not open yet, that screen waits until it opens); the Gentle guardian gives the crook (`unlock.type` `guardian`). Before that, its art shows as a soft Gold outline with `uiText.giftFrom` ({g} = `boss.name`, 'The' as 'the'); then tiers open by level. Switching types on Character is free.
- **Gear words (t358u):** a `word` [word, meaning, Thai] shows in the piece's tooltip under its name (the panel above the rows, for the last tapped piece, and its reward screen; never hover): the word in Gold (Dark Gold `#8A6200` on parchment), the meaning, the Thai. `ref` (free or given pieces only) is a small reference label: never verse text, never tappable, never sold. No word count.
- **Gear sheet (t350u, t357u):** the gear tab opens full screen (the hero panel and tabs hide; Back returns), header `uiText.gear` and the star count, in a carved dark-wood frame (`#3A2618`, Gold filigree corners) on parchment panels: the hero in the center, equipped slots around as beveled square tiles, rings glowing in `--b` (opacity only), type rows below; tooltips dark `#241A12` with a Gold line and parchment inside. At 320 pt rows scroll sideways under the hero. Original art only.
- **Hands (`trophyRules.hands`, t298u/t299u):** `one` (1H sword, 1H axe, 1H mace, sling) in the weapon hand, the other hand empty; a 1H sword, axe or mace may add `shield-sunrise` (round or square, t336u) in the off hand (`.wq`). `two` (2H sword, crook): both hands, no shield. Equipping clears what no longer fits. Off-hand lantern, tome and orb are v6. Dragonbane (Watchman v2): a true two-hand greatsword, a wide square-tipped blade with a dark fuller, a Gold horned guard, a red-wrapped grip as long as two fists and a round Gold pommel with a red gem. Icons: Build draws each weapon from the shared `#wb` parts (`picPlan.weaponParts`; Watchman's library art is reference only).
- **Hero pose:** an open, ready stance (feet apart, free hand open). The equipped weapon is drawn in the hero's hand (`.wp`; pairs and the shield add `.wq`) in the Character portrait (the title keeps the approved t288u pose: Sam's free hand shades his eyes), 1H sword, axe and mace up in one ready grip, wrist in line with the handle (t340u); two-handers in the v5 shoulder rest (blade behind the head, guard on the shoulder, hand at the upper chest), Sam and Nancy alike, never across the face or Nancy's belly; a weapon change redraws it on the same frame.
- **Class line:** under Sam's portrait (HUD, Character; never on the Map emblem), the equipped weapon's `classTitle` (Maxwell's mapping; only weapons set the class): by its `wt` in `trophyRules.classes` (`uiText.classDefender`, `classKnight`, `classWarrior`). The shield has no `classTitle`: with it equipped, the class line is hidden. Words only; no stats. Earned titles (`title` slot) still show on the avatar.
- **Where slots render:** `weapon`, `cape`, `tunic`, `avatarFrame`, `featuredGem`, `title` on the avatar; `mapTheme`, `mapLanterns`, `mapPet`, `arrowTrail` on the Map; `cardFrame` around the question panel; `restSky` on the rest screen; `auraRing` on the cheer aura (the Golden Spoon adds one soft gold ring); `swordSplash` on the sword screen; `sparkle` on right answers.
- **Weapon flourishes:** the 3 Bible weapons (`sling-shepherd`, `staff-shepherd`, `hammer-builder`) show `uiText.weaponGift` under them in Character once she has them. Swords glint in their color on a right answer.
- **Secret blade:** `sword-sunforged` (`unlock.type` `secret`) shows until earned as a flat `#5E6468` silhouette (`.sil *{fill:#5E6468;stroke:#5E6468}.sil{--b:#5E6468;--d:#5E6468;--g:#5E6468;--h:#5E6468}`, glint hidden), seen but not equipped, with `uiText.secretCaption`. Earning it plays a one-time reveal: the silhouette fades to gold, one glint, `uiText.secretReveal` (transform and opacity only).
- **Defaults** (`unlock.type: "start"`) are owned from first launch. `state.equipped` persists choices.

### 11.2 Unlocks

- **Goals** (`trophies[].unlock`): `start`, `level`, `pipFills`, `zoneRight` (`n` right answers in `zone`; Golden Chef: 25 in Kitchen), `bossesWon`, `guardian` (that `zone`'s guardian won), `secret` (all 4 Map regions played through and 100 spoken Got it, lifetime; no timer or streak). All come from play, never from days or sessions; the gold gem needs all 5 bosses.
- **Trophy check:** inside the same transaction as every XP, coin, day, or boss award. Each trophy whose goal is met and whose `unlock:<id>` isn't in the ledger is added to `owned`, ledgered, and queued as a reward screen: picture, name, `uiText.wearIt`, Got it, under the `rewardText` banner. rewardText shows once, as the banner; never repeated in the body.

### 11.3 Reconcile on launch

- Recompute every goal from the counters; grant any met-but-missing trophy through the trophy check. Never remove an earned trophy.
- Drop duplicate `owned` ids and any id not in `trophies`, tier slots or `pantry.items`, and any `equipped` id not owned (fall back to the default).

### 11.4 Golden Pantry

The `uiText.pantry` tab shows a chunky stone-and-Gold shelf of `pantry.items` (cosmetics only, never trophies or verses; a `tint` item recolors the hero's tunic, no rings): each tile shows its picture, name, Thai, and a gold-star price (owned: ✓ and `uiText.wearIt`); `uiText.getFor` asks once, then a soft thud, the stars go down by `stars`, and the item is hers to equip in its `slot` (state `pantryOwned[]`, ledger `buy:<id>`). She earns `pantry.earn` Gold Stars per right answer (Sound Duel too) and finished run (ledger as the card or run). No timer, sale, stock limit, offer or real money; stars drop only here and in the gear tab.

## 12. Sound Duel

- The Echo Knight (`uiText.echoKnight`) shows two similar word tiles (light/right, fine/file, thirteen/thirty) and speaks ONE of them at random; she taps the word she heard (English; a pair with `pics` shows each emoji left of its word, 38 pt). Each pair uses the next on-device English voice (`speechSynthesis.getVoices()` with `lang` starting `en`, up to 4, in turn; one voice if that is all there is; load voices on `voiceschanged`, and if none arrive, use the default voice). Rounds of 8 pairs, untimed, no score, can't be lost.
- +10 XP per right answer. Free `uiText.hearItAgain` replays that one word slowly, same voice. Right answers fill coins; misses never remove or dim a coin.
- **Round end:** `uiText.roundDone` with +30 XP, then Got it, then the reward queue, then a choice of the next round or `uiText.toMap`.

## 13. Day streak

- The `uiText.daysWithEnglish` flame in the Map top bar. A missed day pauses it and never resets it. On return: `welcomeBack`. With `uiText.restWeeks` on, the flame shows a moon (a resting season; nothing else changes).

## 14. Rest screen (optional victory lap)

- After every 3rd finished run since she opened the app, once the reward queue drains: a celebration shows `restScreen` with `verses.rest` (framed with `uiText.verseGift` the first time; once seen it joins the Scrolls shelf, section 2) with a soft Gold burst and two buttons: `uiText.keepGoing` (primary, Gold) starts her next run in the same zone; `uiText.restNow` and the back control go to the Map. Nothing waits; the app never closes itself.
- No session length, daily cap, play timer or forced rest; the whole game can be finished in one sitting.

## 15. Bible verses

- **Boss scrolls** (`zones[].boss.scroll`): Phonics Genesis 1:1; Colors and Shapes Genesis 9:13; Numbers John 6:9; Sight Words 1 Samuel 17:45; Baby and Hospital Isaiah 40:11. Saved to Scrolls (6.8).
- **Daily verse** (Maxwell 7:38 PM PT): one memory verse a day on her first open each day, over the main menu (never the title, t404u), in the pop-up below, seen on Got it (ledger `verse:<local date it opened for>`), else shown again next launch (section 10). Day d = whole local days since `verses.weeklyStart`; the 40-day cycle (`meta.dailyVerses`) is the 10 `verses.weekly`, then the 30 in `daily-verses.json`, a second file given with this prompt (`nancys-adventure-english-v6-08-daily-verses.json`; `rule`, `verses[]`: `ref`, `en`, `th`, `enUrl`, `thUrl`; optional `enGloss`/`thGloss` show small under the Thai, never spoken); index ((d mod 40)+40) mod 40; as `verses.rotation`. Free, never sold; a missed day costs nothing; given verses stay on Scrolls. Daily texts are VERIFIED (see the file's `verifiedBy`). Same text rules.
- **Verse card style:** chunky rounded card, bold saturated Gold and parchment frame, a reward-pop entrance (about 600 ms; none with reduced motion), a chunky Gold Got it. Visual only.
- **Verse screen (scrolls and daily):** a cream parchment panel with a Gold and metal frame: when newly given, `uiText.verseGift` ("A gift for you") at the top; the reference, the English verse bold, **the Thai verse directly under the English**, tap to hear (English only), then at the bottom one small line `uiText.askMax` ("Don't know a word? Ask Max."), then Got it.
- **Daily verse pop-up (Maxwell's pick B, t399u):** a centered parchment card over the main menu (Ink 50% scrim; menu inert): flat gold ribbon `uiText.verseOfDay` (th under), `uiText.verseGift`, ref, `en`, a gold rule, `th`, sources; only the verse body scrolls, the buttons always stay in view; bottom row: a round Replay shield (`uiText.replay` under it) and a wide `gotItText` button in the 6.1 style. Got it closes it. After a missed day `welcomeBack` shows first, then this.
- **Daily gift:** on her first main-menu visit each day, a flat dashed-gold tag (never a button), `uiText.dailyGift` with one small gem, sits above the card (alone on days the verse is already seen); ledger `gift:<local date>`, `giftGems` +1. It never depends on the verse (shown, read or closed) and never gates or boosts it.
- **Verse text is filled and verified (16 verses).** English is the ESV (`enSource`, bible.com version 59); Thai is the Thai Standard Version 2011, ฉบับมาตรฐาน, Thailand Bible Society (`thSource: "THSV11"`, bible.com version 174, Maxwell's choice). Each verse has `status: "VERIFIED"` and its `enUrl`/`thUrl` (data only, never links). Build never generates, edits, trims, capitalizes, or re-punctuates verse text; show it exactly as in the file. **Decided by Maxwell:** Isaiah 41:10 starts with a lowercase "fear not", exactly as the ESV prints it; shown exactly as printed, honesty over formatting (`verses.decided`). The unmatched quote marks in John 3:16, Joshua 1:9, and 1 Samuel 17:45 (including the orphan opening mark) also stay exactly as printed; never add or remove a quote mark. A `\n` in `en` or `th` is a poetry line break: render it as a line break, speak it as a pause (`verses.textRule`). Verse tap-to-hear speaks en only; never speak th. (`verses.ttsRule`) (The Thai is for her to read; no verse is ever spoken in Thai, even if a Thai voice exists.) If a half is ever empty, hide it and never speak it.
- **Jesus words** (`jesusWords`, 6; hint bubble only, never on Scrolls, never purchasable): whole verses of Jesus speaking, from the same bible.com versions, under the same text rules: never add or remove a quote mark (John 14:1 opens with one; John 8:12 keeps its narrator words and marks). `status: "VERIFIED"` (`verifiedBy`); Build shows them exactly as written. `thGloss` is separate helper text, never part of the verse or spoken.
- **Credits:** `verses.attribution` shows small on the Scrolls shelf, each line word for word from its publisher: `esv` is Crossway's official copyright notice for digital works quoting more than one translation (crossway.org/permissions), and `thsv11` is the Thailand Bible Society's own credit for THSV11 as published with bible.com version 174 (four lines: Thai, then English; keep the `\n` breaks). Sources are in `esvSource` and `thsv11Source`. Never shorten or translate either. Per Crossway, each English verse carries a small `verses.attribution.esvTag` ("(ESV)") after it and each Thai verse a small `thsv11Tag` ("(THSV11)"). Show the tags as separate small text; never speak them or join them to the verse text. (`tagRule`)

## 16. Cards

- **211 cards** in `cards.json`: 207 written plus 4 empty personal slots. Format:
  Compact fields: a card's zone is the `zones[]` entry whose `prefix` (space-separated) starts its `id`, cards in file order; a string choice is its `en`; `hint` is `[letters, sound, word]` (a missing `word` is `en`; a string is the `sound`, `letters` then `en`'s first letter and one `_` per other letter); a missing `type` is `meta.typeByZone`, then `picture`.
  `{id, zone, type, mode, en, th, thDef?, thDefStatus?, respell, pic, choices:[{en}×4], answer, hint{letters, sound, word}, trap, trapNote, fill?, tag?, easy?, faith?, personal, slot?, prompts?, reply?, syl?, nursePhrase?, thStatus?}`. A missing field takes `meta.cardDefaults` (`fill`, `easy`, `faith`, `nursePhrase`, `personal` false; `tag`, `answer`, `trap`, `trapNote` null; `choices` []; `type` `picture`); a picture card's missing `answer` is its `en`; a missing `mode` follows `meta.modeByType`; a missing `thStatus` is `meta.cardThStatusDefault` (`NEEDS NANCY`). A missing `thDefStatus`, and outside verses, Jesus words, scrolls and `pantry` a missing `thStatus`/`nameThStatus`, is `meta.thStatusDefault`.
  - `hint.word` is data only (the word `hint.sound` comes from); never display it. `trapNote` shows on a miss. `tag: "Example"` shows `uiText.example`. `slot` names an empty slot's topic.
  - `picture` cards: `mode: "picture-recall"`, with `pic` and `hint`; `answer` and `trap` are among the choices.
  - `say-it` cards: `mode: "english-first"`, `choices: []`, `answer: null`.
  - `two-answer` cards (section 8.1): `mode: "two-answer"`, `choices` [{`en`, `key`, `pic`}]×2, `prompts` [{`key`, `en`, `th`, `respell`, `answer`}]×2, card `answer: null`.
  - `nursePhrase: true` marks `bh-01` to `bh-10` for the Thai Review Queue.
- **Top-level data:** `zones` (with `emblem`, `zoneClip`, `nameThStatus`, `startZone` = Phonics, `prefix`, and `boss` with `name`, `cards`, `clip`, `scroll`), `soundDuel.pairs` (`a`, `b`; 30), `verses`, `jesusWords` (`given`, `thGloss`, `thGlossStatus`, `thGlossBy`), `jesusWordsFallback`, `picPlan` (with `inlineSvg`, `trophyInlineSvg`, `uiInlineSvg`, `svgDrawnCount`, `trophySvgDrawnCount`), `trophies` (weapons carry `classTitle`), `trophyRules`, `mapLayout` (`regions` with `zones`, `color`, `accent`, in path order; `paths`; `pathStyle`), `uiText` (97), `encouragement` (7), `rewardText`, `wrongText`, `welcomeBack`, `restScreen`, `gotItText`, `rewardClips`, `needsMaxwell`, `meta`. File strings win over any Thai here.
- **Traps** are the nearest wrong choice: a sound-alike for Thai speakers (R/L, TH, V/W, dropped endings) only where the picture rules it out (section 5).
- **Tiers:** a very simple word (pizza, taco, cake, corn dog) is never a bare card; it sits in a phrase ("A slice of pizza, please."). A hard word carries `syl` (`spa·ghet·ti`): the reveal and say-it card show it under the respelling, and 🔊 first plays it at Slow Mode speed. The six Thai dish names may stand alone. No tier label, score or timer.
- **Thai:** Build never writes or edits Thai. Every Thai string is a `NEEDS NANCY` draft and still shows, with a tiny dot only the Backup view explains.
- **Personal cards:** 80 are `personal:true`. Written ones sort first (7.8).
- **Inn examples:** `ms-04`, `ms-05`, `ms-06` are hypothetical (Example tag, `fill:true`) until Maxwell confirms them.
- **Approved 7-word exceptions:** `ms-06` and `bh-14` ("Is it a boy or a girl?").
- **Maxwell's voice, 17 clips, each skipped if missing:** 7 zone clips (`maxwell-<zone>.m4a`, first visit), 5 reward clips (`maxwell-reward-1..5.m4a`, random on rewards), 5 boss clips (`maxwell-boss-<zone>.m4a`).

## 17. Personal card slots

Four empty say-it cards wait for Maxwell (`fill:true`, `personal:true`, empty `en`, `th`, `respell`), skipped until written, then sorted first: `bh-30` the baby; `ms-28` the hotel; `ms-29` Maxwell, her husband; `ms-30` faith.

**Needs Maxwell list** (`needsMaxwell`, 7): `ms-04`, `ms-05`, `ms-06`, `bh-30`, `ms-28`, `ms-29`, `ms-30`. He fills them in `cards.json` or through the Backup view's list. The 16 verses are already filled and verified.

## 18. Thai Review Queue

Everything starts `NEEDS NANCY`: 201 of the 207 written cards, the 18 `thDef` hints, `gotItText`, `rewardText`, `wrongText`, `welcomeBack`, `restScreen`, the 7 zone `nameTh` (`nameThStatus`), all 97 `uiText` entries, the 4 map region names (`instructorChecked` marks Instructor's), the 5 boss names, the 7 encouragement lines, 25 trophy names, the 12 gear `thGloss` and `word` Thai, the 3 shirt names, the 6 Jesus-word `thGloss`, the 2 `jesusWordsFallback` lines, and any slot Maxwell fills. The 6 Thai dish names (`fd-01`–`fd-06`, `thStatus: "SIGNED OFF"`) are Maxwell's recorded exception (8:01 PM MT), `th` only; Nancy may still review them. Not in the queue: the 16 verses, the Jesus-word verse text, and `verses.attribution`, which are verified THSV11/ESV text (`status: "VERIFIED"`), never drafts. The Backup view lists the drafts; Nancy taps ✓ (confirm) or ✎ (Maxwell edits). Review the 10 `nursePhrase` cards first, then the `thDef` hints; gear and Jesus-word glosses go in Instructor's nightly batches after launch. The 3 sleepy and nap cards (`ph-25`, `ph-26`, `bh-31`) and the two-answer card `ms-31` are new drafts for Instructor's nightly batches after launch, not the first review. The tie card `ms-32` joins the same after-launch nightly batch; the Thai fixes from Instructor's 6:31 PM audit stay `NEEDS NANCY` too.

## 19. Build order: one paste, four stages

After each stage, `window.__test()` must print `PASS` before the next. Never rewrite an earlier stage unless its test fails.

1. **Core loop** (sword, 3 cards, question, reveal, Hint, XP bar, coins, review):
   - Question screens never show the English answer; `answer` and `trap` are among the choices.
   - The reveal is still there after 10 s; double-tapping Got it advances one card.
   - A hint earns +10; first tap shows `hint.letters`, the next an encouragement line; a miss keeps every coin; no dimming.
   - A run opens with one easy card; on a new visit, up to 2 cards missed on an earlier visit appear by card 3 (never more than 2 per visit); right and wrong feedback starts within 150 ms of the tap; personal cards first; unwritten cards skipped; at most 8 never-seen cards once the zone has 7 seen; say-it cards show Got it and no choices.
   - Hint taps alternate encouragement (3 s) and her given Jesus words (6 s or tap; shown, never spoken); a new player has all 6; after all are seen, `uiText.jesusAllHeard` once, then they start over; the HUD portrait cheers on right (aura rises, weapon lifts, then settles) and gives a small encouraging nod on wrong (head tilts up, about 600 ms; never a droop).
   - A kill on a reveal resumes there with XP unchanged. Ten coins play the glow pulse and add 1 to `pipFills`.
   - No red fills. Button labels sit on label plates: English Hero Yellow 20 px+ (`uiText.letsGo` 24 px+), Thai 17 px+; on iPhone SE nothing clips.
   - Card, boss, and Sound Duel screens use `data-theme="arena"`; menus use `data-theme="menu"` with no arena colors; enter and exit play the banner transition; the HUD sits in the top bar, flat, covering nothing.
   - Two-answer card `ms-31`: each showing picks one of its 2 `prompts` at random; right tap: Gold, +10 XP and one coin once, `uiText.done`; wrong tap: soft Moonstone X, no sound, coins and XP unchanged, then the right one glows Gold; only Done advances.
2. **Map, levels, rewards:**
   - Regions open in order, each by its end guardian only (rule 4), and never close; a zone's guardian follows scene 5 of each run there, 10 cards; no padlock, 'locked', 'fail' or 'can't' in any UI string.
   - One award crossing two levels grants both rewards once and queues two screens; a kill with 2 queued shows both, then none.
   - A boss twice gives its scroll and `bossesWon` once; a boss with 2 misses ends only when all 10 are right, then kneel, scroll, queue; no fail screen.
   - Every level cosmetic exists in `trophies`; a met goal unlocks once, in the award's transaction, with one reward screen; gear names are unique; equipping shows on the same frame on avatar and HUD; the 3 Bible weapons carry no verse text (a `ref` label at most); each shows `uiText.weaponGift`; no gear moves a Jesus word or verse.
   - Map > zone > `uiText.toMap`, five times across every open zone: every row, dot, path and emblem is present each time; at 320 × 568 pt no two tap targets overlap (bounding boxes 8 pt apart), each is 44 pt or more, and the Map never scrolls.
   - The main menu shows exactly two buttons (Map, Character), the corner hearth and the arrow cue. Restore: one tap never replaces her record; a corrupt, partial or empty backup changes nothing; `naeState.bak` holds the old save. At 320 × 568 pt nothing scrolls except the Character pane, gear rows (sideways) and Backup lists (scrollHeight ≤ clientHeight). No Settings, gear button or talent exists anywhere.
   - Character: its columns fill the width with equal gutters; not-yet trophies are full color with a gift icon; a double-tap equips once.
   - `uiText.toMap` on every screen but the sword screen, main menu, Map, Character, reward screens, and the daily verse; closing the app on the daily verse shows it again on relaunch; after a run's last card and the queue, the app is on the Map; every screen but the sword screen and main menu shows its title banner.
3. **Sound Duel:** no timer; word tiles, pictures only on the 6 `pics` pairs; the 6 word-ending pairs appear; misses never remove or dim a coin; round end shows +30, Got it, then next round or Map.
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
   - Grace check: no verse or scroll entry in `cards.json` or `state` has a `cost`, `price`, or currency field; no verse, scroll, or the Scrolls tab is gated on coins, XP spending, gems, or trophies; `gift:`/`giftGems` never depend on a verse; given verses reopen from Scrolls with every counter unchanged; every gift screen shows `uiText.verseGift`, never `rewardText`; the only spend flow is the Golden Pantry (cosmetics and level-opened weapons for Gold Stars; no verse, trophy, timer, offer or real money), and nothing on the Never list; Jesus words have no cost and all 6 are given at start; the two-answer card (`ms-31`, section 8.1) never removes a coin or XP on a wrong tap: a soft Moonstone X, no red, no sound, then the right one glows Gold and Done advances.
   - Privacy scan of every shipped file: no `tel` URLs, no phone numbers (`/(^|\D)(\+?1[\s.-]?)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}(?!\d)/`, and compact `/(tel:|\+1)\d{10}/`), no emails (`/[\w.+-]+@[\w-]+\.[\w.]+/`).

## 20. Maxwell's iPhone checks

- Mid-transition screenshots show no bleed-through. Contrast holds in daylight; yellow button text reads without squinting. Thai tone marks aren't clipped. Every emoji picture renders. The coins look like gold coins at arm's length. Airplane mode works. Audio plays on the second launch. With the ring/silent switch on, iOS mutes sounds and voice: flip it to hear them.

---

## CARD FILE

All card data is in the attached `nancys-adventure-english-v6-08-cards.json` (save it in the build as `cards.json`). Treat the card file as authoritative for all card content: text, Thai, respellings, answers, pictures, hints, zones, bosses, trophies, labels, verses, and slots. If this spec and the card file disagree on card content, the card file wins.
