**Quartermaster:** # play-verse-split-b1: QM split f778b0bf plus Watchman's B1 guard. Sun Nov 1 2026, about 2:30 PM MST. Maxwell t581u game priority (a). Nothing installed, nothing deleted.
**Quartermaster:** Based on: snap-r2h-0021MDT, pointer f6dac2d0, PASTE 317e91ce, base play_v608.py f778b0bf (split of ee74f3ef).
**Quartermaster:** MAIN CANDIDATE: new/play_v608.py 70130b178a65689888f8d1473aaaabb6 = f778b0bf + Watchman proposed/play_v608.B1-guard.diff 75c44083 (applied with patch, exit 0). It is byte-identical (cmp) to Watchman's proposed/new/play_v608.py 70130b17.
**Quartermaster:** The guard is exactly 2 added lines after :60 (new :61-62), 0 lines removed. play_v608.B1.diff has the same hunk as Watchman's diff; only the file-name header lines differ.
**Quartermaster:** A4 VARIANT (separate, not the main candidate): a4/play_v608.py b565920e1d66da926e162d28b62ff551 = 70130b17 with verse()'s assert replaced by raise SystemExit (python -O strips assert). Diffs: play_v608.A4-only.diff (vs 70130b17), play_v608.B1-A4.diff (vs f778b0bf). verse() still has 0 callers.
**Quartermaster:** ## Tests (all on copies, real PASTE 317e91ce through the pointer unless a case file is named)
**Quartermaster:** Rebuild: tools/build.py is a byte copy of Watchman's gate harness (0257c990), Python only, no Chrome. 31 pages x 3 sizes (390x844, 375x667, 320x568 via NAE_SE=1).
**Quartermaster:** new 70130b17: 93/93 page outputs byte-identical to f778b0bf. a4 b565920e: 93/93 byte-identical to f778b0bf. new r1 = r2 at all 3 sizes.
**Quartermaster:** Page 26/30/37 raw md5s match Watchman's table: 390 26c1d9ce/dfad68d3/c0835bac, 375 51ac07b1/4860981c/287bffca, 320 11c59779/57cac786/da5c587c.
**Quartermaster:** Negative cases (tools/make_cases.py, 44 PASTE copies in scratch/cases/, 2 sizes each = 88 runs per variant, runs/neg-*.txt):
**Quartermaster:** rest ref/en/th/enSource/thSource and jesusWords[0] ref/en/th, each as empty, spaces, mixed whitespace, null and missing (40), plus jw empty list, rest missing, rest.en a number, and the control.
**Quartermaster:** new: 86/86 bad cases exit 1, control exits 0 at both sizes. a4: identical results. Blank/null/number give 'PASTE <field> is missing or blank'; missing keys give KeyError and the empty list gives IndexError, all loud with exit 1.
**Quartermaster:** This covers Watchman's 9 B1 cases (rest en/th/ref empty, rest en space, rest en null, jw en/th empty, rest source missing, jw empty list).
**Quartermaster:** B1 reproduced on base f778b0bf: rest-en-empty changes page 37 (c0835bac to 907ddb17) and jw-th-space changes page 26 (26c1d9ce to 004aae5f) with no error. Note: build.py catches page errors per page, so base exit codes are always 0 in this harness and are not a B1 measure.
**Quartermaster:** A4 (runs/a4-test.txt): a PASTE copy whose weekly[0] repeats the rest ref. 70130b17 under python -O returns silently (exit 0); a4 exits 1 with or without -O. Control exits 0 for both, with and without -O.
**Quartermaster:** Static: added lines (2 in new, 5 in a4 vs f778b0bf) have 0 curly quotes, 0 Thai, 0 non-ASCII, no typed scripture (field names only). 0 curly quotes in either whole file.
**Quartermaster:** Side effects: audit hook over every build run shows 0 writes, 0 /tmp reads, 0 socket, subprocess, remove or mkdir events. TMPDIR was set to scratch/tmp/, which stayed empty. No __pycache__, .orig or .rej made.
**Quartermaster:** Read only, untouched: CURRENT-SNAP.txt f6dac2d0, PASTE 317e91ce, QM f778b0bf folder, Watchman's gate folder, live files. df was 76% before and after.
**Quartermaster:** Open advisories from Watchman's REPORT db7f76ae, not done here: A1 (PASTE md5 vs pointer), A2 (unescaped verse HTML), A3 (unclosed handle), A5 (PASTE outside snap).
**Quartermaster:** Ask: Watchman re-gate of new/play_v608.py 70130b17, and say whether the A4 variant b565920e should replace it.
**Quartermaster:** Ready to paste: none yet. CURRENT stays v5-37, `nancys-adventure-english-v5-37-PASTE.md` (acc534a51a922102ee37844e04d17955).
