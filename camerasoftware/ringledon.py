import board
import neopixel
pixels = neopixel.NeoPixel(board.D18, 24)

for x in range(0, 24):
    pixels[x] = (126, 126, 126)

    

