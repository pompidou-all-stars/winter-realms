"""Basilic (palier 2, sol) — kit 2.40 : grand reptile à six regards, écailles vert sombre, crête et collerette, yeux jaunes pétrifiants."""
from communs.creatures import *
INFOS = {'categorie': 'monstre', 'titre': "Basilic"}

def pieces(K):
    nu = K.j('nuque')
    return (meches_dos(K, '#c8a83a', n=6, taille=.8, rangs=False) + griffes(K) +
            [profil(f'Collerette.{n}', '#c8a83a', 'Cou', [(0, 0), (.16, .08), (.14, -.1)], .01, pos=(s * .08, nu.y + .08, nu.z - .02),
                    rot=(0, 0, 0 if s > 0 else math.pi)) for s, n in ((1, 'L'), (-1, 'R'))])

def construire(ctx):
    bete('basilic', dict(z=1.15, poil=('#3a6a3a', '#5a8a4a', '#c8c07a'), patte='#2a4a2a', crete='#c8a83a', tete='lezard', tete_r=1.1,
                         longueur=1.2, pattes=.75, epaisseur=1.1, cou=1.1, queue=1.6, relief=RELIEF_ECAILLE, oeil='#ffe43a',
                         duree=.5, pieces=pieces))
