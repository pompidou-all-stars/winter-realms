"""Ours de guerre (palier 1, sol) — kit 2.40 : ours brun massif, chanfrein et barde de fer, piques sur le dos, griffes."""
from communs.creatures import *
INFOS = {'categorie': 'monstre', 'titre': "Ours de guerre"}

def pieces(K):
    nu, re, ga = K.j('nuque'), K.j('reins'), K.j('garrot')
    return griffes(K) + [plaque('Chanfrein', FER, 'Tete', (0, nu.y - .12, nu.z + .06), .12, .14, .02, rot=(.5, 0, 0)),
                         plaque('Barde', FER, 'Dos', (0, (re.y + ga.y) / 2, re.z + .16), .3, .36, .03, rot=(-.08, 0, 0))] + [
        cone(f'Pique{k}', FER2, 'Dos', (0, ga.y + .1 * k, ga.z + .18 - .02 * k), .025, .002, .09, seg=5) for k in range(4)]

def construire(ctx):
    bete('ours', dict(z=1.0, poil=('#6a4630', '#8a6448', '#9a7a58'), patte='#3a2618', crete='#4a2e1e', tete='ours', tete_r=1.1,
                      longueur=.85, pattes=.9, epaisseur=1.35, cou=.7, queue=.15, oeil='#ffb03a', ech=1.1, pieces=pieces, duree=.55))
