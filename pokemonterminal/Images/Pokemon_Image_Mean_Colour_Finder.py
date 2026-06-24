import os
import cv2
import numpy as np
from PIL import Image

folderPath = '/home/mark/Adams_Dev_Test/Pokemon-Terminal/pokemonterminal/Images/HQ_Images/'
# folderPath = '/home/adam/Pokemon_Images/Pokemon/assets/HQ_Images/'

def pokemonImageBackgroundRemover(imgID):
    pkmnImg = Image.open(imgID)
    pkmnImgRGBA = pkmnImg.convert('RGBA')
    pkmnImgData = pkmnImgRGBA.getdata()

    redValueList = []
    greenValueList = []
    blueValueList = []
    alphaValueList = []

    for pixelValue in pkmnImgData:
        if pixelValue[3] == 0:
            continue
        else:
            redValueList.append(pixelValue[0])
            greenValueList.append(pixelValue[1])
            blueValueList.append(pixelValue[2])
            alphaValueList.append(pixelValue[3])

    redValueListMean = int(sum(redValueList)) / int(len(redValueList))

    greenValueListMean = int(sum(greenValueList)) / int(len(greenValueList))

    blueValueListMean = int(sum(blueValueList)) / int(len(blueValueList))

    alphaValueListMean = int(sum(alphaValueList)) / int(len(alphaValueList))

    print(int(redValueListMean))
    print(int(greenValueListMean))
    print(int(blueValueListMean))
    print(int(alphaValueListMean))

pokemonImageBackgroundRemover('/home/mark/Adams_Dev_Test/Pokemon-Terminal/pokemonterminal/Images/HQ_Images/0014_Kakuna.png')

