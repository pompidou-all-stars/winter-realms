"""Elfes de Lunebois (2.40, direction « grimdark ») : forêt ancienne sous la neige. Écorce noire et tordue, mousse,
pins sombres, pierres levées couvertes de lichen, argent lunaire, lueurs de lune bleu pâle et venin vert acide.

Elfes, gardien sylvestre, ronces, fleur de venin, chouette et arbres au procédé des monstres organiques
(communs/peuples_hd.py, tours_hd.py) ; pierres et pins en pièces peintes avec l'occlusion cuite."""
import math
from mathutils import Vector
from . import tours_hd as HD, peuples_hd as P
from .outils import pivot, cylindre, boite, sphere, cone, prisme, anneau, collection, dans
from .organique import Volume as V, boule, corne, profil, plaque, tore
from .organique import cone as cone_o
from .neige import enneiger

ECORCE, ECORCE2, ECORCE3 = '#4a3c30', '#33291f', '#5e4c3a'
MOUSSE, PIN, PIN2 = '#4f6a3a', '#24382c', '#2f4636'
PIERRE, PIERRE2, NUIT = '#6f7872', '#525a56', '#1a1c1d'
LUNE, LUNE2, VENIN, ARGENT = '#bfe0ff', '#e6f4ff', '#9ad04a', '#a9b0b8'
ELFE, HABIT, HABIT2, CAPE = '#c9b6a2', '#3a473c', '#2c352e', '#26302a'
SOL = .12

# ---------------------------------------------------------------- socle
def socle(r, cote=.8):
    """Tapis de mousse et d'aiguilles sous la neige, dalles moussues, souches d'angle."""
    d = cote / 2
    boite('Assise', NUIT, cote, cote, .05, (0, 0, .025), .01, r)
    dal = pivot('Dallage', (0, 0, 0), r)
    boite('Humus', '#3a3a2c', cote * .92, cote * .92, .05, (0, 0, .07), .012, dal)
    for k, (x, y, s) in enumerate(((-.18, .22, .09), (.2, .24, .07), (.24, -.18, .08), (-.24, -.2, .07), (.02, .3, .06))):
        cylindre(f'Dalle{k}', PIERRE2, s, s * .9, .02, 7, (x * cote / .8, y * cote / .8, .095), dal)
    for k, (x, y, sx, sy) in enumerate(((-.3, .33, .16, .05), (.28, .34, .1, .04), (.34, -.08, .04, .12), (-.33, -.18, .05, .1))):
        sphere(f'Congere{k}', '#e6edf5', 1, (x * cote / .8, y * cote / .8, .1), (sx, sy, .022), 8, 4, dal, rough=.9)
    for sx in (-1, 1):
        for sy in (-1, 1):
            x, y = sx * d * .86, sy * d * .86
            cylindre(f'Souche{sx}{sy}', ECORCE2, .05, .04, .1, 7, (x, y, .05), r)
            sphere(f'Champi{sx}{sy}', '#8a3a2a', .02, (x + sx * .03, y, .155), (1, 1, .5), 6, 3, r)
    return SOL

def debut(nom):
    c = collection(nom); dans(c)
    r = pivot(nom)
    return c, r, socle(r)

def finir(r):
    HD.peindre_sauf_statues(r, sol=.5, cime=1.0, bruit=.14)
    enneiger(r, 6000)
    HD.peindre_architecture(r)
    return r

def pin(nom, parent, pos, h=.5, r=.14, etages=4):
    """Pin sombre en étages pendants (la neige se pose sur chaque étage)."""
    x, y, z = pos
    cylindre(nom + 'Tronc', ECORCE2, r * .14, r * .08, h * .5, 6, (x, y, z), parent)
    for k in range(etages):
        t = k / etages
        cone(f'{nom}Etage{k}', PIN if k % 2 else PIN2, r * (1 - t * .7), h * .38, 8, (x, y, z + h * (.18 + t * .62)), parent)

