"""Construction des tours : 6 archétypes (sim.js, BASE_TW) déclinés dans le style de chaque faction.

Chaque faction fournit un STYLE : murs, toit, chemin de ronde, équipage (race), mage, champion,
couleur de magie. Les emplacements 6 à 9 sont des versions plus grandes et plus riches des
emplacements 0, 1, 2 et 5 (comme dans le jeu : Tireur d'élite, Champion, Entrave, Archimage).

Pièces animées / orientées par le jeu (noms d'objets) :
  Tourelle   pivote vers la cible (archers, baliste, canon, gardien, mage)
  Cristal    tourne sur lui-même (givre)      Eclats   tournent autour (entrave)
  Flamme     vacille (flammes)                Anneaux  tournent (archimage, ombres)
  Orbe       pulse (mage)
"""
import math
from . import outils
from .outils import pivot, cylindre, boite, sphere, cone, prisme, anneau, peindre, collection, dans
from .factions import PAL, SOCLES
from .personnages import (humanoide, arc_court, epee, marteau, gourdin, baton, bouclier, hache, lame_courbe, baguette)

# ---------------------------------------------------------------- styles des factions
STYLE = {
    'alliance': dict(
        mur='pierre', toit='fleche', lueur='#fff1b0', glace='#bfe8ff',
        equipage=dict(peau='#f0c9a0', peau2='#e5a988', tissu='#5a4a3a', torse='#2f5fa8', accent='#2f5fa8', cuir='#6b4423',
                      botte='#4a321f', metal='#c9ced6', carrure=.9, tete=.14, nez=('rond', .3), casque='#c9ced6', epaulieres='or'),
        mage=dict(peau='#f0c9a0', peau2='#e5a988', tissu='#f2ecdc', torse='#f2ecdc', robe='#f2ecdc', accent='#e3b44a', cuir='#6b4423',
                  botte='#4a321f', tete=.15, nez=('rond', .3), barbe='#f4f1ea', chapeau='#2f5fa8'),
        champion=dict(peau='#f0c9a0', peau2='#e5a988', tissu='#5a4a3a', torse='#c9ced6', accent='#2f5fa8', cuir='#6b4423', botte='#6a7380',
                      metal='#c9ced6', carrure=1.1, tete=.12, nez=('rond', .28), casque='#d5dae2', epaulieres='or', cape='#2f5fa8'),
        arme=epee, bouclier=dict(col='#2f5fa8', bord='#e3b44a', embleme='#e3b44a')),
    'horde': dict(
        mur='rondins', toit='tente', lueur='#ff9a4a', glace='#a8e6ff',
        equipage=dict(peau='#4f9a3a', peau2='#63b04a', tissu='#7a4f2c', torse='#4f9a3a', accent='#a8322a', cuir='#4a321f',
                      botte='#3a2a1c', metal='#7d8794', carrure=1.05, tete=.13, nez=('rond', .26), defenses=1, oreilles=.35,
                      cheveux='iroquoise', epaulieres='cuir', sourcils=1, yeux='#ff5a3c'),
        mage=dict(peau='#4f9a3a', peau2='#63b04a', tissu='#a8322a', torse='#a8322a', robe='#7a2a22', accent='#e5b24e', cuir='#4a321f',
                  botte='#3a2a1c', tete=.14, nez=('rond', .26), defenses=1, oreilles=.35, sourcils=1, yeux='#ffb347', capuche='#7a4f2c'),
        champion=dict(peau='#4f9a3a', peau2='#63b04a', tissu='#7a4f2c', torse='#4f9a3a', cuir='#4a321f', botte='#3a2a1c',
                      metal='#7d8794', carrure=1.25, tete=.12, jambes=.33, voute=.15, machoire=1, sourcils=1, yeux='#ff5a3c',
                      nez=('rond', .26), defenses=1, oreilles=.35, cheveux='chignon', epaulieres='pointes', harnais=1, cape='#a8322a'),
        arme=hache, bouclier=dict(col='#6b4423', bord='#7d8794', embleme='#a8322a')),
    'sylvestres': dict(
        mur='ecorce', toit='feuillage', lueur='#c8ffb0', glace='#d8f4ff',
        equipage=dict(peau='#d9c7f0', peau2='#c9b2e6', tissu='#3f7d4a', torse='#4f9a5a', accent='#8c70bd', cuir='#5a3d26',
                      botte='#5a3d26', carrure=.85, tete=.14, nez=('rond', .22), oreilles=.7, capuche='#3f7d4a'),
        mage=dict(peau='#d9c7f0', peau2='#c9b2e6', tissu='#4f9a5a', torse='#4f9a5a', robe='#2e6248', accent='#d8e99b', cuir='#5a3d26',
                  botte='#5a3d26', tete=.15, nez=('rond', .22), oreilles=.7, couronne='#d8e99b'),
        champion=dict(peau='#8a6a44', peau2='#a5835a', tissu='#4f7a3a', torse='#6b4a2f', accent='#8c70bd', cuir='#5a3d26', botte='#5a3d26',
                      carrure=1.1, tete=.13, nez=('long', .25), oreilles=.5, couronne='#6fc06a', epaulieres='cuir', cape='#3f7d4a'),
        arme=lambda p, H: baton(p, H, '#c8ffb0', '#5a3d26'), bouclier=None),
    'nains': dict(
        mur='rivets', toit='dome', lueur='#ffb347', glace='#9fe0ff',
        equipage=dict(peau='#e8b38a', peau2='#d99a74', tissu='#5f6a78', torse='#5f91a8', accent='#c8803e', cuir='#5a3d26',
                      botte='#3a2a1c', metal='#a9adb5', carrure=1.15, tete=.15, jambes=.28, nez=('rond', .36), barbe='#c8692e',
                      casque='#a9adb5', epaulieres='or'),
        mage=dict(peau='#e8b38a', peau2='#d99a74', tissu='#5f91a8', torse='#5f91a8', robe='#3d4148', accent='#e0a34d', cuir='#5a3d26',
                  botte='#3a2a1c', carrure=1.1, tete=.15, jambes=.28, nez=('rond', .36), barbe='#e8e2d6', lunettes=1),
        champion=dict(peau='#8a929c', peau2='#a9adb5', tissu='#5f6a78', torse='#7d8794', accent='#c8803e', cuir='#4a4d55', botte='#4a4d55',
                      metal='#c8803e', carrure=1.25, tete=.11, jambes=.32, nez=('rond', .2), yeux='#ffb347', casque='#7d8794',
                      epaulieres='or'),
        arme=marteau, bouclier=dict(col='#7d8794', bord='#c8803e', embleme='#ffb347')),
    'ombres': dict(
        mur='obsidienne', toit='epines', lueur='#7ff3ff', glace='#c79bff',
        equipage=dict(peau='#b9c3d6', peau2='#9aa6bd', tissu='#2c2340', torse='#3d2f57', accent='#7ff3ff', cuir='#2a1d3a',
                      botte='#1d1726', carrure=.85, tete=.14, nez=('crochu', .22), yeux='#7ff3ff', capuche='#3d2f57'),
        mage=dict(peau='#b9c3d6', peau2='#9aa6bd', tissu='#3d2f57', torse='#3d2f57', robe='#251c38', accent='#7ff3ff', cuir='#2a1d3a',
                  botte='#1d1726', tete=.15, nez=('crochu', .22), yeux='#7ff3ff', capuche='#251c38'),
        champion=dict(peau='#b9c3d6', peau2='#9aa6bd', tissu='#2c2340', torse='#3d2f57', accent='#7ff3ff', cuir='#2a1d3a', botte='#2a1d3a',
                      metal='#4a3a66', carrure=1.15, tete=.12, nez=('crochu', .2), yeux='#7ff3ff', casque='#4a3a66', cornes=1,
                      epaulieres='pointes', cape='#251c38'),
        arme=lambda p, H: lame_courbe(p, H, '#7ff3ff'), bouclier=None),
}
for _f, _s in STYLE.items(): _s['p'] = PAL[_f]; _s['f'] = _f

