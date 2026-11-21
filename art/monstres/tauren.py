"""Ancien taurin (palier 1, spécial, soin) — kit 2.40 : grand homme-taureau à fourrure brune, cornes, bâton-totem vert, collier de crocs."""
from communs.creatures import *
INFOS = {'categorie': 'monstre', 'titre': "Ancien taurin"}

def pieces(K):
    return (cornes(K, col='#e8dcc0', taille=1.1, forme='taureau') + arme(K, 'baton', taille=1.2) + collier_crocs(K) +
            ceinture(K, pagne='#3a6a8a', boucle=OR) + brassards(K, col='#3a6a8a'))

def construire(ctx):
    bipede('ancien_taurin', dict(z=1.0, peau=('#7a5a3a', '#9a7a5a', '#5a3e28'), bas='#6a4a2a', botte='#2a1e14', tete='taureau',
                                 carrure=1.25, jambes=.40, muscle=.8, voute=.4, relief=RELIEF_POIL, magie='#6fcf97', oeil='#6fcf97',
                                 pieces=pieces))
