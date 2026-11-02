#!/usr/bin/env python3
"""Instructor v2b (QM t-room 00:24: leftmost open blank +14 bug fix kept; spoken-target bar +13 moved to a Maxwell pick, instructor-letter-game-bar-pick.py). R2 ask L, letter game, picture grows (Maxwell t430u ask, t492u pick). Costed as ledger_r2.py
LG_LEAN (+413); two fixes to that line (-7): a right letter fills ITS blank, as on the mock (C_K_), so an
out-of-order right letter is never greyed and the word can always finish; '6 plates' = its letters plus
decoys (3-5 letter words); every used plate greys, as on the sheet. Adds uiText.spellIt; uiText count 97 -> 98 (3 places, 0 chars). No verses.
Base = Shop-renamed 1B 24934ef1 (or 1A fca9ce69). Dry-run unless --apply OUT."""
import hashlib, json, sys
SRC = sys.argv[1]; BASES = {"24934ef11a870ebe381e9923dc31bfdd": "1B+Shop", "fca9ce69a1f1d5e556e8414efc524a18": "1A+Shop"}
t = open(SRC, encoding="utf-8").read(); h = hashlib.md5(t.encode()).hexdigest()
assert h in BASES, "base is not 1B+Shop 24934ef1 or 1A+Shop fca9ce69"; print("base", BASES[h], h)
LG = ("\n- **Letter game (Phonics, once per run; Maxwell t430u):** one 3–5 letter `pic` word from the run is spelled: blanks on "
      "the card, 6 letter plates (its letters plus decoys); a right letter fills its leftmost open blank and the picture, small on the ground, "
      "grows a step; a used plate greys, nothing lost. `uiText.spellIt`. Right = that card's usual reward; grace as 7.1.")
EDITS = [("(ledger `card:<runId>:<index>`).", "(ledger `card:<runId>:<index>`)." + LG),
         ('"bigOrSmall":{"en":"Big or small?","th":"ใหญ่หรือเล็ก"}}', '"bigOrSmall":{"en":"Big or small?","th":"ใหญ่หรือเล็ก"},"spellIt":{"en":"Spell it.","th":"สะกดคำนี้"}}'),
         ("`uiText` (97)", "`uiText` (98)"), ("all 97 `uiText` entries", "all 98 `uiText` entries"), ('"uiTextEntries":97', '"uiTextEntries":98')]
n = t
for old, new in EDITS:
    assert n.count(old) == 1, ("anchor count", old, n.count(old)); n = n.replace(old, new)
j = n[n.index("\n```json\n") + 9:n.rindex("\n```")]; d = json.loads(j)
assert len(d["uiText"]) == d["meta"]["uiTextEntries"] == 98 and d["uiText"]["spellIt"]["th"] == "สะกดคำนี้"
print(f"v2; spec line {len(LG)-1} + newline 1 + uiText.spellIt {len(EDITS[1][1])-len(EDITS[1][0])}; JSON parses, uiText 98")
print(f"chars {len(t)} -> {len(n)} ({len(n)-len(t):+d})")
if len(sys.argv) > 3 and sys.argv[2] == "--apply":
    assert sys.argv[3] != SRC; open(sys.argv[3], "w", encoding="utf-8").write(n); print("wrote", sys.argv[3], hashlib.md5(n.encode()).hexdigest())
