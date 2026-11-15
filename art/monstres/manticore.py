"""Manticore (palier 2, volant) : corps de lion roux à crinière sombre, visage grimaçant, ailes de
chauve-souris pourpres, queue de scorpion à dard. Volante : modèle centré sur z = 0. Clé CR « manticore »."""
import math
from communs.outils import collection, dans, pivot, peindre, sphere, cone, cylindre, boite, prisme, anneau, descendants
from communs.betes import volant, yeux_bete, aile
from communs.animations import battement
from communs.export_jeu import preparer

# taille selon le facteur z proposé pour CR (même formule que communs/echelles.py) ; voir PALIERS.md
Z = 1.2
def hauteur(): return .40 * Z ** 1.8
def piece(r, nom): return next(o for o in descendants(r) if o.name.split('.')[0] == nom)

INFOS = {'categorie': 'monstre', 'titre': "Manticore"}

def fabriquer():
    c = collection('manticore'); dans(c)
    r = pivot('manticore'); H = hauteur()
    corps = volant(r, dict(aile='#6a2a4a', os='#3a1a2a'), H, H * 2.0)
    sphere('Tronc', '#c8743a', H * .24, (0, H * .08, 0), (1, 1.5, .85), 12, 8, corps)
    for s in (-1, 1):
        cone(f'Patte{s}', '#c8743a', H * .06, H * .22, 6, (s * H * .12, -H * .15, -H * .15), corps, (-.2, 0, 0))
        cone(f'PatteAr{s}', '#c8743a', H * .06, H * .22, 6, (s * H * .12, H * .3, -H * .15), corps, (.4, 0, 0))
    T = pivot('Tete', (0, -H * .34, H * .1), corps)
    sphere('Criniere', '#5a2a1a', H * .2, (0, H * .04, 0), (1.15, .9, 1.1), 12, 8, T)
    sphere('Visage', '#e0a070', H * .12, (0, -H * .1, 0), (1, .8, 1), 10, 6, T)
    sphere('Nez', '#c8743a', H * .04, (0, -H * .2, -H * .02), (1, 1, 1), 6, 4, T)
    for s in (-1, 1): cone(f'Croc{s}', '#ffffff', H * .015, H * .05, 4, (s * H * .03, -H * .19, -H * .07), T, (math.pi, 0, 0))
    yeux_bete(T, H * .03, -H * .19, H * .04, H * .05, '#ffe45e', False)
    p = corps
    for k in range(4):
        p = pivot(f'Queue{k}' if k else 'Queue', (0, H * .42, H * .02) if k == 0 else (0, 0, H * .14), p); p.rotation_euler = (-.55 if k == 0 else -.45, 0, 0)
        sphere(f'Anneau{k}', '#7a3a2a', H * (.07 - k * .008), (0, 0, H * .07), (1, 1, 1.2), 8, 5, p)
    cone('DardScorpion', '#2a1a1a', H * .04, H * .14, 6, (0, 0, H * .14), p, (-.5, 0, 0))
    peindre(r, sol=.8)
    battement(r, duree=.5, ampl=.65, flottement=H * .06)
    return r

def construire(ctx):
    preparer(fabriquer())
