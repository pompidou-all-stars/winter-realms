"""Maître des nuées (palier 1, spécial, invocation — capacité à venir) — kit 2.40 : prêtre homme-rat en robe verte,
capuche, bâton à cloche et cristal vert, qui appelle des nuées de rats."""
from communs.creatures import *
INFOS = {'categorie': 'monstre', 'titre': "Maître des nuées"}

def pieces(K):
    return casque(K, 'capuche', col='#3a5a2a') + arme(K, 'baton', taille=1.15, col='#c8a040') + collier_crocs(K, n=3)

def construire(ctx):
    bipede('maitre_nuees', dict(z=.95, peau=('#7a6a5a', '#9a8a78', '#5a4a3e'), bas='#3a5a2a', tete='rat', bas_du_corps='robe',
                                voute=.8, carrure=.85, muscle=0, queue=('#d8a59a', 1.2), relief=RELIEF_POIL, magie='#7aff5a',
                                oeil='#7aff5a', pieces=pieces))
