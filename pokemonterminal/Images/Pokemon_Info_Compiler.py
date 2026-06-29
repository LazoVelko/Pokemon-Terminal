import os
import Pokemon_Image_Brightness_Finder as imageBrightness
import pypokedex

# folderPath = '/home/mark/Adams_Dev_Test/Pokemon-Terminal/pokemonterminal/Images/HQ_Images/'
folderPath = '/home/adam/Pokemon_Images/Pokemon/assets/HQ_Images/'

list = os.listdir(folderPath)
list.sort()
testCount = 0

open ('/home/adam/Pokemon_Images/Pokemon_Compiled_Info_Temp.txt', 'w').close()
open ('/home/adam/Pokemon_Images/Pokemon_Compiled_Info_Log.txt', 'w').close()

for fileName in list:
    if fileName in open('/home/adam/Pokemon_Images/Pokemon_Compiled_Info_Log.txt').readlines():
        continue
    pokemonDexNo = fileName[:4]
    pokemonDexNo = int(pokemonDexNo)
    pokemonDexNoFixed = ("{:04d}".format(pokemonDexNo))
    pokemonName = fileName[5:-4]
    pokemonVariable = pypokedex.get(dex=pokemonDexNo)
    # pokemonTypes = ['Fire', 'Psychic']
    testCount = testCount + 1
    print(testCount)
    multipleTypes = ''

    for pokeType in pokemonVariable.types:
        multipleTypes = multipleTypes + '\t' + pokeType
    # with open('/home/mark/Adams_Dev_Test/Pokemon_Compiled_Info.txt', 'a') as compiledTxt:
    with open('/home/adam/Pokemon_Images/Pokemon_Compiled_Info.txt', 'a') as compiledCsv:
        compiledCsv.write(str(pokemonDexNoFixed) + '\t' + pokemonName.title() + '\t' + str(imageBrightness.pokemonImageBrightnessFinder(folderPath, fileName)) + multipleTypes.title() + '\n')
    with open('/home/adam/Pokemon_Images/Pokemon_Compiled_Info_Log.txt', 'a') as infoLog:
        infoLog.write(fileName + '\n')
