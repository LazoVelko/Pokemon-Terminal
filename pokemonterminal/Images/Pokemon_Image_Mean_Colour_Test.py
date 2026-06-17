import cv2
import os
import numpy as np

# folderPath = '/home/mark/Documents/Adams_Dev_Test/Pokemon-Terminal/pokemonterminal/Images/Test'
folderPath = '/home/adam/Pokemon_Images/Pokemon/assets/HQ_Images/'

list = os.listdir(folderPath)
list.sort()

def pokemonImageBrightnessFinder(fileName):
    pokemonDexNo = fileName[:4]
    pkmnImage = cv2.imread(folderPath + fileName)   
    averageColourRow = np.average(pkmnImage, axis=0)
    averageColour= np.average(averageColourRow, axis=0)
    averageRedColourValue = averageColour[:1]
    averageGreenColourValue = averageColour[1:2]
    averageBlueColourValue = averageColour[2:]
    
    averageRedColourValue = round(averageRedColourValue, 3)
    averageGreenColourValue = round(averageGreenColourValue, 3)
    averageBlueColourValue = round(averageBlueColourValue, 3)

    print(pokemonDexNo)
    print(averageRedColourValue)
    print(averageGreenColourValue)
    print(averageBlueColourValue)
    

# pokemonImageBrightnessFinder('1032_Gecqua.png')


for pkmnID in list:
    if pkmnID.endswith('.png'):
        pokemonImageBrightnessFinder(pkmnID)
