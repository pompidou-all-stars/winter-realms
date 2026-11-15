"""Myconide (palier 1, sol) : champignon ambulant au pied blanc, grand chapeau rouge à pois blancs,
petits yeux noirs, bras en racines ; des spores bleues brillent sous le chapeau. Clé CR « myco »."""
import math
from communs.outils import collection, dans, pivot, peindre, sphere, cone, cylindre, boite, prisme, anneau, descendants
from communs.animations import marche
from communs.export_jeu import preparer

# taille selon le facteur z proposé pour CR (même formule que communs/echelles.py) ; voir PALIERS.md
Z = 0.95
def hauteur(): return .40 * Z ** 1.8
def piece(r, nom): return next(o for o in descendants(r) if o.name.split('.')[0] == nom)

INFOS = {'categorie': 'monstre', 'titre': "Myconide"}

def fabriquer():
    c = collection('myconide'); dans(c)
    r = pivot('myconide'); H = hauteur()
    for s, n in ((-1, 'G'), (1, 'D')):
        j = pivot(f'Jambe{n}', (s * H * .1, 0, H * .18), r)
        cylindre(f'Pied{n}', '#e8dcc0', H * .07, H * .06, H * .18, 8, (0, 0, -H * .18), j)
    corps = pivot('Corps', (0, 0, H * .18), r)
    cylindre('Tige', '#efe6cf', H * .17, H * .14, H * .4, 12, (0, 0, 0), corps, lisse=True)
    T = pivot('Tete', (0, 0, H * .4), corps)
    sphere('Chapeau', '#c8322a', H * .38, (0, 0, H * .1), (1, 1, .55), 16, 8, T)
    cylindre('Lamelles', '#d9c7a3', H * .34, H * .2, H * .05, 14, (0, 0, -H * .02), T)
    for k in range(7):
        a = k * 2 * math.pi / 7
        sphere(f'Pois{k}', '#ffffff', H * .06, (math.cos(a) * H * .24, math.sin(a) * H * .24, H * .22), (1, 1, .4), 6, 4, T)
    sphere('PoisHaut', '#ffffff', H * .07, (0, 0, H * .31), (1, 1, .4), 6, 4, T)
    for k in range(4):
        a = k * math.pi / 2 + .4
        sphere(f'Spore{k}', '#7ff3ff', H * .025, (math.cos(a) * H * .3, math.sin(a) * H * .3, -H * .05), (1, 1, 1), 6, 4, T, emis=3)
    for s in (-1, 1): sphere(f'Oeil{s}', '#1b1b1b', H * .035, (s * H * .06, -H * .155, H * .3), (1, .5, 1.2), 6, 4, corps)
    for s, n in ((-1, 'G'), (1, 'D')):
        b = pivot(f'Bras{n}', (s * H * .16, 0, H * .26), corps); b.rotation_euler = (0, s * .5, 0)
        cone(f'Racine{n}', '#d9c7a3', H * .04, H * .2, 5, (0, 0, 0), b, (math.pi, 0, 0))
    peindre(r)
    marche(r, duree=.8, ampl_jambe=.5, ampl_bras=.5, rebond=H * .05, roulis=.14)
    return r

def construire(ctx):
    preparer(fabriquer())
