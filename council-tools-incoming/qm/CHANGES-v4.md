**Quartermaster:** # CHANGES v4 (qm incoming tools, Nov 1, 2026, ~2:22 AM MST)
**Quartermaster:** Based on: snap-r2h-0021MDT, pointer f6dac2d0, PASTE 317e91ce. Answers Auditor gate L1-0207 (REPORT c12ad3ab). Patch only: nothing live was changed, nothing was installed, nothing was deleted.
**Quartermaster:** v3 copies are parked as quote_check.v3.py, selftest_quote_check.v3.py, README-quote_check.v3.md, CHANGELOG.v3.md, README.v3.md and MANIFEST.v3.md5 (51f60a20). The v1 and v2 copies are kept.

## quote_check.py (39fb4671 -> b7c6479e)
**Quartermaster:** A2 fix: in classify()'s OWN branch, the `for t in own:` loop no longer returns ALTERED at the first text that holds the quote mid-sentence. Every own text for the t-number is tried first. It returns VERBATIM if any one is a whole match, and ALTERED-cut only after all were tried. The ALTERED detail names the shortest holding text (ties broken by text), so it doesn't depend on order either.
**Quartermaster:** A3 fix: load_records now builds `texts = sorted({...})`, so the order of a row's quotes no longer changes with PYTHONHASHSEED. With the A2 fix the verdict doesn't depend on order anyway.
**Quartermaster:** Unchanged: the spec path (T6 every-match), WRONG-TNUM, RELAY/PARAPHRASE order, Thai at 6+ characters, exit codes, and scratch under qm/runs/quote_check/.

## selftest_quote_check.py (57bec4b1 -> see MANIFEST)
**Quartermaster:** 9 new cases (64 total, was 55). A2, A3, A3b (short row listed first) and controls A1, A2-cut, A3-cut, A4 and A7 each run under 6 hash seeds (0, 1, 2, 7, 13, 40) and must give one identical output. There's also a source check that texts are sorted and the early-return loop is gone.

## Test runs (scratch only under qm/runs/, never /tmp, PYTHONDONTWRITEBYTECODE=1)
**Quartermaster:** Self-test 64/64. Seed sweep: the whole self-test was run under PYTHONHASHSEED=0..40, giving 41/41 exit 0 and 41/41 identical output (scratch-path line excluded). Folder: runs/quote_check/v4-seed-sweep-20261101-091853UTC/ (that name is in UTC; it's 02:18 MST).
**Quartermaster:** Auditor's cases were run on unchanged copies of run_quote_cases.py d4235f49 and run_new_cases.py d0b1d69d, with data copies of ASKS-LEDGER c7461aa0, SETTLED-RULINGS 3385706f (current live; the gate used 8d8aeff5, which is also copied there) and PASTE 317e91ce. Results: required 36/36 and advisory 1/3 (the same known misses, Q05c and Q06c), and new 17/17 (was 15/17). In the runner's output, the "v3" column is this v4 file. Folder: runs/quote_check/gate0207-rerun-v4-20261101-022035MST/.
**Quartermaster:** A1-A7 were also swept on PYTHONHASHSEED=0..40: v4 gives one output per case. v3 39fb4671, run alongside, reproduces the gate fails: A2 ALTERED x41, and A3 VERBATIM x22 / ALTERED x19.
**Quartermaster:** Fault kit v1.1 (run_kit 222ef325), quote_check only: 7/7, KIT PASS. Its results are at /workspace/audit/fault-kit-v1.1/runs/quote_check-b7c6479e-20261101-022154-2573116/. It wrote only inside the kit's runs/, and /tmp was unchanged before and after.
**Quartermaster:** Note: qm/__pycache__/ is stale bytecode from earlier QM runs. It is not a shipped file and is not in the MANIFEST. It was left in place (not deleted), and v4 runs used PYTHONDONTWRITEBYTECODE=1.
**Quartermaster:** Ready to paste: none yet. CURRENT stays v5-37, `nancys-adventure-english-v5-37-PASTE.md` (acc534a51a922102ee37844e04d17955).
