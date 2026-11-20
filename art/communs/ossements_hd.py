"""Cour des Ossements, passe « haute définition » (2.40) : les créatures sont refaites avec le procédé des monstres
organiques (communs/tours_hd.py : corps fondu, sculpture cuite en texture peinte et en relief) et l'architecture reçoit
la peinture cuite. Les tours que le concepteur a validées (faucheuse…) gardent leur construction de ossements.py.

Changements demandés par le concepteur :
- squelettes trop grossiers → squelettes anatomiques (crâne aux orbites creuses, côtes, bassin, os longs à épiphyses) ;
- gargouille pas convaincante → démon de pierre accroupi, musculeux, cornes et ailes repliées, pierre rongée ;
- autel de peste illisible → encensoir de fer pendu à un gibet, qui crache une fumée de peste au-dessus de rats crevés."""
import bpy, math
from . import outils
from . import ossements as O
from . import tours_hd as HD
from .outils import pivot, cylindre, boite, sphere, cone, prisme, anneau
from .organique import Volume as V, boule, corne, profil, plaque, tore
from .organique import cone as cone_o

OEIL = O.AME

def yeux(t, y, z, ecart=.022, r=.006, col=OEIL):
    return [boule('OeilL', col, 'Tete', (ecart, y, z), r), boule('OeilR', col, 'Tete', (-ecart, y, z), r)]

# ---------------------------------------------------------------- pièces portées (à la hauteur 1)
def arc_long():
    """Arc d'os et de corne tenu à la verticale dans la main gauche tendue (plan YZ)."""
    pts = [(-.012, -.3), (.0, -.28), (.035, -.15), (.045, 0), (.035, .15), (0, .28), (-.012, .3), (.018, .15), (.025, 0), (.018, -.15)]
    a = profil('Arc', O.OS3, 'Main.L', pts, .012, pos=(.12, -.31, .79), rot=(0, 0, math.pi / 2))
    corde = cone_o('Corde', '#9a9078', 'Main.L', (.12, -.26, .51), .0018, .0018, .56, seg=4)
    fleche = cone_o('Fleche', '#4a3a2a', 'Main.R', (.12, -.04, .79), .003, .003, .3, rot=(math.pi / 2, 0, 0), seg=4)
    pointe = cone_o('PointeFleche', O.FER2, 'Main.R', (.12, -.34, .79), .008, 0, .03, rot=(math.pi / 2, 0, 0), seg=4)
    carquois = cone_o('Carquois', '#3a2a22', 'Torse', (.05, .07, .55), .028, .03, .24, rot=(-.25, -.3, 0), seg=8)
    return [a, corde, fleche, pointe, carquois]

def harnois_rouille(epaulieres=True, casque=True):
    p = []
    if casque:
        p.append(boule('Heaume', O.FER, 'Tete', (0, -.005, .93), .07, ech=(1, 1.1, 1.05), demi=True, rot=(-.15, 0, 0), seg=14))
        p.append(plaque('Nasal', O.FER, 'Tete', (0, -.07, .9), .012, .012, .055))
        for s in (1, -1): p.append(corne(f'Corne{s}', O.OS3, 'Tete', (s * .05, 0, .96), .014, .13, -1.2, rot=(0, s * 1.3, 0), seg=6))
    if epaulieres:
        for s, n in ((1, 'L'), (-1, 'R')):
            p.append(boule(f'Spalliere.{n}', O.ROUILLE, f'Bras.{n}', (s * .11, .01, .815), .055, ech=(1.15, 1, .75), demi=True, rot=(0, s * .45, 0)))
            p.append(corne(f'PicSp.{n}', O.FER, f'Bras.{n}', (s * .13, .01, .84), .009, .07, .3, rot=(0, s * .7, 0), seg=5))
    p.append(profil('Tabard', O.TISSU2, 'Hanches', [(-.06, 0), (.06, 0), (.055, -.2), (.03, -.24), (.01, -.19), (-.02, -.25), (-.045, -.2), (-.06, -.17)], .008,
                    pos=(0, -.04, .56)))
    p.append(tore('Ceinturon', '#3a2a22', 'Hanches', (0, .015, .53), .065, .008, ech=(1, .8, 1)))
    return p

