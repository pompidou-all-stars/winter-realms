"""Géant du givre (palier 3, sol) — kit 2.40 : géant à peau bleu pâle, barbe et cheveux blancs tressés, armure de fourrure et de fer,
grande hache de glace."""
from communs.creatures import *
INFOS = {'categorie': 'monstre', 'titre': "Géant du givre"}

def vols(K):
    t = K.j('tete')
    return [V('Tete', '#eef4fb', a=(0, t.y - .1, t.z + .02), b=(0, t.y - .12, t.z - .15), ra=.09, rb=.04, prio=2)]   # barbe

def pieces(K):
    return (casque(K, 'cornu', col='#8a9aaa', col2='#eef4fb') + epaulieres(K, col='#6a7a8a', taille=.8, pointes=2, col_pointe='#bfe6ff', bord='#dfe7ef') +
            arme(K, 'hache', taille=1.4, col='#bfe6ff', manche='#5a6a7a') + ceinture(K, col='#5a6a7a', boucle='#bfe6ff', pagne='#dfe7ef') +
            brassards(K, col='#8a9aaa') + genouilleres(K, col='#8a9aaa'))

def construire(ctx):
    bipede('geant_givre', dict(z=1.6, peau=('#8fb3d4', '#a8c8e4', '#6a8fb0'), bas='#5a6a7a', botte='#dfe7ef', tete='humain', tete_r=.9,
                               carrure=1.35, jambes=.44, muscle=1.0, voute=.25, oeil='#bfe6ff', lourd=1.3, volumes=vols, pieces=pieces))
