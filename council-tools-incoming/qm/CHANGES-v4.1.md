**Quartermaster:** # CHANGES v4.1 (qm incoming tools, Nov 1, 2026, Mountain time)
**Quartermaster:** Based on: snap-r2h-0021MDT, pointer f6dac2d0, PASTE 317e91ce. Answers Auditor gate L1-0226-qcv4 B1 (REPORT 6aca72cd). This is a patch only. Nothing live was changed or installed, nothing was deleted, and no shared file was edited (SETTLED-RULINGS 3385706f and ASKS-LEDGER c7461aa0 are untouched).
**Quartermaster:** The v4 copies are parked as quote_check.v4.py (b7c6479e), selftest_quote_check.v4.py (f3d870a1), README-quote_check.v4.md, CHANGELOG.v4.md, README.v4.md and MANIFEST.v4.md5 (f7c05ac1). The v1-v3 copies are kept.

## quote_check.py (b7c6479e -> 5de0eaa5, diff +31 / -3)
**Quartermaster:** B1 fix: load_records() handles a MAXWELL OWN row whose label is a bare `**Maxwell:**` (empty bracket). The new bare_row_tnums() takes the t-numbers from the same row first: this segment outside its quoted span (first to last straight double quote, the same span load_records reads as text), plus any cell of the line with no label. If there are none, it uses the t-numbers of the nearest `#` heading above, and each heading resets them. Every t-number found is kept, so a cite of any of them matches and none is guessed. If none is found, tnums stays empty, exactly as in v4.
**Quartermaster:** On live data, only two records change: SETTLED-RULINGS.md:166 goes from empty to t560u (from the A27 heading) and :168 goes from empty to t561u (from the row). On the gate data 8d8aeff5, no record changes (147/147 identical).
**Quartermaster:** A VERBATIM on such a row adds "(bare **Maxwell:** label; t-number read from the row/heading)". Verdicts, exit codes, the spec path, RELAY/PARAPHRASE order, WRONG-TNUM and scratch under qm/runs/quote_check/ are unchanged.

## selftest_quote_check.py (f3d870a1 -> 131cc43f, +63 lines)
**Quartermaster:** 17 new checks (81 total, was 64), on a synthetic ledger in the self-test scratch. 10 B1 cases run on 4 hash seeds with identical output:
- a row t-number with a correct cite gives VERBATIM, and the whole-row text names "row"
- a heading t-number gives VERBATIM and names "heading"
- a wrong t-number gives WRONG-TNUM naming t920u, and a heading row cited with another row's t-number gives WRONG-TNUM
- with two t-numbers on one row, either one gives VERBATIM, and neither gives WRONG-TNUM "cite t923u, t924u"
- a table t-number in an unlabelled cell gives VERBATIM
- a bare label with no t-number gives VERBATIM with the hint
**Quartermaster:** Three controls must give output byte-identical to v4: a bare label with no t-number anywhere, cited or not cited, and a t-number that appears only inside the quote under a reset heading. Three checks run on the live A27 rows: t561u :168 gives VERBATIM, t560u with the whole :166 text gives VERBATIM, and t561u words cited as t560u give WRONG-TNUM. There is also one source check.

## Test runs (folder runs/quote_check/v41-20261101-023925MST/, PYTHONDONTWRITEBYTECODE=1, never /tmp)
**Quartermaster:** Self-test 81/81. Seed sweep of the whole self-test on PYTHONHASHSEED=0..40: 41/41 exit 0, and 41/41 identical output with the scratch line excluded (md5 6874ba72).
**Quartermaster:** Auditor's runners were run unchanged, as copies: run_quote_cases.py d4235f49 and run_new_cases.py d0b1d69d. They used data copies of ASKS-LEDGER c7461aa0 and PASTE 317e91ce, with SETTLED-RULINGS 8d8aeff5 (gate data) and 3385706f (live), in gate-8d8aeff5/ and gate-3385706f/.
- **Planted:** required 36/36 and advisory 1/3 on both (the known Q05c and Q06c). The output is byte-identical to Auditor's L1-0226 results: 8d7b3d73 on 8d8aeff5 and 23b15d03 on 3385706f.
- **New cases:** 17/17 on both. The v4.1 column is identical to Auditor's. Only the comparison column differs, because the "v2" slot in these copies holds v4 b7c6479e, not v2.
**Quartermaster:** The A27 check (a27-check.txt a2fde2f6) runs v4.1 and v4 on the live-data copy:
- `**Maxwell (t561u):** "Keep everything else the same"` gives VERBATIM on v4.1, where v4 gave WRONG-TNUM.
- `**Maxwell (t560u):**` with the whole :166 text gives VERBATIM on v4.1, where v4 gave WRONG-TNUM.
- The :168 full text comes back as two pieces because of its nested "urgent" quotes. Both are VERBATIM on v4.1, where v4 gave WRONG-TNUM on both.
- The cut t560u fragment "if he finds anything crazy, urgent, or a big deal" stays ALTERED (cut mid-sentence), which is correct.
- Crossed t-numbers give WRONG-TNUM, naming the right one.
**Quartermaster:** Still open: when a bare row has no t-number anywhere and the post cites one, the result is still WRONG-TNUM with an empty "cite " (unchanged by design). Nested straight quotes in a post split the quote. B2 is unchanged.
**Quartermaster:** Ready to paste: none yet. CURRENT stays v5-37, `nancys-adventure-english-v5-37-PASTE.md` (acc534a51a922102ee37844e04d17955).
