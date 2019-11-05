import requests

from pokedex.models.pokemon import EggGroup


def load_egg_group_from_api(name):
    request = requests.get(f'https://pokeapi.co/api/v2/egg-group/{name}')
    data = request.json()

    egg_group = EggGroup.get_or_none(name=data['name'])
    if egg_group is None:
        egg_group = EggGroup.create(name=data['name'])

    return egg_group


def load_egg_groups_from_api():
    i = 0

    next_page = 'https://pokeapi.co/api/v2/egg-group/'
    while next_page is not None:
        request = requests.get(next_page)
        data = request.json()

        next_page = data['next']

        for egg_group in data['results']:
            load_egg_group_from_api(egg_group['name'])
            i += 1

        print(f'{i} egg groups loaded.')

    return i
