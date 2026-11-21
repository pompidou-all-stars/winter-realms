"""Géant des tempêtes (palier 3, spécial, étourdit) — kit 2.40 : géant à peau bleu-gris, barbe d'orage, armure de bronze,
lance-trident, éclairs bleus dans les yeux et sur les bras."""
from communs.creatures import *
INFOS = {'categorie': 'monstre', 'titre': "Géant des tempêtes"}

def vols(K):
    t = K.j('tete')
    return [V('Tete', '#c8d8e8', a=(0, t.y - .1, t.z + .02), b=(0, t.y - .13, t.z - .16), ra=.075, rb=.03, prio=2)]

def pieces(K):
    e = K.j('epaule.L')
    K.lueurs += [plaque(f'Eclair{k}.{n}', '#7fd8ff', f'Bras.{n}', (s * (e.x + .05), e.y - .07, e.z - .08 - .06 * k), .012, .01, .06, rot=(0, 0, .6 * (k % 2 * 2 - 1)))
                 for s, n in ((1, 'L'), (-1, 'R')) for k in range(2)]
    return (casque(K, 'cornu', col='#b07a3a', col2='#e8dcc0') + epaulieres(K, col='#b07a3a', taille=1.2, pointes=0, bord=OR) +
            arme(K, 'lance', taille=1.4, col='#7fd8ff', manche='#5a4a3a') + ceinture(K, col='#b07a3a', boucle=OR, pagne='#3a5a8a') +
            brassards(K, col='#b07a3a') + cape(K, col='#3a5a8a', longueur=1.0))

def construire(ctx):
    bipede('geant_tempetes', dict(z=1.45, peau=('#7a8aa0', '#98a8bc', '#5a6a80'), bas='#3a5a8a', botte='#5a4a3a', tete='humain', tete_r=.9,
                                  carrure=1.35, jambes=.44, muscle=1.1, voute=.2, oeil='#7fd8ff', lourd=1.2, volumes=vols, pieces=pieces))
