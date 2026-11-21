"""Brute orc (CR orc) — pilote « organique » (2.30) : corps fondu d'un seul tenant, squelette bipède,
texture peinte cuite, animations marche / touche / mort sur os.
Guerrier trapu et voûté, énorme carrure, mâchoire prognathe à défenses, casque cornu, épaulières à pointes, hache."""
import math
from communs.organique import (Volume as V, symetrique, miroir, squelette, corps, colorier_et_lier, boule, cone, corne,
                               tore, plaque, profil, assembler, peindre_texture, lueur, finir, corps_haut, ajouter_pieces)
from communs.squelettes import BIPEDE, animer_bipede
from communs.echelles import hauteur

INFOS = {'categorie': 'monstre', 'titre': "Brute orc"}

PEAU, PEAU2, PEAU3 = '#4e9636', '#6cb04c', '#3d7a2b'
TISSU, CUIR, BOTTE = '#6b4a2e', '#4a321f', '#33261a'
FER, OS_, ROUGE, OR = '#6c7480', '#efe3c4', '#9a2a1e', '#e2b043'

# articulations (H = 1, regard vers -Y) : dos voûté, tête projetée en avant, bras longs
J = {'bassin': (0, .02, .40), 'ventre': (0, .03, .52), 'poitrine': (0, .02, .64), 'cou': (0, -.07, .71),
     'tete': (0, -.12, .75), 'sommet': (0, -.14, .93),
     'clavicule.L': (.06, .01, .69), 'epaule.L': (.22, .02, .69), 'coude.L': (.29, .04, .50),
     'poignet.L': (.30, -.02, .33), 'doigts.L': (.30, -.04, .25),
     'hanche.L': (.10, .02, .38), 'genou.L': (.12, -.02, .21), 'cheville.L': (.13, .02, .06), 'orteils.L': (.13, -.09, .02)}

def volumes():
    v = [
        V('Hanches', TISSU, c=(0, .02, .39), r=(.155, .125, .10)),
        V('Colonne', PEAU, c=(0, -.005, .50), r=(.165, .135, .12)),
        V('Torse', PEAU, c=(0, .025, .63), r=(.215, .16, .125)),
        V('Torse', PEAU, c=(.085, -.075, .635), r=(.095, .06, .07), rot=(0, .25, 0)),           # pectoraux
        V('Torse', PEAU, c=(.11, .05, .715), r=(.12, .09, .07), rot=(0, -.35, 0)),              # trapèzes
        V('Torse', PEAU, c=(0, .07, .70), r=(.15, .11, .08)),                                     # bosse du dos
        V('Cou', PEAU, a=(0, -.03, .69), b=(0, -.10, .76), ra=.078, rb=.07),
        V('Tete', PEAU, c=(0, -.115, .83), r=(.098, .095, .098)),                                 # crâne
        V('Tete', PEAU2, c=(0, -.18, .765), r=(.095, .075, .055), prio=1),                         # mâchoire prognathe
        V('Tete', PEAU3, c=(0, -.195, .855), r=(.088, .037, .032), rot=(.15, 0, 0), prio=1),       # arcade sourcilière
        V('Tete', PEAU2, c=(0, -.22, .815), r=(.032, .036, .032), prio=2),                          # nez
        V('Tete', PEAU2, c=(.025, -.228, .808), r=(.019, .02, .019), prio=2),                       # narine
        V('Tete', PEAU, c=(.115, -.09, .855), r=(.08, .015, .032), rot=(0, -.45, -.35)),            # oreille
        V('Bras.L', PEAU, c=(.215, .02, .675), r=(.085, .085, .085)),                             # deltoïde
        V('Bras.L', PEAU, a=(.235, .025, .64), b=(.29, .04, .50), ra=.075, rb=.058),              # biceps
        V('AvantBras.L', PEAU, a=(.29, .04, .50), b=(.30, -.02, .34), ra=.066, rb=.055),
        V('Main.L', PEAU2, c=(.30, -.03, .28), r=(.064, .07, .066)),                              # gros poing
        V('Cuisse.L', TISSU, a=(.10, .02, .38), b=(.12, -.02, .21), ra=.088, rb=.07),
        V('Tibia.L', BOTTE, a=(.12, -.02, .21), b=(.13, .02, .065), ra=.07, rb=.06),
        V('Pied.L', BOTTE, c=(.13, -.03, .04), r=(.068, .105, .045)),
        # 2.31 : musculature dessinée (abdominaux, obliques, dentelés, avant-bras, mollet) : elle ressort à la cuisson
        V('Colonne', PEAU2, c=(.037, -.128, .575), r=(.036, .026, .03)),                          # abdominaux (3 rangs)
        V('Colonne', PEAU2, c=(.035, -.13, .53), r=(.034, .025, .028)),
        V('Colonne', PEAU2, c=(.033, -.128, .487), r=(.032, .024, .026)),
        V('Colonne', PEAU, c=(.125, -.07, .52), r=(.05, .05, .075), rot=(0, 0, -.3)),              # obliques
        V('Torse', PEAU, c=(.16, -.06, .60), r=(.035, .03, .045), rot=(0, 0, -.4)),                # dentelés
        V('AvantBras.L', PEAU, c=(.297, .03, .455), r=(.07, .066, .075)),                         # avant-bras de forgeron
        V('Bras.L', PEAU2, c=(.255, -.02, .585), r=(.055, .05, .06)),                             # biceps saillant
    ]
    # les volumes hors du milieu rattachés à un os central (pectoral, trapèze, oreille, narine, abdominaux…) n'étaient
    # recopiés que du côté gauche avant la 2.31 : on les recopie aussi à droite
    v += [miroir(x) for x in v if '.L' not in x.os and x.kind == 'ellipse' and abs(x.c.x) > 1e-3]
    return symetrique(v)

