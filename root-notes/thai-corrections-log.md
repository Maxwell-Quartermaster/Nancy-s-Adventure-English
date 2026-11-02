# Thai Corrections Log

Owner: Grok 2: Instructor (Language and Grace)

Purpose: every Thai wording fix Nancy flags, in the game or the phrasebook, is logged here, so the same fix is never made twice. Check this log before writing any new Thai string.

## How to log

Add one entry per fix, newest at the top. Each entry has:

- **Date:** YYYY-MM-DD.
- **Where:** the file plus the card id or screen, e.g. `v5-17 cards.json, sw-04`.
- **Wrong:** the exact Thai that was there.
- **Correction:** the exact Thai to use instead.
- **Why:** one line.
- **Flagged by:** Nancy, or Instructor if I found it in review.

## Entries

### 2026-10-30 (Instructor review, before Nancy has checked any of it)

- **Where:** "God made..." cards (old cs-14, cs-16)
  - **Wrong:** พระเจ้าสร้าง...
  - **Correction:** พระเจ้าทรงสร้าง...
  - **Why:** Thai Christians use ทรง before God's actions.
  - **Flagged by:** Instructor

- **Where:** "It is mine." (old sw-04)
  - **Wrong:** มันเป็นของฉัน
  - **Correction:** นี่ของฉัน
  - **Why:** มัน sounds stiff and unnatural here.
  - **Flagged by:** Instructor

- **Where:** "The baby is coming." (bh emergency)
  - **Wrong:** ลูกกำลังจะออกแล้วค่ะ
  - **Correction:** ลูกจะคลอดแล้วค่ะ
  - **Why:** clearer and more urgent.
  - **Flagged by:** Instructor

- **Where:** trap note for "pleasant"
  - **Wrong:** น่ารัก
  - **Correction:** ร่าเริง / น่าพอใจ
  - **Why:** น่ารัก means "cute," not "pleasant."
  - **Flagged by:** Instructor

- **Where:** "You earned this!" reward text
  - **Wrong:** คุณได้รับสิ่งนี้แล้ว!
  - **Correction:** เก่งมาก! รางวัลนี้เป็นของคุณ
  - **Why:** the old text means "you received this" and loses the sense of earning it.
  - **Flagged by:** Instructor

- **Where:** "Welcome back" streak text
  - **Wrong:** สตรีคของคุณรออยู่
  - **Correction:** วันเรียนของคุณยังอยู่ครบ
  - **Why:** สตรีค is jargon Nancy may not know.
  - **Flagged by:** Instructor

- **Where:** "Got it" button
  - **Wrong:** ได้แล้ว
  - **Correction:** เข้าใจแล้ว
  - **Why:** ได้แล้ว is vague, while เข้าใจแล้ว clearly means "I understand now."
  - **Flagged by:** Instructor

- **Where:** Sight Words zone label
  - **Wrong:** คำพื้นฐาน
  - **Correction:** คำง่ายๆ
  - **Why:** the old label sounds like a textbook; the new one is everyday Thai.
  - **Flagged by:** Instructor

## 2026-10-30 4:35 PM MT, v5-20 candidate
- Where: leaf sayings (8, `v520/jw/picks.json`, SUPERSEDED by Option Two, 6 whole verses)
- Wrong: none. All THSV 2011 and ESV texts match bible.com exactly.
- Correction: added plain glosses, because "เรา" in these sayings means Jesus ("I"), not "we". See `v520/instructor-thai-check.md`.
- Flagged by: Instructor (pre-check, not Nancy)

## 2026-10-30 4:32 PM MT, v5-20 candidate
- Where: My Stuff lock overlay
- Wrong: ยังไม่ปลดล็อก ("not unlocked yet"), which brings back unlock wording against the Grace rule
- Correction: ได้รับเมื่อถึงเลเวล {n} ("Yours at level {n}"), the existing goal line
- Flagged by: Auditor

## 2026-10-30 4:34 PM MT, v5-20 leaf glosses (flagged by Auditor)
- John 8:12 gloss: พระเยซูเป็นแสงสว่าง ไม่ต้องอยู่ในความมืด → พระเยซูเป็นแสงสว่าง คนที่ตามพระองค์จะไม่อยู่ในความมืด (the condition "whoever follows" was missing)
- Luke 12:7 gloss: คุณมีค่ามากสำหรับพระเจ้า → ไม่ต้องกลัว คุณมีค่ามากสำหรับพระเจ้า ("Fear not" was missing)
- John 10:11: now the whole verse, so the gloss becomes พระเยซูดูแลคุณเหมือนคนเลี้ยงแกะ และยอมตายเพื่อคุณ
- All glosses and the leaf label marked NEEDS NANCY

