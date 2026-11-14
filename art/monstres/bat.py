"""Chauve-souris (CR bat) : petite boule violette aux grandes oreilles, yeux jaunes, crocs, ailes membraneuses.
Volante : modèle centré sur z = 0, le jeu ajoute la hauteur de vol."""
import math
from communs.outils import collection, dans, pivot, peindre, sphere, cone
from communs.betes import volant, yeux_bete
from communs.animations import battement
from communs.echelles import hauteur
from communs.export_jeu import preparer

INFOS = {'categorie': 'monstre', 'titre': "Chauve-souris"}

def fabriquer():
    c = collection('chauve_souris'); dans(c)
    r = pivot('chauve_souris'); H = hauteur('chauve_souris')
    corps = volant(r, dict(aile='#5a3f80', os='#3d2a5a'), H, H * 1.9)
    sphere('Boule', '#7d5ba6', H * .32, (0, 0, 0), (1, .9, 1), 12, 8, corps)
    sphere('Ventre', '#a585cf', H * .2, (0, -H * .14, -H * .05), (1, .6, 1), 8, 6, corps)
    for s in (-1, 1):
        cone(f'Oreille{s}', '#7d5ba6', H * .1, H * .3, 4, (s * H * .14, 0, H * .24), corps, (0, s * .35, 0))
        cone(f'Croc{s}', '#ffffff', H * .025, H * .08, 4, (s * H * .05, -H * .28, -H * .08), corps, (math.pi, 0, 0))
    yeux_bete(corps, H * .07, -H * .27, H * .06, H * .1, '#ffe45e', False)
    peindre(r, sol=.8)
    battement(r, duree=.28, ampl=.9, flottement=H * .08)
    return r

def construire(ctx):
    preparer(fabriquer())
