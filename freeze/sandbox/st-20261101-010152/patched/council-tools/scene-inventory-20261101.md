# Scene inventory: zone x location x time of day (Maxwell t508u)

Read-only. Written by Quartermaster at 06:51 on Nov 1, 2026. Nothing was rendered, edited or deleted. INTERNAL working file.

**Base.** Pointer `v608build/CURRENT-SNAP.txt` f6dac2d0, snap-r2h-0021MDT, renders-MANIFEST.md5 62e41535 (1,099 entries), PASTE 1B 317e91ce (188,116 chars). The r2h re-run was writing into `v608build/round2/r2h/` during the scan; its new files are counted as IN PROGRESS, not CURRENT.

**Scanned.** 2828 PNGs (961 unique by md5) under screens-v603..v608, v608build (all snaps, round2, scenes/stage, scenes/tod, title, ceiling-cap, sky-options, decisions, eyes, polish-r1), mocks-*, mock-t*. Each PNG was classified from its paired HTML (scene objects `data-name`/`data-deco`, `data-tod`, the per-step sky stops and tint overlay); copies without HTML inherit by md5; filenames are used only as a last resort. Tools: `council-tools/scene_inventory.py`, `scene_inventory_build.py`. coverage_scan.py and coverage-gaps-20261031.md were NOT used for counts (stale: r2d/1A, per screen).

**Status.** CURRENT = listed in the snapshot manifest (path or md5) and its HTML has none of the superseded-look markers. STALE LOOK = listed, but its HTML still has a look that was replaced: the meadow walkway or ground dots (removed in r2h), the Home Lake chip #D9663F (now #F05A00), or the old ask "Where is the ...?" (P1 t440u: "Can you find the {word}?"). IN PROGRESS = r2h re-run output not yet frozen. OLD = not in the manifest. NEVER = no render found anywhere.

## 1. What the spec defines (PASTE 317e91ce)

**4 world regions (cards JSON `mapLayout.regions`, spec :27, :227) carrying the 7 learning zones:**

| Region | Learning zones | Opens | Locations (spec :227) |
|---|---|---|---|
| Word Meadow (r1, ทุ่งหญ้าคำศัพท์) | Phonics, Sight Words | day one (Phonics is `startZone`) | park (swing set, bench, bus stop, kite); alternate layout: park by a pond |
| Golden Fields (r2, ทุ่งข้าวสีทอง) | Colors and Shapes, Numbers | after the Word guardian | farm (corn row, gate, cow, basket) |
| Home Lake (r3, ทะเลสาบบ้านเรา) | Maxwell Says, Nancy's Kitchen, Baby and Hospital | Maxwell Says and Kitchen day one; the region (Baby and Hospital) after the Number guardian | inside the home (shelf, window, desk, crib, rug); hotel front desk (only ms-03 to ms-06, ms-21 to ms-23); Kitchen runs: the home room set for a meal (small table replaces the crib) |
| Echo Forest (r4, ป่าเสียงสะท้อน) | none of the 7: Sound Duel | after the Gentle guardian | night woods (owl, lantern, tent, footbridge), also behind Sound Duel |

So there are **7 scene locations**, not 4. Maxwell's four names are the regions; the pond, the front desk and the Kitchen meal set are extra locations inside them.

**Times of day (spec :227).** Each scene gets `data-tod` from its zone's step, 1 + `zoneRuns[zone]` mod 5 (Sound Duel rounds for Echo Forest): step 1 `m` morning, 2 `d` midday ("the `a` sky lighter"), 3 `a` afternoon, 4 `e` evening, 5 `n` night, then morning again. Only sky, ground and light tint change. Echo Forest at `m`/`d` is the same woods in dawn mist. **Every location, including the indoor ones, therefore has 5 times: 7 x 5 = 35 combinations.**

Other time-bearing screens: the title (:157, by clock, 4 states `m a e n`, no `d`); menus "take the title's four skies" (:121); the rest screen is a fixed evening sky or the worn `restSky` (pantry `sky-sunset`, trophy `sky-starry`); the Map has one sky sheet with the sun and no time of day (its variants are `mapTheme`).

## 2. Matrix: location x time of day (35 combinations)

Cell = best status found; sizes are the CURRENT sizes (320 = 320x568, 390 = 390x844); STALE count = unique listed renders.

