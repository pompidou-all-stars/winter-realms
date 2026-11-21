"""Homme-rat pilleur (palier 1, sol) — kit 2.40 : homme-rat voûté, museau pointu, grande queue rose, lame rouillée, bouclier."""
from communs.creatures import *
INFOS = {'categorie': 'monstre', 'titre': "Homme-rat pilleur"}

def pieces(K):
    return (arme(K, 'epee', taille=.85, col='#8a7a6a') + bouclier(K, col='#5a4a3a', bord='#7a6a5a', taille=.75) +
            ceinture(K, pagne='#4a3a2e', boucle=None) + brassards(K, col='#4a3a2e'))

def construire(ctx):
    bipede('homme_rat', dict(z=.8, peau=('#7a6a5a', '#9a8a78', '#5a4a3e'), bas='#5a4a3a', botte='#7a6a5a', tete='rat', tete_r=1.1,
                             voute=.8, jambes=.36, carrure=.8, hanches=.85, muscle=.4, queue=('#d8a59a', 1.3), relief=RELIEF_POIL,
                             oeil='#ff3a3a', pieces=pieces))
