import os
import cv2
import numpy as np
from PIL import Image

# folderPath = '/home/mark/Adams_Dev_Test/Pokemon-Terminal/pokemonterminal/Images/HQ_Images/'
folderPath = '/home/adam/Pokemon_Images/Pokemon/assets/HQ_Images/'
fileID = '0655_Delphox-Mega.png'


# list = os.listdir(folderPath)
# list.sort()

# def pokemonImageMeanColourFinder(fileID):
#     pokemonDexNo = fileID[:4]
#     pkmnImage = cv2.imread(f'imgs/{folderPath + fileID}')
    


#     averageColourRow = np.average(pkmnImage, axis=0)
#     averageColour= np.average(averageColourRow, axis=0)


#     averageRedColourValue = int(averageColour[0])
#     averageGreenColourValue = int(averageColour[1])
#     averageBlueColourValue = int(averageColour[2])


#     print(pokemonDexNo)
#     print(averageRedColourValue)
#     print(averageGreenColourValue)
#     print(averageBlueColourValue)
    

# for fileName in os.listdir(folderPath):
#     if fileName.endswith('.png'):
#         pokemonImageMeanColourFinder(fileName)


pkmnImage = Image.open('/home/adam/Pokemon_Images/Pokemon/assets/HQ_Images/0655_Delphox-Mega.png')

pixels = pkmnImage.load()
width, height = pkmnImage.size

for x in range(width):
    for y in range(height):
            r, g, b, a = pixels[x, y]

print(r)


# print(pkmnImage.shape)

# https://pytutorial.com/python-get-image-pixels-guide/
