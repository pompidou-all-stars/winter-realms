"""Maraudeur (palier 1, sol) : pillard humain encapuchonné, foulard sur le visage, cape usée,
brigandine de cuir et épée courte. Clé CR « raider »."""
import math
from communs.outils import collection, dans, pivot, peindre, sphere, cone, cylindre, boite, prisme, anneau, descendants
from communs.personnages import humanoide, epee
from communs.animations import marche
from communs.export_jeu import preparer

# taille selon le facteur z proposé pour CR (même formule que communs/echelles.py) ; voir PALIERS.md
Z = 0.9
def hauteur(): return .40 * Z ** 1.8
def piece(r, nom): return next(o for o in descendants(r) if o.name.split('.')[0] == nom)

INFOS = {'categorie': 'monstre', 'titre': "Maraudeur"}

def fabriquer():
    c = collection('maraudeur'); dans(c)
    r = pivot('maraudeur'); H = hauteur()
    humanoide(r, dict(peau='#e2b48e', peau2='#d29c76', tissu='#4f5a3a', torse='#6b4a2f', cuir='#3a2a1c', botte='#3a2e22',
                      carrure=.95, tete=.12, jambes=.38, voute=.1, nez=('rond', .22), sourcils=1, yeux='#ffffff',
                      capuche='#4a3f36', cape='#5a4a3a', epaulieres='cuir', harnais=1,
                      arme=lambda p, HH: epee(p, HH, '#c9ced6', '#6b4a2f')), H)
    Cr = piece(r, 'Crane'); rh = H * .12
    sphere('Foulard', '#8a2f2f', rh * .78, (0, -rh * .35, -rh * .38), (1.1, .8, .62), 10, 6, Cr)
    peindre(r)
    marche(r, duree=.7, ampl_jambe=.5, ampl_bras=.45, rebond=H * .04, roulis=.08)
    return r

def construire(ctx):
    preparer(fabriquer())
