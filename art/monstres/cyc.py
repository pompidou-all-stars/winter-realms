"""Cyclope des cendres (palier 2, boss) — kit 2.40 : géant à un œil, peau grise craquelée de braises, massue de pierre volcanique,
pagne de peau, collier de crânes."""
from communs.creatures import *
INFOS = {'categorie': 'monstre', 'titre': "Cyclope des cendres"}

def pieces(K):
    p = K.j('poitrine')
    K.lueurs += [plaque(f'Braise{k}', '#ff7a2a', 'Torse', (x, -.17, p.z + z), .05, .01, .012, rot=(0, 0, a))
                 for k, (x, z, a) in enumerate(((-.08, .02, .5), (.07, -.04, -.4), (0, -.1, .2)))]
    return (arme(K, 'gourdin', taille=1.5, manche='#3a3330') + ceinture(K, pagne='#6a4a3a', crane=True) + collier_crocs(K, n=5) +
            brassards(K, col=CUIR) + [boule('Crane_collier', OS_, 'Torse', (0, -.16, p.z + .02), .04, seg=8)])

def construire(ctx):
    bipede('cyclope', dict(z=1.5, peau=('#8a7a70', '#a8988c', '#5a4a44'), bas='#6a4a3a', botte='#3a2a24', tete='cyclope', tete_r=1.05,
                           carrure=1.45, ventre=1.2, jambes=.4, muscle=1.0, voute=.5, relief=RELIEF_PIERRE, oeil='#ff8a2a', lourd=1.5,
                           pieces=pieces))
