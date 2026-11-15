"""Chimère (palier 3, sol) : lion à crinière fauve, tête de bouc noir aux cornes torsadées sur le dos
et serpent vert en guise de queue. Clé CR « chimera »."""
import math
from communs.outils import collection, dans, pivot, peindre, sphere, cone, cylindre, boite, prisme, anneau, descendants
from communs.betes import quadrupede, yeux_bete
from communs.animations import trot
from communs.export_jeu import preparer

# taille selon le facteur z proposé pour CR (même formule que communs/echelles.py) ; voir PALIERS.md
Z = 1.5
def hauteur(): return .40 * Z ** 1.8
def piece(r, nom): return next(o for o in descendants(r) if o.name.split('.')[0] == nom)

INFOS = {'categorie': 'monstre', 'titre': "Chimère"}

def fabriquer():
    c = collection('chimere'); dans(c)
    r = pivot('chimere'); H = hauteur()
    corps = quadrupede(r, dict(poil='#d9a441', poil2='#e8b85a', ventre='#f0d08a', patte='#b8862f', yeux='#ff7a2a',
                               museau='tortue', tete=.25, oreilles=1, queue='#4f9a3a', largeur=.22, pattes=.45, epaisseur=.25,
                               lqueue=.55), H * .75, H * 1.3)
    T = piece(r, 'Tete'); rt = H * .75 * .25
    sphere('Criniere', '#8a4a1a', rt * 1.35, (0, rt * .3, 0), (1.1, .9, 1.1), 12, 8, T)
    sphere('Truffe', '#3a2a1c', rt * .2, (0, -rt * 1.1, -rt * .1), (1.2, .8, .8), 6, 4, T)
    bouc = pivot('Bouc', (0, H * .12, H * .3), corps)
    cylindre('CouBouc', '#2b2b30', H * .06, H * .05, H * .18, 8, (0, 0, 0), bouc)
    sphere('TeteBouc', '#2b2b30', H * .09, (0, -H * .04, H * .22), (1, 1.2, 1), 10, 6, bouc)
    for s in (-1, 1): cone(f'CorneBouc{s}', '#cfc5a8', H * .03, H * .2, 5, (s * H * .05, 0, H * .28), bouc, (.6, s * .6, 0))
    yeux_bete(bouc, H * .02, -H * .11, H * .24, H * .04, '#ffd34d', False)
    q = piece(r, 'Queue')
    sphere('TeteSerpent', '#4f9a3a', H * .07, (0, H * .5, H * .08), (1, 1.3, .8), 8, 6, q)
    yeux_bete(q, H * .015, H * .44, H * .11, H * .03, '#ffd34d', False)
    peindre(r)
    trot(r, duree=.6, ampl=.55, rebond=H * .03, queue=.5)
    return r

def construire(ctx):
    preparer(fabriquer())
