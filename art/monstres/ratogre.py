"""Ogre-rat mutant (palier 2, sol) — kit 2.40 : rat géant gonflé de muscles, cicatrices, chaînes, bras griffus, cristal vert planté dans le dos."""
from communs.creatures import *
INFOS = {'categorie': 'monstre', 'titre': "Ogre-rat mutant"}

def pieces(K):
    p, w = K.j('poitrine'), K.j('poignet.L')
    K.lueurs += [cone(f'Cristal{k}', '#7aff5a', 'Torse', (x, .15, p.z + .1), .035, .002, .14, rot=(-.5, x * 3, 0), seg=5) for k, x in enumerate((-.06, .05))]
    return ([corne(f'Griffe{k}.{n}', OS_, f'Main.{n}', (s * w.x + s * .022 * (k - 1), w.y - .04, w.z - .09), .013, .08, .5, rot=(math.pi - .3, 0, 0), seg=4, n=2)
             for s, n in ((1, 'L'), (-1, 'R')) for k in range(3)] +
            [tore('Chaine', FER, 'Torse', (0, 0, p.z), .2, .012, rot=(0, .7, 0), seg=14, seg2=4)] + brassards(K, col=FER, pointes=FER))

def construire(ctx):
    bipede('ogre_rat', dict(z=1.15, peau=('#8a7a6a', '#a8988a', '#6a5a4e'), bas='#5a4a3a', botte='#8a7a6a', tete='rat', tete_r=.85,
                            voute=.8, jambes=.36, carrure=1.45, bras=1.3, muscle=1.4, queue=('#d8a59a', 1.2), relief=RELIEF_POIL,
                            oeil='#7aff5a', lourd=1.3, pieces=pieces))
