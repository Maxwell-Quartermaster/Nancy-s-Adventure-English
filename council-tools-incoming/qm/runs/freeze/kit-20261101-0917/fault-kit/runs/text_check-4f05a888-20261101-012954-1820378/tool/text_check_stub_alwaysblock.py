# BROKEN ON PURPOSE (fault-kit self-test): text_check stub that blocks everything (over-blocking must fail too).
import sys
print('text-check stub0001 (broken stub)')
for p in sys.argv[1:]: print(f'BLOCK           {p}  (1 problems, 0 warnings)\n    BLOCK   stub blocks all')
print('RESULT BLOCK'); sys.exit(1)
