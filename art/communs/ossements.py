"""Cour des Ossements (2.40, pilote de la refonte des modèles de race) : 10 tours qui ne sont pas toutes des tours.

Direction artistique « grimdark » (demande du concepteur : plus dark fantasy, moins cartoon) : proportions réalistes
(petites têtes, silhouettes élancées), architecture gothique (arcs brisés, contreforts, flèches), fer rouillé, os jaunis,
étendards en lambeaux, chaînes et pointes ; palette désaturée, lueurs rares et maladives (vert-de-gris, violet sourd).

Créatures et objets nécromantiques : archers squelettes sur une tour de guet gothique, ossuaire d'où sort un guerrier
mort, obélisque maudit, autel de peste, gargouille démoniaque, œil sans paupière dans une cage d'os, nécromancien,
puits des âmes, faucheuse, colosse d'os en armure.
Pièces animées par le jeu : Tourelle (vise), Cristal (tourne), Orbe (pulse), Anneaux (tournent), AnneauFlottant.
Socle commun : dalle carrée de mausolée, pierre noire fendue, pointes de fer aux coins ; neige ajoutée par enneiger()."""
import math
from . import outils
from .outils import pivot, cylindre, boite, sphere, cone, prisme, anneau, peindre, collection, dans
from .neige import enneiger

OS, OS2, OS3 = '#b7ab8a', '#968a6b', '#665c46'            # os jauni, os sale, os pourri
PIERRE, PIERRE2, NUIT = '#5a5763', '#3b3943', '#17161c'    # pierre de mausolée, pierre sombre, ombre
FER, FER2, ROUILLE = '#2c2b30', '#4a4850', '#6b3d24'       # fer noir, fer usé, rouille
TISSU, TISSU2 = '#2a2226', '#3e2a2c'                      # linceul, étendard bordeaux passé
AME, MAUDIT, PESTE, CIRE = '#6fd2c0', '#7d58a8', '#8aa83a', '#cfc3a2'
SOL = 0.12

# ---------------------------------------------------------------- pièces de base
def crane(nom, parent, r, pos=(0, 0, 0), rot=(0, 0, 0), lueur=AME, machoire=True, lueur_force=1.6):
    """Crâne allongé et anguleux : arcade sourcilière, orbites profondes (faible lueur au fond), pommettes, mâchoire étroite."""
    c = pivot(nom, pos, parent); c.rotation_euler = rot
    sphere(nom + 'Boite', OS, r, (0, r * .08, 0), (.86, 1.12, .95), 10, 7, c)
    boite(nom + 'Arcade', OS2, r * 1.5, r * .3, r * .22, (0, -r * .78, -r * .12), r * .06, c)
    sphere(nom + 'Face', OS2, r * .62, (0, -r * .55, -r * .5), (1.05, .8, 1.05), 8, 5, c)
    for s in (-1, 1):
        sphere(nom + f'Orbite{s}', NUIT, r * .26, (s * r * .33, -r * .86, -r * .3), (1, .55, .9), 6, 4, c)
        sphere(nom + f'Lueur{s}', lueur, r * .07, (s * r * .33, -r * .95, -r * .3), (1, .5, 1), 5, 3, c, emis=lueur_force)
        boite(nom + f'Pommette{s}', OS2, r * .3, r * .3, r * .18, (s * r * .5, -r * .6, -r * .55), r * .05, c, (0, 0, s * .4))
    cone(nom + 'Nez', NUIT, r * .1, r * .22, 3, (0, -r * 1.05, -r * .55), c, (math.pi, 0, 0))
    if machoire:
        boite(nom + 'Machoire', OS3, r * .85, r * .6, r * .22, (0, -r * .5, -r * 1.02), r * .05, c, (.25, 0, 0))
        for k in range(4):
            cone(nom + f'Dent{k}', OS, r * .05, r * .14, 3, ((k - 1.5) * r * .16, -r * .84, -r * .84), c, (math.pi, 0, 0))
    return c

def os_long(nom, parent, a, b, r, col=OS2):
    """Os entre les points a et b (rayon r) : fût mince et épiphyses aplaties."""
    ax, ay, az = a; bx, by, bz = b
    dx, dy, dz = bx - ax, by - ay, bz - az; L = math.sqrt(dx * dx + dy * dy + dz * dz)
    rot = (math.acos(max(-1, min(1, dz / L))), 0, math.atan2(dy, dx) + math.pi / 2) if L else (0, 0, 0)
    cylindre(nom, col, r, r * .8, L, 5, a, parent, rot=rot)
    for q, p in enumerate((a, b)): sphere(nom + f'Noeud{q}', OS, r * 1.45, p, (1.25, .9, .9), 6, 4, parent, rot=rot)

def pointe(nom, parent, pos, h, r=.012, rot=(0, 0, 0), col=FER):
    cone(nom, col, r, h, 4, pos, parent, rot, metal=.6, rough=.5)

