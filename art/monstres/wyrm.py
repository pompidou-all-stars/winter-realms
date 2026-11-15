"""Ver des neiges (palier 3, sol) : immense ver blanc à anneaux, gueule ronde garnie de crocs de glace,
plaques bleutées sur le dos ; il rampe en ondulant. Clé CR « wyrm »."""
import math
from communs.outils import collection, dans, pivot, peindre, sphere, cone, cylindre, boite, prisme, anneau, descendants
from communs.betes import yeux_bete
from communs.animations import flotte
from communs.export_jeu import preparer

# taille selon le facteur z proposé pour CR (même formule que communs/echelles.py) ; voir PALIERS.md
Z = 1.5
def hauteur(): return .40 * Z ** 1.8
def piece(r, nom): return next(o for o in descendants(r) if o.name.split('.')[0] == nom)

INFOS = {'categorie': 'monstre', 'titre': "Ver des neiges"}

def fabriquer():
    c = collection('ver_neiges'); dans(c)
    r = pivot('ver_neiges'); H = hauteur()
    corps = pivot('Corps', (0, 0, 0), r)
    for k in range(6):
        rk = H * (.24 - k * .025)
        sphere(f'Anneau{k}', '#eef2f5' if k % 2 else '#dfe7ee', rk, (0, k * H * .26, rk), (1, 1.1, .9), 10, 6, corps)
        cone(f'Plaque{k}', '#9fd0ea', rk * .5, rk * .5, 4, (0, k * H * .26, rk * 1.8), corps)
    T = pivot('Tete', (0, -H * .2, H * .38), corps); T.rotation_euler = (-.3, 0, 0)
    sphere('Crane', '#eef2f5', H * .27, (0, 0, 0), (1, 1, 1), 12, 8, T)
    cylindre('Gueule', '#7a2a3a', H * .17, H * .17, H * .05, 12, (0, -H * .26, 0), T, rot=(math.pi / 2, 0, 0))
    for k in range(8):
        a = k * math.pi / 4
        cone(f'Croc{k}', '#d8f8ff', H * .03, H * .1, 4, (math.cos(a) * H * .15, -H * .28, math.sin(a) * H * .15), T, (math.pi / 2, 0, 0), emis=.6)
    yeux_bete(T, H * .04, -H * .18, H * .18, H * .14, '#4ad2ff', False)
    peindre(r)
    flotte(r, duree=1.4, ampl=H * .04, roulis=.08)
    return r

def construire(ctx):
    preparer(fabriquer())
