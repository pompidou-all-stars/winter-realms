"""Élémentaire de feu (palier 3, sol) — kit 2.40 : colosse de roche en fusion, flammes en guise de chevelure et d'épaules,
fissures incandescentes, poings de lave, traîne de feu."""
from communs.creatures import *
INFOS = {'categorie': 'monstre', 'titre': "Élémentaire de feu"}

def pieces(K):
    t, e, p = K.j('tete'), K.j('epaule.L'), K.j('poitrine')
    K.lueurs += [cone(f'Flamme{k}', '#ffb347', 'Tete', (x, t.y + .02, t.z + .12), .05, .002, .2 + .05 * (k % 2), rot=(-.4, x * 3, 0), seg=5)
                 for k, x in enumerate((-.06, 0, .06))]
    K.lueurs += [cone(f'FlammeE{k}.{n}', '#ffb347', f'Bras.{n}', (s * e.x, e.y + .02 * k, e.z + .05), .045, .002, .16, rot=(-.3, s * .4, 0), seg=5)
                 for s, n in ((1, 'L'), (-1, 'R')) for k in range(2)]
    K.lueurs += [plaque(f'Fissure{k}', '#ffcf3a', 'Torse', (x, -.17, p.z + z), .06, .01, .01, rot=(0, 0, a)) for k, (x, z, a) in enumerate(((-.07, .03, .6), (.06, -.03, -.5)))]
    return []

def construire(ctx):
    bipede('elementaire_feu', dict(z=1.4, peau=('#4a2a20', '#6a3a28', '#2a1a14'), bas='#ff7a1a', tete='demon', tete_r=.85,
                                   bas_du_corps='traine', carrure=1.35, bras=1.2, muscle=.6, voute=.4, relief=RELIEF_PIERRE,
                                   oeil='#ffb347', pieces=pieces))