# ---------------------------------------------------------------- arbres et créatures (coordonnées réelles, H = 1)
def tronc_vols(base, h, r0, courbe=(0, 0), racines=5, col=ECORCE, col2=ECORCE2, branches=(), seg=4, rot0=0.0):
    """Tronc tordu en segments, racines qui s'étalent, branches [(hauteur relative, angle, longueur, montée)]."""
    v = []; b = Vector(base)
    pts = [b + Vector((courbe[0] * math.sin(t * 3.1) * t, courbe[1] * math.sin(t * 2.3) * t, h * t)) for t in [i / seg for i in range(seg + 1)]]
    for i in range(seg):
        v.append(V('Tronc', col if i % 2 else col2, a=pts[i], b=pts[i + 1], ra=r0 * (1 - i / seg * .55), rb=r0 * (1 - (i + 1) / seg * .55)))
    for k in range(racines):
        a = k * 2 * math.pi / racines + rot0
        d = Vector((math.cos(a), math.sin(a), 0))
        v.append(V('Racine', col2, a=b + d * r0 * .5 + Vector((0, 0, r0 * .6)), b=b + d * r0 * 2.4 + Vector((0, 0, .005)), ra=r0 * .42, rb=r0 * .12))
    for k, (t, a, l, m) in enumerate(branches):
        p0 = pts[0].lerp(pts[-1], t); d = Vector((math.cos(a), math.sin(a), m)).normalized()
        rr = r0 * (1 - t * .55) * .45
        v.append(V('Branche', col, a=p0, b=p0 + d * l * .6, ra=rr, rb=rr * .6))
        v.append(V('Branche', col2, a=p0 + d * l * .6, b=p0 + d * l + Vector((0, 0, l * .15)), ra=rr * .6, rb=rr * .2))
    return v, pts[-1]

def archer_elfe(nom, H=.4, long_arc=False):
    bl, br = P.pose_tirer_arc(); J = P.joints(bl, br, 'elfe')
    hc = J['tete'] + Vector((0, 0, .06 * .95))
    L = .5 if long_arc else .34
    m = J['poignet.L']
    # 2.40 (retouche) : if clair à poignée d'argent, plus épais ; corde et flèche visibles
    pts = [(-.02, -L), (0, -L * .93), (.045, -L * .5), (.06, 0), (.045, L * .5), (0, L * .93), (-.02, L), (.024, L * .5), (.034, 0), (.024, -L * .5)]
    p = [profil('Arc', '#9a7a54', 'Main.G', pts, .026, pos=tuple(m + Vector((0, -.02, .0))), rot=(0, 0, math.pi / 2)),
         plaque('Poignee', ARGENT, 'Main.G', tuple(m + Vector((0, -.05, 0))), .03, .03, .06),
         cone_o('Corde', '#e6e0cc', 'Main.G', tuple(m + Vector((0, .0, -L * .95))), .0035, .0035, L * 1.9, seg=4),
         cone_o('Fleche', '#6a5238', 'Main.R', tuple(J['poignet.R'] + Vector((0, .02, 0))), .006, .006, .4, rot=(math.pi / 2, 0, .0), seg=4),
         boule('Capuche', CAPE, 'Tete', tuple(hc + Vector((0, .012, .012))), .07, ech=(1, 1.1, 1.05), seg=12),
         cone_o('PointeCapuche', CAPE, 'Tete', tuple(hc + Vector((0, .06, .03))), .03, .004, .1, rot=(1.9, 0, 0), seg=6),
         cone_o('Carquois', ECORCE2, 'Torse', tuple(J['poitrine'] + Vector((-.06, .1, -.12))), .03, .034, .26, rot=(-.25, .35, 0), seg=8)]
    p += P.cape(J, CAPE, .62, 'elfe') + P.ceinture(J, '#2a2620', ARGENT, 'elfe')
    return P.humain_statue(nom, J, g='elfe', pieces=p, H=H, tri=1600, taille=256 if not long_arc else 512, peau=ELFE, habit=HABIT,
                           habit2=HABIT2, cuir='#2a2420', gants='#3a3228', cheveux='#d8d4c8', jupe=.2)

