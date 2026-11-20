"""Cour des Ossements — Nécromancien (emplacement 6 : signature).
Forme : communs/ossements_hd.py (2.40, direction « grimdark » ; créatures au procédé des monstres organiques)."""
from communs.ossements_hd import tour
from communs.export_jeu import preparer

INFOS = {'categorie': 'tour', 'titre': "Nécromancien"}

def construire(ctx):
    preparer(tour(6))
