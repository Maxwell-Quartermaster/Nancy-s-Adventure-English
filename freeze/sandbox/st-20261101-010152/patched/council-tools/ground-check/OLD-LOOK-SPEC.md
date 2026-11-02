# "Old look" — precise definition (owner: Watchman, for Auditor's send-guard)
Based on: snap-r2h-0021MDT, pointer 907062f0 (repointed 00:33 MDT; render code unchanged from 09415ff9). Tool: ground_check.py v2 13fc304c.

Approved look = Maxwell's 16/16S (t441u, t128u): outdoor ground is grass with tufts, there is NO walkway, every tree is rooted in grass.
A screen has the OLD LOOK if ANY of these is true on an outdoor scene:

O1  Walkway/sidewalk stroke — path colour #E8D9A8 @ .85 alpha (find_t328u.py:72,:76; t441u_outdoor.py; stage_v608.py W24/B)
    or #D8C99A @ .8 (stage_v608.py:36-37, scene A), drawn over grass #36A13D / #259D39.
    Test: >= max(40 px, 0.04% of image) path-coloured pixels with grass within W/40 px on the same row.  [AUTOMATED]
O2  Floating tree — a round-crown tree (trunk #8A5A34/#6C4425 under both canopy tones #7ECA72 + #28792D) with no grass
    in the 0.35*trunk-height px below its foot. Cause seen: find_t328u.py:75 (tree 73.3 pt above the grass).  [AUTOMATED]
O3  Bare grass — an outdoor ground band with no tufts.  [EYE CHECK ONLY: tool cannot see tufts yet]
O4  Old ask wording on the scene ("Where is the …", old kite ask) — a TEXT check, owned by Auditor's PASTE/sheet gate, not pixels.

Applies to: dimmed screens too (pause card, modal scrim). v2 estimates the dim level k from the grass palette and re-checks
with every colour scaled by k ([dimmed xk] in the output). Self-test plants O1 at 70% and O2 at 55% brightness: both BLOCK, clean dim PASS.
Does NOT apply to: deliberate "before" panels on before/after sheets (QM decides if those are sent; they will always BLOCK).

Known blind spots (must stay on the eye-check list):
- trunks under 2 px wide (tiny thumbnails), pines (no round canopy), tufts (O3)
- coloured (non-black) overlays: v2 models a black scrim only
- dimming below 40% brightness
- JPEG compression can shift colours past tolerance (untested on real JPEGs)

Rename-proofing (v2): files are picked by header bytes (PNG/JPEG/GIF/WebP), not by extension, so a sheet renamed .jpg or
with no extension is still checked. send-guard should do the same (Auditor's g4 fix 1).
