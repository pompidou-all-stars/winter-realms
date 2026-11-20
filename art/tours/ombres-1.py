"""Cour des Ossements — Ossuaire (emplacement 1 : corps à corps).
Forme : communs/ossements_hd.py (2.40, direction « grimdark » ; créatures au procédé des monstres organiques)."""
from communs.ossements_hd import tour
from communs.export_jeu import preparer

INFOS = {'categorie': 'tour', 'titre': "Ossuaire"}

def construire(ctx):
    preparer(tour(1))
