"""Légion des ombres : les 10 tours (noms de sim.js, FACTIONS). Les formes viennent des archétypes de
communs/tours_communes.py, dans le style de la faction ; retoucher STYLE['ombres'] pour toute la faction,
ou ajouter ici une fonction propre à une tour pour la personnaliser."""
from tours_communes import tour

NOMS = [
    "Tour des damnés",
    "Chevalier funeste",
    "Obélisque maudit",
    "Mortier infernal",
    "Puits de lave",
    "Nexus du néant",
    "Œil démoniaque",
    "Gardien spectral",
    "Cristal corrupteur",
    "Archimage noir",
]

def fabriquer(j):
    return tour('ombres', j)
