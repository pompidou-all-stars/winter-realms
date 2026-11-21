"""Ogre (palier 1, sol) — kit 2.40 : ventre énorme, petite tête, masse cloutée, crâne-trophée, épaulières de cuir."""
from communs.creatures import *
INFOS = {'categorie': 'monstre', 'titre': "Ogre"}

def pieces(K):
    return (arme(K, 'masse', taille=1.3) + ceinture(K, pagne='#7a3a2a', crane=True) +
            epaulieres(K, col=CUIR, taille=.9, pointes=0, bord=None) + brassards(K, col=CUIR))

def construire(ctx):
    bipede('ogre', dict(z=1.1, peau=('#c2a06a', '#d8b885', '#9a7c4a'), bas='#6a4a2a', botte='#4a3420', tete='orc', tete_r=.8,
                        ventre=1.6, carrure=1.4, muscle=.4, voute=.6, jambes=.34, oeil='#ffb03a', lourd=1.4, pieces=pieces))
