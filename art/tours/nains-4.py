"""Nains de Hautroc — Canon antiaérien à éclats (emplacement 4 : anti-aérien).
Forme : communs/hautroc_hd.py (2.40, direction « grimdark » ; créatures au procédé des monstres organiques)."""
from communs.hautroc_hd import tour
from communs.export_jeu import preparer

INFOS = {'categorie': 'tour', 'titre': "Canon antiaérien à éclats"}

def construire(ctx):
    preparer(tour(4))
