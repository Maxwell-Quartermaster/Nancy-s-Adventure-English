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
    spec = [('TPV ask-card phrasings rotate (t427u)', "reads `uiText.tapPrompt` ({word} = `en` in both lines, never `th`) when",
             "reads `uiText.tapPrompt`, then in turn each `|` part of `uiText.tapPromptMore` (ask k of the run uses phrase k mod %d, so one never comes twice in a row; `uiText.tapPromptPlural` when the card has `plural:true`, a plural noun) ({word} = `en` in both lines, never `th`) when" % len(ph))]   # anchor follows instructor-ask-en-both
    return ui, spec
# Auditor glitch hunt 47d0b89c (4:28 PM MDT): patches g1-g9 read from v608build/patches (text-anchored EDITS, applied once each through R), plus R1 and A1 (text only)
def _ag():
    import glob, os
    out = []
    for p in sorted(glob.glob(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'patches', 'auditor-g[1-9]-*.py'))):
        src = open(p, encoding='utf-8').read(); ns = {}
        exec(src[src.index('EDITS='):src.index('\n', src.index('EDITS='))], ns)
        out += [('AG ' + os.path.basename(p)[:-3], a, b) for a, b in ns['EDITS']]
    return out
AG = _ag() + [
    ('AG R1 a scene resumes with its earlier targets done', 'A kill on a reveal resumes on that reveal with no new award.', 'A kill on a reveal resumes on that reveal with no new award. A scene resumes with its earlier targets done.'),
    ('AG A1 Map arrow: the run id carries its local date (after G1)', '`round:<roundId>`, `run:<runId>`, `buy:<id>`', '`round:<roundId>`, `run:<local date>:<runId>`, `buy:<id>`'),
    ('AG A1 Map arrow counts today\'s run: ids', 'else the fewest runs today', 'else the fewest runs today (today\'s `run:` ids)')]
# Instructor sweep 2 (9a7e52d9, verified on c7632e33 = the 4:29 PM MDT working PASTE with AG): six patches read from v608build/patches (E lists, text-anchored)
def _in2():
    import os
    sp, cd = [], []
    for n in ('instructor-ask-en-both', 'instructor-kitchen-tap', 'instructor-color-ask', 'instructor-thai-cs07-sw11', 'instructor-guardian-case', 'instructor-ms04-hint'):
        src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'patches', n + '.py'), encoding='utf-8').read()
        i = src.index('\nE = ['); j = src.index('\nrun(E', i); ns = {}; exec(src[i:j], ns)
        for a, b, where in ns['E']:
            (cd if where == 'both' else sp).append(('IN ' + n, a, b))
    return sp, cd
IN_SPEC, IN_CARDS = _in2()
# Chancellor fun/flow sweep 5da6f734 (4:31 PM MDT): patches C1 newcap (parent: yes, cap 8), C2 firstrun, C3 arrowtie (pairs with AG A1), C4 cssdefaults (cards tex, so the PASTE gets it through the embedded JSON); plus plain fixes a-d
def _ch():
    import os, ast
    sp, cd = [], []
    for n in ('chancellor-newcap', 'chancellor-firstrun', 'chancellor-arrowtie', 'chancellor-cssdefaults'):
        src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'patches', n + '.py'), encoding='utf-8').read()
        i = src.index('EDITS = ['); j = src.index('\n]\n', i) + 2
        for a, b in ast.literal_eval(src[i + 8:j]): (cd if n.endswith('cssdefaults') else sp).append(('CH ' + n, a, b))
    return sp, cd
CH_SPEC, CH_CARDS = _ch()
CH_SPEC += [
    # (a) grace: a miss on a question screen costs nothing (Chancellor test 6). Overlaps Auditor G4: G4 stays for the scene rule, only its now-doubled "no coin off, " is trimmed (one edit, not two)
    ('CH a :216 a miss keeps every coin', 'the meter removes one filled coin if any are filled (none in Baby and Hospital; at 0 nothing changes; no dimming; the rest stay full bright)', 'the meter keeps every coin (a miss costs nothing; no dimming)'),
    ('CH a :216 two-answer line', 'The two-answer card is the exception: a wrong tap there never removes a coin or XP (section 8.1).', 'No miss removes a coin or XP (section 8.1 too).'),
    ('CH a 8.1 no longer an exception', "No coin is removed and no XP is lost (the exception to section 7's coin rule).", 'No coin is removed and no XP is lost (as in section 7).'),
    ('CH a test line', 'a miss removes one filled coin if any (none in Baby and Hospital; at 0 nothing changes); no dimming.', 'a miss keeps every coin; no dimming.'),
    ('CH a / AG G4 one edit: G4 keeps its scene rule, the doubled coin clause goes', 'No timer, nothing lost: no coin off, no return (rule 4 is for question screens).', 'No timer, nothing lost: no return (rule 4 is for question screens).'),
    # (b) ramp: an explicit order rule, not file order
    ('CH b never-seen cards come fewest words first', 'at most 8 never-seen (`seen`) once the zone has 7 seen', 'at most 8 never-seen (`seen`, fewest `en` words first) once the zone has 7 seen'),
    # (c) what comes after the Echo Knight recap
    ('CH c Echo Knight recap ends like a round', 'recaps 10 pairs, no failure;', 'recaps 10 pairs, no failure, and ends like a round;'),
    # (d) ring text for the three untiered weapons, and where Sunforged sits
    ('CH d rings for untiered weapons', 'rings by rank (common 1, rare 3, legendary 5 + glint)', 'rings by rank (common 1, rare 3, legendary 5 + glint; untiered Bloodtide, Dragonbane, Sunforged ring as legendary)'),
    ('CH d Sunforged has a place in the rows', 'free gifts Bloodtide and Dragonbane sit beside the Greatsword row', 'free gifts Bloodtide, Dragonbane and Sunforged sit beside the Greatsword row')]
