"""Clans de l'Orage Blanc (2.40, direction « grimdark ») : clans orcs des steppes gelées. Rondins bruts, peaux tendues,
fourrures blanches, os et défenses, pierres levées couvertes de runes, cuivre verdi, lueur d'orage bleu pâle.

Orcs (lanceur de haches, berserker, chaman) et aigle-tempête au procédé des monstres organiques (communs/peuples_hd.py) ;
huttes, totems et machines en pièces peintes avec l'occlusion cuite."""
import math
from mathutils import Vector
from . import tours_hd as HD, peuples_hd as P
from .outils import pivot, cylindre, boite, sphere, cone, prisme, anneau, collection, dans
from .organique import boule, corne, profil, plaque, tore
from .organique import cone as cone_o
from .neige import enneiger

BOIS, BOIS2, PEAU, PEAU2 = '#5a4430', '#3b2c21', '#7a5f44', '#5e4834'
FOURRURE, OS, OS2 = '#cfc4ad', '#bdb091', '#8f8468'
PIERRE, PIERRE2, NUIT = '#6b6a70', '#4c4b52', '#1b1a1e'
ROUGE, SANG, CUIVRE = '#6e2a22', '#4a1612', '#5f8a74'
FOUDRE, FOUDRE2 = '#a8dcff', '#e8f6ff'
ORC, ORC2 = '#5d6a48', '#4b5639'
SOL = .12

# ---------------------------------------------------------------- socle
def socle(r, cote=.8):
    """Terre gelée bordée de rondins, pieux d'angle coiffés de cornes, peau de bête jetée au sol."""
    d = cote / 2
    boite('Assise', NUIT, cote, cote, .05, (0, 0, .025), .01, r)
    dal = pivot('Dallage', (0, 0, 0), r)
    boite('Terre', '#4d4237', cote * .9, cote * .9, .05, (0, 0, .07), .01, dal)
    for k, (x, y, s) in enumerate(((-.22, .2, .06), (.25, .26, .045), (.28, -.2, .05), (-.26, -.25, .04), (0, .3, .035))):
        sphere(f'Galet{k}', PIERRE2, s, (x * cote / .8, y * cote / .8, .1), (1.2, 1, .55), 7, 4, dal)
    for k, (x, y, sx, sy) in enumerate(((-.3, .33, .16, .05), (.28, .34, .1, .04), (.34, -.08, .04, .12), (-.33, -.18, .05, .1))):
        sphere(f'Congere{k}', '#e6edf5', 1, (x * cote / .8, y * cote / .8, .1), (sx, sy, .022), 8, 4, dal, rough=.9)
    for s in range(4):
        a = s * math.pi / 2
        boite(f'Rondin{s}', BOIS2, cote * .92, .05, .05, (math.cos(a) * d * .93, math.sin(a) * d * .93, .1), .015, r, (0, 0, a + math.pi / 2))
    for sx in (-1, 1):
        for sy in (-1, 1):
            x, y = sx * d * .88, sy * d * .88
            cylindre(f'Pieu{sx}{sy}', BOIS, .03, .025, .2, 6, (x, y, .05), r)
            cylindre(f'Corne{sx}{sy}', OS, .018, .003, .12, 5, (x, y, .24), r, rot=(sy * -.5, sx * .5, 0))
    return SOL

def debut(nom):
    c = collection(nom); dans(c)
    r = pivot(nom)
    s = socle(r)
    return c, r, s

def finir(r):
    HD.peindre_sauf_statues(r, sol=.5, cime=1.0, bruit=.14)
    enneiger(r, 6000)
    HD.peindre_architecture(r)
    return r

def peau_tendue(nom, parent, l, h, pos, rot=(0, 0, 0), col=PEAU):
    pts = [(-l / 2, 0), (-l * .3, -.01), (0, 0), (l * .3, -.01), (l / 2, 0), (l * .48, -h * .7), (l * .3, -h), (0, -h * .93), (-l * .3, -h), (-l * .48, -h * .7)]
    return prisme(nom, col, pts, .008, pos, parent, rot)

def crane_bete(nom, parent, pos, rot=(0, 0, 0), r=.05):
    sphere(nom, OS, r, pos, (.8, 1.3, .7), 8, 5, parent, rot)
    for s in (-1, 1):
        cylindre(f'{nom}Corne{s}', OS2, r * .25, r * .05, r * 2.2, 5, (pos[0] + s * r * .6, pos[1], pos[2] + r * .3), parent, rot=(0, s * 1.2, 0))