# ---------------------------------------------------------------- murs (fût de la tour)
def fut(r, st, z, rb, rt, h):
    """Corps de tour entre z et z+h. Retourne le haut."""
    p, m = st['p'], st['mur']
    if m == 'pierre':
        cylindre('Talus', p['moyen'], rb * 1.25, rb * 1.05, min(.14, h * .35), 10, (0, 0, z), r, biseau=.02)
        for q in range(8):
            a = q * 2 * math.pi / 8
            boite(f'Bloc{q}', p['pierre'], .1, .07, .07, (math.cos(a) * rb * 1.15, math.sin(a) * rb * 1.15, z + .04), 0, r, (0, 0, a + math.pi / 2))
        cylindre('Fut', p['pierre'], rb, rt, h, 10, (0, 0, z), r, biseau=.01)
        anneau('Bandeau', p['moyen'], (rb + rt) / 2 - .005, .018, 16, 3, (0, 0, z + h * .6), r)
    elif m == 'rondins':
        n = 9
        for q in range(n):
            a = q * 2 * math.pi / n; rr = (rb + rt) / 2 * .85
            hh = h * (1 + .08 * ((q * 7) % 3))
            cylindre(f'Rondin{q}', '#7a5234' if q % 2 else '#8a5f3a', rb * .32, rt * .3, hh, 6, (math.cos(a) * rr, math.sin(a) * rr, z), r)
            cone(f'Pointe{q}', '#9a7048', rt * .3, .06, 6, (math.cos(a) * rr, math.sin(a) * rr, z + hh), r)
        cylindre('Coeur', '#4a321f', rt * .8, rt * .8, h, 8, (0, 0, z), r)
        for k, zz in enumerate((.25, .7)):
            anneau(f'Corde{k}', '#c9a46a', (rb + rt) / 2 * 1.05, .018, 14, 3, (0, 0, z + h * zz), r)
        for q in range(4):
            a = q * math.pi / 2 + .4
            cone(f'Pic{q}', '#e8dcc0', .025, .14, 5, (math.cos(a) * rb * 1.05, math.sin(a) * rb * 1.05, z + .08), r, (math.sin(a) * -1.2, math.cos(a) * 1.2, 0))
        prisme('Peau', '#a8322a', [(-.08, 0), (.08, 0), (.07, -.16), (0, -.2), (-.07, -.16)], .012, (0, -(rb + rt) / 2 * 1.02, z + h * .62), r)
    elif m == 'ecorce':
        cylindre('Tronc', '#6b4a2f', rb * 1.15, rt * .9, h, 10, (0, 0, z), r, lisse=True)
        for q in range(5):
            a = q * 2 * math.pi / 5 + .3
            cone(f'Contrefort{q}', '#5a3d26', rb * .4, h * .55, 6, (math.cos(a) * rb * .95, math.sin(a) * rb * .95, z), r, (math.sin(a) * .25, -math.cos(a) * -.25, 0))
        anneau('Lierre', '#4f9a4a', (rb + rt) / 2, .022, 14, 3, (0, 0, z + h * .45), r, rot=(.2, .1, 0))
        for q in range(3):
            a = q * 2.1 + 1
            sphere(f'Mousse{q}', '#5aa84f', .05, (math.cos(a) * rb * .95, math.sin(a) * rb * .95, z + h * (.2 + q * .22)), (1, 1, .6), 8, 4, r)
        sphere('Lanterne', st['lueur'], .03, (0, -rb * 1.02, z + h * .7), (1, 1, 1.3), 8, 4, r, emis=2)
    elif m == 'rivets':
        cylindre('Base', '#4a4d55', rb * 1.2, rb * 1.1, min(.12, h * .3), 6, (0, 0, z), r, biseau=.015)
        cylindre('Fut', st['p']['pierre'], rb, rt, h, 6, (0, 0, z), r, biseau=.012)
        for k, zz in enumerate((.35, .8)):
            cylindre(f'Cercle{k}', '#c8803e', (rb + rt) / 2 * 1.06, (rb + rt) / 2 * 1.04, .035, 6, (0, 0, z + h * zz), r, metal=.7, rough=.3)
        for q in range(6):
            a = q * math.pi / 3 + math.pi / 6
            sphere(f'Rivet{q}', '#d9b37a', .016, (math.cos(a) * rb * .93, math.sin(a) * rb * .93, z + h * .5), (1, 1, 1), 6, 4, r, metal=.7)
        boite('Hublot', '#2b2b30', .07, .03, .07, (0, -rt * .95, z + h * .6), .02, r)
        anneau('CadreHublot', '#c8803e', .045, .01, 8, 3, (0, -rt * .98, z + h * .6), r, (math.pi / 2, 0, 0), metal=.7)
        sphere('Rune', st['lueur'], .025, (0, -rt * .99, z + h * .6), (1, .4, 1), 6, 4, r, emis=3)
    else:  # obsidienne
        cylindre('Fut', '#2c2340', rb * 1.05, rt * .85, h, 5, (0, 0, z), r, biseau=.01)
        boite('Faille', st['lueur'], .025, .02, h * .7, (0, -rb * .82, z + h * .45), 0, r, (-.08, 0, 0), emis=3)
        for q in range(5):
            a = q * 2 * math.pi / 5 + math.pi / 5
            cone(f'Epine{q}', '#4a3a66', .035, .16, 4, (math.cos(a) * rb * .9, math.sin(a) * rb * .9, z + h * (.3 + .1 * (q % 2))), r,
                 (-math.sin(a) * 1.0, math.cos(a) * 1.0, 0))
        anneau('Halo', st['lueur'], rb * 1.15, .01, 16, 3, (0, 0, z + h * .15), r, emis=2)
    return z + h

