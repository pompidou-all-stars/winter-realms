"""Gnoll (palier 1, sol) : homme-hyène voûté au pelage fauve tacheté, crinière noire, museau long,
grandes oreilles, coutelas courbe. Clé CR « gnoll »."""
import math
from communs.outils import collection, dans, pivot, peindre, sphere, cone, cylindre, boite, prisme, anneau, descendants
from communs.personnages import humanoide, lame_courbe
from communs.animations import marche
from communs.export_jeu import preparer

# taille selon le facteur z proposé pour CR (même formule que communs/echelles.py) ; voir PALIERS.md
Z = 0.9
def hauteur(): return .40 * Z ** 1.8
def piece(r, nom): return next(o for o in descendants(r) if o.name.split('.')[0] == nom)

INFOS = {'categorie': 'monstre', 'titre': "Gnoll"}

def fabriquer():
    c = collection('gnoll'); dans(c)
    r = pivot('gnoll'); H = hauteur()
    humanoide(r, dict(peau='#c9a25a', peau2='#e0c088', tissu='#6b3a2a', torse='#c9a25a', cuir='#3a2a1c', botte='#5a4026',
                      carrure=.95, tete=.13, jambes=.36, voute=.4, nez=('long', .5), oreilles=.6, sourcils=1, defenses=1,
                      yeux='#ffd34d', cheveux='iroquoise', epaulieres='cuir',
                      arme=lambda p, HH: lame_courbe(p, HH, '#c9ced6')), H)
    Cr = piece(r, 'Crane'); rh = H * .13
    for k, (x, y, z) in enumerate(((-.6, -.3, .3), (.55, -.2, .4), (-.3, .4, .6), (.4, .5, .2))):
        sphere(f'Tache{k}', '#5a3a22', rh * .16, (x * rh, y * rh, z * rh), (1, 1, .4), 6, 4, Cr)
    B = piece(r, 'Buste')
    for k, (x, z) in enumerate(((-.12, .25), (.1, .15), (0, .32))):
        sphere(f'TacheCorps{k}', '#5a3a22', H * .03, (x * H, -H * .13, z * H), (1, .4, 1), 6, 4, B)
    peindre(r)
    marche(r, duree=.6, ampl_jambe=.55, ampl_bras=.5, rebond=H * .05, roulis=.12)
    return r

def construire(ctx):
    preparer(fabriquer())
