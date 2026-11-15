"""Géant du givre (palier 3, sol) : immense géant à peau bleu pâle, longue barbe blanche, couronne de glace,
pagne de fourrure et marteau de glace. Le plus grand des monstres. Proposé pour la PR B (clé CR « giant »)."""
import math
from communs.outils import collection, dans, pivot, peindre, cone, cylindre, boite, anneau, descendants
from communs.personnages import humanoide
from communs.animations import marche
from communs.export_jeu import preparer

# taille selon le facteur z proposé pour CR (même formule que communs/echelles.py, qui sera complété avec la PR B)
Z = 1.6
def hauteur(): return .40 * Z ** 1.8
def piece(r, nom): return next(o for o in descendants(r) if o.name.split('.')[0] == nom)

INFOS = {'categorie': 'monstre', 'titre': "Géant du givre"}

def marteau_glace(p, H):
    cylindre('Manche', '#5a4636', H * .02, H * .02, H * .5, 6, (0, 0, -H * .12), p)
    boite('MasseGlace', '#a8ecff', H * .2, H * .12, H * .12, (0, 0, H * .38), H * .02, p, rough=.2, emis=.6)
    for s in (-1, 1): cone(f'PicGlace{s}', '#d8f8ff', H * .04, H * .08, 5, (s * H * .1, 0, H * .38), p, (0, s * math.pi / 2, 0), emis=.6)

def fabriquer():
    c = collection('geant_givre'); dans(c)
    r = pivot('geant_givre'); H = hauteur()
    humanoide(r, dict(peau='#8fb3d4', peau2='#a9c8e3', tissu='#e9eef2', torse='#8fb3d4', cuir='#6b4a2f', botte='#d8e2ea',
                      metal='#a8ecff', carrure=1.3, tete=.1, jambes=.36, voute=.12, nez=('rond', .26), sourcils=1,
                      yeux='#bff6ff', barbe='#f4f8fb', epaulieres='pointes', harnais=1, arme=marteau_glace), H)
    Cr = piece(r, 'Crane'); rh = H * .1
    anneau('CouronneGlace', '#a8ecff', rh * .8, rh * .08, 12, 3, (0, 0, rh * .78), Cr, emis=.6)
    for k in range(6):
        a = k * math.pi / 3 + math.pi / 6
        cone(f'Glacon{k}', '#d8f8ff', rh * .12, rh * (.5 if k % 2 else .32), 5, (math.cos(a) * rh * .8, math.sin(a) * rh * .8, rh * .8), Cr, emis=.6)
    peindre(r, cime=1.12)
    marche(r, duree=1.4, ampl_jambe=.4, ampl_bras=.35, rebond=H * .025, roulis=.06)
    return r

def construire(ctx):
    preparer(fabriquer())
