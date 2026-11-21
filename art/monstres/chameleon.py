"""Caméléon géant (palier 2, spécial, invisible) — kit 2.40 : grand lézard aux yeux globuleux, crête, queue enroulée, peau changeante."""
from communs.creatures import *
INFOS = {'categorie': 'monstre', 'titre': "Caméléon géant"}

def vols(K):
    nu = K.j('nuque')
    return [V('Tete', '#3aa89a', c=(.1, nu.y - .12, nu.z + .06), r=(.05, .05, .05), prio=1)]   # yeux globuleux

def pieces(K):
    q2 = K.j('queue2')
    return (meches_dos(K, '#e8a83a', n=6, taille=.6, rangs=False) + griffes(K) +
            [tore('Spirale', '#2a8a7a', 'Queue2', (0, q2.y + .05, q2.z + .02), .07, .03, rot=(0, math.pi / 2, 0), seg=10, seg2=5)])

def construire(ctx):
    bete('cameleon', dict(z=1.0, poil=('#2a8a7a', '#5ac8a8', '#e8d88a'), patte='#1a6a5a', crete='#e8a83a', tete='lezard', tete_r=1.1,
                          longueur=1.1, pattes=.8, epaisseur=1.0, cou=.8, queue=1.0, relief=RELIEF_ECAILLE, taches=.3, taille_taches=5,
                          oeil='#ffe43a', volumes=vols, pieces=pieces))
