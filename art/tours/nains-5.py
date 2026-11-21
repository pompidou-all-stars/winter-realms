"""Nains de Hautroc — Phare runique (emplacement 5 : détection).
Forme : communs/hautroc_hd.py (2.40, direction « grimdark » ; créatures au procédé des monstres organiques)."""
from communs.hautroc_hd import tour
from communs.export_jeu import preparer

INFOS = {'categorie': 'tour', 'titre': "Phare runique"}

def construire(ctx):
    preparer(tour(5))
