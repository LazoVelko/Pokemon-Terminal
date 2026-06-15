import cv2
import os

folderPath = '/home/mark/Adams_Dev_Test/Pokemon-Terminal/pokemonterminal/Images/HQ_Images'
# folderPath = '/home/adam/Pokemon_Images/Pokemon/assets/imagesHQ/'

def pokemonImageBrightnessFinder(fileName):
    image = cv2.imread(folderPath + fileName)   
    grayscaleImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    meanBrightness = grayscaleImage.mean()
    meanBrightness = meanBrightness / 255
    meanBrightness = round(meanBrightness, 3)
    print (meanBrightness)

pokemonImageBrightnessFinder('0655')
# for fileName in os.listdir('/home/mark/Adams_Dev_Test/Pokemon-Terminal/pokemonterminal/Images/HQ_Images'):
for imageNameInput in os.listdir(folderPath):
    if imageNameInput.endswith('.png'):
        pokemonImageBrightnessFinder(imageNameInput)
