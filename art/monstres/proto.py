"""Protoplasme aux mille yeux (palier 2, spécial, se divise) — kit 2.40 : masse informe noir-vert couverte d'yeux et de bouches,
pseudopodes (création originale inspirée de Lovecraft). Les blobs nés de la division utilisent ce modèle réduit."""
from communs.creatures import *
INFOS = {'categorie': 'monstre', 'titre': "Protoplasme aux mille yeux"}
P = ('#2a3a2a', '#3a5a3a', '#1a2a1a')

def vols(K):
    return [V('Hanches', P[0], c=(0, 0, .28), r=(.38, .36, .28)), V('Colonne', P[1], c=(.05, -.03, .52), r=(.27, .25, .2)),
            V('Torse', P[1], c=(-.06, .02, .7), r=(.16, .15, .12)), seul(V('Colonne', P[0], c=(.25, .05, .4), r=(.12, .12, .12)))] + [
        V('Colonne', '#6a1a2a', c=(x, -.27, z), r=(.06, .02, .02), prio=3, rel=0) for x, z in ((.1, .4), (-.12, .55))]

def pieces(K):
    for k, (x, y, z, r) in enumerate(((.0, -.28, .55, .05), (.15, -.25, .45, .035), (-.14, -.24, .62, .04), (.2, -.12, .66, .03),
                                      (-.22, -.15, .38, .035), (.05, -.2, .78, .03), (.25, .05, .5, .03), (-.08, -.3, .32, .03))):
        K.oeil(f'Oeil{k}', 'Colonne', (x, y, z), r)
    return []

def construire(ctx):
    bipede('protoplasme', dict(z=1.15, peau=P, bas=P[2], tete='aucune', bas_du_corps='robe', carrure=.6, bras=.6, muscle=0, jambes=.3,
                               relief=RELIEF_PEAU, taches=.3, oeil='#e8ff5a', lourd=1.6, masse=True, volumes=vols, pieces=pieces))
