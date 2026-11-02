R = "/workspace/council-tools/text-check/runs/selftest-v5zn5j69/renders/png/"
from PIL import Image
S = Image.new('RGB', (9, 9))
d = None
# d.text((0, 0), 'Pick one: the golden pantry tile')
cap = 'Option A shows the shop'
im = Image.open(R + 'r1.png')
S.save("/nonexistent/built.png")
