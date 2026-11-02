**Quartermaster:** # QM incoming tools (patches only; Auditor gates, Chancellor installs into /workspace/council-tools)
**Quartermaster:** Built for Maxwell t547u: send_log.py, disk_watch.py, base_check.py, quote_check.py. Per-tool docs: README-<tool>.md.
**Quartermaster:** Run every self-test: `cd /workspace/v608build/council-tools-incoming/qm && for s in send_log disk_watch base_check quote_check; do python3 selftest_$s.py; done`
**Quartermaster:** Self-test scratch goes to selftest-runs/<Mountain timestamp>-<tool>/ and is never deleted (park, don't delete).
**Quartermaster:** Python 3.13, standard library only (zoneinfo, difflib, hashlib). disk_watch uses du.
**Quartermaster:** md5s are in MANIFEST.md5 (`md5sum -c MANIFEST.md5`).
