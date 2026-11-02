# Nancy's English Flashcards: Improved Spec (v2)

Audience: Nancy, a Thai-speaking adult beginner on iPhone. She's about 7 months pregnant and wants to grow in the Christian faith. Make it calm, warm and never test-like.

---

## 1. Platform (built to work right the first time)

- Build it as an **offline PWA** (one HTML/JS app she adds to her Home Screen with Safari's "Add to Home Screen"). That means no App Store and no Mac or Xcode, and a service worker keeps it working offline. A native SwiftUI app is only worth it if Maxwell wants it in the App Store.
- Bundle every asset locally: fonts, SVG art, card data (JSON) and sounds. Nothing loads from the network after the first install.
- Save progress in `localStorage` (or IndexedDB). That includes the current card in each set, Leitner box per card, settings and streak.
- Text-to-speech uses the Web Speech API (`speechSynthesis`) with an en-US voice. On iOS, speech has to start inside a tap, and the flip tap counts. Default rate 0.8, with a **Slow** toggle at 0.5. Also add a speaker button so she can replay without flipping.
- Stop iOS from hijacking the swipes. Set `touch-action: none` on the card area and `overscroll-behavior: none` on the body, and turn off pull-to-refresh and text selection. Add small ▲ ▼ buttons as a backup for swiping.
- Respect Safe Area insets (notch and home bar). Run portrait-only, with every tap target at least 56 px.

## 2. Visual style (Brighter Child)

- **Fonts:** English in **Fredoka** (bold, rounded). Thai in **Mitr** or **Kanit**, which have rounded Thai glyphs that match Fredoka. Both are free Google Fonts, so bundle them locally.
- **Card:** a big rounded rectangle (radius 32 px) with a thick white border (8 px), a soft drop shadow and a faint paper texture. Behind it, show 2 or 3 card edges peeking out at slight angles so it looks like a real deck.
- **Art:** chunky flat cartoon SVGs with thick dark outlines, 2 to 4 flat colors each, rounded and friendly, never realistic. Keep one consistent style across all 150 cards, either generated as a set or taken from a single open-license pack such as OpenMoji. Don't mix sources.
- **Contrast:** dark text on light backgrounds and white text with a dark outline on dark ones (black, brown, purple, blue). Check that every color card passes WCAG AA.

## 3. Card layout (improved)

**Front:** a large picture, the English word big and bold, and the respelling just under it in a pill, like `red`, `BAY-bee` or `buh-NAN-uh`.
Change from v1: Thai is **hidden on the front by default** so she gets to recall it herself. A "Show Thai hint" setting puts it back in small grey text for tired days.

**Back (after a tap flip):**
1. The Thai translation, large.
2. A short English example sentence of six words or fewer, using words she already knows.
3. The Thai translation of the sentence underneath.
4. A **Sound tip for Thai speakers** in Thai, on cards where one applies (see the Phonics set).
5. Two buttons: **"Again" 🔁** and **"Got it" ✅** (see section 5).

Speech on flip: say the word, pause 600 ms, then say the example sentence.

## 4. Gestures (feeling like real cards)

- **Tap:** a 3D flip on the Y axis (about 400 ms) with a soft paper "flick" sound and a light haptic where the device supports it.
- **Swipe up:** the card slides off the top with a slight tilt and the next card rises from the stack.
- **Swipe down:** the previous card drops back on top.
- **Long-press:** shuffle the deck, with a riffle sound and a stack-shuffle animation.
- The card follows her finger and springs back if the swipe is too short.
- Progress shows two ways: a bar at the top ("12 / 50") and a stack that gets visibly thinner as she goes.

## 5. Learning logic

- Each set is split into **five packs of 10**, taught in order. A pack unlocks when 8 of its 10 cards are in "Got it" (or she can skip ahead).
- Use a light **Leitner** system with three boxes. "Again" cards come back within the next 3 to 5 cards, and "Got it" cards come back less often. Never show a score, a timer or a red X.
- **Review mode:** a daily mix of 10 cards from all sets, weighted toward "Again" cards.
- **Phonics mode toggle:** works in every set. It splits the word into colored syllables (BA·by), makes the stressed syllable larger and bold, and has TTS say each syllable slowly before the whole word.

## 6. Ordering for a Thai speaker

Thai speakers usually find these English sounds hardest:
- final consonants, which get dropped or softened (bus→"bat", ball→"bon"), especially -s, -l, -v and -z
- r and l
- "th"
- v and w
- sh and ch
- consonant clusters, where an extra vowel slips in ("school"→"sa-kool")
- word stress, since Thai uses tone instead

So each set starts with easy wins and works up to those trouble spots. One English grammar point is worth teaching early because Thai does it the other way: in English, **color goes before the thing** ("red apple"), while Thai says แอปเปิลสีแดง.

---

## 7. Phonics (50)

The respelling puts the stressed syllable in CAPS. The Thai tip goes on the back.

| # | Word | Syllables / stress | Respelling | Thai |
|---|---|---|---|---|
| **Pack 1: short vowels (easy wins)** |||||
| 1 | cat | cat | kat | แมว |
| 2 | bed | bed | bed | เตียง |
| 3 | pig | pig | pig | หมู |
| 4 | hot | hot | hot | ร้อน |
| 5 | sun | sun | sun | ดวงอาทิตย์ |
| 6 | man | man | man | ผู้ชาย |
| 7 | ten | ten | ten | สิบ |
| 8 | sit | sit | sit | นั่ง |
| 9 | dog | dog | dawg | สุนัข |
| 10 | cup | cup | kup | ถ้วย |
| **Pack 2: ending sounds** (tip: finish the last sound, don't swallow it) |||||
| 11 | bus | bus | bus | รถบัส |
| 12 | rice | rice | ryss | ข้าว |
| 13 | nose | nose | nohz | จมูก |
| 14 | ball | ball | bawl | ลูกบอล |
| 15 | milk | milk | milk | นม |
| 16 | five | five | fyv | ห้า |
| 17 | bag | bag | bag | กระเป๋า |
| 18 | house | house | hows | บ้าน |
| 19 | cheese | cheese | cheez | ชีส |
| 20 | glass | glass | glass | แก้ว |
| **Pack 3: tricky sounds** (r and l, th, v and w, sh and ch) |||||
| 21 | rain | rain | rayn | ฝน |
| 22 | light | light | lyt | แสงสว่าง |
| 23 | three | three | three | สาม |
| 24 | think | think | think | คิด |
| 25 | mother | MOTH·er | MUH-ther | แม่ |
| 26 | very | VER·y | VEH-ree | มาก |
| 27 | water | WA·ter | WAW-ter | น้ำ |
| 28 | shoe | shoe | shoo | รองเท้า |
| 29 | chair | chair | chair | เก้าอี้ |
| 30 | zoo | zoo | zoo | สวนสัตว์ |
| **Pack 4: blends** (tip: no extra vowel between the consonants) |||||
| 31 | bread | bread | bred | ขนมปัง |
| 32 | play | play | play | เล่น |
| 33 | school | school | skool | โรงเรียน |
| 34 | snow | snow | snoh | หิมะ |
| 35 | star | star | star | ดาว |
| 36 | spoon | spoon | spoon | ช้อน |
| 37 | fruit | fruit | froot | ผลไม้ |
| 38 | sleep | sleep | sleep | นอนหลับ |
| 39 | clean | clean | kleen | สะอาด |
| 40 | friend | friend | frend | เพื่อน |
| **Pack 5: longer words and stress** |||||
| 41 | baby | BA·by | BAY-bee | ทารก |
| 42 | happy | HAP·py | HAP-ee | มีความสุข |
| 43 | doctor | DOC·tor | DOK-ter | หมอ |
| 44 | father | FA·ther | FAH-ther | พ่อ |
| 45 | family | FAM·i·ly | FAM-uh-lee | ครอบครัว |
| 46 | hospital | HOS·pi·tal | HOS-pih-tul | โรงพยาบาล |
| 47 | banana | ba·NAN·a | buh-NAN-uh | กล้วย |
| 48 | tomorrow | to·MOR·row | tuh-MOR-oh | พรุ่งนี้ |
| 49 | Bible | BI·ble | BY-bul | พระคัมภีร์ |
| 50 | Jesus | JE·sus | JEE-zus | พระเยซู |

Sound tips to show on the back (Thai):
- Endings: "ออกเสียงท้ายคำให้ชัด อย่ากลืนเสียง" (say the end of the word clearly)
- th: "แลบลิ้นออกมาเล็กน้อยระหว่างฟัน" (put your tongue a little between your teeth)
- v: "ฟันบนแตะริมฝีปากล่าง" (top teeth touch the bottom lip)
- r: "ม้วนลิ้นขึ้น ไม่แตะเพดาน" (curl the tongue up without touching the roof of the mouth)
- Blends: "อย่าใส่เสียงสระแทรก" (don't add a vowel in between)

## 8. Colors and Shapes (50)

The card background is the color itself. Shape cards rotate through bright backgrounds.

| # | Word | Respelling | Thai | Background |
|---|---|---|---|---|
| **Pack 1: colors** |||||
| 1 | red | red | สีแดง | #E53935 |
| 2 | blue | bloo | สีน้ำเงิน | #1E63D6 |
| 3 | yellow | YEL-oh | สีเหลือง | #FFD600 |
| 4 | green | green | สีเขียว | #2EAD4B |
| 5 | orange | OR-inj | สีส้ม | #FF8A00 |
| 6 | purple | PUR-pul | สีม่วง | #7B3FC4 |
| 7 | pink | pink | สีชมพู | #FF5FA2 |
| 8 | brown | brown | สีน้ำตาล | #8B5A2B |
| 9 | black | blak | สีดำ | #111111 |
| 10 | white | wyt | สีขาว | #FFFFFF |
| 11 | gray | gray | สีเทา | #8E8E93 |
| 12 | gold | gohld | สีทอง | #D4A017 |
| **Pack 2: shapes** |||||
| 13 | circle | SUR-kul | วงกลม | |
| 14 | square | skwair | สี่เหลี่ยมจัตุรัส | |
| 15 | triangle | TRY-ang-gul | สามเหลี่ยม | |
| 16 | rectangle | REK-tang-gul | สี่เหลี่ยมผืนผ้า | |
| 17 | star | star | รูปดาว | |
| 18 | heart | hart | รูปหัวใจ | |
| 19 | oval | OH-vul | วงรี | |
| 20 | diamond | DY-mund | รูปข้าวหลามตัด | |
| 21 | cross | kraws | ไม้กางเขน | |
| 22 | moon | moon | พระจันทร์ | |
| 23 | arrow | AIR-oh | ลูกศร | |
| 24 | line | lyn | เส้น | |
| **Pack 3: describing words** |||||
| 25 | big | big | ใหญ่ | |
| 26 | small | smawl | เล็ก | |
| 27 | long | lawng | ยาว | |
| 28 | short | short | สั้น | |
| 29 | tall | tawl | สูง | |
| 30 | round | rownd | กลม | |
| 31 | same | saym | เหมือนกัน | |
| 32 | different | DIF-runt | ต่างกัน | |
| 33 | light (color) | lyt | อ่อน (สีอ่อน) | |
| 34 | dark (color) | dark | เข้ม (สีเข้ม) | |
| **Packs 4 and 5: colors around us** (color goes first in English) |||||
| 35 | red apple | red AP-ul | แอปเปิลสีแดง | |
| 36 | yellow banana | YEL-oh buh-NAN-uh | กล้วยสีเหลือง | |
| 37 | green leaf | green leef | ใบไม้สีเขียว | |
| 38 | blue sky | bloo sky | ท้องฟ้าสีฟ้า | |
| 39 | white cloud | wyt klowd | เมฆสีขาว | |
| 40 | black cat | blak kat | แมวสีดำ | |
| 41 | orange carrot | OR-inj KAIR-ut | แครอทสีส้ม | |
| 42 | pink flower | pink FLOW-er | ดอกไม้สีชมพู | |
| 43 | brown bread | brown bred | ขนมปังสีน้ำตาล | |
| 44 | purple grapes | PUR-pul grayps | องุ่นสีม่วง | |
| 45 | gray elephant | gray EL-uh-funt | ช้างสีเทา | |
| 46 | gold ring | gohld ring | แหวนทอง | |
| 47 | white snow | wyt snoh | หิมะสีขาว | |
| 48 | yellow sun | YEL-oh sun | ดวงอาทิตย์สีเหลือง | |
| 49 | green tree | green tree | ต้นไม้สีเขียว | |
| 50 | white dove | wyt duv | นกพิราบสีขาว | |

Note for card 2 or 38: in Thai, the blue of the sky is ฟ้า and dark blue is น้ำเงิน, but English uses "blue" for both. Put that on the back as a tip.

## 9. Sight Words (50)

These are ordered by how useful they are in daily life, not alphabetically. Possessives come early because they're Nancy's focus. A few examples gently carry faith themes, about one in eight cards.

| # | Word | Respelling | Thai | Example | Example (Thai) |
|---|---|---|---|---|---|
| 1 | I | eye | ฉัน | I am Nancy. | ฉันชื่อแนนซี่ |
| 2 | you | yoo | คุณ | I love you. | ฉันรักคุณ |
| 3 | yes | yes | ใช่ | Yes, I can. | ใช่ ฉันทำได้ |
| 4 | no | noh | ไม่ | No, thank you. | ไม่ ขอบคุณค่ะ |
| 5 | please | pleez | กรุณา | Water, please. | ขอน้ำหน่อยค่ะ |
| 6 | thank you | THANK-yoo | ขอบคุณ | Thank you, God. | ขอบคุณพระเจ้า |
| 7 | my | my | ของฉัน | This is my bag. | นี่คือกระเป๋าของฉัน |
| 8 | your | yor | ของคุณ | Is this your cup? | นี่ถ้วยของคุณใช่ไหม |
| 9 | he | hee | เขา (ผู้ชาย) | He is my husband. | เขาเป็นสามีของฉัน |
| 10 | she | shee | เธอ (ผู้หญิง) | She is happy. | เธอมีความสุข |
| 11 | his | hiz | ของเขา (ผู้ชาย) | This is his car. | นี่คือรถของเขา |
| 12 | her | hur | ของเธอ (ผู้หญิง) | Her baby is coming. | ลูกของเธอกำลังจะมา |
| 13 | mine | myn | ของฉัน | The blue bag is mine. | กระเป๋าสีน้ำเงินเป็นของฉัน |
| 14 | yours | yorz | ของคุณ | This gift is yours. | ของขวัญนี้เป็นของคุณ |
| 15 | it | it | มัน | It is hot. | อากาศร้อน |
| 16 | we | wee | เรา | We are a family. | เราเป็นครอบครัว |
| 17 | our | OW-er | ของเรา | This is our home. | นี่คือบ้านของเรา |
| 18 | they | thay | พวกเขา | They are my friends. | พวกเขาเป็นเพื่อนของฉัน |
| 19 | their | thair | ของพวกเขา | Their dog is big. | หมาของพวกเขาตัวใหญ่ |
| 20 | is | iz | เป็น / อยู่ | God is good. | พระเจ้าทรงดี |
| 21 | am | am | เป็น / อยู่ (ใช้กับ I) | I am tired. | ฉันเหนื่อย |
| 22 | are | ar | เป็น / อยู่ (ใช้กับ you, we, they) | You are kind. | คุณใจดี |
| 23 | a | uh | หนึ่ง (อัน, ตัว) | I have a cat. | ฉันมีแมวหนึ่งตัว |
| 24 | the | thuh | ใช้ชี้สิ่งที่รู้กันอยู่ (ไม่มีคำแปลตรง) | The baby is sleeping. | ลูกกำลังนอนหลับ |
| 25 | and | and | และ | Mom and Dad. | แม่และพ่อ |
| 26 | this | this | นี่ / นี้ | This is good. | นี่ดีนะ |
| 27 | that | that | นั่น / นั้น | What is that? | นั่นคืออะไร |
| 28 | here | heer | ที่นี่ | Come here, please. | มาที่นี่หน่อย |
| 29 | there | thair | ที่นั่น | The store is there. | ร้านอยู่ที่นั่น |
| 30 | in | in | ใน | The cat is in the box. | แมวอยู่ในกล่อง |
| 31 | on | on | บน | The cup is on the table. | ถ้วยอยู่บนโต๊ะ |
| 32 | at | at | ที่ | I am at home. | ฉันอยู่ที่บ้าน |
| 33 | to | too | ไป / ถึง | We go to church. | เราไปคริสตจักร |
| 34 | not | not | ไม่ | I am not hungry. | ฉันไม่หิว |
| 35 | can | kan | ได้ / สามารถ | I can do it. | ฉันทำได้ |
| 36 | go | goh | ไป | Let's go! | ไปกันเถอะ |
| 37 | come | kum | มา | Come and eat. | มากินข้าว |
| 38 | see | see | เห็น | I see you. | ฉันเห็นคุณ |
| 39 | look | luk | ดู | Look at the baby! | ดูลูกสิ |
| 40 | like | lyk | ชอบ | I like rice. | ฉันชอบข้าว |
| 41 | love | luv | รัก | Jesus loves you. | พระเยซูทรงรักคุณ |
| 42 | want | wont | อยาก / ต้องการ | I want water. | ฉันอยากได้น้ำ |
| 43 | have | hav | มี | I have a gift. | ฉันมีของขวัญ |
| 44 | give | giv | ให้ | God gives good gifts. | พระเจ้าประทานของขวัญที่ดี |
| 45 | eat | eet | กิน | Let's eat. | กินข้าวกันเถอะ |
| 46 | help | help | ช่วย | Help me, please. | ช่วยฉันหน่อย |
| 47 | what | wut | อะไร | What is your name? | คุณชื่ออะไร |
| 48 | where | wair | ที่ไหน | Where is the bathroom? | ห้องน้ำอยู่ที่ไหน |
| 49 | who | hoo | ใคร | Who is he? | เขาคือใคร |
| 50 | good | gud | ดี | Good morning! | สวัสดีตอนเช้า |

Phonics and Colors cards follow the same back format: one short example, in the same style. About one in eight cards in each set can carry a gentle faith theme, for example "The baby is a gift from God." (ลูกเป็นของขวัญจากพระเจ้า) or "Jesus is my friend." (พระเยซูเป็นเพื่อนของฉัน).

## 10. Things that would delight Nancy

- **Record and compare:** a 🎤 button records her saying the word and plays her voice right after the TTS voice. It stays on her phone and nothing is graded.
- **Set complete:** soft confetti and a gentle chime, then a short closing card: "Well done, Nancy! God loves you." (เก่งมากแนนซี่! พระเจ้ารักคุณ) The final card of each set can show a short, simple Bible verse in English and Thai. Take the Thai from a published Thai Bible (THSV 2011) rather than translating it yourself.
- **Gentle streak:** a small sun that grows with each day she practices and never shames her for a missed day.
- **"Baby and Hospital" bonus set**, for her due date around Dec 17. Words like nurse, doctor, pain, push, water, diaper, milk, sleep, hungry, crying, blanket, and "my husband," plus a few phrases ("I need help." "Where is my baby?"). This is the most practical gift the app could give her right now.
- **"Maxwell Says" set (optional):** Maxwell can type a phrase he uses often and the Thai, and it becomes a card with TTS. That helps with the moments when he talks and she doesn't follow.
- **Thai interface:** labels in Thai with English under them ("พลิก / Flip", "อีกครั้ง / Again", "จำได้ / Got it").
- **Comfortable for pregnancy:** a calm mode with softer colors and no sound effects, a large-text option, and sessions short enough to finish lying down (10 cards).

## 11. Acceptance checklist

1. Installs from Safari to the Home Screen, then works with Airplane Mode on.
2. All 150 cards load. Every card has a word, respelling, Thai, an example, Thai for the example, and art.
3. Tapping flips the card and speaks, the first time, on a real iPhone.
4. Swiping up and down moves cards without scrolling the page or triggering pull-to-refresh.
5. Progress survives closing the app and restarting the phone.
6. Thai text renders in Mitr or Kanit with no empty boxes, and every color card passes the contrast check.
7. Phonics mode shows syllables and stress on every multi-syllable card.
8. **Before release:** Nancy (or another native Thai speaker) skims the Thai column and fixes anything that sounds unnatural.
