"""Cour des Ossements — Colosse d’os (emplacement 9 : ultime).
Forme : communs/ossements_hd.py (2.40, direction « grimdark » ; créatures au procédé des monstres organiques)."""
from communs.ossements_hd import tour
from communs.export_jeu import preparer

INFOS = {'categorie': 'tour', 'titre': "Colosse d’os"}

def construire(ctx):
    preparer(tour(9))
