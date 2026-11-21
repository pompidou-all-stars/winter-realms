"""Royaume d’Aubeval — Comptoir marchand (emplacement 6 : signature).
Forme : communs/aubeval_hd.py (2.40, direction « grimdark » ; créatures au procédé des monstres organiques)."""
from communs.aubeval_hd import tour
from communs.export_jeu import preparer

INFOS = {'categorie': 'tour', 'titre': "Comptoir marchand"}

def construire(ctx):
    preparer(tour(6))
