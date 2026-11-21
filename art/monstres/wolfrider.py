"""Chevaucheur de warg gobelin (palier 1, spécial, accéléré) — kit 2.40 : gobelin au sabre sur un warg noir rapide, à crinière."""
from communs.creatures import *
INFOS = {'categorie': 'monstre', 'titre': "Chevaucheur de warg"}
cv = {}

def sabre(s, b):
    return [profil('Sabre', LAME, 'Dos', [(-.02, 0), (.02, 0), (.04, .3), (0, .34), (-.01, .3)], .01, pos=(-.17 * s, b.y - .05, b.z + .2), rot=(.9, 0, 0))]

def vols(K):
    v, cv['p'] = cavalier(K, peau=('#7fb94a', '#97cc5e', '#5f9a38'), tissu='#4a3a2a', taille=.7, pieces=sabre)
    return v

def pieces(K):
    return cv['p'] + meches_dos(K, '#1a1c20', n=5, taille=.85) + griffes(K)

def construire(ctx):
    bete('chevaucheur_warg', dict(z=.85, poil=('#3a3e46', '#555b64', '#7a8088'), patte='#25282e', crete='#1a1c20', tete='loup',
                                  queue=1.0, oeil='#ff4a3a', ech=1.3, duree=.4, foulee=.6, volumes=vols, pieces=pieces))
