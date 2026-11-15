"""Vouivre (palier 2, volant) : petit dragon vert émeraude à deux pattes, cou souple, ailes membraneuses
vert sombre, queue terminée par un dard. Volante : modèle centré sur z = 0. Clé CR « wyvern »."""
import math
from communs.outils import collection, dans, pivot, peindre, sphere, cone, cylindre, boite, prisme, anneau, descendants
from communs.betes import volant, yeux_bete, aile
from communs.animations import battement
from communs.export_jeu import preparer

# taille selon le facteur z proposé pour CR (même formule que communs/echelles.py) ; voir PALIERS.md
Z = 1.15
def hauteur(): return .40 * Z ** 1.8
def piece(r, nom): return next(o for o in descendants(r) if o.name.split('.')[0] == nom)

INFOS = {'categorie': 'monstre', 'titre': "Vouivre"}

def fabriquer():
    c = collection('vouivre'); dans(c)
    r = pivot('vouivre'); H = hauteur()
    corps = volant(r, dict(aile='#2f7a4a', os='#1f5a34'), H, H * 2.1)
    sphere('Tronc', '#3fa060', H * .22, (0, H * .05, 0), (1, 1.5, .85), 12, 8, corps)
    sphere('Ventre', '#cfe08a', H * .15, (0, -H * .02, -H * .07), (1, 1.6, .6), 10, 6, corps)
    for s in (-1, 1): cone(f'Patte{s}', '#2f7a4a', H * .05, H * .2, 6, (s * H * .1, H * .15, -H * .15), corps, (.5, 0, 0))
    cou = pivot('Cou', (0, -H * .28, H * .06), corps); cou.rotation_euler = (-.7, 0, 0)
    cylindre('CouCyl', '#3fa060', H * .08, H * .06, H * .3, 8, (0, 0, 0), cou, lisse=True)
    T = pivot('Tete', (0, 0, H * .32), cou); T.rotation_euler = (.85, 0, 0)
    sphere('Crane', '#3fa060', H * .12, (0, 0, 0), (1, 1.3, .85), 10, 8, T)
    for s in (-1, 1): cone(f'Corne{s}', '#e8e2cf', H * .025, H * .15, 5, (s * H * .06, H * .06, H * .06), T, (-1.2, s * .3, 0))
    yeux_bete(T, H * .03, -H * .1, H * .04, H * .06, '#ffe45e', False)
    q = pivot('Queue', (0, H * .38, 0), corps)
    cone('QueueCone', '#3fa060', H * .07, H * .6, 6, (0, 0, 0), q, (-math.pi / 2 + .15, 0, 0))
    prisme('Dard', '#e8e2cf', [(-H * .06, 0), (0, H * .12), (H * .06, 0)], H * .02, (0, H * .6, -H * .08), q, (math.pi / 2, 0, 0))
    peindre(r, sol=.8)
    battement(r, duree=.55, ampl=.6, flottement=H * .06)
    return r

def construire(ctx):
    preparer(fabriquer())
