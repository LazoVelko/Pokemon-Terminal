import cv2
import os

# folderPath = '/home/mark/Documents/Adams_Dev_Test/Pokemon-Terminal/pokemonterminal/Images/Test'
folderPath = '/home/adam/Pokemon_Images/Pokemon/assets/HQ_Images/'

def pokemonImageBrightnessFinder(fileName):
    # image = cv2.imread('/home/mark/Adams_Dev_Test/Pokemon-Terminal/pokemonterminal/Images/HQ_Images/' + fileName)
    image = cv2.imread(folderPath + fileName)   
    grayscaleImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    meanBrightness = grayscaleImage.mean()
    meanBrightness = meanBrightness / 255
    meanBrightness = round(meanBrightness, 3)
    return meanBrightness
    # print(meanBrightness)

# pokemonImageBrightnessFinder('1032_Gecqua.png')

# for pkmnID in os.listdir(folderPath):
#     if pkmnID.endswith('.png'):
#         pokemonImageBrightnessFinder(pkmnID)