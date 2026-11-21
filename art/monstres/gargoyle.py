"""Gargouille (palier 2, sol) — kit 2.40 : démon de pierre trapu et accroupi, ailes de pierre repliées, cornes, griffes."""
from communs.creatures import *
INFOS = {'categorie': 'monstre', 'titre': "Gargouille"}

def pieces(K):
    return cornes(K, col='#6a6f78', taille=.9, forme='droites') + ailes_dos(K, '#6a6f78', '#7a7f88', envergure=.8)

def construire(ctx):
    bipede('gargouille', dict(z=1.1, peau=('#8a8f99', '#a8adb5', '#6a6f78'), bas='#7a7f88', botte='#6a6f78', tete='demon', tete_r=1.05,
                              voute=.9, jambes=.3, carrure=1.1, bras=1.15, muscle=.8, queue=('#7a7f88', 1.0), relief=RELIEF_PIERRE,
                              oeil='#ff8a2a', pieces=pieces))
