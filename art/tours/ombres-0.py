"""Cour des Ossements — Tour des archers squelettes (emplacement 0 : tir de base).
Forme : communs/ossements_hd.py (2.40, direction « grimdark » ; créatures au procédé des monstres organiques)."""
from communs.ossements_hd import tour
from communs.export_jeu import preparer

INFOS = {'categorie': 'tour', 'titre': "Tour des archers squelettes"}

def construire(ctx):
    preparer(tour(0))
