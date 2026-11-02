#!/usr/bin/env python3
# Instructor (QM support), v6-08 r2h candidate, Nov 1, 2026 MDT. Maxwell t466u (QM-relayed): the zone chooser (showcase tile 5)
# is dropped; every run mixes sight words, phonics and numbers by location (scene) and time-of-day step. FULL = LEAN (anchors 1-4,
# anchor 4 extended with time-of-day moments) + 5 the morning front desk takes the hotel
# sight/number cards + 6 Echo Forest: each Sound Duel round mixes number, sight-word and sound pairs. Spec text only, 0 new Thai.
# Target: 1A PASTE 106a066103da9713220a5e7d6c4285cf (snap-r2g-2326MDT). Never edits a build file.
# Usage: python3 instructor-zone-mix-full.py [--paste IN]                 dry run (default; prints chars and delta, writes nothing)
#        python3 instructor-zone-mix-full.py [--paste IN] --apply OUT     writes the result to OUT (OUT must differ from IN)
#        python3 instructor-zone-mix-full.py --check-anchors FILE ...     anchor counts in any file (no md5 assert, never writes)
import sys, os, hashlib
SRC = '/workspace/v608build/snap-r2g-2326MDT/nancys-adventure-english-v6-08-PASTE.md'
MD5S = {'106a066103da9713220a5e7d6c4285cf','2eebff944f7c30ac2e13fdc8e888d398','fca9ce69a1f1d5e556e8414efc524a18','24934ef11a870ebe381e9923dc31bfdd'}  # 1A, 1B, 1A+Shop, 1B+Shop
MD5 = '106a066103da9713220a5e7d6c4285cf'
LIMIT = 188200
E = [
 # rule 4 (:27): Home Lake's day-one zones no longer open a chooser
 ("Maxwell Says and Kitchen open day one, bright on the faded Home Lake (its row opens their chooser).",
  "Maxwell Says and Kitchen open day one, bright on the faded Home Lake (its row runs them)."),
 # section 3 One style (:121)
 ("the hub and choosers use the Map's sky sheet and scenery strips;",
  "the hub uses the Map's sky sheet and scenery strips;"),
 # 6.3 Taps (:175): a row starts one run; zones take turns, so first launch is still Phonics and the Word guardian comes on run 2
 ("a row opens its zone, or a chooser with one plate per zone (zone `name`/`nameTh`) when it holds two or three;",
  "a row runs its open zone with fewest `zoneRuns` (ties: `mapLayout` order);"),
 # 7 Core loop (:211): the mix by location (scene k = object layout k) and the ramp by time-of-day step (7.1)
 ("A **run** is 5 find-and-tap scenes × 5 cards from one zone (7.1), then its guardian (10).",
  "A **run** is 5 find-and-tap scenes × 5 cards (7.1), then its zone's guardian (10). Mixed (t466u): scenes 1, 5 its zone; 2 `sw`, 3 `ph`, 4 `nm`; time steps 4–5 (7.1) lead with own-`en` asks. First: steps 1–2 Word Meadow `nm` nm-03, nm-04, nm-23; 4–5 Golden Fields `nm` nm-06, nm-24; 5 Home Lake `ph` ph-01–ph-03, ph-25, ph-26."),
 # 7.1 Front desk (:227): the morning desk carries the hotel sight-word and number lines
 ("(only them in that scene, repeats filling it)",
  "(only them, and at steps 1–2 as Home Lake scenes 2, 4 sw-01, sw-02, nm-01–nm-04 (nm-01 = its door); repeats filling it)"),
 # 12 Sound Duel (:322): Echo Forest mixes too (30 pairs: 4 number, 5 sight-word, 21 sound)
 ("Rounds of 8 pairs, untimed, no score, can't be lost.",
  "Rounds of 8 pairs (2 number, 2 of they/she/it/mine/bus; `pics` first at steps 1–2), untimed, no score, can't be lost."),
]
def md5(s): return hashlib.md5(s.encode('utf-8')).hexdigest()
def check_anchors(paths):
    for p in paths:
        t = open(p, encoding='utf-8').read()
        print(f'{p}: md5 {md5(t)}, {len(t)} chars')
        for i, (old, new) in enumerate(E, 1):
            print(f'  anchor {i}: old x{t.count(old)}, new x{t.count(new)}  {old[:60]!r}')
def main():
    a = sys.argv[1:]
    if '--check-anchors' in a:
        check_anchors(a[a.index('--check-anchors') + 1:]); return
    src = a[a.index('--paste') + 1] if '--paste' in a else SRC
    out = a[a.index('--apply') + 1] if '--apply' in a else None
    t0 = open(src, encoding='utf-8').read()
    assert md5(t0) in MD5S, ('wrong input PASTE', src, md5(t0), 'expected one of', sorted(MD5S))
    t = t0
    for old, new in E:
        assert t.count(old) == 1, ('anchor must occur exactly once', old, t.count(old))
        t = t.replace(old, new)
        assert t.count(new) == 1, ('new text must occur exactly once', new)
    assert 'chooser' not in t, 'a chooser mention is left (rule 11)'
    d = len(t) - len(t0)
    print(f'{os.path.basename(__file__)}: {len(t0)} -> {len(t)} chars ({d:+d}); bank {LIMIT - len(t0)} -> {LIMIT - len(t)}; md5 {md5(t0)} -> {md5(t)}')
    if out is None:
        print('  [dry run, nothing written]'); return
    assert os.path.abspath(out) != os.path.abspath(src), 'refusing to overwrite the input'
    assert not os.path.exists(out), ('output exists; pick a new path', out)
    open(out, 'w', encoding='utf-8').write(t); print('  wrote', out)
if __name__ == '__main__': main()
