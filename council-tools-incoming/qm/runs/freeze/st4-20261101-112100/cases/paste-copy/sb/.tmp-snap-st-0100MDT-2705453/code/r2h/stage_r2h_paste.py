# r2h PASTE staging on 1B (Maxwell t492u). Text swaps only: each anchor must appear exactly once; nothing deleted from disk.
# Order: Instructor Shop patch (d75eaa13) -> Auditor ground line (6c468a7d) -> L lean (+413) -> ramp D2 B -> t464u -> t465u/t487u -> t466u.
import json, hashlib, sys
IN = 'staged/1B/PASTE-shop.md'   # parent 12:18 AM: the ground line is NOT in the PASTE for now (kept in PASTE-shop-ground.md)
s = open(IN, encoding='utf-8').read(); base = len(s); rows = []
def sw(tag, a, b):
    global s
    assert s.count(a) == 1, (tag, s.count(a), a[:50]); n0 = len(s); s = s.replace(a, b); rows.append((tag, len(s) - n0, a, b))
LG = ("- **Letter game (Phonics, once per run; Maxwell t430u):** one 3–5 letter `pic` word from the run is spelled: blanks on the card, 6 letter plates "
      "(its letters and 2 decoys); a right letter fills the next blank and the picture, small on the ground, grows a step; a wrong plate just greys, nothing lost. "
      "`uiText.spellIt`. Right = that card's usual reward; grace as 7.1.")
# R2 L lean (+413 = line 366 + newline 1 + uiText 46)
sw('L lean: spec line', "and plays it once; 🔊 replays it. Same taps, reveal and grace.\n", "and plays it once; 🔊 replays it. Same taps, reveal and grace.\n" + LG + "\n")
sw('L lean: uiText.spellIt', '"listenFind":{"en":"Listen. Where is it?","th":"ฟังแล้วหาดู"},', '"listenFind":{"en":"Listen. Where is it?","th":"ฟังแล้วหาดู"},"spellIt":{"en":"Spell it.","th":"สะกดคำนี้"},')
sw('L lean: uiText count', 'all 97 `uiText` entries', 'all 98 `uiText` entries')
# ramp D2 B (t432u): from the zone's step 3 the 5th target is spoken only too
sw('ramp D2 B', "in each scene the 3rd target is spoken only:", "in each scene the 3rd target (from its zone's step 3, the 5th too) is spoken only:")
open('staged/1B/PASTE-1B-shop-L-ramp.md', 'w', encoding='utf-8').write(s); mark_L = len(s)
# t464u opening flow
sw('t464u title button', "then the button `uiText.letsGo`.", "then one button, `uiText.letsGo` (t464u).")
sw('t464u button place', "wide and low, English and the Thai plate on one line (two lines only if it must wrap); 84% wide (88% at 320 × 568), 60 pt tall, 24 pt (16 pt at 320 × 568) plus the safe-area inset above the bottom;",
   "in 6.2's lowest button slot, clear of the sword, English and the Thai plate on one line;")
sw('t464u tap', "- **Tap** (button or sword):", "- **Tap** (the button):")
sw('t464u launch order', "sword tap → reconcile (11.3) → `rewardQueue` → run or main menu; the daily verse, if due, pops up over the main menu (first launch: her first menu visit after the Phonics run); the title never shows a pop-up.",
   "the daily verse, if due, pops up over the title (t464u); Got it shows the title; its tap → reconcile (11.3) → `rewardQueue` → run or main menu.")
sw('t464u verse rule', "over the main menu (never the title, t404u)", "over the title (t464u)")
sw('t464u verse card', "over the main menu (Ink 50% scrim; menu inert)", "over the title (Ink 50% scrim; title inert)")
mark_464 = len(s)
# t465u + t487u main menu (order: choose your character, Gear, Shop, Adventure Map) and map rows at the bottom
L = s.split('\n'); i = next(k for k, l in enumerate(L) if l.startswith('Exactly two buttons, the hearth (a corner button) and one cue:')); old = L[i]
sw('t465u/t487u main menu', old, "In the Map's look (6.3 header logs, top bar, sky sheet; t465u), top to bottom (t487u): the hero select (6.3's band, moved here), `uiText.gear` (opens Character, 6.6), `uiText.pantry` (the Shop), `uiText.titleMap` (opens the Map); the hearth in its corner and one cue, a Gold arrow bobbing at the Map button's right end (transform only; still with reduced motion). Full-width iron buttons 60 pt tall, 8 pt apart, never over the art. Back returns here.")
sw('t465u hero band', "the Map's hero band shows", "the main menu's hero band shows")
sw('t465u menu check', "The main menu shows exactly two buttons (Map, Character), the corner hearth and the arrow cue.", "The main menu shows the hero select, three buttons (Gear, Shop, Map), the corner hearth and the arrow cue.")
sw('t465u rows at bottom', "Rows start in the lower 60%; on taller screens the spare height goes evenly between rows.", "Rows sit at the bottom, 16 pt above the safe area; spare height stays above them (t465u).")
mark_465 = len(s)
open('staged/1B/PASTE-1B-shop-L-ramp-flow.md', 'w', encoding='utf-8').write(s)
# t466u no chooser, mixed zones per scene
sw('t466u taps', "a row opens its zone, or a chooser with one plate per zone (zone `name`/`nameTh`) when it holds two or three;", "a row opens its region at once (t466u): its scenes take its zones in turn, never two in a row from one;")
sw('t466u home lake', "(its row opens their chooser)", "(its row mixes them)")
sw('t466u hub', "the hub and choosers use", "the hub uses")
sw('t466u time of day', "set at run start from that zone's step", "set per scene from its zone's step")
sw('t466u boss', "a recap after scene 5 of a run in that zone", "a recap after scene 5 of a run in its region")
mark_466 = len(s)
open('staged/1B/PASTE-1B-shop-L-ramp-flow-mix.md', 'w', encoding='utf-8').write(s)   # t466u layer is separable (may defer to v6-09)
for t, d, a, b in rows: print(f'{d:+5d}  {t}')
tot = len(s) - base; print('base', base, 'bank', 188200 - base)
print('L+ramp', mark_L - base, '| t464u', mark_464 - mark_L, '| t465u/t487u', mark_465 - mark_464, '| t466u', mark_466 - mark_465)
print('total', tot, 'chars', len(s), 'md5', hashlib.md5(s.encode()).hexdigest(), 'vs 188,200:', 188200 - len(s))
for f in ('PASTE-1B-shop-L-ramp.md', 'PASTE-1B-shop-L-ramp-flow.md', 'PASTE-1B-shop-L-ramp-flow-mix.md'):
    t = open('staged/1B/' + f, encoding='utf-8').read(); print(f, len(t), hashlib.md5(t.encode()).hexdigest(), 'left', 188200 - len(t))
json.dump([dict(tag=t, delta=d, old=a, new=b) for t, d, a, b in rows], open('staged/1B/EDITS.json', 'w'), ensure_ascii=False, indent=1)
