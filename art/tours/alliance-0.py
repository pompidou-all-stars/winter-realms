"""Royaume d’Aubeval — Tour d’arbalétriers (emplacement 0 : tir de base).
Forme : communs/aubeval_hd.py (2.40, direction « grimdark » ; créatures au procédé des monstres organiques)."""
from communs.aubeval_hd import tour
from communs.export_jeu import preparer

INFOS = {'categorie': 'tour', 'titre': "Tour d’arbalétriers"}

def construire(ctx):
    preparer(tour(0))
