"""Hydre (palier 3, magique : se divise) : reptile vert-bleu trapu à trois longs cous et trois têtes
crêtées ; à sa mort, elle se sépare en têtes rampantes. Clé CR « hydra »."""
import math
from communs.outils import collection, dans, pivot, peindre, sphere, cone, cylindre, boite, prisme, anneau, descendants
from communs.betes import quadrupede, yeux_bete
from communs.animations import trot
from communs.export_jeu import preparer

# taille selon le facteur z proposé pour CR (même formule que communs/echelles.py) ; voir PALIERS.md
Z = 1.45
def hauteur(): return .40 * Z ** 1.8
def piece(r, nom): return next(o for o in descendants(r) if o.name.split('.')[0] == nom)

INFOS = {'categorie': 'monstre', 'titre': "Hydre"}

def fabriquer():
    c = collection('hydre'); dans(c)
    r = pivot('hydre'); H = hauteur()
    corps = quadrupede(r, dict(poil='#2f7a6a', poil2='#3f9a7a', ventre='#cfe08a', patte='#1f5a4a', yeux='#ffd34d',
                               museau='tortue', tete=.05, queue='#2f7a6a', largeur=.25, pattes=.3, epaisseur=.28, lqueue=.4), H * .55, H * 1.1)
    for k, a in enumerate((-.5, 0, .5)):
        cou = pivot(f'Cou{k}', (math.sin(a) * H * .12, -H * .35, H * .12), corps); cou.rotation_euler = (-.5, a, 0)
        cylindre(f'CouCyl{k}', '#2f7a6a', H * .07, H * .05, H * .45, 8, (0, 0, 0), cou, lisse=True)
        T = pivot(f'TeteH{k}', (0, 0, H * .47), cou); T.rotation_euler = (.9, 0, 0)
        sphere(f'Crane{k}', '#3f9a7a', H * .09, (0, 0, 0), (1, 1.35, .85), 10, 6, T)
        cone(f'Crete{k}', '#f08a2e', H * .04, H * .12, 4, (0, H * .04, H * .07), T, (-.8, 0, 0))
        yeux_bete(T, H * .02, -H * .07, H * .03, H * .04, '#ffd34d', False)
    peindre(r)
    trot(r, duree=.8, ampl=.4, rebond=H * .02, queue=.4)
    return r

def construire(ctx):
    preparer(fabriquer())
