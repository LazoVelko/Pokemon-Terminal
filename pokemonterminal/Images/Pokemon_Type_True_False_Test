class Pkmn:
    def __init__(self, name, types):
        self.name = name
        self.types = types

pkmnTypes = ['normal', 'grass', 'fire', 'water', 'electric', 'ice', 'fighting', 'poison', 'ground', 'flying', 'psychic', 'bug', 'rock', 'ghost', 'dragon', 'dark', 'steel', 'fairy']


venusaur = Pkmn('Venusaur', ['grass', 'poison'])
charmeleon = Pkmn('Charmeleon', ['fire'])
charizard = Pkmn('Charizard', ['fire', 'flying'])
blastoise = Pkmn('Blastoise', ['water'])
tangela = Pkmn('Tangela', ['grass'])
pkmnList = [venusaur, charmeleon, charizard, blastoise, tangela]


def pokemonTypeTest(type):

    for pkmnObj in pkmnList:
        type = type.lower()
        if all([y in pkmnObj.types for y in type]):
            print(pkmnObj.name)


print("Enter a type:")
typeInput = input().split()

if all([x in pkmnTypes for x in typeInput]):
    pokemonTypeTest(typeInput)
else:
    print ('Nuh uh')