def epee_longue():
    return [profil('Lame', O.FER2, 'Main.R', [(-.012, 0), (.012, 0), (.009, .42), (0, .47), (-.009, .42)], .006, pos=(-.06, -.2, 1.0), rot=(.5, 0, 0)),
            plaque('Garde', O.ROUILLE, 'Main.R', (-.06, -.165, .955), .09, .014, .012, rot=(.5, 0, 0)),
            cone_o('Poignee', '#2a2020', 'Main.R', (-.06, -.15, .88), .007, .007, .08, rot=(.5, 0, 0), seg=5)]

def ecu():
    return [profil('Ecu', O.FER, 'Main.L', [(-.07, .1), (.07, .1), (.07, -.02), (0, -.11), (-.07, -.02)], .014, pos=(.17, -.1, .6), rot=(0, 0, .3)),
            profil('Blason', O.TISSU2, 'Main.L', [(-.045, .07), (.045, .07), (.045, -.01), (0, -.07), (-.045, -.01)], .016, pos=(.165, -.112, .6), rot=(0, 0, .3))]

# ---------------------------------------------------------------- créatures
def archer_squelette(nom):
    J, _ = HD.joints_debout(bras_l=((.105, .01, .79), (.13, -.13, .785), (.12, -.27, .79), (.12, -.31, .79)))
    return HD.squelette_statue(nom, J, bras_r=((-.105, .01, .79), (-.15, .09, .77), (-.06, -.05, .79), (-.045, -.08, .79)),
                               pieces=arc_long(), lueurs=yeux(None, -.062, .91), H=.34, tri=1300, taille=256)

def chevalier_mort(nom):
    J, _ = HD.joints_debout(bras_l=((.105, .01, .79), (.15, -.06, .65), (.16, -.12, .6), (.16, -.14, .56)))
    return HD.squelette_statue(nom, J, bras_r=((-.105, .01, .79), (-.15, -.05, .88), (-.07, -.13, .93), (-.06, -.16, .95)),
                               pieces=harnois_rouille() + epee_longue() + ecu(), lueurs=yeux(None, -.062, .91), H=.6, tri=1700)

def colosse_os(nom):
    """Géant de 2,4 fois la carrure, os épais, spallières à pointes, couronne de fer ; le cœur d'âme reste une pièce animée."""
    J, _ = HD.joints_debout(bras_l=((.105, .01, .79), (.17, -.03, .62), (.17, -.1, .46), (.17, -.13, .4)))
    p = harnois_rouille(casque=False)
    p.append(tore('Couronne', O.FER, 'Tete', (0, -.005, .93), .05, .008, ech=(1, 1.1, 1)))
    for k in range(5): p.append(corne(f'Fleuron{k}', O.FER, 'Tete', (math.sin(k * 1.256) * .05, math.cos(k * 1.256) * .055 - .005, .935), .006, .035, .1, seg=4))
    return HD.squelette_statue(nom, J, bras_r=((-.105, .01, .79), (-.17, -.03, .62), (-.17, -.1, .46), (-.17, -.13, .4)),
                               pieces=p, lueurs=yeux(None, -.062, .91, r=.008), H=.95, tri=2200, epaisseur=1.9, cotes=5)

PIERRE_G, PIERRE_G2, PIERRE_G3 = '#7b7884', '#94919d', '#55535d'

