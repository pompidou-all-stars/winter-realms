"""Clans de l’Orage Blanc — Hutte du berserker (emplacement 1 : corps à corps).
Forme : communs/orage_hd.py (2.40, direction « grimdark » ; créatures au procédé des monstres organiques)."""
from communs.orage_hd import tour
from communs.export_jeu import preparer

INFOS = {'categorie': 'tour', 'titre': "Hutte du berserker"}

def construire(ctx):
    preparer(tour(1))
