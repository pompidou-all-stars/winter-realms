"""Nains de Hautroc (2.40, direction « grimdark ») : forteresse de montagne. Granit taillé en blocs, plaques de fer
noirci rivetées, cuivre et laiton ternis, runes de forge orangées, fumée et braises.

Nains (arbalétrier, forgeron) au procédé des monstres organiques (communs/peuples_hd.py) ; machines et bastions en
pièces peintes avec l'occlusion cuite."""
import math
from mathutils import Vector
from . import tours_hd as HD, peuples_hd as P
from .outils import pivot, cylindre, boite, sphere, cone, prisme, anneau, collection, dans
from .organique import boule, corne, profil, plaque, tore
from .organique import cone as cone_o
from .neige import enneiger

GRANIT, GRANIT2, NUIT = '#77706a', '#58524d', '#1b1a1c'
FER, FER2, CUIVRE, LAITON = '#323134', '#4d4b50', '#8a5634', '#9a7c3e'
RUNE, BRAISE, CHENE = '#ff8a2a', '#ffb050', '#4a3526'
NAIN, BARBE, BARBE2 = '#b08068', '#8a4a2a', '#c8c0b0'
SOL = .12

# ---------------------------------------------------------------- socle
def socle(r, cote=.8):
    """Dalle de granit en blocs, cornières de fer rivetées, bornes octogonales à chapeau de cuivre."""
    d = cote / 2
    boite('Assise', NUIT, cote, cote, .05, (0, 0, .025), .01, r)
    dal = pivot('Dallage', (0, 0, 0), r)
    boite('Dalle', GRANIT2, cote * .92, cote * .92, .05, (0, 0, .07), .006, dal)
    for i in range(3):
        for j in range(3):
            boite(f'Bloc{i}{j}', GRANIT, cote * .28, cote * .28, .014, ((i - 1) * cote * .3, (j - 1) * cote * .3, .1), .006, dal)
    for k, (x, y, sx, sy) in enumerate(((-.3, .33, .16, .05), (.28, .34, .1, .04), (.34, -.1, .04, .12), (-.33, -.2, .05, .1))):
        sphere(f'Congere{k}', '#e6edf5', 1, (x * cote / .8, y * cote / .8, .1), (sx, sy, .022), 8, 4, dal, rough=.9)
    for s in range(4):
        a = s * math.pi / 2
        boite(f'Corniere{s}', FER, cote * .9, .02, .03, (math.cos(a) * d * .93, math.sin(a) * d * .93, .095), .003, r, (0, 0, a + math.pi / 2), metal=.5)
    for sx in (-1, 1):
        for sy in (-1, 1):
            x, y = sx * d * .87, sy * d * .87
            cylindre(f'Borne{sx}{sy}', GRANIT2, .05, .05, .12, 8, (x, y, .05), r)
            cone(f'Chapeau{sx}{sy}', CUIVRE, .055, .04, 8, (x, y, .17), r, metal=.5)
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

def rivets(nom, parent, pts, r=.008):
    for k, p in enumerate(pts): sphere(f'{nom}{k}', LAITON, r, p, (1, 1, .6), 5, 3, parent, metal=.6)

def bastion(nom, r, z, rayon=.24, h=.24, faces=8):
    """Bastion octogonal de granit, ceinture de fer rivetée, rune de forge sur la face avant."""
    cylindre(nom, GRANIT, rayon, rayon * .94, h, faces, (0, 0, z), r, rot=(0, 0, math.pi / faces))
    cylindre(nom + 'Ceinture', FER, rayon * 1.02, rayon * 1.02, .035, faces, (0, 0, z + h * .55), r, rot=(0, 0, math.pi / faces), metal=.5)
    rivets(nom + 'Rivet', r, [(math.cos(k * 2 * math.pi / faces) * rayon * 1.03, math.sin(k * 2 * math.pi / faces) * rayon * 1.03, z + h * .55 + .017) for k in range(faces)])
    boite(nom + 'Rune', RUNE, .05, .006, .035, (0, -rayon * .94 - .003, z + h * .28), 0, r, emis=1.4)
    return z + h

# ---------------------------------------------------------------- nains (hauteur 1, gabarit « nain »)
def casque_nain(J):
    hc = J['tete'] + Vector((0, 0, .075))
    return [boule('Casque', FER2, 'Tete', tuple(hc + Vector((0, .005, .02))), .08, demi=True, seg=14),
            tore('Bordure', LAITON, 'Tete', tuple(hc + Vector((0, .005, .025))), .081, .01, seg=16),
            plaque('Nasal', FER, 'Tete', tuple(hc + Vector((0, -.083, -.005))), .014, .01, .06)]

