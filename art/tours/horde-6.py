"""Horde — Tour des éclaireurs (emplacement 6 : Archer · tireur d'élite).
Forme : archétype de communs/tours_communes.py dans le style de la faction (STYLE['horde']).
Pour personnaliser cette tour seule, remplacer l'appel à tour() par sa propre construction."""
from communs.tours_communes import tour
from communs.export_jeu import preparer

INFOS = {'categorie': 'tour', 'titre': "Tour des éclaireurs"}

def construire(ctx):
    preparer(tour('horde', 6))
