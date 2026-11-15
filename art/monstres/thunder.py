"""Golem du tonnerre (palier 3, magique : étourdissement) : colosse de pierre bleu nuit traversé
d'éclairs, cristaux jaunes sur les épaules et les poings, yeux électriques ; ses décharges étourdissent les tours.
Clé CR « thunder »."""
import math
from communs.outils import collection, dans, pivot, peindre, sphere, cone, cylindre, boite, prisme, anneau, descendants
from communs.personnages import humanoide, epee, hache, marteau, gourdin, baton, bouclier, lame_courbe
from communs.animations import marche
from communs.export_jeu import preparer

# taille selon le facteur z proposé pour CR (même formule que communs/echelles.py) ; voir PALIERS.md
Z = 1.45
def hauteur(): return .40 * Z ** 1.8
def piece(r, nom): return next(o for o in descendants(r) if o.name.split('.')[0] == nom)

INFOS = {'categorie': 'monstre', 'titre': "Golem du tonnerre"}

def fabriquer():
    c = collection('golem_tonnerre'); dans(c)
    r = pivot('golem_tonnerre'); H = hauteur()
    humanoide(r, dict(peau='#3a4a6a', peau2='#4a5a7a', tissu='#2a3450', torse='#3a4a6a', cuir='#ffe45e', botte='#2a3450',
                      carrure=1.5, tete=.09, jambes=.3, voute=.1, nez=('rond', .12), sourcils=1, yeux='#ffe45e',
                      epaulieres='cuir', runes='#ffe45e'), H)
    for o in list(c.objects):
        if o.name.startswith('Epauliere') or o.name.startswith('Poing'):
            for k in range(2): cone(f'Cristal{o.name}{k}', '#ffe45e', H * .025, H * .1, 4, ((k - .5) * H * .04, 0, H * .05), o, ((k - .5) * .6, 0, 0), emis=3)
    B = piece(r, 'Buste')
    prisme('Eclair', '#fff7a0', [(0, 0), (H * .05, -H * .08), (H * .01, -H * .08), (H * .06, -H * .18), (-H * .02, -H * .06), (H * .02, -H * .06)], H * .01, (0, -H * .17, H * .35), B, emis=4)
    peindre(r)
    marche(r, duree=1.2, ampl_jambe=.35, ampl_bras=.3, rebond=H * .02, roulis=.05)
    return r

def construire(ctx):
    preparer(fabriquer())
