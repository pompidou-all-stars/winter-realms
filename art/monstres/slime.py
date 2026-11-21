"""Gelée ocre (palier 1, spécial, se divise) — kit 2.40 : grosse gelée ocre tremblotante, pseudopodes, os et crânes à moitié dissous.
Les fragments nés de la division utilisent ce même modèle, réduit par le jeu."""
from communs.creatures import *
INFOS = {'categorie': 'monstre', 'titre': "Gelée ocre"}
P = ('#c8962a', '#e0b04a', '#a07020')

def vols(K):
    return [V('Hanches', P[0], c=(0, 0, .2), r=(.42, .4, .2)), V('Colonne', P[1], c=(0, -.03, .36), r=(.3, .28, .17)),
            V('Torse', P[1], c=(.02, -.04, .5), r=(.17, .16, .1)), seul(V('Hanches', P[1], c=(.3, -.1, .12), r=(.12, .12, .1)))]

def pieces(K):
    for s, n in ((1, 'L'), (-1, 'R')): K.oeil(f'Oeil.{n}', 'Colonne', (s * .08, -.29, .42), .04)
    return [boule('Crane', OS_, 'Hanches', (.12, -.2, .3), .06, seg=8), boule('Os', OS_, 'Hanches', (-.15, -.15, .2), .03, ech=(3, 1, 1), seg=6)] + [
        boule(f'Bulle{k}', '#f0d07a', 'Colonne', (x, y, z), .035, seg=6) for k, (x, y, z) in enumerate(((.25, -.1, .35), (-.2, -.05, .45), (.05, .2, .55)))]

def construire(ctx):
    bipede('gelee', dict(z=.95, peau=P, bas=P[2], tete='aucune', bas_du_corps='robe', carrure=.6, bras=.6, muscle=0, jambes=.3,
                         relief=RELIEF_LISSE, taches=.25, oeil='#fff07a', lourd=1.5, masse=True, volumes=vols, pieces=pieces))
