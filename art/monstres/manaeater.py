"""Dévoreur de mana (palier 3, magique : anti-magie) : aberration flottante, grosse sphère violette
couverte de runes brisées, immense gueule dentée, tentacules ; il avale la magie. Insensible au Givre et au Mage.
Clé CR « manaeater »."""
import math
from communs.outils import collection, dans, pivot, peindre, sphere, cone, cylindre, boite, prisme, anneau, descendants
from communs.betes import yeux_bete
from communs.animations import flotte
from communs.export_jeu import preparer

# taille selon le facteur z proposé pour CR (même formule que communs/echelles.py) ; voir PALIERS.md
Z = 1.35
def hauteur(): return .40 * Z ** 1.8
def piece(r, nom): return next(o for o in descendants(r) if o.name.split('.')[0] == nom)

INFOS = {'categorie': 'monstre', 'titre': "Dévoreur de mana"}

def fabriquer():
    c = collection('devoreur_mana'); dans(c)
    r = pivot('devoreur_mana'); H = hauteur()
    corps = pivot('Corps', (0, 0, H * .35), r)
    sphere('Globe', '#5a2a7a', H * .32, (0, 0, 0), (1, 1, .95), 14, 9, corps)
    sphere('Gueule', '#2a0a2a', H * .2, (0, -H * .2, -H * .05), (1.1, .5, .7), 12, 6, corps)
    for k in range(7):
        a = (k - 3) * .28
        cone(f'Dent{k}', '#f4ead0', H * .025, H * .07, 4, (math.sin(a) * H * .2, -H * .29, H * .06), corps, (math.pi, 0, 0))
        cone(f'DentBas{k}', '#f4ead0', H * .025, H * .06, 4, (math.sin(a) * H * .18, -H * .28, -H * .15), corps)
    yeux_bete(corps, H * .06, -H * .26, H * .17, H * .11, '#4ad2ff', True)
    for k in range(5):
        a = k * 2 * math.pi / 5
        sphere(f'Rune{k}', '#c77dff', H * .03, (math.cos(a) * H * .3, math.sin(a) * H * .3 + H * .05, H * .1), (1, 1, .4), 6, 4, corps, emis=2)
    for k in range(5):
        a = k * 2 * math.pi / 5 + .3
        cone(f'Tentacule{k}', '#4a1a6a', H * .05, H * .35, 5, (math.cos(a) * H * .15, math.sin(a) * H * .15, -H * .25), corps, (math.pi + math.sin(a) * .4, -math.cos(a) * .4, 0))
    peindre(r, sol=.85)
    flotte(r, duree=1.6, ampl=H * .05, roulis=.1)
    return r

def construire(ctx):
    preparer(fabriquer())
