"""Clans de l’Orage Blanc — Grands tambours de guerre (emplacement 7 : soutien).
Forme : communs/orage_hd.py (2.40, direction « grimdark » ; créatures au procédé des monstres organiques)."""
from communs.orage_hd import tour
from communs.export_jeu import preparer

INFOS = {'categorie': 'tour', 'titre': "Grands tambours de guerre"}

def construire(ctx):
    preparer(tour(7))
