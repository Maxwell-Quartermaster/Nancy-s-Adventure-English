# v6-08 fixes on v6-07 (frozen at the Auditor gate). Each pair is replaced exactly once.
# A1 (council 3:25 PM MDT): the 7.1 ask-card rule produced 'Where is the Wash the baby.?' (31 cards) and 'Where is the a white towel?' (5 cards).
A1 = ("for a 1–3 word `en`, else the card's own `en`",
      "when `en` is 1–3 lower-case words with no . , ? ! and no leading \"a \" and `pic` is not null (not ph-02, ph-07, ph-08, ph-11, ph-17, ph-21, ph-24, cs-22, cs-23, cs-24, sw-15, sw-18, sw-19, sw-24), else the card's own `en`")
# B1 (Auditor v6-07 gate 2b29ce71) + Instructor review 7057dde4 ("and `pic` is not null"); replaces my earlier A1 sketch.
B1_EXCLUDE = ['ph-02', 'ph-07', 'ph-08', 'ph-11', 'ph-17', 'ph-21', 'ph-24', 'cs-22', 'cs-23', 'cs-24', 'sw-15', 'sw-18', 'sw-19', 'sw-24']
# A2 (council 3:25 PM MDT): long Thai (fd-08 croissant) ran past the card at 390; Thai lines in the question card wrap (17 px+, line-height 1.7).
A2 = ("Say-it cards keep Got it after the tap.", "Its Thai wraps, never cut or shrunk. Say-it cards keep Got it after the tap.")
SPEC = [('B1 ask-card rule (Auditor 2b29ce71 + Instructor pic not null)', *A1), ('A2 ask-card Thai wraps', *A2)]
# E1 (Maxwell t398u + 3:27 PM steer): Sam's eyes are dark, thick happy closed arcs everywhere: the shared rig's #rE becomes the arcs (cards), the title Sam's profile eye an arc (title file).
E1_CARDS = ("<g id='rE' stroke='none' fill='#FFF8E1'><ellipse cx='35' cy='20' rx='1.2' ry='.9'/><ellipse cx='45' cy='20' rx='1.2' ry='.9'/><g fill='#10170F'><circle cx='35' cy='20' r='.6'/><circle cx='45' cy='20' r='.6'/></g></g>",
            "<path id='rE' d='M32.6 21q2.4-2.8 4.8 0M42.6 21q2.4-2.8 4.8 0' stroke-width='1.6'/>")   # Maxwell t408u: Nancy's happy eyes exactly (her path, 1.6, Ink by inheritance)
# Nancy keeps her own face snippet byte for byte (gate 2); #rE is a byte-exact copy of her eye path with her 1.6 stroke.
E1_TITLE = ("<g stroke='none'><ellipse cx='48.6' cy='20' rx='1.1' ry='.9' fill='#FFF8E1'/><circle cx='49.1' cy='20' r='.6' fill='#10170F'/></g>",
            "<path d='M46 21q2.4-2.8 4.8 0' stroke-width='1.6'/>")   # title Sam in profile: one of Nancy's arcs, centred in his lens
