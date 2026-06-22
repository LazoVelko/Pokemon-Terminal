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
    rows,cols,_ = pkmnImage.shape
    for i in range(rows):
        for j in range(cols):
            k = pkmnImage[i,j]
            print(k)

    # averageColourRow = np.average(pkmnImage, axis=0)
    # averageColour= np.average(averageColourRow, axis=0)
    # averageRedColourValue = int(averageColour[0])
    # averageGreenColourValue = int(averageColour[1])
    # averageBlueColourValue = int(averageColour[2])
    
    # # print(pokemonDexNo)
    # # print(averageRedColourValue)
    # # print(averageGreenColourValue)
    # # print(averageBlueColourValue)
    
    # print(pokemonDexNo)

    # print (averageRedColourValue, averageGreenColourValue, averageBlueColourValue)
    
    

pokemonImageMeanColourFinder('0011_Metapod.png')

# for pkmnID in list:
#     if pkmnID.endswith('.png'):
#         pokemonImageBrightnessFinder(pkmnID)




