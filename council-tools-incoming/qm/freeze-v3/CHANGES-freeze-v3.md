# freeze-v3 candidate (Quartermaster). NOT installed. Live freeze/freeze.py stays 91aa8a3e.
Based on: snap-r2h-0021MDT, pointer f6dac2d0, PASTE 317e91ce. Base: freeze.base-91aa8a3e.py (byte copy of live).

## One change (Auditor gate point 2, QM ruling)
Any stage file under a directory named exactly `sheets` or `showcase`, at any depth (sheets/x, sheets/sub/x,
scene-fill-20261101/sheets/x, showcase/x), is routed ONLY to the sheets scan, never to ground_check.
- route(rel) -> 'sheets' | 'single'. 'single' paths: unchanged from 91aa8a3e (note: 91aa8a3e never sends them to
  ground_check or send_guard; nothing new is added for them).
- sheets leg: send_guard `--only <prefixes cut at the first sheets/showcase dir> --no-ground` (snapshot/pointer/--only checks kept,
  ground_check never called); only exit 3 passes there (0 is refused as "ground may have run").
- then every image on that leg goes to SHEETS_SCAN = $TOOLS/sheets-scan/sheets_scan.py (Chancellor). Contract assumed:
  `sheets_scan.py FILE...`, CURRENT_SNAP = candidate pointer, exit 0 PASS / 1 BLOCK / 2 ERROR; only 0 passes. Output to
  freeze/work/sheets-scan-<snap>.txt.
- FAIL-CLOSED: if sheets_scan.py is not installed, a stage with any sheets/showcase image fails step 3 ("sheets scan not
  installed"). Today it is NOT installed (Chancellor's per-panel logic exists only inline in incoming/chancellor-freeze-sheets-perpanel
  c19c845f), so this candidate must not be installed before the scan is.
- FREEZE_FAULT sendguard_exit3 kept in FAULTS (parsing unchanged) but is now a no-op.
- Not changed: steps 0-2, 4-8, checks_v608, trim-clip, fit_sheet_check, carry/manifests, pointer, HOLD/lock/rollback, CLI.

## selftest.py (harness)
Freeze runs use FREEZE_TOOLS = small tools copy + STUB sheets scan + logging ground_check wrapper; case 5/5b rewritten for the
new routing; new cases 5c (route() units: showcase/, sheets/, nested scene-fill/sheets/, sheets/sub/, normal render, sheets-ref/,
file named sheets.png; routing dry run asserting scan gets exactly the 4 sheets images, ground_check gets nothing, normal render
goes nowhere new; logger control) and 5d (live tools: fail-closed; stage without sheets passes). Case 22 copies only the tools
it needs instead of `cp -a` of all 8.8 GB council-tools.
