"""Yéti (palier 1, sol) — kit 2.40 : grand singe des neiges à longs bras, fourrure blanche, cornes courtes, éclats de glace."""
from communs.creatures import *
INFOS = {'categorie': 'monstre', 'titre': "Yéti"}

def pieces(K):
    p = K.j('poitrine')
    return cornes(K, col='#b8c4d0', taille=.7, forme='belier') + [
        cone(f'Glace{k}', '#bfe6ff', 'Torse', (x, .12, p.z + .1 + .02 * k), .03, .002, .12 + .03 * (k % 2), rot=(-.5, x * 2, 0), seg=5)
        for k, x in enumerate((-.1, -.04, .03, .09))]

def construire(ctx):
    bipede('yeti', dict(z=1.0, peau=('#e8eef5', '#cfd8e2', '#9fb0c4'), bas='#dfe7ef', botte='#c8d2de', tete='orc', tete_r=.95,
                        carrure=1.35, bras=1.3, voute=.75, jambes=.32, muscle=.6, ventre=1.1, relief=RELIEF_POIL, oeil='#7fd8ff',
                        pieces=pieces))
