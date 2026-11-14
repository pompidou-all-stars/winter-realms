"""Château de sortie (forme dans communs/decor.py)."""
from communs.decor import chateau
from communs.export_jeu import preparer

INFOS = {'categorie': 'decor', 'titre': "Château de sortie"}

def construire(ctx):
    preparer(chateau())
