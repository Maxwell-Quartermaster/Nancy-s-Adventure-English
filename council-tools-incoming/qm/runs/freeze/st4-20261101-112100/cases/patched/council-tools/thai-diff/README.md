# thai-diff (owner: Instructor)
What: lists every Thai run added or removed between BASE and NEW, and for JSON (cards) every key whose Thai changed, so a string that moves to another card is caught.
Run: `python3 thai_diff.py --selftest` first, then `python3 thai_diff.py BASE NEW --manifest MANIFEST.md5`.
First line prints the tool md5, MANIFEST md5, base md5 and new md5.
Writes: stdout only, no temp files. Exit 0 = no Thai change, 1 = changed, 2 = selftest fail.
Self-test plants: a tone mark change, an added run, a moved string, and a typo next to punctuation. All four must be caught, and the clean case must be clean.
Blind spots: can't see Thai drawn in rendered images (sheets need a tile-by-tile visual check); in non-JSON files (PASTE) a moved string isn't caught, only counts; it judges change, not correctness (every new string is still NEEDS NANCY).
