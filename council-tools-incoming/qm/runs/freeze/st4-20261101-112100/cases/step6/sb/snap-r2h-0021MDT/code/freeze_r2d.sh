#!/bin/bash
# r2d: Auditor r2c-2159 gate H1-H7 folded in. Freeze snap-r2d-<HHMM>MDT (read-only) from the round2 working copy. Copies only; deletes nothing.
set -e
export TMPDIR=/tmp/qmtmp
HM=$(TZ=America/Denver date +%H%M); NOW=$(TZ=America/Denver date '+%-I:%M %p MDT'); SN=snap-r2d-${HM}MDT; export NAE_SNAP=$SN
B=/workspace/v608build; R=$B/round2; S=$B/$SN
[ -e $S ] && { echo "exists $S"; exit 1; }
# footers and queue name the snapshot
python3 - "$SN" <<'PY'
import sys; sn=sys.argv[1]; p='/workspace/v608build/round2/showcase/tour.py'; s=open(p).read()
s=s.replace("(round2c, frozen as v608build/snap-r2c-2159MDT:", f"(round2d, frozen as v608build/{sn}:")
s=s.replace("'Round 2 build, frozen as v608build/snap-r2c-2159MDT (round2c: Auditor r2b-2051 and Instructor fixes).", f"'Round 2 build, frozen as v608build/{sn} (round2d: Auditor r2c-2159 gate fixes).")
assert sn in s and 'snap-r2c-2159MDT' not in s, 'tour text not updated'
open(p,'w').write(s)
PY
(cd $R/sheets && for x in sheet_trim.py sheet_frontdesk.py sheets_r2.py sheet_pick_combined.py; do python3 $x > /tmp/qmtmp/frz_$x.log 2>&1; done)
(cd $R/r2d && python3 sheet_jesus26_abcd.py > /tmp/qmtmp/frz_abcd.log 2>&1 && python3 r2_fit_table.py --md $R/r2d/sheets/r2-fit-table.md --check /workspace/chancellor/r2-fit-table-20261031-2227MT.md > $R/r2d/sheets/r2-fit-table-check.txt)
(cd $B/decisions/b2b && python3 sheets_b2b.py > /tmp/qmtmp/frz_b2b.log 2>&1)
(cd $R/showcase && python3 tour.py > /tmp/qmtmp/tour_freeze.log 2>&1)
python3 $R/r2d/make_queue_r2d.py $SN "$NOW"
mkdir -p $S/{checks,sheets,pick-sheets-b2b,showcase,trim-1B,stage,reports,code,renders/{screens,walk24,guardian-24-28,jesus-26,ceiling-cap-r2ask,home-lake-r2ask,sky-B-r2ask}}
cp $R/staged/* $S/; cp $B/snap-r2b-2051MDT/nancys-adventure-english-v6-08-daily-verses.json $B/snap-r2b-2051MDT/nancys-adventure-english-v6-08-title.svg $S/
cp $R/diff-*.diff $S/; cp $R/trim-1B/staged/* $R/trim-1B/diff-*.diff $S/trim-1B/
cp $R/round2.py $R/asset-depth/round_totals.py $R/asset-depth/COSTS-and-LEDGER.md $R/README.md $S/; cp $B/README.md $S/README-v608build.md; cp $B/polish-r1/QUEUE.md $S/QUEUE.md
cp $R/checks/checks_v608.py /tmp/qmtmp/mktree.sh $R/trimcheck/trim_clip_check.py $S/checks/
for x in $R/sheets/*.png; do case $(basename $x) in jesus-words-26-320-A-B-C.png|sky-A-vs-B*) ;; *) cp $x $S/sheets/;; esac; done; cp $R/r2d/sheets/* $S/sheets/; cp $B/decisions/b2b/{B1-reward-pacing,D1-sentence-ask-thai-A-B-C-staged,D2-listen-ramp-A-B-C-staged,TG1-sight-words-repeats,TG2-verse-after-run,TG3-guardian-recap,TG4-tier3-buy,bloodtide-name,coin-rule,letter-game-A-B,night-title-line,state-pairs-lean}.png $S/pick-sheets-b2b/
cp -r $R/showcase/INDEX.md $R/showcase/*.png $R/showcase/tour.py $R/showcase/tiles $S/showcase/
cp $B/scenes/stage/CHECK.md $S/stage/CHECK.md; cp $B/scenes/stage_v608.py $S/stage/
V=/workspace/screens-v608
for f in 02b-main-menu-verse-popup-longest-320x568 02b-main-menu-verse-popup-longest-320x568-scrolled 02c-menu-gemtag-before-verse 02c-menu-gemtag-before-verse-320x568 18-two-answer-wrong-tap 23-level-up-reward 23-level-up-reward-320x568 29-verse-scroll-gift 30-new-weapon-gift 34-echo-forest-sound-duel-320x568 35-sound-duel-right-320x568 36-sound-duel-round-done 36-sound-duel-round-done-320x568 52-title-night; do cp $V/png/$f.png $S/renders/screens/ 2>/dev/null || true; cp $V/html/$f.html $S/renders/screens/; done
cp $V/png/2[4-8]-guardian-*.png $V/html/2[4-8]-guardian-*.html $S/renders/guardian-24-28/
cp $B/scenes/stage/png/W24-walk-B-*.png $S/renders/walk24/
cp -r $R/r2d/g26d/png $R/r2d/g26d/html $S/renders/jesus-26/
cp -r $R/ceiling-cap/png-r2ask/. $S/renders/ceiling-cap-r2ask/ 2>/dev/null || true
cp -r $R/ceiling-cap/home-lake/png-r2ask/. $S/renders/home-lake-r2ask/; cp -r $R/sky-options/B/png-r2ask/. $S/renders/sky-B-r2ask/
cp $B/screens/play_v608.py $B/screens/stage_guardian_play.py $B/screens/stage320_play.py $B/verse-popup/gemtag_v608.py $R/ceiling-cap/home_lake.py $R/r2c/*.py $R/r2c/*.sh $R/r2d/*.py $R/r2d/*.sh $R/sheets/sheetkit.py $R/sheets/sheets_r2.py $R/sheets/sheet_frontdesk.py $R/showcase/tour.py $R/guardian-small/banner_check.py $R/sheets/sheet_pick_combined.py $R/sheets/sheet_jesus26.py $R/sheets/sheet_trim.py $B/decisions/b2b/sheets_b2b.py $S/code/
cp /tmp/qmtmp/dom_r2d.log /tmp/qmtmp/dom_r2d2.log /tmp/qmtmp/occl_r2d.log /tmp/qmtmp/occl_r2d2.log /tmp/qmtmp/occl_g15.log /tmp/qmtmp/sgp_r2d5.log /tmp/qmtmp/stage-r2d2.log $S/reports/ 2>/dev/null || true
# renders manifest: every live render the snapshot points at (paths relative to /workspace)
(cd /workspace && { find screens-v608/html screens-v608/png -type f; find v608build/scenes/stage/html v608build/scenes/stage/png -type f; find v608build/round2/ceiling-cap v608build/round2/sky-options/B v608build/round2/r2c/g26 v608build/round2/r2d/g26d v608build/round2/showcase/tiles v608build/scenes/tod -type f \( -name '*.png' -o -name '*.html' \); } | sort | xargs md5sum) > $S/renders-MANIFEST.md5
(cd $S && find . -type f ! -name MANIFEST.md5 | sort | xargs md5sum > MANIFEST.md5)
chmod -R a-w $S
echo "$SN frozen at $NOW; MANIFEST $(md5sum $S/MANIFEST.md5 | cut -c1-32), $(wc -l < $S/MANIFEST.md5) files; renders-MANIFEST $(wc -l < $S/renders-MANIFEST.md5) lines"
