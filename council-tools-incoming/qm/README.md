**Quartermaster:** # QM incoming tools (patches only; Auditor gates, Chancellor installs into /workspace/council-tools)
**Quartermaster:** Built for Maxwell t547u: send_log.py, disk_watch.py, base_check.py, quote_check.py. Per-tool docs: README-<tool>.md.
**Quartermaster:** Run every self-test: `cd /workspace/v608build/council-tools-incoming/qm && for s in send_log disk_watch base_check quote_check; do python3 selftest_$s.py; done`
**Quartermaster:** Self-test scratch goes to runs/selftest/<Mountain timestamp>-<tool>/ and is never deleted (park, don't delete). Older runs stay in selftest-runs/.
**Quartermaster:** Scratch rule: every tool makes its own scratch folder with os.makedirs under qm/runs/<tool>/. No tool assumes /tmp, /tmp/qmtmp or another bot's folder exists.
**Quartermaster:** v1 files are parked beside v2 as <name>.v1.py / <name>.v1.md. Nothing was deleted.
**Quartermaster:** Python 3.13, standard library only (zoneinfo, difflib, hashlib). disk_watch uses du.
**Quartermaster:** md5s are in MANIFEST.md5 (`md5sum -c MANIFEST.md5`).
**Quartermaster:** Older versions are parked beside the current files as <name>.vN.py / <name>.vN.md (v1-v4), with the matching MANIFEST.vN.md5. quote_check is at v4.1.
