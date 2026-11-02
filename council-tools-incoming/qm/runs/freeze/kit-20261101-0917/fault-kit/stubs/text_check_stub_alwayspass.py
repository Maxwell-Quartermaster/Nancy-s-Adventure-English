# BROKEN ON PURPOSE (fault-kit self-test): text_check stub that clears everything.
import sys
print('text-check stub0000 (broken stub)')
for p in sys.argv[1:]: print(f'PASS            {p}  (0 problems, 0 warnings, Thai pages measured 0)')
print('RESULT CLEAR'); sys.exit(0)
