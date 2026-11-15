"""Kobold (palier 1, sol) : petit homme-dragon à écailles orange, museau long, petites cornes,
casque de mineur avec une bougie, pioche à la main. Clé CR « kobold »."""
import math
from communs.outils import collection, dans, pivot, peindre, sphere, cone, cylindre, boite, prisme, anneau, descendants
from communs.personnages import humanoide
from communs.animations import marche
from communs.export_jeu import preparer

# taille selon le facteur z proposé pour CR (même formule que communs/echelles.py) ; voir PALIERS.md
Z = 0.78
def hauteur(): return .40 * Z ** 1.8
def piece(r, nom): return next(o for o in descendants(r) if o.name.split('.')[0] == nom)

INFOS = {'categorie': 'monstre', 'titre': "Kobold"}

def pioche(p, H):
    cylindre('Manche', '#6b4423', H * .016, H * .016, H * .45, 6, (0, 0, -H * .1), p)
    prisme('Pic', '#9aa3ad', [(-H * .16, H * .3), (0, H * .37), (H * .16, H * .3), (0, H * .34)], H * .025, (0, 0, 0), p, metal=.5)

def fabriquer():
    c = collection('kobold'); dans(c)
    r = pivot('kobold'); H = hauteur()
    humanoide(r, dict(peau='#d9733a', peau2='#f0a060', tissu='#5a4a3a', torse='#e08848', cuir='#4a321f', botte='#7a3a1a',
                      carrure=.8, tete=.16, jambes=.3, voute=.3, nez=('long', .34), oreilles=.25, sourcils=1, yeux='#ffe45e',
                      casque='#8a6a3a', arme=pioche), H)
    Cr = piece(r, 'Crane'); rh = H * .16
    cylindre('Bougie', '#f4efe0', rh * .12, rh * .12, rh * .35, 6, (0, -rh * .3, rh * 1.0), Cr)
    sphere('FlammeBougie', '#ffcf4a', rh * .1, (0, -rh * .3, rh * 1.42), (1, 1, 1.6), 6, 4, Cr, emis=4)
    for s in (-1, 1): cone(f'Cornet{s}', '#f4e4c0', rh * .1, rh * .35, 5, (s * rh * .55, rh * .3, rh * .55), Cr, (-.6, s * .4, 0))
    B = piece(r, 'Buste')
    q = pivot('Queue', (0, H * .12, -H * .04), B); q.rotation_euler = (.9, 0, 0)
    cone('QueueCone', '#d9733a', H * .05, H * .3, 6, (0, 0, 0), q, (-math.pi / 2, 0, 0))
    peindre(r)
    marche(r, duree=.55, ampl_jambe=.6, ampl_bras=.4, rebond=H * .06, roulis=.1)
    return r

def construire(ctx):
    preparer(fabriquer())
