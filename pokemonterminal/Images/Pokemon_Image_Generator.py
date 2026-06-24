# pip install --upgrade pillow

import cv2
import Pokemon_Image_Mean_Colour_Finder as pkmnRGB

from PIL import Image

width = 1366
height = 768

# red, green, blue = [173, 106, 75]
# red, green, blue = [129, 76, 67]
red, green, blue = [189, 168, 86]

# redValue = pkmnRGB.averageRedColourValue
# greenValue = pkmnRGB.averageGreenColourValue
# blueValue = pkmnRGB.averageBlueColourValue

# pkmnRGB.pokemonImageMeanColourFinder(fileName)
# print(pkmnRGB.pokemonImageMeanColourFinder(fileName))

img = Image.new(mode = "RGB", size = (width, height), color = (red, green, blue))
img.show()
