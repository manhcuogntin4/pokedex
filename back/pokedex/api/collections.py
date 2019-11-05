from flask import request
from flask_restful import Resource

from pokedex.managers.analytics import add_pokemon_search_history,add_agent_query_search,get_agent_request
from pokedex.managers.pokemons import search_pokemons, get_pokemon_by_name, create_pokemon, delete_pokemon
from pokedex.managers.types import get_pokemons_from_type
from pokedex.managers.collections import add_user_pokemon,create_user,get_user,create_collection, add_user_collection, add_collection_pokemon

class Users(Resource):
    def post(self):
        data = request.json
        user=create_user(data['name'],data['email'])
        return user.get_small_data()


class Collections(Resource):
    def post(self):
        data=request.json
        collection=create_collection(data['name'])
        return collection.get_small_data()

class UserCollection(Resource):
    def post(self,user_id,collection_id):
        user_collection=add_user_collection(user_id,collection_id)
        return user_collection.get_small_data()


class PokemonCollection(Resource):
    def post(self,collection_id,pokemon_id):
        pokemon_collection=add_collection_pokemon(collection_id,pokemon_id)
        return pokemon_collection.get_small_data()

    def patch(self,pokemonuser_id):
        pass

