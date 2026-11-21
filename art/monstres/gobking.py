"""Grizzak, roi gobelin (palier 1, boss) — kit 2.40 : gobelin énorme et ventru, couronne d'or, cape rouge, masse dorée, colliers."""
from communs.creatures import *
INFOS = {'categorie': 'monstre', 'titre': "Grizzak, roi gobelin"}
P = ('#7fb94a', '#97cc5e', '#5f9a38')

def vols(K):
    t = K.j('tete')
    return [V('Tete', P[0], c=(.13, t.y + .02, t.z + .09), r=(.11, .015, .035), rot=(0, -.25, -.3))]

def pieces(K):
    return (casque(K, 'couronne', col=OR) + cape(K, col=ROUGE, longueur=1.1) + arme(K, 'masse', taille=1.25, col=OR, manche=OR) +
            collier_crocs(K, col=OR, cordon=OR, n=7) + epaulieres(K, col='#e8e0d0', taille=.9, pointes=0, bord=OR) +
            ceinture(K, pagne='#6a2a8a', boucle=OR, crane=True))

def construire(ctx):
    bipede('grizzak', dict(z=1.2, peau=P, bas='#6a2a8a', botte='#3a2a1a', tete='orc', tete_r=1.2, tete_h=.22, ventre=1.8,
                           carrure=1.2, muscle=.3, jambes=.32, voute=.4, oeil='#ffd23a', lourd=1.5, volumes=vols, pieces=pieces))