def gargouille_statue(nom):
    """Démon de pierre accroupi sur sa corniche : bassin bas, cuisses repliées, buste couché en avant, mains agrippées au
    rebord, tête basse projetée vers l'avant, ailes à demi repliées, queue enroulée."""
    P1, P2, P3 = PIERRE_G, PIERRE_G2, PIERRE_G3
    v = [V('Torse', P1, c=(0, -.03, .37), r=(.12, .1, .15), rot=(1.0, 0, 0)),
         V('Torse', P2, c=(.06, -.11, .41), r=(.065, .05, .055), rot=(.6, .3, 0)),                # pectoraux
         V('Torse', P1, c=(.08, .0, .47), r=(.08, .07, .06), rot=(0, -.4, 0)),                    # trapèzes
         V('Colonne', P1, c=(0, .01, .27), r=(.09, .085, .085)),
         V('Hanches', P1, c=(.09, .07, .17), r=(.075, .1, .08)),
         V('Cuisse.L', P1, a=(.09, .05, .18), b=(.13, -.1, .14), ra=.058, rb=.042),
         V('Tibia.L', P1, a=(.13, -.1, .14), b=(.11, .0, .035), ra=.038, rb=.028),
         V('Pied.L', P3, a=(.11, .0, .035), b=(.115, -.1, .012), ra=.028, rb=.018),
         V('Bras.L', P1, c=(.13, -.08, .47), r=(.062, .062, .062)),
         V('Bras.L', P1, a=(.14, -.09, .45), b=(.17, -.17, .28), ra=.045, rb=.034),
         V('AvantBras.L', P1, a=(.17, -.17, .28), b=(.14, -.21, .05), ra=.037, rb=.027),
         V('Main.L', P3, c=(.14, -.23, .03), r=(.036, .048, .02)),
         V('Cou', P1, a=(0, -.09, .47), b=(0, -.17, .52), ra=.05, rb=.044),
         V('Tete', P1, c=(0, -.21, .55), r=(.054, .064, .05)),
         V('Tete', P3, c=(0, -.255, .575), r=(.052, .022, .018), rot=(.25, 0, 0), prio=1),        # arcade lourde
         V('Tete', P2, c=(0, -.27, .53), r=(.037, .044, .027), prio=1),                           # museau
         V('Tete', P2, c=(0, -.25, .5), r=(.039, .039, .016), prio=1),                            # mâchoire
         V('Tete', '#141116', c=(0, -.29, .515), r=(.03, .012, .009), prio=3, rel=0),             # gueule
         V('Tete', P1, c=(.05, -.2, .57), r=(.012, .03, .02), rot=(0, -.4, -.5)),                 # oreille en pointe
         V('Hanches', P1, a=(0, .11, .15), b=(0, .23, .06), ra=.034, rb=.022),                    # queue
         V('Hanches', P1, a=(0, .23, .06), b=(.11, .26, .02), ra=.022, rb=.01)]
    for k in range(5): v.append(V('Colonne', P3, c=(0, .07 - k * .01, .5 - k * .065), r=(.016, .02, .014)))   # échine
    p = []
    for s, n in ((1, 'L'), (-1, 'R')):
        p.append(corne(f'Corne.{n}', O.OS3, 'Tete', (s * .03, -.2, .59), .016, .14, 1.3, rot=(-.4, s * .5, 0), seg=6))
        for k in range(3):
            p.append(corne(f'Serre.{n}{k}', O.OS3, f'Main.{n}', (s * .14 + (k - 1) * .016, -.27, .02), .006, .04, .8, rot=(math.pi / 2 + .6, 0, 0), seg=4))
            p.append(corne(f'Griffe.{n}{k}', O.OS3, f'Pied.{n}', (s * .115 + (k - 1) * .014, -.11, .01), .006, .035, .6, rot=(math.pi / 2 + .3, 0, 0), seg=4))
        b0 = (s * .07, .02, .46); b1 = (s * .2, .09, .6)
        p.append(cone_o(f'AileBras.{n}', P1, 'Torse', b0, .018, .012, .2, rot=(-.6, s * -.8, 0), seg=6))
        for k, d in enumerate([(s * .34, .17, .7), (s * .37, .21, .47), (s * .28, .21, .27)]):
            L = math.dist(b1, d); dx, dy, dz = (d[i] - b1[i] for i in range(3))
            rot = (math.acos(max(-1, min(1, dz / L))), 0, math.atan2(dy, dx) + math.pi / 2)
            p.append(cone_o(f'AileDoigt.{n}{k}', P3, 'Torse', b1, .009, .004, L, rot=rot, seg=5))
        pts = [(0, 0), (.15, .08), (.15, -.04), (.17, -.1), (.12, -.24), (.07, -.16), (.0, -.22)]
        p.append(profil(f'Membrane.{n}', '#3a3842', 'Torse', [(s * x, z) for x, z in pts] if s > 0 else [(s * x, z) for x, z in reversed(pts)],
                        .006, pos=(s * .19, .15, .6), rot=(.35, 0, s * .45)))
    lu = [boule('OeilL', '#d0582a', 'Tete', (.025, -.265, .555), .007), boule('OeilR', '#d0582a', 'Tete', (-.025, -.265, .555), .007)]
    return HD.statue(nom, v, p, lu, couleur_lueur='#d0582a', relief=HD.RELIEF_PIERRE, tri=2200, voxel=.0075, H=.75, taches=.25)

RELIEF_TISSU = [('CLOUDS', .01, .07, None), ('CLOUDS', .003, .015, None)]       # plis et usure d'une robe
RELIEF_CHAIR = [('CLOUDS', .004, .03, None), ('VORONOI', .002, .01, None)]      # chair humide, veinée

