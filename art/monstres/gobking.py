"""Roi gobelin (palier 1, boss) : gobelin obèse et rusé, couronne d'or, cape rouge à col d'hermine,
grosse bedaine, sceptre à pierre précieuse. Boss du palier 1. Clé CR « gobking »."""
import math
from communs.outils import collection, dans, pivot, peindre, sphere, cone, cylindre, boite, prisme, anneau, descendants
from communs.personnages import humanoide, baton
from communs.animations import marche
from communs.export_jeu import preparer

# taille selon le facteur z proposé pour CR (même formule que communs/echelles.py) ; voir PALIERS.md
Z = 1.2
def hauteur(): return .40 * Z ** 1.8
def piece(r, nom): return next(o for o in descendants(r) if o.name.split('.')[0] == nom)

INFOS = {'categorie': 'monstre', 'titre': "Roi gobelin"}

def fabriquer():
    c = collection('roi_gobelin'); dans(c)
    r = pivot('roi_gobelin'); H = hauteur()
    humanoide(r, dict(peau='#7cc04a', peau2='#9ad66a', tissu='#7a2a2a', torse='#e0b44e', cuir='#4a321f', botte='#3a2a1c',
                      metal='#e0b44e', accent='#e0b44e', carrure=1.35, tete=.16, jambes=.28, voute=.12, sourcils=1,
                      nez=('long', .4), oreilles=1.0, yeux='#ffd34d', couronne='#f2c14e', cape='#a8262a', epaulieres='or',
                      arme=lambda p, HH: baton(p, HH, '#ff4ad2', '#e0b44e')), H)
    B = piece(r, 'Buste')
    sphere('Bedaine', '#9ad66a', H * .17, (0, -H * .08, H * .08), (1, .9, .9), 12, 8, B)
    anneau('ColHermine', '#f7f4ee', H * .15, H * .04, 14, 4, (0, 0, H * .3), B)
    for k in range(4): sphere(f'Hermine{k}', '#1b1b1b', H * .015, ((k - 1.5) * H * .07, -H * .14, H * .32), (1, .5, 1.6), 4, 3, B)
    peindre(r)
    marche(r, duree=.9, ampl_jambe=.4, ampl_bras=.3, rebond=H * .05, roulis=.12)
    return r

def construire(ctx):
    preparer(fabriquer())
