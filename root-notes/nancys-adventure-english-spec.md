# Nancy's Adventure English: Build Spec (paste into Grok Build)

A sequel to Nancy's English flashcard app. It's a gentle RPG where flashcard decks are zones, stars become upgrade tokens, and every card is a short, useful sentence.

**Learner:** Nancy is a Thai-speaking adult at an intermediate-beginner level. She uses an iPhone, is about 7 months pregnant (due around Dec 17, 2026), and wants to become a Christian. She may help at a hotel front desk.

**Tone:** warm, never punishing, no timers, no red X marks. Faith content is woven in gently, never preachy.

---

## 1. Tech (build it this way)

Use plain HTML, CSS and JS with no framework, as five files:

`index.html`

`app.js`

`cards.json`

`sw.js`

`manifest.json`

Bundle the fonts too: **Fredoka** (English) and **Kanit** (Thai), both stored locally.

`manifest.json` settings:

`"display": "standalone"`

`"orientation": "portrait"`

`theme_color` and `background_color` set to the theme purple

192 px and 512 px icons

`index.html` needs these meta tags:

`<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">`

`apple-mobile-web-app-capable=yes`

`apple-mobile-web-app-status-bar-style=black-translucent`

`apple-touch-icon`

Pad for the notch and home bar with `env(safe-area-inset-top/bottom/left/right)` on the header and the bottom bar.

**Service worker:** cache-first. Precache every file on install, and use a versioned cache name (`ae-v1`) that gets bumped on each release. After the first load it works fully offline.

**Storage:** keep all progress in `localStorage` under one key, `ae_state`, as versioned JSON. Add **Backup** and **Restore** buttons in the Me screen that export and import the JSON file, so progress is never lost. Tell Nancy to install it from Safari's Share menu with "Add to Home Screen." Installed web apps aren't subject to Safari's 7-day storage purge.

**Speech:** use `speechSynthesis` with an en-US voice at rate 0.85. It speaks the English sentence when the card is flipped, and a 🔊 button replays it. On iOS, speech has to start inside a tap, and flip is a tap. There's no voice recognition.

**Touch:** `touch-action: manipulation`, `overscroll-behavior: none`, no text selection, and every tap target at least 56 px.

## 2. Look and feel (Candy Crush, simplified)

Use **one color theme**: deep candy purple `#5A2DD8` for the background, with gold `#FFC21A` for stars and tokens, mint `#22C55E` for Got It, coral `#FF5A5F` for Again, and white for cards.

**Glossy and blocky:** use straight edges with rounded corners (20 px), flat vector shapes, and a gloss highlight on the top 40% of each button. Give buttons a solid 5 px bottom border in a darker shade so they look pressable, and have them shift down 3 px when tapped. No hand-drawn wobble and no realistic art.

**Fewer layers:** each screen has a header, one main area and a bottom bar. No modals stacked on modals.

**Bottom-heavy for thumbs:** everything she taps is in the bottom 45% of the screen, and the top is display only.

**Header (thin):** ☀️ streak, ⭐ stars toward the next token (shown as 5 bold-outlined star icons), 🪙 tokens.

**Bottom bar:** Map, Shop and Me as three big icon buttons with labels in Thai and English.

## 3. World map (zones)

The map is a vertical candy-style path. Each zone is a big glossy node, and finished levels get a gold checkmark.

| Order | Zone | Unlocked | Why it's here |
|---|---|---|---|
| 1 | 🌳 Phonics Forest | Start | Sounds Thai speakers find hardest, practiced inside real sentences |
| 2 | ⛰️ Sight Words Mountain | Start | Possessives, questions and front-desk survival phrases |
| 3 | 💎 Colors and Shapes Cave | After the Forest boss | Describing things (color goes before the noun) |
| 4 | 🔢 Numbers Valley | After the Mountain boss | Prices, times, rooms, dates |
| ★ | 👶 Baby and Hospital | **Start (bonus)** | Urgent before the birth, so never lock it |
| ★ | 💬 Maxwell Says | Start (bonus) | Phrases Maxwell adds himself |

Each main zone has **Level 1 (10 cards), Level 2 (10 cards) and a Boss**. The Boss is 10 random cards from the zone with 3 hearts, and an "Again" costs one heart. Losing the boss costs nothing and she can just try again. Beating it unlocks the zone's Bible story scroll (section 8) and its cosmetic item in the shop.

