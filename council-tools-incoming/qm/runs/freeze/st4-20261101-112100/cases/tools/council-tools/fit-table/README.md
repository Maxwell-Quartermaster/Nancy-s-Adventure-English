# fit-table (owner: Chancellor)
What: lists every R2 combination (screen 26 option x ask x ramp x savings) that fits the PASTE bank, and what's left.
Run: `python3 fit_table.py --paste <PASTE.md> > out.md`; test first with `python3 fit_table.py --selftest`. The bank is computed as ceiling - PASTE length and the tool refuses to run if costs.json bank disagrees.
Inputs: costs.json only. Update it from measured md5s, never by hand-guessing.
Writes: stdout only, no temp files.
Blind spots: assumes costs add linearly (no shared clause savings); doesn't know about picks outside costs.json; bank must already include bug fixes and the trim.

Pointer (Nov 1, 00:15 MDT): --paste is optional and defaults to the 1A PASTE in QM's CURRENT-SNAP.txt. It refuses if the pointer disagrees with disk, if costs.json manifest is not the pointer's, or if --paste is not the pointer's 1A (use --what-if to explore a non-build PASTE; output is tagged WHAT-IF).
