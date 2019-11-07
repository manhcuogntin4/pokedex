from pokedex.managers.potion import create_potion,get_potion
from flask import request
from flask_restful import Resource
from pokedex.managers.collections import add_user_pokemon,create_user,get_user,create_collection, add_user_collection, add_collection_pokemon,get_collections_user
from pokedex.managers.conbat import Player,Pokemon,Potion
from pokedex.managers.potion import use_potion_collection,use_potion_pokemon
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
        if not all:
            pokemon_id=request.args['collection']
            use_potion_pokemon(user_id,collection_id,pokemon_id,potion_name)
        else:
            use_potion_collection(user_id,collection_id,potion_name)


