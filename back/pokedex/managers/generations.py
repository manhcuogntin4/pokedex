from pokedex.models.pokemon import Generation,Ability,Type

def search_generations(name=None,ability=False,type=False):
    generations=Generation.select()
    if name:
        generations = Generation.select().where(Generation.name.contains(name))
    generations=[generation.get_small_data() for generation in generations]
    print(ability)
    if ability:
        for generation in generations:
            count=Ability.select(Ability.id).join(Generation).where(Generation.id==generation['id']).count()
            generation['ability']=count
    if type:
        for generation in generations:
            count=Type.select(Ability.id).join(Generation).where(Generation.id==generation['id']).count()
            generation['type']=count

    return generations

def create_generation(name):
    generation=Generation.get_or_none(name=name)
    if generation is None:
        generation=Generation.create(name=name)
    return  generation

def search_generation(name):
    generation=Generation.get_or_none(name=name)
    return generation