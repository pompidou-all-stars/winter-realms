"""Grande prêtresse de sang (palier 3, magique : soin) : prêtresse en robe pourpre et or, haute coiffe,
voile, bâton surmonté d'un rubis lumineux ; soigne les alliés. Clé CR « bloodpriest »."""
import math
from communs.outils import collection, dans, pivot, peindre, sphere, cone, cylindre, boite, prisme, anneau, descendants
from communs.personnages import humanoide, epee, hache, marteau, gourdin, baton, bouclier, lame_courbe
from communs.animations import marche
from communs.export_jeu import preparer

# taille selon le facteur z proposé pour CR (même formule que communs/echelles.py) ; voir PALIERS.md
Z = 1.25
def hauteur(): return .40 * Z ** 1.8
def piece(r, nom): return next(o for o in descendants(r) if o.name.split('.')[0] == nom)

INFOS = {'categorie': 'monstre', 'titre': "Grande prêtresse de sang"}

def fabriquer():
    c = collection('pretresse_sang'); dans(c)
    r = pivot('pretresse_sang'); H = hauteur()
    humanoide(r, dict(peau='#e8c8b0', peau2='#d8b098', tissu='#6a1a2a', torse='#8a2232', robe='#6a1a2a', accent='#e0b44e',
                      cuir='#3a1a1a', botte='#2a1a1a', carrure=.9, tete=.12, jambes=.34, nez=('rond', .16), yeux='#ff4a5a',
                      chapeau='#8a2232', cape='#3a1a2a', epaulieres='or',
                      arme=lambda p, HH: baton(p, HH, '#ff3a4a', '#e0b44e')), H)
    peindre(r)
    marche(r, duree=.85, ampl_jambe=.3, ampl_bras=.25, rebond=H * .03, roulis=.04)
    return r

def construire(ctx):
    preparer(fabriquer())
