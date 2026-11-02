**Quartermaster:** # CHANGES v3 (qm incoming tools, Nov 1, 2026, ~2:10 AM MST)
**Quartermaster:** Based on: snap-r2h-0021MDT, pointer f6dac2d0, PASTE 317e91ce. Answers Auditor gate L1-0200 (REPORT ea2e76f0). Patches only: nothing live was changed, nothing was installed, nothing was deleted.
**Quartermaster:** v2 copies are parked as <name>.v2.py / <name>.v2.md / MANIFEST.v2.md5. The v1 copies are kept.

## quote_check.py (e6deb411 -> see MANIFEST)
**Quartermaster:** Fixes T6 (required). `at_sentence_edges` now tries every match of the quote in the text, not just the first (`k.find`). `check_spec` no longer stops at the first PASTE line that holds the quote. It returns SPEC-VERBATIM as soon as any match is a whole value or whole sentence. It returns SPEC-CUT only if no match anywhere is.
**Quartermaster:** "ขนมปัง" now gives SPEC-VERBATIM, exit 0. Its first match is inside the verse word …มีขนมปังบาร์เลย์… at PASTE :427; a later match on the same line is the whole value `"th":"ขนมปัง"`.
**Quartermaster:** Unchanged: the leading '9.' / '- ' strip, WRONG-TNUM, Thai checked at 6+ characters, the SPEC-ALTERED and SPEC-NOTFOUND paths, and exit codes.
**Quartermaster:** Side effect, by design: Maxwell quotes checked against ledger rows use the same every-match rule. All Q/E gate cases are unchanged.
**Quartermaster:** New self-test cases:
**Quartermaster:** - T6 gives SPEC-VERBATIM.
**Quartermaster:** - T6b "ขนมปัน" gives SPEC-ALTERED.
**Quartermaster:** - T6c "ขนมปังบาร์", which appears only inside a longer word, still gives SPEC-CUT.
**Quartermaster:** - Two ASCII cases, "Thai Review Queue" (first match mid-sentence at :246) and "Colors and Shapes" (first match in the zone-tint row), give SPEC-VERBATIM.
**Quartermaster:** - Control: the rule 9 cut still gives SPEC-CUT.
**Quartermaster:** Open limits from the v2 README are unchanged (advisory): Q05c and Q06c.

## send_log.py (7661e485 -> see MANIFEST)
**Quartermaster:** Cosmetic fix. When `check <path>` finds that the path was logged under another md5, the first line now reads "SENT AS OTHER VERSION: this version (md5 …) has no row in …; an earlier version of this path was sent". Before, it said "NOT SENT: …".
**Quartermaster:** The PATH SENT AS OTHER VERSION block and exit 3 are unchanged. A bare md5 with no row still prints NOT SENT, exit 0. The self-test S1 line was updated to match.

## disk_watch.py (2c77cb6f -> see MANIFEST)
**Quartermaster:** Cosmetic fix. The "[SIMULATED x%, real y%]" bracket now uses the same rounded-down `shown()` as the main line: 79.99 shows 79.9%, and 80 shows 80.0% and warns. The threshold and exit codes are unchanged.
**Quartermaster:** 4 self-test cases were added.

## Test runs (scratch only under qm/runs/, never /tmp)
**Quartermaster:** Self-tests: send_log 29/29, disk_watch 24/24 (was 20), base_check 15/15, quote_check 55/55 (was 49).
**Quartermaster:** Auditor's required quote cases (copy of run_quote_cases.py d4235f49 with only the TOOL path changed, on copies of ASKS-LEDGER c7461aa0, SETTLED-RULINGS 8d8aeff5 and PASTE 317e91ce): 36/36 required, advisory 1/3, the same misses as before (Q05c, Q06c). The fault-kit quote posts give 7/7 and were read-only.
**Quartermaster:** Auditor's send_log and disk_watch planted cases.sh were re-run on copies under qm/runs/<tool>/gate0200-cases-20261101-020626MST/. All give the expected verdicts and exit codes.
**Quartermaster:** Ready to paste: none yet. CURRENT stays v5-37, `nancys-adventure-english-v5-37-PASTE.md` (acc534a51a922102ee37844e04d17955).
