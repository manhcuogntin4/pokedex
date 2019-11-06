from .collections import get_collection,get_collections_user,get_pokemon,get_pokemons_collection
class Pokemon:
    def __init__(self,id):
        self.id = id
    def take_damages(self, attack):
        damages = max([0, attack - int(self.stats['defense'])])
        print(f"{self.name} prend {damages} de dommages")
        new_hp = self.get_hp() - damages
        self.stats['hp'] = new_hp
        return self.get_hp()

    def attack(self, pokemon):
        print(f"{self.name} attaque !")
        hp = pokemon.take_damages(int(self.stats['attack']))
        return hp

    def get_hp(self):
        return int(self.stats['hp'])

    def get_base_hp(self):
        return int(self.base_stats['hp'])

    def heal(self, amount):
        self.stats['hp'] = self.get_hp() + amount
        return self.get_hp()
    def load_pokemon_from_database(self):
        pokemon=get_pokemon(self.id)
        self.stats = pokemon.stats
        self.name = pokemon.name
    def display(self):
        print(f"name {self.name}")
        print(f"stats: {self.stats}")



class Collection:
    def __init__(self,id):
        self.id=id
        self.pokemons=self.get_pokemons()

    def get_pokemons_total_hp(self):
        hp = 0
        for pokemon in self.pokemons:
            hp += pokemon.get_hp()
        return hp

    def get_pokemons(self):
        pokemons=[]
        for pokemon in get_pokemons_collection(self.id):
            poke=Pokemon(pokemon.id)
            poke.load_pokemon_from_database()
            pokemons.append(poke)
        self.pokemons=pokemons

    def get_alive_pokemons(self):
        print('Pokemons disponibles :')
        alive_pokemons = []
        for pokemon in self.pokemons:
            if pokemon.get_hp() > 0:
                alive_pokemons.append(pokemon)
        for i,pokemon in enumerate(alive_pokemons):
            print(f"{i}: {pokemon.name}")
        return alive_pokemons
    def choose_pokemon(self,choice):
        pokemons=self.get_alive_pokemons()
        return pokemons[choice]


class Bag:
    def __init__(self):
        self.limit = 10
        self.content = []

    def get_number_of_type(self, type_of_object):
        i = 0
        for item in self.content:
            if type(item) == type_of_object:
                i += 1
        return i

    def add_item(self, item):
        if len(self.content) >= self.limit:
            print('Pas de place')
        elif item in self.content:
            print('Deja dans le sac')
        else:
            self.content.append(item)

    def __contains__(self, item):
        return item in self.content


class Player:
    def __init__(self, id):
        self.id=id
        self.bag = Bag()

    def get_item(self, item):
        self.bag.add_item(item)

    def choose_collection(self,choice):
        print("Choose a collection:")
        for i,collection in enumerate(self.collections):
            print(f"{i}: {collection.name}")
        return self.collections[choice]

    def load_player_from_data_base(self):
        user=get_user(self.id)
        self.name=user.name
        self.email=user.email
        collections=get_collections_user(self.id)
        user_collections=[]
        for c in collections:
            collection=Collection(c.id)
            collection.get_pokemons()
            user_collections.append(collection)
        self.collections=user_collections
    def choose_collection(self,choice):
        print(f"List of collection of {self.name}:")
        for i,collection in enumerate(self.collections):
            print(f"{i} : {collection.name}")
        return(self.collections[choice])



class Duel:
    def __init__(self, player_A, player_B,collection_A,collection_B):
        self.turn = 0
        self.pokemons = []
        self.players=[player_A,player_B]
        self.collections = [collection_A, collection_B]

    def get_turn_collection(self):
        return self.collections[self.turn % 2]

    def get_target_collection(self):
        return self.collections[(self.turn + 1) % 2]

    def get_turn_pokemon(self):
        return self.pokemons[self.turn % 2]

    def get_target_pokemon(self):
        return self.pokemons[(self.turn + 1) % 2]

    def are_all_collections_alive(self):
        for collection in self.collections:
            if collection.get_pokemons_total_hp() == 0:
                return False
        return True

    def start(self):
        print(f'Demarage du combat entre {self.players[0].name} et {self.players[1].name}')

        for collection in self.collections:
            self.pokemons.append(collection.choose_pokemon())

        while self.are_all_collections_alive()():
            player = self.get_turn_player()
            target_player = self.get_target_player()
            print(f"C'est le tour de {player.name} ! (Tour {self.turn + 1})")

            pokemon = self.get_turn_pokemon()
            target_pokemon = self.get_target_pokemon()

            pokemon.attack(target_pokemon)
            print(f'Le {target_pokemon.name} de {target_player.name} a {target_pokemon.get_hp()} HP')

            self.turn += 1
