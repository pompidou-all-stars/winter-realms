"""Dragon ancien (palier 3, volant) — kit 2.40 : grand dragon rouge à ventre doré, cornes en arrière, crête, grandes ailes membraneuses."""
from communs.creatures import *
INFOS = {'categorie': 'monstre', 'titre': "Dragon ancien"}

def pieces(K):
    nu, q2 = K.j('nuque'), K.j('queue2')
    return ([corne(f'Corne.{n}', '#e8dcc0', 'Tete', (s * .04, nu.y - .03, nu.z + .06), .02, .14, .8, rot=(-1.2, s * .3, 0), seg=5, n=3) for s, n in ((1, 'L'), (-1, 'R'))] +
            [corne(f'Crete{k}', '#e8b23a', 'Cou' if k < 2 else 'Hanches', (0, nu.y + .08 + .1 * k, nu.z - .02 * k), .025, .08, .6, rot=(-.5, 0, 0), seg=4, n=2) for k in range(4)] +
            [profil('Fer_queue', '#e8b23a', 'Queue2', [(0, 0), (.06, -.04), (0, .1), (-.06, -.04)], .01, pos=tuple(q2), rot=(math.pi / 2, 0, 0))])

def construire(ctx):
    volant('dragon', dict(z=1.3, corps=('#d6453d', '#e86a5a', '#e8c070'), aile=('#8a2a24', '#c8463a'), tete='dragon', tete_r=1.15,
                          envergure=1.15, cou=1.2, queue=1.3, epaisseur=1.25, relief=RELIEF_ECAILLE, oeil='#ffcf3a', pieces=pieces))