def lambeaux(nom, parent, l, h, pos, rot=(0, 0, 0), col=TISSU2):
    """Étendard ou pan de linceul déchiqueté (bas en dents de scie)."""
    pts = [(-l / 2, 0), (l / 2, 0), (l / 2, -h * .8), (l * .3, -h), (l * .15, -h * .7), (0, -h * .95), (-l * .2, -h * .65), (-l * .35, -h * .9), (-l / 2, -h * .75)]
    return prisme(nom, col, pts, .006, pos, parent, rot)

def chaine(nom, parent, a, b, n=5):
    L = math.sqrt(sum((b[i] - a[i]) ** 2 for i in range(3)))
    n = max(n, int(L / .024) + 1)
    for k in range(n):
        t = k / (n - 1); p = tuple(a[i] + (b[i] - a[i]) * t for i in range(3))
        anneau(f'{nom}{k}', FER2, .014, .004, 6, 3, (p[0], p[1], p[2] - math.sin(t * math.pi) * .04), parent, ((k % 2) * math.pi / 2, 0, 0), metal=.6)

def squelette(racine, H, arme=None, lueur=AME, casque=None, armure=True, linceul=TISSU):
    """Squelette guerrier aux proportions humaines (tête petite), armure rouillée dépareillée, linceul en lambeaux.
    Regarde vers -Y, pieds en z = 0. Pivots : Corps, Tete, BrasG, BrasD, JambeG, JambeD."""
    hz = H * .47
    for s, n in ((-1, 'G'), (1, 'D')):
        j = pivot(f'Jambe{n}', (s * H * .06, 0, hz), racine)
        os_long(f'Femur{n}', j, (0, 0, 0), (0, -H * .02, -hz * .5), H * .016)
        os_long(f'Tibia{n}', j, (0, -H * .02, -hz * .5), (0, 0, -hz + H * .03), H * .014)
        boite(f'Greve{n}', ROUILLE, H * .05, H * .05, H * .14, (0, -H * .01, -hz * .72), H * .006, j, metal=.5, rough=.6)
        boite(f'Pied{n}', OS3, H * .05, H * .1, H * .03, (0, -H * .035, -hz + H * .015), H * .006, j)
    corps = pivot('Corps', (0, 0, hz), racine)
    boite('Bassin', OS2, H * .15, H * .08, H * .05, (0, 0, 0), H * .012, corps)
    lambeaux('Linceul', corps, H * .2, H * .28, (0, -H * .045, H * .01), (0, 0, 0), linceul)
    cylindre('Colonne', OS3, H * .016, H * .014, H * .3, 5, (0, H * .015, 0), corps)
    for k in range(4):
        z = H * (.12 + k * .05); w = H * (.075 - abs(k - 1.5) * .008)
        anneau(f'Cote{k}', OS, w, H * .008, 10, 3, (0, -H * .008, z), corps, (-.12, 0, 0), echelle=(1, .7, 1))
    if armure:
        prisme('Plastron', ROUILLE, [(-H * .08, H * .2), (H * .08, H * .2), (H * .06, H * .02), (0, -H * .02), (-H * .06, H * .02)], H * .02, (0, -H * .07, H * .1), corps, metal=.5, rough=.55)
    for s, n in ((-1, 'G'), (1, 'D')):
        if armure:
            sphere(f'Spalliere{n}', FER, H * .055, (s * H * .1, 0, H * .31), (1.1, 1, .7), 8, 4, corps, metal=.6, rough=.45)
            pointe(f'PicEpaule{n}', corps, (s * H * .12, 0, H * .33), H * .09, H * .012, (0, s * .7, 0))
        b = pivot(f'Bras{n}', (s * H * .1, 0, H * .3), corps)
        os_long(f'Humerus{n}', b, (0, 0, 0), (s * H * .015, 0, -H * .17), H * .013)
        os_long(f'Avant{n}', b, (s * H * .015, 0, -H * .17), (s * H * .015, -H * .03, -H * .32), H * .011)
        for k in range(3): cone(f'Doigt{n}{k}', OS3, H * .006, H * .04, 3, (s * H * .015 + (k - 1) * H * .01, -H * .03, -H * .33), b, (math.pi, 0, 0))
        if n == 'D' and arme: arme(pivot('Arme', (s * H * .015, -H * .03, -H * .33), b), H)
    t = pivot('Tete', (0, 0, H * .35), corps)
    crane('Crane', t, H * .062, (0, 0, H * .07), (0, 0, 0), lueur)
    if casque:
        sphere('Casque', casque, H * .075, (0, H * .005, H * .095), (1, 1.05, .85), 10, 5, t, metal=.6, rough=.45)
        boite('Nasal', casque, H * .015, H * .02, H * .07, (0, -H * .07, H * .06), 0, t, metal=.6)
        for s in (-1, 1): cone(f'Corne{s}', OS3, H * .018, H * .14, 5, (s * H * .06, 0, H * .14), t, (0, s * -.9, 0))
    return corps

