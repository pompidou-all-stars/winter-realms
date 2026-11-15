"""Faucheuse (palier 3, magique : invisible) : grande silhouette en robe noire déchirée, crâne sous
la capuche, yeux violets, faux immense ; flotte au ras du sol. Clé CR « reaper »."""
import math
from communs.outils import collection, dans, pivot, peindre, sphere, cone, cylindre, boite, prisme, anneau, descendants
from communs.betes import yeux_bete
from communs.animations import flotte
from communs.export_jeu import preparer

# taille selon le facteur z proposé pour CR (même formule que communs/echelles.py) ; voir PALIERS.md
Z = 1.3
def hauteur(): return .40 * Z ** 1.8
def piece(r, nom): return next(o for o in descendants(r) if o.name.split('.')[0] == nom)

INFOS = {'categorie': 'monstre', 'titre': "Faucheuse"}

def fabriquer():
    c = collection('faucheuse'); dans(c)
    r = pivot('faucheuse'); H = hauteur()
    corps = pivot('Corps', (0, 0, H * .06), r)
    cylindre('Robe', '#1b1c22', H * .28, H * .14, H * .62, 12, (0, 0, 0), corps, lisse=True)
    for k in range(7):
        a = k * 2 * math.pi / 7
        cone(f'Lambeau{k}', '#24252d', H * .06, H * .16, 4, (math.cos(a) * H * .24, math.sin(a) * H * .24, H * .02), corps, (math.pi, 0, a))
    T = pivot('Tete', (0, 0, H * .66), corps)
    sphere('Capuche', '#1b1c22', H * .17, (0, 0, 0), (1, 1, 1.15), 12, 8, T)
    sphere('Crane', '#e6e2d2', H * .1, (0, -H * .07, -H * .01), (1, .9, 1.05), 10, 6, T)
    for s in (-1, 1): sphere(f'Oeil{s}', '#c77dff', H * .022, (s * H * .035, -H * .16, H * .01), (1, .5, 1.3), 6, 4, T, emis=4)
    for s, n in ((-1, 'G'), (1, 'D')):
        b = pivot(f'Bras{n}', (s * H * .17, 0, H * .5), corps); b.rotation_euler = (-.7, 0, 0)
        cone(f'Manche{n}', '#24252d', H * .06, H * .26, 6, (0, 0, -H * .26), b)
    a = pivot('Arme', (H * .17, -H * .18, H * .28), corps)
    cylindre('Manche', '#3a3330', H * .014, H * .014, H * .95, 6, (0, 0, -H * .3), a)
    prisme('Lame', '#c9ced6', [(0, 0), (-H * .4, -H * .05), (-H * .5, -H * .15), (-H * .3, -H * .06)], H * .015, (0, 0, H * .62), a, metal=.5)
    peindre(r, sol=.85)
    flotte(r, duree=1.8, ampl=H * .06, roulis=.1)
    return r

def construire(ctx):
    preparer(fabriquer())
