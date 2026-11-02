**Quartermaster:** # GATE REQUEST: cards 1A fix (TINY CHANGE, one quick Auditor check per t617u). Folder /workspace/qm/cards-fix-20261102-0704/ (built Mon Nov 2 2026, ~12:04 AM MST).
**Quartermaster:** Based on: snap-r2h-0021MDT, pointer f6dac2d0, PASTE 317e91ce
**Quartermaster:** Source (unchanged): /workspace/qm/cards-flexgap-20261102-0519/new/nancys-adventure-english-v6-08-1B-v32-cards1A-PASTE.md 55e277dc77a3a1079d6c2f019a5a652f (187,987 chars). Fixes from Auditor REPORT 48fce81f.
**Quartermaster:** Candidate: new/nancys-adventure-english-v6-08-1B-v32-cards1A-fix-PASTE.md 5e1666fe6f7189d3886686749335b3ee, 188,007 Python chars (213,241 bytes), bank 193 of 188,200.
**Quartermaster:** Exactly 3 changes (p-diff.txt 67d7fdf6, diff -u exit 1, 3 hunks, lines 289/375/427 only):
**Quartermaster:** 1. P-B1 (:427, +10): ms-28 'Here is your key.' / นี่กุญแจของคุณค่ะ / 'HEER iz yor KEE' becomes 'Your room is ready.' / ห้องของคุณพร้อมแล้วค่ะ / 'yor ROOM iz RED-ee' (SHEET-v5 e53b55dc :42 tile 7A, byte-for-byte). Basis: Maxwell t640u "You can resume I have backup credits", best read of the open card; he can say "overwrite". No meta/spec edit needed (:369 says only "the hotel"; needsMaxwell unchanged).
**Quartermaster:** 2. P-B2 (:375, 0): '201 of the 207 written cards' becomes '205 of the 211 written cards'. Recount: 211 written, 205 NEEDS NANCY.
**Quartermaster:** 3. R-A4 advisory (:289, +10): 'Safari 14 CSS: no aspect-ratio, :has(), color-mix() or container queries.' becomes '... color-mix(), container queries or flex gap.'
**Quartermaster:** Self-check (self-check.txt d8e25f7b, python exit 0): 429/429 lines; only 289, 375, 427 differ; JSON parses; 211 cards, 211 unique ids; only ms-28 changed; verses, jesusWords, jesusWordsFallback, meta, zones, needsMaxwell equal; reverse-applying the 3 edits gives a file byte-identical to 55e277dc (so verses are byte-identical).
**Quartermaster:** Rules: no CSS/Thai size lines touched (Thai 17px+/1.7 unchanged); page 30 untouched; no surnames, no contact info in new text; ms-28 4 words; nm-04 still has 'Here is your key.' as a wrong choice only. df / 32%. No /tmp, nothing deleted.
**Quartermaster:** Ask: SECONDED / NOT SECONDED on these 3 changes only.
**Quartermaster:** Ready to paste: none yet. CURRENT stays v5-37, `nancys-adventure-english-v5-37-PASTE.md` (acc534a51a922102ee37844e04d17955)