def arc_os(p, H):
    k = H * 1.5
    prisme('ArcOs', OS3, [(-.02 * k, -.25 * k), (0, -.23 * k), (.05 * k, -.1 * k), (.06 * k, 0), (.05 * k, .1 * k), (0, .23 * k), (-.02 * k, .25 * k), (.035 * k, 0)], .012, (0, -.02, 0), p, (0, 0, math.pi / 2))

def epee_rouillee(p, H):
    prisme('LameRouillee', FER2, [(-H * .025, 0), (H * .025, 0), (H * .02, H * .45), (0, H * .52), (-H * .02, H * .45)], H * .012, (0, -H * .02, H * .03), p, metal=.6, rough=.55)
    boite('GardeRouillee', ROUILLE, H * .14, H * .03, H * .025, (0, -H * .02, H * .02), 0, p, metal=.5)

def faux(p, H):
    cylindre('Manche', '#241c18', H * .016, H * .014, H * 1.15, 5, (0, 0, -H * .35), p)
    for k in range(3): anneau(f'Bague{k}', FER2, H * .02, H * .006, 6, 3, (0, 0, H * (.05 + k * .3)), p, metal=.6)
    # croissant : arc extérieur puis arc intérieur, de la douille à la pointe
    ext = [(H * x, -H * y) for x, y in [(0, 0), (.18, .01), (.36, .04), (.52, .1), (.66, .19), (.76, .3), (.82, .42)]]
    inn = [(H * x, -H * y) for x, y in [(.7, .3), (.6, .2), (.46, .13), (.3, .1), (.14, .1), (0, .1)]]
    prisme('LameFaux', '#7d838b', ext + inn, H * .014, (0, 0, H * .8), p, (0, 0, 0), metal=.85, rough=.3)
    prisme('Fil', '#b8c0c8', [(H * x, -H * y) for x, y in [(.02, .1), (.3, .105), (.46, .135), (.6, .205), (.7, .305), (.66, .27), (.5, .17), (.3, .125), (.02, .125)]], H * .016, (0, 0, H * .8), p, metal=.9, rough=.2)
    boite('Douille', FER, H * .05, H * .04, H * .09, (0, 0, H * .78), H * .005, p, metal=.6)
    crane('CraneFaux', p, H * .04, (0, -H * .03, H * .86), (0, 0, 0), machoire=False, lueur_force=1)

def bougie(nom, parent, pos, h=.07):
    cylindre(nom, CIRE, .012, .014, h, 5, pos, parent)
    sphere(nom + 'Flamme', '#d9a24a', .009, (pos[0], pos[1], pos[2] + h + .01), (1, 1, 1.8), 5, 3, parent, emis=3)

def socle(racine, cote=.8):
    """Dalle carrée de mausolée à deux gradins, pierre fendue, pointes de fer aux coins, crâne et os dans la neige."""
    d = cote / 2
    boite('Assise', NUIT, cote, cote, .05, (0, 0, .025), .01, racine)
    dal = pivot('Dallage', (0, 0, 0), racine)
    boite('Dalle', PIERRE2, cote * .9, cote * .9, .05, (0, 0, .07), .008, dal)
    for k in range(3):
        boite(f'Pave{k}', PIERRE, cote * .27, cote * .78, .012, ((k - 1) * cote * .29, 0, .1), .004, dal)
    for k, (x, y, sx, sy) in enumerate(((-.3, .33, .16, .05), (.25, .34, .12, .045), (.34, -.1, .045, .14), (-.34, -.2, .05, .1), (.05, -.34, .1, .04))):
        sphere(f'Congere{k}', '#e6edf5', 1, (x * cote / .8, y * cote / .8, .1), (sx, sy, .022), 8, 4, dal, rough=.9)
    for sx in (-1, 1):
        for sy in (-1, 1):
            boite(f'Coin{sx}{sy}', PIERRE, .09, .09, .1, (sx * d * .88, sy * d * .88, .1), .008, racine)
            pointe(f'Pic{sx}{sy}', racine, (sx * d * .88, sy * d * .88, .15), .12, .016)
    crane('CraneSol', racine, .03, (-d * .55, -d * .62, .13), (.3, 0, .6), machoire=False)
    os_long('OsSol', racine, (d * .3, -d * .66, .115), (d * .65, -d * .5, .112), .009)
    bougie('BougieA', racine, (d * .6, d * .62, .105)); bougie('BougieB', racine, (-d * .62, d * .55, .105), .05)
    return SOL

def debut(nom):
    c = collection(nom); dans(c)
    r = pivot(nom)
    return c, r, socle(r)

def finir(r, budget=6000, sol=.45):
    peindre(r, sol=sol, cime=1.0, bruit=.12)
    enneiger(r, budget)
    return r

def arc_brise(nom, parent, l, h, pos, rot=(0, 0, 0), col=NUIT):
    """Ouverture gothique (arc brisé) : rectangle surmonté d'une ogive."""
    pts = [(-l / 2, 0), (l / 2, 0), (l / 2, h * .62), (l * .3, h * .88), (0, h), (-l * .3, h * .88), (-l / 2, h * .62)]
    return prisme(nom, col, pts, .02, pos, parent, rot)

