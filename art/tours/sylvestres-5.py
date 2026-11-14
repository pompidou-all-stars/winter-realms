"""Sylvestres — Cercle druidique (emplacement 5 : Mage · arcanes).
Forme : archétype de communs/tours_communes.py dans le style de la faction (STYLE['sylvestres']).
Pour personnaliser cette tour seule, remplacer l'appel à tour() par sa propre construction."""
from communs.tours_communes import tour
from communs.export_jeu import preparer

INFOS = {'categorie': 'tour', 'titre': "Cercle druidique"}

def construire(ctx):
    preparer(tour('sylvestres', 5))
