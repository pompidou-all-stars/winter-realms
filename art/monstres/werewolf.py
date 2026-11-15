"""Loup-garou (palier 2, sol) : homme-loup massif et voûté, fourrure gris-brun, long museau, grandes
oreilles, crocs, griffes, pantalon déchiré, yeux jaunes. Clé CR « werewolf »."""
import math
from communs.outils import collection, dans, pivot, peindre, sphere, cone, cylindre, boite, prisme, anneau, descendants
from communs.personnages import humanoide, epee, hache, marteau, gourdin, baton, bouclier, lame_courbe, bombe
from communs.animations import marche
from communs.export_jeu import preparer

# taille selon le facteur z proposé pour CR (même formule que communs/echelles.py) ; voir PALIERS.md
Z = 1.15
def hauteur(): return .40 * Z ** 1.8
def piece(r, nom): return next(o for o in descendants(r) if o.name.split('.')[0] == nom)

INFOS = {'categorie': 'monstre', 'titre': "Loup-garou"}

def fabriquer():
    c = collection('loup_garou'); dans(c)
    r = pivot('loup_garou'); H = hauteur()
    humanoide(r, dict(peau='#6f6458', peau2='#8a7f72', tissu='#3a4a6a', torse='#7d7266', cuir='#4a3f36', botte='#5a5046',
                      carrure=1.25, tete=.12, jambes=.34, voute=.45, nez=('long', .55), oreilles=.8, sourcils=1, defenses=1,
                      yeux='#ffd34d', cheveux='iroquoise'), H)
    for o in list(c.objects):
        if o.name.startswith('Poing'):
            for k in (-1, 0, 1): cone(f'Griffe{o.name}{k}', '#f4efe0', H * .012, H * .05, 4, (k * H * .02, -H * .03, -H * .04), o, (math.pi, 0, 0))
    B = piece(r, 'Buste')
    sphere('Poitrail', '#a39a8e', H * .1, (0, -H * .12, H * .22), (1.2, .5, 1), 8, 5, B)
    peindre(r)
    marche(r, duree=.6, ampl_jambe=.6, ampl_bras=.6, rebond=H * .05, roulis=.12)
    return r

def construire(ctx):
    preparer(fabriquer())
