import pypokedex
pokemonTypes = pypokedex.get(dex=655)


multipleTypes = ''
for type in pokemonTypes.types:
    multipleTypes = multipleTypes + type + '\t'

print(multipleTypes)