| Location | Zones | m morning | d midday | a afternoon | e evening | n night | untinted base (not a spec time) |
|---|---|---|---|---|---|---|---|
| Word Meadow / park | Phonics, Sight Words | CURRENT 320/375x667/390 | STALE LOOK (listed, superseded look) (2) | STALE LOOK (listed, superseded look) (2) | STALE LOOK (listed, superseded look) (2) | STALE LOOK (listed, superseded look) (2) | n/a (has sky) |
| Word Meadow / park by a pond | Phonics, Sight Words | **NEVER** | **NEVER** | **NEVER** | IN PROGRESS (r2h re-run, not frozen) | **NEVER** | n/a (has sky) |
| Home Lake / inside the home | Maxwell Says (day one), Baby and Hospital (after Number guardian) | STALE LOOK (listed, superseded look) (6) | STALE LOOK (listed, superseded look) (6) | STALE LOOK (listed, superseded look) (6) | STALE LOOK (listed, superseded look) (6) | STALE LOOK (listed, superseded look) (6) | CURRENT 320/390 |
| Home Lake / meal set (Kitchen) | Nancy's Kitchen (day one) | **NEVER** | **NEVER** | **NEVER** | **NEVER** | **NEVER** | CURRENT 320/390 |
| Home Lake / hotel front desk | Maxwell Says ms-03 to ms-06, ms-21 to ms-23 only (day one) | **NEVER** | **NEVER** | **NEVER** | **NEVER** | **NEVER** | STALE LOOK (listed, superseded look) (9) |
| Golden Fields / farm | Colors and Shapes, Numbers (after Word guardian) | STALE LOOK (listed, superseded look) (2) | STALE LOOK (listed, superseded look) (2) | CURRENT 320/375x667/390 | STALE LOOK (listed, superseded look) (2) | STALE LOOK (listed, superseded look) (2) | n/a (has sky) |
| Echo Forest / night woods | Sound Duel (not one of the 7 zones; after Gentle guardian) | CURRENT 320/375x667/390 | CURRENT 320/390 | CURRENT 320/390 | CURRENT 320/390 | CURRENT 320/375x667/375x812/390 | n/a (has sky) |

**Totals (35):** CURRENT 7, IN PROGRESS 1, STALE LOOK 13, OLD only 0, NEVER 14.

### Per-cell evidence

- **Word Meadow / park, step 1 morning** (m): CURRENT
  - CURRENT: `v608build/round2/r2h/png/10-word-meadow-scene-320x568.png` 320x568; `v608build/round2/r2h/png/10-word-meadow-scene-390x844.png` 390x844; `v608build/round2/r2h/png/11-word-meadow-scene-right-390x844.png` 390x844; `v608build/round2/r2h/png/12-reveal-right-390x844.png` 390x844; `v608build/round2/r2h/png/13-word-meadow-scene-retry-390x844.png` 390x844; `v608build/round2/r2h/png/15-say-it-sight-words-390x844.png` 390x844; `v608build/round2/r2h/png/23-level-up-reward-320x568.png` 320x568; `v608build/round2/r2h/png/23-level-up-reward-390x844.png` 390x844 (+31 more)
  - IN PROGRESS: `v608build/round2/r2h/png/stage-B-meadow-listen-and-find-375x667.png` 375x667; `v608build/round2/r2h/png/stage-B-meadow-listen-and-find-320x568.png` 320x568; `v608build/round2/r2h/png/stage-B-meadow-listen-and-find-390x844.png` 390x844; `v608build/round2/r2h/png/zone-meadow-ask-375x812-skyB.png` 375x812
  - STALE LOOK (72): e.g. `screens-v608/png/27-guardian-kneels-390check.png` 390x844; `screens-v608/png/11-word-meadow-scene-right-390check.png` 390x844; `screens-v608/png/12-reveal-right.png` 390x844. Why: ground dots (tufts in r2h); meadow walkway (removed in r2h); old ask wording "Where is the ...?" (P1 t440u tapPrompt "Can you find the {word}?")
- **Word Meadow / park, step 2 midday** (d): STALE LOOK (listed, superseded look)
  - STALE LOOK (2): e.g. `v608build/scenes/tod/meadow-step2-390.png` 390x844; `v608build/scenes/tod/meadow-step2-320x568.png` 320x568. Why: ground dots (tufts in r2h); meadow walkway (removed in r2h); old ask wording "Where is the ...?" (P1 t440u tapPrompt "Can you find the {word}?")
