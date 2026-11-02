# r2e: INDEX.md for the r2e send, from the r2d INDEX (the five showcase sheets are byte-identical to r2d, so their md5 lines stay true).
# Fixes Auditor r2d L4 (screen 48 was "tile 25" in sheet 5 and "tile 26" in the checks line; the numbering gives 25) and adds the timing lines.
# Usage: python3 index_r2e.py <snapshot name>   (writes round2/showcase/INDEX.md; deletes nothing)
import sys, re
SN = sys.argv[1]; R = '/workspace/v608build/snap-r2d-2233MDT/showcase/INDEX.md'; O = '/workspace/v608build/round2/showcase/INDEX.md'
s = open(R, encoding='utf-8').read()
assert s.count('- **25**: Back after a pause: one Continue button. (48-continue-after-pause.html)') == 1 and s.count('(tile 26, screen 48,') == 1
s = s.replace('(tile 26, screen 48,', '(tile 25, screen 48,')
old = 'From the staged round 2 build (round2d, frozen as v608build/snap-r2d-2233MDT:'
assert s.count(old) == 1
s = s.replace(old, f'From the staged round 2 build (round2d tiles and sheets, frozen as v608build/snap-r2d-2233MDT and carried unchanged into v608build/{SN}; this INDEX is the r2e copy:')
add = ['## Timing for the round 2 picks (r2e)',
       "- Maxwell's R2 pick and screen 26 pick need to land by Nov 2 (freeze Nov 4, 11:59 PM). If they slip past Nov 3, there is no R2 ask in this paste and v6-09 picks it up.",
       '- Writing and Thai-checking time (Instructor): state pairs about 1 hour, letter game about 2 hours. Every new string goes on Nancy\'s Nov 7 list either way.',
       "- No chars are held back. Every fit row shows its chars left; rows with under 20 left are marked \"under 20 left: little room for Nancy's Nov 7 wording fixes\". Nancy's Nov 7 Thai wording fixes draw on the 300-char Thai reserve (188,200-188,500).", '']
i = s.index('## Checks on every tile'); s = s[:i] + '\n'.join(add) + '\n' + s[i:]
open(O, 'w', encoding='utf-8').write(s); print(O)
