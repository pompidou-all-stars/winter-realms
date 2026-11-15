"""Gargouille (palier 2, sol) : statue de pierre grise vivante, voûtée, cornes recourbées, petites ailes
de pierre repliées, griffes et yeux orange. Marche lourdement au sol. Clé CR « gargoyle »."""
import math
from communs.outils import collection, dans, pivot, peindre, sphere, cone, cylindre, boite, prisme, anneau, descendants
from communs.personnages import humanoide, epee, hache, marteau, gourdin, baton, bouclier, lame_courbe, bombe
from communs.animations import marche
from communs.betes import aile
from communs.export_jeu import preparer

# taille selon le facteur z proposé pour CR (même formule que communs/echelles.py) ; voir PALIERS.md
Z = 1.1
def hauteur(): return .40 * Z ** 1.8
def piece(r, nom): return next(o for o in descendants(r) if o.name.split('.')[0] == nom)

INFOS = {'categorie': 'monstre', 'titre': "Gargouille"}

def fabriquer():
    c = collection('gargouille'); dans(c)
    r = pivot('gargouille'); H = hauteur()
    humanoide(r, dict(peau='#8a8f99', peau2='#a4a9b2', tissu='#7a7f89', torse='#8a8f99', cuir='#6c717b', botte='#6c717b',
                      carrure=1.05, tete=.13, jambes=.3, voute=.45, nez=('crochu', .26), sourcils=1, defenses=1,
                      oreilles=.5, yeux='#ff9f2e'), H)
    Cr = piece(r, 'Crane'); rh = H * .13
    for s in (-1, 1): cone(f'CorneG{s}', '#5a5f69', rh * .2, rh * .8, 6, (s * rh * .6, rh * .1, rh * .6), Cr, (-.9, s * .5, 0))
    B = piece(r, 'Buste')
    for s, n in ((-1, 'PierreG'), (1, 'PierreD')):
        a = pivot(n, (s * H * .1, H * .12, H * .22), B); a.rotation_euler = (.5, 0, s * .9)
        aile(a, n, s, H * .55, '#7a7f89', 'membrane', '#5a5f69')
    peindre(r)
    marche(r, duree=.95, ampl_jambe=.4, ampl_bras=.4, rebond=H * .03, roulis=.1)
    return r

def construire(ctx):
    preparer(fabriquer())