def crane_statue(nom, lueur=OEIL, H=1.0):
    """Crâne seul (celui des squelettes HD), centré sur l'origine, pour les obélisques, potences et bâtons."""
    J, _ = HD.joints_debout(z0=-.92)
    v = [x for x in HD.squelette_vols(J) if x.os == 'Tete']
    return HD.statue(nom, v, (), yeux(None, -.062, -.01, r=.007, col=lueur), couleur_lueur=lueur, tri=700, voxel=.0035, H=H, taille=256)

def oeil_statue(nom):
    """Œil du Voile : globe laiteux veiné de sang, iris jaune sale, pupille fendue, nerfs arrachés à l'arrière."""
    v = [V('Tete', '#cdbfa6', c=(0, 0, 0), r=(.15, .15, .15), rel=.25),
         V('Tete', '#8a6a1c', c=(0, -.128, 0), r=(.074, .034, .074), prio=2, rel=0),
         V('Tete', '#c49a2c', c=(0, -.146, 0), r=(.05, .02, .05), prio=3, rel=0),
         V('Tete', '#100d10', c=(0, -.16, 0), r=(.016, .01, .05), prio=4, rel=0)]
    # veines saillantes qui partent des nerfs et se ramifient jusqu'au bord de l'iris
    for k in range(9):
        a = k * 2 * math.pi / 9 + .2; ca, sa = math.cos(a), math.sin(a)
        P = [(ca * R * math.sin(t), -R * math.cos(t), sa * R * math.sin(t)) for R, t in ((.153, 2.5), (.157, 1.75), (.156, 1.15), (.153, .72))]
        for q in range(3):
            v.append(V('Tete', ('#6a1414', '#8a1e1a', '#a3302a')[q], a=P[q], b=P[q + 1], ra=.011 - q * .003, rb=.008 - q * .002, prio=1, rel=.4))
        b2 = (math.cos(a + .25) * .154 * math.sin(1.0), -.154 * math.cos(1.0), math.sin(a + .25) * .154 * math.sin(1.0))
        v.append(V('Tete', '#a3302a', a=P[1], b=b2, ra=.006, rb=.003, prio=1, rel=.3))
    for k, (x, z) in enumerate(((.09, .07), (-.1, -.04), (.05, -.11), (-.06, .1))):
        v.append(V('Tete', '#c99a8a', c=(x * .8, -.05, z * .8), r=(.05, .04, .05), prio=0, rel=.25))          # chair rosée autour de l'iris
    for k, (dx, dz, r0) in enumerate(((0, 0, .06), (.07, -.05, .034), (-.06, .06, .03), (.02, .08, .024))):
        v.append(V('Cou', '#5a2228', a=(dx * .3, .12, dz * .3), b=(dx * 1.3, .32, -.14 + dz), ra=r0, rb=r0 * .4, rel=1))
    return HD.statue(nom, v, (), (), relief=RELIEF_CHAIR, tri=2200, voxel=.0035, H=1.0, taches=.3)

def cage_cotes(nom):
    """Six côtes géantes plantées dans la pierre, recourbées comme des griffes autour de l'œil."""
    v = [V('Colonne', O.OS2, c=(0, 0, .03), r=(.13, .13, .04)), V('Colonne', O.OS, c=(0, 0, .07), r=(.07, .07, .04))]
    p = []
    for k in range(6):
        a = k * math.pi / 3; ca, sa = math.cos(a), math.sin(a)
        pts = [(ca * r, sa * r, z) for r, z in ((.09, .05), (.19, .2), (.215, .38), (.16, .55))]
        for q in range(3):
            v.append(V('Torse', O.OS2 if q % 2 else O.OS, a=pts[q], b=pts[q + 1], ra=.02 - q * .003, rb=.017 - q * .003))
        v.append(V('Torse', O.OS, c=pts[0], r=(.03, .03, .03)))
        p.append(corne(f'Griffe{k}', O.OS3, 'Torse', pts[3], .011, .09, 1.0, rot=(0, -.9, a), seg=5))
    return HD.statue(nom, v, p, (), tri=1600, voxel=.005, H=1.0, taches=.2, taille=384)

ROBE, ROBE2, ROBE3 = '#18141a', '#241c22', '#3a2a30'

