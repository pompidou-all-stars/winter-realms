"""Rhinocéros de guerre (palier 2, sol) : énorme rhinocéros gris à double corne, caparaçon de plaques
d'acier et liserés d'or. Charge lourdement. Clé CR « rhino »."""
import math
from communs.outils import collection, dans, pivot, peindre, sphere, cone, cylindre, boite, prisme, anneau, descendants
from communs.betes import quadrupede
from communs.animations import trot
from communs.export_jeu import preparer

# taille selon le facteur z proposé pour CR (même formule que communs/echelles.py) ; voir PALIERS.md
Z = 1.3
def hauteur(): return .40 * Z ** 1.8
def piece(r, nom): return next(o for o in descendants(r) if o.name.split('.')[0] == nom)

INFOS = {'categorie': 'monstre', 'titre': "Rhinocéros de guerre"}

def fabriquer():
    c = collection('rhino_guerre'); dans(c)
    r = pivot('rhino_guerre'); H = hauteur()
    corps = quadrupede(r, dict(poil='#8a8f99', poil2='#9ea3ac', ventre='#7a7f89', patte='#6c717b', yeux='#ffffff',
                               museau='tortue', tete=.26, oreilles=1, queue='#6c717b', largeur=.27, pattes=.36, epaisseur=.3,
                               lqueue=.12), H * .8, H * 1.35)
    T = piece(r, 'Tete'); rt = H * .8 * .26
    cone('Corne1', '#f4ead0', rt * .28, rt * 1.0, 6, (0, -rt * 1.0, rt * .1), T, (-.35, 0, 0))
    cone('Corne2', '#f4ead0', rt * .18, rt * .5, 6, (0, -rt * .5, rt * .5), T, (-.25, 0, 0))
    for k in range(3):
        boite(f'Plaque{k}', '#5a5f69', H * .45, H * .22, H * .05, (0, -H * .18 + k * H * .24, H * .32 - k * H * .02), H * .02, corps, (.08, 0, 0))
        boite(f'Lisere{k}', '#e0b44e', H * .46, H * .03, H * .055, (0, -H * .28 + k * H * .24, H * .32 - k * H * .02), 0, corps)
    peindre(r)
    trot(r, duree=.8, ampl=.4, rebond=H * .03, queue=.2)
    return r

def construire(ctx):
    preparer(fabriquer())
