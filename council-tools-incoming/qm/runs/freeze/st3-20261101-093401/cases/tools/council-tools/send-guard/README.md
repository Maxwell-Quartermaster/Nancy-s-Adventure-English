# send-guard (owner: Chancellor)
Blocks any send to Maxwell that carries a screenshot or sheet that is not in the current snapshot, or that fails Watchman's ground check.

Run before every send (from anywhere):
    python3 /workspace/council-tools/send-guard/send_guard.py --only sheets/,showcase/ FILE [FILE ...]
The snapshot comes from QM's pointer /workspace/v608build/CURRENT-SNAP.txt (read via council-tools/current_snap.py). --snap DIR is accepted only if it is the pointer's exact folder (realpath); anything else is STALE-SNAP.
Exit 0 = CLEAR; 1 = BLOCK (problems listed); 2 = bad input or an unreadable pointer; 3 = clear but --no-ground was used (test only, never a send).
Line 1 always stamps: send-guard <md5> current_snap <md5> ground_check <md5>, plus snap and MANIFEST/renders-MANIFEST md5s.

Checks:
- each file's md5 is in the pointer snapshot's MANIFEST.md5 or renders-MANIFEST.md5, and the pointer's md5s match disk (both are required);
- with --only, the file must be listed under one of those folders;
- WARN when the same file name has other md5s in the snapshot;
- every image (by extension or PNG/JPEG header) runs through ground-check/ground_check.py: a path stroke, a floating tree or an unreadable image is a GRND BLOCK. --no-ground skips this, prints "GROUND SKIPPED", and exits 3. Option abbreviations are off.
Self-test: python3 send_guard.py --selftest -> 23/23 (pointer, realpath, --only, renders, CLI wiring, ground on/off/renamed, abbreviation, missing pointer, stamp). Scratch goes to send-guard/selftest-scratch/ and is kept (no-delete rule).
Blind spots: being in the snapshot is not the same as being the approved look. ground_check misses dimmed or overlaid scenes (a 15% scrim already hides a planted path and floating tree; tile 25 = screen 48 under its pause card is unverified), trunks under 2 px, pines and tufts. A PASS on those is "unverified", not clean.
