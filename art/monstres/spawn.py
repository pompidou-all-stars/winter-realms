"""Rejeton difforme (palier 2, sol) — kit 2.40 : masse mutante des Ruines, chair violacée, bras inégaux, tentacules, cornes,
yeux en trop, gueule béante (notre version des rejetons du Chaos)."""
from communs.creatures import *
INFOS = {'categorie': 'monstre', 'titre': "Rejeton difforme"}
P = ('#8a4a6a', '#a86a88', '#6a3050')

def vols(K):
    p, w = K.j('poitrine'), K.j('poignet.L')
    return [V('Colonne', P[0], c=(0, -.05, .45), r=(.26, .24, .2)), seul(V('Main.L', P[1], c=(w.x + .02, w.y, w.z - .05), r=(.12, .12, .12))),
            seul(V('Torse', P[2], c=(.12, -.1, p.z + .08), r=(.07, .06, .06))), V('Colonne', '#4a1a2a', c=(0, -.24, .5), r=(.1, .03, .05), prio=3, rel=0)]

def pieces(K):
    p = K.j('poitrine')
    for k, (x, z) in enumerate(((.1, .05), (-.06, .12), (.15, -.05))):
        K.oeil(f'OeilX{k}', 'Torse', (x, -.17, p.z + z), .02)
    return cornes(K, col='#e8dcc0', taille=.9, forme='droites') + [
        corne(f'Tentacule{k}', P[1], 'Torse', (x, .1, p.z), .04, .25, 1.5, rot=(-1.0, x * 4, 0), seg=6, n=5) for k, x in enumerate((-.12, .0, .12))]

def construire(ctx):
    bipede('rejeton', dict(z=1.2, peau=P, bas=P[2], botte=P[2], tete='demon', tete_r=.8, voute=.9, jambes=.3, carrure=1.3, ventre=1.3,
                           muscle=.6, relief=RELIEF_PEAU, taches=.25, oeil='#e8ff3a', lourd=1.4, volumes=vols, pieces=pieces))