## 2026-10-30 5:10 PM MT, leaf sayings Option Two (6 whole verses, Maxwell approved)
- Where: glosses for John 15:9, Luke 12:7, John 10:11, John 8:12, John 15:11 (Watchman drafts plus my John 10:11)
- Wrong: verbs with God or Jesus as the subject had no ทรง (รัก, นับ, ดูแล, ยอมตาย, เป็น, อยากให้)
- Correction: added ทรง, e.g. พระเจ้าทรงนับ, พระเยซูทรงรัก, ทรงยอมตาย. อยากให้ → ทรงต้องการให้. Final list in `v520/instructor-thai-check.md`
- Why: consistent with the earlier fix พระเจ้าสร้าง → พระเจ้าทรงสร้าง
- Flagged by: Instructor (NEEDS NANCY)

## 2026-10-30 6:28 PM MT, v5-20 full loop (scope item 8)
- Where: `uiText.earnedShelf` (My Stuff shelf label)
- Wrong: เก่งมาก! รางวัลนี้เป็นของคุณ / "You earned this!", an exact duplicate of `rewardText`, so the earned line showed twice
- Correction: ถ้วยรางวัลล่าสุดของฉัน / "My newest trophies" (key name kept). `rewardText` now appears once per screen, as the banner only
- Flagged by: Instructor (Maxwell full loop), NEEDS NANCY

