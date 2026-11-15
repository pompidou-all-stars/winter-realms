"""Harpie (palier 1, volant) : femme-oiseau à la chevelure sauvage violette, plumage gris,
grandes ailes de plumes, serres jaunes, yeux jaunes. Volante : modèle centré sur z = 0. Clé CR « harpy »."""
import math
from communs.outils import collection, dans, pivot, peindre, sphere, cone, cylindre, boite, prisme, anneau, descendants
from communs.betes import volant, yeux_bete
from communs.animations import battement
from communs.export_jeu import preparer

# taille selon le facteur z proposé pour CR (même formule que communs/echelles.py) ; voir PALIERS.md
Z = 0.85
def hauteur(): return .40 * Z ** 1.8
def piece(r, nom): return next(o for o in descendants(r) if o.name.split('.')[0] == nom)

INFOS = {'categorie': 'monstre', 'titre': "Harpie"}

def fabriquer():
    c = collection('harpie'); dans(c)
    r = pivot('harpie'); H = hauteur()
    corps = volant(r, dict(aile='#9aa4b8', forme='plumes', os='#5a4a7a'), H, H * 2.0)
    sphere('Plumage', '#9aa4b8', H * .22, (0, H * .1, -H * .05), (1, 1.3, 1), 10, 6, corps)
    sphere('Buste', '#e2b48e', H * .16, (0, -H * .12, H * .08), (1, .8, 1.1), 10, 6, corps)
    for k in range(3): cone(f'Queue{k}', '#7a84a0', H * .05, H * .3, 4, ((k - 1) * H * .06, H * .4, -H * .05), corps, (-math.pi / 2 + .2, 0, (k - 1) * .3))
    for s in (-1, 1):
        cone(f'Serre{s}', '#e8b43a', H * .04, H * .2, 5, (s * H * .08, H * .05, -H * .22), corps, (math.pi - .4, 0, 0))
    T = pivot('Tete', (0, -H * .2, H * .3), corps)
    sphere('Crane', '#e2b48e', H * .13, (0, 0, 0), (1, 1, 1.05), 10, 8, T)
    sphere('Chevelure', '#6a3a8a', H * .15, (0, H * .05, H * .04), (1.1, 1, 1.1), 10, 6, T)
    for k in range(4): cone(f'Meche{k}', '#6a3a8a', H * .05, H * .2, 4, ((k - 1.5) * H * .07, H * .12, H * .08), T, (-1.2, (k - 1.5) * .3, 0))
    cone('Nez', '#d29c76', H * .03, H * .07, 5, (0, -H * .12, -H * .01), T, (1.6, 0, 0))
    yeux_bete(T, H * .03, -H * .11, H * .03, H * .05, '#ffd34d', False)
    peindre(r, sol=.8)
    battement(r, duree=.4, ampl=.75, flottement=H * .07)
    return r

def construire(ctx):
    preparer(fabriquer())
