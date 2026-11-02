#!/bin/bash
# Auditor send_log v2 planted cases. Writes only in this folder (and the tool's own qm/runs/send_log/).
T=/workspace/v608build/council-tools-incoming/qm/send_log.py; L="--log $PWD/SEND-LOG.md --snap-file $PWD/../../data/CURRENT-SNAP.txt"
printf '\x89PNG img v1' > img.png; echo "img v1 $(md5sum < img.png | cut -c1-8)"
echo "== S1 add"; python3 $T $L add --file img.png --to Maxwell --note "tile 6"; echo rc=$?
printf '\x89PNG img v2 CHANGED' > img.png; echo "img v2 $(md5sum < img.png | cut -c1-8)"
echo "== S1 check changed path"; python3 $T $L check img.png; echo rc=$?
echo "== S1b check by bare md5 of v2"; python3 $T $L check $(md5sum < img.png | cut -c1-32); echo rc=$?
echo "== S2 duplicate send"; printf '\x89PNG img v1' > dup.png; python3 $T $L add --file dup.png --to Maxwell; echo rc=$?; python3 $T $L check dup.png; echo rc=$?
echo "== S2b same file twice in one add"; printf 'x2' > two.png; python3 $T $L add --file two.png --file two.png --to Maxwell; echo rc=$?
echo "== S3 missing"; n=$(wc -l < SEND-LOG.md); python3 $T $L add --file nope.png --to Maxwell; echo rc=$?; [ "$(wc -l < SEND-LOG.md)" = "$n" ] && echo "log unchanged"
echo "== S3b check missing"; python3 $T $L check nope.png; echo rc=$?
echo "== S4 missing snap file"; python3 $T --log $PWD/x.md --snap-file $PWD/nosnap.txt add --file dup.png --to M; echo rc=$?; [ -e x.md ] && echo "x.md WRITTEN" || echo "x.md not written"