E1_SPEC = ("Golden Fields ask: Sam's eyes happy closed arcs.", "Sam's eyes are Nancy's happy arcs (shared `#rE`) on every screen (t408u).")
# VP (Maxwell's pick B, 3:35 PM MDT, mocks-verse-popup-t399u/B-390x844.png 89e9811d; t404u/t405u: the title gets no pop-ups). Verses stay byte-identical.
VP = [
 ('VP1 launch order: verse pops up over the main menu', "sword tap → reconcile (11.3) → `rewardQueue` → daily verse if due → run or main menu.",
  "sword tap → reconcile (11.3) → `rewardQueue` → run or main menu; the daily verse, if due, pops up over the main menu (first launch: her first menu visit after the Phonics run); the title never shows a pop-up."),
 ('VP2 no title banner for the daily verse', "Sound Duel `uiText.soundDuel`, daily verse `uiText.verseOfDay`, ", "Sound Duel `uiText.soundDuel`, "),
 ('VP3 + O1 daily verse over the main menu, never the title', "one memory verse a day on her first open each day, titled `uiText.verseOfDay`,",
  "one memory verse a day on her first open each day, over the main menu (never the title, t404u), in the pop-up below,"),
 ('VP4 pop-up B + daily gift', "then at the bottom one small line `uiText.askMax` (\"Don't know a word? Ask Max.\"), then Got it.",
  "then at the bottom one small line `uiText.askMax` (\"Don't know a word? Ask Max.\"), then Got it.\n"
  "- **Daily verse pop-up (Maxwell's pick B, t399u):** a centered parchment card over the main menu (Ink 50% scrim; menu inert): flat gold ribbon `uiText.verseOfDay` (th under), `uiText.verseGift`, ref, `en`, a gold rule, `th`, sources; only the verse body scrolls, the buttons always stay in view; bottom row: a round Replay shield (`uiText.replay` under it) and a wide `gotItText` button in the 6.1 style. Got it closes it.\n"
  "- **Daily gift:** on her first main-menu visit each day, a flat dashed-gold tag (never a button), `uiText.dailyGift` with one small gem, sits above the card (alone on days the verse is already seen); ledger `gift:<local date>`, `giftGems` +1. It never depends on the verse (shown, read or closed) and never gates or boosts it."),
 ('VP5 gift ledger id', "`verse:<local date>`, `unlock:<trophyId>`", "`verse:<local date>`, `gift:<local date>`, `unlock:<trophyId>`"),
 ('VP6 giftGems in state', "pips, streak, settings{slowMode, restWeeks}}", "pips, streak, giftGems, settings{slowMode, restWeeks}}"),
 ('VP7 giftGems only counts up, feeds nothing, missing = 0', "Counters only go up, except `goldStars` (Pantry).",
  "Counters only go up, except `goldStars` (Pantry). `giftGems` feeds no trophy, gem count or gear bonus; missing, it reads 0 (no `schema` change)."),
 ('VP8 restore accepts a save without giftGems', "(JSON, `schema` 5020, all keys)", "(JSON, `schema` 5020, all keys but `giftGems`)"),
 ('VP10 uiText count (93 with dailyGift, 97 with the 4 scene keys)', "`uiText` (92)", "`uiText` (97)"),
 ('VP9 grace check: the gift never touches a verse', "no verse, scroll, or the Scrolls tab is gated on coins, XP spending, gems, or trophies;",
  "no verse, scroll, or the Scrolls tab is gated on coins, XP spending, gems, or trophies; `gift:`/`giftGems` never depend on a verse;"),
]
VP_UI = ('dailyGift', {"en": "Daily gift: +1 gem", "th": "อัญมณีประจำวัน: 1 เม็ด"})   # Thai: Instructor 7057dde4 (ของขวัญ stays for verses only); NEEDS NANCY by meta.thStatusDefault
# H1 (Maxwell t406u, 3:39 PM MDT): hand-only emoji (pray, high five, other hand gestures; Unicode 13.0 or earlier) are fine as emoji; people or bigger
# pictures ("hug territory") are drawn in the library style on the same bordered parchment plate. ms-31's two buttons become 🙏 / 🙌 on 124 pt plates.
H1 = [
 ('H1 two-answer buttons: hand emoji on bordered plates', "two big picture buttons from `choices` (`svg:pray-kneel`, a small kneeling person with folded hands, `uiText.pray`; `svg:high-five`, two hands meeting, `uiText.highFive`; both drawn from `picPlan.svgNotes` in one style, never emoji), at least 120 pt,",
  "two big picture buttons from `choices`, each on a 124 pt bordered parchment plate (Ink edge, Gold inner line): 🙏 `uiText.pray`, 🙌 `uiText.highFive`. Hand-only emoji (Unicode 13.0 or earlier) are fine as emoji; people or bigger pictures (a hug) are drawn from `picPlan.svgNotes` on the same plate, never emoji;"),
 ('H1 svg list note', "`high-five` and `pray-kneel` are also `ms-31`'s two buttons", "`high-five` is kept in the library; `ms-31`'s buttons are hand emoji"),
]
H1_CARDS = {'pray': ('svg:pray-kneel', '🙏'), 'highFive': ('svg:high-five', '🙌')}
# G1 grace fix (council 3:55 PM MDT): tunic-rose word meaning; Thai ความชอบธรรม kept
G1_CARDS = ("Doing what is right in God's eyes", "Right with God as His free gift")
# P1 reveal-picture placement (Maxwell t423u): C (prop on the ground) where it can stand, else A (framed plate top right); hand emoji keep plates (t406u)
P1 = [('P1 reveal pictures: ground prop or top-right plate (t423u)', "people or bigger pictures (a hug) are drawn from `picPlan.svgNotes` on the same plate, never emoji;",
       "people or bigger pictures (a hug) are drawn from `picPlan.svgNotes` on the same plate, never emoji; a reveal picture (t423u) that can stand is a 64 pt prop on the ground with a contact shadow, else a 124 pt framed plate at the top right, never over or beside the hero;")]
