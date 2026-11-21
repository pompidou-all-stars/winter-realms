"""Clans de l’Orage Blanc — Aire des aigles-tempête (emplacement 4 : anti-aérien).
Forme : communs/orage_hd.py (2.40, direction « grimdark » ; créatures au procédé des monstres organiques)."""
from communs.orage_hd import tour
from communs.export_jeu import preparer

INFOS = {'categorie': 'tour', 'titre': "Aire des aigles-tempête"}

def construire(ctx):
    preparer(tour(4))
