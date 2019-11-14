import requests
from pokedex.models.scrapping import Pokemon
from lxml import html
from tqdm import tqdm

def search_pokemons_scrapping(query):
    query = query.lower()
    pokemons = Pokemon.select().where(Pokemon.name.contains(query)).limit(20)
    return  pokemons


def load_pokemons_from_wikipedia():
    wikipedia_request = requests.get('https://en.wikipedia.org/wiki/List_of_Pok%C3%A9mon')
    xpath = '/ html / body / div[3] / div[3] / div[4] / div / table[3]'

    tree = html.fromstring(wikipedia_request.content)
    pokemons_tables = tree.xpath(xpath)

    pokemons_table = pokemons_tables[0]
    pokemons_table_rows = pokemons_table.findall('.//tr')


    pokemons=[]
    generations=pokemons_table_rows[0].findall('th')
    generations=[generation.text_content().strip('\n') for generation in generations]
    print(generations)
    for row in pokemons_table_rows[2:]:

        pokemon_id = None

        i = 0
        for column in row.findall('td'):
            pokemon = {}
            if i % 2 == 0:
                content = column.text_content()
                if 'No additional' not in content:
                    pokemon_id = int(content)

                else:
                    i += 1
            else:
                symbols_to_strip = ['\n', '※', '♭','~','♯']
                pokemon_name = column.text_content()
                sb=''
                for symbol in symbols_to_strip:
                    if symbol in pokemon_name:
                        sb+=symbol
                        pokemon_name = pokemon_name.strip(symbol)

                if pokemon_id is not None:
                    pokemon['id'] = pokemon_id
                    pokemon['name']=pokemon_name
                    pokemon['generation'] = generations[int(i/2)]
                    pokemons.append(pokemon)
                    pokemon['symbol']=sb.strip('\n')

            i += 1


    for pokemon in pokemons:
        pk=Pokemon.get_or_none(name=pokemon['name'])
        if pk is None:
            Pokemon.create(name=pokemon['name'],generation=pokemon['generation'],symbol=pokemon['symbol'])

    print(len(pokemons))