# ---------------------------------------------------------------- les 10 tours
def archers(nom):
    """0 · Tour des archers squelettes : tour de guet gothique à contreforts, flèche d'ardoise, deux archers morts sur le chemin de ronde."""
    c, r, z = debut(nom)
    boite('Fut', PIERRE, .34, .34, .44, (0, 0, z + .22), .01, r)
    for sx in (-1, 1):
        for sy in (-1, 1):
            prisme(f'Contrefort{sx}{sy}', PIERRE2, [(0, 0), (.1, 0), (.02, .4), (0, .4)], .05, (sx * .17, sy * .17, z), r, (0, 0, math.atan2(sy, sx) - math.pi / 2 + (math.pi if sx < 0 else 0)) if False else (0, 0, math.atan2(sy, sx) + math.pi / 2))
    arc_brise('Porte', r, .12, .2, (0, -.176, z), (0, 0, 0))
    arc_brise('Meurtriere', r, .04, .1, (0, -.176, z + .27))
    crane('CraneClef', r, .03, (0, -.18, z + .22), machoire=False)
    zt = z + .44
    boite('Mâchicoulis', PIERRE2, .42, .42, .05, (0, 0, zt + .025), .008, r)
    for k in range(8):
        a = k * math.pi / 4
        x, y = math.cos(a) * .19, math.sin(a) * .19
        boite(f'Merlon{k}', PIERRE, .07, .07, .08, (max(-.18, min(.18, x * 1.1)), max(-.18, min(.18, y * 1.1)), zt + .09), .005, r)
    lambeaux('Etendard', r, .12, .3, (.2, -.215, zt + .02), (0, 0, 0))
    pointe('Hampe', r, (.2, -.215, zt - .02), .14, .006)
    t = pivot('Tourelle', (0, 0, zt + .05), r)
    for s in (-1, 1):
        p = pivot(f'Archer{s}', (s * .09, 0, 0), t)
        outils.SIMPLE = True
        try: squelette(p, .32, arc_os, armure=False)
        finally: outils.SIMPLE = False
    for o in c.objects:
        if o.name.startswith('BrasD'): o.rotation_euler = (-1.45, 0, -.15)
        if o.name.startswith('BrasG'): o.rotation_euler = (-1.35, 0, .25)
    cone('Fleche', '#2b2d38', .2, .4, 4, (0, .1, zt + .05), r, (0, 0, math.pi / 4))
    pointe('Epi', r, (0, .1, zt + .45), .1, .008)
    return finir(r)

def ossuaire(nom):
    """1 · Ossuaire : crypte éventrée, grille de fer arrachée, un chevalier mort en armure rouillée en sort, épée au clair."""
    c, r, z = debut(nom)
    boite('Crypte', PIERRE, .5, .22, .32, (0, .16, z + .16), .01, r)
    arc_brise('Gueule', r, .22, .26, (0, .05, z), (0, 0, 0))
    for k in range(4): pointe(f'Barreau{k}', r, (-.08 + k * .055, -.02, z), .2, .006, (.5 - k * .2, 0, .3))
    prisme('Fronton', PIERRE2, [(-.27, 0), (.27, 0), (0, .14)], .24, (0, .16, z + .32), r)
    crane('CraneFronton', r, .035, (0, .03, z + .37), machoire=False)
    for k in range(4):
        a = k * 1.9
        crane(f'CraneTas{k}', r, .028, (math.cos(a) * .22, -.12 + math.sin(a) * .06, z + .02), (0, 0, a), machoire=False)
    t = pivot('Tourelle', (0, -.07, z), r)
    squelette(t, .55, epee_rouillee, casque=FER)
    prisme('Ecu', FER, [(-.06, .1), (.06, .1), (.06, -.02), (0, -.1), (-.06, -.02)], .02, (-.1, -.07, .27), t, metal=.6, rough=.5)
    boite('Blason', ROUILLE, .035, .025, .07, (-.1, -.085, .28), 0, t)
    for o in c.objects:
        if o.name.startswith('BrasD'): o.rotation_euler = (-1.1, 0, -.25)
    return finir(r)

