"""Wendigo (palier 2, sol) — kit 2.40 : créature décharnée et très grande, crâne de cerf, bois immenses, longs bras griffus."""
from communs.creatures import *
INFOS = {'categorie': 'monstre', 'titre': "Wendigo"}

def pieces(K):
    t, w = K.j('tete'), K.j('poignet.L'); out = []
    for s, n in ((1, 'L'), (-1, 'R')):
        out.append(corne(f'Bois.{n}', '#d8ccb0', 'Tete', (s * .05, t.y, t.z + .14), .02, .25, .6, rot=(-.4, s * .7, 0), seg=5, n=4))
        for k in range(2):
            out.append(corne(f'Andouiller{k}.{n}', '#d8ccb0', 'Tete', (s * (.1 + .05 * k), t.y + .02, t.z + .22 + .05 * k), .013, .1, .5, rot=(-.2, s * 1.2, 0), seg=4, n=2))
        for k in range(3):
            out.append(corne(f'Griffe{k}.{n}', '#2a2420', f'Main.{n}', (s * w.x + s * .02 * (k - 1), w.y - .04, w.z - .1), .01, .1, .4, rot=(math.pi - .2, 0, 0), seg=4, n=2))
    return out

def construire(ctx):
    bipede('wendigo', dict(z=1.25, peau=('#3a3330', '#5a504a', '#2a2420'), bas='#3a3330', botte='#2a2420', tete='crane', tete_r=1.0,
                           carrure=.85, bras=1.45, jambes=.46, muscle=.2, ventre=.7, voute=.75, relief=RELIEF_POIL, oeil='#7affd8',
                           pieces=pieces))
