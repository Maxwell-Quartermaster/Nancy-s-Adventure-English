# Coverage gaps: where the council has spent little or no time (Maxwell t461u, QM-relayed)

Written by QM at 10:59 PM MDT on Oct 31, 2026. This is a read-only analysis. Nothing in the build or the snapshots was changed, and nothing was deleted.

**Base.** Frozen `snap-r2d-2233MDT`: PASTE 1A **106a0661**, cards **501340c2**. Also read: `screens-v608/png` (151 PNGs), `v608build/scenes/stage/png`, `v608build/round2/**` PNGs, and 347 council .md/.txt files under audit/, instructor/, watchman/, chancellor/ and decisions/. Copies inside `snap-*` and `live-*` folders were skipped.

**Method.** `coverage_scan.py` gathers the data into `coverage-data.json`, and `coverage_heatmap.py` draws `coverage-heatmap.png`. Both scripts are in this folder.

**What each column measures.** Each row is one area. **Renders** counts the PNGs of that area's screens. **Sizes** counts the phone sizes rendered, out of 4. **Reports** counts the council files that mention the area. This is a keyword match, so treat it as rough: broad words such as "audio" and "title" overcount. **Checks** counts the matching lines in `checks_v608.py`. **Walks** counts the walk or play-flow notes that touch the area. **Shown** counts how often the area appears on pick sheets, the showcase INDEX or QUEUE.

**How rows are ranked.** Each column is put on a log scale, and the scores are averaged. Rank #1 has the least attention.

## 1. Inventory of the game (from the PASTE and cards)

**Spec sections.** There are 20, from §0 to §20, plus 14 subsections from 6.1 to 11.4.

**Screens.** The renders cover 54 screens, numbered 01 to 54. They break down as follows:
- **Title:** 01 and 52.
- **Menu and verse pop-up:** 02 to 04, and 51.
- **Map:** 05 to 09, and 53.
- **Find-and-tap scenes:** 10, 11, 13, 31 and 32, the four zone-asks, and stage A to H.
- **Reveal:** 12 and 14.
- **Say-it cards:** 15, 16, 20, 21, 33 and 54.
- **Two-answer:** 17 to 19.
- **Kitchen:** 20 to 22.
- **Level-up:** 23.
- **Guardian:** 24 to 28.
- **Gifts:** 29, 30 and 44.
- **Sound Duel:** 34 to 36.
- **Rest:** 37.
- **Character, gear, themes and gems:** 38 to 41.
- **Scrolls:** 42 to 44.
- **Pantry:** 45.
- **Backup and restore:** 46 and 47.
- **Pause and welcome back:** 48 and 49.
- **Open from home screen:** 50.

**Cards.** There are 211 cards in 8 id groups: ph 26, cs 24, sw 24, nm 24, bh 31, ms 32, fd 38 and cv 12. The types are 160 picture-recall cards, 37 say-it, 10 server-talk, 3 picture and 1 two-answer. Of the 211, 205 carry the default `thStatus` "NEEDS NANCY".

**Zones.** There are 7: Phonics, Colors and Shapes, Numbers, Sight Words, Baby and Hospital, Maxwell Says and Kitchen. Five of them have a guardian. Maxwell Says and Kitchen end at scene 5.

**Levels.** Levels run from 2 to 20. Each of the 12 level cosmetics comes from `trophies`, and level 20 gives a title and a crown frame. There are 42 trophies in total. The Pantry has 9 items.

**Verses.** There are 10 weekly verses, then 30 more in `daily-verses.json`, for a 40-day cycle that starts on `weeklyStart` 2026-11-02. There are also 8 rest verses and 6 Jesus words.

**Settings.** There is no Settings screen; the spec forbids one (:396). The two switches, `slowMode` and `restWeeks`, live on the Character screen.

**Systems with no screen of their own.** These are the day streak and its moon, unlocks and reconcile, the Thai Review Queue, personal card slots, the service worker and its update chip, IndexedDB with the localStorage mirror, audio and `speechSynthesis`, auto-pause, rotation, and text size.

## 2. Attention by area