- **Word Meadow / park, step 3 afternoon** (a): STALE LOOK (listed, superseded look)
  - STALE LOOK (2): e.g. `v608build/scenes/tod/meadow-step3-320x568.png` 320x568; `v608build/scenes/tod/meadow-step3-390.png` 390x844. Why: ground dots (tufts in r2h); meadow walkway (removed in r2h); old ask wording "Where is the ...?" (P1 t440u tapPrompt "Can you find the {word}?")
- **Word Meadow / park, step 4 evening** (e): STALE LOOK (listed, superseded look)
  - STALE LOOK (2): e.g. `v608build/scenes/tod/meadow-step4-320x568.png` 320x568; `v608build/scenes/tod/meadow-step4-390.png` 390x844. Why: ground dots (tufts in r2h); meadow walkway (removed in r2h); old ask wording "Where is the ...?" (P1 t440u tapPrompt "Can you find the {word}?")
- **Word Meadow / park, step 5 night** (n): STALE LOOK (listed, superseded look)
  - STALE LOOK (2): e.g. `v608build/scenes/tod/meadow-step5-390.png` 390x844; `v608build/scenes/tod/meadow-step5-320x568.png` 320x568. Why: ground dots (tufts in r2h); meadow walkway (removed in r2h); old ask wording "Where is the ...?" (P1 t440u tapPrompt "Can you find the {word}?")
- **Word Meadow / park by a pond, step 1 morning** (m): **NEVER**
- **Word Meadow / park by a pond, step 2 midday** (d): **NEVER**
- **Word Meadow / park by a pond, step 3 afternoon** (a): **NEVER**
- **Word Meadow / park by a pond, step 4 evening** (e): IN PROGRESS (r2h re-run, not frozen)
  - IN PROGRESS: `v608build/round2/r2h/png/stage-A-meadow-evening-pond-375x667.png` 375x667; `v608build/round2/r2h/png/stage-A-meadow-evening-pond-320x568.png` 320x568; `v608build/round2/r2h/png/stage-A-meadow-evening-pond-390x844.png` 390x844
  - STALE LOOK (3): e.g. `v608build/scenes/stage/png/A-meadow-evening-pond-390x844.png` 390x844; `v608build/scenes/stage/png/A-meadow-evening-pond-320x568.png` 320x568; `v608build/scenes/stage/png/A-meadow-evening-pond-375x667.png` 375x667. Why: meadow walkway (removed in r2h); old ask wording "Where is the ...?" (P1 t440u tapPrompt "Can you find the {word}?")
- **Word Meadow / park by a pond, step 5 night** (n): **NEVER**
- **Home Lake / inside the home, step 1 morning** (m): STALE LOOK (listed, superseded look)
  - STALE LOOK (6): e.g. `v608build/round2/ceiling-cap/home-lake/png-r2ask/lake-step1-375x812.png` 375x812; `v608build/round2/ceiling-cap/home-lake/png/lake-step1-390x844.png` 390x844; `v608build/round2/ceiling-cap/home-lake/png/lake-step1-375x812.png` 375x812. Why: Home Lake chip #D9663F (r2h #F05A00); old ask wording "Where is the ...?" (P1 t440u tapPrompt "Can you find the {word}?")
- **Home Lake / inside the home, step 2 midday** (d): STALE LOOK (listed, superseded look)
  - STALE LOOK (6): e.g. `v608build/round2/ceiling-cap/home-lake/png-r2ask/lake-step2-375x812.png` 375x812; `v608build/round2/ceiling-cap/home-lake/png/lake-step2-375x812.png` 375x812; `v608build/round2/ceiling-cap/home-lake/png/lake-step2-390x844.png` 390x844. Why: Home Lake chip #D9663F (r2h #F05A00); old ask wording "Where is the ...?" (P1 t440u tapPrompt "Can you find the {word}?")
