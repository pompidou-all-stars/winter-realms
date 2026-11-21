"""Vouivre (palier 2, volant) — kit 2.40 : petit dragon vert à deux pattes, ailes membraneuses, crête, longue queue à dard."""
from communs.creatures import *
INFOS = {'categorie': 'monstre', 'titre': "Vouivre"}

def pieces(K):
    q2, nu = K.j('queue2'), K.j('nuque')
    return ([cone('Dard', '#e8d8a0', 'Queue2', tuple(q2), .03, .001, .1, rot=(-math.pi / 2, 0, 0), seg=5)] +
            [corne(f'Crete{k}', '#c8a83a', 'Cou', (0, nu.y + .05 + .05 * k, nu.z + .05 - .02 * k), .02, .07, .6, rot=(-.5, 0, 0), seg=4, n=2) for k in range(3)])

def construire(ctx):
    volant('vouivre', dict(z=1.0, corps=('#3fa060', '#5ab878', '#c8d88a'), aile=('#2f7a48', '#4f9a68'), tete='dragon', envergure=1.05,
                           cou=1.1, queue=1.3, relief=RELIEF_ECAILLE, oeil='#ffcf3a', pieces=pieces))
