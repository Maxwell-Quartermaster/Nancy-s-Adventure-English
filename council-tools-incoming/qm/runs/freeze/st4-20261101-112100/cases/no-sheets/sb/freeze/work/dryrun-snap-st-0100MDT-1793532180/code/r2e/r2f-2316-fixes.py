# r2f-2316 gate fixes. Auditor, Oct 31 2026 MDT. NOT APPLIED. Sheet text only; 0 PASTE chars each.
# Default run is a dry run (anchor + md5 check). QM applies with --apply, then re-renders the two sheets + QUEUE/INDEX and re-freezes.
import sys, hashlib
B = '/workspace/v608build/round2/'
OLD_R = "chars left = room for later English changes; Nancy's Nov 7 Thai fixes use the separate 300-char reserve (188,200 to 188,500)."
NEW_R = "chars left = room for later changes, English or new Thai; Nancy's Nov 7 Thai sign-off fixes use the separate 300-char reserve (188,200 to 188,500)."
FIX = [
 # F1: C'-open also covers the thinking plate (occl: 🤔 covered 9/9 at 320 and 375x667, frozen and br); B's tile names the plate, C' must too.
 (B + 'r2d/sheet_jesus26_abcd.py', 'fd8d354eb3601c03f59b2ef4746b70d1',
  "the verse opens over the scene and covers the heroes' heads {U6}.",
  "the verse opens over the scene and covers the heroes' heads and the picture plate {U6}."),
 (B + 'r2e/make_queue_r2e.py', '662a8ae6025b84d1faf5350fad1e2445',
  "the opened verse covers the heroes' heads, the only option besides A that covers a head;",
  "the opened verse covers the heroes' heads and 🤔, the only option besides A that covers a head;"),
 # F2: the bank also pays for new Thai (asks' Thai is in their cost; Chancellor v5-28 :83 'new ... Thai keys come from under 188,200'); only Nancy's sign-off fixes use the reserve.
 (B + 'r2d/r2_fit_table.py', '80c1d27d9a3ed72c2c5b22cbdbbf2c84', OLD_R, NEW_R),
 (B + 'r2e/make_queue_r2e.py', None, OLD_R, NEW_R),
 (B + 'r2e/index_r2e.py', '526d06047d40b82c0bd44d3b96d8f96e', OLD_R, NEW_R),
]
apply = '--apply' in sys.argv
for p, md5, old, new in FIX:
    s = open(p, encoding='utf-8').read()
    if md5 and hashlib.md5(s.encode()).hexdigest() != md5: print('md5 drift', p)
    n = s.count(old); print(('OK ' if n == 1 else 'ANCHOR x%d ' % n) + p.split('/')[-1] + ': ' + old[:60])
    if apply and n == 1: open(p, 'w', encoding='utf-8').write(s.replace(old, new))
