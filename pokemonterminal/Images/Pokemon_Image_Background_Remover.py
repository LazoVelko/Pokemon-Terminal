import os
import cv2
import numpy as np
from PIL import Image

# folderPath = '/home/mark/Adams_Dev_Test/Pokemon-Terminal/pokemonterminal/Images/HQ_Images/'
folderPath = '/home/adam/Pokemon_Images/Pokemon/assets/HQ_Images/'
newFolderPath = '/home/adam/Pokemon_Images/Pokemon/assets/HQ_Images_Edited/'

def pokemonImageBackgroundRemover(imgID, newImageID):
    pkmnImg = Image.open(imgID)
    pkmnImgRGBA = pkmnImg.convert('RGBA')
    pkmnImgData = pkmnImgRGBA.getdata()
    newPkmnImgData = []

    for uneditedPNG in pkmnImgData:
        if uneditedPNG[3] == 0:
            newPkmnImgData.append((0, 0, 0, 0))
        elif 0 <= uneditedPNG[3] <= 254:
            newPkmnImgData.append((0, 0, 0, 255))
        else:
            newPkmnImgData.append(uneditedPNG)
            
    pkmnImgRGBA.putdata(newPkmnImgData)
    pkmnImgRGBA.save(newImageID)

for fileName in os.listdir(folderPath):
    if fileName.endswith('.png'):
        imagePath = folderPath + fileName
        newImagePath = newFolderPath + fileName
        pokemonImageBackgroundRemover(imagePath, newImagePath)