- **Home Lake / inside the home, step 3 afternoon** (a): STALE LOOK (listed, superseded look)
  - STALE LOOK (6): e.g. `v608build/round2/ceiling-cap/home-lake/png-r2ask/lake-step3-375x812.png` 375x812; `v608build/round2/ceiling-cap/home-lake/png/lake-step3-375x812.png` 375x812; `v608build/round2/ceiling-cap/home-lake/png/lake-step3-390x844.png` 390x844. Why: Home Lake chip #D9663F (r2h #F05A00); old ask wording "Where is the ...?" (P1 t440u tapPrompt "Can you find the {word}?")
- **Home Lake / inside the home, step 4 evening** (e): STALE LOOK (listed, superseded look)
  - STALE LOOK (6): e.g. `v608build/round2/ceiling-cap/home-lake/png-r2ask/lake-step4-375x812.png` 375x812; `v608build/round2/ceiling-cap/home-lake/png/lake-step4-390x844.png` 390x844; `v608build/round2/ceiling-cap/home-lake/png/lake-step4-375x812.png` 375x812. Why: Home Lake chip #D9663F (r2h #F05A00); old ask wording "Where is the ...?" (P1 t440u tapPrompt "Can you find the {word}?")
- **Home Lake / inside the home, step 5 night** (n): STALE LOOK (listed, superseded look)
  - STALE LOOK (6): e.g. `v608build/round2/ceiling-cap/home-lake/png-r2ask/lake-step5-375x812.png` 375x812; `v608build/round2/ceiling-cap/home-lake/png/lake-step5-375x812.png` 375x812; `v608build/round2/ceiling-cap/home-lake/png/lake-step5-390x844.png` 390x844. Why: Home Lake chip #D9663F (r2h #F05A00); old ask wording "Where is the ...?" (P1 t440u tapPrompt "Can you find the {word}?")
- **Home Lake / inside the home, untinted base (no time of day applied)** (base): CURRENT
  - CURRENT: `v608build/round2/r2h/png/16-say-it-maxwell-says-day1-390x844.png` 390x844; `v608build/round2/r2h/png/17-two-answer-pray-high-five-390x844.png` 390x844; `v608build/round2/r2h/png/18-two-answer-wrong-tap-390x844.png` 390x844; `v608build/round2/r2h/png/19-two-answer-right-done-390x844.png` 390x844; `v608build/round2/r2h/png/32-home-lake-scene-390x844.png` 390x844; `v608build/round2/r2h/png/33-say-it-baby-hospital-reply-320x568.png` 320x568; `v608build/round2/r2h/png/33-say-it-baby-hospital-reply-390x844.png` 390x844; `v608build/round2/r2h/png/54-phrase-ask-card-320x568.png` 320x568 (+2 more)
  - STALE LOOK (31): e.g. `v608build/round2/ceiling-cap/home-lake/png-r2ask/18-two-answer-wrong-tap-390x844.png` 390x844; `v608build/round2/sky-options/B/png-r2ask/54-phrase-ask-card-390x844.png` 390x844; `screens-v608/png/16-say-it-maxwell-says-day1-390check.png` 390x844. Why: Home Lake chip #D9663F (r2h #F05A00); old ask wording "Where is the ...?" (P1 t440u tapPrompt "Can you find the {word}?")
- **Home Lake / meal set (Kitchen), step 1 morning** (m): **NEVER**
- **Home Lake / meal set (Kitchen), step 2 midday** (d): **NEVER**
- **Home Lake / meal set (Kitchen), step 3 afternoon** (a): **NEVER**
- **Home Lake / meal set (Kitchen), step 4 evening** (e): **NEVER**
- **Home Lake / meal set (Kitchen), step 5 night** (n): **NEVER**
- **Home Lake / meal set (Kitchen), untinted base (no time of day applied)** (base): CURRENT
  - CURRENT: `v608build/round2/r2h/png/14-reveal-gentle-retry-320x568.png` 320x568; `v608build/round2/r2h/png/14-reveal-gentle-retry-390x844.png` 390x844; `v608build/round2/r2h/png/21-kitchen-say-it-shown-320x568.png` 320x568; `v608build/round2/r2h/png/21-kitchen-say-it-shown-390x844.png` 390x844; `v608build/round2/r2h/png/22-kitchen-server-talk-320x568.png` 320x568; `v608build/round2/r2h/png/22-kitchen-server-talk-390x844.png` 390x844
  - STALE LOOK (30): e.g. `v608build/round2/sky-options/B/png-r2ask/22-kitchen-server-talk-390x844.png` 390x844; `v608build/round2/sky-options/B/png-r2ask/21-kitchen-say-it-shown-320x568.png` 320x568; `v608build/round2/sky-options/B/png-r2ask/22-kitchen-server-talk-320x568.png` 320x568. Why: Home Lake chip #D9663F (r2h #F05A00); old ask wording "Where is the ...?" (P1 t440u tapPrompt "Can you find the {word}?")
