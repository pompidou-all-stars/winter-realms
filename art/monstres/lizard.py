"""Homme-lézard (palier 2, sol) : guerrier reptile à écailles vertes, crête orange sur la tête,
longue queue, lance à pointe d'os et bouclier rond. Clé CR « lizard »."""
import math
from communs.outils import collection, dans, pivot, peindre, sphere, cone, cylindre, boite, prisme, anneau, descendants
from communs.personnages import humanoide, epee, hache, marteau, gourdin, baton, bouclier, lame_courbe, bombe
from communs.animations import marche
from communs.export_jeu import preparer

# taille selon le facteur z proposé pour CR (même formule que communs/echelles.py) ; voir PALIERS.md
Z = 1.05
def hauteur(): return .40 * Z ** 1.8
def piece(r, nom): return next(o for o in descendants(r) if o.name.split('.')[0] == nom)

INFOS = {'categorie': 'monstre', 'titre': "Homme-lézard"}

def lance(p, H):
    cylindre('Hampe', '#6b4423', H * .015, H * .015, H * .7, 6, (0, 0, -H * .25), p)
    cone('PointeOs', '#efe6cc', H * .035, H * .14, 5, (0, 0, H * .45), p)

def fabriquer():
    c = collection('homme_lezard'); dans(c)
    r = pivot('homme_lezard'); H = hauteur()
    humanoide(r, dict(peau='#4f9a5a', peau2='#8acb7a', tissu='#7a5a2a', torse='#5aa864', cuir='#4a321f', botte='#3f7a48',
                      carrure=1.0, tete=.12, jambes=.38, voute=.25, nez=('long', .42), sourcils=1, yeux='#ffd34d',
                      epaulieres='cuir', arme=lance, arme_g=lambda p, HH: bouclier(p, HH, '#7a5a2a', '#e0a34d')), H)
    Cr = piece(r, 'Crane'); rh = H * .12
    for k in range(4): cone(f'Crete{k}', '#f08a2e', rh * .14, rh * .5, 4, (0, -rh * .4 + k * rh * .35, rh * .8), Cr, (-.3, 0, 0))
    B = piece(r, 'Buste')
    q = pivot('Queue', (0, H * .1, -H * .05), B); q.rotation_euler = (1.0, 0, 0)
    cone('QueueCone', '#4f9a5a', H * .06, H * .45, 6, (0, 0, 0), q, (-math.pi / 2, 0, 0))
    peindre(r)
    marche(r, duree=.7, ampl_jambe=.5, ampl_bras=.35, rebond=H * .04, roulis=.12)
    return r

def construire(ctx):
    preparer(fabriquer())
