"""Sylvestres : les 10 tours (noms de sim.js, FACTIONS). Les formes viennent des archétypes de
communs/tours_communes.py, dans le style de la faction ; retoucher STYLE['sylvestres'] pour toute la faction,
ou ajouter ici une fonction propre à une tour pour la personnaliser."""
from tours_communes import tour

NOMS = [
    "Arbre sentinelle",
    "Gardien des racines",
    "Pierre de rosée",
    "Fleur explosive",
    "Cœur ardent",
    "Cercle druidique",
    "Nid des faucons",
    "Dryade protectrice",
    "Cristal lunaire",
    "Ancien arcanique",
]

def fabriquer(j):
    return tour('sylvestres', j)
