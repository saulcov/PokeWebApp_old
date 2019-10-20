## Preprocessing PokeAPI data
#  generates a description for a pokemon given its ID in a certain region
 
import requests

def fetch(url):
    response = requests.get(url)
    return None if response.status_code != 200 else response.json()

class Pokemon:
    pokedex = 'national'
    count = 721

    @classmethod
    def set_region(clc, region):
        clc.pokedex = region
        data = fetch(f'http://pokeapi.co/api/v2/pokedex/{clc.pokedex}')
        clc.count = len(data['pokemon_entries'])

    # Constructor for a pokemon given its National ID
    def __init__(self, id):
        data = fetch(f'http://pokeapi.co/api/v2/pokedex/{Pokemon.pokedex}')
        self.name = data['pokemon_entries'][id-1]['pokemon_species']['name']
        self.url = data['pokemon_entries'][id-1]['pokemon_species']['url']
        self.id = id

    # Creates a description of the pokemon, based on the entries of various pokedex entries
    def describe(self):
        descriptions = frozenset()
        data = fetch(self.url)
        for x in data['flavor_text_entries']:
            toReplace = {'é':'e', '—':'', '-':' ','\xad':''}
            if x['language']['name'] == 'en':
                x['flavor_text'] = x['flavor_text'].lower()
                for a, b in toReplace.items():
                    x['flavor_text'] = x['flavor_text'].replace(a,b)
                x['flavor_text'] = ' '.join(x['flavor_text'].split())
                descriptions |= {x['flavor_text']}
        return ' '.join(descriptions)

## Testing for file
def sample_doc(id):
    Pokemon.set_region('kanto')
    print(f'Pokedex region set to {Pokemon.pokedex.capitalize()}, containing {Pokemon.count} pokemon species.')
    print('\nTHIS IS HOW A POKEMON GENERATED DOCUMENT LOOKS LIKE!')
    print('--------------------------------------------------------------------------------\n')
    pokemon = Pokemon(id)
    print(f'Pokemon with ID = {pokemon.id} in the {Pokemon.pokedex} region is {pokemon.name.capitalize()}. And its been describes as:')
    print(f'\n\t{pokemon.describe()}\n')
    print('--------------------------------------------------------------------------------\n')
    print('Note that the only variables are the pokemon id, the region, its name and its')
    print('description. For that reason we will focus only on the pokemons description.')
