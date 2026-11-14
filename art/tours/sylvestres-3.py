"""Sylvestres — Fleur explosive (emplacement 3 : Canon · artillerie).
Forme : archétype de communs/tours_communes.py dans le style de la faction (STYLE['sylvestres']).
Pour personnaliser cette tour seule, remplacer l'appel à tour() par sa propre construction."""
from communs.tours_communes import tour
from communs.export_jeu import preparer

INFOS = {'categorie': 'tour', 'titre': "Fleur explosive"}

def construire(ctx):
    preparer(tour('sylvestres', 3))
