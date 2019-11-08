from pokedex.managers.generations import search_generations,create_generation,search_generation
from flask import request
from flask_restful import Resource
class Generations(Resource):
    def get(self):
        name=request.args.get("generation",None)
        ability=request.args.get("ability",False)
        type = request.args.get("type", False)
        return search_generations(name,ability,type)
    def put(self):
        data = request.json
        generation=create_generation(data['name'])
        return generation.get_small_data()
class Generation(Resource):
    def get(self,generation_name):
        return search_generation(generation_name).get_small_data()