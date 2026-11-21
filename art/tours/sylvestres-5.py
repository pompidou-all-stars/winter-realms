"""Elfes de Lunebois — Puits de lune (emplacement 5 : détection).
Forme : communs/lunebois_hd.py (2.40, direction « grimdark » ; créatures au procédé des monstres organiques)."""
from communs.lunebois_hd import tour
from communs.export_jeu import preparer

INFOS = {'categorie': 'tour', 'titre': "Puits de lune"}

def construire(ctx):
    preparer(tour(5))
