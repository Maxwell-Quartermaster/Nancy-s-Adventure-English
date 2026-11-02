
## Chancellor, Oct 31 2026
- Hand-added budget rows went wrong again and again: 170 vs 171, sentence cards at ~80 instead of 309-329, the C row called a dead end, the B1 B combination missed, no-ramp rows missed. Fix: every fit and budget answer now comes from council-tools/fit-table (costs.json + self-test), never mental math.
- I agreed to the all-rooms trim because it was cheaper. Cheaper never makes it the council's call: if a change touches an approved screen, it goes to Maxwell as a neutral pick.

## Instructor, Oct 31 2026 ~11:00 PM MT
- I put "swap long verses" (verse option B) on a pick sheet, which broke the verse guard (verses are free gifts: never drop, swap or reorder to save chars). Fix: before any sheet option goes out, I check that it doesn't touch a verse; any that do are removed, not costed.
- My Thai diff counted runs only, so a Thai string moving to another card would have read clean. Fix: thai-diff now also compares per JSON key, and its self-test plants a moved string.

- Chancellor, Oct 31 23:16 MDT: Proposed a row note ("little room for Nancy's fixes") without checking where her fixes are paid from; the 188,200-188,500 reserve already covers them (must-do.md:77, :86). Fix: before any budget note, check which pool pays for it.
- Chancellor, Oct 31 23:26 MDT: Cited must-do.md:77 for the reserve, but that line is the old 1,500 reserve under the 190,000 cap. Fix: when citing a budget line, check that it is from the current ceiling era.

## Watchman, Nov 1 2026 ~12:30 AM MDT (ground-check)
- My first tree test called the Guardian's armour a "floating tree": canopy tone #489B3B is within tolerance of grass #36A13D, so any green nearby counted as a canopy. Then 1 px swing-set legs at sheet scale counted as trunks. Fix: the canopy needs both #7ECA72 and #28792D (and grass is masked out), and a trunk is at least 2 px wide. The self-test now plants a lifted tree whose own grass is cut away, because my first plant carried its grass strip with it and passed.
- A pixel tool can't see a dimmed scene (tile 25 under the pause card read PASS while its HTML still draws the stroke and the floating tree). Fix: the README lists the blind spots, and I report those tiles as "unverified", never as PASS.