def necromancien_statue(nom):
    """Nécromancien émacié : robe noire en lambeaux, capuche profonde d'où sort un crâne, mains d'os ; la gauche tient
    le bâton de vertèbres, la droite est levée pour l'incantation (l'âme est une pièce animée)."""
    J, _ = HD.joints_debout(bras_l=((.105, .01, .79), (.15, -.08, .66), (.15, -.17, .6), (.15, -.2, .6)))
    sq = [x for x in HD.squelette_vols(J) if x.os in ('Tete', 'Main.L')]
    Jr = dict(J); Jr.update(zip(('epaule.L', 'coude.L', 'poignet.L', 'doigts.L'), ((.105, .01, .79), (.18, -.06, .88), (.2, -.14, .98), (.2, -.16, 1.03))))
    from .organique import miroir
    sq += [miroir(x) for x in HD.squelette_vols(Jr) if x.os == 'Main.L']
    for x in sq:
        if x.os == 'Main.L': x.os = 'Main.G'
    v = sq + [
        V('Hanches', ROBE, a=(0, .03, .05), b=(0, .02, .56), ra=.19, rb=.1),
        V('Hanches', ROBE2, c=(0, .05, .1), r=(.21, .19, .08)),
        V('Torse', ROBE, c=(0, .02, .67), r=(.12, .09, .14)),
        V('Torse', ROBE3, a=(0, -.085, .78), b=(0, -.13, .3), ra=.026, rb=.03, prio=1),                  # étole
        V('Tete', ROBE2, c=(0, .035, .93), r=(.092, .09, .105)),                                        # capuche
        V('Tete', ROBE2, a=(0, .06, 1.0), b=(0, .16, 1.08), ra=.045, rb=.008),
        V('Tete', '#0c0a0d', c=(0, -.042, .92), r=(.066, .03, .078), prio=2, rel=0),                   # ombre du visage
        V('Bras.L', ROBE, c=(.1, .01, .77), r=(.06, .06, .05))]
    v[len(sq)] = V('Hanches', ROBE, a=(0, .03, .05), b=(0, .02, .56), ra=.17, rb=.095)
    for k in range(12):                                   # plis verticaux de la robe, plus profonds vers le bas
        a = k * 2 * math.pi / 12 + .13
        v.append(V('Hanches', (ROBE, ROBE2)[k % 2], a=(math.sin(a) * .19, math.cos(a) * .17 + .03, .05),
                   b=(math.sin(a) * .095, math.cos(a) * .085 + .02, .55), ra=.032, rb=.01))
    for (e, c_, p_), s in ((((.105, .01, .79), (.15, -.08, .66), (.15, -.16, .61)), 1), (((-.105, .01, .79), (-.18, -.06, .88), (-.2, -.13, .96)), -1)):
        v.append(V('Bras.G' if s > 0 else 'Bras.R', ROBE, a=e, b=c_, ra=.04, rb=.038))
        v.append(V('Bras.G' if s > 0 else 'Bras.R', ROBE2, a=c_, b=p_, ra=.04, rb=.058))                 # manche évasée
    p = []
    for k in range(9):
        a = k * 2 * math.pi / 9; x, y = math.sin(a) * .18, math.cos(a) * .17 + .03
        p.append(profil(f'Ourlet{k}', ROBE, 'Hanches', [(-.05, 0), (.05, 0), (.04, -.07), (.015, -.04), (0, -.1), (-.02, -.05), (-.045, -.08)], .006,
                        pos=(x, y, .13), rot=(math.pi / 2 - .15, 0, -a + math.pi)))
    p.append(cone_o('Baton', '#241c18', 'Main.G', (.15, -.19, .02), .012, .01, 1.12, seg=6))
    for k in range(6): p.append(tore(f'Vertebre{k}', O.OS3, 'Main.G', (.15, -.19, .9 + k * .04), .022, .009, seg=8, seg2=4))
    p.append(boule('CraneBaton', O.OS, 'Main.G', (.15, -.19, 1.18), .042, ech=(.9, 1.1, 1)))
    lu = yeux(None, -.062, .91) + [boule('OeilB1', OEIL, 'Main.G', (.165, -.225, 1.185), .008), boule('OeilB2', OEIL, 'Main.G', (.135, -.225, 1.185), .008)]
    return HD.statue(nom, v, p, lu, relief=RELIEF_TISSU, tri=2200, voxel=.0055, H=.62, taches=.1)