def gardien(nom, H=1.0):
    """Gardien sylvestre : tronc vivant voûté, bras-branches noueux, jambes-racines, visage d'écorce, yeux de lune."""
    v, top = tronc_vols((0, 0, .02), .42, .1, courbe=(.02, .03), racines=6, seg=4)
    v = [x for x in v if x.os != 'Racine'] + [x for x in v if x.os == 'Racine'][:6]
    v += [V('Tete', ECORCE, c=(0, -.04, .5), r=(.1, .09, .1)),
          V('Tete', ECORCE3, c=(0, -.12, .52), r=(.065, .025, .016), prio=1),                      # arcade
          V('Tete', NUIT, c=(0, -.12, .45), r=(.04, .02, .018), prio=2, rel=0),                      # bouche creuse
          V('Tete', ECORCE2, a=(0, -.12, .5), b=(0, -.17, .46), ra=.018, rb=.01, prio=1)]            # nez-nœud
    for s, n in ((1, 'G'), (-1, 'R')):
        e = Vector((s * .1, -.01, .4)); c_ = Vector((s * .25, -.06, .3)); p_ = Vector((s * .27, -.14, .12))
        v += [V(f'Bras.{n}', ECORCE, a=e, b=c_, ra=.045, rb=.035), V(f'Bras.{n}', ECORCE2, a=c_, b=p_, ra=.035, rb=.025)]
        for q in range(4):
            v.append(V(f'Main.{n}', ECORCE3, a=p_, b=p_ + Vector((s * (q - 1.5) * .03, -.03, -.08 - q * .01)), ra=.014, rb=.004))
        v.append(V(f'Mousse.{n}', MOUSSE, c=e + Vector((0, .02, .04)), r=(.06, .05, .03), prio=1))
    for k in range(5):
        a = k * 1.25
        v.append(V('Couronne', ECORCE2, a=(math.cos(a) * .05, math.sin(a) * .04, .58), b=(math.cos(a) * .16, math.sin(a) * .1, .78), ra=.02, rb=.004))
    lu = [boule('OeilL', LUNE, 'Tete', (.035, -.125, .5), .01), boule('OeilR', LUNE, 'Tete', (-.035, -.125, .5), .01)]
    return HD.statue(nom, v, (), lu, couleur_lueur=LUNE, relief=P.RELIEF_ECORCE, tri=2400, voxel=.006, H=H, taches=.3)

def ronces_vols():
    """Massif de ronces : tiges épaisses qui s'entrelacent en arceaux."""
    v = []
    for k in range(9):
        a = k * 2 * math.pi / 9; a2 = a + 1.7 + (k % 3) * .4
        p0 = Vector((math.cos(a) * .3, math.sin(a) * .26, .0)); p2 = Vector((math.cos(a2) * .28, math.sin(a2) * .24, .0))
        p1 = (p0 + p2) / 2 + Vector((0, 0, .18 + (k % 3) * .05))
        v += [V('Tige', ECORCE2 if k % 2 else '#3e2e2a', a=p0, b=p1, ra=.022, rb=.016), V('Tige', '#3e2e2a', a=p1, b=p2, ra=.016, rb=.01)]
    return v

def fleur_venin(nom, H=1.0):
    """Fleur de venin : tige charnue, gros bulbe veiné entrouvert, pétales lourds, cœur de venin."""
    v = [V('Tige', '#3d5a2e', a=(0, 0, 0), b=(.03, .02, .25), ra=.05, rb=.035),
         V('Tige', '#4a6a34', a=(.03, .02, .25), b=(0, -.02, .42), ra=.035, rb=.03),
         V('Bulbe', '#5a3a4a', c=(0, -.03, .5), r=(.11, .1, .09)),
         V('Bulbe', '#7a3a5a', c=(0, -.08, .5), r=(.08, .05, .06), prio=1)]
    for k in range(6):
        a = k * math.pi / 3
        v.append(V('Feuille', '#2f4a28', a=(.0, .0, .06), b=(math.cos(a) * .3, math.sin(a) * .3, .03), ra=.03, rb=.012))
        v.append(V('Veine', '#8a2a4a', a=(math.cos(a) * .06, math.sin(a) * .06 - .03, .55), b=(math.cos(a) * .1, math.sin(a) * .09 - .03, .47), ra=.008, rb=.004, prio=1))
    p = []
    for k in range(5):
        a = k * 2 * math.pi / 5 + .3
        p.append(profil(f'Petale{k}', '#6a2a4a', 'Bulbe', [(0, 0), (.07, .06), (.06, .16), (0, .2), (-.06, .16), (-.07, .06)], .01,
                        pos=(math.cos(a) * .07, math.sin(a) * .07 - .03, .55), rot=(.0, 0, a - math.pi / 2)))
        p[-1].rotation_euler = (0, 0, 0)
    for k in range(7):
        a = k * .9
        p.append(corne(f'Epine{k}', '#c8c0a0', 'Tige', (math.cos(a) * .035, math.sin(a) * .035, .1 + k * .045), .006, .035, .3, rot=(0, 1.2, a), seg=4))
    lu = [boule('Venin', VENIN, 'Bulbe', (0, -.06, .6), .045)]
    return HD.statue(nom, v, p, lu, couleur_lueur=VENIN, relief=P.RELIEF_PEAU, tri=2000, voxel=.005, H=H, taches=.35)

