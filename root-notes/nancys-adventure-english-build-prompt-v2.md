# BUILD PROMPT: Nancy's Adventure English (v2)

Build a complete, offline, full-screen iPhone web app called **Nancy's Adventure English**. It's a fast-paced, gentle RPG for learning English. For each card the player **hears** a short English phrase, **says it out loud**, then **taps the matching picture**. A right tap earns a star, and the game moves to the next card on its own.

**Player:** Nancy is a Thai-speaking adult at an intermediate-beginner level. She's pregnant (due around Dec 17, 2026) and wants to grow in the Christian faith. She may help at a hotel front desk.

**Tone:** quick and fun, but never punishing. No timers that fail her, and no harsh sounds.

---

## 1. Tech requirements

- Plain HTML, CSS and JS with no framework and no network calls after install. The files are `index.html`, `styles.css`, `app.js`, `cards.json`, `icons.svg` (an SVG sprite), `sw.js`, `manifest.json`, and fonts in `/fonts` (Fredoka for English, Kanit for Thai, both bundled).
- `manifest.json` sets `"display":"standalone"`, `"orientation":"portrait"`, `theme_color` `#5A2DD8`, `background_color` `#5A2DD8`, and 192 px and 512 px icons.
- `index.html` has `viewport-fit=cover`, `apple-mobile-web-app-capable=yes`, `apple-mobile-web-app-status-bar-style=black-translucent` and `apple-touch-icon`. Every screen is padded with `env(safe-area-inset-*)`.
- **Service worker:** cache-first, precaching every file, with a versioned cache name (`nae-v2`) that is bumped each release. It works fully offline in Airplane Mode.
- **Storage:** one versioned JSON object in `localStorage` (`nae_state`). The Me screen has **Backup** (download JSON) and **Restore** (load JSON).
- **Audio:** `speechSynthesis` with an en-US voice at rate 0.85 (0.6 in Slow Mode). iOS needs a tap before any audio plays, so every session opens with one big **▶ START** button that unlocks audio. Use short WebAudio tones for sound effects (no audio files needed).
- **No speech recognition and no microphone.** The "say it" step is honor-based (see section 4). This is deliberate. It's safer, causes no permission prompts and never marks her wrong.
- Use `touch-action: manipulation` and `overscroll-behavior: none`, turn off text selection, and make every tap target at least 64 px. **No swipe gestures anywhere.** Navigation is buttons only.

## 2. Visual style

**One color theme.** The background is candy purple `#5A2DD8`. The accents are gold `#FFC21A` for stars and gems, mint `#22C55E` for a right answer and coral `#FF5A5F` for a wrong one, plus dark outline `#1E1240` and white.

**Bold outside, white inside.** Every button, card and icon has a thick dark outline (5 to 6 px) with a white fill. Pressable buttons get a solid 6 px darker bottom edge and sink 4 px when pressed. Corners are rounded at 18 px, edges are straight and blocky, and there's no hand-drawn wobble.

**Icons are drawn vector SVG, never emoji.** Draw one consistent set: thick dark outline, white body, one or two flat accent colors. The exception is the Colors Cave, where the object's fill is its color. The full list is in section 10.

**Few layers.** Each screen has a thin top, one main area and a bottom bar. No modal on top of a modal.

**Bottom-heavy.** Everything she taps is in the lower half of the screen.

**Button labels are English only**, as icon plus short word, such as ▶ Play, 🛒 Shop and ◀ Back. Add a small Thai subtitle only where the meaning isn't obvious (Backup, Restore, Slow Mode, Emergency).

**Flip and transparency bug (must fix).** Any element that flips or turns over needs an opaque white background on **both** faces, with `backface-visibility:hidden` and `-webkit-backface-visibility:hidden`, and `transform-style:preserve-3d` on its parent. Nothing behind it may ever show through. The card screen in v2 uses slide and pulse transitions rather than flips.

## 3. Screens

### Map (home)