def ronde(r, st, z, rad):
    """Chemin de ronde (plate-forme) au sommet. Retourne le niveau du sol de la plate-forme."""
    p, m = st['p'], st['mur']
    if m == 'pierre':
        for q in range(8):
            a = q * 2 * math.pi / 8
            boite(f'Console{q}', p['moyen'], .06, .07, .07, (math.cos(a) * rad * .8, math.sin(a) * rad * .8, z - .05), 0, r, (0, 0, a + math.pi / 2))
        cylindre('Ronde', p['pierre'], rad, rad, .05, 10, (0, 0, z), r, biseau=.012)
        for q in range(8):
            a = q * 2 * math.pi / 8 + math.pi / 8
            boite(f'Merlon{q}', p['pierre'], .075, .05, .07, (math.cos(a) * rad * .9, math.sin(a) * rad * .9, z + .085), 0, r, (0, 0, a + math.pi / 2))
    elif m == 'rondins':
        cylindre('Plancher', '#8a5a33', rad, rad, .04, 10, (0, 0, z), r)
        for q in range(9):
            a = q * 2 * math.pi / 9
            cylindre(f'Pieu{q}', '#7a5234', .02, .018, .1, 5, (math.cos(a) * rad * .9, math.sin(a) * rad * .9, z + .04), r)
            cone(f'PointePieu{q}', '#9a7048', .018, .04, 5, (math.cos(a) * rad * .9, math.sin(a) * rad * .9, z + .14), r)
    elif m == 'ecorce':
        cylindre('Nid', '#5a3d26', rad, rad * .85, .05, 10, (0, 0, z), r, biseau=.01)
        anneau('Branches', '#6b4a2f', rad * .95, .025, 12, 4, (0, 0, z + .06), r)
    elif m == 'rivets':
        cylindre('Plateau', '#4a4d55', rad, rad, .05, 6, (0, 0, z), r, biseau=.012)
        for q in range(6):
            a = q * math.pi / 3
            cylindre(f'Montant{q}', '#c8803e', .012, .012, .1, 5, (math.cos(a) * rad * .9, math.sin(a) * rad * .9, z + .05), r, metal=.7)
        anneau('Rambarde', '#c8803e', rad * .9, .012, 6, 3, (0, 0, z + .15), r, metal=.7, rough=.3)
    else:
        cylindre('Plateau', '#3d2f57', rad, rad * .9, .05, 7, (0, 0, z), r, biseau=.01)
        for q in range(7):
            a = q * 2 * math.pi / 7
            cone(f'Pic{q}', '#4a3a66', .025, .12, 4, (math.cos(a) * rad * .92, math.sin(a) * rad * .92, z + .05), r)
    return z + .05

