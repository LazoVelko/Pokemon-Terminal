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

    redValueListSum = sum(redValueList)
    redValueListLength = len(redValueList)
    redValueListMean = int(redValueListSum) / int(redValueListLength)
    redValueListMean = int(redValueListMean)

    greenValueListSum = sum(greenValueList)
    greenValueListLength = len(greenValueList)
    greenValueListMean = int(greenValueListSum) / int(greenValueListLength)
    greenValueListMean = int(greenValueListMean)

    blueValueListSum = sum(blueValueList)
    blueValueListLength = len(blueValueList)
    blueValueListMean = int(blueValueListSum) / int(blueValueListLength)
    blueValueListMean = int(blueValueListMean)

    alphaValueListSum = sum(alphaValueList)
    alphaValueListLength = len(alphaValueList)
    alphaValueListMean = int(alphaValueListSum) / int(alphaValueListLength)
    alphaValueListMean = int(alphaValueListMean)

    print(redValueListMean)
    print(greenValueListMean)
    print(blueValueListMean)
    print(alphaValueListMean)

pokemonImageBackgroundRemover('/home/mark/Adams_Dev_Test/Pokemon-Terminal/pokemonterminal/Images/HQ_Images/0014_Kakuna.png')

