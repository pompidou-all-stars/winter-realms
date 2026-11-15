"""Sylvain corrompu (palier 3, sol) : arbre-géant à écorce sombre, branches nues sur la tête portant des
feuilles violettes, mousse, yeux violets lumineux, poings noueux. Clé CR « treant »."""
import math
from communs.outils import collection, dans, pivot, peindre, sphere, cone, cylindre, boite, prisme, anneau, descendants
from communs.personnages import humanoide, epee, hache, marteau, gourdin, baton, bouclier, lame_courbe
from communs.animations import marche
from communs.export_jeu import preparer

# taille selon le facteur z proposé pour CR (même formule que communs/echelles.py) ; voir PALIERS.md
Z = 1.6
def hauteur(): return .40 * Z ** 1.8
def piece(r, nom): return next(o for o in descendants(r) if o.name.split('.')[0] == nom)

INFOS = {'categorie': 'monstre', 'titre': "Sylvain corrompu"}

def fabriquer():
    c = collection('sylvain_corrompu'); dans(c)
    r = pivot('sylvain_corrompu'); H = hauteur()
    humanoide(r, dict(peau='#5a4030', peau2='#6b4e3a', tissu='#4a3426', torse='#5a4030', cuir='#4a6a2a', botte='#4a3426',
                      carrure=1.25, tete=.1, jambes=.4, voute=.18, nez=('long', .3), sourcils=1, yeux='#c77dff', epaulieres='cuir'), H)
    Cr = piece(r, 'Crane'); rh = H * .1
    for k in range(5):
        a = (k - 2) * .45
        b = pivot(f'Branche{k}', (math.sin(a) * rh * .6, 0, rh * .7), Cr); b.rotation_euler = (0, a * 1.3, 0)
        cylindre(f'BrancheCyl{k}', '#4a3426', rh * .06, rh * .12, rh * 1.4, 5, (0, 0, 0), b)
        sphere(f'Feuillage{k}', '#7a3a9a', rh * .45, (0, 0, rh * 1.4), (1, 1, .8), 8, 5, b)
    B = piece(r, 'Buste')
    for k, (x, z) in enumerate(((-.12, .3), (.14, .18))): sphere(f'Mousse{k}', '#5a8a3a', H * .05, (x * H, -H * .15, z * H), (1, .5, 1), 6, 4, B)
    peindre(r)
    marche(r, duree=1.4, ampl_jambe=.3, ampl_bras=.3, rebond=H * .02, roulis=.06)
    return r

def construire(ctx):
    preparer(fabriquer())
