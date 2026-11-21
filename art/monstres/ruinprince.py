"""Prince des Ruines (palier 3, spécial, hâte) — kit 2.40 : démon ailé en armure noire et cuivre, grandes cornes, épée runique,
étendard de guerre (notre version des princes démons du Chaos)."""
from communs.creatures import *
INFOS = {'categorie': 'monstre', 'titre': "Prince des Ruines"}
ARM, CUIV = '#2a2630', '#b8743a'

def pieces(K):
    p = K.j('poitrine')
    return (cornes(K, col=CUIV, taille=1.4, forme='belier') + ailes_dos(K, '#3a1a24', '#5a2a34', envergure=1.1) +
            epaulieres(K, col=ARM, taille=1.2, pointes=3, col_pointe=CUIV, bord=CUIV) + arme(K, 'epee', taille=1.4, col='#c87aff') +
            [cone('Hampe', ARM, 'Torse', (.1, .16, p.z - .1), .01, .01, .55, seg=5), plaque('Etendard', '#8a1a2a', 'Torse', (.1, .17, p.z + .32), .01, .16, .2)] +
            ceinture(K, col=ARM, boucle=CUIV, pagne='#3a1a1a') + genouilleres(K, col=ARM))

def construire(ctx):
    bipede('prince_ruines', dict(z=1.3, peau=('#6a2a3a', '#8a3a4c', '#4a1a28'), bas=ARM, botte=ARM, tete='demon', carrure=1.3,
                                 jambes=.42, muscle=1.2, voute=.3, queue=('#4a1a28', 1.1), relief=RELIEF_PEAU, oeil='#ffcf3a', pieces=pieces))
