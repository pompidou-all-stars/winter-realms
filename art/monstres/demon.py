"""Démon des abysses (palier 3, sol) : démon cramoisi musclé, grandes cornes noires, ailes de chauve-souris
repliées, queue fourchue, sabots, lame de feu. Clé CR « demon »."""
import math
from communs.outils import collection, dans, pivot, peindre, sphere, cone, cylindre, boite, prisme, anneau, descendants
from communs.personnages import humanoide, epee, hache, marteau, gourdin, baton, bouclier, lame_courbe
from communs.animations import marche
from communs.betes import aile
from communs.export_jeu import preparer

# taille selon le facteur z proposé pour CR (même formule que communs/echelles.py) ; voir PALIERS.md
Z = 1.5
def hauteur(): return .40 * Z ** 1.8
def piece(r, nom): return next(o for o in descendants(r) if o.name.split('.')[0] == nom)

INFOS = {'categorie': 'monstre', 'titre': "Démon des abysses"}

def fabriquer():
    c = collection('demon_abysses'); dans(c)
    r = pivot('demon_abysses'); H = hauteur()
    humanoide(r, dict(peau='#a82a2a', peau2='#c84a3a', tissu='#2a1a1a', torse='#b83a30', cuir='#2a1a1a', botte='#1b1212',
                      carrure=1.35, tete=.11, jambes=.38, voute=.15, nez=('crochu', .24), sourcils=1, defenses=1, oreilles=.45,
                      yeux='#ffd34d', arme=lambda p, HH: lame_courbe(p, HH, '#ff9a2a')), H)
    Cr = piece(r, 'Crane'); rh = H * .11
    for s in (-1, 1): cone(f'Corne{s}', '#1b1b1b', rh * .25, rh * 1.3, 6, (s * rh * .6, rh * .1, rh * .6), Cr, (-.7, s * .6, 0))
    B = piece(r, 'Buste')
    for s, n in ((-1, 'DemonG'), (1, 'DemonD')):
        a = pivot(n, (s * H * .1, H * .12, H * .25), B); a.rotation_euler = (.4, 0, s * .8)
        aile(a, n, s, H * .75, '#5a1a2a', 'membrane', '#2a1a1a')
    q = pivot('Queue', (0, H * .1, -H * .05), B); q.rotation_euler = (1.1, 0, 0)
    cone('QueueCone', '#a82a2a', H * .04, H * .45, 6, (0, 0, 0), q, (-math.pi / 2, 0, 0))
    prisme('Fourche', '#1b1b1b', [(-H * .05, 0), (0, H * .08), (H * .05, 0)], H * .015, (0, H * .45, 0), q, (math.pi / 2, 0, 0))
    peindre(r)
    marche(r, duree=.9, ampl_jambe=.45, ampl_bras=.35, rebond=H * .03, roulis=.07)
    return r

def construire(ctx):
    preparer(fabriquer())