def arbaletrier_nain(nom, H=.32):
    bl, br = P.pose_arbalete('nain'); J = P.joints(bl, br, 'nain')
    m = J['poignet.L']; z = m.z + .02
    p = casque_nain(J) + P.ceinture(J, '#2a1e16', LAITON, 'nain')
    p += [cone_o('Fut', CHENE, 'Main.G', (0, -.06, z), .02, .018, .32, rot=(math.pi / 2, 0, 0), seg=6),
          plaque('Chargeur', FER2, 'Main.G', (0, -.2, z + .05), .04, .14, .05),
          profil('Arc', FER2, 'Main.G', [(-.14, 0), (-.07, .03), (0, .04), (.07, .03), (.14, 0), (.07, .015), (0, .025), (-.07, .015)], .014,
                 pos=(0, -.36, z), rot=(math.pi / 2, 0, 0)),
          cone_o('Manivelle', LAITON, 'Main.G', (.04, -.14, z + .02), .006, .006, .07, rot=(0, math.pi / 2, 0), seg=4)]
    return P.humain_statue(nom, J, g='nain', pieces=p, H=H, tri=1600, taille=256, peau=NAIN, habit='#4a3a34', habit2='#3a2e2a',
                           cuir='#2a201a', gants='#3a2e26', barbe=BARBE, jupe=.1, relief=P.RELIEF_PEAU)

def forgeron(nom, H=.55):
    bl = ((.15, .01, .72), (.2, -.08, .6), (.12, -.16, .55), (.1, -.19, .55))
    br = ((-.15, .01, .72), (-.22, .05, .84), (-.2, -.02, .98), (-.19, -.04, 1.03))
    J = P.joints(bl, br, 'nain')
    p = [boule('Tablier', '#3a2a20', 'Torse', tuple(J['ventre'] + Vector((0, -.07, -.06))), .14, ech=(1, .35, 1.6), seg=12)]
    p += P.ceinture(J, '#2a1e16', LAITON, 'nain')
    m = J['poignet.R']
    p += [cone_o('Manche', CHENE, 'Main.R', tuple(m + Vector((0, .02, -.06))), .012, .012, .3, rot=(-.5, 0, 0), seg=6),
          plaque('Masse', FER, 'Main.R', tuple(m + Vector((0, .16, .2))), .1, .07, .07, rot=(-.5, 0, 0)),
          plaque('Pince', FER2, 'Main.G', tuple(J['poignet.L'] + Vector((0, -.08, 0))), .02, .14, .02)]
    return P.humain_statue(nom, J, g='nain', pieces=p, H=H, tri=2000, taille=512, peau=NAIN, habit=NAIN, habit2='#3a2e2a',
                           cuir='#2a201a', gants='#2a201a', barbe=BARBE2, cheveux=BARBE2, jupe=.12, bas='#3a2e2a', relief=P.RELIEF_PEAU)

# ---------------------------------------------------------------- les 10 tours
def arbalete(nom):
    """0 · Bastion octogonal, nain servant d'une arbalète à répétition à chargeur, sur pivot de laiton."""
    c, r, z = debut(nom)
    zt = bastion('Bastion', r, z, .24, .3)
    for k in range(8):
        a = k * math.pi / 4
        boite(f'Merlon{k}', GRANIT2, .07, .06, .07, (math.cos(a) * .22, math.sin(a) * .22, zt + .035), .006, r, (0, 0, a + math.pi / 2))
    cylindre('Pivot', LAITON, .06, .07, .03, 10, (0, 0, zt), r, metal=.6)
    t = pivot('Tourelle', (0, 0, zt + .03), r)
    HD.poser(arbaletrier_nain(nom + '_nain'), t, (0, .02, 0))
    return finir(r)

