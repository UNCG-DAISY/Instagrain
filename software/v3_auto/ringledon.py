# Import the necessary libraries
import board
import neopixel

# Define the NeoPixel object with the appropriate parameters
pixels = neopixel.NeoPixel(board.D18, 24)

# Fill the NeoPixel object with a particular color
pixels.fill((255,255,126))

# for x in range(0, 24):
#     pixels[x] = (126, 126, 126)

    

