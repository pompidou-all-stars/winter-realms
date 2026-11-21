"""Canon-foudre des hommes-rats (palier 1, spécial, étourdit) — kit 2.40 : homme-rat artilleur portant un canon à foudre,
cristal vert lumineux et réservoir sur le dos."""
from communs.creatures import *
INFOS = {'categorie': 'monstre', 'titre': "Canon-foudre des hommes-rats"}

def pieces(K):
    p, w = K.j('poitrine'), K.j('poignet.L')
    K.lueurs += [boule('Cristal', '#7aff5a', 'Torse', (0, .2, p.z + .12), .05, ech=(1, 1, 1.6), seg=6),
                 boule('Bouche', '#7aff5a', 'Main.R', (-w.x, w.y - .3, w.z + .02), .03, seg=6)]
    return [cone('Canon', '#5a4a3a', 'Main.R', (-w.x, w.y + .05, w.z), .045, .035, .35, rot=(1.5, 0, 0), seg=10),
            tore('Cerclage', '#c8a040', 'Main.R', (-w.x, w.y - .12, w.z), .045, .01, rot=(1.5, 0, 0), seg=10, seg2=3),
            plaque('Reservoir', '#4a4038', 'Torse', (0, .16, p.z), .16, .1, .2),
            cone('Tuyau', '#7a6a5a', 'Torse', (.1, .12, p.z - .05), .015, .015, .2, rot=(1.2, .3, 0), seg=6)] + casque(K, 'capuche', col='#3a3028')

def construire(ctx):
    bipede('canon_foudre', dict(z=.95, peau=('#6a5a4a', '#8a7a68', '#4a3e32'), bas='#4a3a2e', botte='#6a5a4a', tete='rat', tete_r=1.05,
                                voute=.75, jambes=.36, carrure=.9, muscle=.4, queue=('#c8958a', 1.2), relief=RELIEF_POIL, oeil='#7aff5a',
                                pieces=pieces))