- A vertical candy-style path with a big blocky node for each level and boss.
- A **bouncing gold arrow** points at the next node to play. Finished nodes get a gold check, and locked nodes are greyed out with a lock icon.
- The streak (☀ with a day count) sits in a small chip at the top of the Map only.
- The bottom bar has a giant **▶ PLAY** button that starts the next node directly, flanked by 🛒 Shop and 👤 Me.
- A red-outlined **EMERGENCY** button is pinned on the Map in the bottom-left, always visible (see section 7).

### Card screen (gameplay)

From top to bottom:

1. **Star meter only** (thin top bar): 5 bold-outlined stars. Nothing else goes in the header.
2. **Phrase panel:** the English phrase large (Fredoka 30 to 36 px, up to 2 lines). Hard words are underlined in gold.
3. **Sound pill:** shown only when the card has a hard word. It's a separate gold pill under the phrase with a 🔊 icon and the respelling, such as `🔊 sword = SORD`, in a different font weight and color so it never looks like part of the sentence. Tapping the pill speaks just that word slowly.
4. **Step guide:** three small icons in a row, **👂 Listen, 👄 Say, 👆 Tap**. The current step glows and pulses.
5. **Choice grid:** a 2×2 grid of big icon buttons in the lower half of the screen. The order is shuffled on every card.
6. **Bottom bar:** ◀ Back (previous card, review only), 🔊 Replay, ⏸ Pause.

### Run end screen

- Each star earned this run **flies in one at a time** and lands in the meter, which **fills smoothly** with a chime per star.
- Cracked stones from this run show in a small pouch (section 5).
- When the meter reaches 5, the **five stars converge, smash together, and burst into one 💎 Gem** (screen shake plus a sparkle, about 1.2 s). Leftover stars carry over.
- Buttons: ▶ Next (big) and ⌂ Map.

### Shop and Me

- **Shop:** one list of big tiles with the gem count at the top of this screen only.
- **Me:** the blocky avatar wearing its armor, plus total stars, gems, streak, Backup, Restore, Slow Mode toggle, and Show Thai After Answer toggle (on by default).

## 4. Core loop (each card takes about 4 to 6 seconds)

1. The card slides in and **the phrase is spoken automatically**. 👂 glows.
2. When the audio ends, **👄 Say** glows and a ring pulses around it for 1.5 s (3 s in Slow Mode). Nancy says the phrase out loud. The very first time, show a one-line hint: "Say it out loud!" (พูดออกเสียงดังๆ).
3. **👆 Tap** glows and the choice buttons pulse once to show they're live. (They become tappable as soon as the audio ends, so speaking is encouraged but never forced.)
4. **Right tap:** the icon pulses mint, a ⭐ flies to the meter, a bright chime plays, and the Thai translation shows under the phrase for 1.0 s. Then it **advances automatically** with a pulse-and-slide transition.
5. **Wrong tap:** the tapped icon shakes, the correct icon pulses mint, a soft low tone plays, and a **cracked stone** drops into the pouch. The Thai shows for 2.5 s, the phrase plays once more, then it advances. The card is queued to come back 3 to 5 cards later.
6. **Pause** stops audio and the auto-advance timers.

**Tutorial (first launch only):** one demo card, "Pick up the sword.", with a pointing hand that walks through Listen, Say and Tap.

## 5. Currency: stars, stones and gems (good and evil paths, with grace)

- ⭐ **Gold Star:** a right tap on the first try.
- 🪨 **Cracked Stone:** a wrong tap. It never costs anything and never takes stars away.
- **Redemption:** when she later gets a card right that once gave her a stone, that stone **turns into a gold star** with a light-burst animation and the word **"Redeemed!"** (ไถ่คืนแล้ว!). The first time this happens, show one line: "God makes all things new." (พระเจ้าทรงสร้างทุกสิ่งขึ้นใหม่) Her mistakes aren't held against her. They get redeemed.
- 💎 **Gem:** 5 stars smash into 1 gem. Gems are the only shop currency.

