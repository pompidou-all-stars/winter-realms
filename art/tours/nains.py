"""Nains : les 10 tours (noms de sim.js, FACTIONS). Les formes viennent des archétypes de
communs/tours_communes.py, dans le style de la faction ; retoucher STYLE['nains'] pour toute la faction,
ou ajouter ici une fonction propre à une tour pour la personnaliser."""
from tours_communes import tour

NOMS = [
    "Tourelle de guet",
    "Automate garde",
    "Cryo-forge",
    "Mortier runique",
    "Forge incandescente",
    "Canon arcanique",
    "Baliste naine",
    "Sentinelle d’acier",
    "Générateur runique",
    "Maître ingénieur",
]

def fabriquer(j):
    return tour('nains', j)
