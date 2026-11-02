from PIL import Image
S = Image.new('RGB', (9, 9))
cap = 'Back after a pause'
S.save('/nonexistent/two-a.png')
T = Image.new('RGB', (9, 9))
cap2 = 'Game over screen'
T.save('/nonexistent/two-b.png')
