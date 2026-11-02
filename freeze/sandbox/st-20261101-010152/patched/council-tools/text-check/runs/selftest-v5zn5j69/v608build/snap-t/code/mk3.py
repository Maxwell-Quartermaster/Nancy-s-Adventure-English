from PIL import Image
R = '/x/'
S = Image.new('RGB', (9, 9))
for r in ['a', 'b']: S.paste(Image.open(R + r + '.png'))
S.save("/nonexistent/dyn.png")