## 4. Card behavior

**Front:**
- The English sentence, large and bold (Fredoka, 28 to 34 px, fitted to two lines).
- The respelling under it, with the stressed syllable in CAPS.
- The **trap sound** underlined in the sentence with a small tag such as "R" or "TH" (Phonics Forest and anywhere else it fits).

**Tap to flip** (3D flip of about 350 ms, then speech):
- The Thai sentence, large (Kanit).
- **Key words:** 2 or 3 English words with their Thai, such as "ready = พร้อม".
- A one-line **sound tip in Thai** when the card has a trap tag.
- Two big buttons at the bottom: **🔁 อีกครั้ง Again** (coral) and **✅ จำได้ Got It** (mint).
- 🔊 to replay.

**Swipes:** swipe up goes to the next card and swipe down goes to the previous one. Arrow buttons sit by the thumb as a backup.

## 5. Spaced repetition and order

Use **Leitner boxes 1 to 5**, with review gaps of the same session, 1 day, 3 days, 7 days and 21 days.

Got It moves a card up one box. Again sends it back to box 1 and repeats it 3 to 5 cards later in the same run.

**Every time she enters a level:** take the cards that are due, shuffle them with Fisher-Yates, then top up with new cards (in the authored order) until there are 10. The order is random on every visit.

A **Daily Review** button on the map gathers up to 10 due cards from all zones.

## 6. Stars, tokens and shop

**Stars per run:** 1 for finishing, +1 if she gets 7 or more right on the first try, +1 if she gets all 10. Beating a boss gives +2.

**Star meter:** 5 bold-outlined stars in the header. When the fifth fills, the stars **converge, smash together and become a 🪙 upgrade token** (with a glossy burst, screen shake and a chime, about 1.2 s). Extra stars carry over.

**Shop** (one scrolling list of big tiles, price on the button):

| Item | Type | Price | Effect |
|---|---|---|---|
| 🎁 Free Gift | Special | **Free** | Already in her inventory on first launch. Opening it shows the Grace scroll (section 8). |
| 💡 Hint ×3 | Utility | 1 🪙 | Shows the key words on the front before flipping |
| 🐢 Slow Mode | Utility, permanent | 2 🪙 | Speech at rate 0.6 and a slower flip |
| ❤️ Extra Life | Utility | 1 🪙 | +1 heart in the next boss |
| 👑 Phonics Crown | Cosmetic | 3 🪙 | Avatar item (after the Forest boss) |
| 🦸 Colors Cape | Cosmetic | 3 🪙 | After the Cave boss |
| 🥾 Mountain Boots | Cosmetic | 3 🪙 | After the Mountain boss |
| ⌚ Numbers Watch | Cosmetic | 3 🪙 | After the Valley boss |
| 🧸 Baby Bear Badge | Cosmetic | 3 🪙 | After the Baby and Hospital boss |

**Avatar:** a simple blocky character on the Me screen wearing the cosmetics she owns. It also shows small in the header.

**The Free Gift is a lesson built into the game.** Everything else in the shop is earned, but this is the one thing she never paid for. That's a picture of grace (Ephesians 2:8-9) she experiences rather than just reads.

## 7. Teaching design (from her teacher)

**Content order:** survival first (help, understanding, possessives), then work phrases (front desk), then description and numbers. Every card is a complete, useful sentence of 3 to 8 words, and each level gets slightly longer.

**Thai sound traps** (tag cards and show these tips on the back):

| Tag | Trap | Tip shown on the back (Thai) |
|---|---|---|
| R/L | Swaps r and l, or turns both into l | R: ม้วนลิ้นขึ้น ไม่แตะเพดาน / L: ปลายลิ้นแตะหลังฟันบน |
| TH | Says "th" as t or d | แลบลิ้นออกมาเล็กน้อยระหว่างฟัน แล้วเป่าลม |
| V/W | Says v as w | V: ฟันบนแตะริมฝีปากล่าง / W: ห่อปาก ไม่ใช้ฟัน |
| SH/CH | Mixes up the two | SH: เป่าลมยาว "ชฺ" / CH: หยุดแล้วปล่อย "ฉ" สั้นๆ |
| END | Drops or softens the final consonant (s, l, v, z, ks) | ออกเสียงท้ายคำให้ชัด อย่ากลืนเสียง |
| BLEND | Puts a vowel inside a cluster ("sa-treet") | อย่าใส่เสียงสระแทรกระหว่างพยัญชนะ |
| STRESS | Gives every syllable equal weight | เน้นพยางค์ตัวใหญ่ให้ดังและยาวขึ้น |
| -TEEN/-TY | 13 vs 30 | thir-TEEN เน้นท้าย / THIR-ty เน้นหน้า |

