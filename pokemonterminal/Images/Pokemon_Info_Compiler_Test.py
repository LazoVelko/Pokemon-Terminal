import Pokemon_Image_Brightness_Finder as imBrightness

# def pokemonInfoCompiler(filePath):

# dexNoStr = filePath[:4]
# dexNoInt = int(dexNoStr)-1
dexNoStr = ('0655')
dexNoInt = int(dexNoStr)-1
# referenceTxt = open('/home/mark/Adams_Dev_Test/Pokemon_Reference_Copy.txt').readlines()
referenceTxt = open('/home/adam/Pokemon_Images/pokemon.txt').readlines()
# open('/home/mark/Adams_Dev_Test/Pokemon_Compilation_Test', 'w').close()
open('/home/adam/Pokemon_Images/Pokemon_Compilation_Test', 'w').close()

chosenLineInput = referenceTxt[dexNoInt]


pokemonDexNo = int(dexNoStr)
pokemonDexNoFixed = ("{:04d}".format(pokemonDexNo))
pokemonName = chosenLineInput.split()[0]
pokemonBrightness = chosenLineInput.split()[1]
pokemonTypes = chosenLineInput.split()[2:]

multipleTypes = ''
for type in pokemonTypes:
    multipleTypes = multipleTypes + type + '\t'


# with open('/home/mark/Adams_Dev_Test/Pokemon_Compilation_Test', 'a') as compiledTxt:
with open('/home/adam/Pokemon_Images/Pokemon_Compilation_Test', 'a') as compiledTxt:
    compiledTxt.write(pokemonDexNoFixed + '\t' + pokemonName.capitalize() + '\t' + str(imBrightness.pokemonImageBrightnessFinder('0655Delphox.png')) + '\t' + multipleTypes.capitalize() + '\n')

print(pokemonDexNoFixed)
print(pokemonName)
print(imBrightness.pokemonImageBrightnessFinder('0655Delphox.png'))
for multipleTypes in pokemonTypes:
    print(multipleTypes)