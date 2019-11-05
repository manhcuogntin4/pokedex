from flask import request
from flask_restful import Resource

from pokedex.managers.analytics import add_pokemon_search_history,add_agent_query_search,get_agent_request

class Analytic(Resource):
    def get(self, platform):
        count = get_agent_request(platform)
        return count