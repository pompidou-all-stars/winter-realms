"""Tortue (CR turtle, blindée) : grosse tortue à carapace bombée en plaques hexagonales cerclées de laiton,
pointes de métal. Lente."""
import math
from communs.outils import collection, dans, pivot, peindre, sphere, cone, cylindre, anneau
from communs.betes import quadrupede
from communs.animations import trot
from communs.echelles import hauteur
from communs.export_jeu import preparer

INFOS = {'categorie': 'monstre', 'titre': "Tortue"}

def fabriquer():
    c = collection('tortue'); dans(c)
    r = pivot('tortue'); H = hauteur('tortue')
    corps = quadrupede(r, dict(poil='#7a9a4a', poil2='#9cc063', patte='#6a8a3a', museau='tortue', tete=.22, pattes=.28,
                               largeur=.3, epaisseur=.16, lqueue=.15), H * .75, H * 1.4)
    sphere('Carapace', '#8a6a3a', H * .55, (0, H * .05, H * .02), (1, 1.15, .62), 14, 8, corps)
    anneau('Rebord', '#c9a25a', H * .55, H * .045, 16, 4, (0, H * .05, -H * .02), corps, echelle=(1, 1.15, 1), metal=.5)
    for k in range(6):
        a = k * math.pi / 3
        cylindre(f'Plaque{k}', '#a5834a', H * .14, H * .13, H * .03, 6, (math.cos(a) * H * .3, H * .05 + math.sin(a) * H * .34, H * .22), corps,
                 rot=(-math.sin(a) * .5, math.cos(a) * .5, 0))
    cylindre('PlaqueHaut', '#a5834a', H * .15, H * .14, H * .03, 6, (0, H * .05, H * .33), corps)
    for k in range(4):
        a = k * math.pi / 2 + math.pi / 4
        cone(f'Pointe{k}', '#c9ced6', H * .04, H * .12, 5, (math.cos(a) * H * .28, H * .05 + math.sin(a) * H * .32, H * .27), corps, metal=.6)
    peindre(r)
    trot(r, duree=.9, ampl=.4, rebond=H * .01, queue=.2)
    return r

def construire(ctx):
    preparer(fabriquer())
