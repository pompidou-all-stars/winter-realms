"""Royaume d’Aubeval — Inquisiteur (emplacement 8 : anti-boss).
Forme : communs/aubeval_hd.py (2.40, direction « grimdark » ; créatures au procédé des monstres organiques)."""
from communs.aubeval_hd import tour
from communs.export_jeu import preparer

INFOS = {'categorie': 'tour', 'titre': "Inquisiteur"}

def construire(ctx):
    preparer(tour(8))
