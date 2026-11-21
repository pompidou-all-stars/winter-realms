"""Briseur de runes (palier 1, spécial, anti-magie) — kit 2.40 : colosse de pierre trapu en armure runique brisée, grand marteau."""
from communs.creatures import *
INFOS = {'categorie': 'monstre', 'titre': "Briseur de runes"}

def pieces(K):
    p = K.j('poitrine')
    for k, (x, z) in enumerate(((-.08, .05), (.06, .0), (0, -.08))):
        K.lueurs.append(plaque(f'Rune{k}', '#b07aff', 'Torse', (x, -.17, p.z + z), .03, .01, .05, rot=(0, 0, .5 * k)))
    return (casque(K, 'heaume', col='#5a5f68') + epaulieres(K, col='#6a6f78', taille=1.1, pointes=0, bord='#4a4f58') +
            arme(K, 'marteau', taille=1.35, col='#7a7f88') + genouilleres(K, col='#5a5f68') + brassards(K, col='#5a5f68'))

def construire(ctx):
    bipede('briseur', dict(z=1.0, peau=('#8a8f99', '#a8adb5', '#6a6f78'), bas='#5a5f68', botte='#4a4f58', tete='orc', tete_r=.85,
                           carrure=1.25, jambes=.34, muscle=.8, voute=.4, relief=RELIEF_PIERRE, oeil='#b07aff', lourd=1.2, pieces=pieces))
