"""Seigneur de guerre orc (palier 3, sol) — kit 2.40 : chef orc colossal, armure noire et or, épaulières à crânes, grande cape rouge,
deux haches, trophées."""
from communs.creatures import *
INFOS = {'categorie': 'monstre', 'titre': "Seigneur de guerre orc"}

def pieces(K):
    return (casque(K, 'cornu', col='#2a2a30', col2=OS_) + epaulieres(K, col='#2a2a30', taille=1.3, pointes=3, col_pointe=OS_, bord=OR) +
            arme(K, 'hache', taille=1.35) + arme(K, 'hache', cote='L', taille=1.1) + cape(K, col='#8a1a1a', longueur=1.2) +
            ceinture(K, col='#2a2a30', boucle=OR, pagne='#8a1a1a', crane=True) + genouilleres(K, col='#2a2a30') +
            brassards(K, col='#2a2a30', pointes=OR) + collier_crocs(K, n=7) + defenses(K, taille=1.2))

def construire(ctx):
    bipede('seigneur_guerre', dict(z=1.3, peau=('#4e7a36', '#6a9a4c', '#3a5e28'), bas='#3a3530', botte='#2a2622', tete='orc', voute=.35,
                                   carrure=1.4, jambes=.4, muscle=1.4, oeil='#ff3a2a', lourd=1.2, pieces=pieces))
