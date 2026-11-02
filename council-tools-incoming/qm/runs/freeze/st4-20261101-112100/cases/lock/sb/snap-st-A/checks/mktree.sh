#!/bin/bash
# mktree.sh <tree> <variant dir holding the 4 staged files> <round2.py> : a scratch NAE_W tree whose top-level v6-08 files AND round2/staged are the variant
set -e; T=$1; V=$2; R=$3; N=nancys-adventure-english
mkdir -p $T/v608build/round2/staged
for e in /workspace/* ; do b=$(basename "$e"); case $b in v608build|$N-v6-08-PASTE.md|$N-FINAL-v6-08.md|$N-v6-08.md|$N-v6-08-cards.json) continue;; esac; ln -sfn "$e" "$T/$b"; done
for f in $N-v6-08-PASTE.md $N-FINAL-v6-08.md $N-v6-08.md $N-v6-08-cards.json; do ln -sfn $V/$f $T/$f; ln -sfn $V/$f $T/v608build/round2/staged/$f; done
for e in /workspace/v608build/*; do b=$(basename "$e"); [ "$b" = round2 ] && continue; ln -sfn "$e" "$T/v608build/$b"; done
for e in /workspace/v608build/round2/*; do b=$(basename "$e"); case $b in staged|round2.py) continue;; esac; ln -sfn "$e" "$T/v608build/round2/$b"; done
ln -sfn $R $T/v608build/round2/round2.py
