"""Tambour de guerre (palier 2, magique : aura de vitesse) : orc trapu, grand tambour de guerre en
peau sur le ventre, baguettes, peintures de guerre rouges ; son rythme presse les alliés. Clé CR « drummer »."""
import math
from communs.outils import collection, dans, pivot, peindre, sphere, cone, cylindre, boite, prisme, anneau, descendants
from communs.personnages import humanoide, epee, hache, marteau, gourdin, baton, bouclier, lame_courbe, bombe
from communs.animations import marche
from communs.export_jeu import preparer

# taille selon le facteur z proposé pour CR (même formule que communs/echelles.py) ; voir PALIERS.md
Z = 1.05
def hauteur(): return .40 * Z ** 1.8
def piece(r, nom): return next(o for o in descendants(r) if o.name.split('.')[0] == nom)

INFOS = {'categorie': 'monstre', 'titre': "Tambour de guerre"}

def baguette(p, H):
    cylindre('Baguette', '#e8dcc0', H * .012, H * .015, H * .22, 6, (0, 0, -H * .02), p)
    sphere('BoutBaguette', '#a33b2a', H * .025, (0, 0, H * .2), (1, 1, 1), 6, 4, p)

def fabriquer():
    c = collection('tambour_guerre'); dans(c)
    r = pivot('tambour_guerre'); H = hauteur()
    humanoide(r, dict(peau='#4f9a3a', peau2='#63b04a', tissu='#6b3a2a', torse='#4f9a3a', cuir='#4a321f', botte='#3a2a1c',
                      carrure=1.2, tete=.13, jambes=.32, voute=.1, nez=('rond', .26), defenses=1, sourcils=1, oreilles=.35,
                      yeux='#ff5a3c', cheveux='iroquoise', epaulieres='cuir', arme=baguette, arme_g=baguette), H)
    for o in list(c.objects):
        if o.name.startswith('BrasG') or o.name.startswith('BrasD'): o.rotation_euler = (-.9, 0, 0)
    B = piece(r, 'Buste')
    cylindre('Tambour', '#a06a3a', H * .17, H * .17, H * .18, 14, (0, -H * .2, H * .02), B, rot=(math.pi / 2, 0, 0))
    cylindre('Peau', '#f2e2c0', H * .165, H * .165, H * .01, 14, (0, -H * .29, H * .02), B, rot=(math.pi / 2, 0, 0))
    for k in range(6):
        a = k * math.pi / 3
        cylindre(f'Corde{k}', '#e0b44e', H * .006, H * .006, H * .18, 4, (math.cos(a) * H * .17, -H * .2, H * .02 + math.sin(a) * H * .17), B, rot=(math.pi / 2, 0, 0))
    Cr = piece(r, 'Crane'); rh = H * .13
    for s in (-1, 1): boite(f'Peinture{s}', '#c0392b', rh * .15, rh * .1, rh * .5, (s * rh * .45, -rh * .85, -rh * .05), 0, Cr)
    peindre(r)
    marche(r, duree=.6, ampl_jambe=.45, ampl_bras=.2, rebond=H * .05, roulis=.08)
    return r

def construire(ctx):
    preparer(fabriquer())