def rat(nom):
    v = [V('Colonne', '#4a4038', c=(0, 0, .05), r=(.04, .07, .04)), V('Tete', '#5a4e44', c=(0, -.07, .045), r=(.025, .035, .022)),
         V('Tete', '#7a5a5a', c=(0, -.105, .04), r=(.008, .008, .007), prio=2),
         V('Hanches', '#6a5a55', a=(0, .06, .03), b=(.04, .16, .01), ra=.008, rb=.003)]
    return HD.statue(nom, v, (), (), relief=HD.RELIEF_OS, tri=260, voxel=.004, H=.5, taches=.2, taille=128)

# ---------------------------------------------------------------- tours refaites
def finir(r):
    """Peinture par sommets, neige, puis peinture cuite de l'architecture (les créatures sont déjà peintes)."""
    from .neige import enneiger
    HD.peindre_sauf_statues(r, sol=.5, cime=1.0, bruit=.12)
    enneiger(r, 6000)
    HD.peindre_architecture(r)
    return r

def archers(nom):
    """0 · Tour de guet gothique, deux archers squelettes anatomiques sur le chemin de ronde."""
    c, r, z = O.debut(nom)
    O.boite('Fut', O.PIERRE, .34, .34, .44, (0, 0, z + .22), .01, r)
    for sx in (-1, 1):
        for sy in (-1, 1):
            O.prisme(f'Contrefort{sx}{sy}', O.PIERRE2, [(0, 0), (.1, 0), (.02, .4), (0, .4)], .05, (sx * .17, sy * .17, z), r, (0, 0, math.atan2(sy, sx) + math.pi / 2))
    O.arc_brise('Porte', r, .12, .2, (0, -.176, z))
    O.arc_brise('Meurtriere', r, .04, .1, (0, -.176, z + .27))
    zt = z + .44
    O.boite('Machicoulis', O.PIERRE2, .42, .42, .05, (0, 0, zt + .025), .008, r)
    for k in range(8):
        a = k * math.pi / 4
        O.boite(f'Merlon{k}', O.PIERRE, .07, .07, .08, (max(-.18, min(.18, math.cos(a) * .21)), max(-.18, min(.18, math.sin(a) * .21)), zt + .09), .005, r)
    O.lambeaux('Etendard', r, .12, .3, (.2, -.215, zt + .02))
    O.cone('Fleche', '#2b2d38', .11, .24, 4, (0, .14, zt + .05), r, (0, 0, math.pi / 4))
    t = pivot('Tourelle', (0, 0, zt + .05), r)
    a1 = archer_squelette(nom + '_archer')
    HD.poser(a1, t, (.09, -.02, 0))
    a2 = [o.copy() if o else None for o in a1]
    for o in a2:
        if o: o.data = o.data.copy(); c.objects.link(o)
    HD.poser(a2, t, (-.09, -.02, 0), (0, 0, .12))
    return finir(r)

def ossuaire(nom):
    """1 · Crypte éventrée d'où sort un chevalier mort en harnois rouillé, épée levée."""
    c, r, z = O.debut(nom)
    O.boite('Crypte', O.PIERRE, .5, .22, .32, (0, .16, z + .16), .01, r)
    O.arc_brise('Gueule', r, .22, .26, (0, .05, z))
    for k in range(4): O.pointe(f'Barreau{k}', r, (-.08 + k * .055, -.02, z), .2, .006, (.5 - k * .2, 0, .3))
    O.prisme('Fronton', O.PIERRE2, [(-.27, 0), (.27, 0), (0, .14)], .24, (0, .16, z + .32), r)
    O.crane('CraneFronton', r, .035, (0, .03, z + .37), machoire=False)
    t = pivot('Tourelle', (0, -.07, z), r)
    HD.poser(chevalier_mort(nom + '_chevalier'), t)
    return finir(r)

