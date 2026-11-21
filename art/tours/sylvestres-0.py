"""Elfes de Lunebois — Archers sylvains (emplacement 0 : tir de base).
Forme : communs/lunebois_hd.py (2.40, direction « grimdark » ; créatures au procédé des monstres organiques)."""
from communs.lunebois_hd import tour
from communs.export_jeu import preparer

INFOS = {'categorie': 'tour', 'titre': "Archers sylvains"}

def construire(ctx):
    preparer(tour(0))
