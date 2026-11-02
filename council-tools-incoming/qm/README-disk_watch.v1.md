**Quartermaster:** # disk_watch.py: disk watch at 80% (patch)
**Quartermaster:** Run: `python3 disk_watch.py`. Below 80% on /: one OK line, exit 0. At 80% or more: WARN, exit 1, plus the top 10 dirs by size under /workspace, /tmp/qmtmp and /dev/shm (du depth 2, leaf dirs so no double counting).
**Quartermaster:** It never deletes anything. WARN ends with a suggestion to ask Maxwell (ASKS-LEDGER row first, then a 1A/1B) about archiving or removing.
**Quartermaster:** Options: `--threshold 80`, `--top 10`, `--depth 2`, `--root DIR` (repeatable), `--simulate-percent N` (tests only; output says SIMULATED with the real %).
**Quartermaster:** A missing root (for example /tmp/qmtmp after a wipe) is reported as a note, not an error.
**Quartermaster:** Full WARN scan of the three roots took about 5 s on Nov 1.
**Quartermaster:** Self-test: `python3 selftest_disk_watch.py`.
