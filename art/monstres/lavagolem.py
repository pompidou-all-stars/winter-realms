"""Golem de lave (palier 3, sol) : colosse de roche volcanique noire, fissures et runes de lave orange,
yeux incandescents, épaules fumantes. Clé CR « lavagolem »."""
import math
from communs.outils import collection, dans, pivot, peindre, sphere, cone, cylindre, boite, prisme, anneau, descendants
from communs.personnages import humanoide, epee, hache, marteau, gourdin, baton, bouclier, lame_courbe
from communs.animations import marche
from communs.export_jeu import preparer

# taille selon le facteur z proposé pour CR (même formule que communs/echelles.py) ; voir PALIERS.md
Z = 1.5
def hauteur(): return .40 * Z ** 1.8
def piece(r, nom): return next(o for o in descendants(r) if o.name.split('.')[0] == nom)

INFOS = {'categorie': 'monstre', 'titre': "Golem de lave"}

def fabriquer():
    c = collection('golem_lave'); dans(c)
    r = pivot('golem_lave'); H = hauteur()
    humanoide(r, dict(peau='#3a3330', peau2='#4a423e', tissu='#2b2522', torse='#3a3330', cuir='#ff6a1a', botte='#2b2522',
                      carrure=1.6, tete=.09, jambes=.3, voute=.12, nez=('rond', .12), sourcils=1, yeux='#ff9a2a',
                      epaulieres='cuir', runes='#ff6a1a'), H)
    B = piece(r, 'Buste')
    for k, (x, z, rz) in enumerate(((-.08, .12, .4), (.07, .22, -.3), (0, .3, .1))):
        boite(f'Fissure{k}', '#ff7a1a', H * .015, H * .02, H * .12, (x * H, -H * .17, z * H), 0, B, (0, rz, 0), emis=3)
    for s in (-1, 1): sphere(f'Fumee{s}', '#5a5450', H * .06, (s * H * .25, 0, H * .42), (1, 1, 1.2), 6, 4, B)
    peindre(r)
    marche(r, duree=1.3, ampl_jambe=.35, ampl_bras=.3, rebond=H * .02, roulis=.05)
    return r

def construire(ctx):
    preparer(fabriquer())