# Scene work (Maxwell approved t401u A-H; J by level; council 3:55 PM MDT). Thai: Instructor 7057dde4, all NEEDS NANCY by meta.thStatusDefault.
SC_SCENES = ("also behind Sound Duel.",
 "also behind Sound Duel. "
 "**Time of day (Maxwell: by level inside each zone):** each scene root gets `data-tod`, set at run start from that zone's step, 1 + `zoneRuns[zone]` mod 5 (her finished runs there; a resumed run keeps it), a CSS var swap of sky, ground and light tint (the title's palettes): step 1 `m` morning, 2 `d` midday (the `a` sky lighter), 3 `a`, 4 `e`, 5 `n` night, then `m` again; props, layout and taps never change; Echo Forest at `m`/`d` is the same woods in dawn mist. "
 "Word Meadow alternates a second layout, the park by a pond (swing set left, bench right, pond mid-right); a floating object sits on the pond with a ripple. Every object stands on a surface (ground, bench, desk, shelf, counter) with a contact shadow, sized to the hero, never floating. "
 "**Front desk (Home Lake):** Maxwell Says `ms-03`–`ms-06` and `ms-21`–`ms-23` play in a hotel front desk: the same wall, floor and window; a wood counter across the right (hip high, three front panels); a wall clock; a full-height room door with a gold 13 on the left wall; keys on a wall key rack; a book on a shelf; the truck small and far, half behind the hill in the window. No names or signs. "
 "Kitchen runs use the home room set for a meal: the crib makes way for a small table (cloth, 2 legs), food on the table, desk and shelf.\n"
 "- **Listen and find:** in each scene the 3rd target is spoken only: the card reads `uiText.listenFind` with no word and plays it once; 🔊 replays it. Same taps, reveal and grace.\n"
 "- **Count it (Numbers, once per run):** the scene shows N of one prop (cow, basket, hat), N from a picture number card 2–10; the card reads `uiText.howMany` ({thing} = cows, baskets or hats; cows use `uiText.howManyCows`) with 3 number plates: the right word and two other number words. Right = that card's usual reward; grace as 7.1.\n"
 "- **Big or small (Colors and Shapes, once per run):** the hero holds a `meta.sizeSort` picture on the open palm; two baskets with the `cs-23`/`cs-24` words as tappable plates; she taps the one that fits. `uiText.bigOrSmall`. Grace as 7.1; it awards and resumes as a scene card (ledger `card:<runId>:<index>`).")
SC = [('SC scenes: time by level, meadow pond, front desk, kitchen table, listen, count, big or small', *SC_SCENES),
      ('G picture pairs (section 12)', "she taps the word she heard (English, no pictures).", "she taps the word she heard (English; a pair with `pics` shows each emoji left of its word, 38 pt)."),
      ('G picture pairs (check 3)', "word tiles, no pictures;", "word tiles, pictures only on the 6 `pics` pairs;")]
SC_UI = [('listenFind', {"en": "Listen. Where is it?", "th": "ฟังแล้วหาดู"}), ('howMany', {"en": "How many {thing}?", "th": "นับดู"}),
         ('howManyCows', {"en": "How many cows?", "th": "มีวัวกี่ตัว"}), ('bigOrSmall', {"en": "Big or small?", "th": "ใหญ่หรือเล็ก"})]
