import cv2
import os

def pokemonImageBrightnessFinder(fileName):
    # image = cv2.imread('/home/adam/Pokemon_Images/Generation VI - Kalos/0655Delphox.png')
    image = cv2.imread('/home/mark/Documents/Adams_Dev_Test/Pokemon-Terminal/pokemonterminal/Images/Generation VI - Kalos/' + fileName)
    grayscaleImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    meanBrightness = grayscaleImage.mean()
    meanBrightness = meanBrightness / 255
    meanBrightness = round(meanBrightness, 3) 
    print(meanBrightness)

# for fileName in os.listdir('/home/adam/Pokemon_Images/Generation VI - Kalos'):
for fileName in os.listdir('/home/mark/Documents/Adams_Dev_Test/Pokemon-Terminal/pokemonterminal/Images/Generation VI - Kalos'):
    if fileName.endswith('.jpg'):
        pokemonImageBrightnessFinder(fileName)