def obelisque(nom):
    """2 · Obélisque de malédiction : aiguille de basalte cerclée de fer, runes sourdes, crâne enchaîné qui tourne au sommet."""
    c, r, z = debut(nom)
    cylindre('Marche', PIERRE2, .22, .2, .07, 4, (0, 0, z), r, rot=(0, 0, math.pi / 4))
    cylindre('Aiguille', NUIT, .11, .05, .72, 4, (0, 0, z + .07), r, rot=(0, 0, math.pi / 4))
    for k in range(3): anneau(f'Cerclage{k}', FER2, .095 - k * .015, .01, 4, 3, (0, 0, z + .16 + k * .2), r, (0, 0, math.pi / 4), metal=.6)
    for k in range(6):
        boite(f'Rune{k}', MAUDIT, .03, .008, .022, (0, -(.08 - k * .007), z + .12 + k * .1), 0, r, emis=1.3)
    for q in range(4):
        a = q * math.pi / 2 + math.pi / 4
        pointe(f'Epine{q}', r, (math.cos(a) * .15, math.sin(a) * .15, z + .05), .2, .016, (math.sin(a) * .35, -math.cos(a) * .35, 0), OS3)
    cr = pivot('Cristal', (0, 0, z + .96), r)
    crane('CraneMaudit', cr, .055, (0, 0, 0), lueur=MAUDIT, lueur_force=2.5)
    chaine('ChaineCrane', r, (0, 0, z + .79), (0, 0, z + .9), 3)
    return finir(r)

def autel(nom):
    """3 · Autel de peste : autel sacrificiel noirci, chaudron de fer cerclé qui bouillonne d'une peste verdâtre, crochets et chaînes."""
    c, r, z = debut(nom)
    boite('Autel', PIERRE, .5, .32, .16, (0, 0, z + .08), .008, r)
    for s in (-1, 1): crane(f'CraneAutel{s}', r, .035, (s * .2, -.165, z + .1), machoire=False)
    boite('Tache', '#3a2a1e', .2, .2, .005, (.06, -.04, z + .16), 0, r)
    for s in (-1, 1):
        cylindre(f'Montant{s}', FER, .014, .014, .5, 5, (s * .2, .06, z + .16), r, metal=.6)
        pointe(f'Croc{s}', r, (s * .2, .06, z + .66), .06, .012)
    cylindre('Traverse', FER, .012, .012, .4, 5, (-.2, .06, z + .62), r, rot=(0, math.pi / 2, 0), metal=.6)
    chaine('ChaineChaudron', r, (0, .06, z + .62), (0, .06, z + .44), 4)
    cylindre('Chaudron', FER, .13, .16, .16, 10, (0, .06, z + .17), r, metal=.5, rough=.6)
    for k in range(2): anneau(f'Cercle{k}', ROUILLE, .15 - k * .015, .008, 10, 3, (0, .06, z + .2 + k * .08), r, metal=.5)
    o = pivot('Orbe', (0, .06, z + .33), r)
    cylindre('Peste', PESTE, .13, .13, .015, 12, (0, 0, 0), o, emis=1.2)
    for k in range(3):
        sphere(f'Bulle{k}', PESTE, .018 + k % 2 * .01, (math.cos(k * 2) * .05, math.sin(k * 2) * .05, .015), (1, 1, 1), 6, 4, o, emis=1.2)
    for k in range(3):
        sphere(f'Fumee{k}', '#59663e', .05 + k * .02, (k * .02 - .02, .02, .1 + k * .09), (1, 1, .7), 7, 4, o, emis=.25)
    return finir(r)

def gargouille(nom):
    """4 · Perchoir des gargouilles : pilier gothique fendu et gargouille démoniaque en pierre, ailes osseuses, cornes et crocs."""
    c, r, z = debut(nom)
    boite('Pilier', PIERRE, .2, .2, .46, (0, 0, z + .23), .008, r)
    for s in (-1, 1): prisme(f'Contrefort{s}', PIERRE2, [(0, 0), (.08, 0), (0, .3)], .06, (s * .1, 0, z), r, (0, 0, 0 if s > 0 else math.pi))
    boite('Corniche', PIERRE2, .3, .3, .05, (0, 0, z + .485), .006, r)
    t = pivot('Tourelle', (0, 0, z + .51), r)
    G, GR = '#4f4c57', '#6a6672'
    sphere('Torse', G, .09, (0, .02, .14), (.9, 1.2, 1.1), 10, 6, t, rot=(.6, 0, 0))
    for k in range(4): pointe(f'Echine{k}', t, (0, .07 + k * .02, .2 - k * .045), .05, .01, (-.8, 0, 0), GR)
    for s in (-1, 1):
        sphere(f'Cuisse{s}', G, .05, (s * .07, -.01, .05), (.9, 1.4, 1), 7, 4, t)
        for k in range(3): pointe(f'Serre{s}{k}', t, (s * .07 + (k - 1) * .015, -.1, .01), .04, .007, (-1.4, 0, 0), OS3)
        sphere(f'Epaule{s}', G, .045, (s * .08, -.04, .2), (1, 1, 1), 7, 4, t)
        os_long(f'BrasG{s}', t, (s * .08, -.05, .19), (s * .07, -.12, .04), .016, G)
        b = pivot(f'Aile{s}', (s * .06, .08, .22), t); b.rotation_euler = (.15, s * .25, s * .5)
        bouts = [(s * .14, .26), (s * .3, .17), (s * .34, .02), (s * .26, -.12)]
        os_long(f'Avantbras{s}', b, (0, 0, 0), (s * .1, .03, .12), .012, GR)
        for k, (x, zz) in enumerate(bouts):
            os_long(f'Phalange{s}{k}', b, (s * .1, .03, .12), (x, .03, zz), .007, GR)
        pts = [(0, 0), (s * .1, .12)]
        for k, (x, zz) in enumerate(bouts):
            pts.append((x, zz))
            if k < len(bouts) - 1:
                nx, nz = bouts[k + 1]
                pts.append(((x + nx) / 2 * .78 + s * .02, (zz + nz) / 2 * .78))
        pts.append((s * .06, -.05))
        prisme(f'Membrane{s}', '#2a2730', pts if s > 0 else list(reversed(pts)), .005, (0, .03, 0), b)
    tt = pivot('Tete', (0, -.1, .24), t)
    sphere('Crane', G, .055, (0, 0, 0), (.9, 1.25, .85), 9, 5, tt)
    prisme('Machoire', GR, [(-.035, 0), (.035, 0), (.02, -.07), (-.02, -.07)], .03, (0, -.04, -.03), tt, (1.57, 0, 0))
    for s in (-1, 1):
        cone(f'Corne{s}', OS3, .016, .14, 5, (s * .03, .03, .03), tt, (-1.1, s * .35, 0))
        sphere(f'Oeil{s}', '#c25a2a', .008, (s * .025, -.055, .015), (1, .6, 1), 4, 3, tt, emis=2)
        pointe(f'Croc{s}', tt, (s * .015, -.09, -.025), .03, .005, (math.pi, 0, 0), OS)
    cylindre('Queue', G, .018, .004, .3, 4, (0, .1, .05), t, rot=(2.1, 0, 0))
    return finir(r)