def marteau_pilon(nom):
    """1 · Marteau-pilon : bâti d'acier riveté, chaudière de cuivre, énorme masse levée sur sa tige, enclume de choc."""
    c, r, z = debut(nom)
    boite('Enclume', FER, .26, .2, .08, (0, 0, z + .04), .01, r, metal=.5)
    for s in (-1, 1):
        boite(f'Montant{s}', FER2, .05, .08, .62, (s * .17, .04, z + .31), .006, r, metal=.5)
        rivets(f'RivetM{s}', r, [(s * .17, -.003, z + .1 + k * .12) for k in range(5)])
    boite('Sommier', FER2, .42, .1, .07, (0, .04, z + .63), .008, r, metal=.5)
    cylindre('Chaudiere', CUIVRE, .09, .09, .26, 12, (0, .25, z), r, metal=.5)
    cone('DomeC', CUIVRE, .09, .06, 12, (0, .25, z + .26), r, metal=.5)
    cylindre('Cheminee', FER, .025, .03, .25, 8, (0, .25, z + .3), r)
    t = pivot('Tourelle', (0, 0, z), r)
    cylindre('Tige', '#8a8a90', .018, .018, .3, 8, (0, 0, .3), t, metal=.7)
    boite('Masse', FER, .18, .16, .14, (0, 0, .24), .012, t, metal=.6)
    boite('RuneM', RUNE, .06, .006, .03, (0, -.083, .26), 0, t, emis=1.5)
    return finir(r)

def baliste_plaque(nom):
    """2 · Baliste perce-plaque : affût d'acier sur bastion, arc de lames d'acier, carreau à pointe de diamant runique."""
    c, r, z = debut(nom)
    zt = bastion('Bastion', r, z, .22, .2)
    t = pivot('Tourelle', (0, 0, zt), r)
    boite('Affut', FER2, .14, .3, .08, (0, .04, .06), .008, t, (.15, 0, 0), metal=.5)
    boite('Rail', FER, .05, .5, .04, (0, -.06, .13), .004, t, (.15, 0, 0), metal=.5)
    for s in (-1, 1):
        prisme(f'Lame{s}', '#7a7a82', [(0, 0), (.24, .05), (.26, .03), (0, -.02)], .02, (s * .02, -.24, .17), t, (math.pi / 2 + .15, 0, 0 if s > 0 else math.pi), metal=.7)
        cylindre(f'Treuil{s}', LAITON, .04, .04, .05, 10, (s * .1, .16, .1), t, rot=(0, math.pi / 2, 0), metal=.6)
    cylindre('Carreau', FER, .012, .012, .46, 6, (0, .16, .17), t, rot=(math.pi / 2 + .15, 0, 0), metal=.6)
    cone('Diamant', RUNE, .028, .08, 4, (0, -.3, .12), t, (-math.pi / 2 + .15, 0, 0), emis=1.4)
    return finir(r)

def mortier(nom):
    """3 · Mortier runique : gros fût de bronze cerclé, gravé de runes, tourné vers le ciel sur un berceau d'acier."""
    c, r, z = debut(nom)
    cylindre('Plateau', GRANIT2, .27, .28, .06, 10, (0, 0, z), r)
    t = pivot('Tourelle', (0, 0, z + .06), r)
    for s in (-1, 1): boite(f'Flasque{s}', FER2, .04, .22, .18, (s * .14, 0, .09), .008, t, metal=.5)
    cylindre('Tourillon', FER, .03, .03, .34, 8, (-.17, 0, .14), t, rot=(0, math.pi / 2, 0), metal=.5)
    cylindre('Fut', '#7a5a34', .1, .12, .3, 12, (0, .06, .06), t, rot=(-.55, 0, 0), metal=.6)
    for k in range(3): anneau(f'Frette{k}', FER, .115 - k * .006, .014, 12, 3, (0, .06 - k * .08, .07 + k * .12), t, (-.55, 0, 0), metal=.5)
    cylindre('Bouche', NUIT, .085, .085, .01, 12, (0, -.1, .32), t, rot=(-.55, 0, 0))
    for k in range(4):
        a = k * math.pi / 2 + .4
        boite(f'Rune{k}', RUNE, .03, .006, .03, (math.cos(a) * .115, .02 + math.sin(a) * .07, .17 + math.sin(a) * .04), 0, t, (0, 0, a + math.pi / 2), emis=1.4)
    for k in range(3): sphere(f'Obus{k}', FER, .04, (.2 - k * .05, .22, z + .04), (1, 1, 1.3), 8, 5, r, metal=.5)
    return finir(r)

