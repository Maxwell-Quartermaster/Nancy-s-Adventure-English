# Maxwell's Eye: checker rules from Maxwell's own tile critiques
Owner: Auditor (design, Maxwell t98u, Nov 1 2026 12:37 AM MDT). Implementation: Chancellor (sole editor). Part of DESIGN-v5 (d7713bf6).
Source: Maxwell's critiques of tiles 1-26 as relayed in t98u. TODO (Watchman): quote his exact words from the QM session per rule.

## What he approves / rejects (the principle every rule serves)
Approves: placement looks intentional, proportions stay consistent, physics look natural (gravity, grounding), colors carry meaning, nothing covers what the player taps.
Rejects: anything that looks accidental, floating, or like a placeholder brush stroke.
Also: don't over-change what is already good.

## Method
- PIXEL: from the PNG (Watchman's ground_check style).
- GEOM: from a render sidecar JSON of element boxes and rotations, exported by the renderer from the DOM (QM). Far more reliable than pixels for layout rules.
- REF: diff against an approved reference render (16/16S ground, 25 hands, 22/26 nameplates, approved tiles).
- EYE: can't be automated reliably; the checker lists it as ASK and a named bot signs it off by eye.
Severity: BLOCK (never sent) or ASK (sent only with a named eye sign-off on the send record).

## Rules
ME1 Grounded trees. "Floating trees that don't connect to the grass." Tiles 6, 11, 12, 15, 18, 19. PIXEL (exists: float). BLOCK.
ME2 No fake walkway. "Thin gray-tan brush strokes randomly placed." Tiles 11, 12, 18, 19. PIXEL (exists: path). BLOCK.
ME3 Ground dots are three-tuft grass, not rocks or flowers. Tile 11. PIXEL: small non-green blobs on grass. BLOCK.
ME4 Room proportions. "Too much ceiling", grow the wall; consistent across levels, no size jumps or hero repositioning. Tiles 8, 10. GEOM: ceiling band / room height <= ref ratio (from approved room); hero box size+position within tolerance across all room screens. BLOCK on jumps; ASK on ratio.
ME5 Focal objects not hidden. "Moon behind the owl, move to center." Tile 9. GEOM: no focal decor (moon, owl, signs, hero, boss) overlapping another focal box. BLOCK.
ME6 Furniture reads in front of the wall. "Bed almost against the wall." Tile 10. GEOM: furniture base sits below the wall baseline by >= ref gap. ASK.
ME7 Gravity. "Tie hanging off to the side... normal gravity." Tiles 8, 10, 13, 14. GEOM: hanging items rotation ~0 deg and centered under the hook. BLOCK.
ME8 Nothing over a tap target. "Word bubbles overlapping buttons." Tiles 17, 26. GEOM (Auditor's occl layout layer): bubble/text box ∩ button box = 0 at 320/375/390. BLOCK.
ME9 Colors carry meaning. Green = right. Zone markers neutral = bright neon orange (Home Lake red "looked like she was doing something wrong", tile 13). Red fills only for boss health bars (tiles 22, 26). PIXEL+GEOM: saturated red outside boss-bar boxes => BLOCK, except approved scenery listed in REF (s36 mushrooms stay red, t501u "always fine"). Zone marker hue must be the approved orange.
ME10 Boss nameplate everywhere. Loved style on 22/26; extrapolate to every boss. Health bar red and a different color from the plate. Echo Knight: same plate, smaller, barless. GEOM+REF: every boss screen has a plate; bar hue red != plate hue; Echo Knight plate scale < boss plate, no bar. BLOCK.
ME11 Reference styles win. Character-select hand from tile 25 over newer ones unless animation is wired (tile 21). REF. ASK.
ME12 Same layout at every size. "Icon placement awkward on L and S"; open/closed book bottom right. GEOM: each icon's relative position matches the reference size within tolerance. BLOCK.
ME13 Don't over-change what's good. Tile 20 (clean borders, compact scroll, but keep what's good); approved tiles stay approved. REF: any approved tile that differs from its approved render beyond threshold => ASK, with the Maxwell message that asked for the change named (e.g. t474u on tile 14), else BLOCK.
ME14 Leave alone what he said is fine (s36 mushrooms, t501u). REF: locked regions must be pixel-identical. BLOCK.

## Owners
Watchman: ME1-3 (pixel), ME9 hue scan, exact-quote pass for every rule.
QM: geometry sidecar from the renderer (element boxes, rotations, names, sizes) + REF library of approved renders with the Maxwell message for each.
Auditor: ME8 (occl), ME4-7/ME10/ME12 geometry rules as diffs to Chancellor; planted-fault case for every rule; mutation pass.
Instructor: ME9/ME10 wording tie-ins (no fail meaning in color/labels), content layer unchanged.
Chancellor: integrates all as layer "maxwell-eye" in send_guard, sole editor, posts md5s.

## Testing
Each rule gets a clean case and a planted-fault case made from real tiles: floating tree, path stroke, rock dots, tall ceiling, moon behind owl, bed on wall, tilted tie, bubble on button, red zone marker, missing boss plate, yellow bar, Echo bar present, moved icon on S, changed approved tile, recolored mushroom.
