# BROKEN ON PURPOSE (fault-kit self-test): quote_check stub that flags every kind on every post.
import sys
for k in ('UNSOURCED', 'TRUNCATED', 'RELAY'): print(f'FLAG {k} 1: stub')
sys.exit(1)
