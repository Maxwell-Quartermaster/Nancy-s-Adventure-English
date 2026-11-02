#!/bin/bash
# Auditor disk_watch v2 planted cases. Writes only in this folder.
T=/workspace/v608build/council-tools-incoming/qm/disk_watch.py
head -c 50000 /dev/urandom > root/a/blob; find root -type f | sort | xargs md5sum > before.md5
for p in 80 80.0 80.01 79.9 79.99 79.95; do echo "== sim $p"; python3 $T --simulate-percent $p --root $PWD/root; echo rc=$?; done
echo "== real"; python3 $T; echo rc=$?
echo "== bad mount"; python3 $T --mount /no/such/mount; echo rc=$?
echo "== /proc"; python3 $T --mount /proc; echo rc=$?
echo "== unreadable root"; mkdir -p noread/sub; head -c 1000 /dev/urandom > noread/sub/f; chmod 000 noread/sub; python3 $T --simulate-percent 90 --root $PWD/noread --root $PWD/root; echo rc=$?; chmod 755 noread/sub
find root -type f | sort | xargs md5sum | diff - before.md5 && echo "no file changed or deleted"
