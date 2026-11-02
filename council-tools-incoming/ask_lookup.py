#!/usr/bin/env python3
"""**Quartermaster:** ask_lookup.py: check ASKS-LEDGER.md and SETTLED-RULINGS.md before anyone asks Maxwell.
Rule (Maxwell t542u, Council room): look it up, then ask QM, then Maxwell.
Usage:  ask_lookup.py "question text" [--top N] [--ledger PATH] [--rulings PATH]
        ask_lookup.py --selftest
Verdicts: ALREADY ANSWERED (show the quote, stop) / MAYBE (QM asks Maxwell one line: "does this still apply?")
          / NEW (post it to QM; QM adds one ledger row naming one asker and records the answer verbatim).
Source labels: MAXWELL OWN (his typed words) / ARA (RELAY) (third-person relay, word for word) /
PARAPHRASE ONLY (a bot's summary; never shown as Maxwell). Read-only: writes nothing.
Exit: 0 ALREADY ANSWERED, 1 MAYBE, 2 NEW, 3 usage or file error."""
import os, re, sys, math

BASE = '/workspace/v608build'
LEDGER = os.path.join(BASE, 'ASKS-LEDGER.md')
RULINGS = os.path.join(BASE, 'SETTLED-RULINGS.md')

STOP = set('''a an the and or but if of to in on at for with by from as is are was were be been being do does did
should would could can will shall may might must we i you he she it they them his her its our your their this that these
those there here what which who whom how why when where any all some no not yes so than then too very just about into
over under up down out off again also only own same such both each few more most other nancy maxwell game app screen
please ask asked asking question still use using get make made need needs want wants like one two'''.split())
SYN = {'pebble': 'rock', 'stone': 'rock', 'rock': 'rock', 'circle': 'dot', 'dot': 'dot', 'tuft': 'tuft',
       'popup': 'pop', 'pop': 'pop', 'colour': 'color', 'cog': 'gear', 'setting': 'gear', 'pantry': 'shop',
       'healthbar': 'health', 'hp': 'health', 'trophy': 'trophy', 'counter': 'tally', 'tally': 'tally'}

def stem(w):
    w = w.lower()
    for suf in ('ings', 'ing', 'ies', 'es', 'ed', 's'):
        if len(w) > 4 and w.endswith(suf):
            w = w[:-len(suf)] + ('y' if suf == 'ies' else '')
            break
    return SYN.get(w, w)

def toks(text):
    out = set()
    for w in re.findall(r"[A-Za-z0-9/']+", text.replace('-', ' ')):
        w = w.strip("'").lower()
        if w.endswith("'s"): w = w[:-2]
        if len(w) < 2 or w in STOP: continue
        if re.fullmatch(r't\d+u', w): continue
        out.add(stem(w))
    return out

LABEL = re.compile(r'\*\*([^*]+?)\*\*')

def classify(label):
    l = label.strip().rstrip(':').strip()
    if re.match(r'(?i)^ara\b', l) or 'relay' in l.lower(): return 'ARA (RELAY)'
    if re.match(r'^Maxwell\b', l) and 'paraphrase' not in l.lower(): return 'MAXWELL OWN'
    if 'paraphrase' in l.lower() or re.match(r'^(Quartermaster|Auditor|Watchman|Chancellor|Instructor)\b', l): return 'PARAPHRASE ONLY'
    return None

def segments(cell):
    """Split a cell into (label, kind, tnums, text) pieces at each bold source label."""
    marks = [(m.start(), m.end(), m.group(1)) for m in LABEL.finditer(cell) if classify(m.group(1))]
    segs = []
    if not marks:
        if cell.strip(): segs.append(('(no label)', 'PARAPHRASE ONLY', [], cell.strip()))
        return segs
    for i, (s, e, lab) in enumerate(marks):
        end = marks[i + 1][0] if i + 1 < len(marks) else len(cell)
        body = cell[e:end].strip(' /;')
        segs.append((lab.strip(), classify(lab), re.findall(r't\d+u', lab), body))
    return segs

def split_row(line):
    cells = [c.strip() for c in re.split(r'(?<!\\)\|', line.strip())[1:-1]]
    return cells

