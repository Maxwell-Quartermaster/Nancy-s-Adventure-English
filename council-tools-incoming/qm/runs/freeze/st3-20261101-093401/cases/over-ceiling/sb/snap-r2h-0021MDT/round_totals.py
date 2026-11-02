# Round totals for every pick round (Chancellor 8:20 PM MDT; Auditor eb2674be and Council 8:43 PM MDT sizes). One table, read by the ledger,
# the combined pick sheet and every pick sheet footer, so the numbers never drift. Sizes read from the staged PASTEs (1A and 1B both 187,797 after the 9:05 PM MDT ruling, QM-relayed: 1A adds ', never over a target' +21).
LIMIT = 188200; P1748 = 187208
FIXES = [('sky B', 79), ('16 pt edges', 41), ('guardian chip (Maxwell t445u, QM-relayed)', 50), ('walk scene shrinks below the banner (eb2674be H2)', 38), ('sw-19 three (eb2674be H1)', 2),
         ('long verses scroll in their card (eb2674be H4; council 9:19 PM MDT, QM-relayed: a fix, not a pick)', 52)]
BANK = 754 - sum(c for _, c in FIXES)   # 492 before the trim pick
TRIM = {'1A': 89, '1B': 89}            # 1A: 68 + 21 ", never over a target" (9:05 PM MDT, QM-relayed); 1B: "front desk and kitchen" (eb2674be H3, -4)
VERSE_FIX = "fixed: long verses scroll in their card (+52, already counted in the 403)"   # verse option B is out: it breaks the verse guard (Instructor 42ecfd0a, council 9:19 PM MDT)
ASK = {'letter game': 413, 'state pairs': 367}; RAMP = 40
def bank(t): return BANK - TRIM[t]                                   # 1A 403, 1B 403
def left(t, a): return bank(t) - ASK[a] - RAMP
COMBOS = [(t, a, left(t, a)) for t in TRIM for a in ASK]
def fmt(n): return format(n, ',')
def verdict(n): return 'fits (%s left)' % fmt(n) if n >= 0 else 'over by %s' % fmt(-n)
_SP = {'1A': '/workspace/v608build/round2/staged/nancys-adventure-english-v6-08-PASTE.md', '1B': '/workspace/v608build/round2/trim-1B/staged/nancys-adventure-english-v6-08-PASTE.md'}
STAGED = {t: LIMIT - len(open(p, encoding='utf-8').read()) for t, p in _SP.items()}   # real staged sizes
assert all(STAGED[t] == bank(t) for t in STAGED), (STAGED, {t: bank(t) for t in STAGED})
SAVES = [('night title B', 60, True), ('B1 B', 11, True), ('night title B + B1 B', 71, True), ('drop the ramp', 40, False)]   # self-chosen savings: (label, chars saved, ramp kept)
CHOICES = [(a, sv, STAGED['1A'] - ASK[a] - (RAMP if keep else 0) + (c if keep else 0)) for a in ASK for sv, c, keep in SAVES]   # both trims bank the same
BUDGET = ('Trim costs %d on both paths, so 1A and 1B both bank %d (the verse scroll is a fix, already counted). '
          'State pairs + ramp (%d) is over by %d; letter game + ramp (%d) is over by %d. Savings Maxwell could choose: night title B -60, B1 B -11, dropping the ramp -40.'
          % (TRIM['1A'], STAGED['1A'], ASK['state pairs'] + RAMP, ASK['state pairs'] + RAMP - STAGED['1A'], ASK['letter game'] + RAMP, ASK['letter game'] + RAMP - STAGED['1A']))
