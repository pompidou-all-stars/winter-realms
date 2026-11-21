"""Elfes de Lunebois — Arbre-Mère (emplacement 9 : ultime).
Forme : communs/lunebois_hd.py (2.40, direction « grimdark » ; créatures au procédé des monstres organiques)."""
from communs.lunebois_hd import tour
from communs.export_jeu import preparer

INFOS = {'categorie': 'tour', 'titre': "Arbre-Mère"}

def construire(ctx):
    preparer(tour(9))
