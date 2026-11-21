"""Colosse d'os relevé : mort relevé par la Cour des Ossements, qui marche sur le chemin (2.40, communs/ossements_hd.py)."""
from communs.ossements_hd import mort_releve
from communs.export_jeu import preparer

INFOS = {'categorie': 'decor', 'titre': "Colosse d'os relevé"}

def construire(ctx):
    preparer(mort_releve(colosse=True))