- **Home Lake / hotel front desk, step 1 morning** (m): **NEVER**
- **Home Lake / hotel front desk, step 2 midday** (d): **NEVER**
- **Home Lake / hotel front desk, step 3 afternoon** (a): **NEVER**
- **Home Lake / hotel front desk, step 4 evening** (e): **NEVER**
- **Home Lake / hotel front desk, step 5 night** (n): **NEVER**
- **Home Lake / hotel front desk, untinted base (no time of day applied)** (base): STALE LOOK (listed, superseded look)
  - STALE LOOK (9): e.g. `v608build/round2/ceiling-cap/png-r2ask/E-lake-front-desk-375x667.png` 375x667; `v608build/round2/ceiling-cap/png-r2ask/E-lake-front-desk-375x812-wallup.png` 375x812; `v608build/round2/ceiling-cap/png-r2ask/E-lake-front-desk-390x844-wallup.png` 390x844. Why: Home Lake chip #D9663F (r2h #F05A00)
- **Golden Fields / farm, step 1 morning** (m): STALE LOOK (listed, superseded look)
  - STALE LOOK (2): e.g. `v608build/scenes/tod/fields-step1-320x568.png` 320x568; `v608build/scenes/tod/fields-step1-390.png` 390x844. Why: old ask wording "Where is the ...?" (P1 t440u tapPrompt "Can you find the {word}?")
- **Golden Fields / farm, step 2 midday** (d): STALE LOOK (listed, superseded look)
  - STALE LOOK (2): e.g. `v608build/scenes/tod/fields-step2-390.png` 390x844; `v608build/scenes/tod/fields-step2-320x568.png` 320x568. Why: old ask wording "Where is the ...?" (P1 t440u tapPrompt "Can you find the {word}?")
- **Golden Fields / farm, step 3 afternoon** (a): CURRENT
  - CURRENT: `v608build/round2/showcase/tiles/screens-v608--31-golden-fields-scene.png` 390x844; `v608build/scenes/stage/png/C-fields-count-it-320x568.png` 320x568; `v608build/scenes/stage/png/C-fields-count-it-375x667.png` 375x667; `v608build/scenes/stage/png/C-fields-count-it-390x844.png` 390x844; `v608build/scenes/stage/png/D-fields-big-or-small-320x568.png` 320x568; `v608build/scenes/stage/png/D-fields-big-or-small-375x667.png` 375x667; `v608build/scenes/stage/png/D-fields-big-or-small-390x844.png` 390x844
  - STALE LOOK (8): e.g. `v608build/round2/sky-options/B/png/zone-fields-ask-320x568.png` 320x568; `v608build/round2/sky-options/B/png/zone-fields-ask-390x844.png` 390x844; `v608build/round2/sky-options/B/png-r2ask/zone-fields-ask-375x812.png` 375x812. Why: old ask wording "Where is the ...?" (P1 t440u tapPrompt "Can you find the {word}?")
- **Golden Fields / farm, step 4 evening** (e): STALE LOOK (listed, superseded look)
  - STALE LOOK (2): e.g. `v608build/scenes/tod/fields-step4-320x568.png` 320x568; `v608build/scenes/tod/fields-step4-390.png` 390x844. Why: old ask wording "Where is the ...?" (P1 t440u tapPrompt "Can you find the {word}?")
- **Golden Fields / farm, step 5 night** (n): STALE LOOK (listed, superseded look)
  - STALE LOOK (2): e.g. `v608build/scenes/tod/fields-step5-390.png` 390x844; `v608build/scenes/tod/fields-step5-320x568.png` 320x568. Why: old ask wording "Where is the ...?" (P1 t440u tapPrompt "Can you find the {word}?")
