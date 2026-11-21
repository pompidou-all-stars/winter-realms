"""Nains de Hautroc — Marteau-pilon (emplacement 1 : corps à corps).
Forme : communs/hautroc_hd.py (2.40, direction « grimdark » ; créatures au procédé des monstres organiques)."""
from communs.hautroc_hd import tour
from communs.export_jeu import preparer

INFOS = {'categorie': 'tour', 'titre': "Marteau-pilon"}

def construire(ctx):
    preparer(tour(1))