## 6. Structure, review and difficulty

**Zones** on the map, top to bottom:

| Zone | Unlocked | Boss reward (always free, never bought) |
|---|---|---|
| Phonics Forest | Start | Belt of Truth plus the Creation scroll |
| Sight Words Mountain | Start | Shield of Faith plus the David and Goliath scroll |
| Colors Cave | After the Forest boss | Breastplate plus the Noah's Rainbow scroll |
| Numbers Valley | After the Mountain boss | Shoes of Peace plus the Five Loaves scroll |
| Baby and Hospital (bonus) | **Start** | Lamb badge plus the Jesus Is Born scroll |
| Maxwell Says (bonus) | Start | none |

- Each main zone has **Level 1 (cards 1 to 10)**, **Level 2 (cards 11 to 20)** and a **Boss** (10 random cards from the zone, 3 hearts, a quicker pace with auto-advance 30% faster). A wrong tap in a boss costs a heart. Losing has no penalty, and Retry is the big button.
- **Spaced repetition:** Leitner boxes 1 to 5 with gaps of the same session, 1 day, 3 days, 7 days and 21 days. A right answer on the first try moves a card up one box, and a wrong answer resets it to box 1.
- **Random order every time:** on entering a level, gather the due cards, shuffle them with Fisher-Yates, then top up with unseen cards until there are 10. Shuffle the choice positions on every card too.
- **Daily Review** node at the top of the map: 10 due cards from all zones.

**Distractors.** The three wrong choices come from the same zone's icons, never matching the answer.
- **Colors Cave:** at least one distractor is the **same object in a different color** (a red apple versus a green apple), so she has to listen for the color.
- **Numbers Valley:** at least one distractor is a **near-miss number** (13 and 30, 15 and 50, 7:00 and 11:00).
- **Phonics Forest:** where possible, one distractor is the **minimal-pair trap** (light and right, van and fan, three and tree, shoe and chew, bell and bear).

## 7. Emergency mode (separate from the game)

This mode is plain, with no game styling. It has a **white background, black text as large as fits (at least 44 px), English on top and Thai under it, and no icons.** One card fills the screen, and a bottom bar has huge ◀ and ▶ buttons and an ✕ Close button. The top says "Show this to the nurse" (ให้พยาบาลดู). It uses Baby and Hospital cards 1 to 9, in order, never shuffled.

## 8. Shop (spends gems)

| Item | Price | Effect |
|---|---|---|
| 🎁 **Free Gift** | **FREE** (in her inventory on first launch) | Opening it gives the **Helmet of Salvation** and the scroll "Salvation is a gift. You cannot earn it." (ความรอดเป็นของขวัญ คุณหามาเองไม่ได้) (Ephesians 2:8-9) |
| 💡 Hint ×3 | 1 💎 | Removes two wrong choices on a card |
| 🐢 Slow Mode | 2 💎, permanent | Slower speech and longer Say and auto-advance windows |
| ❤ Extra Heart | 1 💎 | +1 heart in the next boss |
| Sword skins: Gold, Crystal, Fire | 3 💎 each | Changes the color of her avatar's sword |
| Avatar colors (5 options) | 2 💎 each | Changes the tunic color |

**Armor of God (Ephesians 6:10-18):** her avatar starts with the **Sword of the Spirit** ("The sword is God's Word." ดาบคือพระวจนะของพระเจ้า). Every armor piece is a **gift from beating a boss and is never sold.** Salvation and righteousness can't be bought, so the game shouldn't sell them either. Only fun cosmetics and utilities cost gems.

## 9. Faith content rules

- About **1 card in 10** is faith-themed and still a natural, useful phrase. These are marked *(faith)* below.
- Each boss reward scroll is a three-line Bible story in English with Thai under each line, plus 🔊.
- There's never a quiz question about belief, and no faith card is ever a trick distractor.

