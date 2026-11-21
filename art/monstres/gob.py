"""Sapeur gobelin (palier 1, sol) — kit de créatures 2.40 : petit gobelin à grosse tête et grandes oreilles,
pioche à l'épaule, bombe à mèche dans l'autre main, sac sur le dos."""
from communs.creatures import *
INFOS = {'categorie': 'monstre', 'titre': "Sapeur gobelin"}
P = ('#7fb94a', '#97cc5e', '#5f9a38')

def vols(K):
    t = K.j('tete')
    return [V('Tete', P[0], c=(.13, t.y + .02, t.z + .09), r=(.1, .014, .032), rot=(0, -.25, -.3)),
            V('Tete', P[1], c=(0, t.y - .13, t.z + .05), r=(.03, .06, .03), rot=(.5, 0, 0), prio=2)]

def pieces(K):
    w = K.j('poignet.L'); p = K.j('poitrine')
    return (arme(K, 'marteau', taille=.8, col=FER) + ceinture(K, pagne='#6b4a2e', boucle=None) + casque(K, 'pointe', col=CUIR) +
            [boule('Sac', CUIR, 'Torse', (0, .16, p.z), .1, ech=(1, .7, 1.1), seg=10),
             boule('Bombe', NOIR, 'Main.L', (w.x, w.y - .03, w.z - .07), .055, seg=10),
             corne('Meche', '#d8b070', 'Main.L', (w.x, w.y - .03, w.z - .02), .008, .05, .8, seg=4, n=2)])

def construire(ctx):
    bipede('sapeur', dict(z=.75, peau=P, bas='#6b4a2e', botte='#3a2a1a', tete='orc', tete_r=1.35, tete_h=.27, jambes=.32,
                          carrure=.75, hanches=.85, muscle=0, voute=.6, oeil='#ffd23a', volumes=vols, pieces=pieces))
