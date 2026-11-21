"""Royaume d’Aubeval — Baliste céleste (emplacement 4 : anti-aérien).
Forme : communs/aubeval_hd.py (2.40, direction « grimdark » ; créatures au procédé des monstres organiques)."""
from communs.aubeval_hd import tour
from communs.export_jeu import preparer

INFOS = {'categorie': 'tour', 'titre': "Baliste céleste"}

def construire(ctx):
    preparer(tour(4))