- **Echo Forest / night woods, step 1 morning** (m): CURRENT
  - CURRENT: `v608build/scenes/stage/png/H-forest-dawn-320x568.png` 320x568; `v608build/scenes/stage/png/H-forest-dawn-375x667.png` 375x667; `v608build/scenes/stage/png/H-forest-dawn-390x844.png` 390x844; `v608build/scenes/tod/forest-step1-320x568.png` 320x568; `v608build/scenes/tod/forest-step1-390.png` 390x844
- **Echo Forest / night woods, step 2 midday** (d): CURRENT
  - CURRENT: `v608build/scenes/tod/forest-step2-320x568.png` 320x568; `v608build/scenes/tod/forest-step2-390.png` 390x844
- **Echo Forest / night woods, step 3 afternoon** (a): CURRENT
  - CURRENT: `v608build/scenes/tod/forest-step3-320x568.png` 320x568; `v608build/scenes/tod/forest-step3-390.png` 390x844
- **Echo Forest / night woods, step 4 evening** (e): CURRENT
  - CURRENT: `v608build/scenes/tod/forest-step4-320x568.png` 320x568; `v608build/scenes/tod/forest-step4-390.png` 390x844
- **Echo Forest / night woods, step 5 night** (n): CURRENT
  - CURRENT: `v608build/round2/r2h/png/zone-forest-ask-320x568.png` 320x568; `v608build/round2/r2h/png/zone-forest-ask-375x812.png` 375x812; `v608build/round2/r2h/png/zone-forest-ask-390x844.png` 390x844; `v608build/round2/showcase/tiles/B--zone-forest-ask-390x844.png` 390x844; `v608build/round2/showcase/tiles/screens-v608--zone-forest-ask-320x568.png` 320x568; `v608build/round2/sky-options/B/png-r2ask/34-echo-forest-sound-duel-320x568.png` 320x568; `v608build/round2/sky-options/B/png-r2ask/34-echo-forest-sound-duel-375x812.png` 375x812; `v608build/round2/sky-options/B/png-r2ask/34-echo-forest-sound-duel-390x844.png` 390x844 (+11 more)
  - IN PROGRESS: `v608build/round2/r2h/png/36-sound-duel-round-done-390x844.png` 390x844; `v608build/round2/r2h/png/36-sound-duel-round-done-320x568.png` 320x568
  - STALE LOOK (12): e.g. `v608build/round2/sky-options/B/png/zone-forest-ask-320x568.png` 320x568; `v608build/round2/sky-options/B/png-r2ask/zone-forest-ask-375x812.png` 375x812; `v608build/round2/r2e/d2/png/zone-forest-ask-D2plate-375x667.png` 375x667. Why: old ask wording "Where is the ...?" (P1 t440u tapPrompt "Can you find the {word}?")

## 3. Other time-bearing screens

| Screen | m | a | e | n | Notes |
|---|---|---|---|---|---|
| Title (:157, clock) | CURRENT 320/390 | CURRENT 320/390 | **NEVER** | CURRENT 390 | m = `screens-v608/png/01-title*`; a = `50-open-from-home-screen*` (the title with its hint card); n = `52-title-night` (390 only; 320 exists only as OLD `v608build/title/v608-n-320.png`). No `d` state in the spec. |
| Main menu (:121, "title's four skies") | IN PROGRESS (r2h re-run, not frozen) | CURRENT 320/390 | **NEVER** | **NEVER** | every current menu render (02-04, 49, 51) is `a`; M1/M3 menu concepts at `m` are in the r2h re-run, not frozen; M2 has no greeting. Spec does not say outright that menus follow the clock. |
| Rest screen (:121) | n/a | n/a | CURRENT 390 | n/a | fixed evening sky; CURRENT at 390 only (`round2/r2h/png/37-rest-screen-390x844.png`); no 320. `restSky` variants Sunset Sky and Starry sky: 0 renders. |
| Map (:172) | no time of day in spec | | | | CURRENT: 9 renders, all 390x844 (screens-v608 05-09, 53; r2h 05, 08, 09). **No Map at 320 in the frozen manifest.** The r2h re-run has just written `round2/r2h/png/map-extended-320x568.png` and `-390x844.png` (IN PROGRESS). The only other Map at 320 is OLD `mock-t346u/Q-mock-t346u-map-day1-320x568.png`. |

## 4. Gaps, ranked by how often Nancy would see them