def load(ledger=LEDGER, rulings=RULINGS):
    rows = []
    for path, kind in ((ledger, 'ledger'), (rulings, 'rulings')):
        if not os.path.isfile(path): raise FileNotFoundError(path)
        section = ''
        for n, line in enumerate(open(path, encoding='utf-8'), 1):
            if line.startswith('## '): section = line[3:].strip()
            if not line.startswith('|') or re.match(r'^\|\s*-', line): continue
            c = split_row(line)
            if kind == 'ledger':
                if len(c) < 4 or c[0] == 'Ask': continue
                topic, status, ans, asker = c[0], c[1], c[2], c[3]
                rid = f'LEDGER:{n}'
                answer = ans; date = ''; src = 'ASKS-LEDGER.md'
                segs = segments(ans) if ans else []
                segs += [s for s in segments(topic) if s[1] != 'PARAPHRASE ONLY' or LABEL.search(topic)] if LABEL.search(topic) else []
            else:
                if len(c) < 6 or c[0] == 'ID': continue
                rid, topic, answer, status, date, src = c[:6]
                asker = ''
                segs = segments(answer)
            rows.append(dict(file=os.path.basename(path), line=n, id=rid, section=section, topic=topic, answer=answer,
                             status=status, asker=asker, date=date, src=src, segs=segs,
                             tok=toks(topic) | toks(answer), ttok=toks(topic)))
    return rows

def score(q, row):
    if not q: return 0.0
    hit = q & row['tok']
    thit = q & row['ttok']
    return (len(hit) + 0.5 * len(thit)) / (len(q) + 0.0001), len(hit)

def verdict_for(row, s, nhit):
    st = row['status'].upper()
    if s < 0.34 or nhit < 1: return 'NEW', ''
    if row['file'] == 'ASKS-LEDGER.md' and st.startswith('OPEN'):
        return 'NEW', f"OPEN ROW EXISTS in ASKS-LEDGER.md:{row['line']} (asker: {row['asker'] or 'QM'}). Do not ask Maxwell; post to QM, who carries the existing row."
    if st.startswith('OPEN') or st.startswith('UNKNOWN'):
        return 'NEW', 'Listed as open or unknown in SETTLED-RULINGS; post to QM.'
    weak = any(k in st for k in ('CONFLICT', 'SUPERSEDED', 'UNVERIFIED'))
    if s >= 0.6 and nhit >= 2 and not weak: return 'ALREADY ANSWERED', ''
    return 'MAYBE', ('Status says ' + row['status'] + '. ') if weak else ''

def show_row(row, out):
    out.append(f"  [{row['file']}:{row['line']} {row['id']}] {row['topic']}  | status: {row['status']}" + (f" | {row['date']}" if row['date'] else ''))
    if not row['segs']:
        out.append('    (no recorded answer)')
    for lab, kind, tn, body in row['segs']:
        a, b = body.find('"'), body.rfind('"')
        quotes = [body[a + 1:b]] if 0 <= a < b else []
        tns = ', '.join(tn) or '(t-number in label not given)'
        if kind == 'PARAPHRASE ONLY':
            out.append(f"    PARAPHRASE ONLY, not Maxwell's words [{lab}] {tns}: {body}")
        else:
            q = ' / '.join(f'"{x}"' for x in quotes) if quotes else '(no quoted words on record)'
            out.append(f"    {kind} [{lab}] {tns}: {q}")

def lookup(question, top=3, ledger=LEDGER, rulings=RULINGS):
    rows = load(ledger, rulings)
    q = toks(question)
    ranked = sorted(((score(q, r), r) for r in rows), key=lambda x: (-x[0][0], -x[0][1], x[1]['file'] != 'ASKS-LEDGER.md'))
    best = ranked[0]
    (s, nhit), row = best
    v, note = verdict_for(row, s, nhit)
    out = [f'QUESTION: {question}', f'VERDICT: {v}']
    if note: out.append('NOTE: ' + note)
    if v == 'ALREADY ANSWERED': out.append('ACTION: use the quote below; do not ask Maxwell.')
    elif v == 'MAYBE': out.append('ACTION: post to QM; QM asks Maxwell one line: "does this still apply?" with the quote.')
    else: out.append('ACTION: post to QM; QM adds one ASKS-LEDGER row naming one asker; his answer is recorded verbatim the same turn.')
    out.append('TOP MATCHES:')
    for (sc, nh), r in ranked[:top]:
        if sc <= 0: break
        out.append(f'  score {sc:.2f} ({nh} keywords)')
        show_row(r, out)
    return v, row, ranked, '\n'.join(out)