def toit(r, st, z, rad):
    """Toit sur poteaux au-dessus de la plate-forme (z = bas du toit)."""
    p, t = st['p'], st['toit']
    if t == 'fleche':
        cylindre('Avancee', p['toit'], rad * 1.15, rad, .04, 10, (0, 0, z), r, biseau=.008)
        cone('Fleche', p['toit'], rad, rad * 1.3, 10, (0, 0, z + .04), r)
        anneau('LisereToit', p['or_'], rad * 1.08, .014, 16, 3, (0, 0, z + .02), r, metal=.7, rough=.3)
        sphere('Pommeau', p['or_'], .035, (0, 0, z + rad * 1.3 + .05), (1, 1, 1.2), 8, 6, r, metal=.7, rough=.3)
        cylindre('Hampe', p['or_'], .008, .008, .14, 6, (0, 0, z + rad * 1.3 + .07), r, metal=.7)
        prisme('Banniere', p['accent'], [(0, 0), (.15, -.015), (.12, -.045), (.15, -.075), (0, -.08)], .01, (0, 0, z + rad * 1.3 + .2), r)
    elif t == 'tente':
        cone('Tente', '#8a3a2a', rad * 1.15, rad * 1.1, 8, (0, 0, z), r)
        for q in range(3):
            a = q * 2.1
            cylindre(f'Perche{q}', '#6b4423', .012, .01, rad * 1.5, 5, (0, 0, z + rad * .5), r, rot=(math.cos(a) * .3, math.sin(a) * .3, 0))
        for q in range(4):
            a = q * math.pi / 2 + math.pi / 4
            cone(f'Croc{q}', '#f0e6cc', .025, .12, 5, (math.cos(a) * rad * 1.05, math.sin(a) * rad * 1.05, z + .02), r,
                 (-math.sin(a) * -1.9, math.cos(a) * -1.9, 0))
        prisme('Fanion', '#e5b24e', [(0, 0), (.12, -.02), (0, -.07)], .01, (0, 0, z + rad * 1.55), r)
    elif t == 'feuillage':
        for q, (dx, dy, dz, rr) in enumerate(((0, 0, .12, 1.0), (.55, .2, 0, .7), (-.5, .3, .02, .7), (.1, -.55, -.02, .65), (-.2, .5, .2, .55))):
            sphere(f'Feuilles{q}', '#4f9a4a' if q % 2 else '#5fae55', rad * rr * .75, (dx * rad, dy * rad, z + dz + rad * .3), (1, 1, .75), 10, 6, r)
        for q in range(3):
            a = q * 2.1
            sphere(f'Fleur{q}', '#e8d5ff', .025, (math.cos(a) * rad * .7, math.sin(a) * rad * .7, z + rad * .55), (1, 1, .6), 6, 4, r, emis=.8)
    elif t == 'dome':
        sphere('Dome', '#c8803e', rad, (0, 0, z), (1, 1, .7), 12, 6, r, metal=.7, rough=.35)
        cylindre('Cheminee', '#4a4d55', .04, .045, rad * 1.1, 6, (rad * .4, rad * .2, z), r)
        sphere('Fumee', '#c9c4ba', .05, (rad * .4, rad * .2, z + rad * 1.15), (1, 1, .8), 6, 4, r)
        sphere('Pointe', '#d9b37a', .03, (0, 0, z + rad * .7), (1, 1, 1.3), 6, 4, r, metal=.7)
    else:  # épines
        for q in range(6):
            a = q * math.pi / 3
            cone(f'EpineToit{q}', '#3d2f57', .05, rad * 1.1, 4, (math.cos(a) * rad * .8, math.sin(a) * rad * .8, z), r,
                 (-math.sin(a) * -.35, math.cos(a) * -.35, 0))
        o = pivot('Cristal', (0, 0, z + rad * .8), r)
        cone('CristalHaut', st['lueur'], .06, .14, 4, (0, 0, 0), o, emis=2.5)
        cone('CristalBas', st['lueur'], .06, .1, 4, (0, 0, 0), o, (math.pi, 0, 0), emis=2.5)