# Watchman glitch hunt 73b6d48f (checked on 476f0b65), parent ruling 4:42 PM MDT: the six cheap correctness scripts as written;
# W1 scene-apart and W2 count-prop in a leaner wording that does the same job; W10 parent ruling: Kitchen say-it cards follow :226 (scene targets);
# plus the backup restore keeps her hero and giftGems (and zoneRuns) when a backup lacks them.
def _wg():
    import os, ast
    out = []
    for n in ('watchman-welcomeback-key', 'watchman-region-once', 'watchman-level20-bar', 'watchman-tod-steps', 'watchman-bigsmall-card', 'watchman-frontdesk-scene'):
        src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'patches', n + '.py'), encoding='utf-8').read()
        i = src.index('EDITS = ['); j = src.index('\n', i)
        for a, b in ast.literal_eval(src[i + 8:j]): out.append(('WG ' + n, a, b))
    return out
WG = _wg() + [
    ('WG W1 scene-apart (lean): look-alike groups never share a scene', 'Its Thai wraps, never cut or shrunk.', 'Never in one scene (one waits): ph-02/25/26, cs-08/17/18, cs-02/09/20, cs-11/16, cs-15/19, cs-01/03, cs-04/21/22, bh-12/16/21/28/31, ms-19/20. Its Thai wraps, never cut or shrunk.'),
    ('WG W2 count-prop (lean)', 'the right word and two other number words.', 'the right word and two other number words. Scenery copies of the prop hide; it and Big or small are never the spoken target.'),
    ('WG W10 Kitchen say-it cards are scene targets (:226 wins, parent ruling)', 'A Kitchen say-it card with `pic` opens picture-first: picture and Thai; a tap on `uiText.continue` shows the English.', 'A Kitchen say-it card with `pic` is found in its scene, then shows English-first.'),
    ('WG restore keeps hero and giftGems', 'all keys but `giftGems`, `hero` and `zoneRuns`)', 'all keys but `giftGems`, `hero` and `zoneRuns`; those missing keep hers)')]
# Watchman re-walk b365ef8f (on snap-1700MDT, 5:12 PM MDT): r2 patches fold into the WG b-strings (same final text as the scripts; staged chain 7374cc6f -> 95a4d0fc with recheck F1/F2):
# scene-apart-r2 +69 (size balls, digit pictures, tom yum), auditor-r1-countit-wording 7cfa3a7f 0 ("Count it, Big or small: never the spoken target"; count-prop-r2 dropped 5:17 PM MDT), frontdesk-r2 +8 (only front desk cards in that scene, repeats filling it)
def _wg2():
    import os, ast
    eds = []
    for n in ('watchman-scene-apart-r2', 'watchman-frontdesk-r2', 'auditor-r1-countit-wording'):
        src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'patches', n + '.py'), encoding='utf-8').read()
        i = src.index('EDITS'); i = src.index('[', i); j = src.index('\n', i); eds += [tuple(e) for e in ast.literal_eval(src[i:j])]
    out = []
    for t, a, b in WG:
        for o, n_ in eds:
            if o in b: b = b.replace(o, n_); t = t + ' + r2'
        out.append((t, a, b))
    assert sum(t.endswith(' + r2') for t, a, b in out) == 3
    return out
WG = _wg2()

# Auditor recheck 43b4b669 (5:17 PM MDT, parent): F1 run ids carry the zone and a Sound Duel round writes one (+40); F2 region:<id> in the ledger id list (+15).
# Folded into the AG A1 b-strings so every pin follows the final text.
_RC = [("`run:<local date>:<runId>`, `buy:<id>`", "`run:<local date>:<zone>:<runId>`, `buy:<id>`, `region:<id>`"), ("(today's `run:` ids)", "(today's `run:` ids; a Sound Duel round writes one too)")]
def _rc():
    out = []
    for t, a, b in AG:
        for o, n_ in _RC:
            if o in b: b = b.replace(o, n_); t = t + ' + recheck F1/F2'
        out.append((t, a, b))
    assert sum('recheck' in t for t, a, b in out) == 2
    return out
AG = _rc()