def selftest():
    cases = [
        ('Can the red Start button on the title stay red?', 'ALREADY ANSWERED', 't152u', 'MAXWELL OWN'),
        ('Should the circle dots on grass become grass tufts game-wide?', {'ALREADY ANSWERED', 'MAYBE'}, 't527u', 'MAXWELL OWN'),
        ('Should the gray pebbles on the title hill become tufts?', 'NEW', None, None),
        ('Should Sam wear a winter hat in the snowy kitchen scene?', 'NEW', None, None),
        ('Does the trophy counter show 0/85 or earned of 42?', 'NEW', 't102u', 'ARA (RELAY)'),
        ('Should the s36 mushrooms be recolored orange?', 'ALREADY ANSWERED', 't501u', 'ARA (RELAY)'),
        ('Do we still say Tap it on the ask card?', 'ALREADY ANSWERED', 't402u', 'MAXWELL OWN'),
        ('Is the verse pop-up shown on the title screen or the menu?', 'MAYBE', None, None),
        ('Is there a gear button on the main menu or no Settings gear?', 'NEW', None, None),  # open ledger row :397
        ('Must the attribution prefix be bold at the start of every line?', {'ALREADY ANSWERED', 'MAYBE'}, 't142u', 'ARA (RELAY)'),
        ('Which phrasing for the ask card, Can you find the word?', 'ALREADY ANSWERED', 't440u', 'MAXWELL OWN'),
        ('Should the moon move off the owl on tile 9?', 'ALREADY ANSWERED', 't471u', 'ARA (RELAY)'),
    ]
    ok = fail = 0
    for q, want, tn, kind in cases:
        v, row, ranked, txt = lookup(q)
        good = (v in want) if isinstance(want, set) else (v == want)
        if tn:
            segs = [s for s in row['segs'] if tn in s[2]]
            good = good and bool(segs) and all(s[1] == kind for s in segs)
        # invariant: no paraphrase segment is ever printed under a Maxwell or relay label
        for line in txt.splitlines():
            if ('MAXWELL OWN' in line or 'ARA (RELAY)' in line) and 'paraphrase' in line.lower().split(':')[0]:
                good = False
        print(('PASS' if good else 'FAIL'), '|', q, '->', v, '|', row['id'], row['file'])
        if not good: print(txt)
        ok += good; fail += (not good)
    # invariant over every row: paraphrase labels never classify as Maxwell or relay
    rows = load()
    bad = [(r['id'], s[0]) for r in rows for s in r['segs'] if 'paraphrase' in s[0].lower() and s[1] != 'PARAPHRASE ONLY']
    bad += [(r['id'], s[0]) for r in rows for s in r['segs'] if s[0].lower().startswith('ara') and s[1] != 'ARA (RELAY)']
    good = not bad
    print(('PASS' if good else 'FAIL'), '| invariant: paraphrase and relay labels never shown as Maxwell', bad[:5])
    ok += good; fail += (not good)
    # invariant: every Maxwell-own segment carries a t-number
    miss = [(r['id'], s[0]) for r in rows for s in r['segs'] if s[1] == 'MAXWELL OWN' and not s[2]]
    good = not miss
    print(('PASS' if good else 'FAIL'), '| invariant: every MAXWELL OWN quote has a t-number', miss[:5])
    ok += good; fail += (not good)
    print(f'SELFTEST {ok}/{ok + fail} PASS')
    return 0 if fail == 0 else 1

def main(argv):
    if not argv or argv[0] in ('-h', '--help'):
        print(__doc__); return 3
    if argv[0] == '--selftest': return selftest()
    top = 3; ledger = LEDGER; rulings = RULINGS; words = []
    it = iter(argv)
    for a in it:
        if a == '--top': top = int(next(it))
        elif a == '--ledger': ledger = next(it)
        elif a == '--rulings': rulings = next(it)
        else: words.append(a)
    try:
        v, row, ranked, txt = lookup(' '.join(words), top, ledger, rulings)
    except FileNotFoundError as e:
        print('ERROR: missing', e); return 3
    print(txt)
    return {'ALREADY ANSWERED': 0, 'MAYBE': 1, 'NEW': 2}[v]

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
