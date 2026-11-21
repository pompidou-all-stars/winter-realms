"""Ettin (palier 1, sol) — kit 2.40 : géant à deux têtes, ventru, gourdin énorme, collier de crocs."""
from communs.creatures import *
from communs.creatures import _tete
INFOS = {'categorie': 'monstre', 'titre': "Ettin"}
P = ('#8a8f6a', '#a4a884', '#6a6f50')

def vols(K):
    t = K.j('tete'); v = []
    for x in (.075, -.075): v += _tete(K, (x, t.y - .005, t.z + .05), 'orc', P)
    return [seul(x) for x in v]

def pieces(K):
    return arme(K, 'gourdin', taille=1.4) + ceinture(K, pagne='#6a4a2a', boucle=None) + collier_crocs(K)

def construire(ctx):
    bipede('ettin', dict(z=1.08, peau=P, bas='#6a5a3a', botte='#4a3e2a', tete='aucune', tete_r=.85, carrure=1.4, ventre=1.3,
                         muscle=.6, jambes=.36, voute=.55, oeil='#ffb03a', lourd=1.3, volumes=vols, pieces=pieces))
