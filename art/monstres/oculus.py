"""Oculus abyssal (palier 2, volant) — kit 2.40 : grand œil flottant dans une chair violacée, paupière cornée, couronne de
tentacules pendantes, sans pédoncules (création originale inspirée des horreurs flottantes)."""
from communs.creatures import *
INFOS = {'categorie': 'monstre', 'titre': "Oculus abyssal"}
P = ('#5a3a6a', '#7a5a8a', '#3a2448')

def vols(K):
    return [V('Colonne', P[0], c=(0, 0, .6), r=(.3, .3, .3)), V('Colonne', P[2], c=(0, -.2, .74), r=(.2, .08, .06), prio=2),
            V('Colonne', '#e8e0d8', c=(0, -.24, .6), r=(.15, .07, .15), prio=3, rel=0)]

def pieces(K):
    K.oeil('Iris', 'Colonne', (0, -.31, .6), .08, col='#ffcf3a')
    return [corne(f'Tentacule{k}', P[1], 'Colonne', (math.sin(a) * .2, math.cos(a) * .2, .38), .045, .32, 1.2,
                  rot=(math.pi - .4 * math.cos(a), .4 * math.sin(a), 0), seg=6, n=5) for k, a in enumerate([i * math.pi / 3 for i in range(6)])]

def construire(ctx):
    bipede('oculus', dict(z=1.15, peau=P, bas=P[0], tete='aucune', bas_du_corps='traine', carrure=.5, bras=.4, muscle=0,
                          relief=RELIEF_PEAU, taches=.2, oeil='#ffcf3a', vol=True, volumes=vols, pieces=pieces))
