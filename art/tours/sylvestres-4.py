"""Elfes de Lunebois — Nid des chouettes des neiges (emplacement 4 : anti-aérien).
Forme : communs/lunebois_hd.py (2.40, direction « grimdark » ; créatures au procédé des monstres organiques)."""
from communs.lunebois_hd import tour
from communs.export_jeu import preparer

INFOS = {'categorie': 'tour', 'titre': "Nid des chouettes des neiges"}

def construire(ctx):
    preparer(tour(4))
