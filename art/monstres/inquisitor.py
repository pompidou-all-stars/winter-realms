"""Inquisiteur (palier 2, magique : anti-magie) : chasseur de mages en armure blanche et or, haut
casque fermé, tabard frappé d'un sceau, marteau runique et écu au sceau rouge. Insensible au Givre et au Mage.
Clé CR « inquisitor »."""
import math
from communs.outils import collection, dans, pivot, peindre, sphere, cone, cylindre, boite, prisme, anneau, descendants
from communs.personnages import humanoide, epee, hache, marteau, gourdin, baton, bouclier, lame_courbe, bombe
from communs.animations import marche
from communs.export_jeu import preparer

# taille selon le facteur z proposé pour CR (même formule que communs/echelles.py) ; voir PALIERS.md
Z = 1.1
def hauteur(): return .40 * Z ** 1.8
def piece(r, nom): return next(o for o in descendants(r) if o.name.split('.')[0] == nom)

INFOS = {'categorie': 'monstre', 'titre': "Inquisiteur"}

def fabriquer():
    c = collection('inquisiteur'); dans(c)
    r = pivot('inquisiteur'); H = hauteur()
    humanoide(r, dict(peau='#e2b48e', peau2='#d29c76', tissu='#e8e4dc', torse='#d9dce2', cuir='#6b4a2f', botte='#c9ced6',
                      metal='#d9dce2', accent='#a8262a', carrure=1.1, tete=.12, jambes=.38, voute=.0, nez=('rond', .2),
                      sourcils=1, yeux='#ffffff', casque='#d9dce2', epaulieres='or', cape='#e8e4dc',
                      arme=lambda p, HH: marteau(p, HH, '#e0b44e'),
                      arme_g=lambda p, HH: bouclier(p, HH, '#e8e4dc', '#e0b44e', '#c0392b')), H)
    Cr = piece(r, 'Crane'); rh = H * .12
    cylindre('Cimier', '#e0b44e', rh * .5, rh * .25, rh * .6, 8, (0, 0, rh * .9), Cr, metal=.7, rough=.3)
    peindre(r)
    marche(r, duree=.85, ampl_jambe=.4, ampl_bras=.25, rebond=H * .03, roulis=.05)
    return r

def construire(ctx):
    preparer(fabriquer())