SC_SIZE = {"big": ["ph-22", "ms-22", "ph-01"], "small": ["ms-21", "nm-04", "fd-25"]}
SC_PICS = {('ship', 'sheep'): ['🚢', '🐑'], ('card', 'car'): ['💳', '🚗'], ('three', 'tree'): ['3️⃣', '🌳'], ('bath', 'bat'): ['🛁', '🦇'], ('mouth', 'mouse'): ['👄', '🐭'], ('bread', 'bed'): ['🍞', '🛏️']}
# Watchman playtest v6-08 (REPORT 9f88fb02) patches, applied through qm (same edit in FINAL and spec); Auditor P1 count; council round 4:08 PM MDT
WM = [('K1 state record keeps hero and zoneRuns (Auditor gate 1975f0b8 K1/K3; Watchman S1 8e75b04d folded in)', 'pips, streak, giftGems, settings{slowMode, restWeeks}}', 'pips, streak, giftGems, hero, zoneRuns{}, settings{slowMode, restWeeks}}'),
      ('K1 restore checks all keys but giftGems, hero, zoneRuns', '(JSON, `schema` 5020, all keys but `giftGems`)', '(JSON, `schema` 5020, all keys but `giftGems`, `hero` and `zoneRuns`)'),
      ('K2 tier-slot ids <type>-t<t> (Auditor K2; Watchman G1 e08b0fbd reconciled to this one scheme)', "else `tierNames[t]` + type name with the type's `weaponParts` art.", "else `tierNames[t]` + type name with the type's `weaponParts` art and id `<type>-t<t>` (e.g. `axe1-t2`), kept in `owned`/`equipped` like a trophy id."),
      ('K2 cosmetic is a trophy or a tier slot', 'one of the 42 `trophies` (Pantry', 'one of the 42 `trophies` or a tier slot (Pantry'),
      ('M1 reconcile drops ids that no longer exist (no refund until Maxwell picks)', 'Drop duplicate `owned` ids and any `equipped` id not owned', 'Drop duplicate `owned` ids and any id not in `trophies`, tier slots or `pantry.items`, and any `equipped` id not owned'),
      ('U1 section 18 live uiText count (patch auditor-u1-uitext-count.py 863deae1, same as P1 1297be01)', 'all 91 `uiText` entries', 'all 97 `uiText` entries'),
      ('F2 Sight Words: no back-to-back repeat across scenes', 'never twice in one scene.', 'never twice in one scene or as the next scene\'s first ask.'),
      ('F4 tier 1 is given, never "Get it for 0"', '(tier 1 free on opening)', '(tier 1 is hers free when its row opens, no `getFor`)'),
      ('F3 Sound Duel right answers earn stars too', 'Gold Stars per right answer and finished run', 'Gold Stars per right answer (Sound Duel too) and finished run'),
      ('F5 welcome-back before the verse pop-up (Watchman sweep flow gap)', 'Got it closes it.\n- **Daily gift:**', 'Got it closes it. After a missed day `uiText.welcomeBack` shows first, then this.\n- **Daily gift:**')]
TPV_SETS = {'all5': [1, 2, 3, 4, 5]}   # indices into TPV_PHRASES; Maxwell may pick a subset
TPV_PHRASES = [("Where is the {word}?", "{word} อยู่ที่ไหน"), ("Can you find the {word}?", "หา {word} เจอไหม"), ("Show me the {word}.", "ชี้ {word} ให้ดู"),
               ("Find the {word}.", "หา {word} ให้เจอ"), ("Where's the {word}?", "{word} อยู่ที่ไหน")]
TPV_PLURAL = ("Where are the {word}?", "{word} อยู่ที่ไหนบ้าง")
def tpv(set_='all5'):
    ph = [TPV_PHRASES[i - 1] for i in TPV_SETS.get(set_, set_)]
    more = ph[1:]
    ui = [('tapPromptMore', {"en": '|'.join(e for e, t in more), "th": '|'.join(t for e, t in more)}), ('tapPromptPlural', {"en": TPV_PLURAL[0], "th": TPV_PLURAL[1]})]
    spec = [('TPV ask-card phrasings rotate (t427u)', "reads `uiText.tapPrompt` ({word} = `en`) when",
             "reads `uiText.tapPrompt`, then in turn each `|` part of `uiText.tapPromptMore` (ask k of the run uses phrase k mod %d, so one never comes twice in a row; `uiText.tapPromptPlural` when the card has `plural:true`, a plural noun) ({word} = `en`) when" % len(ph))]
    return ui, spec