def poteaux(r, st, z, rad, h):
    bois = {'pierre': '#6b4423', 'rondins': '#6b4423', 'ecorce': '#5a3d26', 'rivets': '#4a4d55', 'obsidienne': '#3d2f57'}[st['mur']]
    n = 4 if st['mur'] != 'obsidienne' else 3
    for q in range(n):
        a = q * 2 * math.pi / n + math.pi / 4
        cylindre(f'Poteau{q}', bois, .016, .016, h, 6, (math.cos(a) * rad, math.sin(a) * rad, z), r)

def equipage(parent, st, H, arme=None, cle='equipage', **extra):
    o = dict(st[cle]); o.update(extra)
    if arme: o['arme_g' if arme is arc_court else 'arme'] = arme
    outils.SIMPLE = True
    try: humanoide(parent, o, H)
    finally: outils.SIMPLE = False

def _poser_tir(c):
    for o in c.objects:
        if o.name.startswith('BrasG'): o.rotation_euler = (-1.45, 0, .2)
        if o.name.startswith('BrasD'): o.rotation_euler = (-1.2, 0, -.6)

# ---------------------------------------------------------------- archétypes
def debut(nom, faction):
    c = collection(nom); dans(c)
    r = pivot(nom); st = STYLE[faction]
    z = SOCLES[faction](r)
    return c, r, st, z

def archer(nom, faction, elite=False):
    """Emplacements 0 (tour de guet) et 6 (tireur d'élite : tour haute et baliste)."""
    c, r, st, z = debut(nom, faction)
    zt = fut(r, st, z, .2, .17, .44 if elite else .34)
    zp = ronde(r, st, zt, .25)
    tour = pivot('Tourelle', (0, 0, zp), r)
    if elite:
        # baliste : affût, arc horizontal, carreau ; servant derrière
        bois = '#6b4423' if st['mur'] != 'rivets' else '#4a4d55'
        boite('Affut', bois, .1, .18, .06, (0, 0, .05), .01, tour)
        boite('Rail', bois, .04, .3, .03, (0, -.06, .1), .006, tour)
        prisme('ArcBaliste', st['p']['or_'], [(-.2, 0), (-.18, .035), (0, .02), (.18, .035), (.2, 0), (0, -.01)], .03, (0, -.18, .1), tour, (math.pi / 2, 0, 0), metal=.5)
        boite('Carreau', '#e8e2cf', .015, .3, .015, (0, -.12, .125), 0, tour)
        cone('PointeCarreau', '#c9ced6', .02, .05, 4, (0, -.27, .125), tour, (math.pi / 2, 0, 0), metal=.6)
        a = pivot('Servant', (0, .14, 0), tour)
        equipage(a, st, .24)
        if st['mur'] in ('pierre', 'rondins', 'ecorce'):
            cylindre('Mat', '#6b4423', .01, .01, .45, 5, (-.2, .1, zp), r)
            prisme('Etendard', st['p']['accent'], [(0, 0), (.14, -.02), (.12, -.06), (.14, -.1), (0, -.11)], .01, (-.2, .1, zp + .44), r)
    else:
        poteaux(r, st, zp, .17, .24)
        toit(r, st, zp + .24, .25)
        equipage(tour, st, .26, arc_court)
        _poser_tir(c)
    peindre(r, sol=.7)
    return r

def garde(nom, faction, champion=False):
    """Emplacements 1 (gardien) et 7 (champion, plus grand, cape et bouclier)."""
    c, r, st, z = debut(nom, faction)
    p = st['p']
    cylindre('Piedestal', p['moyen'], .26, .24, .08, 10 if st['mur'] != 'rivets' else 6, (0, 0, z), r, biseau=0 if champion else .015)
    cylindre('Marche', p['pierre'], .22, .21, .04, 10 if st['mur'] != 'rivets' else 6, (0, 0, z + .08), r, biseau=.01)
    tour = pivot('Tourelle', (0, 0, z + .12), r)
    H = .74 if champion else .62
    o = dict(st['champion'] if champion else st['equipage'])
    if not champion:
        o.update(carrure=o.get('carrure', 1) * 1.05)
        o.pop('cape', None)
    o['arme'] = st['arme']
    if champion and st.get('bouclier'):
        b = st['bouclier']; o['arme_g'] = lambda pv, HH: bouclier(pv, HH, b['col'], b['bord'], b['embleme'])
    outils.SIMPLE = not champion
    try: humanoide(tour, o, H)
    finally: outils.SIMPLE = False
    # pose : arme levée en garde
    for x in c.objects:
        if x.name.startswith('BrasD'): x.rotation_euler = (-.9, .25, 0)
        if x.name.startswith('BrasG'): x.rotation_euler = (-.6, -.3, 0)
    peindre(r, sol=.7)
    return r