Rule used (from the spec, not playtest data): each time of day is 1/5 of a location's runs in the long run, so locations rank by exposure: Word Meadow (start zone, both layouts alternate) > Home Lake home room (Maxwell Says day one, Baby and Hospital later) > Kitchen meal set (day one) > front desk (7 Maxwell Says cards only) > Golden Fields (after the Word guardian) > Echo Forest (after the Gentle guardian). Within a location, earlier steps first (her 1st run there is morning). NEVER ranks above STALE at equal exposure.

| # | Location | Time | Status now | Renders to fill (320 + 390) |
|---|---|---|---|---|
| 1 | Word Meadow / park by a pond | step 1 morning | **NEVER** | 2 |
| 2 | Word Meadow / park by a pond | step 2 midday | **NEVER** | 2 |
| 3 | Word Meadow / park by a pond | step 3 afternoon | **NEVER** | 2 |
| 4 | Word Meadow / park by a pond | step 5 night | **NEVER** | 2 |
| 5 | Word Meadow / park | step 2 midday | STALE LOOK (listed, superseded look) | 2 |
| 6 | Word Meadow / park | step 3 afternoon | STALE LOOK (listed, superseded look) | 2 |
| 7 | Word Meadow / park by a pond | step 4 evening | IN PROGRESS (r2h re-run, not frozen) | 2 |
| 8 | Word Meadow / park | step 4 evening | STALE LOOK (listed, superseded look) | 2 |
| 9 | Word Meadow / park | step 5 night | STALE LOOK (listed, superseded look) | 2 |
| 10 | Home Lake / inside the home | step 1 morning | STALE LOOK (listed, superseded look) | 2 |
| 11 | Home Lake / inside the home | step 2 midday | STALE LOOK (listed, superseded look) | 2 |
| 12 | Home Lake / inside the home | step 3 afternoon | STALE LOOK (listed, superseded look) | 2 |
| 13 | Home Lake / inside the home | step 4 evening | STALE LOOK (listed, superseded look) | 2 |
| 14 | Home Lake / inside the home | step 5 night | STALE LOOK (listed, superseded look) | 2 |
| 15 | Home Lake / meal set (Kitchen) | step 1 morning | **NEVER** | 2 |
| 16 | Home Lake / meal set (Kitchen) | step 2 midday | **NEVER** | 2 |
| 17 | Home Lake / meal set (Kitchen) | step 3 afternoon | **NEVER** | 2 |
| 18 | Home Lake / meal set (Kitchen) | step 4 evening | **NEVER** | 2 |
| 19 | Home Lake / meal set (Kitchen) | step 5 night | **NEVER** | 2 |
| 20 | Home Lake / hotel front desk | step 1 morning | **NEVER** | 2 |
| 21 | Home Lake / hotel front desk | step 2 midday | **NEVER** | 2 |
| 22 | Home Lake / hotel front desk | step 3 afternoon | **NEVER** | 2 |
| 23 | Home Lake / hotel front desk | step 4 evening | **NEVER** | 2 |
| 24 | Home Lake / hotel front desk | step 5 night | **NEVER** | 2 |
| 25 | Golden Fields / farm | step 1 morning | STALE LOOK (listed, superseded look) | 2 |
| 26 | Golden Fields / farm | step 2 midday | STALE LOOK (listed, superseded look) | 2 |
| 27 | Golden Fields / farm | step 4 evening | STALE LOOK (listed, superseded look) | 2 |
| 28 | Golden Fields / farm | step 5 night | STALE LOOK (listed, superseded look) | 2 |

Other gaps: title `e` (320+390) and title `n` at 320; menu `e` and `n` (and `m` unless the r2h M1/M3 concepts are frozen); rest screen at 320; the 2 `restSky` variants; the Map at 320 until map-extended is frozen. Guardian runs: the only guardian-run renders (24-28) are on the Word Meadow park at morning; none in Golden Fields, Home Lake or at any other time.

## 5. Renders needed to fill every gap at 320 and 390

