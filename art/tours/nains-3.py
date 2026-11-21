"""Nains de Hautroc — Mortier runique (emplacement 3 : zone).
Forme : communs/hautroc_hd.py (2.40, direction « grimdark » ; créatures au procédé des monstres organiques)."""
from communs.hautroc_hd import tour
from communs.export_jeu import preparer

INFOS = {'categorie': 'tour', 'titre': "Mortier runique"}

def construire(ctx):
    preparer(tour(3))
