import os

import numpy as np
from PIL import Image


# folderPath = '/home/mark/Adams_Dev_Test/Pokemon-Terminal/pokemonterminal/Images/HQ_Images'
folderPath = '/home/mark/Adams_Dev_Test/Pokemon-Terminal/pokemonterminal/Images/HQ_Images/'
grayFolderPath = '/home/mark/Adams_Dev_Test/Pokemon-Terminal/pokemonterminal/Images/HQ_Images_Gray/'
# folderPath = '/home/adam/Pokemon_Images/Pokemon/assets/HQ_Images/'
# grayFolderPath = '/home/adam/Pokemon_Images/Pokemon/assets/Gray_HQ_Images/'

def pokemonImageBrightnessFinder(imageInput, imageOutput, fileName):
    fileInput = (imageInput + fileName)
    fileOutput = (imageOutput + fileName)

    # pkmnImg = Image.open(fileInput)
    # pkmnImgRGBA = pkmnImg.convert('RGBA')
    # pkmnImgData = pkmnImgRGBA.getdata()

    pkmnImg = Image.open(fileInput)
    pkmnImgGray = pkmnImg.convert('L')
    pkmnImgGray.save(fileOutput)

    pkmnImgGrayNew = Image.open(fileOutput)
    pkmnImgRGBA = pkmnImgGrayNew.convert('RGBA')
    pkmnImgData = pkmnImgRGBA.getdata()

    meanBrightness = []
    
    for pixelValue in pkmnImgData:
        if pixelValue[3] == 0:
            continue
        else:
            meanBrightness = int(sum(pixelValue)) / int(len(pixelValue))
            print(meanBrightness)



for pkmnID in os.listdir(folderPath):
    if pkmnID.endswith('.png'):
        pokemonImageBrightnessFinder(folderPath, grayFolderPath, '0014_Kakuna.png')

# https://pythonexamples.org/pillow-convert-image-to-grayscale/