def chouette(nom, H=.32):
    v = P.rapace_vols(plumage='#d6d4cc', ventre='#eeece6', bec='#3a3430', ailes=.0, chouette=True)
    for k in range(10):     # mouchetures sombres
        a = k * 1.7
        v.append(V('Torse', '#7a7468', c=(math.cos(a) * .17, math.sin(a) * .15, .3 + (k % 5) * .05), r=(.03, .03, .02), prio=1))
    lu = [boule('OeilL', '#f0c040', 'Tete', (.065, -.158, .75), .02), boule('OeilR', '#f0c040', 'Tete', (-.065, -.158, .75), .02)]
    return HD.statue(nom, v, (), lu, couleur_lueur='#f0c040', relief=P.RELIEF_PLUME, tri=1500, voxel=.006, H=H, taches=.3, taille=256)

def arbre_statue(nom, h, r0, branches, racines=6, H=1.0, tri=2000, lueurs=(), couleur_lueur=LUNE, pieces=(), extra=()):
    v, top = tronc_vols((0, 0, 0), h, r0, courbe=(.04, .03), racines=racines, branches=branches)
    return HD.statue(nom, v + list(extra), pieces, lueurs, couleur_lueur=couleur_lueur, relief=P.RELIEF_ECORCE, tri=tri, voxel=.006, H=H, taches=.3)

