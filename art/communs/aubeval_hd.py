"""Royaume d'Aubeval (2.40, direction « grimdark » validée sur la Cour des Ossements) : 10 tours qui ne sont pas toutes
des tours. Royaume humain austère et pieux : pierre calcaire noircie, ardoise, chêne, fer, bleu royal passé, or terni.

Soldats et inquisiteur au procédé des monstres organiques (communs/peuples_hd.py) ; machines de siège et bâtiments en
pièces peintes avec l'occlusion cuite (tours_hd.peindre_architecture).
Pièces animées : Tourelle (vise), Cristal (tourne), Anneaux (tournent), Orbe (flotte), Flamme (vacille)."""
import math
from mathutils import Vector
from . import tours_hd as HD, peuples_hd as P
from .outils import pivot, cylindre, boite, sphere, cone, prisme, anneau, collection, dans
from .organique import boule, corne, profil, plaque, tore
from .organique import cone as cone_o
from .neige import enneiger

CALC, CALC2, NUIT = '#8c867a', '#6b665d', '#1c1b1f'          # calcaire, calcaire sombre, ombre
ARDOISE, CHENE, CHENE2 = '#3a3d47', '#5a4230', '#3d2c20'     # ardoise, chêne, chêne sombre
FER, FER2, OR, BLEU, BLEU2 = '#34343a', '#55555c', '#a8873a', '#2c3a5c', '#1f2940'
CIRE, LUMIERE = '#d8cba6', '#ffd98a'
CHAIR, CHAIR2 = '#a98470', '#8f6a5a'
SOL = .12

# ---------------------------------------------------------------- socle
def socle(r, cote=.8):
    """Dallage de pierre calcaire à bordure moulurée, bornes d'angle coiffées de fer, congères."""
    d = cote / 2
    boite('Assise', NUIT, cote, cote, .05, (0, 0, .025), .01, r)
    dal = pivot('Dallage', (0, 0, 0), r)
    boite('Dalle', CALC2, cote * .92, cote * .92, .05, (0, 0, .07), .008, dal)
    for i in range(4):
        for j in range(4):
            boite(f'Pave{i}{j}', CALC, cote * .21, cote * .21, .012, ((i - 1.5) * cote * .225, (j - 1.5) * cote * .225, .1), .004, dal)
    for k, (x, y, sx, sy) in enumerate(((-.3, .33, .16, .05), (.28, .34, .1, .04), (.34, -.12, .04, .12), (-.33, -.22, .05, .1))):
        sphere(f'Congere{k}', '#e6edf5', 1, (x * cote / .8, y * cote / .8, .1), (sx, sy, .022), 8, 4, dal, rough=.9)
    for sx in (-1, 1):
        for sy in (-1, 1):
            cylindre(f'Borne{sx}{sy}', CALC, .045, .05, .12, 8, (sx * d * .88, sy * d * .88, .05), r)
            cone(f'Coiffe{sx}{sy}', FER, .05, .05, 8, (sx * d * .88, sy * d * .88, .17), r, metal=.5)
    return SOL

def debut(nom):
    c = collection(nom); dans(c)
    r = pivot(nom)
    return c, r, socle(r)

def finir(r):
    HD.peindre_sauf_statues(r, sol=.5, cime=1.0, bruit=.12)
    enneiger(r, 6000)
    HD.peindre_architecture(r)
    return r

def creneaux(nom, parent, cote, z, n=3, col=CALC):
    for s in range(4):
        a = s * math.pi / 2
        for k in range(n):
            t = (k - (n - 1) / 2) * cote / n
            x, y = math.cos(a) * cote / 2 + -math.sin(a) * t, math.sin(a) * cote / 2 + math.cos(a) * t
            boite(f'{nom}{s}{k}', col, .055, .055, .07, (x, y, z + .035), .004, parent, (0, 0, a))

