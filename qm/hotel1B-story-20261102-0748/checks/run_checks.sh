#!/bin/bash
# QM: freeze.py-style checks_v608 run (staged checks, snap mktree.sh). Variants: PASTE swapped (freeze gate) and cards.json = PASTE line 427.
set -e; H=/workspace/qm/hotel1B-story-20261102-0748/checks; N=nancys-adventure-english; S=/workspace/v608build/snap-r2h-0021MDT
CHK=/workspace/v608build/round2/checks/checks_v608.py; R2=$S/round2.py
BASE=/workspace/qm/cards-fix-20261102-0704/new/$N-v6-08-1B-v32-cards1A-fix-PASTE.md
CAND=/workspace/qm/hotel1B-story-20261102-0748/$N-v6-08-1B-v32-hotel1B-story-PASTE.md
one(){ tag=$1; p=$2; cardsfrom=$3; w=$H/$tag; mkdir -p $w/var
  for f in $N-FINAL-v6-08.md $N-v6-08.md; do cp -p $S/trim-1B/$f $w/var/$f; done
  cp -p $p $w/var/$N-v6-08-PASTE.md
  if [ "$cardsfrom" = line427 ]; then sed -n 427p $p | tr -d '\n' > $w/var/$N-v6-08-cards.json; else cp -p $S/trim-1B/$N-v6-08-cards.json $w/var/; fi
  bash $S/checks/mktree.sh $w/tree/ $w/var $R2
  (cd /workspace/v520 && NAE_W=$w/tree/ NAE_VERSION=v6-08 timeout 900 python3 $CHK > $w/checks.out 2>&1; echo "rc=$?" >> $w/checks.out)
  echo "$tag $(tail -1 $w/checks.out) lines=$(wc -l < $w/checks.out)"; }
one base-c427$1 $BASE line427 & one cand-c427$1 $CAND line427 & wait   # (first run, pre-fix: base-paste/cand-paste done; base-cards427/cand-cards427 dirs are the failed permission attempt, kept)
