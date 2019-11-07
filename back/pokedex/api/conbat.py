from pokedex.managers.conbat import Duel
from flask import request
from flask_restful import Resource
class Match(Resource):
    def get(self,u1,u2,c1,c2):
        duel=Duel(int(u1),int(u2),int(c1),int(c2))
        winner=duel.start()
        return {"winner":winner}