**Scrolls:**

| Scroll | English | Thai |
|---|---|---|
| Creation | In the beginning, God made the world. He made the trees and the light. He said, "It is good." | ในปฐมกาล พระเจ้าทรงสร้างโลก พระองค์ทรงสร้างต้นไม้และแสงสว่าง พระองค์ตรัสว่า "ดี" |
| David and Goliath | David was small. Goliath was big. David did not trust his own strength. He trusted God, and God won. | ดาวิดตัวเล็ก โกลิอัทตัวใหญ่ ดาวิดไม่ได้พึ่งกำลังของตัวเอง เขาวางใจพระเจ้า และพระเจ้าทรงให้ชัยชนะ |
| Noah's Rainbow | God put a rainbow in the sky. It is His promise. God always keeps His promises. | พระเจ้าทรงวางรุ้งไว้บนท้องฟ้า นั่นคือพระสัญญาของพระองค์ พระเจ้าทรงรักษาสัญญาเสมอ |
| Five Loaves | A boy had five loaves and two fish. Jesus fed five thousand people. God gives more than enough. | เด็กชายคนหนึ่งมีขนมปังห้าก้อนกับปลาสองตัว พระเยซูทรงเลี้ยงคนห้าพันคน พระเจ้าประทานให้อย่างเหลือเฟือ |
| Jesus Is Born | Mary had a baby boy in Bethlehem. His name is Jesus. He is God's gift to the world. | มารีย์คลอดบุตรชายที่เมืองเบธเลเฮม พระองค์ทรงพระนามว่าเยซู พระองค์คือของขวัญจากพระเจ้าสำหรับโลก |
| Armor captions | Belt of Truth: "God's Word is true." / Shield of Faith: "Trust God, not yourself." / Breastplate: "Jesus makes us clean." / Shoes of Peace: "God gives peace." / Lamb: "Jesus is the Lamb of God." | พระวจนะของพระเจ้าเป็นความจริง / จงวางใจพระเจ้า ไม่ใช่ตัวเอง / พระเยซูทรงชำระเราให้สะอาด / พระเจ้าประทานสันติสุข / พระเยซูคือลูกแกะของพระเจ้า |

## 10. Card data (`cards.json`)

Schema:

```json
{"id":"pf-01","zone":"forest","level":1,"en":"Pick up the sword.","th":"หยิบดาบขึ้นมา","hard":[{"word":"sword","respell":"SORD","trap":"SILENT"}],"icon":"sword","faith":false}
```

`trap` codes and the tip shown in Thai on a wrong tap and in the sound pill:

| Code | Tip (Thai) |
|---|---|
| R | ม้วนลิ้นขึ้น ไม่แตะเพดาน |
| L | ปลายลิ้นแตะหลังฟันบน |
| TH | แลบลิ้นออกมาเล็กน้อยระหว่างฟัน แล้วเป่าลม |
| V | ฟันบนแตะริมฝีปากล่าง |
| W | ห่อปาก ไม่ใช้ฟัน |
| SH | เป่าลมยาว ไม่หยุด |
| CH | หยุดแล้วปล่อยลมสั้นๆ |
| END | ออกเสียงท้ายคำให้ชัด อย่ากลืนเสียง |
| BLEND | อย่าใส่เสียงสระแทรกระหว่างพยัญชนะ |
| SILENT | ตัวอักษรนี้ไม่ออกเสียง |
| TEEN | -TEEN เน้นท้าย / -TY เน้นหน้า |

Thai lines use ค่ะ or คะ where Nancy is the speaker. Respellings use simple letters with the stressed syllable in CAPS and appear **only for hard words.**

### Phonics Forest

