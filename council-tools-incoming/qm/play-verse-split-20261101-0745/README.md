**Quartermaster:** # play-verse-split: pages 26 and 37 only, from candidate 72b0d50d. Page 30 is left exactly as ee74f3ef, held for Maxwell's 1A/1B/1C pick. Nov 1 2026, about 7:45 AM MST. Nothing installed, nothing deleted.
**Quartermaster:** Based on: snap-r2h-0021MDT, pointer f6dac2d0, PASTE 317e91ce, base play_v608.py ee74f3ef.
**Quartermaster:** Built by make_split.py, which is make_candidate.py minus the two weapon_gift replacements. The unused verse() helper stays in, and page 30 doesn't call it.
**Quartermaster:** html: pages 26 and 30 are byte-identical to the old renders at all 3 sizes. Page 37 is byte-identical to candidate 72b0d50d at all 3 sizes.
**Quartermaster:** byte_check: 24 PASS and 6 FAIL. The 6 FAILs are all page 30 (Isaiah 41:10 en and th missing at 3 sizes), which is the held design, so they're expected. byte_check doesn't check order yet (Auditor finding 2).
