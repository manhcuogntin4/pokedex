from peewee import *
from playhouse.shortcuts import model_to_dict

from .database import db


class CommonModel(Model):
    def get_small_data(self):
        return model_to_dict(self, recurse=False, backrefs=False)
    class Meta:
        database = db
        schema = 'collections'


class User(CommonModel):
    id=PrimaryKeyField()
    name=CharField()
    email=CharField()

class Collection(CommonModel):
    id=PrimaryKeyField()
    name=CharField()

class UserColection(CommonModel):
    id=PrimaryKeyField()
    user=ForeignKeyField(User)
    collection=ForeignKeyField(Collection)

class PokemonCollection(CommonModel):
    id = PrimaryKeyField()
    name = CharField()
    hp = FloatField()
    special_attack = FloatField()
    defense = FloatField()
    attack = FloatField()
    special_defense = FloatField()
    speed = FloatField()
    sprite_back = CharField()
    sprite_front = CharField()
    collection=ForeignKeyField(Collection)
    @property
    def stats(self):
        return {'hp': self.hp, 'special-attack': self.special_attack, 'defense': self.defense, 'attack': self.attack,
                'special-defense': self.special_defense, 'speed': self.speed}

    def get_small_data(self):
        return {"id": self.id, "name": self.name, "stats": self.stats, 'sprite_back': self.sprite_back,
                'sprite_front': self.sprite_front}

class Duel(CommonModel):
    id=PrimaryKeyField()
    user1=ForeignKeyField(User)
    user2=ForeignKeyField(User)
    winner=CharField()



with db:
    User.create_table(fail_silently=True)
    Collection.create_table(fail_silently=True)
    UserColection.create_table(fail_silently=True)
    Duel.create_table(fail_silently=True)
    PokemonCollection.create_table(fail_silently=True)
