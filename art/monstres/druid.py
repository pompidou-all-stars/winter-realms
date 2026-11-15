"""Druidesse (palier 2, magique : soin) : elfe sylvestre en robe verte et brune, capuche de feuilles,
petits bois de cerf, bâton noueux à orbe vert lumineux ; soigne les alliés. Clé CR « druid »."""
import math
from communs.outils import collection, dans, pivot, peindre, sphere, cone, cylindre, boite, prisme, anneau, descendants
from communs.personnages import humanoide, epee, hache, marteau, gourdin, baton, bouclier, lame_courbe, bombe
from communs.animations import marche
from communs.export_jeu import preparer

# taille selon le facteur z proposé pour CR (même formule que communs/echelles.py) ; voir PALIERS.md
Z = 1.05
def hauteur(): return .40 * Z ** 1.8
def piece(r, nom): return next(o for o in descendants(r) if o.name.split('.')[0] == nom)

INFOS = {'categorie': 'monstre', 'titre': "Druidesse"}

def fabriquer():
    c = collection('druidesse'); dans(c)
    r = pivot('druidesse'); H = hauteur()
    humanoide(r, dict(peau='#e8c8a8', peau2='#d8b090', tissu='#4a7a3a', torse='#5a8a42', robe='#3a6a32', accent='#c9a24a',
                      cuir='#5a3d26', botte='#3a2a1c', carrure=.85, tete=.13, jambes=.34, nez=('rond', .18), oreilles=.6,
                      yeux='#7ee0a0', capuche='#3f6e30', arme=lambda p, HH: baton(p, HH, '#7ee0a0', '#6b4a2f')), H)
    Cr = piece(r, 'Crane'); rh = H * .13
    for s in (-1, 1):
        cone(f'BoisPetit{s}', '#cfc5a8', rh * .07, rh * .6, 4, (s * rh * .45, 0, rh * .8), Cr, (0, s * .5, 0))
        cone(f'Feuille{s}', '#6fbf4a', rh * .2, rh * .35, 4, (s * rh * .8, rh * .3, rh * .2), Cr, (0, s * 1.2, 0))
    peindre(r)
    marche(r, duree=.8, ampl_jambe=.35, ampl_bras=.25, rebond=H * .03, roulis=.05)
    return r

def construire(ctx):
    preparer(fabriquer())
