"""Alliance : les 10 tours (noms de sim.js, FACTIONS). Les formes viennent des archétypes de
communs/tours_communes.py, dans le style de la faction ; retoucher STYLE['alliance'] pour toute la faction,
ou ajouter ici une fonction propre à une tour pour la personnaliser."""
from tours_communes import tour

NOMS = [
    "Tour des archers",
    "Bastion du chevalier",
    "Obélisque de givre",
    "Bombarde royale",
    "Brasier du griffon",
    "Sanctuaire solaire",
    "Tour des sentinelles",
    "Garde du lion",
    "Cristal hivernal",
    "Arcaniste royal",
]

def fabriquer(j):
    return tour('alliance', j)
