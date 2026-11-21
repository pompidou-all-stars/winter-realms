"""Chasseur sauvage (palier 2, spécial, accéléré) — kit 2.40 : cavalier spectral à tête de crâne couronnée de bois de cerf, lance,
sur un destrier fantôme bleuté (la Chasse sauvage des légendes européennes)."""
from communs.creatures import *
INFOS = {'categorie': 'monstre', 'titre': "Chasseur sauvage"}
cv = {}

def armes(s, b):
    out = lance_cavalier(s, b, col='#bfe6ff', manche='#3a4a5a')
    for sg in (1, -1):
        out.append(corne(f'BoisC{sg}', '#d8ccb0', 'Dos', (sg * .04 * s, b.y - .02, b.z + .42 * s), .015, .16, .7, rot=(-.3, sg * .8, 0), seg=4, n=3))
    return out

def vols(K):
    v, cv['p'] = cavalier(K, peau=('#e6e2d2', '#d0ccbc', '#b8b4a4'), tissu='#2a3a5a', taille=.75, pieces=armes)
    return v

def pieces(K):
    return cv['p'] + meches_dos(K, '#9fd8ff', n=5, taille=.7, rangs=False)

def construire(ctx):
    bete('chasseur_sauvage', dict(z=1.15, poil=('#3a4a6a', '#5a6a8a', '#7a8aa8'), patte='#2a3448', crete='#9fd8ff', tete='cheval',
                                  longueur=1.05, pattes=1.25, epaisseur=.9, cou=1.1, queue=1.0, relief=RELIEF_POIL, oeil='#7fd8ff',
                                  ech=1.05, duree=.4, foulee=.6, volumes=vols, pieces=pieces))