def givre(nom, faction, entrave=False):
    """Emplacements 2 (obélisque et cristal) et 8 (entrave : plus grand, éclats en orbite)."""
    c, r, st, z = debut(nom, faction)
    p = st['p']
    seg = 4 if st['mur'] != 'rivets' else 6
    hh = .5 if entrave else .38
    pierre = {'ecorce': '#6b4a2f', 'obsidienne': '#2c2340', 'rondins': '#7a5234'}.get(st['mur'], p['pierre'])
    cylindre('Obelisque', pierre, .15, .1, hh, seg, (0, 0, z), r, biseau=.012, rot=(0, 0, math.pi / 4))
    cylindre('Chapiteau', p['moyen'], .14, .15, .05, seg, (0, 0, z + hh), r, biseau=.01, rot=(0, 0, math.pi / 4))
    boite('Rune', st['lueur'], .03, .02, hh * .55, (0, -.11, z + hh * .45), 0, r, emis=2.5)
    if st['mur'] == 'rondins':
        for s in (-1, 1): cone(f'Corne{s}', '#f0e6cc', .03, .2, 6, (s * .1, 0, z + hh), r, (0, s * .6, 0))
    if st['mur'] == 'ecorce':
        for q in range(3): sphere(f'Feuille{q}', '#5fae55', .06, (math.cos(q * 2.1) * .12, math.sin(q * 2.1) * .12, z + hh * .9), (1, 1, .5), 8, 4, r)
    cr = pivot('Cristal', (0, 0, z + hh + .2), r)
    k = 1.35 if entrave else 1
    cone('CristalHaut', st['glace'], .09 * k, .22 * k, 6, (0, 0, 0), cr, emis=1.2, rough=.2)
    cone('CristalBas', st['glace'], .09 * k, .14 * k, 6, (0, 0, 0), cr, (math.pi, 0, 0), emis=1.2, rough=.2)
    anneau('Givre', '#e8fbff', .2 * k, .01, 16, 3, (0, 0, z + hh + .03), r, emis=1.5)
    if entrave:
        ec = pivot('Eclats', (0, 0, z + hh + .2), r)
        for q in range(3):
            a = q * 2.094
            cone(f'Eclat{q}', st['glace'], .035, .12, 4, (math.cos(a) * .26, math.sin(a) * .26, -.05), ec, emis=1.5, rough=.2)
        for s in (-1, 1):
            cylindre(f'Chaine{s}', '#8a929c', .012, .012, .3, 4, (s * .2, 0, z), r, rot=(0, -s * .45, 0), metal=.6)
    peindre(r, sol=.72)
    return r

