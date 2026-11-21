"""Esprit du blizzard (palier 1, volant) — kit 2.40 : spectre de glace sans jambes, longue traîne, couronne d'éclats, yeux bleus."""
from communs.creatures import *
INFOS = {'categorie': 'monstre', 'titre': "Esprit du blizzard"}

def pieces(K):
    t = K.j('tete')
    return [cone(f'Eclat{k}', '#bfe6ff', 'Tete', (math.sin(a) * .07, t.y - math.cos(a) * .07, t.z + .13), .022, .002, .1 + .03 * (k % 2),
                 rot=(-math.cos(a) * .5, math.sin(a) * .5, 0), seg=4) for k, a in enumerate((-1.2, -.6, 0, .6, 1.2))] + [
        cone(f'Givre{k}.{n}', '#dff2ff', f'AvantBras.{n}', (s * .3, .0, .42 - .05 * k), .02, .001, .08, rot=(0, s * 1.4, 0), seg=4)
        for s, n in ((1, 'L'), (-1, 'R')) for k in range(2)]

def construire(ctx):
    bipede('esprit_blizzard', dict(z=.7, peau=('#cfe8ff', '#e8f4ff', '#a8c8e8'), bas='#b8d8f0', tete='humain', bas_du_corps='traine',
                                   carrure=.8, bras=1.15, muscle=0, voute=.35, relief=RELIEF_LISSE, oeil='#5ab8ff', vol=True, pieces=pieces))
