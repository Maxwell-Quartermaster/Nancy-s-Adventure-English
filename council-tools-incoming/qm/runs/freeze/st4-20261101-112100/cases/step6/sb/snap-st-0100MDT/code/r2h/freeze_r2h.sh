#!/bin/bash
# r2h freeze (Nov 1 2026). Made from freeze_r2g.sh, base snap-r2g-2326MDT. Copies only; deletes nothing.
# Adds: r2h/ (staged 1B PASTE layers + 1A Shop files kept, EDITS.json, FIXLOG, fix/render/sheet code, r2h renders html+png, sheet + sources),
# Auditor r2g-2326-fixes.py applied to make_queue_r2e.py (QUEUE regenerated). Root PASTE, trim-1B PASTE, cards, verses, title: byte-identical to r2g.
set -e
export PYTHONPATH=/tmp/qmtmp/r2e/shim
HM=$(TZ=America/Denver date +%H%M); NOW=$(TZ=America/Denver date '+%-I:%M %p MDT'); SN=snap-r2h-${HM}MDT; export NAE_SNAP=$SN
B=/workspace/v608build; R=$B/round2; E=$R/r2e; H=$R/r2h; P=$B/snap-r2g-2326MDT; S=$B/$SN
[ -e $S ] && { echo "exists $S"; exit 1; }
python3 $E/make_queue_r2e.py $SN "$NOW"
mkdir -p $S; cp -a $P/. $S/; chmod -R u+w $S
cp $B/polish-r1/QUEUE.md $S/QUEUE.md
mkdir -p $S/r2h $S/code/r2h $S/renders/r2h
cp -a $H/staged $S/r2h/; cp $H/FIXLOG.md $S/r2h/; cp -a $H/sheets $S/r2h/
cp $H/fix_r2h.py $H/render_r2h.py $H/cdp_shot.py $H/stage_r2h_paste.py $H/sheet_r2h.py $H/freeze_r2h.sh $S/code/r2h/
cp $E/make_queue_r2e.py /workspace/audit/patches/r2g-2326-fixes.py /workspace/v608build/patches/instructor-shop-rename.py $S/code/r2e/
cp -a $H/html $H/png $S/renders/r2h/
(cd /workspace && { find screens-v608/html screens-v608/png -type f; find v608build/scenes/stage/html v608build/scenes/stage/png -type f; find v608build/round2/ceiling-cap v608build/round2/sky-options/B v608build/round2/r2c/g26 v608build/round2/r2d/g26d v608build/round2/showcase/tiles v608build/scenes/tod v608build/round2/r2e/g26e v608build/round2/r2e/d2 v608build/round2/r2h/html v608build/round2/r2h/png v608build/round2/r2h/sheets -type f \( -name '*.png' -o -name '*.html' \); } | sort | xargs md5sum) > $S/renders-MANIFEST.md5
python3 - "$P" "$S" "$SN" "$NOW" <<'PY'
import sys, hashlib, os
P, S, SN, NOW = sys.argv[1:]
old = dict((l.split()[1], l.split()[0]) for l in open(P + '/MANIFEST.md5') if l.split()[1] not in ('./DELTA.md', './MANIFEST.md5'))
new = {}
for root, ds, fs in os.walk(S):
    for f in fs:
        p = './' + os.path.relpath(os.path.join(root, f), S)
        if p not in ('./MANIFEST.md5', './DELTA.md'): new[p] = hashlib.md5(open(os.path.join(root, f), 'rb').read()).hexdigest()
ch = sorted(p for p in new if p in old and new[p] != old[p]); nw = sorted(p for p in new if p not in old); gone = sorted(p for p in old if p not in new)
L = [f'# DELTA: {SN} vs snap-r2g-2326MDT (MANIFEST 3bee8d986541c795edc6e5cf020f2ac8; DELTA.md itself excluded)', '', f'Frozen {NOW}, Nov 1, 2026. Copies only; nothing deleted. Root PASTE (1A 106a0661) and trim-1B PASTE (2eebff94) are byte-identical to r2g; the r2h PASTE candidates (base 1B, Maxwell t492u) are in r2h/staged/1B.', '',
     f'Changed: {len(ch)}. New: {len(nw)}. Gone: {len(gone)}. Same: {len([p for p in new if p in old and new[p] == old[p]])}.', '', '## Changed (old md5 -> new md5)', '']
L += [f'- {p}: {old[p]} -> {new[p]}' for p in ch] + ['', '## New', ''] + [f'- {p}: {new[p]}' for p in nw] + ['', '## Gone', ''] + ([f'- {p}: {old[p]}' for p in gone] or ['- none']) + ['']
open(S + '/DELTA.md', 'w').write('\n'.join(L)); print(f'DELTA: {len(ch)} changed, {len(nw)} new, {len(gone)} gone')
PY
(cd $S && find . -type f ! -name MANIFEST.md5 | sort | xargs md5sum > MANIFEST.md5)
chmod -R a-w $S
echo "SN=$SN NOW=$NOW MANIFEST=$(md5sum $S/MANIFEST.md5 | cut -c1-32) FILES=$(wc -l < $S/MANIFEST.md5) RMAN=$(md5sum $S/renders-MANIFEST.md5 | cut -c1-32) RLINES=$(wc -l < $S/renders-MANIFEST.md5)"