def canon(nom, faction):
    """Emplacement 3 : artillerie à explosion (canon, mortier, fleur explosive…)."""
    c, r, st, z = debut(nom, faction)
    p = st['p']; f = faction
    cylindre('Plate', p['moyen'], .3, .29, .06, 10 if f != 'nains' else 6, (0, 0, z), r, biseau=.012)
    tour = pivot('Tourelle', (0, 0, z + .06), r)
    if f == 'sylvestres':
        # fleur explosive : bulbe sur une tige, pétales, graines-bombes
        cylindre('Tige', '#4f9a4a', .04, .03, .2, 8, (0, 0, 0), tour, lisse=True)
        for q in range(5):
            a = q * 2 * math.pi / 5
            sphere(f'Petale{q}', '#e86fa8', .1, (math.cos(a) * .1, math.sin(a) * .1, .22), (1, .5, .25), 8, 4, tour, rot=(0, 0, a))
        sphere('Bulbe', '#f4c04e', .1, (0, -.04, .27), (1, 1, 1.1), 10, 6, tour)
        sphere('Graine', '#5a3d26', .045, (0, -.12, .32), (1, 1, 1), 8, 4, tour)
        for q in range(3):
            a = q * 2.1 + .5
            sphere(f'Feuille{q}', '#5fae55', .08, (math.cos(a) * .17, math.sin(a) * .17, .05), (1.4, .5, .25), 8, 4, tour, rot=(0, 0, a))
        peindre(r, sol=.72); return r
    bois = {'alliance': '#6b4423', 'horde': '#5a3a22', 'nains': '#4a4d55', 'ombres': '#2c2340'}[f]
    metal = {'alliance': '#4a4f58', 'horde': '#3a3330', 'nains': '#c8803e', 'ombres': '#4a3a66'}[f]
    for s in (-1, 1):
        boite(f'Flasque{s}', bois, .05, .26, .13, (s * .1, 0, .09), .012, tour)
        cylindre(f'Roue{s}', bois, .09, .09, .035, 10, (s * .15, .02, .09), tour, rot=(0, math.pi / 2, 0), biseau=.006)
        cylindre(f'Moyeu{s}', p['or_'], .03, .03, .04, 6, (s * .17, .02, .09), tour, rot=(0, math.pi / 2, 0), metal=.7)
    mortier = f == 'nains'
    ang = -.9 if mortier else -.35
    fut_c = pivot('Fut', (0, 0, .17), tour); fut_c.rotation_euler = (math.pi / 2 + ang, 0, 0)
    L, R = (.22, .085) if mortier else (.36, .065)
    cylindre('Canon', metal, R * 1.2, R, L, 12, (0, 0, -L * .3), fut_c, biseau=.008, metal=.6, rough=.4)
    for k, t in enumerate((.0, .45, .95)):
        anneau(f'Frette{k}', p['or_'], R * (1.2 - .2 * t) + .004, .012, 12, 3, (0, 0, -L * .3 + L * t), fut_c, metal=.7, rough=.3)
    cylindre('Bouche', '#1b1b1b', R * .7, R * .7, .01, 10, (0, 0, L * .7 - .004), fut_c)
    if f == 'horde':
        for q in range(4):
            a = q * math.pi / 2
            cone(f'Pique{q}', '#d9d2c0', .015, .06, 4, (math.cos(a) * R * 1.15, math.sin(a) * R * 1.15, L * .2), fut_c, (-math.sin(a) * 1.57, math.cos(a) * 1.57, 0))
    if f == 'ombres':
        sphere('Crane', '#e8e2cf', .055, (0, 0, -L * .32), (1, 1, 1), 8, 6, fut_c)
        for s in (-1, 1): sphere(f'Orbite{s}', st['lueur'], .013, (s * .022, -.05, -L * .32), (1, 1, 1), 6, 4, fut_c, emis=3)
    if f == 'alliance':
        sphere('Lion', p['or_'], .04, (0, 0, -L * .32), (1, 1, .8), 8, 4, fut_c, metal=.7)
    # boulets empilés
    for q, (x, y) in enumerate(((.2, .15), (.24, .1), (.17, .1))):
        sphere(f'Boulet{q}', '#2b2b30', .035, (x, y, .035), (1, 1, 1), 8, 4, tour)
    peindre(r, sol=.72)
    return r

def flammes(nom, faction):
    """Emplacement 4 : brasier à flammes continues (souffle en cône)."""
    c, r, st, z = debut(nom, faction)
    p = st['p']; f = faction
    fl = None
    if f == 'nains':
        boite('Fourneau', '#4a4d55', .36, .3, .3, (0, 0, z + .15), .03, r)
        boite('Gueule', '#1b1b1b', .16, .03, .12, (0, -.15, z + .13), .02, r)
        sphere('Braise', '#ff8a2a', .07, (0, -.13, z + .12), (1.1, .4, .7), 8, 4, r, emis=4)
        cylindre('Cheminee', '#3d4148', .06, .07, .4, 6, (.1, .06, z + .3), r, biseau=.008)
        anneau('Cercle', '#c8803e', .2, .014, 6, 3, (0, 0, z + .28), r, metal=.7)
        fl = pivot('Flamme', (.1, .06, z + .72), r)
    elif f == 'ombres':
        cylindre('Margelle', '#2c2340', .28, .26, .14, 7, (0, 0, z), r, biseau=.015)
        cylindre('Lave', '#ff6a2a', .22, .22, .02, 14, (0, 0, z + .13), r, emis=3)
        for q in range(4):
            a = q * 1.6
            sphere(f'Bulle{q}', '#ffb347', .03, (math.cos(a) * .12, math.sin(a) * .12, z + .15), (1, 1, .6), 6, 4, r, emis=4)
        for q in range(4):
            a = q * math.pi / 2 + math.pi / 4
            cone(f'Corne{q}', '#4a3a66', .04, .26, 4, (math.cos(a) * .24, math.sin(a) * .24, z + .12), r, (-math.sin(a) * -.3, math.cos(a) * -.3, 0))
        fl = pivot('Flamme', (0, 0, z + .15), r)
    else:
        col = {'alliance': p['moyen'], 'horde': '#5a3a22', 'sylvestres': '#6b4a2f'}[f]
        cylindre('Colonne', col, .12, .1, .3, 8, (0, 0, z), r, biseau=.012)
        vasque = {'alliance': '#c9ced6', 'horde': '#3a3330', 'sylvestres': '#5a3d26'}[f]
        cylindre('Vasque', vasque, .14, .24, .14, 12, (0, 0, z + .3), r, biseau=.012, metal=.5 if f != 'sylvestres' else 0)
        anneau('Bord', p['or_'], .24, .016, 14, 3, (0, 0, z + .44), r, metal=.6)
        if f == 'alliance':
            for s in (-1, 1):
                prisme(f'Aile{s}', p['or_'], [(0, 0), (s * .22, .14), (s * .25, .06), (s * .2, 0), (s * .22, -.06), (s * .1, -.04)], .02, (s * .2, 0, z + .38), r, metal=.6)
        if f == 'horde':
            for q in range(5):
                a = q * 2 * math.pi / 5
                cone(f'Pique{q}', '#d9d2c0', .02, .1, 4, (math.cos(a) * .24, math.sin(a) * .24, z + .44), r)
        if f == 'sylvestres':
            for q in range(4):
                a = q * math.pi / 2
                cone(f'Racine{q}', '#5a3d26', .04, .28, 5, (math.cos(a) * .18, math.sin(a) * .18, z + .48), r, (-math.sin(a) * .5, math.cos(a) * .5, 0))
        fl = pivot('Flamme', (0, 0, z + .44), r)
    feu = {'sylvestres': ('#2fb34a', '#9cf06a', '#f0ffb0'), 'ombres': ('#d93a1a', '#ff7a1a', '#ffd34d')}.get(f, ('#e0401a', '#ff8a1a', '#ffe08a'))
    sphere('FeuBase', feu[0], .15, (0, 0, .03), (1, 1, .45), 10, 5, fl, emis=1.2)
    for q in range(5):
        a = q * 2 * math.pi / 5
        cone(f'Langue{q}', feu[0], .06, .2 + .05 * (q % 2), 5, (math.cos(a) * .09, math.sin(a) * .09, .02), fl,
             (math.sin(a) * .35, -math.cos(a) * .35, 0), emis=1.2)
    cone('FeuMilieu', feu[1], .1, .3, 7, (0, 0, .02), fl, emis=1.8)
    cone('FeuCoeur', feu[2], .05, .18, 6, (0, 0, .03), fl, emis=2.5)
    peindre(r, sol=.72)
    return r

