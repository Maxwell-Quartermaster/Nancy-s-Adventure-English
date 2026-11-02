# Composes FIXLOG.md: every line starts with the bold attribution prefix.
B = '/workspace/v608build/scene-fill-20261101/'; P = '**Quartermaster:** '
L = ['scene-fill fixes. The per-page lines come from fix_r2h.fix (imported read-only) via code/fill.py.'] + [l for l in open(B + 'code/fixlog-fill.txt').read().splitlines() if l.strip()]
L += ['extra fixes beyond fix_r2h.fix (code/fill.py, code/menu.py, code/rest.py):',
 'front desk (E-*, 12 pages): ms-21 is a sentence card and keeps its own PASTE ask "Where are the keys?" / "กุญแจอยู่ไหนครับ" (as bh-24). An earlier tapPrompt rewrite was reverted (Instructor copy fault 1, 01:24 MDT).',
 'indoor windows (home, kitchen, front desk; not front-desk base): the window sky follows the step (m #F9CFA4, d #9CCBF2, a #F6D98E, e #F4A862, n #2B3A6B). The disc is the sun #FFE27A, or the moon #FFF3C4 at night.',
 'pond m/d/a: stage A pins an evening setting sun at the right edge, so these use the meadow tod sun placement for steps 1-4 (translate(-170px,120px)), the same as the park.',
 'kitchen 320 (5 pages): Thai ask "หา croissant เจอไหม" is set to nowrap (it had wrapped to a clipped 4th line). 17px / lh 1.7 unchanged.',
 'menus (8 pages): snapshot copies of r2h M1/M3 (src-snapshot/). Sky stops are set to the title e/n skies, with a tint rect inside the sky SVGs only. Banner greeting is uiText greetEvening / greetNight (A). The sun is recoloured (orange at e, moon at n). Morning is not re-rendered because M1/M3 have it.',
 'rest (5 pages): the verse card comes from PASTE 317e91ce verses.rest + verses.attribution: no added quote marks (:344), the THSV11 Thai line (:404), and (ESV) and (THSV11) as separate small tags (:346). This replaces the play_v608 text (quoted EN + "ESV · THSV11") (Instructor copy fault 2). Card is 260pt at 390 (content 242pt) and 292pt at 320 (content 291pt). At 320 the ribbon is at top 126 and 296pt wide, and the scene is held to the screen bottom.',
 'rest Sunset / Starry skies are CONCEPT palettes; the spec gives only the names (pantry sky-sunset, trophy sky-starry).',
 'note: the current r2h 390 rest (round2/r2h/html/37-rest-screen-390x844.html 3c780acd) and screens-v608 37 carry the same verse fault. They were not touched here.',
 'pond evening: skipped on purpose (brief: skip pond evening if the r2h job has it). fill.py PONDE checks that round2/r2h/png/stage-A-meadow-evening-pond-390x844.png and -320x568.png exist; both did (r2h, 00:48 MDT; a0d98dbb / b483659c), so jobs.json has pond_evening_skipped=true. It was not a failure. S03/S04 therefore have 4 panels (m, d, a, n).',
 'menus 390 (4 pages): Maxwell t527u / Watchman BLOCK: the 4 five-petal circle flowers on the menu grass are replaced by 4 three-blade tufts (fix_r2h.tuft, #0F3A14) at the same spots. The 320 menus have no scene panel and no flowers, so they are unchanged.',
 'midday uses spec :227 state d (step 2), emitted as data-tod=\'d\' (the old renderer marked step 2 as \'a\').']
open(B + 'FIXLOG.md', 'w').write('\n\n'.join(P + l for l in L) + '\n')
print(len(L))