def fenetre(nom, parent, l, h, pos, rot=(0, 0, 0), col=NUIT):
    pts = [(-l / 2, 0), (l / 2, 0), (l / 2, h * .7), (0, h), (-l / 2, h * .7)]
    return prisme(nom, col, pts, .02, pos, parent, rot)

def etendard(nom, parent, pos, h=.3, col=BLEU, rot=(0, 0, 0)):
    """Oriflamme bleue à liseré d'or, bas fendu en deux pointes."""
    pts = [(-.05, 0), (.05, 0), (.05, -h), (0, -h * .8), (-.05, -h)]
    prisme(nom, col, pts, .006, pos, parent, rot)
    prisme(nom + 'Lis', OR, [(-.012, -.04), (.012, -.04), (.012, -.12), (-.012, -.12)], .008, pos, parent, rot)

# ---------------------------------------------------------------- soldats (hauteur 1)
def chapel(hc, col=FER):
    return [boule('Chapel', col, 'Tete', tuple(hc + Vector((0, 0, .022))), .066, demi=True, seg=14),
            tore('Bord', col, 'Tete', tuple(hc + Vector((0, 0, .03))), .085, .012, ech=(1, 1, .45), seg=16)]

def tabard(J, col=BLEU, liseré=OR):
    b = J['poitrine'] + Vector((0, -.088, .06))
    pts = [(-.07, 0), (.07, 0), (.075, -.36), (0, -.4), (-.075, -.36)]
    return [profil('Tabard', col, 'Torse', pts, .008, pos=tuple(b)),
            profil('Croix', liseré, 'Torse', [(-.012, -.04), (.012, -.04), (.012, -.2), (-.012, -.2)], .01, pos=tuple(b + Vector((0, -.004, 0)))),
            profil('Traverse', liseré, 'Torse', [(-.045, -.08), (.045, -.08), (.045, -.1), (-.045, -.1)], .01, pos=tuple(b + Vector((0, -.004, 0))))]

def arbalete(J):
    m = J['poignet.L']; z = m.z + .02
    return [cone_o('Fut', CHENE, 'Main.G', (0, -.08, z), .014, .012, .3, rot=(math.pi / 2, 0, 0), seg=6),
            profil('Arc', FER2, 'Main.G', [(-.13, 0), (-.07, .025), (0, .035), (.07, .025), (.13, 0), (.07, .012), (0, .02), (-.07, .012)], .012,
                   pos=(0, -.36, z), rot=(math.pi / 2, 0, 0)),
            cone_o('Corde', '#9a9078', 'Main.G', (-.125, -.36, z + .004), .002, .002, .25, rot=(0, math.pi / 2, 0), seg=4),
            cone_o('Carreau', '#4a3a2a', 'Main.G', (0, -.2, z + .016), .004, .004, .2, rot=(math.pi / 2, 0, 0), seg=4)]

def arbaletrier(nom, H=.36):
    bl, br = P.pose_arbalete(); J = P.joints(bl, br)
    hc = J['tete'] + Vector((0, 0, .06))
    pieces = chapel(hc) + tabard(J) + arbalete(J) + P.ceinture(J) + [cone_o('Carquois', CHENE2, 'Hanches', (.1, .05, .52), .03, .03, .18, rot=(.2, .3, 0), seg=8)]
    return P.humain_statue(nom, J, pieces=pieces, H=H, tri=1500, taille=256, peau=CHAIR, habit='#4a4a50', habit2='#3a3436',
                           cuir='#2e2420', gants='#3a2e26', cheveux=None, barbe='#4a3a2e', jupe=.12)

