"""Royaume d’Aubeval — Rayon de l’Aube (emplacement 9 : ultime).
Forme : communs/aubeval_hd.py (2.40, direction « grimdark » ; créatures au procédé des monstres organiques)."""
from communs.aubeval_hd import tour
from communs.export_jeu import preparer

INFOS = {'categorie': 'tour', 'titre': "Rayon de l’Aube"}

def construire(ctx):
    preparer(tour(9))
