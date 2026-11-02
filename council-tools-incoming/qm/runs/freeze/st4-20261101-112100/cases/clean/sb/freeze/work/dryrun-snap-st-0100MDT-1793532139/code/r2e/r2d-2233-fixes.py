# r2d-2233 gate fixes. Auditor, Oct 31 2026 MDT. NOT APPLIED. Sheet-text only; PASTE cost 0 chars for every fix.
# Run by QM only: python3 r2d-2233-fixes.py --apply   (default is a dry run that only checks the anchors)
import sys
B = '/workspace/v608build/'
FIX = [
 # R1: screen 26 tile wording neutral: D's limit in lowercase, and B gets the same visible-Thai figure (dfit 320: B box 125-259, 2 full Thai lines need 256).
 (B + 'round2/r2d/sheet_jesus26_abcd.py', 'a2a287c1473f3b97155f769e19e92d6d',
  "Two full Thai lines do NOT fit above Sam at 320 (37 pt short; about 1 Thai line shows before scrolling)",
  "Two full Thai lines do not fit above Sam at 320 (37 pt short; about 1 Thai line shows before scrolling)"),
 (B + 'round2/r2d/sheet_jesus26_abcd.py', None,
  "it covers the picture plate {U6}.'",
  "it covers the picture plate {U6}. At 320 two full Thai lines show before scrolling.'"),
 # R2: D2 question still leans with 'keep'.
 (B + 'decisions/b2b/sheets_b2b.py', '2e4ebdd4cdffc9c0906c64960399e4ca',
  'A keep one, B two from step 3, or C a steady ramp?',
  'A one, B two from step 3, or C a steady ramp?'),
]
import hashlib
apply = '--apply' in sys.argv
for p, md5, old, new in FIX:
    s = open(p).read()
    if md5 and hashlib.md5(s.encode()).hexdigest() != md5 and not apply: print('md5 drift', p)
    n = s.count(old); print(('OK ' if n == 1 else 'ANCHOR x%d ' % n) + p.split('/')[-1] + ': ' + old[:50])
    if apply and n == 1: open(p, 'w').write(s.replace(old, new))
# Then re-render sheets/jesus-words-26-320-A-B-C-D.png and pick-sheets-b2b/D2-listen-ramp-A-B-C-staged.png and re-freeze.