def hallebardier(nom, H=.6):
    bl, br = P.pose_lance(); J = P.joints(bl, br)
    hc = J['tete'] + Vector((0, 0, .06))
    pieces = [boule('Barbute', FER, 'Tete', tuple(hc + Vector((0, .004, .006))), .07, ech=(1, 1.08, 1.12), seg=14),
              plaque('Fente', NUIT, 'Tete', tuple(hc + Vector((0, -.074, .005))), .05, .01, .012),
              plaque('Nasal', FER2, 'Tete', tuple(hc + Vector((0, -.076, -.02))), .012, .008, .05)]
    for s, n in ((1, 'G'), (-1, 'R')):
        e = J['epaule.L' if s > 0 else 'epaule.R']
        pieces.append(boule(f'Spalliere{n}', FER2, f'Bras.{n}', tuple(e + Vector((s * .01, 0, .025))), .056, ech=(1.1, 1, .75), demi=True, rot=(0, s * .4, 0)))
    pieces += tabard(J) + P.ceinture(J) + P.cape(J, BLEU2, .55)
    # hallebarde tenue à deux mains, dressée
    a = J['poignet.R'] + Vector((0, 0, -.25)); u = (J['poignet.L'] - J['poignet.R']).normalized()
    hampe = Vector((u.x * .25, u.y * .25 - .25, 1.0)).normalized()
    rot = Vector((0, 0, 1)).rotation_difference(hampe).to_euler()
    pieces.append(cone_o('Hampe', CHENE2, 'Main.G', tuple(a), .011, .01, 1.15, rot=tuple(rot), seg=6))
    tete = a + hampe * 1.08
    pieces += [profil('Fer', FER2, 'Main.G', [(0, -.07), (.1, -.04), (.12, .03), (.03, .02), (0, .1), (-.01, .02), (-.05, .0)], .008,
                      pos=tuple(tete), rot=(rot.x, rot.y, rot.z + math.pi / 2)),
               cone_o('Pique', FER2, 'Main.G', tuple(tete + hampe * .06), .01, 0, .14, rot=tuple(rot), seg=4)]
    return P.humain_statue(nom, J, pieces=pieces, H=H, tri=1900, taille=512, peau=CHAIR, habit='#45454c', habit2='#383338',
                           cuir='#2a221d', gants='#3a3a40', barbe='#3a2e26', jupe=.16)

def inquisiteur(nom, H=.66):
    """Inquisiteur : chapeau à large bord, long manteau de cuir, col montant, épée droite levée, arbalète de poing."""
    bl = ((.105, .01, .79), (.17, -.06, .66), (.16, -.17, .62), (.16, -.21, .62))
    br = ((-.105, .01, .79), (-.16, -.02, .9), (-.13, -.1, 1.0), (-.12, -.12, 1.05))
    J = P.joints(bl, br); hc = J['tete'] + Vector((0, 0, .06))
    pieces = [cone_o('Calotte', '#1c1a1e', 'Tete', tuple(hc + Vector((0, .005, .035))), .058, .05, .08, seg=14),
              tore('Bord', '#1c1a1e', 'Tete', tuple(hc + Vector((0, .005, .04))), .1, .016, ech=(1, 1, .25), seg=18),
              tore('Ruban', OR, 'Tete', tuple(hc + Vector((0, .005, .05))), .058, .006, seg=14),
              cone_o('Col', '#241e20', 'Cou', tuple(J['cou'] + Vector((0, .01, -.03))), .07, .085, .1, seg=12)]
    pieces += P.ceinture(J, '#1c1612', OR) + P.cape(J, '#2a1e1c', .7, largeur=1.1)
    pieces.append(plaque('Medaillon', OR, 'Torse', tuple(J['poitrine'] + Vector((0, -.095, .02))), .04, .008, .05))
    # épée levée (main droite), arbalète de poing (main gauche)
    m = J['poignet.R']
    pieces += [profil('Lame', '#8a8c94', 'Main.R', [(-.012, 0), (.012, 0), (.009, .45), (0, .5), (-.009, .45)], .006, pos=tuple(m + Vector((0, -.02, .02))), rot=(-.25, 0, 0)),
               plaque('Garde', OR, 'Main.R', tuple(m + Vector((0, -.02, .02))), .09, .016, .014, rot=(-.25, 0, 0)),
               boule('Pommeau', OR, 'Main.R', tuple(m + Vector((0, .0, -.06))), .015)]
    pieces += [cone_o('Fut', CHENE2, 'Main.G', tuple(J['poignet.L'] + Vector((0, .04, .02))), .012, .012, .2, rot=(math.pi / 2, 0, 0), seg=6),
               profil('Arc', FER2, 'Main.G', [(-.08, 0), (0, .02), (.08, 0), (0, .01)], .01, pos=tuple(J['poignet.L'] + Vector((0, -.15, .02))), rot=(math.pi / 2, 0, 0))]
    return P.humain_statue(nom, J, pieces=pieces, H=H, tri=2200, taille=512, peau='#9e7c6a', habit='#2c2224', habit2='#241c1e',
                           cuir='#1e1816', gants='#1e1816', cheveux='#8a8a88', jupe=.3)

