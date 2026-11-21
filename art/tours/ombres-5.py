"""Cour des Ossements — Œil du Voile (emplacement 5 : détection).
Forme : communs/ossements_hd.py (2.40, direction « grimdark » ; créatures au procédé des monstres organiques)."""
from communs.ossements_hd import tour
from communs.export_jeu import preparer

INFOS = {'categorie': 'tour', 'titre': "Œil du Voile"}

def construire(ctx):
    preparer(tour(5))
