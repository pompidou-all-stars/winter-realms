"""Dragon ancien (CR dragon) : dragon rouge au ventre doré, long cou, cornes ivoire, yeux jaunes,
grandes ailes membraneuses, queue à pointe. Le plus grand des volants."""
import math
from communs.outils import collection, dans, pivot, peindre, sphere, cone, cylindre, prisme
from communs.betes import volant, yeux_bete
from communs.animations import battement
from communs.echelles import hauteur
from communs.export_jeu import preparer

INFOS = {'categorie': 'monstre', 'titre': "Dragon ancien"}

def fabriquer():
    c = collection('dragon_ancien'); dans(c)
    r = pivot('dragon_ancien'); H = hauteur('dragon')
    corps = volant(r, dict(aile='#a02c2c', os='#6e1f1f'), H, H * 2.1)
    sphere('Tronc', '#d6453d', H * .25, (0, H * .05, 0), (1, 1.5, .85), 12, 8, corps)
    sphere('Ventre', '#f6cf6b', H * .18, (0, -H * .05, -H * .08), (1, 1.6, .6), 10, 6, corps)
    for k in range(4):
        cone(f'Ecaille{k}', '#f3e3b3', H * .03, H * .08, 4, (0, -H * .15 + k * H * .12, H * .2), corps, (.3, 0, 0))
    for s in (-1, 1):
        cone(f'Patte{s}', '#b83a33', H * .05, H * .2, 6, (s * H * .12, H * .2, -H * .15), corps, (.5, 0, 0))
    cou = pivot('Cou', (0, -H * .3, H * .08), corps); cou.rotation_euler = (-.6, 0, 0)
    cylindre('CouCyl', '#d6453d', H * .1, H * .08, H * .3, 8, (0, 0, 0), cou, lisse=True)
    T = pivot('Tete', (0, 0, H * .32), cou); T.rotation_euler = (.75, 0, 0)
    sphere('Crane', '#d6453d', H * .14, (0, 0, 0), (1, 1.2, .9), 10, 8, T)
    sphere('Machoire', '#e8695f', H * .1, (0, -H * .14, -H * .03), (1, 1.3, .6), 8, 6, T)
    for s in (-1, 1):
        cone(f'Corne{s}', '#f3e3b3', H * .035, H * .2, 5, (s * H * .08, H * .06, H * .08), T, (-1.1, s * .3, 0))
        sphere(f'Narine{s}', '#6e1f1f', H * .015, (s * H * .035, -H * .26, 0), (1, 1, 1), 6, 4, T)
    yeux_bete(T, H * .035, -H * .1, H * .06, H * .08, '#ffe45e', False)
    q = pivot('Queue', (0, H * .4, 0), corps)
    cone('QueueCone', '#d6453d', H * .08, H * .55, 6, (0, 0, 0), q, (-math.pi / 2 + .15, 0, 0))
    prisme('Dard', '#f3e3b3', [(-H * .07, 0), (0, H * .1), (H * .07, 0), (0, -H * .03)], H * .02, (0, H * .55, -H * .08), q, (math.pi / 2, 0, 0))
    peindre(r, sol=.8)
    battement(r, duree=.7, ampl=.55, flottement=H * .05)
    return r

def construire(ctx):
    preparer(fabriquer())
