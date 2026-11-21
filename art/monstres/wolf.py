"""Warg (CR wolf) — pilote « organique » (2.30) : grand loup de guerre, corps fondu d'un seul tenant, squelette
quadrupède (19 os), texture peinte cuite, animations trot / touche / mort.
Pelage gris acier, crinière noire hérissée sur les épaules, gueule entrouverte à crocs, yeux rouges, collier à pointes."""
import math
from communs.organique import (Volume as V, symetrique, squelette, corps, colorier_et_lier, boule, cone, corne,
                               tore, assembler, peindre_texture, lueur, finir, corps_haut, ajouter_pieces)
from communs.squelettes import QUADRUPEDE, animer_quadrupede
from communs.echelles import hauteur

INFOS = {'categorie': 'monstre', 'titre': "Warg"}

POIL, POIL2, VENTRE = '#69707a', '#8d959e', '#b3bac2'
PATTE, CRETE, TRUFFE = '#454a52', '#25292f', '#16181c'
GUEULE, SELLE = '#8f2a2a', '#4d535c'
CUIR, FER, OS_ = '#4a321f', '#6c7480', '#efe3c4'

# articulations (1 = hauteur de la tête ; regard vers -Y)
J = {'bassin': (0, .40, .55), 'reins': (0, .14, .60), 'garrot': (0, -.18, .66), 'nuque': (0, -.36, .74),
     'museau': (0, -.70, .66), 'machoire': (0, -.44, .66), 'menton': (0, -.66, .585),
     'queue0': (0, .52, .58), 'queue1': (0, .74, .50), 'queue2': (0, .93, .36),
     'epaule.L': (.13, -.20, .55), 'coude.L': (.14, -.15, .31), 'poignet.L': (.13, -.21, .10), 'doigtsA.L': (.13, -.30, .02),
     'hanche.L': (.14, .40, .50), 'jarret.L': (.15, .28, .30), 'cheville.L': (.15, .44, .12), 'doigtsP.L': (.15, .36, .02)}

def volumes():
    v = [
        V('Hanches', POIL, c=(0, .37, .56), r=(.165, .21, .16)),                                  # croupe
        V('Dos', POIL, c=(0, .07, .58), r=(.18, .30, .17)),                                       # tronc
        V('Dos', POIL, c=(0, -.17, .57), r=(.22, .17, .21)),                                      # poitrail
        V('Dos', VENTRE, c=(0, -.02, .455), r=(.12, .26, .07), prio=1),                          # ventre clair
        V('Dos', CRETE, c=(0, -.20, .73), r=(.20, .19, .12), prio=1),                             # crinière sur le garrot
        V('Cou', CRETE, a=(0, -.20, .68), b=(0, -.36, .76), ra=.15, rb=.115, prio=1),               # crinière du cou
        V('Tete', POIL, c=(0, -.43, .76), r=(.125, .13, .11)),                                     # crâne
        V('Tete', POIL2, a=(0, -.50, .72), b=(0, -.67, .68), ra=.075, rb=.052, prio=1),            # museau
        V('Tete', TRUFFE, c=(0, -.70, .69), r=(.032, .028, .026), prio=2, rel=0),                  # truffe
        V('Tete', CRETE, c=(0, -.47, .815), r=(.095, .045, .03), rot=(.25, 0, 0), prio=1),         # arcades
        V('Machoire', POIL2, a=(0, -.46, .665), b=(0, -.64, .625), ra=.048, rb=.034, prio=1),
        V('Machoire', GUEULE, c=(0, -.565, .652), r=(.03, .065, .016), prio=3, rel=0),              # 2.31 : gueule rouge entre les crocs
        V('Dos', SELLE, c=(0, .12, .705), r=(.11, .27, .05), prio=1),                                 # 2.31 : selle sombre sur le dos
        V('Avant.L', POIL, a=(.13, -.20, .55), b=(.14, -.15, .31), ra=.1, rb=.07),
        V('AvantBas.L', PATTE, a=(.14, -.15, .31), b=(.13, -.21, .10), ra=.062, rb=.048),
        V('PatteAvant.L', PATTE, c=(.13, -.255, .035), r=(.06, .08, .038)),
        V('Arriere.L', POIL, c=(.135, .37, .45), r=(.10, .15, .16)),                              # cuisse
        V('Arriere.L', POIL, a=(.14, .40, .48), b=(.15, .28, .30), ra=.085, rb=.062),
        V('ArriereBas.L', PATTE, a=(.15, .28, .30), b=(.15, .44, .12), ra=.058, rb=.045),
        V('PatteArriere.L', PATTE, c=(.15, .40, .035), r=(.058, .08, .038)),
        V('Queue1', POIL, a=(0, .50, .58), b=(0, .74, .50), ra=.06, rb=.065),
        V('Queue2', CRETE, a=(0, .74, .50), b=(0, .93, .36), ra=.06, rb=.025),
    ]
    return symetrique(v)

