# Nancy's eyes: showcase tour (Maxwell t446u, QM-relayed)

From the staged round 2 build (round2d tiles and sheets, frozen as v608build/snap-r2d-2233MDT and carried unchanged into v608build/snap-r2g-2326MDT; this INDEX is the r2g copy: PASTE 1A 106a0661 187,797 with "never over a target"; 1B 2eebff94 187,797 under trim-1B/): round 2 ask wording on every ask, sky B at 320, 16 pt edges, Guardian on the chip line, screens 33 and 48 inert. 390 renders; a 320 copy (tile "s") only where the scene layout differs. Answer with a tile number ("fix 13", "9s").

## Sheet 1: Opening the game  (showcase-1-opening.png, md5 8dcce473f9dbc98ee2b0c03e3caa2351)
- **1**: Title screen. (01-title.html)
- **2**: Verse of the day pops up over the menu. (02-main-menu-verse-popup.html)
- **3**: Main menu. (03-main-menu.html)
- **4**: The map on day 1. (05-map-day1.html)
- **5**: She taps Word Meadow: the zone chooser. (07-map-word-meadow-chooser.html)

## Sheet 2: Each zone's first scene  (showcase-2-zones.png, md5 923bacf2d4bfd6003db88372b61d89ae)
- **6**: Word Meadow, first ask. (10-word-meadow-scene.html)
- **6s**: Word Meadow at 320 × 568: the scene shrinks so the kite stays below the top bar. (10-word-meadow-scene-320x568.html, 320 × 568)
- **7**: Golden Fields. (31-golden-fields-scene.html)
- **8**: Home Lake. (32-home-lake-scene.html)
- **9**: Echo Forest, first ask. (zone-forest-ask-390x844.html)
- **9s**: Echo Forest at 320 × 568: the owl and lantern stay below the top bar. (zone-forest-ask-320x568.html, 320 × 568)

## Sheet 3: Asking and answering  (showcase-3-asking.png, md5 f4a8453e5a2d57fbc24084a5c68d9f64)
- **10**: An ask card with a phrase. (54-phrase-ask-card.html)
- **11**: A right answer. (11-word-meadow-scene-right.html)
- **12**: The reveal: a hug card to say out loud. (12-reveal-right.html)
- **13**: A gentle miss on a two-answer card. (18-two-answer-wrong-tap.html)
- **14**: After a miss: "Now you know it." (14-reveal-gentle-retry.html)
- **15**: Say it: a sight-word card. (15-say-it-sight-words.html)

## Sheet 4: The walk and the Word Guardian  (showcase-4-walk-guardian.png, md5 dc0939b8b077d425faec4b2d0f85a85f)
- **16**: The walk (screen 24, staged): the Guardian name sits on the zone-chip line. (W24-walk-B-390x844.html)
- **16s**: The walk at 320 × 568. (W24-walk-B-320x568.html, 320 × 568)
- **17**: The Guardian's hint: words of Jesus. (26-guardian-hint-jesus-words.html)
- **18**: The Guardian kneels. (27-guardian-kneels.html)
- **19**: Sam wins: the Guardian kneels and gives the scroll. (28-guardian-win.html)

## Sheet 5: Rewards, gear, pause and the end of a level  (showcase-5-rewards-pause.png, md5 f1a2e8d00ec840a6ef8c1708eb9b8e26)
- **20**: A verse scroll as a gift. (29-verse-scroll-gift.html)
- **21**: Level up. (23-level-up-reward.html)
- **22**: End of a Sound Duel round. (36-sound-duel-round-done.html)
- **23**: Character gear. (38-character-gear-mmo-tooltip.html)
- **24**: The golden pantry. (45-character-golden-pantry.html)
- **25**: Back after a pause: one Continue button. (48-continue-after-pause.html)

