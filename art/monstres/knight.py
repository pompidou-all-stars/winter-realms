"""Chevalier noir (palier 2, sol) : chevalier en armure d'acier noirci, heaume à cornes, yeux rouges
derrière la visière, cape pourpre, épée et écu. Clé CR « knight »."""
import math
from communs.outils import collection, dans, pivot, peindre, sphere, cone, cylindre, boite, prisme, anneau, descendants
from communs.personnages import humanoide, epee, hache, marteau, gourdin, baton, bouclier, lame_courbe, bombe
from communs.animations import marche
from communs.export_jeu import preparer

# taille selon le facteur z proposé pour CR (même formule que communs/echelles.py) ; voir PALIERS.md
Z = 1.1
def hauteur(): return .40 * Z ** 1.8
def piece(r, nom): return next(o for o in descendants(r) if o.name.split('.')[0] == nom)

INFOS = {'categorie': 'monstre', 'titre': "Chevalier noir"}

def fabriquer():
    c = collection('chevalier_noir'); dans(c)
    r = pivot('chevalier_noir'); H = hauteur()
    humanoide(r, dict(peau='#3a3d48', peau2='#4a4e5a', tissu='#2a2c34', torse='#3a3d48', cuir='#2a2c34', botte='#2f323c',
                      metal='#4a4e5a', cape='#6a1f3a', carrure=1.1, tete=.12, jambes=.38, voute=.05, nez=('rond', .1),
                      yeux='#ff3a3a', casque='#3a3d48', cornes=1, epaulieres='pointes',
                      arme=lambda p, HH: epee(p, HH, '#9aa3ad', '#8a2a3a'),
                      arme_g=lambda p, HH: bouclier(p, HH, '#2f323c', '#8a2a3a', '#ff3a3a')), H)
    peindre(r)
    marche(r, duree=.85, ampl_jambe=.4, ampl_bras=.25, rebond=H * .03, roulis=.05)
    return r

def construire(ctx):
    preparer(fabriquer())
