"""Centaure messager (palier 2, magique : accéléré) : corps de cheval bai, buste d'homme en tunique
bleue, besace de messager, cor en bandoulière ; galope de plus en plus vite. Clé CR « centaur »."""
import math
from communs.outils import collection, dans, pivot, peindre, sphere, cone, cylindre, boite, prisme, anneau, descendants
from communs.betes import quadrupede
from communs.animations import trot
from communs.export_jeu import preparer

# taille selon le facteur z proposé pour CR (même formule que communs/echelles.py) ; voir PALIERS.md
Z = 1.15
def hauteur(): return .40 * Z ** 1.8
def piece(r, nom): return next(o for o in descendants(r) if o.name.split('.')[0] == nom)

INFOS = {'categorie': 'monstre', 'titre': "Centaure messager"}

def fabriquer():
    c = collection('centaure_messager'); dans(c)
    r = pivot('centaure_messager'); H = hauteur()
    corps = quadrupede(r, dict(poil='#8a5a34', poil2='#9a6a40', ventre='#a07448', patte='#3a2a1c', yeux='#ffffff',
                               museau='tortue', tete=.06, queue='#2b211c', largeur=.2, pattes=.55, epaisseur=.22, lqueue=.4), H * .6, H * 1.1)
    B = pivot('Buste', (0, -H * .3, H * .28), corps)
    cylindre('Torse', '#3a6ab0', H * .1, H * .13, H * .28, 10, (0, 0, 0), B, lisse=True)
    boite('Ceinture', '#4a321f', H * .27, H * .2, H * .04, (0, 0, H * .02), H * .01, B)
    T = pivot('Tete', (0, 0, H * .36), B)
    sphere('Visage', '#e2b48e', H * .1, (0, 0, 0), (1, 1, 1.05), 10, 8, T)
    sphere('Cheveux', '#5a3a22', H * .105, (0, H * .03, H * .03), (1, 1, .9), 10, 6, T)
    sphere('Nez', '#d29c76', H * .025, (0, -H * .1, -H * .01), (1, 1, 1), 6, 4, T)
    for s in (-1, 1): sphere(f'Oeil{s}', '#1b1b1b', H * .015, (s * H * .035, -H * .09, H * .02), (1, .5, 1), 4, 3, T)
    for s, n in ((-1, 'G'), (1, 'D')):
        b = pivot(f'Bras{n}', (s * H * .13, 0, H * .25), B); b.rotation_euler = (-.4, s * .2, 0)
        cylindre(f'BrasCyl{n}', '#e2b48e', H * .035, H * .03, H * .22, 6, (0, 0, -H * .22), b)
    anneau('Cor', '#e0b44e', H * .06, H * .015, 10, 3, (H * .12, H * .05, H * .1), B, (0, math.pi / 2, 0), metal=.7)
    boite('Besace', '#7a5a2a', H * .1, H * .06, H * .1, (-H * .14, 0, H * .02), H * .01, B)
    peindre(r)
    trot(r, duree=.45, ampl=.7, rebond=H * .04, queue=.6)
    return r

def construire(ctx):
    preparer(fabriquer())
