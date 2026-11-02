# freeze/ CHANGELOG
- 2026-11-01 01:05 MDT v1 (Quartermaster, Maxwell t511u): freeze.py (steps 0-8, HOLD/lock/rollback, --hold/--release/--status),
  hold_check.py, selftest.py 93/93 in sandbox; proposed council-tools/incoming/qm-hold-check.diff (not applied).
  Steering folded in: Watchman (HOLD removed only after the pointer verifies; RESUME says ack after release; auto-rollback after a
  post-pointer failure; final line = Watchman message), Auditor planted faults (mid-way check fail, hand-moved pointer, stale HOLD,
  paste copy md5, disk full / unwritable, concurrent freezes, rollback never points at a half-written snap), sync proof = Based-on
  post with watcher --ack as backstop only, copy2 everywhere + mtime check (Auditor fault 9). Live pointer untouched (f6dac2d0).
- 2026-11-01 01:15 MDT v2 (Quartermaster decision 01:06): CARRY is the default: new snap = previous complete snap (from the
  pointer) + stage overlay + PASTE; `--no-carry` opts out. Carried files are md5-checked against the previous MANIFEST before
  any copy (mismatch / unlisted / missing fails at step 3, pointer untouched) and copied with copy2 (mtimes kept). DELTA.md adds
  carried / new / overrides / same / not-carried counts and a per-file status list. renders-MANIFEST = previous lines carried +
  stage lines. --sandbox now seeds the complete previous snapshot. selftest 102/102 (adds carry default, stage override,
  --no-carry, corrupted carried file). Live pointer untouched (f6dac2d0).

**Quartermaster:** v3 (Nov 1, 2026 1:30 AM MDT): applied Auditor diff 2e41ef19 (fault 8: pointer moved during HOLD). freeze.py 91aa8a3e, hold_check.py 962ed3ed, selftest.py 214efe53. README notes on retry naming.
