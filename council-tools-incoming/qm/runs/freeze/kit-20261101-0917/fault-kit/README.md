**Auditor:** # Planted-fault kit v1.1 (owner: Auditor). Approved by Maxwell in Council, Nov 1, 2026 ("I'm actually fine with us executing on all those tools you guys mentioned").
**Auditor:** Purpose: every council tool must pass its case set here before Chancellor installs it into /workspace/council-tools/. Each case is a known-bad (or known-good control) input, an expected verdict, a one-line why, and the real incident it comes from.
**Auditor:** Status: a PATCH. It lives in /workspace/audit/fault-kit/ and ships as council-tools/incoming/auditor-fault-kit-v1.tar.gz. It edits no live council-tools file.

## How to run
**Auditor:** `python3 run_kit.py <tool-name> <path-to-tool> [--only ID,ID] [--keep]` with tool-name text_check, ground_check, tuft_check, freeze, quote_check or conflict_check.
**Auditor:** It prints PASS/FAIL per case, then a TOTAL line. Exit 0 only if every REQUIRED case gives its expected verdict; 1 if any required case fails; 2 for bad usage or a tool path that does not exist (NOT BUILT). Advisory cases print but never decide the exit. A case with expect RECORD is a recorded edge case: it prints as REC with the tool's result and is never graded.
**Auditor:** `python3 run_kit.py --self-test` runs the kit against deliberately broken stubs in stubs/ (always-pass, always-block, do-nothing freeze, never-flag, always-flag, no-hits, flag-everything; tuft_check never-flag and always-flag). The kit must report failure (exit 1) on every stub, and exit 2 on a missing path. `--list` prints case counts.
**Auditor:** Results go to runs/<tool>-<md5>-<time>-<pid>/results.json. Bulky scratch (fixtures, freeze sandboxes, the council-tools copy) is deleted after the run, only inside runs/. `--keep` keeps it.

## Safety rules the runner enforces
**Auditor:** - The tool under test is copied into runs/<run>/tool/ (plus text_check_words.json for text_check, hold_check.py for freeze) and only the copy is run.
**Auditor:** - freeze is only ever called with `--sandbox runs/<run>/sbx/<case>/sb` and `FREEZE_TOOLS` = a kit copy of council-tools (send_guard wrapped with the gate hook; current_snap.py given the one-line GATE_STEP6_FAIL plant for F7b). It is never run without --sandbox. The live pointer md5 is read before and after every case; if anything else moves it, the affected cases read FAIL.
**Auditor:** - text_check runs against a fixture pointer (CURRENT_SNAP env) in runs/, never the live pointer.
**Auditor:** - Nothing outside /workspace/audit/fault-kit/ is written or deleted. Never /tmp.

## Case sets (cases/<tool>/cases.json)
| tool | cases | required | interface the kit assumes |
|---|---|---|---|
| text_check | 30 | 28 | CLI with CURRENT_SNAP env; status column PASS/BLOCK/TEXT UNVERIFIED/SKIP; exit 0/1/2 |
| ground_check | 44 | 34 (+5 recorded) | module `check(path)` -> [] or problems; `mode: panels` cases are split at the cream gaps by cases/ground_check/panels.py and each panel is judged on its own |
| tuft_check | 6 | 5 (+1 recorded) | module `check(path)` -> reasons; FLAG = a reason starting with 'rock'. Scope Maxwell t545u: tufts only on grass, dots on dirt/path/sand/hill left alone |
| freeze | 34 | 34 | freeze.py --sandbox ...; exit 0/1/2; hold_check.py next to it |
| quote_check | 7 | 7 | NOT BUILT. Assumed `quote_check.py POST LEDGER SPEC`, `FLAG <KIND> <line>:` lines, exit 0/1/2 |
| conflict_check | 3 | 3 | `conflict_check.py PASTE LINE "new"`, hit lines contain `:<line> `, exit 0/1/2 |

**Auditor:** Dim rule for ground_check: a dimmed case is required when it is at or brighter than the real pause-card scrim (screen 48, x0.6). Stronger dims are advisory. This was fixed from the real scrim before any tool was run, not from tool results.
**Auditor:** quote_check and conflict_check: if the shipped interface differs from the assumed one, change only that tool's adapter in run_kit.py. Never change an expected verdict to fit a tool.

## How to add a case
**Auditor:** 1. Add an object to cases/<tool>/cases.json with a unique `id`, `expect`, `required` (true unless it is a stretch goal), a one-line `why`, and `source` naming the real incident (t-number, file path + md5, or report).
**Auditor:** 2. Planted images are built by tools/make_planted.py (tuft_check U01-U06, ground_check S01-path-in-panel1) from kit copies only; re-run it after changing a plant and record the new md5s. Put input files under cases/<tool>/ (copied in, never linked to the build; keep the kit under ~50 MB). text_check cases are built from data at run time (kinds: pair, sidecar_sheet, builder, copy, png_nosource, file). freeze cases are code in cases/freeze/freeze_cases.py: add a `@case('<id>')` function that calls rec('<id>', ...).
**Auditor:** 3. Run the kit on the live tool and any candidate, and record the result in CHANGELOG.md. A live tool failing a new case is a finding to report, never a reason to soften the case.
**Auditor:** 4. Re-run `--self-test`; it checks every case has why + source and unique ids.

## Files
**Auditor:** run_kit.py (runner), cases/ (6 case sets + inputs), tools/make_planted.py, stubs/ (broken tools for --self-test), README.md, CHANGELOG.md. Input files and their sources are listed in CHANGELOG.md.
