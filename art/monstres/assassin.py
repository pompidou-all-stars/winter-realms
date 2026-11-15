"""Assassin des ombres (palier 2, magique : invisible) : silhouette fine encapuchonnée de noir, masque
violet, cape effilochée, deux lames courbes à lueur violette, yeux violets. Clé CR « assassin »."""
import math
from communs.outils import collection, dans, pivot, peindre, sphere, cone, cylindre, boite, prisme, anneau, descendants
from communs.personnages import humanoide, epee, hache, marteau, gourdin, baton, bouclier, lame_courbe, bombe
from communs.animations import marche
from communs.export_jeu import preparer

# taille selon le facteur z proposé pour CR (même formule que communs/echelles.py) ; voir PALIERS.md
Z = 1
def hauteur(): return .40 * Z ** 1.8
def piece(r, nom): return next(o for o in descendants(r) if o.name.split('.')[0] == nom)

INFOS = {'categorie': 'monstre', 'titre': "Assassin des ombres"}

def fabriquer():
    c = collection('assassin_ombres'); dans(c)
    r = pivot('assassin_ombres'); H = hauteur()
    humanoide(r, dict(peau='#c9b4a0', peau2='#b39c88', tissu='#22242c', torse='#2a2c36', cuir='#3a2a4a', botte='#1b1c22',
                      carrure=.85, tete=.12, jambes=.4, voute=.2, nez=('rond', .18), sourcils=1, yeux='#c77dff',
                      capuche='#22242c', cape='#2a2c36', epaulieres='cuir',
                      arme=lambda p, HH: lame_courbe(p, HH, '#c77dff'), arme_g=lambda p, HH: lame_courbe(p, HH, '#c77dff')), H)
    Cr = piece(r, 'Crane'); rh = H * .12
    sphere('Masque', '#4a2a6a', rh * .78, (0, -rh * .35, -rh * .38), (1.1, .8, .62), 10, 6, Cr)
    peindre(r)
    marche(r, duree=.55, ampl_jambe=.55, ampl_bras=.45, rebond=H * .03, roulis=.06)
    return r

def construire(ctx):
    preparer(fabriquer())
