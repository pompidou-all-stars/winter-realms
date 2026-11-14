"""Portail d'apparition (forme dans communs/decor.py)."""
from communs.decor import portail
from communs.export_jeu import preparer

INFOS = {'categorie': 'decor', 'titre': "Portail d'apparition"}

def construire(ctx):
    preparer(portail())
