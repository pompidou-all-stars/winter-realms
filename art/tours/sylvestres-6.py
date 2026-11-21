"""Elfes de Lunebois — Cercle de Floraison (emplacement 6 : signature).
Forme : communs/lunebois_hd.py (2.40, direction « grimdark » ; créatures au procédé des monstres organiques)."""
from communs.lunebois_hd import tour
from communs.export_jeu import preparer

INFOS = {'categorie': 'tour', 'titre': "Cercle de Floraison"}

def construire(ctx):
    preparer(tour(6))
