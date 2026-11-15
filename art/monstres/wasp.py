"""Guêpe des glaces (palier 1, volant) : grosse guêpe rayée jaune et bleu nuit, dard de glace,
ailes translucides bleutées, yeux à facettes. Volante : modèle centré sur z = 0. Clé CR « wasp »."""
import math
from communs.outils import collection, dans, pivot, peindre, sphere, cone, cylindre, boite, prisme, anneau, descendants
from communs.betes import volant, yeux_bete
from communs.animations import battement
from communs.export_jeu import preparer

# taille selon le facteur z proposé pour CR (même formule que communs/echelles.py) ; voir PALIERS.md
Z = 0.7
def hauteur(): return .40 * Z ** 1.8
def piece(r, nom): return next(o for o in descendants(r) if o.name.split('.')[0] == nom)

INFOS = {'categorie': 'monstre', 'titre': "Guêpe des glaces"}

def fabriquer():
    c = collection('guepe_glaces'); dans(c)
    r = pivot('guepe_glaces'); H = hauteur()
    corps = volant(r, dict(aile='#cdeefc', os='#8fbcd0'), H, H * 1.8)
    sphere('Thorax', '#2a3550', H * .2, (0, -H * .05, 0), (1, 1.1, 1), 10, 6, corps)
    for k, col in enumerate(('#f5c534', '#2a3550', '#f5c534', '#2a3550')):
        sphere(f'Abdomen{k}', col, H * (.22 - k * .035), (0, H * (.2 + k * .12), -H * (.02 + k * .04)), (1, .75, 1), 10, 6, corps)
    cone('Dard', '#bff6ff', H * .05, H * .2, 6, (0, H * .62, -H * .17), corps, (-math.pi / 2 - .3, 0, 0), emis=1)
    T = pivot('Tete', (0, -H * .3, H * .02), corps)
    sphere('Crane', '#f5c534', H * .15, (0, 0, 0), (1, .9, 1), 10, 6, T)
    yeux_bete(T, H * .08, -H * .07, H * .04, H * .09, '#3a2f8a', False)
    for s in (-1, 1): cone(f'Antenne{s}', '#2a3550', H * .015, H * .2, 4, (s * H * .05, -H * .05, H * .12), T, (.5, s * .4, 0))
    for s in (-1, 1): cone(f'Patte{s}', '#2a3550', H * .03, H * .18, 4, (s * H * .1, 0, -H * .15), corps, (math.pi - .3, s * .3, 0))
    peindre(r, sol=.8)
    battement(r, duree=.12, ampl=.6, flottement=H * .06)
    return r

def construire(ctx):
    preparer(fabriquer())
