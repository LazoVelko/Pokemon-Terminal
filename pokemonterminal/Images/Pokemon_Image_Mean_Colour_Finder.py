import cv2
import os
import numpy as np

folderPath = '/home/mark/Adams_Dev_Test/Pokemon-Terminal/pokemonterminal/Images/HQ_Images/'
# folderPath = '/home/adam/Pokemon_Images/Pokemon/assets/HQ_Images/'

list = os.listdir(folderPath)
list.sort()

def pokemonImageMeanColourFinder(fileName):
    pokemonDexNo = fileName[:4]
    pkmnImage = cv2.imread(folderPath + fileName)   
    averageColourRow = np.average(pkmnImage, axis=0)
    averageColour= np.average(averageColourRow, axis=0)
    averageRedColourValue = int(averageColour[0])
    averageGreenColourValue = int(averageColour[1])
    averageBlueColourValue = int(averageColour[2])
    
    # print(pokemonDexNo)
    # print(averageRedColourValue)
    # print(averageGreenColourValue)
    # print(averageBlueColourValue)
    
    print(averageColour)

    print (averageRedColourValue, averageGreenColourValue, averageBlueColourValue)
    
    

pokemonImageMeanColourFinder('0014_Kakuna.png')

# for pkmnID in list:
#     if pkmnID.endswith('.png'):
#         pokemonImageBrightnessFinder(pkmnID)

# https://stackoverflow.com/questions/55292321/read-png-image-with-cv2-imread-form-opencv3-in-python3-7-1-and-no-pixel-at-all-w
