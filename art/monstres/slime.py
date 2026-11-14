"""Gelée mutante (CR slime, se divise) : grosse goutte vert acide, bulles, gros yeux. Avance en rebondissant.
Le Petit limon (petit_limon.py) en est une version réduite."""
from communs.outils import collection, dans, pivot, peindre
from communs.betes import gelee
from communs.animations import saut
from communs.echelles import hauteur
from communs.export_jeu import preparer

INFOS = {'categorie': 'monstre', 'titre': "Gelée mutante"}

def fabriquer(nom='gelee_mutante', cle='gelee'):
    c = collection(nom); dans(c)
    r = pivot(nom); H = hauteur(cle)
    gelee(r, H)
    peindre(r, sol=.8)
    saut(r, duree=.7, ecrase=.18, hauteur=H * .15)
    return r

def construire(ctx):
    preparer(fabriquer())
