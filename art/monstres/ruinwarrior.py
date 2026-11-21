"""Guerrier des Ruines (palier 2, sol) — kit 2.40 : guerrier colossal en armure noire et cuivre, heaume cornu, hache à deux mains,
cape en lambeaux (les « Ruines » : notre version des guerriers du Chaos)."""
from communs.creatures import *
INFOS = {'categorie': 'monstre', 'titre': "Guerrier des Ruines"}
ARM, CUIV = '#2a2630', '#b8743a'

def pieces(K):
    return (casque(K, 'heaume', col=ARM) + cornes(K, col=CUIV, taille=1.0, forme='droites') +
            epaulieres(K, col=ARM, taille=1.25, pointes=3, col_pointe=CUIV, bord=CUIV) + arme(K, 'hache', taille=1.35, col='#8a8f99') +
            cape(K, col='#5a1a1a', longueur=1.0) + genouilleres(K, col=ARM) + brassards(K, col=ARM, pointes=CUIV) + ceinture(K, col=ARM, boucle=CUIV, pagne='#3a1a1a'))

def construire(ctx):
    bipede('guerrier_ruines', dict(z=1.1, peau=(ARM, '#3a3640', '#1a181e'), bas=ARM, botte=ARM, tete='humain', tete_r=.95,
                                   carrure=1.3, jambes=.42, muscle=.3, voute=.15, relief=RELIEF_PIERRE, oeil='#ff3a2a', lourd=1.2, pieces=pieces))