def mage(nom, faction, archimage=False):
    """Emplacements 5 (sanctuaire du mage) et 9 (archimage : plus haut, anneaux flottants)."""
    c, r, st, z = debut(nom, faction)
    p = st['p']
    h = .44 if archimage else .3
    zt = fut(r, st, z, .17, .14, h)
    seg = 6 if st['mur'] == 'rivets' else 10
    cylindre('Balcon', p['moyen'] if st['mur'] == 'pierre' else {'rondins': '#5a3a22', 'ecorce': '#5a3d26', 'rivets': '#4a4d55', 'obsidienne': '#3d2f57'}[st['mur']],
             .23, .2, .05, seg, (0, 0, zt), r, biseau=.012)
    anneau('LisereBalcon', p['or_'] if st['mur'] != 'obsidienne' else st['lueur'], .23, .012, 14, 3, (0, 0, zt + .05), r, metal=.6,
           emis=1.5 if st['mur'] == 'obsidienne' else 0)
    tour = pivot('Tourelle', (0, 0, zt + .05), r)
    extra = dict(epaulieres='or', cape=p['accent'] if faction != 'ombres' else '#251c38') if archimage else {}
    equipage(tour, st, .34 if archimage else .3, lambda pv, HH: baton(pv, HH, st['lueur'], '#5a3a1c'), cle='mage', **extra)
    for x in c.objects:
        if x.name.startswith('BrasD'): x.rotation_euler = (-.5, .2, 0)
        if x.name.startswith('BrasG'): x.rotation_euler = (-1.2, -.2, .3)
    ob = pivot('Orbe', (0, -.05, zt + .58 if archimage else zt + .52), r)
    sphere('OrbeMagique', st['lueur'], .06, (0, 0, 0), (1, 1, 1), 12, 8, ob, emis=4)
    if archimage:
        an = pivot('Anneaux', (0, 0, zt + .28), r)
        anneau('AnneauA', st['lueur'], .3, .012, 20, 3, (0, 0, 0), an, (.35, 0, 0), emis=2.5)
        anneau('AnneauB', p['or_'], .27, .01, 20, 3, (0, 0, 0), an, (-.3, .4, 0), emis=1.5)
        for q in range(4):
            a = q * math.pi / 2
            prisme(f'Rune{q}', st['lueur'], [(-.025, 0), (.025, 0), (0, .06)], .006, (math.cos(a) * .3, math.sin(a) * .3, 0), an, (0, 0, a), emis=3)
    peindre(r, sol=.72)
    return r

# emplacement j → (archétype, options)
EMPLACEMENTS = [(archer, {}), (garde, {}), (givre, {}), (canon, {}), (flammes, {}), (mage, {}),
                (archer, {'elite': True}), (garde, {'champion': True}), (givre, {'entrave': True}), (mage, {'archimage': True})]
FACTIONS = ['alliance', 'horde', 'sylvestres', 'nains', 'ombres']

def tour(faction, j):
    fn, kw = EMPLACEMENTS[j]
    return fn(f'{faction}_{j}', faction, **kw)
