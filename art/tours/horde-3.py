"""Clans de l’Orage Blanc — Catapulte à rochers (emplacement 3 : zone).
Forme : communs/orage_hd.py (2.40, direction « grimdark » ; créatures au procédé des monstres organiques)."""
from communs.orage_hd import tour
from communs.export_jeu import preparer

INFOS = {'categorie': 'tour', 'titre': "Catapulte à rochers"}

def construire(ctx):
    preparer(tour(3))
