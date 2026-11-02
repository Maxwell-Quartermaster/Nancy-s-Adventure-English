**Quartermaster:** scene-fill-20261101: a staging CANDIDATE for the gaps in scene-inventory-20261101.md (d3cde7b5). Not frozen, the pointer has not been moved, and nothing has been sent.

**Maxwell:** "Yes, fill every gap" (t511s1901, scene-fill card).

**Quartermaster:** base: snap-r2h-0021MDT, pointer CURRENT-SNAP.txt f6dac2d0, PASTE 317e91ce. Every sidecar renders/<tag>.json carries html_md5 (the md5 of html/<tag>.html, the exact file that was rendered), png_md5, source_html + source_html_md5, paste_md5, pointer_md5, vw, vh, snap, html, png, el.

**Quartermaster:** code/: fill.py (scenes + titles), menu.py, rest.py, shoot.py (private Chrome on port 9349, profile /dev/shm/qm-fill), sheets.py. src-snapshot/ holds the shutil.copy2 copies of the live r2h M1/M3 menus and the 37 rest page.

**Quartermaster:** sheets/S01-S17 are pick sheets grouped by location, with at most 6 tiles each. S14-INTERNAL-title-night-AB is INTERNAL (night B) and must never go on a Maxwell send.

**Quartermaster:** ground_check f46a2d29 BLOCKs park-a-390x844, pond-m-390x844 and pond-m-320x568. The flagged pixels are sky just above the hill line, where the warm m/a tints fall inside the path tolerance (97-100% of them sit above the first grass pixel in their column). The art was not altered. These 3 are pending an eye review.

**Quartermaster:** pond evening was skipped on purpose: the r2h job already has stage-A-meadow-evening-pond at 390 and 320 (00:48 MDT). It did not fail, which is why S03/S04 have no Evening panel.

**Quartermaster:** see FIXLOG.md for every change made to each page.
