"""Cour des Ossements — Autel de peste (emplacement 3 : zone).
Forme : communs/ossements_hd.py (2.40, direction « grimdark » ; créatures au procédé des monstres organiques)."""
from communs.ossements_hd import tour
from communs.export_jeu import preparer

INFOS = {'categorie': 'tour', 'titre': "Autel de peste"}

def construire(ctx):
    preparer(tour(3))