# ---------------------------------------------------------------- les 10 tours
def archers(nom):
    """0 · Plate-forme de guet dans un vieux pin, archer elfe qui bande son arc."""
    c, r, z = debut(nom)
    HD.poser(arbre_statue(nom + '_arbre', .62, .07, [(.75, .5, .18, .3), (.85, 2.6, .16, .4)], tri=1400), r, (.12, .14, z))
    pin(nom + 'Cime', r, (.12, .14, z + .55), .35, .16, 3)
    cylindre('Plateforme', ECORCE3, .2, .2, .035, 10, (0, 0, z + .4), r)
    for k in range(4): cylindre(f'Etai{k}', ECORCE2, .012, .012, .28, 5, ((k % 2 * 2 - 1) * .1, (k // 2 * 2 - 1) * .1, z + .12), r, rot=((k // 2 * 2 - 1) * .25, (k % 2 * 2 - 1) * -.25, 0))
    for k in range(8):
        a = k * math.pi / 4
        cylindre(f'Rambarde{k}', ECORCE2, .008, .008, .1, 4, (math.cos(a) * .19, math.sin(a) * .19, z + .435), r)
    t = pivot('Tourelle', (0, 0, z + .435), r)
    HD.poser(archer_elfe(nom + '_elfe'), t, (0, -.04, 0))
    return finir(r)

def haie(nom):
    """1 · Haie de ronces : arceaux de tiges épineuses, baies de venin, ossements pris dans les épines."""
    c, r, z = debut(nom)
    p = []
    for k in range(26):
        a = k * 2.4; rr = .14 + (k % 4) * .045
        p.append(corne(f'Epine{k}', '#cfc6a6', 'Tige', (math.cos(a) * rr, math.sin(a) * rr * .9, .05 + (k % 5) * .045), .008, .05, .3, rot=(0, 1.0 + (k % 3) * .3, a), seg=4))
    lu = [boule(f'Baie{k}', VENIN, 'Tige', (math.cos(k * 1.3) * .22, math.sin(k * 1.3) * .2, .12 + (k % 3) * .04), .014) for k in range(7)]
    HD.poser(HD.statue(nom + '_ronces', ronces_vols(), p, lu, couleur_lueur=VENIN, relief=P.RELIEF_ECORCE, tri=2200, voxel=.005, H=1.0, taches=.3), r, (0, 0, z))
    sphere('Crane', '#bdb091', .035, (.08, -.12, z + .03), (.85, 1, .9), 7, 5, r, (.3, 0, .5))
    t = pivot('Tourelle', (0, 0, z + .2), r)
    return finir(r)

def enracineur(nom):
    """2 · Gardien enracineur : gardien sylvestre voûté, racines plongées dans un anneau de pierres runiques."""
    c, r, z = debut(nom)
    for k in range(7):
        a = k * 2 * math.pi / 7
        cylindre(f'Pierre{k}', PIERRE, .035, .025, .08 + (k % 2) * .04, 5, (math.cos(a) * .3, math.sin(a) * .3, z), r)
        boite(f'Rune{k}', LUNE, .02, .005, .015, (math.cos(a) * .27, math.sin(a) * .27, z + .05), 0, r, (0, 0, a + math.pi / 2), emis=1.2)
    t = pivot('Tourelle', (0, 0, z), r)
    HD.poser(gardien(nom + '_gardien'), t)
    return finir(r)

def fleur(nom):
    """3 · Fleur de venin : fleur carnivore géante au bulbe veiné, cœur de venin luisant, flaque acide."""
    c, r, z = debut(nom)
    sn = pivot('SansNeige', (0, 0, 0), r)
    cylindre('Flaque', '#3e5424', .11, .11, .006, 10, (.08, -.12, z + .002), sn, emis=.15)
    t = pivot('Tourelle', (0, 0, z), r)
    HD.poser(fleur_venin(nom + '_fleur'), t)
    return finir(r)

def nid_chouettes(nom):
    """4 · Nid des chouettes des neiges : chicot de pin mort, nid de branchages, chouette blanche mouchetée."""
    c, r, z = debut(nom)
    HD.poser(arbre_statue(nom + '_chicot', .55, .09, [(.5, .3, .22, .5), (.7, 2.9, .2, .6), (.9, 1.7, .15, .8)], tri=1500), r, (0, .04, z))
    cylindre('Nid', '#4a3a2a', .12, .1, .05, 10, (0, .04, z + .52), r)
    for k in range(8):
        a = k * math.pi / 4
        cylindre(f'Brindille{k}', ECORCE2, .006, .004, .2, 4, (math.cos(a) * .1, .04 + math.sin(a) * .1, z + .55), r, rot=(1.35, 0, a))
    t = pivot('Tourelle', (0, .04, z + .56), r)
    HD.poser(chouette(nom + '_chouette'), t)
    return finir(r)

def puits_lune(nom):
    """5 · Puits de lune : bassin de pierres moussues, eau qui reflète la lune, arche de pierre à croissant d'argent."""
    c, r, z = debut(nom)
    for k in range(10):
        a = k * 2 * math.pi / 10
        boite(f'Margelle{k}', PIERRE if k % 2 else PIERRE2, .12, .07, .08, (math.cos(a) * .22, math.sin(a) * .22, z + .04), .01, r, (0, 0, a + math.pi / 2))
    sn = pivot('SansNeige', (0, 0, 0), r)
    cylindre('Eau', '#4a7aa0', .2, .2, .006, 14, (0, 0, z + .06), sn, emis=.8)
    for s in (-1, 1): cylindre(f'Pilier{s}', PIERRE, .035, .03, .5, 6, (s * .2, .14, z), r)
    boite('Linteau', PIERRE2, .5, .06, .06, (0, .14, z + .53), .008, r)
    ob = pivot('Orbe', (0, 0, 0), pivot('Tourelle', (0, .14, z + .7), r))
    anneau('Croissant', ARGENT, .07, .015, 14, 4, (0, 0, 0), ob, (math.pi / 2, 0, 0), metal=.7)
    sphere('Lune', LUNE2, .028, (0, 0, 0), (1, 1, 1), 8, 5, ob, emis=2)
    return finir(r)

def cercle_floraison(nom):
    """6 · Cercle de Floraison : pierres levées liées de lierre autour d'une fleur de lune qui s'ouvre au-dessus."""
    c, r, z = debut(nom)
    for k in range(5):
        a = k * 2 * math.pi / 5
        cylindre(f'Pierre{k}', PIERRE, .05, .035, .32 + (k % 2) * .08, 5, (math.cos(a) * .26, math.sin(a) * .26, z), r, rot=(0, 0, a))
        for q in range(3): sphere(f'Lierre{k}{q}', MOUSSE, .03, (math.cos(a) * .27, math.sin(a) * .27, z + .08 + q * .09), (1, 1, 1.3), 6, 4, r)
    cylindre('Autel', PIERRE2, .1, .12, .1, 8, (0, 0, z), r)
    ob = pivot('Orbe', (0, 0, 0), pivot('Tourelle', (0, 0, z + .4), r))
    for k in range(7):
        a = k * 2 * math.pi / 7
        prisme(f'Petale{k}', '#d8e6f4', [(0, 0), (.04, .05), (0, .14), (-.04, .05)], .006, (math.cos(a) * .02, math.sin(a) * .02, 0), ob, (1.0, 0, a - math.pi / 2), emis=.6)
    sphere('Pistil', VENIN, .03, (0, 0, .02), (1, 1, 1), 8, 5, ob, emis=2)
    return finir(r)

def bosquet(nom):
    """7 · Bosquet ancien : trois pins noirs serrés, lanternes de lune pendues aux branches, pierre gravée."""
    c, r, z = debut(nom)
    for k, (x, y, h, rr) in enumerate(((-.12, .1, .72, .17), (.15, .12, .58, .15), (.0, -.12, .5, .13))):
        pin(f'Pin{k}', r, (x, y, z), h, rr, 4)
    for k, (x, y, zz) in enumerate(((-.2, -.02, .36), (.24, .0, .3), (.08, -.22, .26))):
        cylindre(f'Fil{k}', '#2a2420', .002, .002, .06, 3, (x, y, z + zz), r)
        f = pivot('Flamme' if k == 0 else f'Lanterne{k}', (x, y, z + zz - .02), r)
        sphere(f'Lanterne{k}', LUNE, .025, (0, 0, 0), (1, 1, 1.3), 6, 4, f, emis=2)
    boite('Stele', PIERRE2, .12, .04, .18, (.22, -.22, z + .09), .01, r, (0, 0, .4))
    boite('Gravure', LUNE, .05, .006, .06, (.21, -.244, z + .12), 0, r, (0, 0, .4), emis=1)
    return finir(r)

def tireur(nom):
    """8 · Tireur des cimes : haut pin noir, nid de guet perché, archer elfe au grand arc."""
    c, r, z = debut(nom)
    HD.poser(arbre_statue(nom + '_arbre', .85, .08, [(.6, .4, .2, .2), (.7, 2.8, .2, .3), (.85, 1.5, .15, .5)], tri=1500), r, (0, .1, z))
    pin(nom + 'Cime', r, (0, .1, z + .8), .3, .14, 3)
    cylindre('Nacelle', ECORCE3, .14, .12, .04, 8, (0, 0, z + .6), r)
    for k in range(6):
        a = k * math.pi / 3
        cylindre(f'Garde{k}', ECORCE2, .008, .008, .08, 4, (math.cos(a) * .13, math.sin(a) * .13, z + .64), r)
    t = pivot('Tourelle', (0, 0, z + .64), r)
    HD.poser(archer_elfe(nom + '_elfe', H=.42, long_arc=True), t, (0, -.02, 0))
    return finir(r)

def arbre_mere(nom):
    """9 · Arbre-Mère (ultime) : arbre colossal aux racines énormes, runes de lune dans l'écorce, cœur de lumière qui tourne
    dans un creux du tronc."""
    c, r, z = debut(nom)
    br = [(.55, .3, .35, .45), (.62, 2.4, .32, .5), (.7, 4.2, .3, .55), (.8, 1.3, .26, .7), (.85, 5.3, .22, .8)]
    runes = [boule(f'Rune{k}', LUNE, 'Tronc', (math.cos(k * 2.1) * .12, math.sin(k * 2.1) * .12, .12 + k * .09), .012) for k in range(5)]
    HD.poser(arbre_statue(nom + '_arbre', .75, .15, br, racines=8, tri=2600, lueurs=runes), r, (0, .04, z))
    for k, (x, y, zz, s) in enumerate(((.25, .2, .74, .15), (-.22, .14, .76, .14), (.05, -.14, .84, .13), (0, .14, .9, .14), (-.08, .2, .72, .12))):
        for q in range(3): cone(f'Frondaison{k}{q}', PIN if (k + q) % 2 else PIN2, s * (1 - q * .28), s * .9, 8, (x, y, z + zz + q * s * .4), r)
    cr = pivot('Cristal', (0, -.12, z + .3), r)
    sphere('Coeur', LUNE2, .05, (0, 0, 0), (1, 1, 1.2), 8, 5, cr, emis=3)
    for k in range(4):
        a = k * math.pi / 2
        cone(f'Eclat{k}', LUNE, .012, .07, 3, (math.cos(a) * .05, math.sin(a) * .05, 0), cr, (0, math.pi / 2, a), emis=2)
    return finir(r)

def tour(j):
    return [archers, haie, enracineur, fleur, nid_chouettes, puits_lune, cercle_floraison, bosquet, tireur, arbre_mere][j](f'lunebois_{j}')
