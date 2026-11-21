"""Faucheuse (palier 3, spécial, invisible) — kit 2.40 : grande silhouette flottante en robe noire déchirée, capuche profonde, crâne aux
yeux bleus, ailes de lambeaux, lanterne d'âmes, faux immense."""
from communs.creatures import *
INFOS = {'categorie': 'monstre', 'titre': "Faucheuse"}

def pieces(K):
    p, w = K.j('poitrine'), K.j('poignet.L')
    K.lueurs += [boule('Lanterne', '#7fd8ff', 'Main.L', (w.x, w.y - .02, w.z - .16), .045, seg=8),
                 boule('Ame', '#bfe6ff', 'Torse', (0, -.17, p.z - .02), .03, seg=6)]
    return (casque(K, 'capuche', col='#1a1a20') + arme(K, 'faux', taille=1.6, col='#c8d0d8', manche='#2a2420') +
            ailes_dos(K, '#1a1a20', '#2a2a34', envergure=1.1) + cape(K, col='#1a1a20', longueur=1.0) +
            [cone('Chaine', FER, 'Main.L', (w.x, w.y - .02, w.z - .06), .008, .008, .1, seg=4)])

def construire(ctx):
    bipede('faucheuse', dict(z=1.6, peau=('#e6e2d2', '#d0ccbc', '#b8b4a4'), bas='#24252d', tete='crane', tete_r=1.1, bas_du_corps='traine',
                             carrure=1.05, bras=1.3, muscle=0, voute=.45, relief=RELIEF_LISSE, oeil='#7fd8ff', pieces=pieces))
