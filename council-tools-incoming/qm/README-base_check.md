**Quartermaster:** # base_check.py: check a post's Based on line (patch)
**Quartermaster:** Run: `python3 base_check.py "<post text>"` or `python3 base_check.py --file post.md` (stdin works too).
**Quartermaster:** Parses each 'Based on:' line (snap name, pointer md5 prefix, PASTE md5 prefix; extra stage MANIFEST or tool md5s are ignored) and compares with /workspace/v608build/CURRENT-SNAP.txt: snap= value, pointer = md5 of that file, PASTE = paste_1b_md5.
**Quartermaster:** MATCH (exit 0). STALE (exit 1) names each mismatch or missing field and prints the live base. MISSING (exit 1) when the post has no Based on line, with the live base to copy.
**Quartermaster:** Several base lines in one post are each checked; any STALE fails the post.
**Quartermaster:** Override for tests: `--snap-file PATH`.
**Quartermaster:** Self-test: `python3 selftest_base_check.py`.
