# freeze/ — Quartermaster's one-button freeze (Maxwell t510u / t511u). Owner: Quartermaster.

## The button
    python3 /workspace/v608build/freeze/freeze.py --stage <stage dir> --paste <PASTE.md> --snap-name snap-<round>-<HHMM>MDT --note "what changed" --dry-run
    python3 /workspace/v608build/freeze/freeze.py --stage <stage dir> --paste <PASTE.md> --snap-name snap-<round>-<HHMM>MDT --note "what changed"
Dry run first (no HOLD, pointer untouched, snapshot built and verified under freeze/work/), then the real run.

Stop everyone / release / look:
    python3 freeze.py --hold "reason"     # writes freeze/HOLD, prints the HOLD broadcast
    python3 freeze.py --release           # archives HOLD (+ HOLD.reason) to freeze/holds/, prints RESUME with the sync line
    python3 freeze.py --status            # exit 0 no HOLD, 1 HOLD (age, reason, STALE if no freeze is running and no reason was written)
Any bot or tool: `python3 /workspace/v608build/freeze/hold_check.py` -> exit 0 clear, exit 1 HOLD (prints why).

## Steps (stop on the first failure: exit 1, one `REASON: step N <name>: <file>: <what>` line)
0. HOLD: fcntl lock freeze/freeze.lock (a second freeze exits 2); refuse (exit 2) if freeze/HOLD exists unless --force-clear
   (the old HOLD is archived, not deleted); write HOLD + hold-msg.txt; print the HOLD broadcast.
1. Preflight: pointer parses and current_snap.verify is clean; the pointer's paste_1b is on disk at its md5; new PASTE exists,
   chars <= 188,200; disk < 80%; snapshot name free.
2. Content: the daily-verses JSON the PASTE names (stage first, then snapshot, then /workspace) is byte-identical to the previous
   version's file except the one "version" field (and that field is the right version); "if due" present; no 911 / Call Max /
   Show the Nurse; no phone, email or street-address pattern; thai_diff old PASTE -> new PASTE run, report in freeze/work/.