def oeil(nom):
    """5 · Œil du Voile : œil sans paupière, injecté de sang, tenu dans une cage de côtes plantée dans la pierre."""
    c, r, z = debut(nom)
    cylindre('Socle', PIERRE2, .13, .15, .1, 6, (0, 0, z), r)
    for k in range(6):
        a = k * math.pi / 3
        os_long(f'Cote{k}', r, (math.cos(a) * .1, math.sin(a) * .1, z + .1), (math.cos(a) * .2, math.sin(a) * .2, z + .48), .014)
        pointe(f'Griffe{k}', r, (math.cos(a) * .2, math.sin(a) * .2, z + .48), .1, .012, (-math.sin(a) * .5, math.cos(a) * .5, 0), OS3)
    t = pivot('Tourelle', (0, 0, z + .42), r)
    sphere('Globe', '#cdbfa6', .15, (0, 0, 0), (1, 1, 1), 14, 10, t)
    sphere('Iris', '#8a6a1c', .075, (0, -.12, 0), (1, .45, 1), 12, 6, t, emis=.5)
    sphere('Pupille', NUIT, .04, (0, -.15, 0), (.45, .4, 1.25), 8, 4, t)
    for k in range(8):
        a = k * .8
        cylindre(f'Veine{k}', '#7a1e1c', .005, .002, .14, 3, (math.cos(a) * .13, .05, math.sin(a) * .13), t, rot=(1.1, a, 0))
    for k in range(3):
        cylindre(f'Nerf{k}', '#5a2228', .02 - k * .004, .006, .2, 5, (0, .12, 0), t, rot=(-1.1 + k * .3, (k - 1) * .5, 0))
    return finir(r)

def necromancien(nom):
    """6 · Nécromancien : silhouette émaciée en robe noire en lambeaux, crâne sous la capuche, bâton de vertèbres, cercle de sel et cierges."""
    c, r, z = debut(nom)
    anneau('Cercle', '#cfc8b8', .27, .006, 24, 3, (0, 0, z + .002), r)
    for q in range(5):
        a = q * 2 * math.pi / 5 + .3
        bougie(f'Cierge{q}', r, (math.cos(a) * .27, math.sin(a) * .27, z), .04 + (q % 2) * .04)
    t = pivot('Tourelle', (0, 0, z), r)
    cylindre('Robe', '#18141a', .16, .07, .44, 8, (0, 0, 0), t)
    for k in range(7):
        a = k * 2 * math.pi / 7
        lambeaux(f'Ourlet{k}', t, .07, .12, (math.cos(a) * .14, math.sin(a) * .14, .1), (0, 0, a + math.pi / 2), '#18141a')
    prisme('Cape', '#221a20', [(-.12, .4), (.12, .4), (.17, 0), (.08, .05), (0, -.02), (-.08, .04), (-.17, 0)], .01, (0, .07, .02), t, (.1, 0, 0))
    boite('Etole', '#4a2f3a', .05, .02, .3, (0, -.075, .26), 0, t)
    sphere('Capuche', '#1d171c', .075, (0, .01, .5), (1, 1.1, 1.3), 10, 6, t)
    pointe('PointeCapuche', t, (0, .05, .57), .1, .03, (.6, 0, 0), '#1d171c')
    crane('CraneN', t, .042, (0, -.035, .48), (0, 0, 0), lueur=AME, lueur_force=2.2)
    for s in (-1, 1):
        sphere(f'EpauleN{s}', '#1d171c', .045, (s * .08, 0, .42), (1, 1, .8), 7, 4, t)
        os_long(f'BrasN{s}', t, (s * .09, -.02, .4), (s * .13, -.12, .3), .011)
    p = pivot('Arme', (.13, -.12, .3), t)
    cylindre('Baton', '#241c18', .011, .011, .72, 5, (0, 0, -.3), p)
    for k in range(6): cylindre(f'Vertebre{k}', OS3, .02, .02, .016, 6, (0, 0, .27 + k * .03), p)
    crane('CraneBaton', p, .03, (0, 0, .5), lueur=AME, lueur_force=2.5)
    ob = pivot('Orbe', (-.14, -.13, .32), r)
    sphere('AmeMain', AME, .02, (0, 0, z), (1, 1, 1.3), 7, 4, ob, emis=2.5)
    return finir(r)