**Grammar habits from Thai to watch for**, shown as gentle tips on the matching cards:
- English adds -s for plurals and for he or she ("she likes").
- English needs "is," "am" or "are" ("I am tired," not "I tired").
- The color comes before the noun.

**How much faith content:** about 1 card in 10 in each zone is gently faith-themed and still a useful everyday sentence. Each zone's boss reward is a short Bible story scroll, and the Free Gift opens the Grace scroll. No faith card is ever a quiz question on belief.

**Politeness:** Thai sentences use ค่ะ or คะ, since Nancy is the speaker.

**Respellings:** the Phonics Forest has them written out below. For other zones, generate them with the same scheme (simple English letters, stressed syllable in CAPS, hyphens between syllables) and have Nancy or Maxwell spot-check them.

**Before release:** a native Thai speaker (Nancy herself is ideal) skims every Thai line.

## 8. Bible story scrolls (boss rewards)

Each one opens as a glossy scroll with three short English lines, Thai under each, and 🔊 to hear it.

| Zone | Story | English | Thai |
|---|---|---|---|
| Forest | Creation | In the beginning, God made the world. He made the trees and the light. He said, "It is good." | ในปฐมกาล พระเจ้าทรงสร้างโลก พระองค์ทรงสร้างต้นไม้และแสงสว่าง พระองค์ตรัสว่า "ดี" |
| Mountain | David and Goliath | David was small. Goliath was big. David did not trust his own strength. He trusted God, and God won. | ดาวิดตัวเล็ก โกลิอัทตัวใหญ่ ดาวิดไม่ได้พึ่งกำลังของตัวเอง เขาวางใจพระเจ้า และพระเจ้าทรงให้ชัยชนะ |
| Cave | Noah's rainbow | God put a rainbow in the sky. It is His promise. God always keeps His promises. | พระเจ้าทรงวางรุ้งไว้บนท้องฟ้า นั่นคือพระสัญญาของพระองค์ พระเจ้าทรงรักษาสัญญาเสมอ |
| Valley | Five loaves, two fish | A boy had five loaves and two fish. Jesus fed five thousand people. God gives more than enough. | เด็กชายคนหนึ่งมีขนมปังห้าก้อนกับปลาสองตัว พระเยซูทรงเลี้ยงคนห้าพันคน พระเจ้าประทานให้อย่างเหลือเฟือ |
| Baby | Jesus is born | Mary had a baby boy in Bethlehem. His name is Jesus. He is God's gift to the world. | มารีย์คลอดบุตรชายที่เมืองเบธเลเฮม พระองค์ทรงพระนามว่าเยซู พระองค์คือของขวัญจากพระเจ้าสำหรับโลก |
| Free Gift | Grace | You did not earn this. It is a gift. God's love is free for you. | คุณไม่ได้หามาเอง นี่คือของขวัญ ความรักของพระเจ้าให้คุณฟรี |

## 9. Card data

Schema for each entry in `cards.json`:

```json
{ "id": "pf-01", "zone": "phonics", "level": 1, "en": "The room is ready.", "respell": "thuh ROOM iz RED-ee", "th": "ห้องพร้อมแล้วค่ะ", "keys": [{"en":"room","th":"ห้อง"},{"en":"ready","th":"พร้อม"}], "trap": ["R"], "tip_th": "ม้วนลิ้นขึ้น ไม่แตะเพดาน", "faith": false }
```

Fill in `keys` with 2 or 3 of the most useful words in each sentence, and `tip_th` from the trap table.

### 🌳 Phonics Forest

