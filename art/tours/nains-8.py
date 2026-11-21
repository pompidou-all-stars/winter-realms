"""Nains de Hautroc — Champ de mines (emplacement 8 : anti-boss).
Forme : communs/hautroc_hd.py (2.40, direction « grimdark » ; créatures au procédé des monstres organiques)."""
from communs.hautroc_hd import tour
from communs.export_jeu import preparer

INFOS = {'categorie': 'tour', 'titre': "Champ de mines"}

def construire(ctx):
    preparer(tour(8))
