"""Cour des Ossements — Faucheuse (emplacement 8 : anti-boss).
Forme : communs/ossements_hd.py (2.40, direction « grimdark » ; créatures au procédé des monstres organiques)."""
from communs.ossements_hd import tour
from communs.export_jeu import preparer

INFOS = {'categorie': 'tour', 'titre': "Faucheuse"}

def construire(ctx):
    preparer(tour(8))