| # | English | Respelling | Thai | Trap |
|---|---|---|---|---|
| **Level 1** |||||
| 1 | The room is ready. | thuh ROOM iz RED-ee | ห้องพร้อมแล้วค่ะ | R |
| 2 | Please lock the door. | pleez LOK thuh DOR | กรุณาล็อกประตูค่ะ | L, END |
| 3 | It is raining a lot. | it iz RAYN-ing uh LOT | ฝนตกหนักมาก | R/L |
| 4 | Your room is on the left. | yor ROOM iz on thuh LEFT | ห้องของคุณอยู่ทางซ้ายค่ะ | R/L, END |
| 5 | The light is red. | thuh LYT iz RED | ไฟสีแดง | R/L |
| 6 | Here is your bill. | HEER iz yor BIL | นี่คือบิลของคุณค่ะ | END |
| 7 | I need more rice. | eye NEED mor RYSS | ฉันอยากได้ข้าวเพิ่มค่ะ | R, END |
| 8 | Five towels, please. | FYV TOW-ulz, PLEEZ | ขอผ้าเช็ดตัวห้าผืนค่ะ | END |
| 9 | The bus is late. | thuh BUS iz LAYT | รถบัสมาสาย | END |
| 10 | Call me later. | KAWL mee LAY-ter | โทรหาฉันทีหลังนะคะ | L |
| **Level 2** |||||
| 11 | Thank you very much. | THANK yoo VEH-ree MUCH | ขอบคุณมากค่ะ | TH, V/W |
| 12 | I think so. | eye THINK soh | ฉันคิดว่าใช่ค่ะ | TH |
| 13 | This is the third floor. | THIS iz thuh THURD FLOR | นี่คือชั้นสามค่ะ | TH, BLEND |
| 14 | We have free Wi-Fi. | wee hav FREE WY-fy | เรามีไวไฟฟรีค่ะ | V/W |
| 15 | The van is waiting. | thuh VAN iz WAYT-ing | รถตู้รออยู่ค่ะ | V/W |
| 16 | Please wash your hands. | pleez WOSH yor HANDZ | กรุณาล้างมือค่ะ | SH/CH, END |
| 17 | Please sit in this chair. | pleez SIT in this CHAIR | เชิญนั่งเก้าอี้ตัวนี้ค่ะ | SH/CH |
| 18 | Breakfast starts at seven. | BREK-fust STARTS at SEV-un | อาหารเช้าเริ่มเจ็ดโมงค่ะ | BLEND, V/W |
| 19 | The street is very quiet. | thuh STREET iz VEH-ree KWY-ut | ถนนเงียบมาก | BLEND, V/W |
| 20 | God's love is free. | GODZ LUV iz FREE | ความรักของพระเจ้าให้ฟรี ไม่ต้องจ่าย | END, V/W *(faith)* |

### ⛰️ Sight Words Mountain

| # | English | Thai |
|---|---|---|
| **Level 1** |||
| 1 | Is this your key? | นี่กุญแจของคุณใช่ไหมคะ |
| 2 | No, it is not mine. | ไม่ใช่ค่ะ ไม่ใช่ของฉัน |
| 3 | That bag is his. | กระเป๋าใบนั้นเป็นของเขา |
| 4 | This phone is hers. | โทรศัพท์เครื่องนี้เป็นของเธอ |
| 5 | Is this coat yours? | เสื้อโค้ทตัวนี้เป็นของคุณไหมคะ |
| 6 | Where is my husband? | สามีของฉันอยู่ที่ไหนคะ |
| 7 | What is your name? | คุณชื่ออะไรคะ |
| 8 | Can I help you? | มีอะไรให้ช่วยไหมคะ |
| 9 | Please wait here. | กรุณารอที่นี่ค่ะ |
| 10 | I don't understand. | ฉันไม่เข้าใจค่ะ |
| **Level 2** |||
| 11 | Can you say that again, please? | พูดอีกครั้งได้ไหมคะ |
| 12 | Please speak slowly. | กรุณาพูดช้าๆ ค่ะ |
| 13 | How do you spell it? | สะกดยังไงคะ |
| 14 | Do you have a reservation? | คุณจองไว้หรือเปล่าคะ |
| 15 | Who is it for? | สำหรับใครคะ |
| 16 | Here is your key. | นี่กุญแจของคุณค่ะ |
| 17 | Have a good day! | ขอให้เป็นวันที่ดีนะคะ |
| 18 | I am tired, but I am happy. | ฉันเหนื่อย แต่ฉันมีความสุขค่ะ |
| 19 | This gift is not mine. It is yours. | ของขวัญนี้ไม่ใช่ของฉัน เป็นของคุณค่ะ *(faith, grace)* |
| 20 | I can't do it alone. God helps me. | ฉันทำคนเดียวไม่ได้ พระเจ้าช่วยฉัน *(faith)* |

