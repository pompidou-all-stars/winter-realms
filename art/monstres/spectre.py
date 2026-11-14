"""Spectre (CR spectre, invisible) : fantôme encapuchonné, voile pâle aux bords déchirés, visage d'ombre
et yeux cyan. Flotte au ras du sol (le jeu le rend translucide quand il est caché)."""
import math
from communs.outils import collection, dans, pivot, peindre, sphere, cone, cylindre, prisme
from communs.animations import flotte
from communs.echelles import hauteur
from communs.export_jeu import preparer

INFOS = {'categorie': 'monstre', 'titre': "Spectre"}

def fabriquer():
    c = collection('spectre'); dans(c)
    r = pivot('spectre'); H = hauteur('spectre')
    corps = pivot('Corps', (0, 0, H * .08), r)
    cylindre('Voile', '#d7defa', H * .32, H * .16, H * .6, 12, (0, 0, 0), corps, lisse=True)
    for k in range(6):
        a = k * math.pi / 3
        cone(f'Lambeau{k}', '#c3cdf2', H * .08, H * .18, 4, (math.cos(a) * H * .26, math.sin(a) * H * .26, H * .02), corps, (math.pi, 0, a))
    T = pivot('Tete', (0, 0, H * .62), corps)
    sphere('Capuche', '#d7defa', H * .2, (0, 0, 0), (1, 1, 1.15), 12, 8, T)
    sphere('Ombre', '#2a2f52', H * .14, (0, -H * .1, -H * .01), (1, .6, 1.1), 10, 6, T)
    for s in (-1, 1): sphere(f'Oeil{s}', '#7ff3ff', H * .035, (s * H * .05, -H * .17, H * .01), (1, .5, 1.3), 6, 4, T, emis=4)
    cone('PointeCapuche', '#d7defa', H * .1, H * .2, 6, (0, H * .12, H * .15), T, (-1.1, 0, 0))
    for s, n in ((-1, 'G'), (1, 'D')):
        b = pivot(f'Bras{n}', (s * H * .2, 0, H * .48), corps); b.rotation_euler = (-.6, 0, 0)
        cone(f'Manche{n}', '#c3cdf2', H * .07, H * .3, 6, (0, 0, -H * .3), b)
        sphere(f'Main{n}', '#2a2f52', H * .035, (0, 0, -H * .32), (1, 1, 1), 6, 4, b)
    peindre(r, sol=.85)
    flotte(r, duree=1.6, ampl=H * .08)
    return r

def construire(ctx):
    preparer(fabriquer())