def autel(nom):
    """3 · Encensoir de peste : gibet de fer, encensoir à pointes qui crache une fumée verdâtre, rats crevés au pied."""
    c, r, z = O.debut(nom)
    O.boite('Marche', O.PIERRE, .36, .3, .06, (0, .06, z + .03), .006, r)
    for s in (-1, 1):
        O.cylindre(f'Montant{s}', O.FER, .018, .016, .66, 6, (s * .17, .1, z + .06), r, metal=.6)
        O.pointe(f'Pic{s}', r, (s * .17, .1, z + .72), .07, .014)
    O.cylindre('Traverse', O.FER, .015, .015, .42, 6, (-.21, .1, z + .68), r, rot=(0, math.pi / 2, 0), metal=.6)
    for s in (-1, 1): O.boite(f'Equerre{s}', O.FER2, .09, .012, .012, (s * .12, .1, z + .63), 0, r, (0, s * .78, 0))
    O.chaine('Chaine', r, (0, .1, z + .67), (0, .1, z + .5), 5)
    o = pivot('Orbe', (0, 0, 0), pivot('Tourelle', (0, .1, z + .4), r))
    O.sphere('Panse', O.FER, .085, (0, 0, 0), (1, 1, .85), 12, 8, o, metal=.6, rough=.45)
    O.anneau('Ceinture', O.ROUILLE, .086, .009, 14, 3, (0, 0, 0), o, metal=.5)
    for k in range(8):
        a = k * math.pi / 4
        O.pointe(f'Pointe{k}', o, (math.cos(a) * .08, math.sin(a) * .08, 0), .06, .012, (-math.sin(a) * 1.57, math.cos(a) * 1.57, 0))
        O.boite(f'Ajour{k}', O.PESTE, .008, .01, .03, (math.cos(a + .4) * .08, math.sin(a + .4) * .08, .025), 0, o, (0, 0, a + .4 + math.pi / 2), emis=1.4)
    O.cone('Couvercle', O.FER2, .06, .08, 8, (0, 0, .06), o, metal=.6)
    O.sphere('Braise', O.PESTE, .05, (0, 0, -.01), (1, 1, 1), 8, 5, o, emis=1.6)
    # la fumée sera un effet animé du jeu (des boules fixes se lisaient comme des feuilles)
    for k, (x, y, a) in enumerate(((-.1, -.08, .4), (.09, -.1, -.7), (.02, .0, 1.9))):
        HD.poser(rat(f'{nom}_rat{k}'), r, (x, y, z + .06), (0, (k % 2) * 3.0, a))
    O.crane('CraneMarche', r, .028, (.13, -.04, z + .08), (0, 0, .5), machoire=False)
    return finir(r)

def gargouille(nom):
    """4 · Pilier gothique fendu et gargouille démoniaque accroupie, prête à fondre sur les volants."""
    c, r, z = O.debut(nom)
    O.boite('Pilier', O.PIERRE, .2, .2, .46, (0, 0, z + .23), .008, r)
    for s in (-1, 1): O.prisme(f'Contrefort{s}', O.PIERRE2, [(0, 0), (.08, 0), (0, .3)], .06, (s * .1, 0, z), r, (0, 0, 0 if s > 0 else math.pi))
    O.boite('Corniche', O.PIERRE2, .3, .3, .05, (0, 0, z + .485), .006, r)
    t = pivot('Tourelle', (0, .02, z + .51), r)
    HD.poser(gargouille_statue(nom + '_gargouille'), t, (0, .04, 0))
    return finir(r)

def colosse(nom):
    """9 · Colosse d'os (ultime) debout sur son tombeau, harnois rouillé, couronne de fer, cœur d'âme qui pulse dans la cage."""
    c, r, z = O.debut(nom)
    O.boite('Tombeau', O.PIERRE, .62, .44, .1, (0, .02, z + .05), .006, r)
    t = pivot('Tourelle', (0, 0, z + .1), r)
    HD.poser(colosse_os(nom + '_colosse'), t)
    cg = pivot('Orbe', (0, -.01, .68 * .95), t)
    O.sphere('Coeur', O.AME, .03, (0, 0, 0), (1, 1, 1.1), 8, 5, cg, emis=1.8)
    return finir(r)

def obelisque(nom):
    """2 · Obélisque de malédiction : aiguille de basalte cerclée de fer, runes sourdes, crâne sculpté enchaîné qui tourne."""
    c, r, z = O.debut(nom)
    O.cylindre('Marche', O.PIERRE2, .22, .2, .07, 4, (0, 0, z), r, rot=(0, 0, math.pi / 4))
    O.cylindre('Aiguille', O.NUIT, .11, .05, .72, 4, (0, 0, z + .07), r, rot=(0, 0, math.pi / 4))
    for k in range(3): O.anneau(f'Cerclage{k}', O.FER2, .095 - k * .015, .01, 4, 3, (0, 0, z + .16 + k * .2), r, (0, 0, math.pi / 4), metal=.6)
    for k in range(6):
        O.boite(f'Rune{k}', O.MAUDIT, .03, .008, .022, (0, -(.08 - k * .007), z + .12 + k * .1), 0, r, emis=1.3)
    for q in range(4):
        a = q * math.pi / 2 + math.pi / 4
        O.pointe(f'Epine{q}', r, (math.cos(a) * .15, math.sin(a) * .15, z + .05), .2, .016, (math.sin(a) * .35, -math.cos(a) * .35, 0), O.OS3)
    cr = pivot('Tourelle', (0, 0, z + .93), r)
    HD.poser(crane_statue(nom + '_crane', O.MAUDIT, H=.75), cr)
    O.chaine('ChaineCrane', r, (0, 0, z + .79), (0, 0, z + .9), 3)
    return finir(r)

