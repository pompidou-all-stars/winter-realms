"""Elfes de Lunebois — Bosquet ancien (emplacement 7 : soutien).
Forme : communs/lunebois_hd.py (2.40, direction « grimdark » ; créatures au procédé des monstres organiques)."""
from communs.lunebois_hd import tour
from communs.export_jeu import preparer

INFOS = {'categorie': 'tour', 'titre': "Bosquet ancien"}

def construire(ctx):
    preparer(tour(7))
