"""Clans de l’Orage Blanc — Cœur de l’Orage (emplacement 9 : ultime).
Forme : communs/orage_hd.py (2.40, direction « grimdark » ; créatures au procédé des monstres organiques)."""
from communs.orage_hd import tour
from communs.export_jeu import preparer

INFOS = {'categorie': 'tour', 'titre': "Cœur de l’Orage"}

def construire(ctx):
    preparer(tour(9))