### 💎 Colors and Shapes Cave

Give each card a background tint that matches the color in its sentence, kept inside the theme's glossy style.

| # | English | Thai |
|---|---|---|
| **Level 1** |||
| 1 | I have a red bag. | ฉันมีกระเป๋าสีแดงค่ะ |
| 2 | My car is white. | รถของฉันสีขาว |
| 3 | Her dress is pink. | ชุดของเธอสีชมพู |
| 4 | His shirt is blue. | เสื้อของเขาสีน้ำเงิน |
| 5 | The sky is blue today. | วันนี้ท้องฟ้าสีฟ้า |
| 6 | I like green tea. | ฉันชอบชาเขียวค่ะ |
| 7 | The key card is black. | คีย์การ์ดสีดำค่ะ |
| 8 | Please sit at the round table. | เชิญนั่งที่โต๊ะกลมค่ะ |
| 9 | The sign is a red circle. | ป้ายเป็นวงกลมสีแดง |
| 10 | The box is too big. | กล่องใหญ่เกินไป |
| **Level 2** |||
| 11 | Do you have a smaller one? | มีอันเล็กกว่านี้ไหมคะ |
| 12 | The white towels are in the closet. | ผ้าเช็ดตัวสีขาวอยู่ในตู้ค่ะ |
| 13 | Turn left at the yellow sign. | เลี้ยวซ้ายที่ป้ายสีเหลืองค่ะ |
| 14 | Which one is yours, blue or gray? | อันไหนของคุณคะ สีน้ำเงินหรือสีเทา |
| 15 | These two are the same. | สองอันนี้เหมือนกัน |
| 16 | That one is different. | อันนั้นไม่เหมือนกัน |
| 17 | The baby's room is light green. | ห้องของลูกเป็นสีเขียวอ่อน |
| 18 | I want a long, warm coat. | ฉันอยากได้เสื้อโค้ทยาวที่อุ่นค่ะ |
| 19 | There is a cross on the church. | มีไม้กางเขนอยู่บนโบสถ์ *(faith)* |
| 20 | God made every color. | พระเจ้าทรงสร้างทุกสี *(faith)* |

Tip on card 5: Thai says ฟ้า for sky blue and น้ำเงิน for dark blue, but English uses "blue" for both.

### 🔢 Numbers Valley

| # | English | Thai |
|---|---|---|
| **Level 1** |||
| 1 | How many nights? | กี่คืนคะ |
| 2 | Two adults and one child. | ผู้ใหญ่สองคน เด็กหนึ่งคน |
| 3 | Your room is two-oh-four. | ห้องของคุณคือ 204 ค่ะ |
| 4 | Check-out is at eleven. | เช็คเอาท์สิบเอ็ดโมงค่ะ |
| 5 | Breakfast is from seven to ten. | อาหารเช้าตั้งแต่เจ็ดโมงถึงสิบโมงค่ะ |
| 6 | It is ninety-nine dollars a night. | คืนละเก้าสิบเก้าดอลลาร์ค่ะ |
| 7 | Thirteen or thirty? | สิบสามหรือสามสิบคะ (trap: -TEEN/-TY) |
| 8 | Fifteen minutes, please. | สิบห้านาทีค่ะ |
| 9 | What time is it? | กี่โมงแล้วคะ |
| 10 | Please write your phone number. | กรุณาเขียนเบอร์โทรศัพท์ค่ะ |
| **Level 2** |||
| 11 | It is three thirty. | สามโมงครึ่งค่ะ |
| 12 | That is twenty dollars and fifty cents. | ยี่สิบดอลลาร์ห้าสิบเซนต์ค่ะ |
| 13 | Your change is five dollars. | เงินทอนห้าดอลลาร์ค่ะ |
| 14 | I need two more pillows. | ฉันต้องการหมอนเพิ่มอีกสองใบค่ะ |
| 15 | The laundry room is on the first floor. | ห้องซักผ้าอยู่ชั้นหนึ่งค่ะ |
| 16 | I am seven months pregnant. | ฉันตั้งครรภ์เจ็ดเดือนแล้วค่ะ |
| 17 | The baby is due December seventeenth. | ลูกกำหนดคลอดวันที่สิบเจ็ดธันวาคมค่ะ |
| 18 | There are seven days in a week. | หนึ่งสัปดาห์มีเจ็ดวัน |
| 19 | We have two rooms left. | เราเหลือห้องว่างสองห้องค่ะ |
| 20 | Jesus fed five thousand people. | พระเยซูทรงเลี้ยงคนห้าพันคน *(faith)* |

