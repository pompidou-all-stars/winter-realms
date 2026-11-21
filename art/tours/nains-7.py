"""Nains de Hautroc — Enclume runique (emplacement 7 : soutien).
Forme : communs/hautroc_hd.py (2.40, direction « grimdark » ; créatures au procédé des monstres organiques)."""
from communs.hautroc_hd import tour
from communs.export_jeu import preparer

INFOS = {'categorie': 'tour', 'titre': "Enclume runique"}

def construire(ctx):
    preparer(tour(7))