## Timing for the round 2 picks (r2e)
- Maxwell's R2 pick and screen 26 pick need to land by Nov 2 (freeze Nov 4, 11:59 PM). If they slip past Nov 3, there is no R2 ask in this paste and v6-09 picks it up.
- Writing and Thai-checking time (Instructor): state pairs about 1 hour, letter game about 2 hours. Every new string goes on Nancy's Nov 7 list either way.
- chars left = room for later changes, English or new Thai; Nancy's Nov 7 Thai sign-off fixes use the separate 300-char reserve (188,200 to 188,500).

## Checks on every tile
- DOM check (domcheck_r2: Thai 17 px+, Thai line height 1.7+, clipping, overlap, 44 pt, 16 pt edges): all clean
- Placeholder text (___, (word), {word}, NEEDS NANCY, TODO): none
- Old ask wording left in the tour tiles, visible or hidden ("Where is the …?" / "อยู่ที่ไหน"): none. Every tile is its round 2 copy (tile 25, screen 48, reads "Can you find the kite?" under its pause card too); the pre-round-2 candidate renders in screens-v608 keep the old ask.
- Old tapPrompt wording in every frozen render source (107 html): none. "Where are the keys?" is card ms-21's own sentence, which P1 keeps (sentence cards keep their en/th): 6 front-desk renders.

## Left out, and notes for Auditor (sending waits on Auditor)
- Auditor eb2674be: tile 21 (screen 23) has no Back button (reward screens leave only by Got it, PASTE :72); the 02b verse at 320 scrolls in its card (P7, +52; 02b-main-menu-verse-popup-longest-320x568-scrolled.png shows the end); the 1A trim on 17-19 cuts the Pray / High five plates (open finding, see the trim sheet). Tile 22 at 320: roundDone heads the card.
- Instructor gate 8:35 PM MDT, fixed as render bugs (no PASTE change): tile 13 (screen 18) now has the Moonstone X on her wrong tap (High five) and the Gold glow on Pray, the shown prompt's answer, as PASTE :250 says (the old render put both on High five; the two-answer card uses an X, not a wiggle: "no shake", :250); tile 21 (screen 23) card now reads Level 3 like its HUD (the Level 2 was hard-coded in the render; the PASTE gives no level number); tile 22 (screen 36) Round complete! moved under the Echo Knight plate at 390 (it sat on the plate; the PASTE :324 gives no position), and at 320 it heads the card with +30 XP so it never covers the heroes. Tile 19 reads The Guardian is beaten.
- For Auditor: at 320, screen 36 (and the 34/35 duel screens that share it) the Echo Knight plate overlaps the knight's helmet; unchanged from the approved 320, not fixed here.
- Settings: no settings screen is rendered in v6-08 (46 backup view is not settings and shows a "(word) อยู่ไหน" review-queue line and a "bh-30 · ______" blank), so it is not in the tour.
- 13 (meadow retry: the kite glows after a wrong tap, with "Take your time"): this is the after-miss grace hint the spec allows (PASTE :231 "Another tap: that object wiggles, the right one glows as a hint, then `wrongText` and a grace line; she tries again"). It already shows the after-miss state; unchanged, not in the tour.
- 25 (guardian letters "t____/th/"): staged (round2.py P6, a QM-relayed staged fix; Auditor eb2674be H1): sw-19 choices run -> three (nm-10's own word, 5 letters, /th/), +2 chars, so "t____ /th/" fits two choices. Screens 25 and 26 re-rendered; 25 is not a tour tile, 26 is tile 17.
- 24-28 now carry the Guardian name on the zone-chip line (P5); 24 itself is replaced on the path by the staged walk (tile 16).
- Tile 2: the menu under the verse pop-up is now inert (aria-hidden, no taps), 0 chars; png unchanged.
- Home-lake rooms (tiles 8, 10, 14) are shown as approved: the 390 ceiling trim is still Maxwell's 1A/1B pick (round2/sheets/trim-pick-1A-vs-1B-390.png).
- Near-duplicates skipped: 52 night title, 04/51 hearth menus, 06/08/09/53 maps, 11-13 meadow variants, 16/20/21 say-it, 19, 35, 37-47 other character pages.

