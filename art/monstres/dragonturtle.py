"""Tortue-dragon (palier 3, spécial, blindée) — kit 2.40 : énorme tortue à tête de dragon, carapace bombée à pointes et plaques
rouge et bronze, crête."""
from communs.creatures import *
INFOS = {'categorie': 'monstre', 'titre': "Tortue-dragon"}

def vols(K):
    re = K.j('reins')
    return [V('Dos', '#8a3a2a', c=(0, re.y - .05, re.z + .05), r=(.34, .46, .24), prio=1)]   # carapace

def pieces(K):
    re, nu = K.j('reins'), K.j('nuque'); out = []
    for k in range(7):
        a = k / 7 * 2 * math.pi
        out.append(cone(f'Pointe{k}', '#e8b23a', 'Dos', (math.cos(a) * .2, re.y - .05 + math.sin(a) * .28, re.z + .22), .04, .002, .12,
                        rot=(-math.sin(a) * .6, math.cos(a) * .6, 0), seg=5))
    out.append(cone('PointeH', '#e8b23a', 'Dos', (0, re.y - .05, re.z + .29), .05, .002, .16, seg=5))
    out += [corne(f'Corne.{n}', '#e8dcc0', 'Tete', (s * .05, nu.y - .05, nu.z + .08), .025, .14, .9, rot=(-1.0, s * .4, 0), seg=5, n=3) for s, n in ((1, 'L'), (-1, 'R'))]
    return out + griffes(K)

def construire(ctx):
    bete('tortue_dragon', dict(z=1.45, poil=('#3a6a4a', '#5a8a64', '#c8b88a'), patte='#2a4a34', crete='#e8b23a', tete='lezard', tete_r=1.15,
                               longueur=.9, pattes=.7, epaisseur=1.3, cou=.9, queue=.8, relief=RELIEF_ECAILLE, oeil='#ffcf3a', ech=1.0,
                               duree=.75, foulee=.35, volumes=vols, pieces=pieces))
