"""Nains — Maître ingénieur (emplacement 9 : Mage · archimage).
Forme : archétype de communs/tours_communes.py dans le style de la faction (STYLE['nains']).
Pour personnaliser cette tour seule, remplacer l'appel à tour() par sa propre construction."""
from communs.tours_communes import tour
from communs.export_jeu import preparer

INFOS = {'categorie': 'tour', 'titre': "Maître ingénieur"}

def construire(ctx):
    preparer(tour('nains', 9))
