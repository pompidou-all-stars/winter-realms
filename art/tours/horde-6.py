"""Clans de l’Orage Blanc — Totem de foudre (emplacement 6 : signature).
Forme : communs/orage_hd.py (2.40, direction « grimdark » ; créatures au procédé des monstres organiques)."""
from communs.orage_hd import tour
from communs.export_jeu import preparer

INFOS = {'categorie': 'tour', 'titre': "Totem de foudre"}

def construire(ctx):
    preparer(tour(6))
