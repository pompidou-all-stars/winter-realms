"""Minotaure (palier 2, sol) : homme-taureau à pelage brun, grandes cornes ivoire, anneau d'or au
museau, sabots, hache à double lame. Clé CR « minotaur »."""
import math
from communs.outils import collection, dans, pivot, peindre, sphere, cone, cylindre, boite, prisme, anneau, descendants
from communs.personnages import humanoide, epee, hache, marteau, gourdin, baton, bouclier, lame_courbe, bombe
from communs.animations import marche
from communs.export_jeu import preparer

# taille selon le facteur z proposé pour CR (même formule que communs/echelles.py) ; voir PALIERS.md
Z = 1.2
def hauteur(): return .40 * Z ** 1.8
def piece(r, nom): return next(o for o in descendants(r) if o.name.split('.')[0] == nom)

INFOS = {'categorie': 'monstre', 'titre': "Minotaure"}

def double_hache(p, H):
    hache(p, H)
    prisme('LameDos', '#cfd6df', [(0, H * .22), (-H * .2, H * .17), (-H * .22, H * .3), (-H * .2, H * .42), (0, H * .36)], H * .03, (0, 0, 0), p, metal=.35)

def fabriquer():
    c = collection('minotaure'); dans(c)
    r = pivot('minotaure'); H = hauteur()
    humanoide(r, dict(peau='#7a4a2e', peau2='#a06a46', tissu='#4a3a2a', torse='#7a4a2e', cuir='#3a2a1c', botte='#2b211c',
                      carrure=1.35, tete=.12, jambes=.36, voute=.15, nez=('rond', .42), sourcils=1, oreilles=.35,
                      yeux='#ff4a3a', epaulieres='cuir', harnais=1, arme=double_hache), H)
    Cr = piece(r, 'Crane'); rh = H * .12
    for s in (-1, 1): cone(f'Corne{s}', '#f4ead0', rh * .22, rh * 1.1, 6, (s * rh * .8, 0, rh * .45), Cr, (0, s * 1.3, 0))
    anneau('AnneauNez', '#f2c14e', rh * .2, rh * .05, 10, 3, (0, -rh * 1.25, -rh * .3), Cr, metal=.7, rough=.3)
    peindre(r)
    marche(r, duree=.85, ampl_jambe=.45, ampl_bras=.4, rebond=H * .04, roulis=.08)
    return r

def construire(ctx):
    preparer(fabriquer())
