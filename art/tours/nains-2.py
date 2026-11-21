"""Nains de Hautroc — Baliste perce-plaque (emplacement 2 : contrôle).
Forme : communs/hautroc_hd.py (2.40, direction « grimdark » ; créatures au procédé des monstres organiques)."""
from communs.hautroc_hd import tour
from communs.export_jeu import preparer

INFOS = {'categorie': 'tour', 'titre': "Baliste perce-plaque"}

def construire(ctx):
    preparer(tour(2))
