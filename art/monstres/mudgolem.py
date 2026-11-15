"""Golem de boue (palier 2, magique : se divise) : gros tas de boue brune animé, pierres et touffes
d'herbe incrustées, yeux de braise ; se divise en petits golems à sa mort. Clé CR « mudgolem »."""
import math
from communs.outils import collection, dans, pivot, peindre, sphere, cone, cylindre, boite, prisme, anneau, descendants
from communs.betes import gelee, yeux_bete
from communs.animations import saut
from communs.export_jeu import preparer

# taille selon le facteur z proposé pour CR (même formule que communs/echelles.py) ; voir PALIERS.md
Z = 1.15
def hauteur(): return .40 * Z ** 1.8
def piece(r, nom): return next(o for o in descendants(r) if o.name.split('.')[0] == nom)

INFOS = {'categorie': 'monstre', 'titre': "Golem de boue"}

def fabriquer():
    c = collection('golem_boue'); dans(c)
    r = pivot('golem_boue'); H = hauteur()
    corps = gelee(r, H * .72, '#6b4a2a', '#83603a'); H = H * .72  # tas plus compact
    for k, (x, y, z) in enumerate(((.35, -.2, .45), (-.4, .1, .35), (.1, .3, .7), (-.2, -.35, .2), (.3, .25, .25))):
        sphere(f'Caillou{k}', '#8a8f99', H * .08, (x * H, y * H, z * H), (1, .9, .8), 6, 4, corps)
    for k, (x, y) in enumerate(((-.15, .1), (.2, -.05))):
        cone(f'Herbe{k}', '#5a8a3a', H * .04, H * .14, 4, (x * H, y * H, H * .75), corps)
    for o in list(c.objects):
        if o.name.startswith('Oeil'): o.data.materials[0] = __import__('communs.outils', fromlist=['mat']).mat('#ff7a2a', emis=3)
    peindre(r, sol=.75)
    saut(r, duree=.9, ecrase=.2, hauteur=H * .1)
    return r

def construire(ctx):
    preparer(fabriquer())
