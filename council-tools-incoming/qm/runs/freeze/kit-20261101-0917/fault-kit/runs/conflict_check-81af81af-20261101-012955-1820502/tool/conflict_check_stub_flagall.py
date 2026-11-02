# BROKEN ON PURPOSE (fault-kit self-test): conflict_check stub that reports every non-blank line as a hit.
import sys
L = open(sys.argv[1], encoding='utf-8').read().split('\n')
for i, l in enumerate(L, 1):
    if l.strip() and i != int(sys.argv[2]): print(f':{i} A-ruling {l[:40]}')
sys.exit(1)
