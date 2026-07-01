import Pokemon_Image_Brightness_Finder as imageBrightness

class pkmnVariables:
    def __init__(self, dexNo, name, brightnessValue, types):
        self.dexNo = dexNo
        self.name = name
        self.brightnessValue = brightnessValue
        self.types = types

dexNoStr = "655"
dexNoInt = int(dexNoStr)-1
# namesTxt = open('/home/mark/Documents/Adams_Dev_Test/Pokemon-Terminal/pokemonterminal/Data/pokemon.txt').readlines()
namesTxt = open('/home/adam/Pokemon_Images/pokemon.txt').readlines()
chosenLine = namesTxt[dexNoInt]
print(pkmnVariables)
pkmnDexNo = dexNoStr
pkmnName = chosenLine.split()[0]
pkmnBrightnessValue = 'imageBrightness.pokemonImageBrightnessFinder(fileName)'
pkmnTypes = chosenLine.split()[2:]
p1 = pkmnVariables(pkmnDexNo, pkmnName, pkmnBrightnessValue, pkmnTypes)

print(p1.dexNo)
print(p1.name)
print(p1.brightnessValue)
for multipleTypes in p1.types:
    print(multipleTypes)




# class pkmnTypes:
#     pkmnTypes = ("Normal", "Grass", "Fire", "Water", "Electric", "Ice", "Fighting", "Poison", "Ground", "Flying", "Psychic", "Bug", "Rock", "Ghost", "Dragon", "Dark", "Steel", "Fairy")
