"""Chevaucheur de sanglier (palier 1, sol) — kit 2.40 : gobelin à la lance sur un sanglier de guerre à défenses et crinière."""
from communs.creatures import *
INFOS = {'categorie': 'monstre', 'titre': "Chevaucheur de sanglier"}
cv = {}

def lance(s, b): return lance_cavalier(s, b)

def vols(K):
    v, cv['p'] = cavalier(K, peau=('#7fb94a', '#97cc5e', '#5f9a38'), tissu='#6b4a2e', taille=.75, pieces=lance)
    return v

def pieces(K):
    m, re = K.j('museau'), K.j('reins')
    return (cv['p'] + meches_dos(K, '#2e231a', n=4, taille=.8, rangs=False) +
            [corne(f'Defense.{n}', OS_, 'Tete', (s * .06, m.y + .1, m.z - .02), .022, .09, 1.2, rot=(-.3, s * .4, 0)) for s, n in ((1, 'L'), (-1, 'R'))] +
            [plaque('Selle', ROUGE, 'Dos', (0, re.y - .1, re.z + .15), .22, .2, .03)])

def construire(ctx):
    bete('chevaucheur_sanglier', dict(z=.9, poil=('#6a4a30', '#8a6448', '#a08060'), patte='#3a2a1e', crete='#2e231a', tete='sanglier',
                                      longueur=.9, pattes=.8, epaisseur=1.2, cou=.7, queue=.4, oeil='#ff6a2a', ech=1.15, volumes=vols, pieces=pieces))
