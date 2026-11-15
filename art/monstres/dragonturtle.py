"""Tortue-dragon (palier 3, magique : armure) : tortue colossale à tête de dragon cornue, carapace
bombée hérissée de pics, plaques de bronze. Blindée. Clé CR « dragonturtle »."""
import math
from communs.outils import collection, dans, pivot, peindre, sphere, cone, cylindre, boite, prisme, anneau, descendants
from communs.betes import quadrupede, yeux_bete
from communs.animations import trot
from communs.export_jeu import preparer

# taille selon le facteur z proposé pour CR (même formule que communs/echelles.py) ; voir PALIERS.md
Z = 1.45
def hauteur(): return .40 * Z ** 1.8
def piece(r, nom): return next(o for o in descendants(r) if o.name.split('.')[0] == nom)

INFOS = {'categorie': 'monstre', 'titre': "Tortue-dragon"}

def fabriquer():
    c = collection('tortue_dragon'); dans(c)
    r = pivot('tortue_dragon'); H = hauteur()
    corps = quadrupede(r, dict(poil='#4a8a6a', poil2='#5aa07a', patte='#3a6a52', yeux='#ff9f2e', museau='loup', tete=.24,
                               pattes=.28, largeur=.26, epaisseur=.16, lqueue=.25), H * .7, H * 1.3)
    sphere('Carapace', '#8a3a2a', H * .5, (0, H * .05, H * .04), (1, 1.2, .62), 14, 8, corps)
    anneau('Rebord', '#c9a25a', H * .5, H * .04, 16, 4, (0, H * .05, -H * .01), corps, echelle=(1, 1.2, 1), metal=.5)
    for k in range(7):
        a = k * 2 * math.pi / 7
        cone(f'Pic{k}', '#e8e2cf', H * .05, H * .16, 5, (math.cos(a) * H * .28, H * .05 + math.sin(a) * H * .33, H * .22), corps)
    cone('PicHaut', '#e8e2cf', H * .06, H * .2, 5, (0, H * .05, H * .32), corps)
    T = piece(r, 'Tete'); rt = H * .7 * .24
    for s in (-1, 1): cone(f'Corne{s}', '#e8e2cf', rt * .18, rt * .9, 5, (s * rt * .45, rt * .2, rt * .5), T, (-1.0, s * .3, 0))
    peindre(r)
    trot(r, duree=1.0, ampl=.35, rebond=H * .01, queue=.2)
    return r

def construire(ctx):
    preparer(fabriquer())
