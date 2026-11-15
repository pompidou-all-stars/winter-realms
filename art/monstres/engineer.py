"""Ingénieur nain renégat (palier 2, magique : étourdissement) : nain trapu à barbe rousse tressée,
lunettes de soudeur, casque à pointe, sac à dos fumant, clé à molette et bombe assommante. Clé CR « engineer »."""
import math
from communs.outils import collection, dans, pivot, peindre, sphere, cone, cylindre, boite, prisme, anneau, descendants
from communs.personnages import humanoide, epee, hache, marteau, gourdin, baton, bouclier, lame_courbe, bombe
from communs.animations import marche
from communs.export_jeu import preparer

# taille selon le facteur z proposé pour CR (même formule que communs/echelles.py) ; voir PALIERS.md
Z = 1
def hauteur(): return .40 * Z ** 1.8
def piece(r, nom): return next(o for o in descendants(r) if o.name.split('.')[0] == nom)

INFOS = {'categorie': 'monstre', 'titre': "Ingénieur nain renégat"}

def fabriquer():
    c = collection('ingenieur_nain'); dans(c)
    r = pivot('ingenieur_nain'); H = hauteur()
    humanoide(r, dict(peau='#e2b48e', peau2='#d29c76', tissu='#5a4a3a', torse='#7a5a3a', cuir='#4a321f', botte='#3a2a1c',
                      metal='#b07a3a', carrure=1.25, tete=.15, jambes=.26, voute=.05, nez=('rond', .34), sourcils=1,
                      yeux='#ffffff', barbe='#c8562a', lunettes=1, casque='#9aa3ad', sac='#6b4a2f', epaulieres='or',
                      arme=lambda p, HH: marteau(p, HH, '#b07a3a'), arme_g=bombe), H)
    peindre(r)
    marche(r, duree=.6, ampl_jambe=.5, ampl_bras=.4, rebond=H * .05, roulis=.1)
    return r

def construire(ctx):
    preparer(fabriquer())
