"""Horde : les 10 tours (noms de sim.js, FACTIONS). Les formes viennent des archétypes de
communs/tours_communes.py, dans le style de la faction ; retoucher STYLE['horde'] pour toute la faction,
ou ajouter ici une fonction propre à une tour pour la personnaliser."""
from tours_communes import tour

NOMS = [
    "Tour des chasseurs",
    "Totem du berserker",
    "Totem de glace",
    "Canon des clans",
    "Fourneau de guerre",
    "Chaman des flammes",
    "Tour des éclaireurs",
    "Garde-lame",
    "Totem des esprits",
    "Grand sorcier orc",
]

def fabriquer(j):
    return tour('horde', j)
