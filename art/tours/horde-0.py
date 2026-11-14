"""Horde — Tour des chasseurs (emplacement 0 : Archer · tir rapide).
Forme : archétype de communs/tours_communes.py dans le style de la faction (STYLE['horde']).
Pour personnaliser cette tour seule, remplacer l'appel à tour() par sa propre construction."""
from communs.tours_communes import tour
from communs.export_jeu import preparer

INFOS = {'categorie': 'tour', 'titre': "Tour des chasseurs"}

def construire(ctx):
    preparer(tour('horde', 0))
