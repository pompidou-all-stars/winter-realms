"""Phénix de givre (palier 3, volant) : grand oiseau de glace bleu pâle et blanc, ailes de plumes
lumineuses, longue traîne de plumes, aigrette de cristal. Volant : modèle centré sur z = 0. Clé CR « phoenix »."""
import math
from communs.outils import collection, dans, pivot, peindre, sphere, cone, cylindre, boite, prisme, anneau, descendants
from communs.betes import volant, yeux_bete
from communs.animations import battement
from communs.export_jeu import preparer

# taille selon le facteur z proposé pour CR (même formule que communs/echelles.py) ; voir PALIERS.md
Z = 1.3
def hauteur(): return .40 * Z ** 1.8
def piece(r, nom): return next(o for o in descendants(r) if o.name.split('.')[0] == nom)

INFOS = {'categorie': 'monstre', 'titre': "Phénix de givre"}

def fabriquer():
    c = collection('phenix_givre'); dans(c)
    r = pivot('phenix_givre'); H = hauteur()
    corps = volant(r, dict(aile='#bfeaff', forme='plumes', os='#ffffff'), H, H * 2.3)
    sphere('Tronc', '#9fdcff', H * .2, (0, H * .05, 0), (1, 1.4, .9), 12, 8, corps, emis=.6)
    sphere('Poitrail', '#f0fbff', H * .15, (0, -H * .12, H * .03), (1, 1, 1), 10, 6, corps)
    for k in range(5): cone(f'Traine{k}', '#bfeaff', H * .05, H * .6, 4, ((k - 2) * H * .05, H * .3, -H * .03), corps, (-math.pi / 2 + .1, 0, (k - 2) * .2), emis=.8)
    T = pivot('Tete', (0, -H * .3, H * .15), corps)
    sphere('Crane', '#f0fbff', H * .12, (0, 0, 0), (1, 1.1, 1), 10, 8, T)
    cone('Bec', '#4ad2ff', H * .05, H * .14, 6, (0, -H * .12, -H * .02), T, (1.9, 0, 0))
    for k in range(3): cone(f'Aigrette{k}', '#7ff3ff', H * .025, H * .2, 4, ((k - 1) * H * .04, H * .05, H * .1), T, (-.6, (k - 1) * .3, 0), emis=3)
    yeux_bete(T, H * .03, -H * .09, H * .04, H * .06, '#4ad2ff', False)
    peindre(r, sol=.85)
    battement(r, duree=.6, ampl=.6, flottement=H * .05)
    return r

def construire(ctx):
    preparer(fabriquer())
