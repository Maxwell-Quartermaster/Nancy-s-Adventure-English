# pixdiff.py <dirA> <dirB>: per PNG, count of differing pixels (RGBA exact) and bbox
import sys, os
from PIL import Image, ImageChops
a, b = sys.argv[1], sys.argv[2]; tot = 0; n = 0
for f in sorted(os.listdir(a)):
    A = Image.open(f'{a}/{f}').convert('RGBA'); B = Image.open(f'{b}/{f}').convert('RGBA'); assert A.size == B.size, f
    d = ImageChops.difference(A, B); px = sum(1 for p in d.getdata() if p != (0, 0, 0, 0)); n += 1; tot += px
    print(f, A.size, px, d.getbbox())
print('FILES', n, 'TOTAL_DIFF_PX', tot)
