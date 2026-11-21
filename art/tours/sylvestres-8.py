"""Elfes de Lunebois — Tireur des cimes (emplacement 8 : anti-boss).
Forme : communs/lunebois_hd.py (2.40, direction « grimdark » ; créatures au procédé des monstres organiques)."""
from communs.lunebois_hd import tour
from communs.export_jeu import preparer

INFOS = {'categorie': 'tour', 'titre': "Tireur des cimes"}

def construire(ctx):
    preparer(tour(8))
