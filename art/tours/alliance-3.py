"""Royaume d’Aubeval — Trébuchet (emplacement 3 : zone).
Forme : communs/aubeval_hd.py (2.40, direction « grimdark » ; créatures au procédé des monstres organiques)."""
from communs.aubeval_hd import tour
from communs.export_jeu import preparer

INFOS = {'categorie': 'tour', 'titre': "Trébuchet"}

def construire(ctx):
    preparer(tour(3))
