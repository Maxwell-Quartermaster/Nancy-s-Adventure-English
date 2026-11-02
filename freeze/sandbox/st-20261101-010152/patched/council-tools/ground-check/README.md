# ground-check (owner: Watchman; built for QM's r2h "16/16S look on every screen")
What: a no-browser pixel check on PNG renders and sheets. It flags (a) the old scene path stroke and (b) floating round-crowned trees. Pillow + numpy only.
Run: `python3 ground_check.py --selftest` first, then `python3 ground_check.py FOLDER [FOLDER...]` (it walks each folder recursively for *.png).
First line per folder: the tool md5, the folder, and the MANIFEST.md5 md5 (from the folder or its parent) or "none". Then one line per PNG: relative name, md5, PASS or BLOCK with the reason. Then a summary line.
Exit: 0 = all PASS (or selftest PASS), 2 = any BLOCK (or selftest FAIL), 1 = usage.
Writes: stdout only. `--selftest` writes 3 small PNGs into ./runs/selftest/ (never /tmp or /dev/shm) and never deletes anything.

Colours, from the draw code (not guessed):
- Path: #E8D9A8 at opacity .85 (mock-t328u/find_t328u.py:72 at 320 and :76 at 390, "M140 844q20-140 120-250", width 26; mock-t312u/find_t312u.py:95; the t441u/stage B and W24 copy "M118 844q26-70 170-128"), and #D8C99A at .8 (scenes/stage_v608.py:36-37, scene A "M330 844q-30-70 -190-120"). Matched raw and blended over grass, with a tolerance of 14 per channel. A pixel counts only if grass lies within W/40 px on the same row, so tan cards and parchment don't count. BLOCK at max(40, 0.04% of the image) px.
- Grass: #36A13D near hill and #259D39 far hill (P.ground), tolerance 22.
- Trees (P.tree = mock-t277u/style_test.py:23-28): trunk #8A5A34 and shade #6C4425, canopy #7ECA72 and #28792D. #489B3B is left out because it sits within tolerance of the grass. A trunk is an upright blob at least 2 px wide and 4 px tall, with both canopy tones above it. It floats if the max(4, 0.35 × trunk height) px under its lowest row hold no grass.

Self-test: from tile 16's stage render (W24-walk-B-390x844.png, both trees grounded, tufts), it crops above the ask card, which gives a clean "tile 6". It then plants (1) the old #E8D9A8 stroke and (2) the right tree lifted 76 pt (only the tree's pixels, not the grass it stood in). Both must BLOCK, and the clean crop must PASS.

Blind spots (say "unverified" for these, don't call them PASS):
- dimmed or overlaid scenes, such as screen 48 under its pause card (tile 25) or any scene under a scrim: the colours shift past tolerance.
- very small sheet tiles, where a trunk is under 2 px wide (the 320 copies on some sheets).
- Echo Forest pines (trunk #5A3A22 on purple hills), which are not checked. The tod night and evening tints are not modelled either; those scenes use the same ground colours today.
- tufts (presence or overlap with targets), which are not checked. Use the HTML-side check in watchman/r2h-ground-sweep/overlap.py.
- a path drawn in a new colour or as the toggle sidewalk (#D6CFC1), which won't be seen. Add its hex here first.
