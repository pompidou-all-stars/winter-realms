"""Cour des Ossements — Perchoir des gargouilles (emplacement 4 : anti-aérien).
Forme : communs/ossements_hd.py (2.40, direction « grimdark » ; créatures au procédé des monstres organiques)."""
from communs.ossements_hd import tour
from communs.export_jeu import preparer

INFOS = {'categorie': 'tour', 'titre': "Perchoir des gargouilles"}

def construire(ctx):
    preparer(tour(4))
