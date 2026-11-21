"""Loup-garou (palier 2, sol) — kit 2.40 : bête-loup dressée, voûtée, griffes immenses, fourrure grise hérissée, haillons."""
from communs.creatures import *
INFOS = {'categorie': 'monstre', 'titre': "Loup-garou"}

def pieces(K):
    w, p = K.j('poignet.L'), K.j('poitrine')
    return ([corne(f'Griffe{k}.{n}', OS_, f'Main.{n}', (s * w.x + s * .022 * (k - 1), w.y - .04, w.z - .09), .012, .08, .5, rot=(math.pi - .3, 0, 0), seg=4, n=2)
             for s, n in ((1, 'L'), (-1, 'R')) for k in range(3)] +
            [corne(f'Hirsute{k}', '#4a4038', 'Torse', (x, .13, p.z + .1), .035, .11, .8, rot=(-.6, x * 3, 0), seg=5, n=3) for k, x in enumerate((-.08, 0, .08))] +
            ceinture(K, col='#3a3028', boucle=None, pagne='#5a4a3a'))

def construire(ctx):
    bipede('loup_garou', dict(z=1.1, peau=('#6f6458', '#8f8478', '#4f463e'), bas='#6f6458', botte='#3a332c', tete='loup', tete_r=1.15,
                              voute=.85, jambes=.4, carrure=1.2, bras=1.25, muscle=.9, relief=RELIEF_POIL, queue=('#5a5048', .9),
                              oeil='#ffd23a', pieces=pieces))
