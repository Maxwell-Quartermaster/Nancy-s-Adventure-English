# v5-34 Art Direction — "Hill Sword" storybook look (from library #77)
Logged Oct 31 2026, 2:38 AM PT. Maxwell order t273u. SPEC ONLY — no art work started.
Reference: asset-library #77 = council-images/Q-0759_title-screen-excalibur-hill-concept.jpg (md5 f2e8d32c8e3ddbb91dcd5ec3ada89fd0; AI concept render from t216u, Oct 30; write-up v520/q0759-title-screen-concept.md). Reference only — never pasted or traced; all build art is hand-drawn original SVG. "Excalibur" is an internal nickname; no brand/legend names in Build text or art files.

## Goal
Roll the #77 warm storybook look across the whole game for v5-34: backgrounds, lighting and UI.

## Keep as-is
- Character models (Sam, Nancy): unchanged — same rig, faces, hair, clothing, proportions (Sam 5.98 heads per #294 fix), line weight. The new style does not touch them.
- Weapons designs, verses (byte-identical), Thai rules (17px+, lh 1.7, no stroke, Kanit/Thonburi), grace wording, no timers/energy/leaderboards.

## The look (what changes)
1. Lighting: warm sunny key light from upper left; soft light rays from the sky (CSS/SVG shapes, opacity only); one warm glow and a sparkle around hero objects (title sword, unlocked weapons, trophies).
2. Backgrounds: painterly storybook scenes — rounded grassy hills, chunky round storybook trees, small cottages/paths where they fit — layered on the existing Bob Ross 7-layer structure (L0 sky to L6 framing trees stay; restyle each layer, do not add or remove layers).
3. Hero sword accent: ornate gold with a blue gem and soft glow as the signature accent colour pairing (gold + blue) for highlights, badges and the title sword.
4. UI: gold-and-stone frames (ring/stud trim from Q-0758) on panels, cards and buttons; chunky rounded shapes kept.
5. Palette: warm golds, sunny greens, sky blue, stone grey; Ink #10170F outline on the front layer kept.

## Caution (Maxwell): overlap between elements
- No element may overlap another unless it is meant to (frame trim must not cover text, Thai, buttons, hero or sword; light rays and sparkles sit behind UI and never over text; trees never cut through cards or buttons).
- Check every screen at 320x568 and 390x844 (Safari 14 / iOS 14.2): minimum 8px clear gap between frame trim and any text or tap target; tap targets 44pt; Thai lines never clipped.
- Pre-ship pass adds an overlap check per screen (bounding boxes of text, buttons, hero, sword, frames) with screenshots.

## Open points for council vote before art starts
- Conflicts with standing rules: rugged dark-line world style, flat iron button #3E5A7A + Hero Yellow text, "no UI gradients except the sky", one flat highlight per material. Decide which give way to the storybook look (soft glows, painterly shading) and how, within transform/opacity animation and the static reduced-motion fallback.
- Budget: v5-34 stays under the 188,200 hard ceiling (188,200–188,500 Thai reserve untouched) and the art cap; any single SVG over 2,500 chars needs a vote. Painterly texture must come from flat shapes, not big paths or raster.
- Timing: v5-34 gate is Nov 4, 11:59 PM PT (content freeze). If the restyle doesn't fit, it moves to v6; weapons keep priority.

## LOCKED (Maxwell t330u, Oct 31, 2026): one parchment base for all gameplay UI
- Tan parchment is the single base tone for every gameplay UI surface: buttons, plates, panels, question cards, HUD plates.
- Use the same tone everywhere across the whole interface. Gold accents (frames, trims, rings) do the separating work, not different base colors.
- Exact hex = the tan parchment of the Maxwell-approved t328u play-screen mocks (council-images/Q-shot-t328u-*); builder pins it in the spec as one shared token.
- Exceptions only where meaning needs color: the darker green Next/correct button (#2E7D32, t320u) and rarity ring colors.
- Sits alongside the #77 Hill Sword storybook aesthetic above (v5-34).

- Shields are round or square only, never teardrop or kite (Maxwell t336u).
