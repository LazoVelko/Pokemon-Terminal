import os
import numpy as np
from PIL import Image

# folderPath = '/home/mark/Adams_Dev_Test/Pokemon-Terminal/pokemonterminal/Images/HQ_Images/'
folderPath = '/home/adam/Pokemon_Images/Pokemon/assets/HQ_Images/'

def pokemonImageBrightnessFinder(imageInput, fileName):
    fileInput = (imageInput + fileName)
    # fileOutput = (imageOutput + fileName)

    pkmnImg = Image.open(fileInput)
    pkmnImgRGBA = pkmnImg.convert('LA')
    pkmnImgData = pkmnImgRGBA.getdata()

        # Obsolete script, doesn't work how I want it to,
        # causes image artifacting on PNGs, which taints
        # the average brightness of the Pokémon.

    # pkmnImg = Image.open(fileInput)
    # pkmnImgGray = pkmnImg.convert('L')
    # pkmnImgGray.save(fileOutput)

    # pkmnImgGrayNew = Image.open(fileOutput)
    # pkmnImgRGBA = pkmnImgGrayNew.convert('RGBA')
    # pkmnImgData = pkmnImgRGBA.getdata()

    meanBrightness = []
    meanBrightnessList = []
    
    for pixelValue in pkmnImgData:
        if pixelValue[1] == 0:
            continue
        else:
            meanBrightnessList.append(int(sum(pixelValue[:1])))

    meanBrightness = round((int(sum(meanBrightnessList)) / int(len(meanBrightnessList)) / 255), 3)
    print(meanBrightness)

# for pkmnID in os.listdir(folderPath):
#     if pkmnID.endswith('.png'):
#         pokemonImageBrightnessFinder(folderPath, grayFolderPath, '0014_Kakuna.png')

pokemonImageBrightnessFinder(folderPath, '1032_Gecqua.png')

