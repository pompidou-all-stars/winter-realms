"""Nains — Cryo-forge (emplacement 2 : Givre · contrôle).
Forme : archétype de communs/tours_communes.py dans le style de la faction (STYLE['nains']).
Pour personnaliser cette tour seule, remplacer l'appel à tour() par sa propre construction."""
from communs.tours_communes import tour
from communs.export_jeu import preparer

INFOS = {'categorie': 'tour', 'titre': "Cryo-forge"}

def construire(ctx):
    preparer(tour('nains', 2))
