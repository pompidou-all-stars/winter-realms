"""Azh'Khar, seigneur des lames (palier 3, boss) — kit 2.40 : maître d'armes démoniaque violet en armure noire et argent, quatre
lames (deux épées, deux lames sur les avant-bras), couronne de cornes, cape violette."""
from communs.creatures import *
INFOS = {'categorie': 'monstre', 'titre': "Azh'Khar, seigneur des lames"}

def pieces(K):
    w = K.j('poignet.L'); c = K.j('coude.L')
    return (cornes(K, col='#d0d8e0', taille=1.1, forme='droites') + casque(K, 'couronne', col='#d0d8e0') +
            epaulieres(K, col='#1a1a24', taille=1.25, pointes=3, col_pointe='#d0d8e0', bord='#a77cff') +
            arme(K, 'epee', taille=1.35, col='#c8b0ff') + arme(K, 'epee', cote='L', taille=1.35, col='#c8b0ff') +
            [profil(f'LameBras.{n}', '#d0d8e0', f'AvantBras.{n}', [(0, 0), (.04, .02), (.02, -.3)], .012, pos=(s * (c.x + .06), c.y, c.z - .02),
                    rot=(0, 0, 0 if s > 0 else math.pi)) for s, n in ((1, 'L'), (-1, 'R'))] +
            cape(K, col='#4a2a7a', longueur=1.15) + genouilleres(K, col='#1a1a24') + ceinture(K, col='#1a1a24', boucle='#a77cff', pagne='#4a2a7a'))

def construire(ctx):
    bipede('azhkhar', dict(z=1.35, peau=('#7a5aa8', '#9a7ac8', '#5a3a88'), bas='#1a1a24', botte='#1a1a24', tete='demon', carrure=1.3,
                           jambes=.44, muscle=1.3, voute=.2, relief=RELIEF_PEAU, oeil='#e8b0ff', pieces=pieces))
