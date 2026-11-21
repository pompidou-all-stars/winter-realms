"""Chimère (palier 3, sol) — kit 2.40 : lion fauve à crinière, tête de bouc cornue sur le dos, queue terminée en serpent
(mythologie grecque)."""
from communs.creatures import *
INFOS = {'categorie': 'monstre', 'titre': "Chimère"}

def vols(K):
    nu, ga = K.j('nuque'), K.j('garrot')
    return [V('Cou', '#8a5a2a', c=(0, nu.y + .06, nu.z - .02), r=(.15, .1, .15), prio=1),                 # crinière
            V('Dos', '#c8c0b0', a=(0, ga.y + .15, ga.z + .1), b=(.05, ga.y + .1, ga.z + .3), ra=.06, rb=.055),  # cou du bouc
            V('Dos', '#c8c0b0', c=(.06, ga.y + .04, ga.z + .36), r=(.085, .11, .08))]

def pieces(K):
    ga, q2 = K.j('garrot'), K.j('queue2')
    K.oeil('OeilBouc', 'Dos', (.09, ga.y + .0, ga.z + .36), .014)
    K.oeil('OeilSerpent', 'Queue2', (q2.x + .02, q2.y + .02, q2.z + .03), .012, col='#7aff5a')
    return ([corne(f'CorneBouc.{n}', '#3a3330', 'Dos', (.06 + s * .03, ga.y + .08, ga.z + .4), .02, .14, 2.0, rot=(-.8, s * .4, 0), n=5) for s, n in ((1, 'L'), (-1, 'R'))] +
            [boule('TeteSerpent', '#3a8a3a', 'Queue2', tuple(q2), .05, ech=(1, 1.6, .8), seg=8)] + griffes(K))

def construire(ctx):
    bete('chimere', dict(z=1.5, poil=('#d9a441', '#e8c070', '#f0dcb0'), patte='#a87a2a', crete='#3a8a3a', tete='felin', tete_r=1.45,
                         longueur=1.0, pattes=1.05, epaisseur=1.2, cou=.95, queue=1.2, relief=RELIEF_POIL, oeil='#ffcf3a', ech=1.0,
                         duree=.45, volumes=vols, pieces=pieces))
