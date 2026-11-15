"""Roi-liche (palier 3, sol) : squelette couronné en longue robe violette à liserés d'or, cape en lambeaux,
yeux et bâton à orbe vert spectral. Clé CR « lich »."""
import math
from communs.outils import collection, dans, pivot, peindre, sphere, cone, cylindre, boite, prisme, anneau, descendants
from communs.personnages import humanoide, epee, hache, marteau, gourdin, baton, bouclier, lame_courbe
from communs.animations import marche
from communs.export_jeu import preparer

# taille selon le facteur z proposé pour CR (même formule que communs/echelles.py) ; voir PALIERS.md
Z = 1.3
def hauteur(): return .40 * Z ** 1.8
def piece(r, nom): return next(o for o in descendants(r) if o.name.split('.')[0] == nom)

INFOS = {'categorie': 'monstre', 'titre': "Roi-liche"}

def fabriquer():
    c = collection('roi_liche'); dans(c)
    r = pivot('roi_liche'); H = hauteur()
    humanoide(r, dict(peau='#e6e2d2', peau2='#cfc9b4', tissu='#3a2a5a', torse='#4a3470', robe='#3a2a5a', accent='#e0b44e',
                      cuir='#2a1d3a', botte='#2a1d3a', carrure=.9, tete=.12, jambes=.38, voute=.15, nez=('rond', .1),
                      machoire=1, sourcils=1, yeux='#6aff9a', couronne='#e0b44e', cape='#2a1d3a', epaulieres='pointes',
                      arme=lambda p, HH: baton(p, HH, '#6aff9a', '#3a3330')), H)
    peindre(r)
    marche(r, duree=1.0, ampl_jambe=.3, ampl_bras=.25, rebond=H * .02, roulis=.05)
    return r

def construire(ctx):
    preparer(fabriquer())