def oeil(nom):
    """5 · Œil du Voile : œil sans paupière, veiné de sang, tenu par six côtes géantes plantées dans la pierre."""
    c, r, z = O.debut(nom)
    O.cylindre('Socle', O.PIERRE2, .15, .17, .06, 6, (0, 0, z), r)
    HD.poser(cage_cotes(nom + '_cage'), r, (0, 0, z + .04))
    t = pivot('Tourelle', (0, 0, z + .44), r)
    HD.poser(oeil_statue(nom + '_oeil'), t)
    return finir(r)

def necromancien(nom):
    """6 · Nécromancien sur son cercle de sel, cierges, âme qui tourne au-dessus de la main levée."""
    c, r, z = O.debut(nom)
    O.anneau('Cercle', '#cfc8b8', .27, .006, 24, 3, (0, 0, z + .002), r)
    for q in range(5):
        a = q * 2 * math.pi / 5 + .3
        O.bougie(f'Cierge{q}', r, (math.cos(a) * .27, math.sin(a) * .27, z), .04 + (q % 2) * .04)
    t = pivot('Tourelle', (0, 0, z), r)
    HD.poser(necromancien_statue(nom + '_necro'), t)
    ob = pivot('Orbe', (-.124, -.1, .7), t)
    O.sphere('AmeMain', O.AME, .022, (0, 0, 0), (1, 1, 1.3), 7, 4, ob, emis=2.5)
    return finir(r)

def puits(nom):
    """7 · Puits des âmes : margelle de mausolée, gouffre noir où luit le fond d'âmes (sans neige), potence, chaîne,
    crâne sculpté ; les âmes qui remontent sont une pièce animée."""
    c, r, z = O.debut(nom)
    O.cylindre('Margelle', O.PIERRE, .23, .23, .16, 8, (0, 0, z), r)
    sn = pivot('SansNeige', (0, 0, 0), r)
    O.cylindre('Gouffre', O.NUIT, .175, .175, .006, 8, (0, 0, z + .174), sn)
    O.cylindre('Fond', O.AME, .1, .1, .004, 8, (0, 0, z + .181), sn, emis=1)
    for k in range(8):
        a = k * math.pi / 4 + math.pi / 8
        O.boite(f'Moellon{k}', O.PIERRE2, .16, .05, .035, (math.cos(a) * .22, math.sin(a) * .22, z + .17), .004, r, (0, 0, a + math.pi / 2))
    O.cylindre('Potence', O.FER, .016, .016, .6, 5, (-.2, .1, z + .16), r, metal=.6)
    O.cylindre('Bras', O.FER, .013, .013, .26, 5, (-.2, .1, z + .73), r, rot=(0, math.pi / 2, 0), metal=.6)
    O.chaine('ChainePuits', r, (.05, .1, z + .72), (.05, .1, z + .3), 6)
    HD.poser(crane_statue(nom + '_crane', H=.5), r, (-.2, .1, z + .81))
    an = pivot('Anneaux', (0, 0, z + .3), r)
    for k in range(3):
        a = k * 2 * math.pi / 3
        ame = pivot(f'Ame{k}', (math.cos(a) * .12, math.sin(a) * .12, k * .09), an)
        O.sphere(f'AmeTete{k}', '#bfe6dc', .022, (0, 0, .04), (.9, .9, 1.2), 7, 4, ame, emis=1.3)
        O.cone(f'AmeQueue{k}', O.AME, .02, .12, 5, (0, 0, .03), ame, (math.pi, 0, 0), emis=.9)
    return finir(r)

def faucheuse(nom):
    """8 · Faucheuse validée par le concepteur : même construction, occlusion cuite sur les pièces fixes."""
    r = O.faucheuse(nom); HD.peindre_architecture(r)
    return r

def tour(j):
    """Les 10 tours de la Cour des Ossements en haute définition."""
    return [archers, ossuaire, obelisque, autel, gargouille, oeil, necromancien, puits, faucheuse, colosse][j](f'ombres_{j}')
