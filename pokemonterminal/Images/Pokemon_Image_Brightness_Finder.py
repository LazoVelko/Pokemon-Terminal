import os
import cv2
import numpy as np
from PIL import Image
from PIL import ImageFilter

# folderPath = '/home/mark/Documents/Adams_Dev_Test/Pokemon-Terminal/pokemonterminal/Images/Test'
folderPath = '/home/adam/Pokemon_Images/Pokemon/assets/'

def pokemonImageBrightnessFinder(fileName):
    pkmnImg = Image.open(fileName)
    pkmnImgGray = pkmnImg.convert('L')
    pkmnImgData = pkmnImgGray.getdata()

    meanBrightness = []
    
    for pixelValue in pkmnImgData:
        if pixelValue[3] == 0:
            continue
        else:
            meanBrightness = int(sum(pixelValue)) / int(len(pixelValue))
            print(meanBrightness)


testVal = (folderPath + 'Test.png')
pokemonImageBrightnessFinder(testVal)

# for pkmnID in os.listdir(folderPath):
#     if pkmnID.endswith('.png'):
#         pokemonImageBrightnessFinder(pkmnID)

# https://pythonexamples.org/pillow-convert-image-to-grayscale/
