"""Minotaure (palier 2, sol) — kit 2.40 : homme-taureau musclé, grandes cornes, anneau au museau, hache double, pagne de cuir."""
from communs.creatures import *
INFOS = {'categorie': 'monstre', 'titre': "Minotaure"}

def pieces(K):
    t = K.j('tete')
    return (cornes(K, col='#e8dcc0', taille=1.3, forme='taureau') + arme(K, 'hache', taille=1.3) +
            [tore('Anneau', OR, 'Tete', (0, t.y - .19, t.z + .02), .025, .006, rot=(math.pi / 2, 0, 0), seg=10, seg2=3)] +
            ceinture(K, pagne='#5a3a22', boucle=FER) + brassards(K, col=CUIR))

def construire(ctx):
    bipede('minotaure', dict(z=1.2, peau=('#7a4a2e', '#9a6a48', '#5a341e'), bas='#5a3a22', botte='#2a1a10', tete='taureau', tete_r=1.05,
                             carrure=1.35, jambes=.42, muscle=1.3, voute=.45, relief=RELIEF_POIL, oeil='#ff5a2a', pieces=pieces))
