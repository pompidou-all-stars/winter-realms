"""Cour des Ossements — Obélisque de malédiction (emplacement 2 : contrôle).
Forme : communs/ossements_hd.py (2.40, direction « grimdark » ; créatures au procédé des monstres organiques)."""
from communs.ossements_hd import tour
from communs.export_jeu import preparer

INFOS = {'categorie': 'tour', 'titre': "Obélisque de malédiction"}

def construire(ctx):
    preparer(tour(2))
