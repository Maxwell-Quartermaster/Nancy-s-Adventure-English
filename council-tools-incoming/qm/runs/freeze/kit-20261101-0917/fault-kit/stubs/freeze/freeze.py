# BROKEN ON PURPOSE (fault-kit self-test): freeze stub that says "frozen" and does nothing (never seeds its sandbox).
import sys
print('stub freeze: FROZEN (did nothing)'); sys.exit(0)
