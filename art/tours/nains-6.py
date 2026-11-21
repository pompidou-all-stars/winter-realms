"""Nains de Hautroc — Gueule de forge (emplacement 6 : signature).
Forme : communs/hautroc_hd.py (2.40, direction « grimdark » ; créatures au procédé des monstres organiques)."""
from communs.hautroc_hd import tour
from communs.export_jeu import preparer

INFOS = {'categorie': 'tour', 'titre': "Gueule de forge"}

def construire(ctx):
    preparer(tour(6))
