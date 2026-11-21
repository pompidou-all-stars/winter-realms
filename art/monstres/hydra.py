"""Hydre (palier 3, spécial, se divise) — kit 2.40 : grand reptile vert-bleu à cinq cous et cinq têtes, crêtes, ventre clair
(mythologie grecque). Les têtes nées de la division utilisent ce modèle réduit."""
from communs.creatures import *
INFOS = {'categorie': 'monstre', 'titre': "Hydre"}
P = ('#2f7a6a', '#4a9a88', '#c8d0a0')

def vols(K):
    ga = K.j('garrot'); v = []
    for k, x in enumerate((-.2, -.1, .1, .2)):
        top = (x * 1.6, ga.y - .3, ga.z + .25 - abs(x) * .4)
        v += [seul(V('Dos', P[0], a=(x * .5, ga.y, ga.z), b=top, ra=.07, rb=.05)),
              seul(V('Dos', P[1], c=(top[0], top[1] - .07, top[2] + .02), r=(.06, .1, .05)))]
    return v

def pieces(K):
    ga = K.j('garrot')
    for k, x in enumerate((-.2, -.1, .1, .2)):
        top = (x * 1.6, ga.y - .3, ga.z + .25 - abs(x) * .4)
        for s in (1, -1): K.oeil(f'OeilH{k}{s}', 'Dos', (top[0] + s * .035, top[1] - .1, top[2] + .04), .012)
    return meches_dos(K, '#c8a83a', n=5, taille=.7, rangs=False) + griffes(K)

def construire(ctx):
    bete('hydre', dict(z=1.45, poil=P, patte='#1f5a4a', crete='#c8a83a', tete='lezard', tete_r=1.0, longueur=1.0, pattes=.85,
                       epaisseur=1.3, cou=1.1, queue=1.3, tete_z=.12, relief=RELIEF_ECAILLE, oeil='#ffe43a', ech=1.0, duree=.55,
                       volumes=vols, pieces=pieces))
