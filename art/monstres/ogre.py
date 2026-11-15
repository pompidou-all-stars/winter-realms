"""Ogre (palier 2, sol) : grosse brute ventrue à peau jaune-brun, petite tête, mâchoire énorme, sourcils
épais, pagne de peau et massue à clous. Clé CR « ogre »."""
import math
from communs.outils import collection, dans, pivot, peindre, sphere, cone, cylindre, boite, prisme, anneau, descendants
from communs.personnages import humanoide, epee, hache, marteau, gourdin, baton, bouclier, lame_courbe, bombe
from communs.animations import marche
from communs.export_jeu import preparer

# taille selon le facteur z proposé pour CR (même formule que communs/echelles.py) ; voir PALIERS.md
Z = 1.2
def hauteur(): return .40 * Z ** 1.8
def piece(r, nom): return next(o for o in descendants(r) if o.name.split('.')[0] == nom)

INFOS = {'categorie': 'monstre', 'titre': "Ogre"}

def fabriquer():
    c = collection('ogre'); dans(c)
    r = pivot('ogre'); H = hauteur()
    humanoide(r, dict(peau='#c2a86a', peau2='#d8c088', tissu='#7a5634', torse='#c2a86a', cuir='#4a321f', botte='#6b4a2f',
                      carrure=1.5, tete=.1, jambes=.3, voute=.2, machoire=1, sourcils=1, nez=('rond', .3), defenses=1,
                      oreilles=.3, yeux='#ffffff', cheveux='chignon', harnais=1,
                      arme=lambda p, HH: gourdin(p, HH, '#6b4a2f')), H)
    B = piece(r, 'Buste')
    sphere('Bedaine', '#d8c088', H * .19, (0, -H * .09, H * .08), (1, .85, .9), 12, 8, B)
    peindre(r)
    marche(r, duree=1.0, ampl_jambe=.4, ampl_bras=.4, rebond=H * .04, roulis=.12)
    return r

def construire(ctx):
    preparer(fabriquer())