| # | English | Hard word = respelling (trap) | Thai | Icon |
|---|---|---|---|---|
| 1 | Pick up the sword. | sword = SORD (SILENT) | หยิบดาบขึ้นมา | sword |
| 2 | Open the red door. | red = RED (R) | เปิดประตูสีแดง | red-door |
| 3 | Turn on the light. | light = LYT (L) | เปิดไฟ | lightbulb |
| 4 | Ring the bell. | ring = RING (R); bell = BEL (L, END) | สั่นกระดิ่ง | bell |
| 5 | Lock the room. | lock = LOK (L); room = ROOM (R) | ล็อกห้อง | padlock |
| 6 | Look at the rain. | rain = RAYN (R) | ดูฝนสิ | rain-cloud |
| 7 | Take the glass of water. | glass = GLASS (END) | หยิบแก้วน้ำ | glass-water |
| 8 | Hold up five fingers. | five = FYV (V, END) | ชูห้านิ้ว | hand-five |
| 9 | Drive the van. | van = VAN (V) | ขับรถตู้ | van |
| 10 | Wash the window. | wash = WOSH (W, SH); window = WIN-doh (W) | ล้างหน้าต่าง | window |
| 11 | Drink the warm milk. | milk = MILK (L, END) | ดื่มนมอุ่น | milk-cup |
| 12 | Find three keys. | three = THREE (TH) | หาลูกกุญแจสามดอก | three-keys |
| 13 | Take the thick book. | thick = THIK (TH) | หยิบหนังสือเล่มหนา | thick-book |
| 14 | Sit on the chair. | chair = CHAIR (CH) | นั่งบนเก้าอี้ | chair |
| 15 | Put on your shoes. | shoes = SHOOZ (SH, END) | ใส่รองเท้า | shoes |
| 16 | Read the Bible. | Bible = BY-bul (END) | อ่านพระคัมภีร์ | bible *(faith)* |
| 17 | Climb the tree. | climb = KLYM (BLEND, SILENT) | ปีนต้นไม้ | tree |
| 18 | Follow the street. | street = STREET (BLEND) | เดินตามถนน | road |
| 19 | Hold the shield. | shield = SHEELD (SH, END) | ถือโล่ | shield |
| 20 | Wear the belt of truth. | truth = TROOTH (BLEND, TH) | คาดเข็มขัดแห่งความจริง | belt *(faith)* |

Minimal-pair distractor icons to draw for this zone: `right-arrow` (light/right), `fan` (van/fan), `tree` (three/tree), `chew-gum` (shoe/chew), `bear` (bell/bear), `grass` (glass/grass), `rock` (lock/rock), `lane` (rain/lane).

### Sight Words Mountain (possessives and front desk)

| # | English | Hard word = respelling (trap) | Thai | Icon |
|---|---|---|---|---|
| 1 | This is my key. | | นี่คือกุญแจของฉัน | key |
| 2 | That is his hat. | his = HIZ (END) | นั่นคือหมวกของเขา | man-hat |
| 3 | This is her bag. | | นี่คือกระเป๋าของเธอ | purse |
| 4 | The phone is mine. | | โทรศัพท์เป็นของฉัน | phone |
| 5 | Is this coat yours? | yours = YORZ (END) | เสื้อโค้ทตัวนี้ของคุณใช่ไหมคะ | coat |
| 6 | Here is your room key. | room = ROOM (R) | นี่คีย์การ์ดห้องของคุณค่ะ | key-card |
| 7 | Please sign here. | sign = SYN (SILENT) | กรุณาเซ็นชื่อตรงนี้ค่ะ | pen |
| 8 | Ring the bell for help. | | กดกริ่งถ้าต้องการความช่วยเหลือค่ะ | desk-bell |
| 9 | Please wait here. | wait = WAYT (W) | กรุณารอที่นี่ค่ะ | hourglass |
| 10 | Can I help you? | | มีอะไรให้ช่วยไหมคะ | helping-hand |
| 11 | Where is the bathroom? | bathroom = BATH-room (TH) | ห้องน้ำอยู่ที่ไหนคะ | toilet-sign |
| 12 | Say it again, please. | | พูดอีกครั้งได้ไหมคะ | ear-repeat |
| 13 | Please speak slowly. | slowly = SLOH-lee (BLEND) | กรุณาพูดช้าๆ ค่ะ | turtle |
| 14 | Write your name. | write = RYT (SILENT, R) | เขียนชื่อของคุณค่ะ | paper-pencil |
| 15 | Our car is outside. | | รถของเราอยู่ข้างนอก | car |
| 16 | Their dog is big. | their = THAIR (TH) | หมาของพวกเขาตัวใหญ่ | dog |
| 17 | Your coffee is ready. | ready = RED-ee (R) | กาแฟของคุณพร้อมแล้วค่ะ | coffee |
| 18 | Have a good night. | | ราตรีสวัสดิ์ค่ะ | moon |
| 19 | This gift is yours. | | ของขวัญนี้เป็นของคุณ | gift-box *(faith: grace)* |
| 20 | Hold up the shield of faith. | faith = FAYTH (TH) | ชูโล่แห่งความเชื่อ | shield-cross *(faith)* |

