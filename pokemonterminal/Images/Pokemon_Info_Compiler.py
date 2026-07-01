import os
import Pokemon_Image_Brightness_Finder as imageBrightness
import pypokedex

folderPath = '/home/mark/Adams_Dev_Test/Pokemon-Terminal/pokemonterminal/Images/HQ_Images/'
# folderPath = '/home/adam/Pokemon_Images/Pokemon/assets/HQ_Images/'

list = os.listdir(folderPath)
list.sort()

open('/home/mark/Adams_Dev_Test/Pokemon_Compiled_Info_Temp.txt', 'w').close()
open('/home/mark/Adams_Dev_Test/Pokemon_Compiled_Info_Log_Temp.txt', 'w').close()
# open('/home/adam/Pokemon_Images/Pokemon_Compiled_Info_Temp.txt', 'w').close()
# open('/home/adam/Pokemon_Images/Pokemon_Compiled_Info_Log_Temp.txt', 'w').close()

pkmnTypeVariants = open('/home/mark/Adams_Dev_Test/Pokemon_Mega_And_Regional_Type_Variations.py').read().split()
pkmnNameLog = open('/home/mark/Adams_Dev_Test/Pokemon_Compiled_Info_Log.txt').read().split()
# pkmnTypeVariants = open('/home/adam/Pokemon_Images/Adams_Tests/Pokemon_Mega_And_Regional_Type_Variations.py').read().split()
# pkmnNameLog = open('/home/adam/Pokemon_Images/Pokemon_Compiled_Info_Log.txt').read().split()

testCount = 0

for fileName in list:
    # if fileName in pkmnNameLog:
    #     continue
    if fileName in pkmnTypeVariants:
        testCount = testCount + 1
        print(testCount)
        print(fileName)
        with open('/home/mark/Adams_Dev_Test/Pokemon_Compiled_Info_Temp.txt', 'a') as amendCompiledCsv:
        # with open('/home/adam/Pokemon_Images/Pokemon_Compiled_Info_Temp.txt', 'a') as compiledCsv:
        amendCompiledCsv.write(str(pokemonDexNoFixed) + '\t' + pokemonName.title() + '\t' + str(imageBrightness.pokemonImageBrightnessFinder(folderPath, fileName)) + multipleTypes.title() + '\n')
        continue
    else:
        pokemonDexNo = fileName[:4]
        pokemonDexNo = int(pokemonDexNo)
        pokemonDexNoFixed = ("{:04d}".format(pokemonDexNo))
        pokemonName = fileName[5:-4]
        pokemonVariable = pypokedex.get(dex=pokemonDexNo)
        # pokemonTypes = ['Fire', 'Psychic']
        multipleTypes = ''

    for pokeType in pokemonVariable.types:
        multipleTypes = multipleTypes + '\t' + pokeType
    with open('/home/mark/Adams_Dev_Test/Pokemon_Compiled_Info_Temp.txt', 'a') as compiledCsv:
    # with open('/home/adam/Pokemon_Images/Pokemon_Compiled_Info_Temp.txt', 'a') as compiledCsv:
        compiledCsv.write(str(pokemonDexNoFixed) + '\t' + pokemonName.title() + '\t' + str(imageBrightness.pokemonImageBrightnessFinder(folderPath, fileName)) + multipleTypes.title() + '\n')
    with open('/home/mark/Adams_Dev_Test/Pokemon_Compiled_Info_Log_Temp.txt', 'a') as infoLog:
    # with open('/home/adam/Pokemon_Images/Pokemon_Compiled_Info_Log_Temp.txt', 'a') as infoLog:
        infoLog.write(fileName + '\n')