def canon_aa(nom):
    """4 · Canon antiaérien à éclats : quatre tubes courts sur tourelle pivotante, pare-éclats riveté, caisses d'obus."""
    c, r, z = debut(nom)
    zt = bastion('Bastion', r, z, .2, .16)
    t = pivot('Tourelle', (0, 0, zt), r)
    cylindre('Couronne', FER2, .17, .17, .05, 12, (0, 0, 0), t, metal=.5)
    prisme('Masque', FER, [(-.16, 0), (.16, 0), (.13, .16), (-.13, .16)], .03, (0, -.1, .05), t, metal=.5)
    rivets('RivetMq', t, [(x, -.118, .1) for x in (-.11, -.05, .05, .11)])
    for i in range(2):
        for j in range(2):
            cylindre(f'Tube{i}{j}', FER2, .028, .03, .34, 8, ((i - .5) * .08, .05, .12 + j * .07), t, rot=(-.6 - math.pi / 2 + math.pi, 0, 0), metal=.6)
    for k in range(2):
        boite(f'Caisse{k}', CHENE, .12, .09, .08, (.22 - k * .02, .22 - k * .1, z + .04 + k * .0), .006, r)
        boite(f'Marque{k}', RUNE, .03, .005, .03, (.22 - k * .02, .175 - k * .1, z + .05), 0, r, emis=1)
    return finir(r)

def phare(nom):
    """5 · Phare runique : tour de granit à assises, lanterne d'acier ajourée, prisme runique qui tourne."""
    c, r, z = debut(nom)
    for k in range(4):
        cylindre(f'Assise{k}', GRANIT if k % 2 else GRANIT2, .17 - k * .02, .155 - k * .02, .16, 8, (0, 0, z + k * .16), r, rot=(0, 0, math.pi / 8))
    cylindre('Balcon', FER, .17, .17, .03, 8, (0, 0, z + .64), r, rot=(0, 0, math.pi / 8), metal=.5)
    for k in range(8):
        a = k * math.pi / 4
        cylindre(f'Montant{k}', FER2, .008, .008, .16, 4, (math.cos(a) * .1, math.sin(a) * .1, z + .67), r, metal=.5)
    cone('Toit', CUIVRE, .14, .12, 8, (0, 0, z + .83), r, rot=(0, 0, math.pi / 8), metal=.5)
    tr = pivot('Tourelle', (0, 0, z + .75), r)
    cr = pivot('Cristal', (0, 0, 0), tr)
    cylindre('Prisme', RUNE, .06, .06, .1, 4, (0, 0, -.05), cr, emis=2)
    boite('Faisceau', '#ffd8a0', .04, .3, .02, (0, -.2, 0), 0, tr, emis=1.2)
    boite('Porte', NUIT, .08, .02, .12, (0, -.17, z + .06), 0, r)
    return finir(r)

def gueule_forge(nom):
    """6 · Gueule de forge : fourneau de granit en tête de bélier, gueule rougeoyante, soufflets de cuir, tuyau de cuivre."""
    c, r, z = debut(nom)
    boite('Fourneau', GRANIT2, .34, .3, .3, (0, .06, z + .15), .02, r)
    t = pivot('Tourelle', (0, -.05, z + .2), r)
    sphere('Tete', GRANIT, .14, (0, 0, 0), (1, 1.1, .85), 10, 6, t)
    for s in (-1, 1):
        cylindre(f'Corne{s}', FER2, .04, .01, .2, 6, (s * .1, .04, .06), t, rot=(.4, s * 1.6, 0), metal=.5)
        sphere(f'Oeil{s}', RUNE, .018, (s * .06, -.12, .04), (1, .6, .8), 6, 3, t, emis=2)
    sn = pivot('SansNeige', (0, 0, 0), t)
    sphere('Gueule', '#ff6a1a', .07, (0, -.13, -.04), (1, .5, .7), 8, 4, sn, emis=2.5)
    for k in range(4): cone(f'Croc{k}', FER, .012, .04, 4, ((k - 1.5) * .03, -.15, .0), t, (math.pi, 0, 0), metal=.5)
    f = pivot('Flamme', (0, -.2, -.04), t)
    cone('Feu', BRAISE, .05, .12, 6, (0, 0, 0), f, (math.pi / 2, 0, 0), emis=3)
    for s in (-1, 1):
        sphere(f'Soufflet{s}', '#4a3424', .08, (s * .2, .18, z + .1), (.5, 1, .8), 8, 5, r)
    cylindre('Tuyau', CUIVRE, .025, .025, .3, 8, (0, .22, z + .3), r, rot=(.0, 0, 0), metal=.5)
    return finir(r)