See `coverage-heatmap.png`, with 34 areas ranked. The raw numbers are in `coverage-data.json`.

**Heavily covered:**
- Bible verses and Jesus words: 22 renders, 4 sizes, 69 checks, shown 26 times.
- Guardian runs: 40 renders, 4 sizes, shown 19 times.
- Find-and-tap asks: 71 renders, 4 sizes, shown 20 times.
- Character: 70 checks.
- Say-it cards: 62 renders.
- Title: 64 checks.

**Never rendered at any size:**
- End of game and after the last level.
- Personal card slots.
- Day streak.
- Landscape.
- Real iPhone behaviour.
- Error and edge states.
- The 414 and 430 sizes.
- Audio.
- The Thai Review Queue.
- Unlock and trophy reward screens.
- Accessibility and text size.
- Long-term flow.

**Size skew across the 151 screens-v608 PNGs:**

| Size | PNGs |
|---|---|
| 390 | 105 (57 renders and 48 check renders) |
| 320×568 | 36 |
| 375×812 | 5 |
| 375×667 | 5 (guardian screens only) |
| 414 and 430 | 0 |
| Landscape | 0 |

**Cards on screen.** Only **38 of the 211 card words** appear in any rendered HTML:

| Group | Rendered |
|---|---|
| ph | 12 of 26 |
| cs | 9 of 24 |
| sw | 7 of 24 |
| nm | 3 of 24 |
| ms | 3 of 32 |
| fd | 3 of 38 |
| bh | 1 of 31 |
| cv | 0 of 12 |

Nine cards have English text longer than 30 characters; the longest is 40.

**Map renders.** All 6 Map screens were rendered once each, at 390 only. Spec :396 demands no overlaps and no scroll at 320×568, but the Map has never been rendered at 320.

**There is no runnable game.** Watchman's playtest (`watchman/playtest-v608/`) states it plainly: the "play" harnesses are static screen renderers. Every "walk" so far has been a spec walk or a sequence of renders. Nothing has run in Safari. Nothing has exercised IndexedDB, the service worker, audio wake, or a kill-and-resume.

## 3. Patterns

**What we keep finding:**
1. **Layout over the HUD, banner or heads.** Examples: the guardian toasts at 375×667, the 26 bubble over คิด, screen 48's ask under the pause card.
2. **The scene shrinking when a size changes.** Screens 25 and 28 shrank at 375×667, and it was found only when someone looked at that size.
3. **Stale or leading wording.** Examples: old ask wording, "Keep" labels, footers naming the wrong snapshot.
4. **Tool blind spots.** Examples: occl.py hung; the ribbon counted as the scene top; DOM checks see only files that were rendered; SUPERSEDED check lines still print True.

**Where the same problems probably hide, untouched:**
- Every screen that has never been rendered at 320 or 375×667: the Map, Rest, Pantry, gifts 29, 30 and 44, title 01, and backup.
- Cards with long text, such as the cv, fd and ms phrases, on say-it and server-talk cards at 320.
- Reward screens for trophies, unlocks and level 20.
- The full Map once all 7 zones are open.

The tool blind spot is built in. Any check that runs over the renders cannot see screens or states nobody has rendered.

## 4. Top 10 blind spots, ranked

