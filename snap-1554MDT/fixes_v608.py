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
 ('VP10 uiText count', "`uiText` (92)", "`uiText` (93)"),
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
