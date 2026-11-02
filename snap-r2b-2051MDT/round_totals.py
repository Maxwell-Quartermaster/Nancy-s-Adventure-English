# Round totals for every pick round (Chancellor 8:20 PM MDT; Auditor eb2674be and Council 8:43 PM MDT sizes). One table, read by the ledger,
# the combined pick sheet and every pick sheet footer, so the numbers never drift. Sizes from the staged PASTEs (1A 187,776 / 1B 187,797).
LIMIT = 188200; P1748 = 187208
FIXES = [('sky B', 79), ('16 pt edges', 41), ('guardian chip (Maxwell t445u, QM-relayed)', 50), ('walk scene shrinks below the banner (eb2674be H2)', 38), ('sw-19 three (eb2674be H1)', 2)]
BANK = 754 - sum(c for _, c in FIXES)   # 544 before the trim and verse picks
TRIM = {'1A': 68, '1B': 89}            # 1B: "front desk and kitchen" (eb2674be H3, -4)
VERSE = {'A': 52, 'B': 0}              # A: scroll in its card (+52, staged in both PASTEs); B: shorter verses (0 chars)
ASK = {'letter game': 413, 'state pairs': 367}; RAMP = 40
VLAB = {'A': 'scroll in its card, all 30 verses kept, +52', 'B': "swap the long verses for shorter ones, 0 chars, some peace verses replaced, needs a new Thai check and Nancy's sign-off"}
def bank(t, v): return BANK - TRIM[t] - VERSE[v]                     # 1A/A 424, 1A/B 476, 1B/A 403, 1B/B 455
def left(t, v, a): return bank(t, v) - ASK[a] - RAMP
COMBOS = [(t, v, a, left(t, v, a)) for t in TRIM for v in VERSE for a in ASK]
def fmt(n): return format(n, ',')
def verdict(n): return 'fits (%s left)' % fmt(n) if n >= 0 else 'over by %s' % fmt(-n)
STAGED = {'1A': bank('1A', 'A'), '1B': bank('1B', 'A')}
BUDGET = ('Only one lean ask fits beside the ramp: %d vs %d (1A) / %d (1B) with the verse scroll staged (%d / %d without it); '
          'with the scroll, letter game + ramp (453) fits neither trim and state pairs + ramp (407) fits 1A only.'
          % (ASK['letter game'] + ASK['state pairs'] + RAMP, STAGED['1A'], STAGED['1B'], bank('1A', 'B'), bank('1B', 'B')))
LEFTS = [c[3] for c in COMBOS]
ROUNDS = {
 'R0': dict(name='R0 bug fixes (taken)', picks=', '.join(f'{n} {c}' for n, c in FIXES), lo=754 - BANK, hi=754 - BANK, before={'post-HOLD bank': 754}),
 'R1': dict(name='R1 ceiling trim (Maxwell t444u, QM-relayed)', picks='1A all rooms +68 or 1B front desk and kitchen +89', lo=68, hi=89, before={'bank': BANK}),
 'RV': dict(name='RV long verse at 320', picks='A scroll in its card +52 or B shorter verses 0', lo=0, hi=52, before={'1A': BANK - 68, '1B': BANK - 89}),
 'R2': dict(name="R2 Maxwell's asks + ramp (t428u-t432u, QM-relayed)", picks='letter game lean 413 or state pairs lean 367, each + D2 B ramp 40; full: letter game 523, state pairs 885, ramps D2 C 63 + D1 C 128',
            lo=407, hi=523 + 885 + 191, hione=885 + 191, before={'1A/A': bank('1A', 'A'), '1A/B': bank('1A', 'B'), '1B/A': bank('1B', 'A'), '1B/B': bank('1B', 'B')}),
 'R3': dict(name='R3 open picks (coin, TG1-TG4, Echo recap, Bloodtide, B1, night title)', picks='coin B 80, TG2 B 60, TG3 B 55, TG1 B+C 54, TG4 B 35, Echo recap 22, Bloodtide +2; B1 B -11 and night title B -60 only save',
            lo=-71, hi=308, before={'most left after R2': max(LEFTS)}),
 'R4': dict(name='R4 extras (Watchman, Instructor)', picks='mirror 146, milk + eggs 418, clinic room 352 / ~724 / ~1,743, market counter 300 / ~672 / ~2,300',
            lo=146, hi=146 + 418 + 1743 + 2300, before={'most left after R2': max(LEFTS)}),
}
def line(r):
    R = ROUNDS[r]; b = R['before']; worst = R['hi']; over = [k for k, v in b.items() if worst > v]
    s = f"Round total ({R['name']}): picks combined {fmt(R['lo']) + ' to ' + fmt(worst) if R['lo'] != worst else fmt(worst)} chars against " + ', '.join(f'{k} {fmt(v)}' for k, v in b.items()) + f" left. Worst case {fmt(worst)}"
    if 'hione' in R: s += f" (both asks full; one ask full at most {fmt(R['hione'])})"
    s += ': ' + (('OVERRUN, short by ' + ', '.join(f'{fmt(worst - b[k])} ({k})' for k in over)) if over else 'fits on every path') + '.'
    if R['lo'] > max(b.values()): s += f" Even the cheapest pick ({fmt(R['lo'])}) overruns every path."
    return s
SHEET_ROUND = {'walk24': 'R0', 'trim-pick': 'R1', 'front-desk-t444u': 'R1', 'home-lake-trim': 'R1', 'pick-combined': None,
 'letter-game-A-B': 'R2', 'state-pairs-lean': 'R2', 'D1-sentence': 'R2', 'D2-listen': 'R2',
 'TG1-': 'R3', 'TG2-': 'R3', 'TG3-': 'R3', 'TG4-': 'R3', 'coin-rule': 'R3', 'bloodtide-name': 'R3', 'B1-reward': 'R3', 'night-title': 'R3', 'showcase-': None}
def for_sheet(out):
    b = out.split('/')[-1]
    for k, r in SHEET_ROUND.items():
        if b.startswith(k): return ((line(r) + ' ') if r else '') + BUDGET
    return ''
if __name__ == '__main__':
    for r in ROUNDS: print(line(r))
    print(BUDGET)
    for c in COMBOS: print(c, verdict(c[3]))
