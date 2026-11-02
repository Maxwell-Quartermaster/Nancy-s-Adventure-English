# Round totals for every pick round (Chancellor, 8:20 PM MDT): what a round's picks cost combined against what is left, the worst case, and an overrun flag.
# One table, read by the ledger and by every pick sheet's footer, so the numbers never drift.
BANK = 584   # post-HOLD 754 minus the bug fixes: sky B 79, 16 pt edges 41, guardian chip 50 (Maxwell t445u, QM-relayed)
TRIM = {'1A': 68, '1B': 93}
ASK = {'LG': 413 + 40, 'SP': 367 + 40}   # lean ask + listen ramp (D2 B)
PATHS = [('1A + letter game', '1A', 'LG'), ('1A + state pairs', '1A', 'SP'), ('1B + letter game', '1B', 'LG'), ('1B + state pairs', '1B', 'SP')]
LEFT = {p: BANK - TRIM[t] - ASK[a] for p, t, a in PATHS}   # 63, 109, 38, 84
ROUNDS = {
 'R0': dict(name='R0 round2b bug fixes (taken)', picks='sky B 79, 16 pt edges 41, guardian chip 50 (Maxwell t445u, QM-relayed)', lo=170, hi=170, before={'post-HOLD bank': 754}),
 'R1': dict(name='R1 ceiling trim (t444u)', picks='1A all rooms +68 or 1B front desk and night table +93', lo=68, hi=93, before={'all paths': BANK}),
 'R2': dict(name="R2 Maxwell's asks + ramps (t428u-t432u; D1, D2)", picks='letter game lean 413 or state pairs lean 367, each + D2 B ramp 40; full: letter game 523, state pairs 885, ramps D2 C 63 + D1 C 128',
            lo=407, hi=523 + 885 + 191, hione=885 + 191, before={'1A': BANK - 68, '1B': BANK - 93}),
 'R3': dict(name='R3 open picks (coin, TG1-TG4, Echo recap, Bloodtide, B1, night title)', picks='coin B 80, TG2 B 60, TG3 B 55, TG1 B+C 54, TG4 B 35, Echo recap 22, Bloodtide +2; B1 B -11 and night title B -60 only save',
            lo=-71, hi=308, before=LEFT),
 'R4': dict(name='R4 extras (Watchman, Instructor)', picks='mirror 146, milk + eggs 418, clinic room 352 / ~724 / ~1,743, market counter 300 / ~672 / ~2,300',
            lo=146, hi=146 + 418 + 1743 + 2300, before=LEFT),
}
def fmt(n): return format(n, ',')
def line(r):
    R = ROUNDS[r]; b = R['before']
    lefts = ', '.join(f'{k} {fmt(v)}' for k, v in b.items())
    worst = R['hi']; over = [k for k, v in b.items() if worst > v]
    s = f"Round total ({R['name']}): picks combined {fmt(R['lo']) + ' to ' + fmt(worst) if R['lo'] != worst else fmt(worst)} chars against {lefts} left. Worst case {fmt(worst)}"
    if 'hione' in R: s += f" (both asks full; one ask full at most {fmt(R['hione'])})"
    s += ': ' + (('OVERRUN, short by ' + ', '.join(f'{fmt(worst - b[k])} ({k})' for k in over)) if over else 'fits on every path') + '.'
    if R['lo'] > max(b.values()): s += f" Even the cheapest pick ({fmt(R['lo'])}) overruns every path."
    return s
if __name__ == '__main__':
    for r in ROUNDS: print(line(r))

SHEET_ROUND = {'sky-A-vs-B': 'R0', 'walk24': 'R0', 'trim-pick': 'R1', 'front-desk-t444u': 'R1', 'home-lake-trim': 'R1',
 'letter-game-A-B': 'R2', 'state-pairs-lean': 'R2', 'D1-sentence': 'R2', 'D2-listen': 'R2',
 'TG1-': 'R3', 'TG2-': 'R3', 'TG3-': 'R3', 'TG4-': 'R3', 'coin-rule': 'R3', 'bloodtide-name': 'R3', 'B1-reward': 'R3', 'night-title': 'R3', 'clinic-idea': 'R4'}
def for_sheet(out):
    b = out.split('/')[-1]
    for k, r in SHEET_ROUND.items():
        if b.startswith(k): return line(r)
    return ''
