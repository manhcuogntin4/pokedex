from flask import request
from flask_restful import Resource
from pokedex.managers.websrapping import load_pokemons_from_wikipedia, search_pokemons_scrapping

class PokemonsScrapping(Resource):
    def get(self):
        query = request.args['query']
        pokemons_matching = search_pokemons_scrapping(query)
        pokemons = [pokemon.get_small_data() for pokemon in pokemons_matching]
        return pokemons
    def put(self):
        load_pokemons_from_wikipedia()