def enclume(nom):
    """7 · Enclume runique : forgeron nain qui lève sa masse au-dessus d'une enclume gravée, foyer de braises."""
    c, r, z = debut(nom)
    boite('Billot', CHENE, .14, .14, .1, (.06, -.08, z + .05), .01, r)
    boite('Corps', FER, .16, .08, .06, (.06, -.08, z + .13), .008, r, metal=.6)
    cone('Bigorne', FER, .035, .1, 6, (.14, -.08, z + .14), r, (0, math.pi / 2, 0), metal=.6)
    boite('RuneE', RUNE, .06, .005, .03, (.06, -.123, z + .13), 0, r, emis=1.6)
    cylindre('Foyer', GRANIT2, .1, .11, .08, 8, (-.18, .15, z), r)
    sn = pivot('SansNeige', (0, 0, 0), r)
    sphere('Braises', '#ff7a2a', .08, (-.18, .15, z + .08), (1, 1, .3), 8, 4, sn, emis=2)
    t = pivot('Tourelle', (-.08, .06, z), r)
    HD.poser(forgeron(nom + '_forgeron'), t, (0, 0, 0), (0, 0, -.5))
    return finir(r)

def mines(nom):
    """8 · Champ de mines : caisses de poudre, fourneau de charge, mines runiques en couronne prêtes à être posées."""
    c, r, z = debut(nom)
    for k, (x, y, s) in enumerate(((-.14, .14, .16), (.06, .18, .13), (-.05, .02, .11))):
        boite(f'Caisse{k}', CHENE, s, s * .8, s * .7, (x, y, z + s * .35), .006, r, (0, 0, k * .3))
        boite(f'Cerclage{k}', FER, s * 1.02, s * .82, .012, (x, y, z + s * .35), 0, r, (0, 0, k * .3), metal=.5)
    for k in range(5):
        a = k * 2 * math.pi / 5 + .3
        x, y = math.cos(a) * .25, math.sin(a) * .22 - .05
        cylindre(f'Mine{k}', FER2, .045, .05, .03, 10, (x, y, z), r, metal=.5)
        sphere(f'Detonateur{k}', RUNE, .012, (x, y, z + .035), (1, 1, .6), 6, 3, r, emis=1.6)
    t = pivot('Tourelle', (.15, -.05, z), r)
    cylindre('Baril', CHENE, .05, .05, .14, 10, (0, 0, 0), t)
    return finir(r)

def grondeterre(nom):
    """9 · Grondeterre (ultime) : canon de siège long, gueule en tête de dragon, affût à roues ferrées, runes qui brûlent."""
    c, r, z = debut(nom)
    t = pivot('Tourelle', (0, .03, z), r)
    for s in (-1, 1):
        boite(f'Flasque{s}', CHENE, .04, .46, .12, (s * .12, .05, .1), .008, t)
        cylindre(f'Roue{s}', CHENE, .11, .11, .035, 12, (s * .155, .1, .11), t, rot=(0, math.pi / 2, 0))
        anneau(f'Bandage{s}', FER, .11, .012, 12, 3, (s * .175, .1, .11), t, (0, math.pi / 2, 0), metal=.5)
    cylindre('Fut', FER2, .09, .065, .72, 12, (0, .3, .2), t, rot=(math.pi / 2 + .12, 0, 0), metal=.6)
    for k in range(4): anneau(f'Frette{k}', LAITON, .09 - k * .007, .014, 12, 3, (0, .2 - k * .15, .21 + k * .018), t, (math.pi / 2 + .12, 0, 0), metal=.6)
    for k in range(4): boite(f'Rune{k}', RUNE, .03, .006, .03, (0, .15 - k * .14, .29 + k * .016), 0, t, (.12, 0, 0), emis=1.6)
    sphere('Dragon', FER, .1, (0, -.44, .29), (1, 1.2, .9), 10, 6, t, metal=.5)
    for s in (-1, 1): cylindre(f'CorneD{s}', LAITON, .025, .006, .14, 5, (s * .06, -.4, .36), t, rot=(-.8, s * .5, 0), metal=.6)
    sphere('Gueule', '#ff6a1a', .05, (0, -.54, .28), (1, .4, .8), 8, 4, t, emis=2)
    for k in range(3): sphere(f'Boulet{k}', FER, .05, (.22 - k * .06, .3, z + .05), (1, 1, 1), 8, 5, r, metal=.5)
    return finir(r)

def tour(j):
    return [arbalete, marteau_pilon, baliste_plaque, mortier, canon_aa, phare, gueule_forge, enclume, mines, grondeterre][j](f'hautroc_{j}')
