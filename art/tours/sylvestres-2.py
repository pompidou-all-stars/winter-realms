"""Elfes de Lunebois — Gardien enracineur (emplacement 2 : contrôle).
Forme : communs/lunebois_hd.py (2.40, direction « grimdark » ; créatures au procédé des monstres organiques)."""
from communs.lunebois_hd import tour
from communs.export_jeu import preparer

INFOS = {'categorie': 'tour', 'titre': "Gardien enracineur"}

def construire(ctx):
    preparer(tour(2))