def puits(nom):
    """7 · Puits des âmes : margelle de mausolée, potence de fer, chaînes qui plongent, âmes pâles qui en remontent."""
    c, r, z = debut(nom)
    cylindre('Margelle', PIERRE, .23, .23, .16, 8, (0, 0, z), r)
    cylindre('Gouffre', NUIT, .17, .17, .005, 8, (0, 0, z + .16), r)
    cylindre('Fond', AME, .1, .1, .004, 8, (0, 0, z + .163), r, emis=1)
    for k in range(8):
        a = k * math.pi / 4 + math.pi / 8
        boite(f'Moellon{k}', PIERRE2, .16, .05, .035, (math.cos(a) * .22, math.sin(a) * .22, z + .17), .004, r, (0, 0, a + math.pi / 2))
    cylindre('Potence', FER, .016, .016, .6, 5, (-.2, .1, z + .16), r, metal=.6)
    cylindre('Bras', FER, .013, .013, .26, 5, (-.2, .1, z + .73), r, rot=(0, math.pi / 2, 0), metal=.6)
    chaine('ChainePuits', r, (.05, .1, z + .72), (.05, .1, z + .3), 6)
    crane('CranePotence', r, .03, (-.2, .1, z + .8), machoire=False)
    an = pivot('Anneaux', (0, 0, z + .3), r)
    for k in range(3):
        a = k * 2 * math.pi / 3
        ame = pivot(f'Ame{k}', (math.cos(a) * .12, math.sin(a) * .12, k * .09), an)
        sphere(f'AmeTete{k}', '#bfe6dc', .022, (0, 0, .04), (.9, .9, 1.2), 7, 4, ame, emis=1.3)
        cone(f'AmeQueue{k}', AME, .02, .12, 5, (0, 0, .03), ame, (math.pi, 0, 0), emis=.9)
    return finir(r)

def faucheuse(nom):
    """8 · Faucheuse : grande silhouette décharnée qui flotte au-dessus d'un gisant brisé ; manteau ouvert en couches de lambeaux
    sur une cage thoracique, capuche profonde, mains d'os, faux à lame en croissant."""
    c, r, z = debut(nom)
    boite('Gisant', PIERRE, .36, .17, .09, (0, .1, z + .045), .006, r)
    sphere('Effigie', PIERRE2, .06, (0, .03, z + .11), (1, 1.6, .5), 7, 4, r)
    prisme('EpeeGisant', FER2, [(-.01, 0), (.01, 0), (.006, .2), (0, .22), (-.006, .2)], .006, (0, .03, z + .13), r, (-1.57, 0, 0), metal=.6)
    t = pivot('Tourelle', (0, 0, z + .2), r)
    # dos et flancs du manteau (ouvert devant), trois couches de pans qui s'effilochent vers le bas
    for k in range(9):
        a = math.pi * (.15 + k * .0875) * 2
        x, y = math.sin(a) * .13, math.cos(a) * .13
        if y < -.06: continue
        lambeaux(f'Pan{k}', t, .085, .5, (x, y, .52), (0, 0, -a), '#141116')
    for k in range(7):
        a = math.pi * (.2 + k * .1) * 2
        x, y = math.sin(a) * .1, math.cos(a) * .1
        if y < -.05: continue
        lambeaux(f'SousPan{k}', t, .07, .32, (x, y, .44), (0, 0, -a), '#1e1a22')
    cylindre('Col', '#141116', .1, .07, .07, 8, (0, .02, .47), t)
    # cage thoracique visible dans l'ouverture
    cylindre('Echine', OS3, .012, .01, .24, 5, (0, .03, .22), t)
    for k in range(4):
        anneau(f'CoteF{k}', OS, .055 - abs(k - 1.5) * .007, .007, 10, 3, (0, -.005, .3 + k * .04), t, (-.15, 0, 0), echelle=(1, .7, 1))
    boite('Bassin', OS2, .08, .05, .03, (0, 0, .2), .005, t)
    # capuche profonde, pointue, visage invisible : deux braises au fond
    sphere('Capuche', '#1b171d', .085, (0, .02, .57), (1, 1.15, 1.3), 10, 6, t)
    prisme('Visiere', '#1b171d', [(-.07, 0), (.07, 0), (.05, .1), (0, .14), (-.05, .1)], .03, (0, -.06, .5), t, (.25, 0, 0))
    pointe('PointeCapuche', t, (0, .08, .65), .14, .035, (.8, 0, 0), '#1b171d')
    sphere('Vide', NUIT, .055, (0, -.045, .56), (1, .6, 1.2), 8, 4, t)
    for s in (-1, 1): sphere(f'OeilF{s}', AME, .006, (s * .02, -.085, .565), (1, .5, 1), 4, 3, t, emis=3)
    for s in (-1, 1):
        lambeaux(f'Manche{s}', t, .07, .14, (s * .11, -.06, .42), (0, s * .5, s * .4), '#141116')
        os_long(f'BrasF{s}', t, (s * .1, -.03, .44), (s * .15, -.13, .33), .011)
        for k in range(4): cone(f'DoigtF{s}{k}', OS3, .005, .055, 3, (s * .15 + (k - 1.5) * .008, -.14, .31), t, (math.pi - .2, 0, 0))
    p = pivot('Arme', (.15, -.14, .33), t); p.rotation_euler = (0, -.15, 0)
    faux(p, .72)
    return finir(r)

