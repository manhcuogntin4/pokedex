from pokedex.models.pokemon import Generation,Ability

def search_generations(name=None,ability=False):
    generations=Generation.select()
    if name:
        generations = Generation.select().where(Generation.name.contains(name))
    generations=[generation.get_small_data() for generation in generations]
    print(ability)
    if ability:
        print("Here")
        for generation in generations:
            count=Ability.select(Ability.id).join(Generation).where(Generation.id==generation['id']).count()
            generation['ability']=count

    return generations