# ---------------------------------------------------------------- les 10 tours
def arbaletriers(nom):
    """0 · Tour carrée de calcaire, ardoise, deux arbalétriers au chemin de ronde."""
    c, r, z = debut(nom)
    boite('Fut', CALC, .36, .36, .46, (0, 0, z + .23), .01, r)
    boite('Talus', CALC2, .42, .42, .08, (0, 0, z + .04), .01, r)
    fenetre('Porte', r, .12, .2, (0, -.181, z + .02))
    fenetre('Archere', r, .035, .1, (0, -.181, z + .28))
    for k in range(4): boite(f'Chaine{k}', CALC2, .03, .03, .46, ((k % 2 * 2 - 1) * .18, (k // 2 * 2 - 1) * .18, z + .23), .004, r)
    zt = z + .46
    boite('Hourd', CHENE2, .44, .44, .05, (0, 0, zt + .025), .006, r)
    creneaux('Merlon', r, .42, zt + .05)
    etendard('Oriflamme', r, (.2, -.225, zt), .26)
    t = pivot('Tourelle', (0, 0, zt + .05), r)
    a1 = arbaletrier(nom + '_arb'); HD.poser(a1, t, (.09, -.03, 0))
    a2 = HD.copier_statue(a1, c); HD.poser(a2, t, (-.09, -.03, 0), (0, 0, .1))
    return finir(r)

def hallebardiers(nom):
    """1 · Poste de garde : palissade de pieux, auvent d'ardoise, hallebardier en barbute et cape."""
    c, r, z = debut(nom)
    for k in range(9):
        a = math.pi * (.15 + k * .0875) * 2
        x, y = math.sin(a) * .3, math.cos(a) * .3
        if y < -.12: continue
        cylindre(f'Pieu{k}', CHENE, .026, .024, .3 + (k % 3) * .04, 6, (x, y, z), r)
        cone(f'Pointe{k}', CHENE2, .026, .06, 6, (x, y, z + .3 + (k % 3) * .04), r)
    for s in (-1, 1): cylindre(f'Poteau{s}', CHENE2, .02, .02, .52, 6, (s * .2, .2, z), r)
    prisme('Auvent', ARDOISE, [(-.26, 0), (.26, 0), (.24, .02), (-.24, .02)], .24, (0, .2, z + .52), r, (.35, 0, 0))
    boite('Rateau', CHENE2, .3, .03, .03, (0, .22, z + .3), .003, r)
    for k in range(3): cylindre(f'Lance{k}', CHENE, .007, .007, .5, 5, ((k - 1) * .08, .24, z + .05), r, rot=(-.15, 0, 0))
    t = pivot('Tourelle', (0, -.06, z), r)
    HD.poser(hallebardier(nom + '_halle'), t)
    return finir(r)

def lance_filets(nom):
    """2 · Lance-filets : affût de chêne sur roues ferrées, tube à ressort de fer, filets lestés enroulés."""
    c, r, z = debut(nom)
    for sx in (-1, 1):
        for sy in (-1, 1):
            cylindre(f'Roue{sx}{sy}', CHENE2, .07, .07, .025, 10, (sx * .2, sy * .14, z + .07), r, rot=(0, math.pi / 2, 0))
            anneau(f'Bandage{sx}{sy}', FER, .07, .008, 10, 3, (sx * .2 + sx * .013, sy * .14, z + .07), r, (0, math.pi / 2, 0), metal=.5)
    boite('Chassis', CHENE, .36, .34, .06, (0, 0, z + .12), .006, r)
    t = pivot('Tourelle', (0, 0, z + .18), r)
    boite('Socle', CHENE2, .16, .16, .1, (0, 0, .05), .006, t)
    cylindre('Tube', FER, .055, .06, .36, 10, (0, .08, .14), t, rot=(math.pi / 2 + .45, 0, 0), metal=.6, rough=.45)
    for k in range(3): anneau(f'Frette{k}', OR, .064, .009, 10, 3, (0, .08 - k * .11, .14 + k * .05), t, (math.pi / 2 + .45, 0, 0), metal=.5)
    for k in range(4):
        a = k * math.pi / 2
        sphere(f'Lest{k}', FER2, .02, (math.cos(a) * .04, -.25 + math.sin(a) * .0, .3 + math.sin(a) * .04), (1, 1, 1), 6, 4, t, metal=.5)
    for k in range(2):
        sphere(f'Filet{k}', '#7a6a4e', .07, (.13 * (k * 2 - 1), .15, -.01), (1, 1, .55), 9, 5, t)
        anneau(f'Maille{k}', '#5a4c38', .06, .006, 10, 3, (.13 * (k * 2 - 1), .15, .02), t)
    return finir(r)

def trebuchet(nom):
    """3 · Trébuchet : deux chevalets de chêne, verge, huche de contrepoids cerclée de fer, fronde chargée d'un boulet."""
    c, r, z = debut(nom)
    t = pivot('Tourelle', (0, 0, z), r)
    boite('Longrine', CHENE2, .5, .3, .05, (0, 0, .025), .006, t)
    for s in (-1, 1):
        for q in (-1, 1):
            boite(f'Montant{s}{q}', CHENE, .04, .04, .5, (s * .1, q * .1, .24), .004, t, (q * .35, 0, 0))
        boite(f'Moise{s}', CHENE2, .04, .3, .04, (s * .1, 0, .1), .004, t)
    cylindre('Axe', FER, .016, .016, .26, 6, (-.13, 0, .46), t, rot=(0, math.pi / 2, 0), metal=.6)
    boite('Verge', CHENE, .045, .7, .045, (0, -.12, .6), .004, t, (-.55, 0, 0))
    boite('Huche', CHENE2, .16, .14, .16, (0, .2, .32), .006, t)
    for k in range(2): boite(f'Cercle{k}', FER, .17, .15, .015, (0, .2, .27 + k * .1), .002, t, metal=.5)
    cylindre('Corde', '#8a7a5a', .004, .004, .3, 4, (0, -.42, .88), t, rot=(2.6, 0, 0))
    sphere('Boulet', CALC2, .045, (0, -.36, .62), (1, 1, 1), 8, 6, t)
    sphere('Tas', CALC2, .04, (.2, .12, .04), (1, 1, 1), 7, 5, r)
    sphere('Tas2', CALC, .035, (.25, .07, .035), (1, 1, 1), 7, 5, r)
    return finir(r)

def baliste(nom):
    """4 · Baliste céleste : bastion rond, baliste lourde ornée d'un aigle d'or, carreau de fer prêt à percer les volants."""
    c, r, z = debut(nom)
    cylindre('Bastion', CALC, .27, .29, .26, 12, (0, 0, z), r)
    cylindre('Cordon', CALC2, .3, .3, .03, 12, (0, 0, z + .26), r)
    for k in range(8):
        a = k * math.pi / 4 + .2
        boite(f'Merlon{k}', CALC, .07, .05, .07, (math.cos(a) * .27, math.sin(a) * .27, z + .32), .004, r, (0, 0, a + math.pi / 2))
    t = pivot('Tourelle', (0, 0, z + .29), r)
    boite('Affut', CHENE2, .12, .3, .08, (0, .02, .1), .006, t, (.25, 0, 0))
    boite('Glissiere', CHENE, .05, .5, .04, (0, -.06, .18), .004, t, (.25, 0, 0))
    for s in (-1, 1):
        boite(f'Bras{s}', CHENE, .26, .035, .03, (s * .13, -.22, .24), .004, t, (.25, 0, s * .32))
        cylindre(f'Ecrou{s}', FER, .035, .035, .08, 8, (s * .06, -.2, .19), t, metal=.6)
    cylindre('CordeB', '#9a9078', .003, .003, .5, 4, (-.25, -.15, .24), t, rot=(0, math.pi / 2, .0))
    cylindre('CarreauB', FER2, .01, .01, .44, 6, (0, .14, .23), t, rot=(math.pi / 2 + .25, 0, 0), metal=.6)
    cone('PointeB', FER, .022, .07, 4, (0, -.3, .13), t, (-math.pi / 2 + .25, 0, 0), metal=.6)
    prisme('Aigle', OR, [(-.12, 0), (-.05, .03), (0, .09), (.05, .03), (.12, 0), (.06, -.02), (0, .02), (-.06, -.02)], .012, (0, -.21, .17), t, (.25, 0, 0), metal=.6)
    return finir(r)

def chapelle(nom):
    """5 · Chapelle du guet : nef de calcaire, toit d'ardoise, clocher ajouré, sceau du Jugement doré qui flotte."""
    c, r, z = debut(nom)
    boite('Nef', CALC, .3, .44, .3, (0, .05, z + .15), .008, r)
    prisme('Toit', ARDOISE, [(-.19, 0), (.19, 0), (0, .2)], .48, (0, .29, z + .3), r)
    prisme('Pignon', CALC, [(-.15, 0), (.15, 0), (0, .17)], .02, (0, -.17, z + .3), r)
    fenetre('Portail', r, .1, .18, (0, -.171, z))
    fenetre('Rosace', r, .07, .08, (0, -.181, z + .33), col='#d8b860')
    for k in range(2): fenetre(f'Vitrail{k}', r, .04, .12, (.151, -.05 + k * .2, z + .1), (0, 0, math.pi / 2), col='#c9a24a')
    boite('Clocher', CALC2, .14, .14, .3, (0, .2, z + .5 + .15), .006, r)
    for s in range(4):
        a = s * math.pi / 2
        fenetre(f'Abat{s}', r, .05, .1, (math.cos(a) * .071, .2 + math.sin(a) * .071, z + .7), (0, 0, a + math.pi / 2))
    cone('Fleche', ARDOISE, .11, .26, 4, (0, .2, z + .8), r, (0, 0, math.pi / 4))
    cylindre('Cloche', OR, .03, .04, .05, 8, (0, .2, z + .68), r, metal=.6)
    ob = pivot('Orbe', (0, 0, 0), pivot('Tourelle', (0, -.27, z + .45), r))
    anneau('Sceau', LUMIERE, .07, .008, 18, 3, (0, 0, 0), ob, (math.pi / 2, 0, 0), emis=2.2)
    boite('SceauV', LUMIERE, .012, .006, .1, (0, 0, 0), 0, ob, emis=2.2)
    boite('SceauH', LUMIERE, .07, .006, .012, (0, 0, .015), 0, ob, emis=2.2)
    return finir(r)

def comptoir(nom):
    """6 · Comptoir marchand : échoppe à colombages, auvent rayé, coffres cerclés, sacs d'or, balance de changeur."""
    c, r, z = debut(nom)
    boite('Echoppe', '#b8ad94', .44, .24, .32, (0, .14, z + .16), .006, r)
    for k in range(4): boite(f'Colombe{k}', CHENE2, .025, .01, .32, (-.18 + k * .12, .018, z + .16), 0, r)
    boite('Sabliere', CHENE2, .46, .02, .03, (0, .015, z + .32), 0, r)
    prisme('Toit', ARDOISE, [(-.25, 0), (.25, 0), (0, .16)], .3, (0, .27, z + .32), r)
    for k in range(5):
        boite(f'Bande{k}', BLEU if k % 2 else '#b8a888', .1, .2, .008, (-.2 + k * .1, -.08, z + .34), 0, r, (.45, 0, 0))
    boite('Etal', CHENE, .44, .14, .04, (0, -.04, z + .16), .004, r)
    for s in (-1, 1): boite(f'PiedEtal{s}', CHENE2, .03, .03, .16, (s * .2, -.09, z + .08), 0, r)
    boite('Coffre', CHENE2, .16, .1, .08, (-.2, -.24, z + .04), .006, r)
    cylindre('Couvercle', CHENE2, .05, .05, .16, 8, (-.28, -.24, z + .08), r, rot=(0, math.pi / 2, 0))
    for k in range(2): boite(f'Ferrure{k}', FER, .01, .105, .1, (-.25 + k * .1, -.24, z + .06), 0, r, metal=.5)
    for k, (x, y) in enumerate(((.14, -.25), (.22, -.2), (.2, -.3))):
        sphere(f'Sac{k}', '#8a7454', .045, (x, y, z + .04), (1, 1, 1.1), 8, 5, r)
        cone(f'Lien{k}', '#5a4a34', .02, .03, 6, (x, y, z + .085), r)
    for k in range(5): cylindre(f'Pile{k}', OR, .02, .02, .008, 8, (-.05 + (k % 3) * .04, -.04, z + .18 + (k // 3) * .01), r, metal=.7)
    ob = pivot('Orbe', (.12, -.05, z + .28), r)
    cylindre('Fleau', OR, .004, .004, .16, 4, (-.08, 0, 0), ob, rot=(0, math.pi / 2, 0), metal=.7)
    for s in (-1, 1): cylindre(f'Plateau{s}', OR, .03, .025, .008, 10, (s * .075, 0, -.06), ob, metal=.7)
    cylindre('Colonne', FER, .006, .006, .1, 4, (.12, -.05, z + .18), r)
    return finir(r)

def etendard_royal(nom):
    """7 · Étendard royal : mât de chêne cerclé d'or, grande bannière au lion, deux braseros allumés."""
    c, r, z = debut(nom)
    cylindre('Socle', CALC2, .16, .18, .08, 8, (0, 0, z), r)
    cylindre('Mat', CHENE2, .02, .016, 1.0, 8, (0, 0, z + .08), r)
    for k in range(3): anneau(f'Bague{k}', OR, .022, .006, 8, 3, (0, 0, z + .2 + k * .3), r, metal=.6)
    boite('Traverse', CHENE2, .34, .025, .025, (.15, 0, z + .98), .003, r)
    cone('Fleuron', OR, .03, .08, 6, (0, 0, z + 1.08), r, metal=.6)
    pts = [(0, 0), (.32, 0), (.32, -.42), (.24, -.36), (.16, -.46), (.08, -.36), (0, -.42)]
    prisme('Banniere', BLEU, pts, .008, (-.01, -.012, z + .97), r)
    prisme('Bordure', OR, [(0, 0), (.32, 0), (.32, -.025), (0, -.025)], .01, (-.01, -.012, z + .97), r)
    prisme('Couronne', OR, [(.07, -.26), (.25, -.26), (.25, -.14), (.21, -.19), (.185, -.12), (.16, -.19), (.135, -.12), (.11, -.19), (.07, -.14)], .011, (-.01, -.012, z + .97), r)
    for s in (-1, 1):
        x = s * .25
        cylindre(f'Trepied{s}', FER, .012, .02, .22, 5, (x, -.18, z), r, metal=.5)
        cylindre(f'Brasero{s}', FER, .06, .04, .06, 8, (x, -.18, z + .22), r, metal=.5)
        f = pivot('Flamme', (x, -.18, z + .28), r)
        cone(f'Feu{s}', '#ffb050', .045, .12, 6, (0, 0, 0), f, emis=3)
    return finir(r)

def inquisition(nom):
    """8 · Inquisiteur debout sur un échafaud de pierre, entre deux bûchers éteints aux chaînes pendantes."""
    c, r, z = debut(nom)
    boite('Echafaud', CALC2, .42, .36, .1, (0, .02, z + .05), .006, r)
    for k in range(3): boite(f'Marche{k}', CALC, .2, .05, .033 * (k + 1), (0, -.18 - (2 - k) * .0, z + .0165 * (k + 1)), .003, r)
    for s in (-1, 1):
        cylindre(f'Bucher{s}', CHENE2, .018, .016, .5, 6, (s * .27, .16, z), r)
        for k in range(5): cylindre(f'Fagot{s}{k}', CHENE, .012, .012, .14, 5, (s * .27 + (k - 2) * .02, .16, z + .02), r, rot=(0, math.pi / 2, k * .6))
        anneau(f'Carcan{s}', FER, .03, .006, 8, 3, (s * .27, .14, z + .38), r, (math.pi / 2, 0, 0), metal=.5)
    t = pivot('Tourelle', (0, .03, z + .1), r)
    HD.poser(inquisiteur(nom + '_inq'), t)
    return finir(r)

def rayon_aube(nom):
    """9 · Rayon de l'Aube (ultime) : haute tour blanche à contreforts dorés, lentille de cristal qui tourne dans un
    soleil de fer doré."""
    c, r, z = debut(nom)
    cylindre('Fut', '#a9a294', .2, .16, .62, 8, (0, 0, z), r)
    for k in range(8):
        a = k * math.pi / 4
        prisme(f'Contrefort{k}', CALC2, [(0, 0), (.08, 0), (.02, .45), (0, .45)], .04, (math.cos(a) * .18, math.sin(a) * .18, z), r, (0, 0, a - math.pi / 2))
        boite(f'Filet{k}', OR, .012, .012, .45, (math.cos(a) * .2, math.sin(a) * .2, z + .2), 0, r, metal=.6)
    fenetre('Porte', r, .1, .16, (0, -.18, z))
    cylindre('Couronne', CALC, .22, .22, .05, 8, (0, 0, z + .62), r)
    for k in range(8):
        a = k * math.pi / 4 + math.pi / 8
        cone(f'Pinacle{k}', OR, .025, .09, 4, (math.cos(a) * .2, math.sin(a) * .2, z + .67), r, metal=.6)
    tr = pivot('Tourelle', (0, 0, z + .86), r)
    an = pivot('Anneaux', (0, 0, 0), tr)
    anneau('Soleil', OR, .18, .012, 24, 4, (0, 0, 0), an, (math.pi / 2, 0, 0), metal=.7)
    for k in range(12):
        a = k * math.pi / 6
        cone(f'Rai{k}', OR, .014, .07 + (k % 2) * .04, 4, (math.cos(a) * .19, 0, math.sin(a) * .19), an, (0, math.pi / 2 - a, 0), metal=.7)
    cr = pivot('Cristal', (0, 0, 0), tr)
    sphere('Lentille', '#fff1c4', .1, (0, 0, 0), (1, .35, 1), 14, 8, cr, emis=1.6)
    sphere('Coeur', '#ffffff', .04, (0, 0, 0), (1, 1, 1), 8, 5, cr, emis=3)
    return finir(r)

def tour(j):
    return [arbaletriers, hallebardiers, lance_filets, trebuchet, baliste, chapelle, comptoir, etendard_royal, inquisition, rayon_aube][j](f'aubeval_{j}')