3. Render: checks_v608 (round2/checks, via the snapshot's mktree.sh) on the new PASTE vs the pointer PASTE — FAIL only on NEW live
   False lines (the r2h PASTE already carries 15 live False because those pins are the round2 derivation; baseline cached in work/);
   trim_clip_check (the DOM trim-band check) on every stage html; send_guard --only sheets/,showcase/ on every stage sheets/ and
   showcase/ file (only exit 0 passes; 1, 2 and 3 FAIL); fit_sheet_check on any *fit*.md in the stage (only exit 0 passes).
   send_guard and fit_sheet_check are run against a CANDIDATE pointer in freeze/work/precheck-*/ whose MANIFESTs are the exact bytes
   the snapshot will get, so they judge the new build while the live pointer stays put.
4. Snapshot (default = CARRY, QM 01:06): new snap = the previous COMPLETE snap named by the pointer + the stage files overlaid +
   the PASTE at trim-1B/nancys-adventure-english-v6-08-PASTE.md. Before anything is copied (step 3 plan) every carried file's md5
   is checked against the previous MANIFEST; a mismatch, an unlisted file or a missing file FAILS (pointer never moves). A stage file
   at the same path overrides the carried one. `--no-carry` builds stage + PASTE only.
   Built in v608build/.tmp-<snap>-<pid>, every copy with shutil.copy2 (mtimes kept, then checked = source mtime, Auditor fault 9).
   renders-MANIFEST.md5 = the previous renders-MANIFEST lines carried verbatim (they are the previous freeze's record; 45 of the
   r2h sources have been re-rendered since, so they are NOT re-hashed against disk) + one line per stage .png/.html
   (md5 + /workspace-relative source path, re-hashed), sorted. DELTA.md (vs the old snap): counts for carried / stage new /
   stage overrides / stage same / not carried, Changed, New, Not carried, and a per-file status list. MANIFEST.md5 (`md5  ./path`,
   sorted, not itself). Every md5 re-verified, MANIFEST must equal the one step 3 checked; then renamed to v608build/<snap> and made
   read-only. A write failure (disk full, unwritable) leaves only the .tmp dir (named in the reason, never pointed at).
5. Pointer: refuse if the pointer changed since the HOLD (hand-moved); back up to CURRENT-SNAP.txt.pre-<snap>; write tmp + fsync +
   rename with snap, manifest md5s, paste_1b md5/path/chars, bank, working, updated (America/Denver), paste_1b_chain; re-read.
6. Self-check: Chancellor's current_snap.read/verify on the new pointer in a subprocess + paste_1b md5 + bank = ceiling - chars.
   Any failure at 5-6 ROLLS THE POINTER BACK from the .pre backup and verifies it; HOLD.reason says
   "POINTER MOVED to X; ROLLED BACK to Y (verified)" or "NOT ROLLED BACK (why). Restore by hand: cp ...".
7. Messages: last-freeze.json, resume-msg.txt, watchman-msg.txt.
8. Release: only if the pointer is still the one step 5 wrote, HOLD is archived to freeze/holds/. Then it prints the RESUME+SYNC
   text and, as the LAST line, the Watchman agent message `FREEZE <new pointer md5> <snap>`.
   On any failure HOLD stays and HOLD.reason is written, so everyone stays stopped until QM fixes it and re-runs (--force-clear) or --release.

## Messages QM sends (freeze.py prints them; it cannot post)
(a) HOLD (step 0, also freeze/hold-msg.txt): `QM HOLD: freeze <snap> in progress. Stop work now. No edits, no sends, no patches past this point until RESUME.`
(b) RESUME+SYNC (Council): new pointer, snap, MANIFESTs, PASTE md5, chars, bank, what changed; sync proof = each bot's next Council
    post opening `Based on: <snap>, pointer <8>, PASTE <8>`; `watcher.py --ack <you>` is a backstop only, after the release
    (watcher a54f904e refuses acks while HOLD exists; Auditor has not seconded the Watcher). freeze.py does not call watcher.py.
(c) Watchman (agent message): exactly `FREEZE <new pointer md5> <snap name>`.

## Tests
`python3 selftest.py` (102 cases, ~3 min, real checks_v608 in the clean runs) or `--quick` (skips checks_v608). Every case runs in
freeze/sandbox/st-<MT time>/<case>/sb (--sandbox seeds a copy of the pointer, its complete snapshot (copy2) and its PASTE, ~71 MB per sandbox); the live
CURRENT-SNAP.txt md5 is asserted after every case. Planted faults (FREEZE_FAULT, honoured only with --sandbox): step6_bad_pointer,
rollback_fails, paste_copy_corrupt, manifest_enospc, pointer_handmove, crash_after_hold, sendguard_exit3, plain_copy.
--skip-checks-v608 and FREEZE_TOOLS are refused without --sandbox.

## Not wired / blind spots
- occl sweep (code/occl_qm.py, occl_list.py): hard-coded render globs and multi-minute Chrome runs, not stage-parameterised.
- Watchman's DOM scripts (watchman/*/domcheck*.py) are scratch, not a council tool; the trim-band DOM check is wired instead.
- stage/CHECK.md (stage_v608.py prop anchoring) is not re-run.
- Carried renders-MANIFEST lines are not re-hashed (their sources may have been re-rendered since the previous freeze); the
  snapshot's own copies of those renders are covered by MANIFEST.md5, which IS checked.
- checks_v608 is a regression gate (new live False only), not an absolute one.
- Proposed (not applied): council-tools/incoming/qm-hold-check.diff makes send_guard and current_snap refuse during a HOLD
  (freeze.py sets NAE_FREEZE_RUNNING=1 for itself). Chancellor owns council-tools.

**Quartermaster:** If a freeze fails at step 5 or 6, the pointer rolls back, but the complete snap stays read-only under its final name. A re-run with that same name is refused as "already exists", so pick a new snap name for the retry. A step 4 failure leaves a `.tmp-<snap>-<pid>` folder, and HOLD.reason names it.
**Quartermaster:** `--force-clear` refuses with exit 2 if the pointer moved since the HOLD. `--status` and `hold_check.py` print "POINTER MOVED since the HOLD: a -> b". (Auditor's fix 2e41ef19, applied Nov 1, 2026 1:30 AM MDT.)
