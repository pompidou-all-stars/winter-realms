"""Légion des ombres — Puits de lave (emplacement 4 : Flammes · dégâts continus).
Forme : archétype de communs/tours_communes.py dans le style de la faction (STYLE['ombres']).
Pour personnaliser cette tour seule, remplacer l'appel à tour() par sa propre construction."""
from communs.tours_communes import tour
from communs.export_jeu import preparer

INFOS = {'categorie': 'tour', 'titre': "Puits de lave"}

def construire(ctx):
    preparer(tour('ombres', 4))
