**Quartermaster:** # disk_watch.py: disk watch at 80% (patch)
**Quartermaster:** Run: `python3 disk_watch.py`. Below 80% on /: one OK line, exit 0 (79.9% is OK). At 80% or more (exactly 80% warns): WARN, exit 1, plus the top 10 dirs by size under /workspace, /tmp/qmtmp and /dev/shm (du depth 2, leaf dirs so no double counting).
**Quartermaster:** It never deletes anything. WARN ends with a suggestion to ask Maxwell (ASKS-LEDGER row first, then a 1A/1B) about archiving or removing.
**Quartermaster:** Options: `--threshold 80`, `--top 10`, `--depth 2`, `--root DIR` (repeatable), `--simulate-percent N` (tests only; output says SIMULATED with the real %).
**Quartermaster:** A missing root (for example /tmp/qmtmp after a wipe) is reported as a note, not an error.
**Quartermaster:** Full WARN scan of the three roots took about 5 s on Nov 1.
**Quartermaster:** Self-test: `python3 selftest_disk_watch.py`.
**Quartermaster:** Errors: a bad or missing mount, a permission error, a mount that reports 0 total bytes (like /proc) or any other crash prints one ERROR line and exits 2, never a traceback. So a cron caller can tell a crash (2) from a real WARN (1).
**Quartermaster:** If du can't read part of a root (permissions), the WARN still runs and a note says how many paths du could not read, because sizes may be low.
**Quartermaster:** The percent is shown rounded down to one decimal, so 79.99% prints 79.9%, never '80.0% ... below 80%'.
**Quartermaster:** /tmp/qmtmp is only a root it reads with du. It never creates or writes it. Scratch: the tool makes its own folder qm/runs/disk_watch/ with os.makedirs.
**Quartermaster:** v2 (Nov 1, 2026): fixes Auditor gate L1-0141 D-mount (exit 2 on errors). v1 is parked as disk_watch.v1.py.
**Quartermaster:** v3 (Nov 1, 2026): cosmetic fix from gate L1-0200. The "[SIMULATED x%, real y%]" bracket now rounds down too, the same as the main line (79.99 shows 79.9%). Thresholds and exit codes are unchanged. v2 is parked as disk_watch.v2.py.
