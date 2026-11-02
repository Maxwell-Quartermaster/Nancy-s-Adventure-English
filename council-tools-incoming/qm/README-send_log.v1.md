**Quartermaster:** # send_log.py: send log with image fingerprints (patch for Auditor to gate, Chancellor to install)
**Quartermaster:** Add a send: `python3 send_log.py add --file a.png [--file b.png ...] --to Maxwell --note 'tile 6 tree grounded'`
**Quartermaster:** Appends one row per image to /workspace/v608build/SEND-LOG.md: Mountain time (MST/MDT label), To, absolute path, full md5, snap name and pointer md5 (md5 of CURRENT-SNAP.txt) at send time, note.
**Quartermaster:** Check: `python3 send_log.py check a.png` (or a bare 32-char md5). SENT (exit 1) lists every earlier send and when; NOT SENT exits 0.
**Quartermaster:** List: `python3 send_log.py list`.
**Quartermaster:** Append-only. It never edits or deletes a row. Re-adding an md5 already sent prints ALREADY SENT and still logs the new send.
**Quartermaster:** Missing file: exit 2, nothing written. Pipes in notes are escaped.
**Quartermaster:** Overrides for tests: `--log PATH`, `--snap-file PATH` (before the subcommand).
**Quartermaster:** Self-test: `python3 selftest_send_log.py` (writes only to selftest-runs/, never to the real SEND-LOG.md).
