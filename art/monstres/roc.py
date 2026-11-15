"""Oiseau-roc (palier 3, volant) : aigle gigantesque au plumage brun, tête blanche, bec jaune crochu,
serres énormes. Le plus grand des volants. Volant : modèle centré sur z = 0. Clé CR « roc »."""
import math
from communs.outils import collection, dans, pivot, peindre, sphere, cone, cylindre, boite, prisme, anneau, descendants
from communs.betes import volant, yeux_bete
from communs.animations import battement
from communs.export_jeu import preparer

# taille selon le facteur z proposé pour CR (même formule que communs/echelles.py) ; voir PALIERS.md
Z = 1.45
def hauteur(): return .40 * Z ** 1.8
def piece(r, nom): return next(o for o in descendants(r) if o.name.split('.')[0] == nom)

INFOS = {'categorie': 'monstre', 'titre': "Oiseau-roc"}

def fabriquer():
    c = collection('oiseau_roc'); dans(c)
    r = pivot('oiseau_roc'); H = hauteur()
    corps = volant(r, dict(aile='#6b4a2f', forme='plumes', os='#4a321f'), H, H * 2.4)
    sphere('Tronc', '#7a5634', H * .22, (0, H * .05, 0), (1, 1.4, .85), 12, 8, corps)
    for k in range(3): cone(f'Queue{k}', '#5a3a22', H * .06, H * .3, 4, ((k - 1) * H * .06, H * .35, 0), corps, (-math.pi / 2, 0, (k - 1) * .25))
    for s in (-1, 1): cone(f'Serre{s}', '#e8b43a', H * .05, H * .2, 5, (s * H * .1, H * .05, -H * .2), corps, (math.pi - .3, 0, 0))
    T = pivot('Tete', (0, -H * .3, H * .1), corps)
    sphere('Crane', '#f4efe0', H * .13, (0, 0, 0), (1, 1.1, 1), 10, 8, T)
    cone('Bec', '#f2c14e', H * .06, H * .17, 6, (0, -H * .12, -H * .02), T, (2.1, 0, 0))
    yeux_bete(T, H * .03, -H * .1, H * .04, H * .07, '#ffd34d', False)
    peindre(r, sol=.8)
    battement(r, duree=.8, ampl=.5, flottement=H * .05)
    return r

def construire(ctx):
    preparer(fabriquer())
