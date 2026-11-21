"""Nains de Hautroc — Arbalète à répétition (emplacement 0 : tir de base).
Forme : communs/hautroc_hd.py (2.40, direction « grimdark » ; créatures au procédé des monstres organiques)."""
from communs.hautroc_hd import tour
from communs.export_jeu import preparer

INFOS = {'categorie': 'tour', 'titre': "Arbalète à répétition"}

def construire(ctx):
    preparer(tour(0))
