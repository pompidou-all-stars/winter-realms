"""Scarabée cuirassé (magique : insensible au canon) : gros scarabée à carapace vert-bleu irisée et bombée,
corne frontale, élytres cerclés d'or, six pattes. Les explosions glissent sur sa carapace.
Proposé pour la PR B (clé CR « beetle »)."""
import math
from communs.outils import collection, dans, pivot, peindre, sphere, cone, cylindre, anneau, descendants
from communs.betes import quadrupede
from communs.animations import trot
from communs.export_jeu import preparer

# taille selon le facteur z proposé pour CR (même formule que communs/echelles.py, qui sera complété avec la PR B)
Z = 0.95
def hauteur(): return .40 * Z ** 1.8
def piece(r, nom): return next(o for o in descendants(r) if o.name.split('.')[0] == nom)

INFOS = {'categorie': 'monstre', 'titre': "Scarabée cuirassé"}

def fabriquer():
    c = collection('scarabee_cuirasse'); dans(c)
    r = pivot('scarabee_cuirasse'); H = hauteur()
    corps = quadrupede(r, dict(poil='#1f2f3a', poil2='#2a3f4c', patte='#1a242c', museau=None, tete=.24, pattes=.3,
                               largeur=.22, epaisseur=.2, lqueue=.01, yeux='#ff9f2e'), H * .7, H * 1.3)
    for s in (-1, 1):
        sphere(f'Elytre{s}', '#2f8a7a', 1, (s * H * .085, H * .1, H * .13), (H * .12, H * .46, H * .15), 12, 8, corps, metal=.5, rough=.25)
    anneau('LisereElytres', '#e0b44e', H * .2, H * .016, 14, 3, (0, H * .1, H * .06), corps, echelle=(1, 1.6, 1), metal=.7, rough=.3)
    cylindre('Suture', '#e0b44e', H * .012, H * .012, H * .8, 5, (0, -H * .3, H * .275), corps, rot=(-math.pi / 2, 0, 0), metal=.7)
    T = piece(r, 'Tete'); rt = H * .7 * .24
    cone('Corne', '#2f8a7a', rt * .3, rt * 1.6, 6, (0, -rt * .6, rt * .4), T, (-.55, 0, 0), metal=.5, rough=.25)
    for s in (-1, 1): cone(f'Mandibule{s}', '#1a242c', rt * .12, rt * .5, 4, (s * rt * .35, -rt * .8, -rt * .4), T, (1.5, 0, s * .4))
    for s in (-1, 1):  # paire de pattes du milieu (immobiles)
        m = pivot(f'PatteMilieu{s}', (s * H * .18, 0, H * .7 * .3), r)
        cylindre(f'PatteM{s}', '#1a242c', H * .04, H * .03, H * .22, 6, (0, 0, -H * .2), m, rot=(0, s * .3, 0))
    peindre(r)
    trot(r, duree=.55, ampl=.5, rebond=H * .015, queue=0)
    return r

def construire(ctx):
    preparer(fabriquer())
