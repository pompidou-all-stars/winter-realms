"""Colosse de pierre (palier 3, sol) : géant de grès sculpté, visage de statue antique, couronne de pierre,
runes bleues sur le torse, lierre sur les épaules. Le plus grand des monstres au sol. Clé CR « colossus »."""
import math
from communs.outils import collection, dans, pivot, peindre, sphere, cone, cylindre, boite, prisme, anneau, descendants
from communs.personnages import humanoide, epee, hache, marteau, gourdin, baton, bouclier, lame_courbe
from communs.animations import marche
from communs.export_jeu import preparer

# taille selon le facteur z proposé pour CR (même formule que communs/echelles.py) ; voir PALIERS.md
Z = 1.75
def hauteur(): return .40 * Z ** 1.8
def piece(r, nom): return next(o for o in descendants(r) if o.name.split('.')[0] == nom)

INFOS = {'categorie': 'monstre', 'titre': "Colosse de pierre"}

def fabriquer():
    c = collection('colosse_pierre'); dans(c)
    r = pivot('colosse_pierre'); H = hauteur()
    humanoide(r, dict(peau='#c9b48a', peau2='#d8c4a0', tissu='#b09a72', torse='#c9b48a', cuir='#5a8a3a', botte='#a8926a',
                      carrure=1.45, tete=.1, jambes=.34, voute=.05, nez=('rond', .2), sourcils=1, yeux='#4ad2ff',
                      couronne='#b09a72', epaulieres='cuir', runes='#4ad2ff'), H)
    peindre(r)
    marche(r, duree=1.5, ampl_jambe=.3, ampl_bras=.25, rebond=H * .015, roulis=.04)
    return r

def construire(ctx):
    preparer(fabriquer())
