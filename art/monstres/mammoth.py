"""Mammouth de bataille à tour (palier 2, sol) — kit 2.40 : mammouth laineux aux défenses ferrées, tour de guerre en bois sur le dos
(plancher, poteaux d'angle, palissade, boucliers ronds, toit pointu rouge), bannières rouges (notre version hivernale de l'oliphant)."""
from communs.creatures import *
INFOS = {'categorie': 'monstre', 'titre': "Mammouth de bataille à tour"}

def pieces(K):
    m, re, ga = K.j('museau'), K.j('reins'), K.j('garrot'); yc = (re.y + ga.y) / 2; z = re.z + .2; out = []
    out.append(corne('Trompe', '#5a3a24', 'Tete', (0, m.y + .1, m.z), .05, .3, -1.6, rot=(math.pi * .95, 0, 0), seg=7, n=5))
    for s, n in ((1, 'L'), (-1, 'R')):
        out.append(corne(f'Defense.{n}', OS_, 'Tete', (s * .07, m.y + .12, m.z - .04), .035, .35, 1.6, rot=(-1.9, s * .35, 0), seg=7, n=5))
        out.append(tore(f'Bague.{n}', FER, 'Tete', (s * .08, m.y + .02, m.z - .1), .035, .01, rot=(-1.2, s * .35, 0), seg=8, seg2=3))
        out.append(cone(f'Bannierehampe.{n}', BOIS, 'Dos', (s * .2, yc + .16, z + .1), .01, .01, .6, seg=5))
        out.append(plaque(f'Banniere.{n}', ROUGE, 'Dos', (s * .21, yc + .22, z + .55), .01, .12, .2))
        for k, dy in enumerate((-.1, .1)):   # boucliers ronds sur les flancs de la tour
            out.append(cone(f'Bouclier{k}.{n}', ROUGE if k else '#c8a040', 'Dos', (s * .17, yc + dy, z + .14), .07, .07, .015, rot=(0, s * math.pi / 2, 0), seg=10))
            out.append(boule(f'Umbo{k}.{n}', FER, 'Dos', (s * .185, yc + dy, z + .14), .02, seg=6))
    out += [plaque('Tapis', ROUGE, 'Dos', (0, yc, z - .06), .52, .46, .02), plaque('Plancher', '#5a4028', 'Dos', (0, yc, z), .4, .44, .04),
            plaque('Palissade', '#7a5a3a', 'Dos', (0, yc, z + .12), .32, .36, .2), plaque('Rambarde', '#5a4028', 'Dos', (0, yc, z + .24), .36, .4, .03)]
    out += [cone(f'Poteau{k}', '#4a3420', 'Dos', (sx * .17, yc + sy * .19, z), .018, .018, .42, seg=5) for k, (sx, sy) in enumerate(((1, 1), (1, -1), (-1, 1), (-1, -1)))]
    out += [cone('Toit', ROUGE, 'Dos', (0, yc, z + .42), .3, .002, .24, seg=4, rot=(0, 0, math.pi / 4)), cone('Pointe', '#c8a040', 'Dos', (0, yc, z + .66), .012, .002, .1, seg=4)]
    return out

def construire(ctx):
    bete('mammouth', dict(z=1.45, poil=('#6e4a30', '#8a6448', '#5a3a24'), patte='#4a3020', crete='#4a3020', tete='mammouth', tete_r=1.15,
                          longueur=1.0, pattes=1.1, epaisseur=1.5, cou=.55, queue=.3, oeil='#ffb03a', ech=1.0, duree=.7, foulee=.35,
                          pieces=pieces))
