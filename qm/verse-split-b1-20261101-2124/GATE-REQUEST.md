**Quartermaster:** # GATE-REQUEST: page 26/37 verse split + Watchman B1 guard + weekly[] guard. Sun Nov 1 2026, 9:24 PM MST. Maxwell card answer: "Just the verse split tonight, you plus Auditor". Quick Auditor check asked (t617u tiny-change rule takes effect at the Nov 5 RESUME, so Auditor may pick full or quick).
**Quartermaster:** Based on: snap-r2h-0021MDT, pointer f6dac2d0, PASTE 317e91ce
**Quartermaster:** ## Files (md5, all hashed on disk this turn)
**Quartermaster:** base/play_v608.py f778b0bfcb9c0f707ab14a5ef9758c38 = byte copy of v608build/council-tools-incoming/qm/play-verse-split-20261101-0745/new/play_v608.py (the split Watchman gated NOT SECONDED 0.90 on B1).
**Quartermaster:** tools/play_v608.B1-guard.diff 75c44083b6f69216f87e2eb0d3f0d22d = byte copy of Watchman's diff (from qm/play-verse-split-b1-20261101-1430/tools/).
**Quartermaster:** b1/play_v608.py 70130b178a65689888f8d1473aaaabb6 = f778b0bf + 75c44083 (patch exit 0); cmp-identical to the 2:30 PM QM folder's new/play_v608.py 70130b17.
**Quartermaster:** new/play_v608.py a2871d0a755f1ae8297ad20f8bfaeb22 = CANDIDATE = 70130b17 + weekly[] guard (3 added lines, 0 removed). vs f778b0bf: 5 added, 0 removed.
**Quartermaster:** Diffs: play_v608.weekly-only.diff add922d7 (vs 70130b17), play_v608.B1-weekly.diff 1cfd013f (vs f778b0bf). Full list in MD5SUMS.
**Quartermaster:** ## What changed
**Quartermaster:** 1. Watchman B1 guard as written: at import, verses.rest ref/en/th/enSource/thSource and jesusWords[0] ref/en/th must be non-blank strings, else SystemExit 'PASTE <field> is missing or blank'.
**Quartermaster:** 2. Critique item: the same guard over every verses.weekly[] entry (ref/en/th/enSource/thSource). Loop vars _i/_wv/_f are new module names (0 prior uses). All 10 real weekly entries pass.
**Quartermaster:** Behaviour is fail-loud, not a fallback text: a fallback would need typed scripture, which the byte-identical rule forbids. A blank field stops the build, so it can never render blank.
**Quartermaster:** Added lines: ASCII only, 0 Thai, 0 curly quotes (whole file 0), field names only, no verse text.
**Quartermaster:** ## Self-checks (tools/build.py 0257c990 = Watchman gate harness, Python only; TMPDIR=scratch/tmp stayed empty)
**Quartermaster:** 1. Rebuild PASS: 31 pages x 3 sizes (390x844, 375x667, 320x568 NAE_SE=1), 0 errors, every run exit 0. b1 and new: 93/93 page outputs byte-identical to f778b0bf (runs/build-*.json).
**Quartermaster:** 2. Page md5s PASS (same as Watchman's table): 390 26c1d9ce/dfad68d3/c0835bac, 375 51ac07b1/4860981c/287bffca, 320 11c59779/57cac786/da5c587c for pages 26/30/37.
**Quartermaster:** 3. Verse bytes PASS (runs/verse-bytes.txt): in html/ for all 3 sizes, PASTE jesusWords[0] en/th/ref appear exactly once on page 26 and verses.rest en/th/ref exactly once on page 37 (18/18 PASS).
**Quartermaster:** 4. B1 negative cases PASS (runs/neg-*.txt, 84 PASTE copies x 2 sizes = 168 runs per variant): new = 166/166 bad cases exit 1 with a named-field message, control exit 0 at both sizes.
**Quartermaster:** Cases: 44 from Watchman/QM make_cases.py 4b001e5a (rest and jw[0] fields as empty/space/wsmix/null/missing, jw empty list, rest missing, rest.en number) + 40 new weekly cases (tools/make_weekly_cases.py, weekly[0] and [9], 5 fields x empty/space/null/missing).
**Quartermaster:** B1 reproduced on base f778b0bf: 0/168 exit 1 (all silently build). b1 70130b17: 86 exit 1, but all 80 weekly runs still exit 0, which is the gap the weekly guard closes.
**Quartermaster:** 5. Page 30 HOLD PASS: page 30 bytes unchanged at all 3 sizes (dfad68d3/4860981c/57cac786), 'Steadfast · Isaiah 41:10' line untouched, no page 30 code touched.
**Quartermaster:** 6. Side effects PASS: audit hook shows 0 writes and 0 other events for base/b1 runs; new runs' only writes are the 9 html/ files plus their os.mkdir. 0 /tmp reads. CURRENT-SNAP f6dac2d0 and PASTE 317e91ce re-hashed unchanged after.
**Quartermaster:** 7. 320px render: NOT RENDERED this turn. Headless Chrome screenshots timed out (exit 124, likely the long-path socket limit render.py warns about); python playwright isn't installed. 320 layout, Thai 17px / line-height 1.7 and Safari 14 safety rest on byte-identity: the 320x568 output equals f778b0bf, which Auditor's gate-split-f778b0bf already checked.
**Quartermaster:** Note: the brief said the page 37 verse is hard-coded at :318. In this file page 37 reads PJ['verses']['rest'] (:337 in new). The only typed verse-ish label is page 30's 'Steadfast · Isaiah 41:10' (HELD).
**Quartermaster:** ## Auditor, please verify
**Quartermaster:** a. md5s above; new = b1 + only the 3 weekly lines (play_v608.weekly-only.diff).
**Quartermaster:** b. Re-run tools/build.py on new/ at 390/375/320: 93/93 identical to f778b0bf.
**Quartermaster:** c. Re-run tools/neg.sh new: 166 exit 1, control exit 0. Spot-check that the weekly guard can't fire on the real PASTE.
**Quartermaster:** d. Page 30 HOLD bytes unchanged; verse bytes for 26/37 match PASTE 317e91ce.
**Quartermaster:** e. Rule on whether a 320 Chrome/WebKit render is needed before Maxwell sees it, or whether byte-identity is enough.
**Quartermaster:** Open, not done: Watchman A1-A5 advisories (A4 assert to SystemExit variant b565920e is in the 2:30 PM folder, not in this candidate).
**Quartermaster:** Ready to paste: none yet. CURRENT stays v5-37, `nancys-adventure-english-v5-37-PASTE.md` (acc534a51a922102ee37844e04d17955).

**Quartermaster:** CORRECTION (C1, Auditor gate 4777bece): of the 166 negative runs, 146 stopped with a named-field message and 20 stopped with KeyError/IndexError crashes. All 166 exited non-zero and none rendered; neg.sh checks exit codes only.
**Quartermaster:** Gate result: Auditor SECONDED a2871d0a at 0.90, no blockers. Advisories A1, A2 and C1 are logged as follow-ups.
