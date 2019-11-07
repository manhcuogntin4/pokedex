from flask import Blueprint
from flask_restful import Api

from pokedex.models.database import db

from .pokemons import Pokemon, Pokemons, Pokemons_Type
from .species import Species, Specie
from .types import Types
from .Analytic import Analytic
from .collections import Users, PokemonCollection, UserCollection, Collections,User
from .conbat import Match
from .potion import Potions, PotionHeal
api_bp = Blueprint('api', __name__)
api = Api(api_bp)


def register_api(app):
    @api_bp.before_request
    def before_request():
        db.connect(reuse_if_open=True)

    @api_bp.teardown_request
    def after_request(exception=None):
        db.close()

    api.add_resource(Pokemons, '/pokemons')
    api.add_resource(Pokemon, '/pokemon/<pokemon_name>')

    api.add_resource(Types, '/types')
    api.add_resource(Species, '/species')
    api.add_resource(Pokemons_Type, '/pokemons/type/<type_id>')
    api.add_resource(Specie, '/specie/<specie_id>')
    api.add_resource(Analytic, '/analytic/<platform>')
    api.add_resource(Users,'/users')
    api.add_resource(UserCollection,'/usercollection/<user_id>/<collection_id>')
    api.add_resource(Collections,'/collections')
    api.add_resource(User,'/user/<user_id>')
    api.add_resource(PokemonCollection,'/pokemoncollection/<collection_id>/<pokemon_id>')
    api.add_resource(Match,'/duel/<u1>/<u2>/<c1>/<c2>')
    api.add_resource(Potions,'/potions')
    api.add_resource(PotionHeal,'/potion/<potion_name>')
    app.register_blueprint(api_bp, url_prefix="/api/v1")
