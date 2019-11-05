from flask import request
from flask_restful import Resource
from pokedex.managers.egg_groups import get_egg_groups, get_spices_of_egg_groups, get_egg_group
from pokedex.managers.species import get_pokemons_of_species



class Egg_groups(Resource):
    def get(self):
        sp = request.args.get('species', 'false') == 'true'
        pokemons = request.args.get('pokemons', 'false') == 'true'
        egg_groups = get_egg_groups()
        results = [egg.get_small_data() for egg in egg_groups]

        if sp:
            spices_by_egg_groups = get_spices_of_egg_groups(egg_groups)
            for egg in results:
                egg['species'] = [p.name for p in spices_by_egg_groups[egg['id']]]
        if pokemons:
            spices_by_egg_groups = get_spices_of_egg_groups(egg_groups)
            for egg in results:
                species=spices_by_egg_groups[egg['id']]
                pokemons=get_pokemons_of_species(species)
                names=[]
                for k,v in pokemons.items():
                    for pokemon in v:
                        if pokemon.name not in names:
                            names.append(pokemon.name)
                egg['pokemons']=names
        return results


class Egg_group(Resource):
    def get(self, egg_group_id):
        egg = get_egg_group(egg_group_id)
        results = egg.get_small_data()
        '''
        pokemons_by_species = get_pokemons_of_species([specie])
        results['pokemons'] = [p.get_small_data() for p in pokemons_by_species[specie.id]]
        '''
        return results