| # | Blind spot | Why it matters for Nancy's first run | Cheap check | Owner |
|---|---|---|---|---|
| 1 | **No live build has ever run on a real iPhone.** This covers Safari 14 behaviour, IndexedDB, the service worker, audio wake, the silent switch, and Add to Home Screen. | Her first run happens in Safari on her phone. A dead audio wake, a lost save or a 7-day storage wipe would break day 1, and no render can show any of it. | Once a stage-1 build exists, Maxwell does a 10-minute pass of the §20 list on his iPhone: airplane mode, second launch with audio, kill and relaunch. Until then, QM checks every §4 API against Safari 14 support. | QM build, Watchman UX |
| 2 | **Audio and pronunciation.** 0 renders and 6 checks, even though the spec mentions audio 276 times. | Every card is spoken. On an iPhone the voice may mispronounce names, numbers, "Dr." or the respellings. Sound Duel depends on there being up to 4 English voices. | Script a list of every card's `en` that contains a digit, abbreviation, apostrophe or name, then have an iPhone speak 20 of them at 0.85 and 0.6. | Instructor language, Watchman |
| 3 | **173 of the 211 cards have never been on screen.** That includes all 12 cv cards and 30 of the 31 bh cards. | Long phrases such as "A corn dog with mustard, please." at 320 are exactly where overflow and clipped Thai happen, which is the same class of bug we keep finding. | QM loops every card through its card template at 320, then runs one DOM overflow check and makes one contact sheet. | QM build, Auditor gate |
| 4 | **The Map at 320 and in later states.** There are 6 Map renders, all at 390, one each. | She sees the Map after every run. The spec requires no overlaps and no scroll at 320, and nobody has looked. | Render 05 to 09 and 53 at 320×568 and 375×667 with all 7 zones open, then run the DOM tap-target check (44 pt, 8 pt apart). | QM build, Watchman |
| 5 | **Phone sizes other than 390 and 320.** There are 0 renders at 414/430, 5 at 375×812, and 375×667 only for the guardian screens. | We don't know Nancy's phone. The 375×667 shrink bug appeared the moment someone looked at that size. | Re-run `play_v608.py` for all 54 screens at 375×667 and 430×932, then run hidden_check and occl_qm. | QM build |
| 6 | **Rarely reached reward screens.** Rest has 2 renders, at 390 only. Gifts 29, 30 and 44 are at 390 only. There are no renders at all of the trophy, unlock, level-20 crown or streak moon screens. | Reward screens are the "you did it" moments. They show up after runs 3, 6 and 9 and after every level, and they share the banner-over-HUD layout that keeps failing. | Render each of them at 320 and 390 with real data from cards.json, then run the DOM check. | QM build, Auditor gate |
| 7 | **End of game and long-term play.** The spec has no text for this, and it has 0 renders. | The verse cycle needs `daily-verses.json`, which is not in the snapshot, so its place in the send set should be confirmed. `weeklyStart` is 2026-11-02, so a launch on Nov 1 gives d = −1 and index 39, which is a verse from that file. What happens after the last boss, all Pantry items bought, or level 20 is undefined. | Chancellor writes one paragraph each on "day 1 before Nov 2", "day 41" and "everything done". QM renders the Map and Character from a filled-in state. | Chancellor scope |
| 8 | **Pause, resume, kill and error states.** There are 5 renders, and no state test has been run. | A phone call or locked screen during her first run triggers auto-pause and Continue. A kill on a reveal or mid-boss must lose nothing (§10). | Auditor writes a small Python state-machine table for the §10 launch order with 6 kill points, plus corrupt or empty backups and a failed IndexedDB write. | Auditor gate |
| 9 | **The Thai Review Queue.** 205 of the 211 cards are "NEEDS NANCY", and there are new chip strings. | If the queue screen is cramped, or the Thai she flags isn't saved, she loses trust in the Thai on day 1. Pending strings also need Nancy by Nov 7. | Instructor makes one list of every NEEDS NANCY string with its first-run order. QM renders the backup and review lists at 320 with 205 entries. | Instructor language |
| 10 | **Landscape, iOS text size and accessibility.** 0 renders. | A child often turns the phone sideways. Reduce Motion and contrast are in the spec (:203, §9) but have never been checked. | Render 10 key screens at 568×320, again at 125% zoom, and again with `prefers-reduced-motion`. | Watchman UX |

**Areas that were left out of the top 10 and why.** Personal card slots (#2 on the heatmap) and the day streak (#3) are thin, but they don't block day 1. Unlocks and reconcile are covered by 18 checks, though nothing has rendered them. The thin areas also include the guardian zones' kneel screens at 375×812 and the Sound Duel at 375×667.

**Disk.** Usage was 92% (121.93 GB of 133.58 GB), below the 93% stop, and the outputs add less than 1 MB. The first scan attempt ran out of memory because the recursive glob followed something in audit/. It was rerun with os.walk and a memory cap, and it changed nothing.
