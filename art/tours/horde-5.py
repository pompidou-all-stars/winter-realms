"""Clans de l’Orage Blanc — Hutte du chaman des esprits (emplacement 5 : détection).
Forme : communs/orage_hd.py (2.40, direction « grimdark » ; créatures au procédé des monstres organiques)."""
from communs.orage_hd import tour
from communs.export_jeu import preparer

INFOS = {'categorie': 'tour', 'titre': "Hutte du chaman des esprits"}

def construire(ctx):
    preparer(tour(5))