# ---------------------------------------------------------------- orcs (hauteur 1)
def _orc(nom, J, pieces, H, tri=1900, taille=512, jupe=.14, **kw):
    cols = dict(peau=ORC, habit=PEAU2, habit2='#3e3328', cuir='#2c241c', cheveux=None, barbe=None, jupe=jupe)
    cols.update(kw)
    return P.humain_statue(nom, J, g='orc', pieces=pieces, H=H, tri=tri, taille=taille, relief=P.RELIEF_PEAU, **cols)

def defenses(J):
    hc = J['tete'] + Vector((0, 0, .063))
    return [corne(f'Defense{s}', '#d8ccb0', 'Tete', tuple(hc + Vector((s * .03, -.07, -.05))), .007, .04, .8, rot=(-.3, 0, 0), seg=4) for s in (1, -1)]

def fourrure_epaules(J, col=FOURRURE):
    p = []
    for s, n in ((1, 'G'), (-1, 'R')):
        e = J['epaule.L' if s > 0 else 'epaule.R']
        p.append(boule(f'Fourrure{n}', col, f'Bras.{n}', tuple(e + Vector((s * .015, .01, .03))), .075, ech=(1.1, 1.05, .7), seg=10))
    return p

def hache(nom, os_, J, cote, l=.32, tourne=0.0):
    """Hache tenue dans le prolongement de l'avant-bras (cote : 'L' ou 'R')."""
    c_, m = J['coude.' + cote], J['poignet.' + cote]
    d = (m - c_).normalized(); q = Vector((0, 0, 1)).rotation_difference(d)
    rot = q.to_euler(); rot.rotate_axis('Z', tourne)
    a = m - d * .07
    return [cone_o(nom + 'Manche', BOIS2, os_, tuple(a), .011, .009, l, rot=tuple(rot), seg=6),
            profil(nom + 'Fer', '#5a5a60', os_, [(0, 0), (.07, .03), (.09, -.04), (.07, -.11), (0, -.06)], .012,
                   pos=tuple(a + d * (l - .02)), rot=tuple(rot))]

def lanceur(nom, H=.4):
    bl, br = P.pose_lancer(); J = P.joints(bl, br, 'orc', penche=.03)
    p = defenses(J) + fourrure_epaules(J) + hache('H', 'Main.R', J, 'R', l=.28) + P.ceinture(J, '#2a2018', OS2, 'orc')
    p += [cone_o('Carquois', PEAU2, 'Torse', tuple(J['poitrine'] + Vector((.08, .11, -.05))), .04, .045, .2, rot=(.2, -.3, 0), seg=8)]
    return _orc(nom, J, p, H, tri=1600, taille=256)

def berserker(nom, H=.62):
    bl = ((.15, .01, .79), (.25, -.05, .72), (.3, -.15, .78), (.31, -.18, .8))
    br = ((-.15, .01, .79), (-.24, .03, .9), (-.27, -.04, 1.04), (-.27, -.06, 1.09))
    J = P.joints(bl, br, 'orc', penche=.06)
    p = defenses(J) + P.ceinture(J, '#2a2018', OS2, 'orc')
    p += hache('G', 'Main.G', J, 'L', l=.3) + hache('D', 'Main.R', J, 'R', l=.3, tourne=math.pi)
    hc = J['tete'] + Vector((0, 0, .063))
    p += [corne('Tresse', '#1e1a16', 'Tete', tuple(hc + Vector((0, .05, .05))), .016, .16, -.9, rot=(.6, 0, 0), seg=5)]
    for k in range(3):     # scarifications rouges sur le buste nu
        p.append(plaque(f'Peinture{k}', ROUGE, 'Torse', tuple(J['poitrine'] + Vector(((k - 1) * .04, -.1, .02 - k * .01))), .012, .006, .08, rot=(0, 0, .3)))
    return _orc(nom, J, p, H, tri=2200, habit=ORC, habit2='#3e3328', jupe=.18, bas='#4a3a2a')

