"""Automate blindé (palier 2, sol) : machine de guerre en bronze rivetée, œil unique bleu, cheminée
fumante dans le dos, bras-marteau. Clé CR « automaton »."""
import math
from communs.outils import collection, dans, pivot, peindre, sphere, cone, cylindre, boite, prisme, anneau, descendants
from communs.personnages import humanoide, epee, hache, marteau, gourdin, baton, bouclier, lame_courbe, bombe
from communs.animations import marche
from communs.export_jeu import preparer

# taille selon le facteur z proposé pour CR (même formule que communs/echelles.py) ; voir PALIERS.md
Z = 1.2
def hauteur(): return .40 * Z ** 1.8
def piece(r, nom): return next(o for o in descendants(r) if o.name.split('.')[0] == nom)

INFOS = {'categorie': 'monstre', 'titre': "Automate blindé"}

def fabriquer():
    c = collection('automate_blinde'); dans(c)
    r = pivot('automate_blinde'); H = hauteur()
    humanoide(r, dict(peau='#b07a3a', peau2='#c99a5a', tissu='#7d5a2e', torse='#b07a3a', cuir='#5a4026', botte='#7d5a2e',
                      metal='#c99a5a', carrure=1.3, tete=.11, jambes=.3, voute=.05, nez=('rond', .12), un_oeil=1, yeux='#4ad2ff',
                      epaulieres='or', arme=lambda p, HH: marteau(p, HH, '#7d808a')), H)
    B = piece(r, 'Buste')
    cylindre('Cheminee', '#5a5f69', H * .05, H * .04, H * .25, 8, (H * .06, H * .14, H * .2), B)
    sphere('Fumee', '#c9ced6', H * .05, (H * .06, H * .14, H * .5), (1, 1, 1), 6, 4, B)
    for k in range(4): sphere(f'Rivet{k}', '#e0b44e', H * .015, ((k - 1.5) * H * .07, -H * .16, H * .2), (1, .5, 1), 6, 4, B, metal=.7)
    peindre(r)
    marche(r, duree=1.0, ampl_jambe=.35, ampl_bras=.3, rebond=H * .02, roulis=.04)
    return r

def construire(ctx):
    preparer(fabriquer())
