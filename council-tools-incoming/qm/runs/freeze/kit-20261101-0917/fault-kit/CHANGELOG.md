**Auditor:** # fault-kit CHANGELOG (times MST, box clock; Nov 1 2026 is after the 2 AM fall-back, so 01:xx here is the second 01:xx)

## v1.1 (Nov 1 2026, ~01:45 MST): run_kit.py fe8edbe37d115fddf1cfdc330c0d9c7a
**Auditor:** - Added the tuft_check case set (6 cases: 5 required + 1 recorded edge case), scoped to Maxwell t545u (via QM): tufts only on grass; dots on dirt/path/sand/hill left alone. Images built by tools/make_planted.py (72e87204) from a kit copy of W24-walk-B-390x844.png 3685711d. Cases cases/tuft_check/cases.json 37bcf6cd.
**Auditor:** - Planted tuft images: U01-clean b3b77260, U02-circle-dot-on-grass 71348e28; U03-pebble-on-dirt 33781bec, U04-pebble-on-sand-strip 43f82c61, U05-dot-on-grass-dirt-edge ef9c34d1, U06-pebble-on-dirt-plus-dot-on-grass 5e1160fc (rebuilt after the dirt patch was moved off the sword).
**Auditor:** - Added ground_check multi-panel cases G35-G44 (from Watchman's S01-S04 finding, watchman/s01-s04-eye/REPORT.md 279fac1b). Real sheets copied from v608build/scene-fill-20261101/sheets/: S01 04d39532, S02 8fe1165e, S03 ad02c96a, S04 e10b9581. The true-positive S01-path-in-panel1.png a8e535e0 has a 26 pt path stroke on panel 1 grass only (2976 px). `mode: panels` splits the sheet at the cream gaps (cases/ground_check/panels.py a0d3405c) and judges each panel. A whole-sheet result is RECORDED, never graded. Cases cases/ground_check/cases.json f76418cc (44 cases).
**Auditor:** - New verdict RECORD (printed as REC, never counted). Two new self-test stubs: tuft never-flag and always-flag. Self-test now 18/18.
**Auditor:** - Caveat on G43: the plant uses ground_check's own PATH colour (#E8D9A8 @ .85). Scene-fill sheet grass renders as ~#56B05C, which is outside ground_check's GRASS palette (#36A13D/#259D39, tol 22). So a per-panel miss here means the tool is blind on this grass. It does not mean the plant is invalid. I did not tune the case.

## v1 (Nov 1 2026, ~01:27 MST): run_kit.py e0347e78 (first run ac27e15b; its text_check status regex missed 'TEXT UNVERIFIED' with one space; fixed before any reported result)
**Auditor:** - Case sets: text_check 30 (28 req), ground_check 34 (30 req), freeze 34 (34 req), quote_check 7 (data only, NOT BUILT), conflict_check 3.
**Auditor:** - Inputs copied in: text_check MANIFEST.md5 7b7c357f and renders-MANIFEST.md5 62e41535 (from snap-r2h-0021MDT), chk1B-rerun.log d34a7c6f (from audit/text-check-g4/r2h-rerun-stage/reports/). Ground images come from audit/gc-cap-gate/planted and dimin (34 files; tile-B-float was left out because the planted.py float box has no tree in tile B). Freeze stage: 05-map-day1 png 2b14fcd0 and html 0a0a4eaa, showcase-1-opening 8dcce473, 09-map-later bf88ff86; hooks copied from audit/freeze-gate-91aa8a3e/hooks. Quote ledger-excerpt.md a74a500b comes from SETTLED-RULINGS.md 8d8aeff5 rows A02/A21/A29/M05/P16/T12. Spec and PASTE excerpts (0fa795ff, 3f9be484) are taken from PASTE 317e91ce at the original line numbers.

## Results (final runs, run_kit fe8edbe3; reports in runs/report-*.txt)
| tool / version | required | advisory | recorded | exit |
|---|---|---|---|---|
| text_check live 9c433cba | 10/28 | 1/2 | - | 1 |
| text_check candidate 14d216c9 | 28/28 | 2/2 | - | 0 |
| ground_check live f46a2d29 | 21/34 | 1/5 | 5 | 1 |
| ground_check v2 13fc304c | 27/34 | 3/5 | 5 | 1 |
| ground_check v2cap 9979400b | 28/34 | 3/5 | 5 | 1 |
| tuft_check b19579ac | 5/5 | - | 1 (U05 PASS) | 0 |
| tuft_check current 9edb03b4 | 5/5 | - | 1 (U05 PASS) | 0 |
| freeze 91aa8a3e, run 1 01:28 MST (run_kit e0347e78) | 34/34 | - | - | 0 |
| freeze 91aa8a3e, runs 2-3 ~01:50 MST | 16/34 | - | - | 1 (ENVIRONMENT: /tmp/qmtmp missing, see below) |
| conflict_check (incoming) 570c5e00 | 2/3 | - | - | 1 |
| quote_check | NOT BUILT | | | 2 |
| --self-test | 18/18 | | | 0 |

**Auditor:** Freeze runs 2-3: every clean path now stops at step 3. The cause is trim_clip_check.py (in the live snapshot checks) calling `tempfile.mkdtemp(dir='/tmp/qmtmp')`, and /tmp/qmtmp no longer exists on the box. A real freeze would fail the same way right now. That is QM's to fix. The kit does not create it, because nothing outside the kit gets written.
