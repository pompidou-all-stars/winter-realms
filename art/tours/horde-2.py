"""Clans de l’Orage Blanc — Totem des pluies glacées (emplacement 2 : contrôle).
Forme : communs/orage_hd.py (2.40, direction « grimdark » ; créatures au procédé des monstres organiques)."""
from communs.orage_hd import tour
from communs.export_jeu import preparer

INFOS = {'categorie': 'tour', 'titre': "Totem des pluies glacées"}

def construire(ctx):
    preparer(tour(2))
