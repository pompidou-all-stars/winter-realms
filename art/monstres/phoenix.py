"""Phénix de givre (palier 3, volant) — kit 2.40 : grand oiseau de glace bleu pâle, ailes de plumes cristallines, longue queue
en éventail, aigrette lumineuse."""
from communs.creatures import *
INFOS = {'categorie': 'monstre', 'titre': "Phénix de givre"}

def pieces(K):
    nu, q1 = K.j('nuque'), K.j('queue1')
    K.lueurs += [cone(f'Aigrette{k}', '#9fdcff', 'Tete', (x, nu.y - .02, nu.z + .07), .015, .002, .12, rot=(-.6, x * 4, 0), seg=4) for k, x in enumerate((-.03, 0, .03))]
    return [profil(f'Queue{k}', '#cfeaff' if k % 2 else '#7fc8f0', 'Queue1', [(-.03, 0), (.03, 0), (.02, -.4), (0, -.45), (-.02, -.4)], .01,
                   pos=(.0, q1.y, q1.z), rot=(math.pi / 2 - .2, 0, (k - 2) * .25)) for k in range(5)]

def construire(ctx):
    volant('phenix', dict(z=1.3, corps=('#9fdcff', '#cfeaff', '#e8f6ff'), aile=('#e8f6ff', '#7fc8f0'), forme='plumes', tete='bec',
                          bec='#5ab8ff', envergure=1.15, queue=.6, relief=RELIEF_POIL, oeil='#5ab8ff', pieces=pieces))