Maxwell should edit cards 3, 5, 6 and 15 to match the real room numbers, hours and rates at his inn.

### 👶 Baby and Hospital (bonus, open from the start)

| # | English | Thai |
|---|---|---|
| **Level 1** |||
| 1 | I need a Thai interpreter. | ฉันต้องการล่ามภาษาไทยค่ะ |
| 2 | I am in pain. | ฉันเจ็บค่ะ |
| 3 | My water broke. | น้ำคร่ำของฉันแตกแล้วค่ะ |
| 4 | The pain comes every five minutes. | เจ็บทุกห้านาทีค่ะ |
| 5 | Please call my husband. | กรุณาโทรหาสามีของฉันค่ะ |
| 6 | I am bleeding. | ฉันมีเลือดออกค่ะ |
| 7 | The baby is not moving. | ลูกไม่ดิ้นค่ะ |
| 8 | I feel sick. | ฉันรู้สึกไม่สบายค่ะ |
| 9 | Can I have some water? | ขอน้ำหน่อยได้ไหมคะ |
| 10 | I am allergic to ___. | ฉันแพ้ ___ ค่ะ |
| **Level 2** |||
| 11 | I want to push. | ฉันอยากเบ่งค่ะ |
| 12 | Is my baby okay? | ลูกของฉันปลอดภัยไหมคะ |
| 13 | I want to hold my baby. | ฉันอยากอุ้มลูกค่ะ |
| 14 | Is it a boy or a girl? | ผู้ชายหรือผู้หญิงคะ |
| 15 | The baby is hungry. | ลูกหิวค่ะ |
| 16 | Please help me feed the baby. | ช่วยฉันให้นมลูกหน่อยค่ะ |
| 17 | I need a clean diaper. | ฉันต้องการผ้าอ้อมสะอาดค่ะ |
| 18 | The baby is sleeping. | ลูกกำลังนอนหลับ |
| 19 | When can we go home? | เมื่อไหร่เราจะกลับบ้านได้คะ |
| 20 | Thank you, God, for my baby. | ขอบคุณพระเจ้าสำหรับลูกของฉันค่ะ *(faith)* |

Card 1 is first on purpose. US hospitals have to provide a free interpreter, and that one sentence covers everything else in an emergency. Add a pinned **"Emergency" button** in this zone that shows cards 1 to 7 large, one per screen, so she can show them to a nurse.

### 💬 Maxwell Says (bonus)

This starts empty with an **"Add a card" form** (English, Thai, optional respelling). The form sits behind a 2-second long-press on the zone title so Nancy doesn't open it by accident. Cards are saved locally and included in Backup. They use the same Leitner system and shuffle, but there's no boss and no stars, so it stays low pressure.

## 10. Acceptance checklist

1. Install from Safari to the Home Screen, turn on Airplane Mode, force-quit and reopen. Everything works.
2. Nothing overlaps the notch or home bar, in portrait on an iPhone with Face ID.
3. Every tap target is in the bottom 45% of the screen and at least 56 px.
4. Tapping flips the card and speaks it on the first tap. 🔊 replays it.
5. Again repeats the card in the same run. Got It moves it up a box. Re-entering a level gives a different order.
6. The five-star smash plays and adds exactly 1 token. The Free Gift is in her inventory on first launch and opens the Grace scroll.
7. Losing a boss gives no penalty. Beating one unlocks its scroll and its cosmetic.
8. Progress survives closing the app and restarting the phone, and Backup and Restore round-trip the JSON.
9. Thai renders in Kanit with no empty boxes. All text passes WCAG AA contrast.
10. Nancy reads every Thai line before release.
