import cv2
import os

def pokemonImageBrightnessFinder(fileName):
    image = cv2.imread('/home/mark/Adams_Dev_Test/Pokemon-Terminal/pokemonterminal/Images/HQ_Images/' + fileName)
    # image = cv2.imread('/home/adam/Pokemon_Images/Generation VI - Kalos/0655Delphox.png')
    grayscaleImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    meanBrightness = grayscaleImage.mean()
    meanBrightness = meanBrightness / 255
    meanBrightness = round(meanBrightness, 3) 
    print(meanBrightness)

for fileName in os.listdir('/home/mark/Adams_Dev_Test/Pokemon-Terminal/pokemonterminal/Images/HQ_Images'):
# for fileName in os.listdir('/home/adam/Pokemon_Images/Generation VI - Kalos'):
    if fileName.endswith('.png'):
        pokemonImageBrightnessFinder(fileName)
