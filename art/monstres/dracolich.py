"""Dracoliche (palier 3, volant) — kit 2.40 : dragon mort-vivant, os blanchis, ailes déchirées gris-violet, crâne à cornes,
lueur verte dans les orbites et la cage thoracique."""
from communs.creatures import *
INFOS = {'categorie': 'monstre', 'titre': "Dracoliche"}

def pieces(K):
    nu, po = K.j('nuque'), K.j('poitrine')
    K.lueurs.append(boule('Coeur', '#7aff8a', 'Hanches', (0, po.y + .05, po.z - .02), .05, seg=8))
    return ([corne(f'Corne.{n}', '#d0ccbc', 'Tete', (s * .04, nu.y - .03, nu.z + .06), .02, .16, .8, rot=(-1.2, s * .3, 0), seg=5, n=3) for s, n in ((1, 'L'), (-1, 'R'))] +
            [corne(f'Cote{k}.{n}', '#e6e2d2', 'Hanches', (s * .05, po.y + .04 * k, po.z + .06), .012, .14, 1.4, rot=(0, s * 1.6, 0), seg=4, n=3)
             for s, n in ((1, 'L'), (-1, 'R')) for k in range(3)])

def construire(ctx):
    volant('dracoliche', dict(z=1.45, corps=('#d0ccbc', '#e6e2d2', '#5a4a6a'), aile=('#b8b4a4', '#5a4a6a'), tete='crane', tete_r=1.15,
                              envergure=1.2, cou=1.2, queue=1.3, epaisseur=.85, relief=RELIEF_PIERRE, oeil='#7aff8a', pieces=pieces))