def chaman(nom, H=.6):
    bl, br = P.pose_bras_leves(); J = P.joints(bl, br, 'orc', penche=.02)
    hc = J['tete'] + Vector((0, 0, .063))
    p = defenses(J) + fourrure_epaules(J, '#8a7a62') + P.cape(J, '#5a4a3a', .6, 'orc')
    p += [boule('Crane', OS, 'Tete', tuple(hc + Vector((0, .0, .055))), .055, ech=(.9, 1.2, .7), seg=10)]
    for s in (1, -1): p.append(corne(f'Bois{s}', OS2, 'Tete', tuple(hc + Vector((s * .04, .02, .09))), .012, .18, .6, rot=(0, s * .9, 0), seg=5))
    m = J['poignet.L']
    p += [cone_o('Baton', BOIS2, 'Main.G', tuple(m + Vector((0, 0, -.5))), .013, .009, .8, seg=6)]
    for k in range(4): p.append(tore(f'Plume{k}', ('#7a3a2a', '#cfc4ad')[k % 2], 'Main.G', tuple(m + Vector((0, 0, .1 + k * .025))), .016, .006, seg=8, seg2=3))
    lu = [boule('Eclair', FOUDRE, 'Main.G', tuple(m + Vector((0, 0, .34))), .035)]
    return _orc(nom, J, p, H, lueurs=lu, couleur_lueur=FOUDRE, tri=2200, jupe=.38, habit='#4a3c30', habit2='#3a2e24')

def aigle(nom, H=.5):
    v = P.rapace_vols(plumage='#4a3a2c', ventre='#7a6a52', tete='#e4ddd0', bec='#c9a040', ailes=.75)
    lu = [boule('OeilL', FOUDRE, 'Tete', (.045, -.172, .815), .008), boule('OeilR', FOUDRE, 'Tete', (-.045, -.172, .815), .008)]
    return HD.statue(nom, v, (), lu, couleur_lueur=FOUDRE, relief=P.RELIEF_PLUME, tri=2000, voxel=.006, H=H, taches=.25)

# ---------------------------------------------------------------- les 10 tours
def lanceurs(nom):
    """0 · Mirador de rondins, toit de peaux, lanceur de haches orc à la plateforme."""
    c, r, z = debut(nom)
    for sx in (-1, 1):
        for sy in (-1, 1):
            cylindre(f'Poteau{sx}{sy}', BOIS, .025, .022, .5, 6, (sx * .14, sy * .14, z), r, rot=(sy * -.08, sx * .08, 0))
    for k in range(2): boite(f'Croix{k}', BOIS2, .03, .3, .03, ((k * 2 - 1) * .14, 0, z + .2), .004, r, (.8, 0, 0))
    boite('Plancher', BOIS2, .4, .4, .04, (0, 0, z + .48), .006, r)
    for k in range(10):
        a = k * 2 * math.pi / 10
        cylindre(f'Garde{k}', BOIS, .014, .012, .12 + (k % 2) * .03, 5, (math.cos(a) * .19, math.sin(a) * .19, z + .5), r)
    for s in (-1, 1): cylindre(f'Mat{s}', BOIS2, .014, .014, .36, 5, (s * .17, .15, z + .5), r)
    peau_tendue('Toit', r, .44, .2, (0, .15, z + .86), (-.9, 0, 0))
    crane_bete('Trophee', r, (0, -.21, z + .46), (0, 0, 0), .04)
    t = pivot('Tourelle', (0, 0, z + .5), r)
    HD.poser(lanceur(nom + '_lanceur'), t, (0, -.03, 0))
    return finir(r)

def hutte_berserker(nom):
    """1 · Hutte du berserker : yourte de peaux sur perches, défenses de mammouth à l'entrée, berserker aux deux haches."""
    c, r, z = debut(nom)
    cylindre('Yourte', PEAU, .26, .2, .2, 10, (0, .14, z), r)
    cone('Comble', PEAU2, .23, .2, 10, (0, .14, z + .2), r)
    for k in range(6):
        a = k * math.pi / 3
        cylindre(f'Perche{k}', BOIS2, .008, .006, .18, 4, (math.cos(a) * .05, .14 + math.sin(a) * .05, z + .34), r, rot=(math.sin(a) * .3, -math.cos(a) * .3, 0))
    prisme('Porte', NUIT, [(-.06, 0), (.06, 0), (.04, .14), (-.04, .14)], .02, (0, -.12, z), r)
    for s in (-1, 1):
        cylindre(f'Defense{s}', '#d8ccb0', .025, .006, .4, 6, (s * .16, -.14, z), r, rot=(.5, s * -.5, 0))
    t = pivot('Tourelle', (0, -.18, z), r)
    HD.poser(berserker(nom + '_berserker'), t)
    return finir(r)