### Colors Cave

The background stays the theme purple. The object icons are filled with their color.

| # | English | Hard word = respelling (trap) | Thai | Icon |
|---|---|---|---|---|
| 1 | Tap the red apple. | red = RED (R) | แตะแอปเปิลสีแดง | apple-red |
| 2 | Find the blue cup. | blue = BLOO (BLEND) | หาถ้วยสีน้ำเงิน | cup-blue |
| 3 | Pick up the yellow key. | yellow = YEL-oh (L) | หยิบกุญแจสีเหลือง | key-yellow |
| 4 | Take the green leaf. | green = GREEN (BLEND) | หยิบใบไม้สีเขียว | leaf-green |
| 5 | Touch the white towel. | white = WYT (W) | แตะผ้าเช็ดตัวสีขาว | towel-white |
| 6 | Open the black box. | black = BLAK (BLEND) | เปิดกล่องสีดำ | box-black |
| 7 | Find the pink flower. | flower = FLOW-er (BLEND) | หาดอกไม้สีชมพู | flower-pink |
| 8 | Take the orange carrot. | | หยิบแครอทสีส้ม | carrot-orange |
| 9 | Pick up the purple grapes. | purple = PUR-pul (R, L) | หยิบองุ่นสีม่วง | grapes-purple |
| 10 | Find the brown bear. | brown = BROWN (BLEND) | หาหมีสีน้ำตาล | bear-brown |
| 11 | Tap the big circle. | circle = SUR-kul (L) | แตะวงกลมใหญ่ | circle-big |
| 12 | Tap the small square. | square = SKWAIR (BLEND) | แตะสี่เหลี่ยมเล็ก | square-small |
| 13 | Find the triangle. | triangle = TRY-ang-gul (BLEND) | หาสามเหลี่ยม | triangle |
| 14 | Pick up the long pencil. | long = LAWNG (L) | หยิบดินสอแท่งยาว | pencil-long |
| 15 | Tap the gold star. | | แตะดาวสีทอง | star-gold |
| 16 | Find the gray rock. | gray = GRAY (BLEND); rock = ROK (R) | หาก้อนหินสีเทา | rock-gray |
| 17 | Find the light blue shirt. | light = LYT (L) | หาเสื้อสีฟ้าอ่อน | shirt-lightblue |
| 18 | Find the round table. | round = ROWND (R, END) | หาโต๊ะกลม | table-round |
| 19 | Put on God's armor. | armor = AR-mer (R) | สวมเกราะของพระเจ้า | armor *(faith)* |
| 20 | Look at the rainbow. | rainbow = RAYN-boh (R) | ดูรุ้งสิ | rainbow *(faith link: Noah scroll)* |

Also draw the color-swap distractors: apple-green, cup-red, key-blue, leaf-yellow, towel-black, box-white, flower-purple, carrot-green, grapes-green, bear-black, circle-small, square-big, pencil-short, star-silver, rock-brown, shirt-darkblue, table-square.