def accessoires():
    p = []
    # ceinture, boucle, pagne, baudrier
    p.append(tore('Ceinture', CUIR, 'Hanches', (0, .015, .455), .16, .022, ech=(1, .86, 1)))
    p.append(plaque('Boucle', OR, 'Hanches', (0, -.128, .455), .065, .02, .052, biseau=.006))
    p.append(profil('PagneAvant', ROUGE, 'Hanches', [(-.07, 0), (.07, 0), (.06, -.15), (0, -.17), (-.06, -.15)], .016,
                    pos=(0, -.115, .43), rot=(-.12, 0, 0)))
    p.append(profil('PagneArriere', ROUGE, 'Hanches', [(-.09, 0), (.09, 0), (.08, -.15), (-.08, -.15)], .016,
                    pos=(0, .14, .43), rot=(.15, 0, 0)))
    p.append(tore('Baudrier', CUIR, 'Torse', (0, .02, .61), .19, .016, rot=(0, .75, 0), ech=(1, .82, 1)))
    for s, n in ((1, 'L'), (-1, 'R')):
        # épaulières : coque de fer + pointes d'os
        # 2.31 : épaulières plus massives et pointes plus longues (silhouette lisible de loin)
        p.append(boule(f'Epauliere.{n}', FER, f'Bras.{n}', (s * .235, .02, .72), .118, ech=(1, 1, .72), demi=True,
                       rot=(0, s * .5, 0)))
        p.append(tore(f'Rivets.{n}', OR, f'Bras.{n}', (s * .235, .02, .717), .116, .01, rot=(0, s * .5, 0), seg=12, seg2=4))
        for k, (dy, h) in enumerate(((-.05, .095), (.025, .12), (.09, .08))):
            p.append(corne(f'Pointe{k}.{n}', OS_, f'Bras.{n}', (s * .265, dy, .77), .022, h, .5, rot=(0, s * .35, 0)))
        # brassards et revers de bottes
        p.append(cone(f'Brassard.{n}', CUIR, f'AvantBras.{n}', (s * .295, .015, .39), .066, .062, .07, rot=(.33, 0, 0), seg=10))
        p.append(tore(f'Revers.{n}', CUIR, f'Tibia.{n}', (s * .123, -.015, .19), .072, .018))
        # défenses
        p.append(corne(f'Defense.{n}', OS_, 'Tete', (s * .05, -.235, .77), .02, .075, .9))
    # casque : calotte de fer + bandeau + cornes
    p.append(boule('Casque', FER, 'Tete', (0, -.105, .845), .108, ech=(1, 1.02, .85), demi=True, rot=(-.15, 0, 0)))
    p.append(tore('Bandeau', CUIR, 'Tete', (0, -.105, .845), .107, .012, rot=(-.15, 0, 0), ech=(1, 1.02, 1)))
    for s, n in ((1, 'L'), (-1, 'R')):
        p.append(corne(f'Corne.{n}', OS_, 'Tete', (s * .085, -.10, .89), .034, .16, 1.4, rot=(-.4, s * 1.2, 0)))
    # hache dans la main droite : manche + lame + pommeau
    m = (-.30, -.04, .28)
    p.append(cone('Manche', '#6e4a2a', 'Main.R', (m[0], m[1], m[2] - .1), .016, .014, .42, rot=(.25, 0, 0)))
    p.append(profil('Lame', '#c9d0d8', 'Main.R', [(0, .085), (.14, .155), (.165, 0), (.14, -.155), (0, -.085)], .018,
                    pos=(m[0] - .005, m[1] - .07, m[2] + .23), rot=(.25, 0, math.pi)))
    p.append(cone('Pommeau', OR, 'Main.R', (m[0], m[1] + .03, m[2] - .12), .024, .02, .025, rot=(.25, 0, 0)))
    # 2.31 : trophées et protections qui racontent le guerrier
    p.append(tore('Cordon', CUIR, 'Torse', (0, -.045, .685), .105, .007, rot=(.55, 0, 0), ech=(1, .9, 1), seg=12, seg2=3))
    for k in range(5):                                              # collier de crocs pendus sur le poitrail
        a = (k - 2) * .42
        p.append(corne(f'Croc{k}', OS_, 'Torse', (math.sin(a) * .1, -.045 - math.cos(a) * .088, .685 - math.cos(a) * .045),
                       .011, .04, .4, rot=(math.pi - .5, 0, a), seg=5, n=3))
    for s, n in ((1, 'L'), (-1, 'R')):
        p.append(boule(f'Genouillere.{n}', FER, f'Tibia.{n}', (s * .12, -.07, .215), .05, ech=(1, .55, 1), demi=True,
                       rot=(-1.45, 0, 0), seg=10))
        p.append(corne(f'PointeBras.{n}', FER, f'AvantBras.{n}', (s * .35, .02, .40), .014, .05, .3, rot=(0, s * 1.5, 0), seg=5, n=3))
    p.append(boule('Crane', OS_, 'Hanches', (.155, -.07, .43), .036, ech=(.9, .9, 1), seg=9))   # crâne-trophée à la ceinture
    p.append(plaque('CraneMachoire', OS_, 'Hanches', (.155, -.096, .405), .045, .022, .016, biseau=.004))
    # yeux (lueur)
    yeux = [boule(f'Oeil.{n}', '#ff6a2a', 'Tete', (s * .042, -.207, .832), .019, seg=7) for s, n in ((1, 'L'), (-1, 'R'))]
    return p, yeux

RELIEFS = [('CLOUDS', .013, .05, None),      # bosses et plis larges (chair, veines)
           ('CLOUDS', .005, .011, None)]     # grain de peau, plis du tissu

def fabriquer(cuire=True, animer=True):
    arm = squelette('brute_orc', J, BIPEDE)
    vols = volumes()
    c = corps('brute_orc', vols, voxel=.0095, lissage=5, triangles=1650)
    colorier_et_lier(c, vols)
    pieces, yeux = accessoires()
    # 2.31 : sculpture détaillée (grain de peau, rides, petits reliefs musculaires), cuite sur le corps léger
    haut = ajouter_pieces(corps_haut('brute_orc', vols, voxel=.0042, reliefs=RELIEFS), pieces) if cuire else None
    peau, lu = assembler('brute_orc', arm, c, pieces, yeux)
    if cuire: peindre_texture(peau, taille=512, occl=.07, source=haut, relief=1.0, taille_relief=384, taches=.12, taille_taches=9)
    lueur(lu, '#ff6a2a')
    finir(arm, hauteur('brute_orc'))
    if animer: animer_bipede(arm, hauteur('brute_orc'), lourd=1.0)
    return arm

def construire(ctx):
    fabriquer()