def totem_pluies(nom):
    """2 · Totem des pluies glacées : mât sculpté de visages, ailes de bois, nuée glacée qui flotte et pleure des glaçons."""
    c, r, z = debut(nom)
    cylindre('Mat', BOIS, .07, .06, .7, 8, (0, 0, z), r)
    for k in range(3):
        zz = z + .12 + k * .2
        sphere(f'Visage{k}', BOIS2, .075, (0, -.02, zz + .06), (1, .9, .8), 8, 5, r)
        boite(f'Bouche{k}', NUIT, .06, .02, .018, (0, -.085, zz + .03), 0, r)
        for s in (-1, 1): sphere(f'Oeil{k}{s}', '#2a6a8a', .012, (s * .025, -.085, zz + .085), (1, .6, 1), 5, 3, r, emis=1.2)
        boite(f'Nez{k}', BOIS, .02, .04, .05, (0, -.09, zz + .06), .004, r)
    for s in (-1, 1): prisme(f'Aile{s}', BOIS2, [(0, 0), (.22, .1), (.2, .04), (.24, -.02), (.12, -.05)], .02, (s * .06, 0, z + .62), r, (0, 0, 0 if s > 0 else math.pi))
    ob = pivot('Orbe', (0, 0, 0), pivot('Tourelle', (0, 0, z + .9), r))
    for k, (x, y, zz, s) in enumerate(((0, 0, 0, .1), (.09, .03, -.02, .07), (-.08, -.02, -.01, .075), (.02, .07, .03, .06), (-.03, -.08, .02, .06))):
        sphere(f'Nuee{k}', '#c8d6e0', s, (x, y, zz), (1.2, 1.1, .7), 9, 5, ob)
    for k in range(7):
        a = k * 2 * math.pi / 7
        cone(f'Glacon{k}', '#bfe4f4', .012, .09, 4, (math.cos(a) * .09, math.sin(a) * .07, -.06), ob, (math.pi, 0, 0), emis=.6)
    return finir(r)

def catapulte(nom):
    """3 · Catapulte à rochers : châssis de troncs liés, bras à cuilleron de peau chargé d'un rocher, torsion de cordages."""
    c, r, z = debut(nom)
    t = pivot('Tourelle', (0, 0, z), r)
    for s in (-1, 1):
        cylindre(f'Longeron{s}', BOIS, .035, .035, .56, 7, (s * .14, .28, .05), t, rot=(math.pi / 2, 0, 0))
        boite(f'Chevalet{s}', BOIS2, .04, .04, .3, (s * .14, .02, .2), .004, t, (.2, 0, 0))
        sphere(f'RoueP{s}', BOIS2, .06, (s * .18, -.2, .06), (.4, 1, 1), 8, 6, t)
    cylindre('Traverse', BOIS2, .03, .03, .32, 7, (-.16, -.05, .32), t, rot=(0, math.pi / 2, 0))
    cylindre('Torsion', '#8a7a5a', .05, .05, .18, 8, (-.09, .12, .1), t, rot=(0, math.pi / 2, 0))
    cylindre('BrasC', BOIS, .025, .02, .55, 6, (0, .12, .1), t, rot=(-1.15, 0, 0))
    sphere('Cuilleron', PEAU2, .07, (0, -.38, .32), (1, 1, .45), 8, 4, t)
    sphere('Rocher', PIERRE, .065, (0, -.38, .37), (1, .9, .85), 7, 5, t)
    for k in range(3): sphere(f'Reserve{k}', PIERRE2, .045, (.2 + k * .03, .25 - k * .06, .05), (1, 1, .8), 6, 4, r)
    return finir(r)