### Numbers Valley

Items marked **[INN]** are placeholders. Maxwell has to fill them in with Elk Refuge Inn's real numbers before the build. (I didn't make up the inn's rates or hours.)

| # | English | Hard word = respelling (trap) | Thai | Icon |
|---|---|---|---|---|
| 1 | Find room two-oh-four. | | หาห้อง 204 | door-204 |
| 2 | Take two pillows. | pillows = PIL-ohz (L, END) | หยิบหมอนสองใบ | pillows-2 |
| 3 | Find three towels. | three = THREE (TH) | หาผ้าเช็ดตัวสามผืน | towels-3 |
| 4 | Pick up five dollars. | five = FYV (V) | หยิบเงินห้าดอลลาร์ | bill-5 |
| 5 | Set the clock to seven. | seven = SEV-un (V) | ตั้งนาฬิกาเจ็ดโมง | clock-7 |
| 6 | Check-out is at **[INN: eleven]**. | eleven = ih-LEV-un (V) | เช็คเอาท์ **[INN]** โมงค่ะ | clock-11 |
| 7 | Breakfast is at **[INN: seven thirty]**. | breakfast = BREK-fust (BLEND) | อาหารเช้า **[INN]** ค่ะ | clock-730 |
| 8 | Find thirteen. | thirteen = thur-TEEN (TH, TEEN) | หาเลขสิบสาม | num-13 |
| 9 | Find thirty. | thirty = THUR-tee (TH, TEEN) | หาเลขสามสิบ | num-30 |
| 10 | Find fifty. | fifty = FIF-tee (TEEN) | หาเลขห้าสิบ | num-50 |
| 11 | One night is **[INN: rate]** dollars. | | คืนละ **[INN]** ดอลลาร์ค่ะ | price-tag |
| 12 | Two adults and one child. | adults = uh-DULTS (END) | ผู้ใหญ่สองคน เด็กหนึ่งคน | family-2-1 |
| 13 | Take one key card. | | หยิบคีย์การ์ดหนึ่งใบ | keycard-1 |
| 14 | Go to the first floor. | first = FURST (R, END); floor = FLOR (BLEND) | ไปชั้นหนึ่ง | floor-1 |
| 15 | Find twenty dollars. | twenty = TWEN-tee (BLEND) | หาเงินยี่สิบดอลลาร์ | bill-20 |
| 16 | Count seven days. | | นับเจ็ดวัน | calendar-week |
| 17 | Find December seventeenth. | seventeenth = sev-un-TEENTH (V, TH) | หาวันที่สิบเจ็ดธันวาคม | calendar-dec17 |
| 18 | Take two fish. | fish = FISH (SH) | หยิบปลาสองตัว | fish-2 |
| 19 | Take five loaves of bread. | loaves = LOHVZ (L, V, END) | หยิบขนมปังห้าก้อน | bread-5 |
| 20 | Jesus fed five thousand people. | thousand = THOW-zund (TH) | พระเยซูทรงเลี้ยงคนห้าพันคน | crowd *(faith)* |

Near-miss distractors to draw: num-15, num-14, num-40, clock-1, clock-10, bill-50, bill-2, door-240, pillows-3, towels-2, fish-5, bread-2, calendar-dec7.

### Baby and Hospital (bonus, open from the start; cards 1 to 9 also feed Emergency mode)

