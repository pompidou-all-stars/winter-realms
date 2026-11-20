"""Elfes de Lunebois — Fleur de venin (emplacement 3 : zone).
Forme : communs/lunebois_hd.py (2.40, direction « grimdark » ; créatures au procédé des monstres organiques)."""
from communs.lunebois_hd import tour
from communs.export_jeu import preparer

INFOS = {'categorie': 'tour', 'titre': "Fleur de venin"}

def construire(ctx):
    preparer(tour(3))
