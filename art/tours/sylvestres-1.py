"""Elfes de Lunebois — Haie de ronces (emplacement 1 : corps à corps).
Forme : communs/lunebois_hd.py (2.40, direction « grimdark » ; créatures au procédé des monstres organiques)."""
from communs.lunebois_hd import tour
from communs.export_jeu import preparer

INFOS = {'categorie': 'tour', 'titre': "Haie de ronces"}

def construire(ctx):
    preparer(tour(1))
