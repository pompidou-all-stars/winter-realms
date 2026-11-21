"""Horreur recousue (palier 2, sol) — kit 2.40 : golem de chair blafarde, coutures, ventre énorme, crochet et couperet, pointes de fer."""
from communs.creatures import *
INFOS = {'categorie': 'monstre', 'titre': "Horreur recousue"}

def pieces(K):
    v = K.j('ventre')
    return (arme(K, 'epee', taille=1.1, col='#8a8f99') +
            [plaque(f'Couture{k}', '#3a2a2a', 'Colonne', (0, -.2, v.z + .07 * (k - 1)), .14, .012, .012) for k in range(3)] +
            [cone(f'Pointe{k}', FER, 'Torse', (x, .12, K.j('poitrine').z + .08), .02, .002, .09, rot=(-.6, x * 2, 0), seg=5) for k, x in enumerate((-.1, 0, .1))] +
            ceinture(K, col='#3a2a2a', boucle=FER, pagne='#4a3a3a'))

def construire(ctx):
    bipede('horreur_recousue', dict(z=1.2, peau=('#b8a8a0', '#d0c4bc', '#8a7a74'), bas='#5a4a4a', botte='#3a2a2a', tete='humain', tete_r=.75,
                                    ventre=1.9, carrure=1.4, muscle=.3, voute=.5, jambes=.34, taches=.25, oeil='#9aff5a', lourd=1.5,
                                    pieces=pieces))
