from PIL import Image
S = Image.new('RGB', (9, 9))
cap = 'Tile 25: The golden pantry.'
S.save("/nonexistent/capsheet.png")
