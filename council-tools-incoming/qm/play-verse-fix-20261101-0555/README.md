**Quartermaster:** # play-verse-fix: CANDIDATE play_v608.py that reads verse text from the PASTE (pages 26, 30, 37). Nov 1 2026, 5:55-6:00 AM MST. Nothing installed, nothing posted, nothing deleted.
**Quartermaster:** Based on: snap-r2h-0021MDT, pointer CURRENT-SNAP.txt f6dac2d0e7b391436a160eab1bbf17fe, PASTE 317e91ce86f073c961f8169183d2bbd3 (r2h-build/nancys-adventure-english-v6-08-1B-v32-PASTE.md, JSON on line 427), base play_v608.py ee74f3ef184f843aa1734462900eb5fc (snap code/). All re-hashed this run, before and after.
**Quartermaster:** Input: Instructor's triage REPORT 6f935084 (/workspace/council-tools/instructor-ext/f5-real50/triage-6fails/REPORT.md, re-hashed).
**Quartermaster:** Status: CANDIDATE only. The snap, pointer, PASTE, live screens/play_v608.py and every other bot's folder are untouched, and their md5s are the same as at the start.
**Quartermaster:**
**Quartermaster:** ## 1. Convention found in play_v608.py ee74f3ef (copied exactly)
**Quartermaster:** Two cards already render verses from data: 26's Words of Jesus bubble (:268) and the 29/44 verse scroll (:286).
**Quartermaster:** - Neither adds quote marks. The en string goes out as it is in the data: tx(j['en'], 'e15') and tx(s['en'], 'e15', 'font-size:18px;line-height:1.35').
**Quartermaster:** - Thai always comes right under the English, in its own line: tx(th, 't17'). The t17 class is `font:400 17px/1.7 Kanit,Thonburi,sans-serif`, so 17 px with line-height 1.7. Neither card adds an extra style to the Thai.
**Quartermaster:** - The ref comes first. 26 builds it as label + ' · ' + ref in e15, and 29 has the ref alone in e20. 29 and 37 end with a source line 'ESV · THSV11' in e15.
**Quartermaster:** - Only 37 (:318, hard-coded with U+201C/U+201D and no Thai line) and 30 (:293, hard-coded 'Steadfast · Isaiah 41:10' with no verse text) broke this.
**Quartermaster:** - '\n' in a verse: play_v608 has no example. The PASTE says "`\n` as a line break" (:404, verses.textRule), and mock-t303u/hearth.py renders verse text with white-space:pre-line. The candidate does the same, but only when a '\n' is present.
**Quartermaster:**
**Quartermaster:** ## 2. What the candidate changes (play_v608.candidate.py 72b0d50d, diff play_v608.candidate.diff a0b95ee5: 69 lines, 25 added, 5 removed)
**Quartermaster:** - New loader `PJ`: it reads the PASTE JSON line, from NAE_PASTE or by default the pointer's paste_1b_path. `verse(ref)` finds the one verse in verses.rest / verses.weekly[] with that ref. `vtx()` is tx() plus white-space:pre-line, and only when the text has '\n'.
**Quartermaster:** - 26 (:268): j now comes from PJ['jesusWords'][0] instead of cards.json. The bytes are the same, and the 26 html is byte-identical old vs new at all 3 sizes. The joined label 'Words of Jesus · John 15:9' is unchanged (reported only, as asked).
**Quartermaster:** - 37 (rest()): the card is [verses.rest.ref e20, verses.rest.en e15 18px, verses.rest.th t17, enSource + ' · ' + thSource e15]. There are no quote marks and the Thai is added. The card is 320 tall (was 260), or 300 at 320x568 so it clears the restScreen ribbon.
**Quartermaster:** - 30 (weapon_gift()): the label is trophies[axe-oak].word[0] + ' · ' + .ref, the same bytes as before but now from the PASTE. Under it, verses.weekly[2] (Isaiah 41:10) en e15 and th t17 sit in a capped scroll box (max-height 130 at 390/375, 82 at 320). That box follows the r2d 26-D bubble pattern: Thai scrolls inside, 17 px / lh 1.7, inset shadow hint. The card is 420 tall at 390/375 and 345 at 320 (was 290).
**Quartermaster:** - 'Oak Axe' stays hard-coded at :293. It's a label, not a verse, so it's out of scope; PASTE :30 says Build never hardcodes label text. The 29/44 scroll still reads cards.json, which is byte-equal to the PASTE for verses, jesusWords, trophies, restScreen and zones (checked this run).
**Quartermaster:**
**Quartermaster:** ## 3. Render path (render.py, shoot.py)
**Quartermaster:** - Old = a copy of ee74f3ef in old/; new = the candidate in new/. Both are imported first on sys.path, with an assert on the file actually loaded.
**Quartermaster:** - 390x844: play_v608 page() (+ guardian_chip on 26), as play_v608 __main__ does it. 26 at 320x568 and 375x667: stage_guardian_play.py's logic, i.e. UI parts at that size, the 320 UI from an NAE_SE=1 child, stage_v608.measure / scenery_top / fit_whole / compose. After that, every page goes through snap code/r2h/fix_r2h.fix and is shot with snap code/r2h/cdp_shot.py (CDP Emulation.setDeviceMetricsOverride, DPR 2).
**Quartermaster:** - Proof the path matches the snap: the OLD html is byte-identical to snap renders/r2h/html for all 5 renders the snap has (26 at 320/375/390, 30-390, 37-390).
**Quartermaster:** - NOT a snap path: 30 and 37 at 320x568 and 375x667. The snap renders them only at 390. These use play_v608 page() at that size (320 via NAE_SE=1, 375 via PV.W/H, as stage_guardian_play does for its 375 UI). Their scenes are not production-faithful: there's no fit_whole, rest()'s 390 px sky and 340 px ribbon are hard-coded, and the hero is hidden behind the card in old and new alike.
**Quartermaster:** - No /tmp: TMPDIR is scratch/tmp, set *relative* with cwd scratch/. An absolute path under this long folder makes Chrome die with "SingletonSocket path too long", past the 107-byte unix socket limit. stage_v608's mkdtemp(dir='/tmp') and rmtree are swapped in-process for scratch/tmp and a no-op, so its temp dirs are kept.
**Quartermaster:**
**Quartermaster:** ## 4. Viewport actually used (window.innerWidth x innerHeight, DPR), Chrome/156.0.8078.47
**Quartermaster:** - All 18 renders (9 old, 9 new) report exactly their target: 320x568, 375x667, 390x844, DPR 2 (runs/shots-old.json, runs/shots-new.json).
**Quartermaster:** - The 500 px issue Instructor saw comes from --window-size. The CDP device-metrics override used here doesn't have it.
**Quartermaster:** - Caveat: stage_v608.measure/scenery_top (used only for 26's 320/375 fit) still launch Chrome with --window-size and measure against the given W/H, not innerWidth. I didn't change that, and its output equals the snap's fits byte for byte (old html identical to the snap). Fits: 375x667 s 0.8032, 320x568 s 0.8155.
**Quartermaster:**
**Quartermaster:** ## 5. Byte check (byte_check.py)
**Quartermaster:** - new: `python3 byte_check.py html/new` gives exit 0. TOTAL 30 checks, 30 PASS, 0 FAIL (runs/byte_check-new.txt). Every verse en/th, the composed labels and the 37 ref/source line match the PASTE byte for byte, at all 3 sizes.
**Quartermaster:** - old: exit 1, with 33 checks, 18 PASS and 15 FAIL (runs/byte_check-old.txt). On 37 the en is off at byte 0 (e2 80 9c), 78 B vs 72 B, and the th is missing, at 3 sizes. On 30 the Isaiah 41:10 en and th are missing at 3 sizes.
**Quartermaster:** - planted: a curly quote put back on 37-390 and one Thai mark dropped on 37-375 give exit 1 with 4 FAIL (runs/byte_check-planted.txt).
**Quartermaster:**
**Quartermaster:** ## 6. Thai size and fit (runs/shots-new.json)
**Quartermaster:** - Every Thai element on these pages computes to 17px with line-height ratio 1.700, old and new.
**Quartermaster:** - 37 new: the Thai verse takes 2 lines at 390/375 and 3 at 320. Nothing falls outside the card or covers the buttons.
**Quartermaster:** - 30 new: the scroll box shows 2.21 of 4 Thai lines at 390 and 375. **At 320x568 it shows 0 of 6 Thai lines**, because the 4-line English fills the 82 px box and the Thai can only be reached by scrolling. **Page 30 does NOT meet "works at 320".** It needs a decision (section 8).
**Quartermaster:** - 30 new at 390: the 420 pt card covers most of the cheering hero (see png/compare-30.png).
**Quartermaster:**
**Quartermaster:** ## 7. Snap render checks run on old and new (checks.py, the round2/r2h cdp_checks.py set: Watchman domcheck_r2 JS 6cd930d1, snap occl_qm JS aa963b83, snap banner_check JS 901b5c4a)
**Quartermaster:** - old: 1 DOM issue, 31 occl hits, 0 banner issues. The DOM issue is textClipped on 37-320, rest()'s 340 px ribbon, which exists only at the non-snap 320 size. The occl hits are scene-svg-behind-card baseline.
**Quartermaster:** - new: 6 DOM issues, 35 occl hits, 0 banner issues. 26 and 37 are the same as old. All 5 new DOM issues and 4 new occl hits are on 30's scroll box: thaiCut at 390, 375 and 320, plus textClipped and thaiClipped at 320 (the Thai below the fold). The check flags them because the Thai is clipped by design.
**Quartermaster:** - Not run: checks_v608.py (it checks the PASTE/spec, which the candidate doesn't change), stage_v608 CHECK (scene stage, not these pages) and trim_clip_check (1A trim).
**Quartermaster:**
**Quartermaster:** ## 8. Open: page 30 is a design call (not made here)
**Quartermaster:** - A. Keep the scroll box (this candidate). It's byte-exact, but Thai is hidden at 320 and the hero is covered at 390.
**Quartermaster:** - B. Thai only under the label. That breaks :404's "ESV English bold with THSV11 Thai under it", and 6 Thai lines still don't fit at 320.
**Quartermaster:** - C. Keep the label only, as in ee74f3ef, and rule that a trophy word + ref isn't "a verse". The byte check would then drop its two 30 verse rows.
**Quartermaster:** - Also seen, not changed: :404 says "ESV English bold", but every verse card here uses e15 Lilita One at weight 400.
**Quartermaster:**
**Quartermaster:** ## 9. Disk (df -B1 /, read before each render batch; stop rule 79%)
**Quartermaster:** - Readings: folder created 101,468,499,968 (74.18%); old build 101,506,347,008; new build 101,691,531,264; old shots 101,874,184,192; new shots 101,936,009,216; new build (capped) 102,000,328,704; new shots 102,172,217,344 / 102,172,622,848; checks 102,173,118,464; final 102,396,211,200 (74.86%). Size 136,782,041,088.
**Quartermaster:** - scratch/ is about 872 MB (Chrome profiles, stage_v608 temp dirs, injected check copies, iter1-uncapped renders), all kept.
**Quartermaster:**
**Quartermaster:** ## 10. Files
**Quartermaster:** - play_v608.candidate.py, play_v608.candidate.diff (vs ee74f3ef), and make_candidate.py, which builds new/play_v608.py from old/ by count-checked replacements.
**Quartermaster:** - render.py and shoot.py produce html/{old,new}/*.html and png/{old,new}/*.png (9 each; old = before, new = after), plus png/compare-26/30/37.png side by side.
**Quartermaster:** - byte_check.py and checks.py, with runs/*.txt and *.json.
**Quartermaster:** - scratch/iter1-uncapped/ holds the first try of 30 without the scroll box: the card overflowed the screen at 320 with the buttons off-screen.
**Quartermaster:** Ready to paste: none. CURRENT stays v5-37, `nancys-adventure-english-v5-37-PASTE.md` (acc534a51a922102ee37844e04d17955).