## 2026-10-30 ~6:39 PM MT, v5-20 6:31 PM full loop audit (Instructor, before Nancy; all NEEDS NANCY)
Full list with reasons: v520/instructor-thai-audit-631.md. Fixes:
- ph-17 thDef: หลายคนนั้น → คนกลุ่มนั้น (natural)
- cs-06: รุ้งกินน้ำ → สายรุ้ง (one term for rainbow)
- cs-07: สีสันทั้งหลาย → สีสันต่างๆ (natural)
- sw-11 trapNote: nine = เก้าโมง → nine = เก้า (meaning)
- sw-24 trapNote: lock = ล็อก → lock = แม่กุญแจ (consistency with ph-12)
- bh-29: ฉันต้องการพยาบาล → ฉันต้องการพยาบาลค่ะ (Nancy's particle)
- ms-04: เช็คเอาท์ 11 โมงค่ะ → เช็คเอาท์สิบเอ็ดโมงค่ะ (times in words)
- ms-14: พระเยซูเป็น → พระเยซูทรงเป็น (ทรง rule)
- uiText.unlocksPips/Days/Bosses: เป็นของคุณเมื่อ… → ได้รับเมื่อ… (same family as the logged ได้รับเมื่อถึงเลเวล {n})
- uiText.scrollsEmpty: ม้วนคัมภีร์ของคุณจะมาอยู่ที่นี่เมื่อคุณเล่น → ม้วนคัมภีร์ที่คุณได้รับจะมาอยู่ที่นี่ (translationese; grace)
- uiText.classMage: นักเวทย์ → นักเวท (spelling)
- welcomeBack: ยินดีต้อนรับกลับ! → ยินดีต้อนรับกลับมา! (spoken form)
- encouragement[0]: ผมรักคุณนะ → ผมรักคุณนะครับ (Maxwell's particle)
- trophy theme-stars: คืนเต็มไปด้วยดาว → คืนฟ้าเต็มดาว (natural)
- gear sling-shepherd: สลิงหินอันน้อย → สลิงหินอันเล็ก (natural)
- jesusWordsFallback[0]: เพราะพระเจ้าดี → เพราะพระเจ้าทรงดี (ทรง rule)
- map region r3: ทะเลสาบบ้าน → ทะเลสาบบ้านเรา (reads as "lake house")
- New tie card ms-32: brief's ให้ฉันจัดเนคไทให้นะคะที่รัก → เดี๋ยวฉันจัดเนคไทให้นะคะ ที่รัก ("let me" in Thai; no double ให้)
- Rule added: goal lines for My Stuff all start with ได้รับเมื่อ…
- Flagged by: Instructor

## 2026-10-30 ~8:05 PM PT, Q-0757 infinity loop (t49u), Instructor; all NEEDS NANCY (after launch)
Sheet: v520/instructor-q0757-fixes.json; patch v520/instructor_patch_q0757.py
- uiText.pantry: ตู้เสบียงทองคำ → ตู้กับข้าวทองคำ (ตู้เสบียง = train dining car / supply locker; ตู้กับข้าว = home pantry)
- pantry trail-hearts: ทางหัวใจ → รอยหัวใจ; trophy trail-leaf: ทางใบไม้ → รอยใบไม้ (a trail left behind = รอย, not ทาง road)
- restScreen: วันนี้เก่งมากเลย! เล่นต่อหรือพักก่อนดีคะ → วันนี้เก่งมากเลย! เล่นต่อหรือพักก่อนดี (คะ is Nancy's particle, but the game is the speaker; neutral, like the bh-11 reply)
- ms-31 (Maxwell Says): มาอธิษฐานกันนะ → มาอธิษฐานกันนะครับ; แปะมือ! → แปะมือครับ! (card th summary + both prompts; Maxwell's particle, as on ms-12)
- fd-31: รับข้าวหรือเส้นคู่กัน → รับข้าวหรือเส้นดี (คู่กัน reads "as a pair/together")
- fd-29: เผ็ดสองดาวหรือสามดาว → เผ็ดแค่ไหน สองดาวหรือสามดาว (English now "How spicy? Two stars or three?")
- fd-36: วันนี้แกงเขียวหวานขายดีมาก → วันนี้แกงเขียวหวานขายดี (English "very" dropped)
- fd-38: โต๊ะสองที่ ข้างในหรือริมหน้าต่าง → โต๊ะสองที่ ริมหน้าต่างหรือข้างใน (English order now "Window or inside?")
- fd-33 trapNote: (ฟังเสียง t ท้ายคำ) → (can't เสียงหนักกว่า) (US English often drops the final t; stress is the real cue)
- cv-04: ชูร์โรส → ชูโรส (common menu spelling); cv-10: เพรทเซลนุ่ม → เพรตเซลนุ่ม (standard transliteration)
- Checked, no change: gems อัญมณี (uiText + 5 gem trophies, consistent, no jewel leftovers), Gold Stars ดาวทอง, getFor แลกด้วย {n}, Map แผนที่ผจญภัย / กลับไปที่แผนที่, Defender ผู้ปกป้อง (distinct from boss ผู้พิทักษ์), Wide Halo รัศมีกว้าง, serverAsks พนักงานถามว่า, verseOfDay, unlocksZoneRight, ph-03 thDef นอนบนนี้ (mockup fix already live)
- Flagged by: Instructor

## 2026-10-30 ~8:00 PM PT, daily-verse Thai glosses (new, not corrections), Instructor; all NEEDS NANCY
- Where: v520/instructor-q0757-verse-glosses.json (days 11-40 + Psalm 86:15; 1 John 4:8 superseded)
- Rule applied: ทรง whenever God or Jesus is the verb's subject (e.g. พระเจ้าไม่ทรงทิ้งคุณ, พระเยซูไม่ทรงเปลี่ยน: ไม่ goes before ทรง). Neutral helper voice with no ค่ะ/ครับ.
- For Nancy: day 23 uses พระเยซูทรงประทาน (ทรง + ประทาน is common church usage, though ประทาน is already royal); simpler alternative พระเยซูทรงให้สันติสุข.

## 2026-10-30 8:18 PM PT, Q-0758 cycle 1 (Instructor); NEEDS NANCY
- uiText.wearIt: ใส่เลย → ใช้เลย; en "Wear it" → "Use it". It now labels owned Pantry tiles and pets, skies, frames and lanterns (ใส่ = put on clothes). Matches uiText.wearing th กำลังใช้.
- uiText.wearing en "Wearing" → "Using" (Thai unchanged, กำลังใช้).
- Checked, no change: uiText.weaponGift "Bible weapon" / อาวุธจากพระคัมภีร์ (Quartermaster c4): natural and true after Option A, with no ทรง issue.
- Sheet: v520/instructor-q0758-fixes.json; patch v520/instructor_patch_q0758.py
- (cycle 2, 8:22 PM PT) trophy title-golden-chef: เชฟหมวกทอง → เชฟทองคำ. "Gold-hat chef" no longer matches the cream chef-hat v3, and the English is "Golden Chef". Matches ตู้กับข้าวทองคำ. NEEDS NANCY.

## 2026-10-30 9:19 PM PT — t51 loop (base v5-22 cards md5 2022aaac)
- cs-07, sw-07, nm-09, bh-17: added Nancy's ค่ะ to say-it faith lines (bh-29 precedent).
- encouragement[5] "God loves you.": พระเจ้าทรงรักคุณ → พระเจ้าทรงรักคุณครับ (Maxwell's voice, matches [0]-[6]).
- daily verse day 36 Psalm 103:13 thGloss: พระเจ้าทรงรักเหมือนพ่อ → พระเจ้าทรงเมตตาเหมือนพ่อ (compassion, not general love).
- Sign-off list: removed stale day 31 1 John 4:8 item (replaced by Psalm 86:15 earlier).