def aire_aigles(nom):
    """4 · Aire des aigles-tempête : aiguille de roche fendue, nid de branchages et d'os, aigle aux ailes à demi ouvertes."""
    c, r, z = debut(nom)
    for k, (x, y, rr, h, a) in enumerate(((0, .02, .14, .45, 0), (.1, -.06, .08, .3, .3), (-.1, .06, .07, .25, -.2))):
        cylindre(f'Roche{k}', PIERRE if k else PIERRE2, rr, rr * .6, h, 6, (x, y, z), r, rot=(0, a * .2, a))
    for k in range(10):
        a = k * 2 * math.pi / 10
        cylindre(f'Branche{k}', BOIS2, .01, .008, .24, 4, (math.cos(a) * .12, .02 + math.sin(a) * .12, z + .46), r, rot=(1.3, 0, a))
    cylindre('Nid', '#4a3a2a', .13, .1, .05, 10, (0, .02, z + .43), r)
    for k in range(2): sphere(f'OsNid{k}', OS, .015, ((k - .5) * .14, -.08, z + .48), (1, 3, 1), 5, 3, r, (0, 0, k))
    t = pivot('Tourelle', (0, .02, z + .47), r)
    HD.poser(aigle(nom + '_aigle'), t)
    return finir(r)

def hutte_chaman(nom):
    """5 · Hutte du chaman des esprits : tipi de peaux peintes, crâne cornu au faîte, chaman orc qui appelle la foudre."""
    c, r, z = debut(nom)
    cone('Tipi', PEAU, .2, .45, 9, (0, .17, z), r)
    for k in range(5):
        a = k * 2 * math.pi / 5
        cylindre(f'Perche{k}', BOIS2, .007, .005, .18, 4, (math.cos(a) * .02, .17 + math.sin(a) * .02, z + .4), r, rot=(math.sin(a) * .35, -math.cos(a) * .35, 0))
    for k in range(3): prisme(f'Signe{k}', ROUGE, [(-.03, 0), (.03, 0), (0, .05)], .004, (0 + (k - 1) * .06, .03 + abs(k - 1) * .02, z + .12 + (k % 2) * .06), r)
    crane_bete('Faite', r, (0, .1, z + .4), (0, 0, 0), .04)
    t = pivot('Tourelle', (0, -.15, z), r)
    HD.poser(chaman(nom + '_chaman'), t)
    return finir(r)

def totem_foudre(nom):
    """6 · Totem de foudre : menhir gravé de runes, spirale de cuivre verdi, cristal d'orage qui tourne entre deux cornes."""
    c, r, z = debut(nom)
    cylindre('Menhir', PIERRE, .13, .07, .62, 6, (0, 0, z), r)
    for k in range(5): boite(f'Rune{k}', FOUDRE, .03, .006, .02, (0, -.105 + k * .009, z + .1 + k * .1), 0, r, emis=1.4)
    for k in range(9):
        a = k * .9
        sphere(f'Spire{k}', CUIVRE, .015, (math.cos(a) * (.12 - k * .006), math.sin(a) * (.12 - k * .006), z + .06 + k * .06), (1, 1, 1), 5, 3, r, metal=.6)
    for s in (-1, 1): cylindre(f'Corne{s}', OS, .025, .006, .26, 6, (s * .05, 0, z + .6), r, rot=(0, s * .55, 0))
    cr = pivot('Cristal', (0, 0, 0), pivot('Tourelle', (0, 0, z + .8), r))
    sphere('Orage', FOUDRE, .07, (0, 0, 0), (.8, .8, 1.3), 6, 4, cr, emis=2)
    for k in range(4):
        a = k * math.pi / 2
        cone(f'Arc{k}', FOUDRE2, .008, .12, 3, (math.cos(a) * .05, math.sin(a) * .05, 0), cr, (math.sin(a) * 1.2, -math.cos(a) * 1.2, 0), emis=3)
    return finir(r)

def tambours(nom):
    """7 · Grands tambours de guerre : deux fûts tendus de peau sur un bâti de rondins, cornes de guerre, bannière de clan."""
    c, r, z = debut(nom)
    boite('Bati', BOIS2, .5, .26, .05, (0, .05, z + .12), .006, r)
    for s in (-1, 1):
        for q in (-1, 1): cylindre(f'Pied{s}{q}', BOIS, .02, .02, .14, 5, (s * .22, .05 + q * .1, z), r)
    for s, h, rr in ((-1, .26, .13), (1, .2, .1)):
        cylindre(f'Fut{s}', BOIS, rr, rr, h, 12, (s * .12, .05, z + .14), r)
        cylindre(f'Peau{s}', '#c8b48e', rr * 1.02, rr * 1.02, .012, 12, (s * .12, .05, z + .14 + h), r)
        for k in range(8):
            a = k * math.pi / 4
            cylindre(f'Lacet{s}{k}', '#3a2a1e', .004, .004, h, 3, (s * .12 + math.cos(a) * rr * 1.01, .05 + math.sin(a) * rr * 1.01, z + .14), r)
    for s in (-1, 1):
        cylindre(f'Mailloche{s}', BOIS2, .008, .008, .2, 4, (s * .12, -.08, z + .44), r, rot=(.9, s * .4, 0))
        sphere(f'Tete{s}', PEAU2, .02, (s * .16, -.2, z + .56), (1, 1, 1), 6, 4, r)
    cylindre('Cor', OS, .03, .008, .3, 8, (.22, -.2, z + .1), r, rot=(1.2, 0, .6))
    cylindre('Hampe', BOIS2, .012, .012, .8, 5, (-.28, .2, z), r)
    peau_tendue('Banniere', r, .16, .3, (-.2, .2, z + .78), (0, 0, 0), ROUGE)
    return finir(r)

