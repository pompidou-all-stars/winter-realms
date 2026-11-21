"""Spectre des glaces (palier 1, spécial, invisible) — kit 2.40 : spectre encapuchonné, longue traîne, cape en lambeaux, longues griffes
de glace, éclats de givre en couronne, yeux bleus."""
from communs.creatures import *
INFOS = {'categorie': 'monstre', 'titre': "Spectre des glaces"}

def pieces(K):
    w, t = K.j('poignet.L'), K.j('tete')
    K.lueurs += [cone(f'Givre{k}', '#bfe6ff', 'Tete', (x, t.y + .02, t.z + .1), .018, .001, .09, rot=(0, x * 4, 0), seg=4)
                 for k, x in enumerate((-.06, 0, .06))]
    return casque(K, 'capuche', col='#2a3a5a') + cape(K, col='#3a4a6a', longueur=.9) + [
        corne(f'Griffe{k}.{n}', '#dff2ff', f'Main.{n}', (s * w.x + s * .02 * (k - 1), w.y - .03, w.z - .08), .012, .1, .5, rot=(math.pi, 0, 0), seg=4, n=2)
        for s, n in ((1, 'L'), (-1, 'R')) for k in range(3)]

def construire(ctx):
    bipede('spectre', dict(z=1.0, peau=('#9fb8d8', '#c8d8f0', '#7890b0'), bas='#3a4a6a', tete='crane', bas_du_corps='traine',
                           carrure=.95, bras=1.3, muscle=0, voute=.55, relief=RELIEF_LISSE, oeil='#5ab8ff', pieces=pieces))
