"""Clans de l’Orage Blanc — Lanceurs de haches (emplacement 0 : tir de base).
Forme : communs/orage_hd.py (2.40, direction « grimdark » ; créatures au procédé des monstres organiques)."""
from communs.orage_hd import tour
from communs.export_jeu import preparer

INFOS = {'categorie': 'tour', 'titre': "Lanceurs de haches"}

def construire(ctx):
    preparer(tour(0))
