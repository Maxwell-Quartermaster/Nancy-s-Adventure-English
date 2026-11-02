# QM play-verse-split (26+37 only; page 30 left exactly as ee74f3ef, per QM ruling Nov 1 2026): builds new/play_v608.py from old/play_v608.py (ee74f3ef) by exact, count-checked string replacements.
p_old, p = 'old/play_v608.py', 'new/play_v608.py'; s = open(p_old, encoding='utf-8').read()
def rep(a, b):
    global s; assert s.count(a) == 1, a[:80]; s = s.replace(a, b)
rep("G = json.load(open('/workspace/v604build/screens/guardians.json'))   # dumped from mock-t346u/map_t346u.guardian() by dump_guardians.py\n",
"G = json.load(open('/workspace/v604build/screens/guardians.json'))   # dumped from mock-t346u/map_t346u.guardian() by dump_guardians.py\n"
"# QM play-verse-fix (Nov 1 2026, candidate): verse text comes straight from the PASTE JSON line, never retyped here (PASTE :344, :404, verses.textRule).\n"
"# NAE_PASTE overrides the path; default is the pointer's paste_1b_path. No quote marks are added; '\\n' renders as a line break (white-space:pre-line).\n"
"def _paste_json():\n"
"    p = os.environ.get('NAE_PASTE')\n"
"    if not p:\n"
"        ptr = dict(l.split('=', 1) for l in open('/workspace/v608build/CURRENT-SNAP.txt', encoding='utf-8').read().splitlines() if '=' in l)\n"
"        p = '/workspace/v608build/' + ptr['paste_1b_path']\n"
"    for l in open(p, encoding='utf-8'):\n"
"        if l.startswith('{\"version\"'): return json.loads(l)\n"
"    raise SystemExit('no PASTE JSON line in ' + p)\n"
"PJ = _paste_json()\n"
"def verse(ref):   # the one PASTE verse with this ref: verses.rest or verses.weekly[]\n"
"    vs = [v for v in [PJ['verses']['rest']] + PJ['verses']['weekly'] if v['ref'] == ref]; assert len(vs) == 1, ref; return vs[0]\n"
"def vtx(t, cls, extra=''):   # a verse string exactly as in the file; a '\\n' poetry break shows as a line break\n"
"    return tx(t, cls, ((extra + ';') if extra else '') + 'white-space:pre-line') if '\\n' in t else tx(t, cls, extra)\n")
rep("        j = D['jesusWords'][0]   # 9:05", "        j = PJ['jesusWords'][0]   # play-verse-fix: from the PASTE (same bytes as cards.json). 9:05")
rep("card([tx('Matthew 11:28', 'e20'), tx('“Come to me, all who labor and are heavy laden, and I will give you rest.”', 'e15', 'font-size:18px'), tx('ESV · THSV11', 'e15')], 260,",
    "card([tx(r_['ref'], 'e20'), vtx(r_['en'], 'e15', 'font-size:18px'), vtx(r_['th'], 't17'), tx(r_['enSource'] + ' · ' + r_['thSource'], 'e15')], 300 if SE else REST_CH,")
rep("    v = D['restScreen']\n", "    v = D['restScreen']; r_ = PJ['verses']['rest']   # play-verse-fix: verses.rest from the PASTE, no added quotes, Thai under the English (as the 29 scroll)\n")
rep("def rest():\n", "REST_CH = 320   # play-verse-fix: card height with the Thai line (was 260); 300 at 320 x 568 so the card clears the restScreen ribbon\ndef rest():\n")
open(p, 'w', encoding='utf-8').write(s); print('wrote', p)
