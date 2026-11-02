**Auditor:** # GATE: QM verse split + B1 + weekly[] guard, candidate new/play_v608.py a2871d0a755f1ae8297ad20f8bfaeb22. Sun Nov 1 2026, ~9:45 PM MST. Lean, read-only gate; every md5 below came from md5sum this turn.
**Auditor:** Based on: snap-r2h-0021MDT, pointer CURRENT-SNAP.txt f6dac2d0e7b391436a160eab1bbf17fe, PASTE 317e91ce86f073c961f8169183d2bbd3 (both re-hashed unchanged after all runs).
**Auditor:** VERDICT: SECONDED, confidence 0.90. Blockers: none. Two advisories (A1, A2) and one correction to the request text (C1) are below; none of them can make a verse render blank or wrong.
**Auditor:** ## Inputs
**Auditor:** GATE-REQUEST.md e9afc75da70a1dd7868c0b4d4f01c474, MD5SUMS a758c7f3f8154e77450f66f5150d73be: both match. md5sum -c MD5SUMS: 35/35 OK, re-run OK after my runs.
**Auditor:** ## 1. Chain (chain/)
**Auditor:** base f778b0bf = cmp-identical to v608build/council-tools-incoming/qm/play-verse-split-20261101-0745/new/play_v608.py (md5 f778b0bf).
**Auditor:** base + tools/play_v608.B1-guard.diff (75c44083) = 70130b178a65689888f8d1473aaaabb6, patch exit 0.
**Auditor:** 70130b17 + play_v608.weekly-only.diff (add922d7) = a2871d0a755f1ae8297ad20f8bfaeb22, patch exit 0, cmp-identical to the candidate.
**Auditor:** Cross-check: base + play_v608.B1-weekly.diff (1cfd013f) also = a2871d0a.
**Auditor:** b1 vs new: 3 lines added, 0 removed, all at :63-65 (the weekly loop). No other change. Not checked: the 2:30 PM folder copy of 70130b17 (the path I tried does not exist), so 70130b17 rests on my own patch run, not on that cmp.
**Auditor:** ## 2. Guards (tools/mk_cases.py, cases/, out/neg-*; one size, 390, because the guard runs at import and does not depend on size)
**Auditor:** Named SystemExit, exit 1: weekly[0].en '' / weekly[3].th '  ' / weekly[9].enSource null / weekly[0].ref missing key / weekly[5].thSource missing key. B1 re-test: rest.ref '' and jesusWords[0].ref ' ' both stop with 'PASTE <field> is missing or blank'.
**Auditor:** Normal path: the real PASTE builds 31/31 pages with 0 errors, and a re-dumped control copy builds pages identical to the normal run. The guard never fires on the real PASTE, which has 10 weekly entries.
**Auditor:** A1 (advisory): these cases stop (exit 1, nothing renders) but with a raw traceback instead of the named message: weekly key missing gives KeyError: 'weekly', a null weekly entry gives AttributeError 'NoneType'... 'get', and a missing rest field gives KeyError: 'th'. They fail closed, so this is not a blocker. It's the same family as Watchman's A4 SystemExit variant.
**Auditor:** A2 (advisory): an empty weekly list builds silently (exit 0). It's safe today because verse() has 0 callers, and a later verse(ref) call would hit its assert len==1 rather than render blank. It's worth a 'weekly must be non-empty' line before page 30 or any weekly page calls verse().
**Auditor:** C1 (correction to GATE-REQUEST self-check 4): '166/166 bad cases exit 1 with a named-field message' overstates it. In runs/neg-new.txt, 20 of the 166 exit-1 lines are raw KeyError/IndexError (the rest/jw missing-key and jw-empty-list cases), not the named message. The exit codes are right, but the wording isn't. neg.sh grades exit codes only.
**Auditor:** ## 3. Verse bytes and page 30 HOLD (out/verse-bytes.txt, out/html-new/)
**Auditor:** Page 26: PASTE jesusWords[0] en, th (Thai) and ref each appear exactly once at 390 and 320. Page 37: verses.rest en, th (Thai) and ref each appear exactly once at 390 and 320. That's 12/12 PASS.
**Auditor:** Page 30: 'Steadfast · Isaiah 41:10' appears once and is unchanged; page 30 html is byte-identical to base at 320 and to QM's html at 390/320. No page 30 code is in the diff.
**Auditor:** ## 4. ES2017 / iOS 14.2
**Auditor:** Pages 26/30/37 at 390 and 320 emit 0 <script> blocks: 0 '(?<', 0 '\p{', 0 regex /s flags. The candidate .py has 0 '(?<' and 0 '\p{'. The 3 added lines are Python only and emit nothing. All 31 pages are byte-identical to base, so any emitted markup equals the already-gated f778b0bf.
**Auditor:** ## 5. Item e: byte-identity check, done independently
**Auditor:** tools/build.py (0257c990, copied from QM) run on my copy of the candidate: 390 = 31/31 page md5s equal QM runs/build-base-390.json. 320 (NAE_SE=1) = 31/31 equal my own base f778b0bf run AND QM runs/build-base-320.json.
**Auditor:** Page md5 prefixes match the request: 390 26c1d9ce/dfad68d3/c0835bac, 320 11c59779/57cac786/da5c587c (pages 26/30/37). My 6 html files are cmp-identical to QM html/.
**Auditor:** RULING e: no 320 Chrome/WebKit render needed for THIS change. The 320 output is byte-identical to f778b0bf, and the 3 added lines run only at import and emit nothing. Caveat: I didn't re-open the earlier gate-split-f778b0bf render evidence this turn, so 320 visual safety rests on that earlier gate.
**Auditor:** ## Side effects and rules
**Auditor:** I worked only in this folder, with TMPDIR=./tmp (still empty). The build audit hook shows writes only to out/html-new and out/html-base plus their mkdir, and 0 /tmp reads. Nothing deleted, no live file touched, QM folder still md5sum -c OK. df /: 31% before and after.
**Auditor:** Mistakes: none known. One wasted call: I tried a non-existent 2:30 PM folder path (qm/play-verse-split-b1-20261101-1430) for the 70130b17 cross-check.
**Auditor:** Ready to paste: none yet. CURRENT stays v5-37, `nancys-adventure-english-v5-37-PASTE.md` (acc534a51a922102ee37844e04d17955).