| # | English | Hard word = respelling (trap) | Thai | Icon |
|---|---|---|---|---|
| 1 | I need a Thai interpreter. | interpreter = in-TUR-pruh-ter (R) | ฉันต้องการล่ามภาษาไทยค่ะ | interpreter |
| 2 | I am in pain. | | ฉันเจ็บค่ะ | pain |
| 3 | My water broke. | broke = BROHK (BLEND) | น้ำคร่ำแตกแล้วค่ะ | water-drop |
| 4 | Please call my husband. | husband = HUZ-bund | กรุณาโทรหาสามีของฉันค่ะ | phone-heart |
| 5 | I am bleeding. | bleeding = BLEED-ing (BLEND) | ฉันมีเลือดออกค่ะ | blood-drop |
| 6 | The baby is not moving. | moving = MOO-ving (V) | ลูกไม่ดิ้นค่ะ | belly-still |
| 7 | I feel sick. | | ฉันรู้สึกไม่สบายค่ะ | sick-face |
| 8 | Please call the nurse. | nurse = NURS (R, END) | กรุณาเรียกพยาบาลค่ะ | nurse |
| 9 | Can I have some water? | water = WAW-ter (W) | ขอน้ำหน่อยได้ไหมคะ | glass-water |
| 10 | I need to push. | push = PUSH (SH) | ฉันต้องเบ่งค่ะ | push-arrows |
| 11 | Hold the baby. | | อุ้มลูก | baby-arms |
| 12 | Feed the baby. | | ให้นมลูก | baby-bottle |
| 13 | Change the diaper. | diaper = DY-per (CH, R) | เปลี่ยนผ้าอ้อม | diaper |
| 14 | Wrap the baby in a blanket. | wrap = RAP (SILENT); blanket = BLANG-kit (BLEND) | ห่อลูกด้วยผ้าห่ม | blanket |
| 15 | The baby is sleeping. | sleeping = SLEEP-ing (BLEND) | ลูกกำลังนอนหลับ | baby-sleep |
| 16 | Put the baby in the car seat. | | วางลูกในคาร์ซีท | car-seat |
| 17 | Where is my medicine? | medicine = MED-ih-sin | ยาของฉันอยู่ไหนคะ | pill |
| 18 | Is it a boy or a girl? | girl = GURL (R, L) | ผู้ชายหรือผู้หญิงคะ | boy-girl |
| 19 | We can go home now. | | เรากลับบ้านได้แล้ว | house |
| 20 | Thank you, God, for my baby. | thank = THANK (TH) | ขอบคุณพระเจ้าสำหรับลูกของฉันค่ะ | baby-light *(faith)* |

### Maxwell Says (bonus)

This starts empty. A **2-second long-press on the zone title** opens an "Add card" form with fields for English, Thai, an optional hard word with respelling, and an icon picked from the existing icon set. Cards are saved locally and included in Backup. They use the same loop and Leitner boxes, with no boss and no stars, so it stays low pressure.

**Icons for the UI itself:** play, back, replay, pause, shop, me, map, lock, check, arrow-pointer, star, star-outline, stone-cracked, gem, heart, gift, helmet, sword (plus 3 skins), belt, shield-cross, breastplate, shoes, lamb, scroll, sun, ear, mouth, finger.

## 11. Acceptance tests

1. Install from Safari with Add to Home Screen, turn on Airplane Mode, force-quit and reopen. Everything works.
2. Nothing sits under the notch or home bar. All tap targets are at least 64 px and in the lower half of the screen.
3. After ▶ START, every card speaks automatically, and the Listen, Say and Tap steps glow in order.
4. A right tap sends a star flying to the meter and auto-advances. A wrong tap shows the right answer, drops a stone, and the card comes back 3 to 5 cards later.
5. Getting a card right that once gave a stone shows "Redeemed!" and turns the stone into a star.
6. Five stars smash into exactly one gem, and leftover stars carry over.
7. Card order and choice positions are different on every visit.
8. No emoji appear anywhere. Every icon is from the SVG sprite with a bold outline and a white inside.
9. Nothing is see-through during any transition.
10. Emergency mode is plain white with huge text and has no game styling. It works from the Map in one tap.
11. The Free Gift is in her inventory on first launch. Armor pieces only come from bosses and are never sold.
12. Backup and Restore round-trip all progress.
13. **Before release:** every [INN] value is filled in, and Nancy reads every Thai line.
