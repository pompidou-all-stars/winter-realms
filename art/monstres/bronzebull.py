"""Taureau d'airain (palier 2, spécial, anti-magie) — kit 2.40 : taureau de bronze forgé, plaques rivetées, cornes dorées,
feu dans les naseaux et les jointures (taureaux de Colchide de la mythologie grecque)."""
from communs.creatures import *
INFOS = {'categorie': 'monstre', 'titre': "Taureau d'airain"}

def pieces(K):
    t, m, re, ga = K.j('nuque'), K.j('museau'), K.j('reins'), K.j('garrot')
    K.lueurs += [boule(f'Naseau.{n}', '#ff8a2a', 'Tete', (s * .03, m.y + .07, m.z - .06), .02, seg=6) for s, n in ((1, 'L'), (-1, 'R'))]
    return ([corne(f'Corne.{n}', OR, 'Tete', (s * .1, t.y - .05, t.z + .06), .035, .2, 1.1, rot=(0, s * 1.5, 0)) for s, n in ((1, 'L'), (-1, 'R'))] +
            [plaque('Plastron', '#8a5a2a', 'Dos', (0, ga.y - .05, ga.z - .05), .3, .06, .28), plaque('Echine', '#8a5a2a', 'Dos', (0, (re.y + ga.y) / 2, re.z + .16), .2, .4, .03)] +
            [boule(f'Rivet{k}', OR, 'Dos', ((k % 2 - .5) * .2, ga.y - .09, ga.z - .1 + .08 * (k // 2)), .015, seg=6) for k in range(6)])

def construire(ctx):
    bete('taureau_airain', dict(z=1.1, poil=('#b07a3a', '#c8945a', '#8a5a2a'), patte='#6a4220', crete='#6a4220', tete='taureau', tete_r=1.1,
                                longueur=.95, pattes=.95, epaisseur=1.3, cou=.7, queue=.6, relief=RELIEF_PIERRE, oeil='#ff8a2a',
                                ech=1.15, duree=.5, pieces=pieces))
