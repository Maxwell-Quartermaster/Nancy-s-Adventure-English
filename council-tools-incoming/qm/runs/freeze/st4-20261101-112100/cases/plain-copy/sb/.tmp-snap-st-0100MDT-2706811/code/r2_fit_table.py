# R2 fit table by script (10:20 PM MDT steering, QM-relayed): every screen-26 option x ask x ramp (yes/no) x night title B (yes/no) x B1 B (yes/no).
# left = (staged bank - option cost) + 60 (night title B) + 11 (B1 B) - ask - 40 (ramp kept). Fits when left >= 0. Numbers come from round_totals.py.
# Usage: python3 r2_fit_table.py [--paste PASTE.md ...] [--md out.md] [--check chancellor.md]
import sys, re, itertools
sys.path.insert(0, '/workspace/v608build/round2/asset-depth'); import round_totals as RT
# r2e (Auditor r2d L1 + Chancellor's fit_table.py rule): the bank is worked out from the PASTE length, never pinned. Every PASTE given with
# --paste (default: the two staged PASTEs) must give the same bank, and it must equal round_totals.STAGED; on any mismatch the script refuses (exit 2).
import os as _os
LIMIT = RT.LIMIT
def bank_of(path): return LIMIT - len(open(path, encoding='utf-8').read())
def _pastes(argv):
    ps = [argv[i + 1] for i, x in enumerate(argv) if x == '--paste']
    if not ps and _os.environ.get('NAE_FIT_PASTE'): ps = _os.environ['NAE_FIT_PASTE'].split(':')
    return ps or list(RT._SP.values())
PASTES = _pastes(sys.argv[1:]); _banks = {p: bank_of(p) for p in PASTES}
if len(set(_banks.values())) != 1 or set(_banks.values()) != set(RT.STAGED.values()):
    sys.stderr.write('REFUSED: bank mismatch. From PASTE length: %s; round_totals.STAGED: %s\n' % (_banks, RT.STAGED)); sys.exit(2)
BANK = next(iter(_banks.values()))   # 403 on the r2d/r2e PASTEs (1A and 1B bank the same)
RESERVE = "chars left = room for later changes, English or new Thai; Nancy's Nov 7 Thai sign-off fixes use the separate 300-char reserve (188,200 to 188,500)."   # r2f (council 11:15 PM MDT): one neutral line per sheet; no per-row marks
COST = {'A': 0, 'B': 36, "C'": 82, 'D': 36}   # measured on the staged PASTE (r2d): B and D need only the spec 1.12 words (+36); C' names uiText.jesusWords at :220 (+82; no 📜, spec :344)
COST_C_NEW = 142   # C with a new uiText.jesusChip entry (61, NEEDS NANCY by meta.thStatusDefault) + its :220 clause (81): reproduces Auditor r2c H2
NTB, B1B = 60, 11   # night title B saves 60; B1 B saves 11 (round_totals SAVES)
assert dict((s[0], s[1]) for s in RT.SAVES)['night title B'] == NTB and dict((s[0], s[1]) for s in RT.SAVES)['B1 B'] == B1B
def rows(opt):
    b = BANK - COST[opt]
    for ask, ramp, ntb, b1 in itertools.product(('letter game', 'state pairs'), (True, False), (False, True), (False, True)):
        yield ask, ramp, ntb, b1, b + (NTB if ntb else 0) + (B1B if b1 else 0) - RT.ASK[ask] - (RT.RAMP if ramp else 0)
def fits(opt): return [r for r in rows(opt) if r[4] >= 0]
yn = lambda x: 'yes' if x else 'no'
def label(r):
    ask, ramp, ntb, b1, left = r; extra = [s for s, on in (('night title B', ntb), ('B1 B', b1)) if on]
    return f"{ask} {'+ ramp' if ramp else 'no ramp'}{(' + ' + ' + '.join(extra)) if extra else ''}: {left} left"
if __name__ == '__main__':
    a = sys.argv[1:]; md = ['# R2 fit table, every combination (QM, by r2_fit_table.py)', '', 'PASTE: ' + ', '.join(f'{p} ({LIMIT - _banks[p]:,} chars, bank {_banks[p]})' for p in PASTES), '', RESERVE, '', f'left = (bank {BANK} - option cost) + 60 night title B + 11 B1 B - ask (letter game {RT.ASK["letter game"]}, state pairs {RT.ASK["state pairs"]}) - {RT.RAMP} ramp kept.', '']
    for o in COST:
        md += [f'## Screen 26 {o} (+{COST[o]}): {BANK - COST[o]} banked', '', '| ask | ramp | night title B | B1 B | left | fits |', '|---|---|---|---|---|---|']
        md += [f'| {r[0]} | {yn(r[1])} | {yn(r[2])} | {yn(r[3])} | {r[4]} | {"yes" if r[4] >= 0 else "no"} |' for r in rows(o)] + ['']
    if '--md' in a: open(a[a.index('--md') + 1], 'w').write('\n'.join(md) + '\n')
    for o in COST: print(o, BANK - COST[o], '|', '; '.join(label(r) for r in fits(o)) or 'nothing fits')
    if '--check' in a:   # compare with a fit list in Chancellor's format: '- <ask>, ramp yes|no, night title B yes|no, B1 B yes|no: N left' under '## Screen 26 X'
        cur = None; theirs = {}
        for l in open(a[a.index('--check') + 1]):
            m = re.match(r"## Screen 26 (\w'?)", l); cur = m.group(1) if m else cur
            m = re.match(r'- (letter game|state pairs), ramp (yes|no), night title B (yes|no), B1 B (yes|no): (\d+) left', l.strip())
            if m: theirs.setdefault(cur, set()).add((m.group(1), m.group(2) == 'yes', m.group(3) == 'yes', m.group(4) == 'yes', int(m.group(5))))
        for o in COST:
            mine = set(fits(o)); th = theirs.get(o, set())
            print(f'CHECK {o}: mine {len(mine)}, theirs {len(th)}; only mine {sorted(mine - th)}; only theirs {sorted(th - mine)}')