LEFTS = [c[2] for c in COMBOS]   # as listed, before any self-chosen saving
ROUNDS = {
 'R0': dict(name='R0 bug fixes (taken)', picks=', '.join(f'{n} {c}' for n, c in FIXES), lo=754 - BANK, hi=754 - BANK, before={'post-HOLD bank': 754}),
 'R1': dict(name='R1 ceiling trim (Maxwell t444u, QM-relayed)', picks='1A all rooms, never over a target +89 or 1B front desk and kitchen +89', lo=89, hi=89, before={'bank': BANK}),
 'R2': dict(name="R2 Maxwell's asks + ramp (t428u-t432u, QM-relayed)", picks='letter game lean 413 or state pairs lean 367, each + D2 B ramp 40; full: letter game 523, state pairs 885, ramps D2 C 63 + D1 C 128',
            lo=407, hi=523 + 885 + 191, hione=885 + 191, before={'1A': bank('1A'), '1B': bank('1B')}),
 'R3': dict(name='R3 open picks (coin, TG1-TG4, Echo recap, Bloodtide, B1, night title)', picks='coin B 80, TG2 B 60, TG3 B 55, TG1 B+C 54, TG4 B 35, Echo recap 22, Bloodtide +2; B1 B -11 and night title B -60 only save',
            lo=-71, hi=308, before={'most left after R2': max(LEFTS)}),
 'R4': dict(name='R4 extras (Watchman, Instructor)', picks='mirror 146, milk + eggs 418, clinic room 352 / ~724 / ~1,743, market counter 300 / ~672 / ~2,300',
            lo=146, hi=146 + 418 + 1743 + 2300, before={'most left after R2': max(LEFTS)}),
}
def line(r):
    R = ROUNDS[r]; b = R['before']; worst = R['hi']; over = [k for k, v in b.items() if worst > v]
    if r in ('R3', 'R4'):   # r2d (Auditor r2c L1): no '-4 left'; say what R2 leaves, from over by 4 (state pairs + ramp) to 36 left (state pairs, no ramp)
        lo_l, hi_l = max(LEFTS), max(l for a, sv, l in CHOICES if sv == 'drop the ramp'); hi_lab = [f'{a}, no ramp' for a, sv, l in CHOICES if l == hi_l and sv == 'drop the ramp'][0]   # R3's own savings (night title B, B1 B) are R3 picks, so not counted here
        aft = (f'over by {-lo_l}' if lo_l < 0 else f'{lo_l} left') + ' (state pairs + ramp) to ' + f'{hi_l} left ({hi_lab})'
        al = 'all together ' if r == 'R3' else ''
        return (f"Round total ({R['name']}): picks combined {fmt(R['lo'])} to {fmt(worst)} chars. After R2: {aft}. "
                f"Worst case {fmt(worst)} {al}fits no R2 path" + ('; a single pick of up to %d chars fits on its own, and up to %d with night title B and B1 B also picked.' % (hi_l, max(c[2] for c in CHOICES)) if r == 'R3' else '.'))
    s = f"Round total ({R['name']}): picks combined {fmt(R['lo']) + ' to ' + fmt(worst) if R['lo'] != worst else fmt(worst)} chars against " + ', '.join(f'{k} {fmt(v)}' for k, v in b.items()) + f" left. Worst case {fmt(worst)}"
    if 'hione' in R: s += f" (both asks full; one ask full at most {fmt(R['hione'])})"
    s += ': ' + (('OVERRUN, short by ' + ', '.join(f'{fmt(worst - b[k])} ({k})' for k in over)) if over else 'fits on every path') + '.'
    if R['lo'] > max(b.values()): s += f" Even the cheapest pick ({fmt(R['lo'])}) overruns every path" + (' with the ramp.' if r == 'R2' else '.')
    return s
SHEET_ROUND = {'walk24': 'R0', 'trim-pick': 'R1', 'front-desk-t444u': 'R1', 'home-lake-trim': 'R1', 'pick-combined': None,
 'letter-game-A-B': 'R2', 'state-pairs-lean': 'R2', 'D1-sentence': 'R2', 'D2-listen': 'R2',
 'TG1-': 'R3', 'TG2-': 'R3', 'TG3-': 'R3', 'TG4-': 'R3', 'coin-rule': 'R3', 'bloodtide-name': 'R3', 'B1-reward': 'R3', 'night-title': 'R3', 'showcase-': None, 'jesus-words-26': None}
import os as _os
def snap_line():   # r2d (Auditor r2c H5): every sheet footer names the frozen snapshot it ships in (NAE_SNAP, set by the freeze script)
    s = _os.environ.get('NAE_SNAP'); return f' Frozen in v608build/{s}.' if s else ''
def for_sheet(out):
    b = out.split('/')[-1]
    for k, r in SHEET_ROUND.items():
        if b.startswith(k): return ((line(r) + ' ') if r else '') + BUDGET + snap_line()
    return snap_line().strip()
if __name__ == '__main__':
    for r in ROUNDS: print(line(r))
    print(BUDGET)
    for c in COMBOS: print(c, verdict(c[2]))
    for c in CHOICES: print(c, verdict(c[2]))