def colosse(nom):
    """9 · Colosse d'os (ultime) : géant assemblé d'os et de crânes, plaques de fer rivetées, chaînes, cœur d'âme dans la cage."""
    c, r, z = debut(nom)
    boite('Tombeau', PIERRE, .62, .44, .1, (0, .02, z + .05), .006, r)
    t = pivot('Tourelle', (0, 0, z + .1), r)
    for s, n in ((-1, 'G'), (1, 'D')):
        os_long(f'CuisseC{n}', t, (s * .11, .02, .32), (s * .17, -.1, .14), .034)
        os_long(f'JambeC{n}', t, (s * .17, -.1, .14), (s * .17, -.04, .02), .03)
        boite(f'Jambiere{n}', FER, .08, .07, .13, (s * .17, -.08, .09), .008, t, metal=.6, rough=.5)
        boite(f'PiedC{n}', OS3, .08, .14, .04, (s * .17, -.08, .02), .008, t)
    boite('BassinC', OS2, .26, .13, .08, (0, .03, .33), .01, t)
    lambeaux('Pagne', t, .22, .2, (0, -.04, .34))
    cylindre('ColonneC', OS3, .03, .025, .4, 6, (0, .07, .36), t, rot=(-.25, 0, 0))
    for k in range(5):
        anneau(f'CoteC{k}', OS, .14 - abs(k - 2) * .018, .012, 12, 3, (0, -.02, .44 + k * .06), t, (-.2, 0, 0), echelle=(1, .72, 1))
    cg = pivot('Orbe', (0, -.02, .55), t)
    sphere('Coeur', AME, .045, (0, 0, 0), (1, 1, 1.1), 8, 5, cg, emis=1.8)
    prisme('Plaque', ROUILLE, [(-.11, .12), (.11, .12), (.13, -.02), (0, -.07), (-.13, -.02)], .025, (0, -.11, .72), t, (-.2, 0, 0), metal=.5, rough=.6)
    for s, n in ((-1, 'G'), (1, 'D')):
        sphere(f'SpalliereC{n}', FER, .1, (s * .22, .02, .78), (1.1, 1, .7), 9, 5, t, metal=.6, rough=.45)
        for k in range(3): pointe(f'PicSp{n}{k}', t, (s * (.18 + k * .05), .02, .84), .12, .016, (0, s * .3, 0))
        os_long(f'BrasC{n}', t, (s * .24, 0, .72), (s * .32, -.1, .46), .034)
        os_long(f'AvantC{n}', t, (s * .32, -.1, .46), (s * .29, -.2, .2), .03)
        boite(f'Brassard{n}', FER, .07, .07, .12, (s * .31, -.15, .33), .006, t, (-.4, 0, 0), metal=.6)
        sphere(f'PoingC{n}', OS2, .05, (s * .29, -.21, .17), (1, 1, 1.1), 7, 5, t)
        chaine(f'ChaineC{n}', t, (s * .29, -.21, .14), (s * .29, -.15, .0), 4)
    crane('CraneC', t, .07, (0, -.07, .9), (.1, 0, 0), lueur=AME, lueur_force=2.5)
    boite('Couronne', FER, .14, .12, .02, (0, -.06, .96), 0, t, metal=.6)
    for k in range(5): pointe(f'Fleuron{k}', t, ((k - 2) * .03, -.06, .97), .06 + (k == 2) * .04, .008)
    return finir(r)

BATISSEURS = [archers, ossuaire, obelisque, autel, gargouille, oeil, necromancien, puits, faucheuse, colosse]

def tour(j):
    return BATISSEURS[j](f'ombres_{j}')
