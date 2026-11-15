"""Héraut de guerre (palier 3, magique : aura de vitesse) : champion en armure dorée portant une grande
bannière dans le dos et un cor ; sa sonnerie presse les alliés. Clé CR « herald »."""
import math
from communs.outils import collection, dans, pivot, peindre, sphere, cone, cylindre, boite, prisme, anneau, descendants
from communs.personnages import humanoide, epee, hache, marteau, gourdin, baton, bouclier, lame_courbe
from communs.animations import marche
from communs.export_jeu import preparer

# taille selon le facteur z proposé pour CR (même formule que communs/echelles.py) ; voir PALIERS.md
Z = 1.3
def hauteur(): return .40 * Z ** 1.8
def piece(r, nom): return next(o for o in descendants(r) if o.name.split('.')[0] == nom)

INFOS = {'categorie': 'monstre', 'titre': "Héraut de guerre"}

def fabriquer():
    c = collection('heraut_guerre'); dans(c)
    r = pivot('heraut_guerre'); H = hauteur()
    humanoide(r, dict(peau='#e2b48e', peau2='#d29c76', tissu='#8a2a2a', torse='#e0b44e', cuir='#6b4a2f', botte='#c9a24a',
                      metal='#e0b44e', accent='#a8262a', carrure=1.15, tete=.12, jambes=.38, nez=('rond', .2), sourcils=1,
                      yeux='#ffffff', casque='#e0b44e', epaulieres='or', arme=lambda p, HH: epee(p, HH)), H)
    B = piece(r, 'Buste')
    cylindre('Hampe', '#5a3a22', H * .015, H * .015, H * .9, 6, (0, H * .14, -H * .1), B)
    prisme('Banniere', '#a8262a', [(0, 0), (H * .3, 0), (H * .3, -H * .32), (H * .15, -H * .25), (0, -H * .32)], H * .012, (0, H * .15, H * .78), B)
    sphere('Embleme', '#e0b44e', H * .05, (H * .15, H * .14, H * .62), (1, .4, 1), 8, 4, B, metal=.6)
    anneau('Cor', '#f4ead0', H * .07, H * .02, 10, 3, (-H * .16, -H * .02, H * .05), B, (0, math.pi / 2, 0))
    peindre(r)
    marche(r, duree=.75, ampl_jambe=.45, ampl_bras=.3, rebond=H * .04, roulis=.06)
    return r

def construire(ctx):
    preparer(fabriquer())
