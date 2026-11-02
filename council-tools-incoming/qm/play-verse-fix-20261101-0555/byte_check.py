# QM play-verse-fix byte check. Usage: python3 byte_check.py <html dir> [PASTE path]
# For pages 26, 30, 37 at 320x568 / 375x667 / 390x844 it pulls every leaf text segment (<div class=.. data-txt=1 style=..>TEXT</div>) out of the html,
# finds each segment that carries a verse (its text, quote marks and whitespace ignored, contains the opening of a PASTE verse en or th), and compares
# that segment's raw UTF-8 bytes with the PASTE field. Every expected field must appear exactly once per render and match byte for byte.
# Composed labels (label + ' · ' + ref) and the ref / source lines are checked against the PASTE parts they are built from.
# Exit 0 only if every check matches; 1 otherwise. Read-only.
import sys, os, re, json, glob
D = sys.argv[1]; P = sys.argv[2] if len(sys.argv) > 2 else '/workspace/v608build/r2h-build/nancys-adventure-english-v6-08-1B-v32-PASTE.md'
J = next(json.loads(l) for l in open(P, encoding='utf-8') if l.startswith('{"version"'))
jw = J['jesusWords'][0]; t30 = next(t for t in J['trophies'] if t['id'] == 'axe-oak'); i30 = J['trophies'].index(t30)
w30 = [(i, v) for i, v in enumerate(J['verses']['weekly']) if v['ref'] == t30['ref']]; assert len(w30) == 1; iw, v30 = w30[0]; vr = J['verses']['rest']
EXP = {   # page: [(PASTE path, expected string, kind)]
 '26': [('.jesusWords[0].en', jw['en'], 'verse'), ('.jesusWords[0].th', jw['th'], 'verse'),
        ('.uiText.jesusWords.en + " · " + .jesusWords[0].ref', J['uiText']['jesusWords']['en'] + ' · ' + jw['ref'], 'label')],
 '30': [(f'.verses.weekly[{iw}].en', v30['en'], 'verse'), (f'.verses.weekly[{iw}].th', v30['th'], 'verse'),
        (f'.trophies[{i30}].word[0] + " · " + .trophies[{i30}].ref', t30['word'][0] + ' · ' + t30['ref'], 'label')],
 '37': [('.verses.rest.en', vr['en'], 'verse'), ('.verses.rest.th', vr['th'], 'verse'), ('.verses.rest.ref', vr['ref'], 'label'),
        ('.verses.rest.enSource + " · " + .verses.rest.thSource', vr['enSource'] + ' · ' + vr['thSource'], 'label')]}
for pg in EXP.values():
    for path, s, k in pg: assert not re.search(r'[<>&]', s), path   # no html escaping needed: raw bytes compare directly
SEG = re.compile(r"<div class='([^']*)' data-txt=1 style='([^']*)'>([^<]*)</div>")
NORM = lambda s: re.sub(r'[\s“”"‘’\']+', '', s)
ALLV = [v for v in [vr] + J['verses']['weekly'] + [jw]]
rows, bad = [], 0
for f in sorted(glob.glob(os.path.join(D, '*.html'))):
    tag = os.path.basename(f)[:-5]; pg = tag[:2]
    if pg not in EXP: continue
    raw = open(f, 'rb').read(); segs = [(m.group(1), m.group(3)) for m in SEG.finditer(raw.decode('utf-8'))]
    for path, want, kind in EXP[pg]:
        if kind == 'verse':
            key = NORM(want)[:16]; hits = [s for c, s in segs if key in NORM(s)]
        else:
            hits = [s for c, s in segs if s == want] or [s for c, s in segs if NORM(want)[:10] in NORM(s)]
        ok = len(hits) == 1 and hits[0].encode('utf-8') == want.encode('utf-8')
        if not hits: why = 'MISSING (no segment carries it)'
        elif len(hits) > 1: why = f'{len(hits)} segments carry it'
        elif ok: why = f'MATCH {len(want.encode())} bytes'
        else:
            a, b = hits[0].encode(), want.encode(); k = next((i for i in range(min(len(a), len(b))) if a[i] != b[i]), min(len(a), len(b)))
            why = f'DIFF at byte {k}: render {a[max(0,k-4):k+8]!r} vs PASTE {b[max(0,k-4):k+8]!r} (render {len(a)} B, PASTE {len(b)} B)'
        bad += not ok; rows.append((tag, kind, path, 'PASS' if ok else 'FAIL', why))
    # any other verse-looking segment that matches no expected field (e.g. a retyped verse)
    for c, s in segs:
        for v in ALLV:
            for fld in ('en', 'th'):
                if NORM(v[fld])[:16] in NORM(s) and s != v[fld] and not any(s == w for _, w, _ in EXP[pg]):
                    bad += 1; rows.append((tag, 'stray', f"verse '{v['ref']}' {fld}", 'FAIL', f'segment not byte-identical: {s[:40]!r}'))
for r in rows: print(' | '.join(r))
print(f'TOTAL checks {len(rows)}  PASS {sum(r[3] == "PASS" for r in rows)}  FAIL {bad}  (PASTE {P})')
sys.exit(0 if bad == 0 and rows else 1)
