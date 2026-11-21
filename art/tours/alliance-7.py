"""Royaume d’Aubeval — Étendard royal (emplacement 7 : soutien).
Forme : communs/aubeval_hd.py (2.40, direction « grimdark » ; créatures au procédé des monstres organiques)."""
from communs.aubeval_hd import tour
from communs.export_jeu import preparer

INFOS = {'categorie': 'tour', 'titre': "Étendard royal"}

def construire(ctx):
    preparer(tour(7))
