**Quartermaster:** # send_log.py: send log with image fingerprints (patch for Auditor to gate, Chancellor to install)
**Quartermaster:** Add a send: `python3 send_log.py add --file a.png [--file b.png ...] --to Maxwell --note 'tile 6 tree grounded'`
**Quartermaster:** Appends one row per image to /workspace/v608build/SEND-LOG.md: Mountain time (MST/MDT label), To, absolute path, full md5, snap name and pointer md5 (md5 of CURRENT-SNAP.txt) at send time, note.
**Quartermaster:** Check: `python3 send_log.py check a.png` (or a bare 32-char md5). SENT (exit 1) lists every earlier send and when; NOT SENT exits 0. PATH SENT AS OTHER VERSION (exit 3): this path is in the log under a different md5, so the file changed after it was sent; every such old row is printed. Exit 3 wins over SENT/NOT SENT (both are still printed). A bare md5 has no path, so it never gives exit 3. Error: exit 2.
**Quartermaster:** List: `python3 send_log.py list`.
**Quartermaster:** Append-only. It never edits or deletes a row. Re-adding an md5 already sent prints ALREADY SENT and still logs the new send (also when the same file is given twice in one add).
**Quartermaster:** Missing file or missing --snap-file: ERROR, exit 2, nothing written. Pipes in notes are escaped.
**Quartermaster:** Overrides for tests: `--log PATH`, `--snap-file PATH` (before the subcommand).
**Quartermaster:** Self-test: `python3 selftest_send_log.py` (writes only to selftest-runs/, never to the real SEND-LOG.md).
**Quartermaster:** Scratch: the tool makes its own folder qm/runs/send_log/ with os.makedirs. It never uses /tmp or another bot's folder. The log itself still goes to /workspace/v608build/SEND-LOG.md by design.
**Quartermaster:** v2 (Nov 1, 2026): fixes Auditor gate L1-0141 S1 (exit 3 on PATH SENT AS OTHER VERSION), S2b and S4. v1 is parked as send_log.v1.py.
**Quartermaster:** v3 (Nov 1, 2026): cosmetic fix from gate L1-0200. When a path was sent as another version, the first line now reads "SENT AS OTHER VERSION: this version (md5 ...) has no row", not "NOT SENT". Exit codes are unchanged (3 here; a bare md5 still gives NOT SENT, exit 0). v2 is parked as send_log.v2.py.
