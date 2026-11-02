#!/bin/bash
# Freeze snap-r2c-<HHMM>MDT (read-only) from the round2 working copy. Copies only; deletes nothing.
set -e
export TMPDIR=/tmp/qmtmp
HM=$(TZ=America/Denver date +%H%M); NOW=$(TZ=America/Denver date '+%-I:%M %p MDT'); SN=snap-r2c-${HM}MDT
B=/workspace/v608build; R=$B/round2; S=$B/$SN
[ -e $S ] && { echo "exists $S"; exit 1; }
# footers and queue name the snapshot
python3 - "$SN" <<'PY'
import sys; sn=sys.argv[1]; p='/workspace/v608build/round2/showcase/tour.py'; s=open(p).read()
s=s.replace("(round2 working copy after snap-r2b-2051MDT, not frozen: PASTE 1A 106a0661 187,797 with \"never over a target\"; 1B 2eebff94 187,797 under trim-1B/)",
            f"(round2c, frozen as v608build/{sn}: PASTE 1A 106a0661 187,797 with \"never over a target\"; 1B 2eebff94 187,797 under trim-1B/)")
s=s.replace("'Round 2 working copy (staged after snap-r2b-2051MDT, not frozen; 1A trim never over a target).", f"'Round 2 build, frozen as v608build/{sn} (round2c: Auditor r2b-2051 and Instructor fixes).")
assert sn in s and 'not frozen' not in s, 'tour text not updated'
open(p,'w').write(s)
PY
(cd $R/showcase && python3 tour.py > /tmp/qmtmp/tour_freeze.log 2>&1)
python3 $R/r2c/make_queue.py $SN "$NOW"
mkdir -p $S/{checks,sheets,pick-sheets-b2b,showcase,trim-1B,stage,reports,code,renders/{screens,walk24,guardian-24-28,jesus-26,ceiling-cap-r2ask,home-lake-r2ask,sky-B-r2ask}}
cp $R/staged/* $S/; cp $B/snap-r2b-2051MDT/nancys-adventure-english-v6-08-daily-verses.json $B/snap-r2b-2051MDT/nancys-adventure-english-v6-08-title.svg $S/
cp $R/diff-*.diff $S/; cp $R/trim-1B/staged/* $R/trim-1B/diff-*.diff $S/trim-1B/
cp $R/round2.py $R/asset-depth/round_totals.py $R/asset-depth/COSTS-and-LEDGER.md $R/README.md $S/; cp $B/README.md $S/README-v608build.md; cp $B/polish-r1/QUEUE.md $S/QUEUE.md
cp $R/checks/checks_v608.py /tmp/qmtmp/mktree.sh $R/trimcheck/trim_clip_check.py $S/checks/
cp $R/sheets/*.png $S/sheets/; cp $B/decisions/b2b/{B1-reward-pacing,D1-sentence-ask-thai-A-B-C-staged,D2-listen-ramp-A-B-C-staged,TG1-sight-words-repeats,TG2-verse-after-run,TG3-guardian-recap,TG4-tier3-buy,bloodtide-name,coin-rule,letter-game-A-B,night-title-line,state-pairs-lean}.png $S/pick-sheets-b2b/
cp -r $R/showcase/INDEX.md $R/showcase/*.png $R/showcase/tour.py $R/showcase/tiles $S/showcase/
cp $B/scenes/stage/CHECK.md $S/stage/CHECK.md; cp $B/scenes/stage_v608.py $S/stage/
V=/workspace/screens-v608
for f in 02b-main-menu-verse-popup-longest-320x568 02b-main-menu-verse-popup-longest-320x568-scrolled 02c-menu-gemtag-before-verse 02c-menu-gemtag-before-verse-320x568 18-two-answer-wrong-tap 23-level-up-reward 23-level-up-reward-320x568 29-verse-scroll-gift 30-new-weapon-gift 34-echo-forest-sound-duel-320x568 35-sound-duel-right-320x568 36-sound-duel-round-done 36-sound-duel-round-done-320x568 52-title-night; do cp $V/png/$f.png $S/renders/screens/ 2>/dev/null || true; cp $V/html/$f.html $S/renders/screens/; done
cp $V/png/2[4-8]-guardian-*.png $V/html/2[4-8]-guardian-*.html $S/renders/guardian-24-28/
cp $B/scenes/stage/png/W24-walk-B-*.png $S/renders/walk24/
cp -r $R/r2c/g26/png $R/r2c/g26/html $S/renders/jesus-26/
cp -r $R/ceiling-cap/png-r2ask/. $S/renders/ceiling-cap-r2ask/ 2>/dev/null || true
cp -r $R/ceiling-cap/home-lake/png-r2ask/. $S/renders/home-lake-r2ask/; cp -r $R/sky-options/B/png-r2ask/. $S/renders/sky-B-r2ask/
cp $B/screens/play_v608.py $B/screens/stage_guardian_play.py $B/screens/stage320_play.py $B/verse-popup/gemtag_v608.py $R/ceiling-cap/home_lake.py $R/r2c/*.py $R/r2c/*.sh $R/guardian-small/banner_check.py $R/sheets/sheet_pick_combined.py $R/sheets/sheet_jesus26.py $R/sheets/sheet_trim.py $B/decisions/b2b/sheets_b2b.py $S/code/
cp $R/guardian-small/banner_check.txt /tmp/qmtmp/dom_r2c.log /tmp/qmtmp/chk1A-r2c.log /tmp/qmtmp/chk1B-r2c.log $S/reports/ 2>/dev/null || true
cat /tmp/qmtmp/occl_full.log /tmp/qmtmp/occl_rest.log > $S/reports/occl-sweep.log 2>/dev/null || true
# renders manifest: every live render the snapshot points at (paths relative to /workspace)
(cd /workspace && { find screens-v608/html screens-v608/png -type f; find v608build/scenes/stage/html v608build/scenes/stage/png -type f; find v608build/round2/ceiling-cap v608build/round2/sky-options/B v608build/round2/r2c/g26 v608build/round2/showcase/tiles v608build/scenes/tod -type f \( -name '*.png' -o -name '*.html' \); } | sort | xargs md5sum) > $S/renders-MANIFEST.md5
(cd $S && find . -type f ! -name MANIFEST.md5 | sort | xargs md5sum > MANIFEST.md5)
chmod -R a-w $S
echo "$SN frozen at $NOW; MANIFEST $(md5sum $S/MANIFEST.md5 | cut -c1-32), $(wc -l < $S/MANIFEST.md5) files; renders-MANIFEST $(wc -l < $S/renders-MANIFEST.md5) lines"
