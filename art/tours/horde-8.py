"""Clans de l’Orage Blanc — Totem de sang (emplacement 8 : anti-boss).
Forme : communs/orage_hd.py (2.40, direction « grimdark » ; créatures au procédé des monstres organiques)."""
from communs.orage_hd import tour
from communs.export_jeu import preparer

INFOS = {'categorie': 'tour', 'titre': "Totem de sang"}

def construire(ctx):
    preparer(tour(8))
