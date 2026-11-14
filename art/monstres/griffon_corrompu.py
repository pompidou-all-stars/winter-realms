"""Griffon corrompu (CR griffon) : corps de lion doré, tête d'aigle blanche, bec orange, ailes de plumes
dont les pointes sont gagnées par une corruption violette. Volant."""
import math
from outils import collection, dans, pivot, peindre, sphere, cone, prisme
from betes import volant, yeux_bete
from animations import battement
from echelles import hauteur

def fabriquer():
    c = collection('griffon_corrompu'); dans(c)
    r = pivot('griffon_corrompu'); H = hauteur('griffon')
    corps = volant(r, dict(aile='#f3e3b3', forme='plumes', os='#8a4fb0'), H, H * 2.0)
    sphere('Tronc', '#d9a441', H * .28, (0, H * .12, -H * .02), (1, 1.4, .85), 12, 8, corps)
    sphere('Poitrail', '#fff4d6', H * .22, (0, -H * .2, H * .05), (1, 1, 1), 10, 6, corps)
    for s in (-1, 1):
        cone(f'Patte{s}', '#d9a441', H * .06, H * .25, 6, (s * H * .14, H * .3, -H * .15), corps, (.6, 0, 0))
        cone(f'Serre{s}', '#e8a03a', H * .05, H * .18, 5, (s * H * .1, -H * .22, -H * .15), corps, (-.3, 0, 0))
    T = pivot('Tete', (0, -H * .36, H * .16), corps)
    sphere('Crane', '#fff4d6', H * .17, (0, 0, 0), (1, 1.1, 1), 10, 8, T)
    cone('Bec', '#f08a2e', H * .07, H * .2, 6, (0, -H * .15, -H * .02), T, (1.9, 0, 0))
    for s in (-1, 1):
        prisme(f'Aigrette{s}', '#8a4fb0', [(0, 0), (s * H * .06, H * .2), (s * H * .1, H * .05)], H * .02, (s * H * .06, H * .05, H * .1), T, emis=.6)
    yeux_bete(T, H * .045, -H * .12, H * .05, H * .08, '#c77dff', False)
    q = pivot('Queue', (0, H * .48, 0), corps)
    cone('QueueCone', '#d9a441', H * .04, H * .3, 5, (0, 0, 0), q, (-math.pi / 2 - .2, 0, 0))
    sphere('Touffe', '#8a4fb0', H * .06, (0, H * .3, -H * .06), (1, 1.3, 1), 6, 4, q)
    peindre(r, sol=.8)
    battement(r, duree=.45, ampl=.7, flottement=H * .06)
    return r

if __name__ == '__main__': fabriquer()
