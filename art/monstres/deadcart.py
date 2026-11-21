"""Charrette des morts (palier 1, spécial, résurrection — capacité à venir) — kit 2.40 : charrette de bois chargée de cadavres et de
crânes, roues cerclées, lanterne verte, poussée par un cocher squelette."""
from communs.creatures import *
INFOS = {'categorie': 'monstre', 'titre': "Charrette des morts"}
cv = {}

def vols(K):
    v, cv['p'] = cavalier(K, peau=('#e6e2d2', '#d0ccbc', '#b8b4a4'), tissu='#3a3040', taille=.6, y=K.j('bassin').y + .02, z=.42)
    return v

def pieces(K):
    re, ga, b = K.j('reins'), K.j('garrot'), K.j('bassin'); z = .3
    out = [plaque('Caisse', BOIS, 'Dos', (0, (ga.y + b.y) / 2, z + .12), .42, .62, .2), plaque('Fond', '#4a3420', 'Dos', (0, (ga.y + b.y) / 2, z), .44, .66, .05)]
    for s, n in ((1, 'L'), (-1, 'R')):
        for k, y in enumerate((ga.y + .05, b.y - .1)):
            out += [tore(f'Roue{k}.{n}', '#5a4028', 'Dos', (s * .25, y, .14), .13, .02, rot=(0, math.pi / 2, 0), seg=12, seg2=4),
                    cone(f'Moyeu{k}.{n}', FER, 'Dos', (s * .22, y, .14), .03, .03, .05, rot=(0, s * math.pi / 2, 0), seg=6)]
    for k in range(5):
        out.append(boule(f'Crane{k}', OS_, 'Dos', (-.12 + .06 * k, ga.y + .1 + .07 * (k % 3), z + .27), .045, seg=8))
    out.append(cone('Perche', BOIS, 'Dos', (.15, ga.y, z + .2), .01, .01, .4, seg=5))
    K.lueurs.append(boule('Lanterne', '#7aff8a', 'Dos', (.15, ga.y - .03, z + .6), .04, seg=8))
    return out + cv['p']

def construire(ctx):
    bete('charrette_morts', dict(z=.95, poil=('#5a4028', '#7a5a3a', '#4a3420'), tete='aucune', queue=0, sans_pattes=True, epaisseur=.5,
                                 relief=RELIEF_LISSE, oeil='#7aff8a', ech=1.2, duree=.7, foulee=.1, volumes=vols, pieces=pieces))
