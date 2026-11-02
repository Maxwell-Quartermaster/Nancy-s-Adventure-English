#!/bin/bash
# r2f (council 11:15 PM MDT): reserve wording settled; under-20 marks removed; README reserve line. Made from freeze_r2e.sh, base snap-r2e-2313MDT.
# Was r2e: Auditor r2d-2233 gate fixes (patch 10dbcc02 applied) + the r2e delta (C' head note, INDEX tile 25, timing lines, under-20 notes, fit table bank from
# the PASTE length, D2 mock evidence, C' chip line-break test). Made from freeze_r2d.sh: freeze snap-r2e-<HHMM>MDT (read-only) from the round2 working copy.
# Copies only; deletes nothing. Unchanged r2d files are carried byte for byte from snap-r2d-2233MDT; only the sheets this delta changes are re-rendered.
set -e
export PYTHONPATH=/tmp/qmtmp/r2e/shim   # no-delete shim (every delete call is logged and skipped)
HM=$(TZ=America/Denver date +%H%M); NOW=$(TZ=America/Denver date '+%-I:%M %p MDT'); SN=snap-r2f-${HM}MDT; export NAE_SNAP=$SN
B=/workspace/v608build; R=$B/round2; E=$R/r2e; P=$B/snap-r2e-2313MDT; S=$B/$SN; L=/tmp/qmtmp/r2e
[ -e $S ] && { echo "exists $S"; exit 1; }
# 1. re-render only what the delta changes (footers name the new snapshot)
(cd $R/r2d && python3 sheet_jesus26_abcd.py > $L/frz_abcd.log 2>&1)
(cd $R/r2d && python3 r2_fit_table.py --paste $R/staged/nancys-adventure-english-v6-08-PASTE.md --paste $R/trim-1B/staged/nancys-adventure-english-v6-08-PASTE.md --md $R/r2d/sheets/r2-fit-table.md --check /workspace/chancellor/r2-fit-table-20261031-2227MT.md > $R/r2d/sheets/r2-fit-table-check.txt)
(cd $R/sheets && python3 sheet_pick_combined.py > $L/frz_pc.log 2>&1)
python3 $E/index_r2e.py $SN > $L/frz_index.log
python3 $E/make_queue_r2e.py $SN "$NOW"
# 2. the snapshot: r2d carried, then the r2e files over it
mkdir -p $S; cp -a $P/. $S/; chmod -R u+w $S
cp $R/r2d/sheets/jesus-words-26-320-A-B-C-D.png $R/r2d/sheets/r2-fit-table.md $R/r2d/sheets/r2-fit-table-check.txt $R/sheets/pick-combined-trim-ask-verse.png $S/sheets/
cp $R/showcase/INDEX.md $S/showcase/; cp $B/polish-r1/QUEUE.md $S/QUEUE.md; cp $B/README.md $S/README-v608build.md
cp $R/r2d/sheet_jesus26_abcd.py $R/r2d/r2_fit_table.py $R/sheets/sheet_pick_combined.py $S/code/
cp $E/index_r2e.py $E/make_queue_r2e.py $E/freeze_r2f.sh $S/code/r2e/
# 3. renders manifest (same list as r2d, plus the r2e render dirs), DELTA, MANIFEST, read-only
(cd /workspace && { find screens-v608/html screens-v608/png -type f; find v608build/scenes/stage/html v608build/scenes/stage/png -type f; find v608build/round2/ceiling-cap v608build/round2/sky-options/B v608build/round2/r2c/g26 v608build/round2/r2d/g26d v608build/round2/showcase/tiles v608build/scenes/tod v608build/round2/r2e/g26e v608build/round2/r2e/d2 -type f \( -name '*.png' -o -name '*.html' \); } | sort | xargs md5sum) > $S/renders-MANIFEST.md5
python3 - "$P" "$S" "$SN" "$NOW" <<'PY'
import sys, hashlib, os
P, S, SN, NOW = sys.argv[1:]
old = dict((l.split()[1], l.split()[0]) for l in open(P + '/MANIFEST.md5'))
new = {}
for root, ds, fs in os.walk(S):
    for f in fs:
        p = './' + os.path.relpath(os.path.join(root, f), S)
        if p not in ('./MANIFEST.md5', './DELTA.md'): new[p] = hashlib.md5(open(os.path.join(root, f), 'rb').read()).hexdigest()
ch = sorted(p for p in new if p in old and new[p] != old[p]); nw = sorted(p for p in new if p not in old); gone = sorted(p for p in old if p not in new)
L = [f'# DELTA: {SN} vs snap-r2e-2313MDT (MANIFEST f0cc3c1b2e25f0d26bf43e6b4b96570e)', '', f'Frozen {NOW}, Oct 31, 2026. Copies only; nothing deleted. PASTE 1A/1B, FINAL, spec, cards, verses, title, round2.py and checks_v608.py are byte-identical to r2e.', '',
     f'Changed: {len(ch)}. New: {len(nw)}. Gone: {len(gone)}. Same: {len([p for p in new if p in old and new[p] == old[p]])}.', '', '## Changed (old md5 -> new md5)', '']
L += [f'- {p}: {old[p]} -> {new[p]}' for p in ch] + ['', '## New', ''] + [f'- {p}: {new[p]}' for p in nw] + ['', '## Gone', ''] + ([f'- {p}: {old[p]}' for p in gone] or ['- none']) + ['']
open(S + '/DELTA.md', 'w').write('\n'.join(L)); print(f'DELTA: {len(ch)} changed, {len(nw)} new, {len(gone)} gone')
PY
(cd $S && find . -type f ! -name MANIFEST.md5 | sort | xargs md5sum > MANIFEST.md5)
chmod -R a-w $S
echo "$SN frozen at $NOW; MANIFEST $(md5sum $S/MANIFEST.md5 | cut -c1-32), $(wc -l < $S/MANIFEST.md5) files; renders-MANIFEST $(md5sum $S/renders-MANIFEST.md5 | cut -c1-32) $(wc -l < $S/renders-MANIFEST.md5) lines"
