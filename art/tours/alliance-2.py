"""Alliance — Obélisque de givre (emplacement 2 : Givre · contrôle).
Forme : archétype de communs/tours_communes.py dans le style de la faction (STYLE['alliance']).
Pour personnaliser cette tour seule, remplacer l'appel à tour() par sa propre construction."""
from communs.tours_communes import tour
from communs.export_jeu import preparer

INFOS = {'categorie': 'tour', 'titre': "Obélisque de givre"}

def construire(ctx):
    preparer(tour('alliance', 2))