- Scene matrix: **28 at 320 + 28 at 390 = 56** (14 NEVER cells = 28; 13 STALE cells = 26 re-renders; pond evening = 2, already being re-rendered by the r2h job, so 54 once that freezes).
- Title: 2 at 320 + 1 at 390 = 3. Menu: 3 + 3 = 6 (4 if M1/M3 are frozen as the morning menu). Rest: 1 at 320. restSky variants: 2 at 390 + 2 at 320 = 4.
- **Total: 66 renders, or 70 with the restSky variants.**
- **Rough time:** the renderer itself is about 1-4 s per PNG (median gap 1.1 s in scenes/tod, 3.5 s in scenes/stage), so a few minutes of machine time. The real cost is work: `scenes/tod_v608.py` only knows meadow (park), fields, lake (home room) and forest, so the pond, front desk and Kitchen meal set need a time-of-day path added first, then the stage CHECK, DOM and occl checks and an eye pass. Estimate 1-2 hours of QM time, plus Auditor gating. About 10 MB of disk (PNGs are about 150 KB). No PASTE characters: every location and time is already in :227.

## 6. What the spec does not define

- No times beyond the 5 steps: no separate dawn, dusk or sunset step (dawn only as Echo Forest's `m`/`d` mist), no weather or seasons.
- The title and menus have no `d` (midday) state; the Map has no time of day at all; the rest screen is always evening (or its worn sky).
- How the time of day shows indoors is not spelled out beyond "sky, ground and light tint". The room's window is drawn with no sky, so the tod renders show indoor time only as a colour tint.
- Renderer note, not a spec gap: the tod renders mark step 2 (midday) as `data-tod='a'` with lighter sky stops, not `data-tod='d'`. The spec names `d`, so Build must emit `d`.
- Whether the pond alternates per scene or per run is not stated ("Word Meadow alternates a second layout").

## 7. Cross-check with Chancellor's partial (chancellor/r2h/coverage-gaps-partial-0044MDT.md, 687f2fef)

**Agree:** the 4 regions, 7 zones and 7 locations; the 5 steps plus the title's 4 clock states; `scenes/tod/` has steps 1-5 for meadow park, fields, lake home room and forest at 390 and 320 (40 PNGs plus 8 strips), all listed in the manifest; Home Lake steps are also in round2/ceiling-cap/home-lake at 390x844 and 375x812; the pond has one render set (A, evening, confirmed by `data-tod='e'` and by eye); the front desk exists only untinted; no new spec text is needed.

**Disagree or refine:**
- "All 5 times covered for park, farm, home and forest": only Echo Forest's 5 are current. The meadow tod renders still have the walkway and ground dots r2h removed; the Home Lake ones have the old #D9663F chip; meadow, fields and lake tod renders show the old "Where is the ...?" ask. So 13 of those 20 cells are STALE LOOK and need re-rendering. Fields afternoon is current only through stage C/D.
- Pond: listed render A is also stale (walkway and old ask). The r2h job is re-rendering it right now (`round2/r2h/png/stage-A-meadow-evening-pond-*`, not frozen). The gaps are m, d, a, n: 4 cells.
- Front desk: "default" is untinted, which is none of the 5 times, and it has the old chip colour. So all 5 cells are missing, not 4.
- Kitchen meal set: it is in more renders than 2. Screens 14, 20, 21 and 22 plus stage F (`F-lake-night-table` / `F-lake-kitchen`) all use it, all untinted. 0 of 5 times; 14, 21 and 22 are CURRENT at 320 and 390 as the untinted base.
- Title: not night only. Morning (01-title, 320 and 390) and afternoon (50-open-from-home-screen, 320 and 390) are CURRENT; night is CURRENT at 390 only; evening was never rendered anywhere.
- Size of the job: not about 12-13 cells and about 25 renders, but 28 scene cells and 56 renders, plus 14 for title, menu and rest.
- Map at 320 in r2h: there is none in the frozen manifest. The re-run has only now written `map-extended-320x568.png` (IN PROGRESS).

## 8. Caveats

- The look check runs only where a PNG has its own HTML (or an md5-identical copy of one). PNGs with no HTML count as CURRENT on manifest membership alone (look_ok null in the JSON).
- The r2h re-run was still writing during the scan (2,802 to 2,828 PNGs over the session). Cells it touches may move from STALE or IN PROGRESS to CURRENT at the next freeze.
- The `-before` copies in round2/r2h are excluded from every count.
- The contact sheet `scene-inventory-20261101-INTERNAL-contact-sheet.png` is INTERNAL, not for Maxwell yet.
