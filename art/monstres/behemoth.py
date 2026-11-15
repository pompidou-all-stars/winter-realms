"""Béhémoth (palier 3, sol) : bête titanesque à cuir violet sombre, échine hérissée de pics d'os,
quatre cornes, défenses, yeux rouges. Clé CR « behemoth »."""
import math
from communs.outils import collection, dans, pivot, peindre, sphere, cone, cylindre, boite, prisme, anneau, descendants
from communs.betes import quadrupede, yeux_bete
from communs.animations import trot
from communs.export_jeu import preparer

# taille selon le facteur z proposé pour CR (même formule que communs/echelles.py) ; voir PALIERS.md
Z = 1.7
def hauteur(): return .40 * Z ** 1.8
def piece(r, nom): return next(o for o in descendants(r) if o.name.split('.')[0] == nom)

INFOS = {'categorie': 'monstre', 'titre': "Béhémoth"}

def fabriquer():
    c = collection('behemoth'); dans(c)
    r = pivot('behemoth'); H = hauteur()
    corps = quadrupede(r, dict(poil='#4a3a5a', poil2='#5a4a6a', ventre='#6a5a6a', patte='#2f2538', crete='#e8e2cf', yeux='#ff3a3a',
                               museau='tortue', tete=.27, queue='#2f2538', largeur=.26, pattes=.42, epaisseur=.3, lqueue=.3), H * .78, H * 1.25)
    T = piece(r, 'Tete'); rt = H * .78 * .27
    for s in (-1, 1):
        cone(f'Corne{s}', '#e8e2cf', rt * .25, rt * 1.1, 6, (s * rt * .6, 0, rt * .5), T, (-.7, s * .6, 0))
        cone(f'CornePetite{s}', '#e8e2cf', rt * .15, rt * .5, 5, (s * rt * .35, -rt * .4, rt * .7), T, (-.4, s * .3, 0))
        cone(f'Defense{s}', '#fff3d6', rt * .12, rt * .6, 6, (s * rt * .4, -rt * 1.05, -rt * .4), T, (-.5, s * .3, 0))
    peindre(r)
    trot(r, duree=1.1, ampl=.35, rebond=H * .02, queue=.2)
    return r

def construire(ctx):
    preparer(fabriquer())
