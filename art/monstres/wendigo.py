"""Wendigo (palier 2, sol) : créature décharnée et très grande, crâne de cerf blanchi, bois immenses,
fourrure sombre en lambeaux, longs bras griffus, yeux bleu glacé. Clé CR « wendigo »."""
import math
from communs.outils import collection, dans, pivot, peindre, sphere, cone, cylindre, boite, prisme, anneau, descendants
from communs.personnages import humanoide, epee, hache, marteau, gourdin, baton, bouclier, lame_courbe, bombe
from communs.animations import marche
from communs.export_jeu import preparer

# taille selon le facteur z proposé pour CR (même formule que communs/echelles.py) ; voir PALIERS.md
Z = 1.25
def hauteur(): return .40 * Z ** 1.8
def piece(r, nom): return next(o for o in descendants(r) if o.name.split('.')[0] == nom)

INFOS = {'categorie': 'monstre', 'titre': "Wendigo"}

def fabriquer():
    c = collection('wendigo'); dans(c)
    r = pivot('wendigo'); H = hauteur()
    humanoide(r, dict(peau='#3a3330', peau2='#e6e2d2', tissu='#2b2522', torse='#4a403a', cuir='#2b2522', botte='#3a3330',
                      carrure=.85, tete=.11, jambes=.44, voute=.35, nez=('long', .35), sourcils=1, yeux='#7ff3ff'), H)
    Cr = piece(r, 'Crane'); rh = H * .11
    sphere('CraneCerf', '#e6e2d2', rh * .95, (0, -rh * .1, 0), (.9, 1.05, .95), 10, 6, Cr)
    for s in (-1, 1):
        b = pivot(f'Bois{s}', (s * rh * .5, 0, rh * .7), Cr); b.rotation_euler = (0, s * .6, 0)
        cylindre(f'BoisTige{s}', '#cfc5a8', rh * .07, rh * .1, rh * 1.6, 5, (0, 0, 0), b)
        for k in range(3): cone(f'Andouiller{s}{k}', '#cfc5a8', rh * .06, rh * .6, 4, (0, 0, rh * (.5 + k * .4)), b, (-.8 + k * .3, s * .7, 0))
    for o in list(c.objects):
        if o.name.startswith('Poing'):
            for k in (-1, 1): cone(f'Griffe{o.name}{k}', '#e6e2d2', H * .01, H * .07, 4, (k * H * .015, -H * .02, -H * .05), o, (math.pi, 0, 0))
    peindre(r)
    marche(r, duree=.9, ampl_jambe=.45, ampl_bras=.55, rebond=H * .03, roulis=.14)
    return r

def construire(ctx):
    preparer(fabriquer())