def accessoires():
    p = []
    for s, n in ((1, 'L'), (-1, 'R')):
        p.append(cone(f'Oreille.{n}', CRETE, 'Tete', (s * .07, -.40, .82), .04, .004, .12, rot=(.35, s * .35, 0), seg=5,
                      ech=(1, .55, 1)))
        p.append(corne(f'Croc.{n}', OS_, 'Tete', (s * .03, -.64, .665), .011, .05, -.4, rot=(math.pi, 0, 0)))
        p.append(corne(f'CrocBas.{n}', OS_, 'Machoire', (s * .028, -.60, .63), .009, .035, .3))
    # crinière hérissée : mèches pointues le long du dos (2.31 : plus longues, et deux rangs sur les côtés)
    for k, (y, z, h) in enumerate(((-.30, .83, .15), (-.20, .84, .19), (-.10, .80, .17), (.0, .76, .13), (.10, .73, .09))):
        os_ = 'Cou' if y < -.25 else 'Dos'
        p.append(corne(f'Meche{k}', CRETE, os_, (0, y, z - .03), .05, h, .9, rot=(-.5, 0, 0)))
        if k < 4:
            for s, n in ((1, 'L'), (-1, 'R')):
                p.append(corne(f'MecheCote{k}.{n}', CRETE, os_, (s * .075, y + .04, z - .07), .04, h * .75, .8, rot=(-.6, s * .55, 0)))
    # 2.31 : touffes de poils qui cassent la silhouette lisse : joues, poitrail, coudes, bout de la queue
    for s, n in ((1, 'L'), (-1, 'R')):
        p.append(corne(f'Joue.{n}', POIL2, 'Tete', (s * .105, -.45, .72), .032, .085, .7, rot=(0, s * 1.35, 0)))
        p.append(corne(f'Joue2.{n}', POIL, 'Tete', (s * .1, -.41, .69), .028, .07, .6, rot=(-.4, s * 1.2, 0)))
        p.append(corne(f'Coude.{n}', POIL, f'Avant.{n}', (s * .15, -.12, .36), .03, .075, .5, rot=(-2.4, 0, s * .35)))
        p.append(corne(f'Jarret.{n}', POIL, f'Arriere.{n}', (s * .16, .33, .36), .03, .07, .5, rot=(-2.2, 0, s * .3)))
    for k, (x, y, z) in enumerate(((0, -.33, .56), (.06, -.31, .58), (-.06, -.31, .58), (.03, -.30, .50), (-.03, -.30, .50))):
        p.append(corne(f'Poitrail{k}', POIL2, 'Cou' if z > .55 else 'Dos', (x, y, z), .035, .09, .5, rot=(-2.6, 0, x * 3)))
    for k, (x, y, z) in enumerate(((0, .80, .47), (.025, .85, .43), (-.025, .85, .43))):
        p.append(corne(f'QueueTouffe{k}', CRETE, 'Queue2', (x, y, z), .04, .11, .4, rot=(-2.2, 0, x * 6)))
    # collier de cuir à pointes de fer
    p.append(tore('Collier', CUIR, 'Cou', (0, -.31, .71), .115, .02, rot=(1.05, 0, 0), ech=(1, 1, 1)))
    for k in range(5):
        a = -1.2 + k * .6
        p.append(cone(f'Clou{k}', FER, 'Cou', (math.sin(a) * .12, -.31 - math.cos(a) * .04, .71 - math.cos(a) * .08),
                      .016, .002, .035, rot=(-1.9 + .0, 0, a * .9), seg=5))
    # 2.31 : griffes (3 par patte)
    for s, n in ((1, 'L'), (-1, 'R')):
        for pat, (py, pz) in (('PatteAvant', (-.325, .03)), ('PatteArriere', (.325, .03))):
            for d in (-.028, 0, .028):
                p.append(corne(f'Griffe{pat}{d}.{n}', OS_, f'{pat}.{n}', (s * (.14 if pat == 'PatteArriere' else .13) + d, py, pz), .009, .03, -.6,
                               rot=(-1.45, 0, 0), seg=4, n=2))
    yeux = [boule(f'Oeil.{n}', '#ff4a3a', 'Tete', (s * .055, -.52, .78), .018, seg=7) for s, n in ((1, 'L'), (-1, 'R'))]
    return p, yeux

RELIEFS = [('CLOUDS', .020, .020, (1.0, 11.0, 1.6)),  # mèches allongées le long du corps (de la tête vers la queue)
           ('CLOUDS', .006, .006, (1.0, 9.0, 1.0))]   # brins fins

def fabriquer(cuire=True, animer=True):
    arm = squelette('warg', J, QUADRUPEDE)
    vols = volumes()
    c = corps('warg', vols, voxel=.0105, lissage=5, triangles=1900)
    colorier_et_lier(c, vols, adoucir=.03)
    pieces, yeux = accessoires()
    # 2.31 : sculpture détaillée (mèches de poils couchées vers l'arrière, crinière ébouriffée), cuite sur le corps léger
    haut = ajouter_pieces(corps_haut('warg', vols, voxel=.0045, reliefs=RELIEFS), pieces) if cuire else None
    peau, lu = assembler('warg', arm, c, pieces, yeux)
    if cuire: peindre_texture(peau, taille=512, occl=.07, H=.85, source=haut, relief=1.0, taille_relief=512, taches=.08,
                              taille_taches=6)
    lueur(lu, '#ff4a3a')
    finir(arm, hauteur('warg') * 1.62)   # même encombrement que le warg 2.29 (0,39 de haut, 0,75 de long)
    if animer: animer_quadrupede(arm, hauteur('warg') * 1.62)
    return arm

def construire(ctx):
    fabriquer()
