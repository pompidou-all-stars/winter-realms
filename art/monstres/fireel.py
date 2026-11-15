"""Élémentaire de feu (palier 3, sol) : torse de braises et de flammes orange qui flotte au ras du sol,
cœur blanc incandescent, bras de feu, couronne de flammes. Clé CR « fireel »."""
import math
from communs.outils import collection, dans, pivot, peindre, sphere, cone, cylindre, boite, prisme, anneau, descendants
from communs.betes import yeux_bete
from communs.animations import flotte
from communs.export_jeu import preparer

# taille selon le facteur z proposé pour CR (même formule que communs/echelles.py) ; voir PALIERS.md
Z = 1.4
def hauteur(): return .40 * Z ** 1.8
def piece(r, nom): return next(o for o in descendants(r) if o.name.split('.')[0] == nom)

INFOS = {'categorie': 'monstre', 'titre': "Élémentaire de feu"}

def fabriquer():
    c = collection('elementaire_feu'); dans(c)
    r = pivot('elementaire_feu'); H = hauteur()
    corps = pivot('Corps', (0, 0, H * .1), r)
    cone('Base', '#d8401a', H * .22, H * .5, 10, (0, 0, H * .42), corps, (math.pi, 0, 0), emis=1.5)
    sphere('Torse', '#ff7a1a', H * .26, (0, 0, H * .45), (1, .85, 1.1), 12, 8, corps, emis=2)
    sphere('Coeur', '#fff2b0', H * .1, (0, -H * .2, H * .45), (1, .6, 1), 8, 6, corps, emis=4)
    T = pivot('Tete', (0, 0, H * .78), corps)
    sphere('Crane', '#ff9a2a', H * .14, (0, 0, 0), (1, 1, 1.1), 10, 8, T, emis=2)
    for k in range(5):
        a = k * 2 * math.pi / 5
        cone(f'Flamme{k}', '#ffcf4a', H * .05, H * .2, 5, (math.cos(a) * H * .08, math.sin(a) * H * .08, H * .1), T, (math.sin(a) * .7, -math.cos(a) * .7, 0), emis=3)
    yeux_bete(T, H * .03, -H * .12, H * .02, H * .05, '#ffffff', False)
    for s, n in ((-1, 'G'), (1, 'D')):
        b = pivot(f'Bras{n}', (s * H * .26, 0, H * .55), corps); b.rotation_euler = (-.4, s * .4, 0)
        cone(f'BrasFeu{n}', '#ff7a1a', H * .08, H * .35, 6, (0, 0, -H * .35), b, emis=2)
    peindre(r, sol=.9)
    flotte(r, duree=1.2, ampl=H * .05, roulis=.1)
    return r

def construire(ctx):
    preparer(fabriquer())
