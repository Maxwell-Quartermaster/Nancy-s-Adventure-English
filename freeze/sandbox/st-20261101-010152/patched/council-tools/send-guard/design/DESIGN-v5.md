# send-guard v5 design (owner: Auditor, per Maxwell t97u, Nov 1 2026 12:35 AM MDT)
Base: send_guard.py 80615576 + ground_check e6873c57 (re-gate running), pointer 907062f0.
Goal: nothing reaches Maxwell unless it is current, approved-look, on-spec, readable, and stamped.

## Exit codes (one entry point)
0 CLEAR, 1 BLOCK, 2 ERROR, 3 SKIPPED/test-only (never valid for a send).

## Layers (each has an owner and planted-fault self-tests)
L1 Freshness (Chancellor, done): md5 vs pointer MANIFEST/renders-MANIFEST, realpath, --only scoping.
L2 Any image by header, not name (Chancellor, done in 80615576).
L3 Ground look (Watchman): path stroke, floating tree, + DIM DETECT: dimmed/overlaid screen => BLOCK unless an undimmed twin render in the same snapshot passes. Fixes the tile 25/48 blind spot and the 15% overlay case.
L4 Internal-only sheets (QM rule, t419u): before/after and any sheet tagged internal => BLOCK for Maxwell sends.
L5 Content (Instructor): OCR text on sheets vs banned list (locked, padlock, failed, lost, 911, Call Max, Show the Nurse, timers/energy/leaderboard, brand names); stale wording (e.g. "Where is the kite?"); any verse text on a sheet must match the build verses JSON word for word; Thai on sheets must match the spec.
L6 Layout (Auditor, occl): 320/375/390, text >= 8px, taps >= 44pt, gaps >= 8pt, 16pt side margins, nothing over a target or head.
L7 Sheet stamp (Chancellor, sheetkit): every sheet footer carries snapshot + pointer md5; guard BLOCKs a sheet whose footer pointer != current pointer.
L8 Send record (QM): QM sends only with a guard stamp from the same pointer, < 30 min old; log md5 of each image sent.

## Testing standard (Auditor)
Every check gets a planted-fault case; Auditor runs a mutation pass (disable each check in turn) and a check only counts if the self-test catches its removal.

## Order
1) Gate 80615576 + e6873c57 now. 2) L3 dim + L4 internal. 3) L7 stamp. 4) L5 content. 5) L6 layout. Re-gate after each.
