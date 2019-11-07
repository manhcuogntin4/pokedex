from pokedex.models.potion import Potion
from pokedex.managers.collections import add_user_pokemon,create_user,get_user,create_collection, add_user_collection, add_collection_pokemon,get_collections_user
from pokedex.managers.conbat import Player,Pokemon,Potion as P

def get_potion(name):
    potion = Potion.get_or_none(name=name)
    return potion

def create_potion(name,amount):
    potion=Potion.get_or_none(name=name)
    if potion is None:
        potion=Potion.create(name=name, amount=amount)
    return potion

def use_potion_pokemon(user_id,collection_id,pokemon_id,potion_name):
    user = Player(user_id)
    user.load_player_from_data_base()
    collection = user.choose_collection_by_id(collection_id)
    collection.get_pokemons()
    potion = P(get_potion(potion_name).name, get_potion(potion_name).amount)
    pokemon = collection.choose_pokemon_id(pokemon_id)
    potion.use(pokemon)
    pokemon.update()

def use_potion_collection(user_id,collection_id, potion_name):
    user = Player(user_id)
    user.load_player_from_data_base()
    collection = user.choose_collection_by_id(collection_id)
    collection.get_pokemons()
    potion = P(get_potion(potion_name).name, get_potion(potion_name).amount)
    potion.use_collection(collection)