def totem_sang(nom):
    """8 · Totem de sang : pierre de sacrifice ruisselante, crânes sur des pieux, chaînes, vasque de sang qui luit."""
    c, r, z = debut(nom)
    cylindre('Pierre', PIERRE2, .15, .12, .4, 7, (0, .05, z), r)
    for k in range(5): boite(f'Coulure{k}', SANG, .02, .01, .15 + (k % 3) * .06, (-.08 + k * .04, -.08, z + .2), 0, r)
    for k, (x, y, h) in enumerate(((-.22, -.1, .45), (.22, -.12, .5), (-.18, .2, .55), (.2, .18, .42))):
        cylindre(f'Pieu{k}', BOIS2, .012, .01, h, 5, (x, y, z), r)
        sphere(f'Crane{k}', OS, .04, (x, y, z + h + .02), (.85, 1, .95), 8, 5, r)
        for s in (-1, 1): sphere(f'Orbite{k}{s}', NUIT, .01, (x + s * .014, y - .033, z + h + .025), (1, .6, 1), 4, 3, r)
    cylindre('Vasque', '#3a3438', .1, .07, .06, 10, (0, -.18, z), r, metal=.4)
    sn = pivot('SansNeige', (0, 0, 0), r)
    cylindre('Sang', '#8a1a14', .09, .09, .006, 10, (0, -.18, z + .058), sn, emis=.8)
    ob = pivot('Orbe', (0, 0, 0), pivot('Tourelle', (0, .05, z + .52), r))
    sphere('Goutte', '#a8201a', .04, (0, 0, 0), (1, 1, 1.4), 8, 5, ob, emis=1.5)
    return finir(r)

def coeur_orage(nom):
    """9 · Cœur de l'Orage (ultime) : cercle de pierres levées runiques, anneaux d'éclairs qui tournent autour d'un cœur d'orage."""
    c, r, z = debut(nom)
    cylindre('Dalle', PIERRE2, .25, .27, .05, 10, (0, 0, z), r)
    for k in range(6):
        a = k * math.pi / 3
        cylindre(f'Menhir{k}', PIERRE, .055, .03, .45 + (k % 2) * .12, 5, (math.cos(a) * .3, math.sin(a) * .3, z), r, rot=(math.sin(a) * .12, -math.cos(a) * .12, 0))
        boite(f'Rune{k}', FOUDRE, .025, .006, .02, (math.cos(a) * .27, math.sin(a) * .27, z + .25), 0, r, (0, 0, a + math.pi / 2), emis=1.4)
    tr = pivot('Tourelle', (0, 0, z + .62), r)
    an = pivot('Anneaux', (0, 0, 0), tr)
    for k in range(3):
        anneau(f'Eclair{k}', FOUDRE, .16 + k * .04, .007, 20, 3, (0, 0, 0), an, (k * .9, k * .5, 0), emis=2.5)
    cr = pivot('Cristal', (0, 0, 0), tr)
    sphere('Coeur', FOUDRE2, .09, (0, 0, 0), (1, 1, 1), 10, 6, cr, emis=3)
    for k in range(6):
        a = k * math.pi / 3
        cone(f'Pointe{k}', FOUDRE, .02, .12, 3, (math.cos(a) * .08, math.sin(a) * .08, 0), cr, (0, math.pi / 2, a), emis=2)
    return finir(r)

def tour(j):
    return [lanceurs, hutte_berserker, totem_pluies, catapulte, aire_aigles, hutte_chaman, totem_foudre, tambours, totem_sang, coeur_orage][j](f'orage_{j}')
