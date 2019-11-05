import requests
from playhouse.shortcuts import update_model_from_dict

from pokedex.models.collections import User, PokemonCollection,Collection,UserColection

from pokedex.models.pokemon import Pokemon


def create_user(name, email):
    user = User.get_or_none(name=name)
    if user is None:
        user = User.create(name=name, email=email)
    return user
def create_collection(name):
    collection=Collection.get_or_none(name=name)
    if collection is None:
        collection=Collection.create(name=name)
    return  collection

def add_user_collection(user_id,collection_id):
    user=User.get_or_none(id=user_id)
    collection=Collection(id=collection_id)
    user_collection=UserColection.get_or_none(user=user, collection=collection)
    if user_collection is None:
        user_collection = UserColection.create(user=user, collection=collection)
    return user_collection

def add_user_pokemon(user_id, pokemon_id):
    user=User.get_or_none(id=user_id)
    pokemon=Pokemon.get_or_none(id=pokemon_id)
    pokemon_stats=pokemon.stats
    name=pokemon.name
    stats = {}
    for k,v in pokemon_stats.items():
        stats[k.replace('-', '_')]=v
    new_pokemon_user=PokemonUser.create(name=name,user=user,sprite_back=pokemon.sprite_back, sprite_front=pokemon.sprite_front, **stats)
    return new_pokemon_user

def add_collection_pokemon(collection_id, pokemon_id):
    collection=Collection.get_or_none(id=collection_id)
    pokemon = Pokemon.get_or_none(id=pokemon_id)
    pokemon_stats = pokemon.stats
    name = pokemon.name
    stats = {}
    for k, v in pokemon_stats.items():
        stats[k.replace('-', '_')] = v
    new_pokemon_collection = PokemonCollection.create(name=name, collection=collection, sprite_back=pokemon.sprite_back,
                                          sprite_front=pokemon.sprite_front, **stats)
    return new_pokemon_collection
def get_user(user_id)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               :
    user=User.get_or_none(id=user_id)
    return user

def get_collection(collection_id):
    collection=Collection.get_or_none(id=collection_id)
    return collection

