"""Titan déchu (palier 3, sol) — kit 2.40 : géant de marbre fissuré aux veines d'or, couronne brisée, chaînes rompues aux poignets,
grande épée (mythologie grecque)."""
from communs.creatures import *
INFOS = {'categorie': 'monstre', 'titre': "Titan déchu"}

def pieces(K):
    p, w = K.j('poitrine'), K.j('poignet.L')
    K.lueurs += [plaque(f'Veine{k}', '#ffd23a', 'Torse', (x, -.17, p.z + z), .07, .01, .01, rot=(0, 0, a)) for k, (x, z, a) in enumerate(((-.07, .05, .7), (.08, -.02, -.6), (0, -.1, .1)))]
    return (casque(K, 'couronne', col=OR) + arme(K, 'epee', taille=1.5, col='#e8e0d0') +
            [tore(f'Menotte.{n}', FER, f'AvantBras.{n}', (s * w.x, w.y, w.z + .05), .06, .015, seg=10, seg2=4) for s, n in ((1, 'L'), (-1, 'R'))] +
            [corne(f'Chaine{n}', FER, f'AvantBras.{n}', (s * w.x, w.y, w.z + .02), .012, .12, .4, rot=(math.pi, 0, 0), seg=4, n=3) for s, n in ((1, 'L'), (-1, 'R'))] +
            cape(K, col='#e8e0d0', longueur=.9) + ceinture(K, col=OR, boucle=OR, pagne='#e8e0d0'))

def construire(ctx):
    bipede('titan', dict(z=1.65, peau=('#d0c8bc', '#f2ece2', '#9a9286'), bas='#c8c2b8', botte='#a8a298', tete='humain', tete_r=.85,
                         carrure=1.4, jambes=.44, muscle=1.4, voute=.2, relief=RELIEF_ROC, ecailles=3, oeil='#ffd23a', lourd=1.3, pieces=pieces))
