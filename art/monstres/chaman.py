"""Chaman orc sur warg (palier 1, spécial, hâte) — kit 2.40 : chaman orc à coiffe de plumes, bâton-totem lumineux, monté sur un warg brun."""
from communs.creatures import *
INFOS = {'categorie': 'monstre', 'titre': "Chaman orc sur warg"}
cv = {}

def baton(s, b):
    base = (-.16 * s, b.y - .05, b.z + .05)
    return [cone('Baton', BOIS, 'Dos', base, .012, .01, .55, rot=(.2, 0, 0)),
            boule('Totem', OS_, 'Dos', (base[0], base[1] - .11, base[2] + .53), .04, seg=8),
            corne('PlumeA', ROUGE, 'Dos', (.0, b.y + .02, b.z + .42 * s), .02, .1, .5, rot=(-.4, .3, 0), seg=4, n=2),
            corne('PlumeB', '#e8b23a', 'Dos', (.0, b.y + .03, b.z + .42 * s), .02, .1, .5, rot=(-.4, -.3, 0), seg=4, n=2)]

def vols(K):
    v, cv['p'] = cavalier(K, peau=('#5f9c45', '#7ab05a', '#4a7a35'), tissu='#8a5a2a', taille=.75, pieces=baton)
    return v

def pieces(K):
    b = K.j('reins'); s = .75
    K.lueurs.append(boule('Orbe', '#ffe45e', 'Dos', (-.16 * s, b.y - .16, b.z + .62), .035, seg=8))
    return cv['p'] + meches_dos(K, '#3a2a1e', n=4, taille=.7, rangs=False) + griffes(K)

def construire(ctx):
    bete('chaman_warg', dict(z=.9, poil=('#7a5a3a', '#9a7a58', '#b89a78'), patte='#4a3424', crete='#3a2a1e', tete='loup', queue=1.0,
                             oeil='#ffe45e', ech=1.25, volumes=vols, pieces=pieces))
