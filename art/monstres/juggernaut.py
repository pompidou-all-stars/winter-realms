"""Mastodonte de fer (palier 3, sol) : engin de siège blindé sur chenilles, bélier en tête de bélier,
plaques rivetées, cheminées fumantes et lucarnes rougeoyantes. Clé CR « juggernaut »."""
import math
from communs.outils import collection, dans, pivot, peindre, sphere, cone, cylindre, boite, prisme, anneau, descendants
from communs.animations import marche
from communs.export_jeu import preparer

# taille selon le facteur z proposé pour CR (même formule que communs/echelles.py) ; voir PALIERS.md
Z = 1.6
def hauteur(): return .40 * Z ** 1.8
def piece(r, nom): return next(o for o in descendants(r) if o.name.split('.')[0] == nom)

INFOS = {'categorie': 'monstre', 'titre': "Mastodonte de fer"}

def fabriquer():
    c = collection('mastodonte_fer'); dans(c)
    r = pivot('mastodonte_fer'); H = hauteur()
    corps = pivot('Corps', (0, 0, H * .12), r)
    for s in (-1, 1):
        boite(f'Chenille{s}', '#2b2b30', H * .14, H * .75, H * .16, (s * H * .24, 0, -H * .04), H * .05, corps)
        for k in range(4): cylindre(f'Roue{s}{k}', '#7d808a', H * .055, H * .055, H * .15, 8, (s * H * .245, -H * .27 + k * H * .18, -H * .04), corps, rot=(0, math.pi / 2, 0))
    boite('Caisse', '#6c717b', H * .4, H * .65, H * .3, (0, 0, H * .12), H * .03, corps, metal=.4, rough=.45)
    boite('Toit', '#5a5f69', H * .36, H * .5, H * .1, (0, H * .03, H * .32), H * .03, corps, metal=.4, rough=.45)
    for k in range(3): boite(f'Lucarne{k}', '#ff6a2a', H * .07, H * .02, H * .04, ((k - 1) * H * .12, -H * .33, H * .2), 0, corps, emis=3)
    for s in (-1, 1):
        cylindre(f'Cheminee{s}', '#3a3330', H * .045, H * .035, H * .25, 8, (s * H * .1, H * .2, H * .35), corps)
        sphere(f'Fumee{s}', '#c9ced6', H * .05, (s * H * .1, H * .2, H * .65), (1, 1, 1), 6, 4, corps)
    T = pivot('Tete', (0, -H * .38, H * .12), corps)
    cylindre('Belier', '#7a5634', H * .07, H * .07, H * .28, 8, (0, 0, 0), T, rot=(math.pi / 2, 0, 0))
    sphere('TeteBelier', '#9aa3ad', H * .1, (0, -H * .3, 0), (1, 1.1, .9), 10, 6, T, metal=.5)
    for s in (-1, 1): anneau(f'CorneBelier{s}', '#c9ced6', H * .06, H * .025, 10, 4, (s * H * .09, -H * .26, H * .03), T, (0, math.pi / 2, 0), metal=.5)
    for k in range(4): sphere(f'Rivet{k}', '#e0b44e', H * .015, ((k - 1.5) * H * .1, -H * .33, H * .05), (1, .5, 1), 6, 4, corps, metal=.7)
    peindre(r)
    marche(r, duree=.8, rebond=H * .015, roulis=.03)
    return r

def construire(ctx):
    preparer(fabriquer())
