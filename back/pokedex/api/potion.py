from pokedex.managers.potion import create_potion,get_potion
from flask import request
from flask_restful import Resource
from pokedex.managers.collections import add_user_pokemon,create_user,get_user,create_collection, add_user_collection, add_collection_pokemon,get_collections_user
from pokedex.managers.conbat import Player,Pokemon,Potion
class Potions(Resource):
    def post(self):
        data = request.json
        potion = create_potion(data['name'], data['amount'])
        return potion.get_small_data()
class PotionHeal(Resource):
    def get(self,potion_name):
        potion=get_potion(potion_name)
        return potion.get_small_data()

    def patch(self,potion_name):
        print("hello")
        user_id=request.args['user']
        print(user_id)
        collection_id = request.args['collection']
        print("hello")
        all = request.args['all']
        print(user_id,collection_id,all)
        user=Player(user_id)
        user.load_player_from_data_base()
        collection = user.choose_collection_by_id(collection_id)
        collection.get_pokemons()
        potion=Potion(get_potion(potion_name).name,get_potion(potion_name).amount)
        potion.name=get_potion(potion_name).name
        potion.amount=get_potion(potion_name).amount

        if not all:
            pokemon_id=request.args['collection']
            pokemon=collection.choose_pokemon_id(pokemon_id)
            potion.use(pokemon)
            pokemon.update()
        else:
            potion.use_collection(collection)
            collection.update_pokemons()


