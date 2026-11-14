"""Gelée mutante (CR slime, se divise) : grosse goutte vert acide, bulles, gros yeux. Avance en rebondissant.
Le Petit limon (petit_limon.py) en est une version réduite."""
from outils import collection, dans, pivot, peindre
from betes import gelee
from animations import saut
from echelles import hauteur

def fabriquer(nom='gelee_mutante', cle='gelee'):
    c = collection(nom); dans(c)
    r = pivot(nom); H = hauteur(cle)
    gelee(r, H)
    peindre(r, sol=.8)
    saut(r, duree=.7, ecrase=.18, hauteur=H * .15)
    return r

if __name__ == '__main__': fabriquer()
