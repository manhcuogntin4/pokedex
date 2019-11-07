from pokedex.models.potion import Potion


def get_potion(name):
    potion = Potion.get_or_none(name=name)
    return potion

def create_potion(name,amount):
    potion=Potion.get_or_none(name=name)
    if potion is None:
        potion=Potion.create(name=name, amount=amount)
    return potion