"""Rat des neiges (palier 1, sol) : gros rat au pelage blanc-gris, oreilles et longue queue roses, yeux rouges,
dents jaunes. Rapide et nerveux. Clé CR « rat »."""
import math
from communs.outils import collection, dans, pivot, peindre, sphere, cone, cylindre, boite, prisme, anneau, descendants
from communs.betes import quadrupede
from communs.animations import trot
from communs.export_jeu import preparer

# taille selon le facteur z proposé pour CR (même formule que communs/echelles.py) ; voir PALIERS.md
Z = 0.7
def hauteur(): return .40 * Z ** 1.8
def piece(r, nom): return next(o for o in descendants(r) if o.name.split('.')[0] == nom)

INFOS = {'categorie': 'monstre', 'titre': "Rat des neiges"}

def fabriquer():
    c = collection('rat_neiges'); dans(c)
    r = pivot('rat_neiges'); H = hauteur()
    quadrupede(r, dict(poil='#d9dfe4', poil2='#eef2f5', ventre='#f7f9fa', patte='#e8a3a8', yeux='#ff3a4a', oreilles=0,
                       museau='loup', tete=.26, queue='#e8a3a8', largeur=.2, pattes=.35, epaisseur=.26, lqueue=.95), H * .7, H * 1.4)
    T = piece(r, 'Tete'); rt = H * .7 * .26
    for s in (-1, 1): sphere(f'OreilleRonde{s}', '#e8a3a8', rt * .38, (s * rt * .6, rt * .1, rt * .7), (1, .35, 1), 8, 5, T)
    boite('Dents', '#f2d36a', rt * .25, rt * .1, rt * .2, (0, -rt * 1.7, -rt * .55), 0, T)
    piece(r, 'Queue').rotation_euler = (-.3, 0, 0)  # longue queue qui traîne derrière
    peindre(r)
    trot(r, duree=.32, ampl=.75, rebond=H * .05, queue=.7)
    return r

def construire(ctx):
    preparer(fabriquer())
