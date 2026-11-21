"""Royaume d’Aubeval — Poste de hallebardiers (emplacement 1 : corps à corps).
Forme : communs/aubeval_hd.py (2.40, direction « grimdark » ; créatures au procédé des monstres organiques)."""
from communs.aubeval_hd import tour
from communs.export_jeu import preparer

INFOS = {'categorie': 'tour', 'titre': "Poste de hallebardiers"}

def construire(ctx):
    preparer(tour(1))
