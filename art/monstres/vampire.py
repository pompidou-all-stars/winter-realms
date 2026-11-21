"""Seigneur vampire (palier 3, spécial, soin) — kit 2.40 : noble vampire pâle en armure noire et rouge sang, grande cape à haut col,
couronne de fer, épée, ailes de chauve-souris repliées."""
from communs.creatures import *
INFOS = {'categorie': 'monstre', 'titre': "Seigneur vampire"}

def pieces(K):
    p = K.j('poitrine')
    return (casque(K, 'couronne', col='#3a3a40') + cape(K, col='#6a0a1a', longueur=1.25) + arme(K, 'epee', taille=1.2, col='#d0d8e0') +
            epaulieres(K, col='#1a1a20', taille=.95, pointes=2, col_pointe='#8a1a2a', bord='#8a1a2a') + ailes_dos(K, '#1a1a20', '#3a0a14', envergure=.7) +
            [profil('Col', '#6a0a1a', 'Torse', [(-.2, 0), (.2, 0), (.24, .2), (0, .13), (-.24, .2)], .012, pos=(0, .08, p.z + .06), rot=(.3, 0, 0))] +
            ceinture(K, col='#1a1a20', boucle='#8a1a2a', pagne='#3a0a14'))

def construire(ctx):
    bipede('seigneur_vampire', dict(z=1.25, peau=('#d8d4dc', '#eeeaf0', '#a8a0b0'), bas='#1a1a20', botte='#1a1a20', tete='humain',
                                    carrure=1.05, jambes=.44, muscle=.3, voute=.1, relief=RELIEF_LISSE, oeil='#ff2a3a', pieces=pieces))
