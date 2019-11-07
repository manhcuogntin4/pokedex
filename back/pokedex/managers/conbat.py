from .collections import get_collection,get_collections_user,get_pokemon,\
    get_pokemons_collection, edit_pokemon_stats,delete_pokemon,get_user,create_duel
#from .potion import create_potion,get_potion

class Pokemon:
    def __init__(self,id):
        self.id = id
        self.used=False
    def take_damages(self, attack):
        damages = max([1, attack - int(self.stats['defense'])])
        print(f"{self.name} prend {damages} de dommages")
        new_hp = self.get_hp() - damages
        self.stats['hp'] = new_hp
        self.used=True
        return self.get_hp()

    def attack(self, pokemon):
        print(f"{self.name} attaque !")
        hp = pokemon.take_damages(int(self.stats['attack']))
        self.used = True
        return hp

    def get_hp(self):
        return int(self.stats['hp'])

    def get_base_hp(self):
        return int(self.base_stats['hp'])

    def heal(self, amount):
        self.stats['hp'] = self.get_hp() + amount
        self.used = True
        return self.get_hp()
    def load_pokemon_from_database(self):
        pokemon=get_pokemon(self.id)
        self.stats = pokemon.stats
        self.name = pokemon.name
    def display(self):
        print(f"name {self.name}")
        print(f"stats: {self.stats}")

    def update(self):
        if self.used:
            if self.get_hp()==0:
                delete_pokemon(self.id)
            else:
                edit_pokemon_stats(self.id,'hp',self.get_hp())


class Potion():
    def __init__(self, name, amount):
        self.name = name
        self.amount = amount
    def use(self, pokemon):
        pokemon.heal(self.amount)

    def use_collection(self,collection):
        for pokemon in collection.pokemons:
            self.use(pokemon)
        collection.update_pokemons()

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
        alive_pokemons = []
        for pokemon in self.pokemons:
            if pokemon.get_hp() > 0:
                print(pokemon.get_hp())
                alive_pokemons.append(pokemon)
        return alive_pokemons
    def choose_pokemon(self,choice):
        pokemons=self.get_alive_pokemons()
        if(len(pokemons)>0):
            return pokemons[choice]
        return None

    def choose_pokemon_id(self,pokemon_id):
        for pokemon in self.get_alive_pokemons():
            if pokemon.id==pokemon_id:
                return pokemon

    def load_collection(self,collection_id):
        collection=get_collection(collection_id)
        self.name=collection.name
        self.get_pokemons()
    def update_pokemons(self):
        for pokemon in self.pokemons:
            pokemon.update()

    def heal(self,potion):
        for pokemon in self.pokemons:
            potion.use(pokemon)



class Player:
    def __init__(self, id):
        self.id=id
        self.bag = Bag()

    def get_item(self, item):
        self.bag.add_item(item)

    def choose_collection(self,choice):
        if len(self.collections)>0:
            return self.collections[choice]
        else:
            return None

    def load_player_from_data_base(self):
        user=get_user(self.id)
        self.name=user.name
        self.email=user.email
        collections=get_collections_user(self.id)
        user_collections=[]
        for c in collections:
            collection=Collection(c.id)
            collection.load_collection(c.id)
            user_collections.append(collection)
        self.collections=user_collections

    def choose_collection(self,choice):
        if len(self.collections)>0:
            print(f"List of collection of {self.name}:")
            for i,collection in enumerate(self.collections):
                print(f"{i} : {collection.name}")
            return(self.collections[choice])
        else:
            return None
    def choose_collection_by_id(self,id):
        for collection in self.collections:
            print("collection_id", type(collection.id))
            print("id",type(id))
            if collection.id == int(id):
                print("Here")
                collection.load_collection(id)
                collection.get_pokemons()
                print("found collection")
                return collection
        else:
            print("not found collection")
            return None



class Duel:
    def __init__(self, player_A, player_B,collection_A,collection_B):
        self.turn = 0
        self.pokemons = []
        player1=Player(player_A)
        player1.load_player_from_data_base()
        player2=Player(player_B)
        player2.load_player_from_data_base()
        collection1=player1.choose_collection(collection_A)
        collection2=player2.choose_collection(collection_B)
        self.players=[player1,player2]
        self.collections = [collection1, collection2]

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
            if collection.get_pokemons_total_hp() <= 0:
                return False
        return True

    def start(self):
        print(f'Demarage du combat entre {self.players[0].name} et {self.players[1].name}')
        if(len(self.players[0].collections)>0) and((len(self.players[0].collections)>0)):
            while len(self.collections[0].get_alive_pokemons()) and len(self.collections[1].get_alive_pokemons()):
                print("User1:", len(self.collections[0].get_alive_pokemons()))
                print("User2:", len(self.collections[1].get_alive_pokemons()))
                pokemons=[]
                for collection in self.collections:
                    pokemons.append(collection.choose_pokemon(0))
                self.pokemons=pokemons

                while self.are_all_collections_alive():
                    player_collection= self.get_turn_collection()
                    target_player_collection = self.get_target_collection()
                    print(f"C'est le tour de {player_collection.name} ! (Tour {self.turn + 1})")
                    pokemon = self.get_turn_pokemon()
                    target_pokemon = self.get_target_pokemon()

                    pokemon.attack(target_pokemon)
                    print(f'Le {target_pokemon.name} de {target_player_collection.name} a {target_pokemon.get_hp()} HP')
                    self.turn += 1
                for collection in self.collections:
                    print("hp:", collection.choose_pokemon(0).get_hp())
                break
            if len(self.collections[0].get_alive_pokemons())==0:
                create_duel(self.players[0].id,self.players[1].id,self.players[1].name)
            else:
                create_duel(self.players[0].id, self.players[1].id, self.players[0].name)
            for collection in self.collections:
                collection.update_pokemons()

        else:
            if len(self.players[0].collections) ==0:
                print(f"{self.player[0].name} hasn't any collection")
            else:
                print(f"{self.player[1].name} hasn't any collection")





