from flask import request
from flask_restful import Resource

from pokedex.managers.analytics import add_pokemon_search_history,add_agent_query_search,get_agent_request
from pokedex.managers.pokemons import search_pokemons, get_pokemon_by_name, create_pokemon, delete_pokemon
from pokedex.managers.types import get_pokemons_from_type

class Pokemons(Resource):
    def get(self):
        query = request.args['query']
        moyens = request.args.get('moyen', 'false') == 'true'

        pokemons_matching = search_pokemons(query, type=None)
        pokemons = [pokemon.get_small_data() for pokemon in pokemons_matching]
        add_agent_query_search(request,query)
        print(pokemons[1]['stats'].keys())
        if moyens:
            pokemons_moyens={}
            keys=pokemons[0]['stats'].keys()
            for key in keys:
                pokemons_moyens[key]=0
            for key in keys:
                for pokemon in pokemons:
                    pokemons_moyens[key]+=pokemon['stats'][key]
                pokemons_moyens[key]=pokemons_moyens[key]/len(pokemons)
            return pokemons_moyens

        return pokemons



    def post(self):
        data = request.json
        pokemon = create_pokemon(data['name'], data['hp'], 10, 0, 0, 0, 0)
        return pokemon.get_small_data()


class Pokemon(Resource):
    def get(self, pokemon_name):
        pokemon = get_pokemon_by_name(pokemon_name)
        if pokemon is None:
            return {'msg': 'Not found'}, 404

        return pokemon.get_small_data()

    def patch(self, pokemon_name):
        return 'panic', 500

    def delete(self, pokemon_name):
        result = delete_pokemon(pokemon_name)
        return result
class Pokemons_Type(Resource):
    def get(self, type_id):
        pokemons_matching=get_pokemons_from_type(type_id)

        pokemons=[p.get_small_data() for p in pokemons_matching]
        return pokemons