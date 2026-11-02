# r2g-2326 gate fix. Auditor, Oct 31 2026 MDT. NOT APPLIED. QUEUE text only (no image), 0 PASTE chars.
# Dry run by default; QM applies with --apply, regenerates QUEUE (make_queue_r2e.py) and re-freezes.
import sys, hashlib
P = '/workspace/v608build/round2/r2e/make_queue_r2e.py'; MD5 = '050fe2717ec6f29826f8f68476ddfa15'
OLD1 = "- Code/comment fix: screens/play_v608.py tplate() draws the plate at sz=104 pt, but its comment says 'framed 124 pt plate' (PASTE :246 says 124 pt). Make the two agree in v6-09 (decide which number is meant); no render or PASTE change now."
NEW1 = "- Open question for v6-09: the guardian-run picture plate (screens/play_v608.py tplate()) is drawn at 104 pt, but its code comment says 'framed 124 pt plate'. PASTE :246's 124 pt is for the 8.1 two-answer reveal picture only; the PASTE gives no size for the guardian plate. Which size is meant: 104 (as in the approved renders) or 124? No render or PASTE change now."
OLD2 = "would sit under the top-right reveal plate spot (:246, design 262-366 x 234-338, 32 pt overlap) if that plate were ever drawn on a zone scene. Today no zone scene draws it."
NEW2 = "would sit under tplate()'s top-right spot (play_v608.py:116-118, design 262-366 x 234-338, 32 pt overlap) if that plate were ever drawn on a zone scene. Today only guardian runs draw it, and they have no scene targets."
s = open(P, encoding='utf-8').read()
if hashlib.md5(s.encode()).hexdigest() != MD5: print('md5 drift', P)
for o, n in ((OLD1, NEW1), (OLD2, NEW2)):
    print(('OK ' if s.count(o) == 1 else 'ANCHOR x%d ' % s.count(o)) + o[:60]); s = s.replace(o, n) if s.count(o) == 1 else s
if '--apply' in sys.argv: open(P, 'w', encoding='utf-8').write(s)
