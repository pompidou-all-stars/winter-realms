"""Peuples « haute définition » (2.40) : humains, orcs, elfes et nains des tours, au procédé des monstres organiques
(communs/tours_hd.py : corps fondu d'un seul tenant, sculpture cuite en texture peinte et en relief).

Direction « grimdark » validée sur la Cour des Ossements : proportions réalistes (tête petite), visages durs, vêtements
usés, métal terni ; pas de grosses têtes ni de couleurs vives.

Construction à la hauteur 1 (pieds en z = 0, regard vers -Y, côté .L = +X), puis mise à la taille H par statue().
Les jambes et les détails du visage sont posés à gauche (.L) et recopiés à droite ; les deux bras sont posés à part
(bras_l, bras_r : épaule, coude, poignet, bout des doigts), pour tenir une arme ou viser."""
import math
from mathutils import Vector
from . import tours_hd as HD
from .organique import Volume as V, boule, corne, profil, plaque, tore
from .organique import cone as cone_o

RELIEF_PEAU = [('CLOUDS', .004, .035, None), ('VORONOI', .0015, .008, None)]    # peau burinée, pores
RELIEF_ETOFFE = [('CLOUDS', .007, .05, None), ('CLOUDS', .002, .012, None)]    # plis, laine, cuir
RELIEF_ECORCE = [('VORONOI', .012, .03, None), ('CLOUDS', .006, .015, None)]   # écorce, racines
RELIEF_PLUME = [('CLOUDS', .005, .02, None), ('VORONOI', .002, .006, None)]    # plumage

GABARITS = {
    #          carrure  tête  cou   nez   mâchoire oreille
    'humain': (1.0,     1.0,  1.0,  1.0,  1.0,     'ronde'),
    'orc':    (1.38,    1.05, 1.7,  1.5,  1.45,    'pointe'),
    'elfe':   (.86,     .95,  .85,  .8,   .85,     'longue'),
    'nain':   (1.55,    1.25, 1.5,  1.7,  1.2,     'ronde'),
}

def joints(bras_l, bras_r, g='humain', z0=0.0, penche=0.0):
    """Articulations (hauteur 1) ; nain : jambes courtes et buste large ; penche : buste porté vers l'avant (orc)."""
    J = {'bassin': (0, .02, .5), 'ventre': (0, .03, .6), 'poitrine': (0, .02, .7), 'cou': (0, 0, .82), 'tete': (0, -.01, .87),
         'hanche.L': (.065, .02, .49), 'genou.L': (.075, -.01, .27), 'cheville.L': (.08, .02, .06)}
    if g == 'nain':
        J.update({'bassin': (0, .02, .4), 'ventre': (0, .02, .52), 'poitrine': (0, .01, .65), 'cou': (0, 0, .77), 'tete': (0, -.01, .8),
                  'hanche.L': (.09, .02, .38), 'genou.L': (.1, -.01, .21), 'cheville.L': (.1, .02, .05)})
    if penche:
        for k, f in (('ventre', .3), ('poitrine', .6), ('cou', 1.0), ('tete', 1.15)):
            x, y, z = J[k]; J[k] = (x, y - penche * f, z - abs(penche) * f * .3)
    J['epaule.L'], J['coude.L'], J['poignet.L'], J['doigts.L'] = bras_l
    J['epaule.R'], J['coude.R'], J['poignet.R'], J['doigts.R'] = bras_r
    return {k: Vector((x, y, z + z0)) for k, (x, y, z) in J.items()}

def corps(J, g='humain', peau='#b08a74', habit='#4a4048', habit2='#3a3236', cuir='#3a2a20', cheveux=None, barbe=None,
          jupe=0.0, gants=None, ventre=1.0, bas=None):
    """Volumes d'un corps vêtu. jupe : longueur d'un pan de tunique ou de robe sous la ceinture (0 = pantalon)."""
    k, kt, kc, kn, km, oreille = GABARITS[g]
    v = []
    hc = J['tete'] + Vector((0, 0, .06 * kt))
    R = lambda x, y, z: (x * kt, y * kt, z * kt)
    # tête : crâne, mâchoire, pommettes, nez, arcades, orbites sombres, oreilles
    v += [V('Tete', peau, c=hc, r=R(.056, .064, .07)),
          V('Tete', peau, c=hc + Vector(R(0, -.03, -.046)), r=R(.044 * km, .042, .03 * km)),
          V('Joue.L', peau, c=hc + Vector(R(.03, -.045, -.01)), r=R(.018, .018, .016), prio=1),
          V('Tete', peau, a=hc + Vector(R(0, -.064, .012)), b=hc + Vector(R(0, -.078 - .01 * kn, -.022)), ra=.008 * kn * kt, rb=.012 * kn * kt, prio=1),
          V('Tete', peau, c=hc + Vector(R(0, -.056, .024)), r=R(.05, .014, .011 * km), prio=1),
          V('Oeil.L', '#16110f', c=hc + Vector(R(.023, -.06, .006)), r=R(.011, .006, .006), prio=3, rel=0)]
    if oreille == 'longue':
        v.append(V('Oreille.L', peau, a=hc + Vector(R(.05, .005, .0)), b=hc + Vector(R(.12, .04, .06)), ra=.014 * kt, rb=.003, prio=1))
    elif oreille == 'pointe':
        v.append(V('Oreille.L', peau, a=hc + Vector(R(.052, .005, -.005)), b=hc + Vector(R(.09, .02, .025)), ra=.016 * kt, rb=.004, prio=1))
    else:
        v.append(V('Oreille.L', peau, c=hc + Vector(R(.056, .006, 0)), r=R(.01, .017, .022), prio=1))
    if cheveux:
        v.append(V('Tete', cheveux, c=hc + Vector(R(0, .022, .02)), r=R(.06, .062, .066)))
    if barbe:
        v.append(V('Tete', barbe, c=hc + Vector(R(0, -.05, -.07)), r=R(.05, .036, .05 * (1.6 if g == 'nain' else 1)), prio=1))
        if g == 'nain':
            v.append(V('Tete', barbe, a=hc + Vector(R(0, -.06, -.1)), b=J['poitrine'] + Vector((0, -.1, -.08)), ra=.05, rb=.022, prio=1))
            v.append(V('Joue.L', barbe, c=hc + Vector(R(.035, -.03, -.04)), r=R(.025, .03, .045), prio=1))
    # cou, buste, ventre, bassin
    v.append(V('Cou', peau, a=J['cou'], b=hc + Vector((0, .01, -.05 * kt)), ra=.03 * kc, rb=.028 * kc))
    v += [V('Torse', habit, c=J['poitrine'] + Vector((0, 0, .03)), r=(.125 * k, .085 * k ** .5, .12)),
          V('Torse', habit, c=J['ventre'], r=(.105 * k * ventre, .08 * k ** .5 * ventre, .09)),
          V('Hanches', habit2, c=J['bassin'], r=(.1 * k, .075 * k ** .5, .07))]
    # bras (posés à part : .G à gauche, .R à droite, pas de recopie)
    for s, n in ((1, 'G'), (-1, 'R')):
        e, c_, p_, d_ = (J[f'{x}.{"L" if s > 0 else "R"}'] for x in ('epaule', 'coude', 'poignet', 'doigts'))
        v += [V(f'Bras.{n}', habit, c=e + Vector((0, 0, .005)), r=(.045 * k, .045 * k, .042 * k)),
              V(f'Bras.{n}', habit2, a=e, b=c_, ra=.033 * k, rb=.027 * k),
              V(f'AvantBras.{n}', gants or habit2, a=c_, b=p_, ra=.028 * k, rb=.022 * k),
              V(f'Main.{n}', gants or peau, c=p_.lerp(d_, .5), r=(.021 * k ** .7, .019 * k ** .7, .027 * k ** .7)),
              V(f'Main.{n}', gants or peau, a=p_.lerp(d_, .3) + Vector((0, -.012, 0)), b=p_.lerp(d_, .55) + Vector((0, -.03, .01)), ra=.008, rb=.007)]
    # jambes (gauche, recopiées) : cuisse, bottes, pied
    h, gn, ch = J['hanche.L'], J['genou.L'], J['cheville.L']
    v += [V('Cuisse.L', habit2, a=h, b=gn, ra=.045 * k ** .8, rb=.034 * k ** .8),
          V('Tibia.L', cuir, a=gn, b=ch, ra=.034 * k ** .8, rb=.029 * k ** .8),
          V('Tibia.L', cuir, c=gn + Vector((0, -.012, 0)), r=(.036 * k ** .8,) * 3),
          V('Pied.L', cuir, c=ch + Vector((0, -.035, -.032)), r=(.03 * k ** .7, .058 * k ** .7, .026))]
    if jupe:
        b = J['bassin']
        # pan évasé fait de plis (un seul gros membre finissait en boule : sphère du bout)
        tj = bas or habit; t2 = bas or habit2; bas = .1 * k + jupe * .28
        v.append(V('Hanches', tj, a=b + Vector((0, 0, .03)), b=b + Vector((0, 0, -jupe * .8)), ra=.1 * k, rb=bas * .8))
        for q in range(12):
            a_ = q * math.pi / 6 + .26
            d = Vector((math.sin(a_), math.cos(a_) * .85, 0))
            v.append(V('Hanches', tj if q % 2 else t2, a=b + d * .095 * k + Vector((0, 0, .02)), b=b + d * bas + Vector((0, 0, -jupe)),
                       ra=.026 * k, rb=.02 + jupe * .04))
    return v

def ceinture(J, col='#2a201a', boucle='#8a7440', g='humain'):
    k = GABARITS[g][0]; b = J['bassin'] + Vector((0, 0, .055))
    return [tore('Ceinture', col, 'Hanches', tuple(b), .102 * k, .012, ech=(1, .8 / k ** .5, 1)),
            plaque('Boucle', boucle, 'Hanches', tuple(b + Vector((0, -.08 * k ** .5, 0))), .03, .01, .026)]

def cape(J, col, longueur=.6, g='humain', largeur=1.0):
    """Cape tombant des épaules dans le dos, bas déchiqueté."""
    k = GABARITS[g][0] * largeur; e = J['cou'] + Vector((0, .07 * k ** .5, -.04))
    pts = [(-.13 * k, 0), (.13 * k, 0), (.17 * k, -longueur * .85), (.1 * k, -longueur), (.05 * k, -longueur * .88), (0, -longueur * .98),
           (-.06 * k, -longueur * .86), (-.11 * k, -longueur * .99), (-.17 * k, -longueur * .82)]
    return [profil('Cape', col, 'Torse', [(x, z) for x, z in pts], .008, pos=tuple(e), rot=(-.12, 0, 0))]

def humain_statue(nom, J, g='humain', pieces=(), lueurs=(), H=.4, tri=1800, voxel=.0045, taille=512, couleur_lueur='#ffd27a',
                  relief=RELIEF_ETOFFE, **kw):
    return HD.statue(nom, corps(J, g, **kw), pieces, lueurs, couleur_lueur=couleur_lueur, relief=relief, tri=tri, voxel=voxel,
                     H=H, taches=.12, taille=taille)

# ------------------------------------------------------------------ poses courantes (hauteur 1, nain : épaules à .74)
def pose_arbalete(g='humain'):
    """Arbalète épaulée, visée vers -Y."""
    z = .79 if g != 'nain' else .72; x = .105 if g != 'nain' else .15
    return ((x, .01, z), (.13, -.1, z - .1), (.06, -.2, z - .03), (.04, -.24, z - .02)), \
           ((-x, .01, z), (-.13, -.04, z - .14), (-.05, -.12, z - .07), (-.03, -.15, z - .06))

def pose_lance(g='humain'):
    """Arme d'hast tenue à deux mains devant soi, pointe vers le haut et l'avant."""
    z = .79 if g != 'nain' else .72; x = .105 if g != 'nain' else .15
    return ((x, .01, z), (.15, -.08, z - .15), (.06, -.16, z - .1), (.04, -.19, z - .09)), \
           ((-x, .01, z), (-.14, -.02, z - .2), (-.05, -.12, z - .25), (-.03, -.15, z - .26))

def pose_bras_leves(g='humain'):
    """Incantation : deux bras levés vers le ciel."""
    z = .79 if g != 'nain' else .72; x = .105 if g != 'nain' else .15
    return ((x, .01, z), (.19, -.05, z + .1), (.2, -.08, z + .26), (.2, -.09, z + .31)), \
           ((-x, .01, z), (-.19, -.05, z + .1), (-.2, -.08, z + .26), (-.2, -.09, z + .31))

def pose_lancer(g='humain'):
    """Bras droit armé derrière la tête (lancer de hache), bras gauche tendu vers la cible."""
    z = .79 if g != 'nain' else .72; x = .105 if g != 'nain' else .15
    return ((x, .01, z), (.16, -.12, z - .02), (.17, -.25, z), (.17, -.29, z)), \
           ((-x, .01, z), (-.17, .06, z + .1), (-.12, .12, z + .24), (-.11, .13, z + .29))

def pose_tirer_arc(g='elfe'):
    """Arc bandé : bras gauche tendu, main droite à la joue."""
    z = .79 if g != 'nain' else .72; x = .1
    return ((x, .01, z), (.11, -.14, z + .01), (.1, -.28, z + .02), (.1, -.32, z + .02)), \
           ((-x, .01, z), (-.12, -.06, z - .02), (-.03, -.08, z + .08), (-.02, -.1, z + .09))

def pose_repos(g='humain'):
    z = .79 if g != 'nain' else .72; x = .105 if g != 'nain' else .15
    return ((x, .01, z), (x + .03, .03, z - .19), (x + .035, 0, z - .35), (x + .035, -.02, z - .41)), \
           ((-x, .01, z), (-x - .03, .03, z - .19), (-x - .035, 0, z - .35), (-x - .035, -.02, z - .41))

# ------------------------------------------------------------------ bêtes des tours
def rapace_vols(plumage='#5a4a3a', ventre='#8a7a62', tete='#e8e2d6', bec='#c9a040', ailes=.0, chouette=False):
    """Rapace perché (aigle ou chouette), hauteur 1, regard vers -Y ; ailes : 0 repliées, 1 grandes ouvertes."""
    if chouette:
        v = [V('Torse', plumage, c=(0, 0, .42), r=(.2, .18, .26)), V('Torse', ventre, c=(0, -.08, .38), r=(.15, .1, .2), prio=1),
             V('Tete', plumage, c=(0, -.02, .74), r=(.17, .15, .14)),
             V('Disque.L', ventre, c=(.07, -.12, .74), r=(.07, .03, .075), prio=1),
             V('Oeil.L', '#141010', c=(.065, -.15, .75), r=(.03, .012, .03), prio=3, rel=0),
             V('Tete', bec, a=(0, -.15, .72), b=(0, -.17, .68), ra=.018, rb=.004, prio=2, rel=0),
             V('Aigrette.L', plumage, a=(.1, -.03, .84), b=(.14, .0, .93), ra=.03, rb=.006)]
    else:
        v = [V('Torse', plumage, c=(0, .02, .45), r=(.16, .2, .25), rot=(-.35, 0, 0)), V('Torse', ventre, c=(0, -.08, .42), r=(.12, .1, .18), prio=1),
             V('Cou', tete, a=(0, -.05, .6), b=(0, -.1, .75), ra=.09, rb=.075), V('Tete', tete, c=(0, -.12, .8), r=(.08, .1, .08)),
             V('Tete', tete, c=(0, -.16, .83), r=(.07, .04, .025), prio=1),
             V('Oeil.L', '#3a2a10', c=(.045, -.17, .815), r=(.012, .01, .01), prio=3, rel=0),
             V('Tete', bec, a=(0, -.19, .81), b=(0, -.27, .78), ra=.035, rb=.012, prio=2),
             V('Tete', bec, a=(0, -.27, .78), b=(0, -.27, .73), ra=.012, rb=.003, prio=2)]
    v += [V('Cuisse.L', plumage, a=(.08, .0, .25), b=(.08, -.02, .12), ra=.06, rb=.035),
          V('Patte.L', bec, a=(.08, -.02, .12), b=(.08, -.04, .02), ra=.02, rb=.016, rel=.3),
          V('Queue', plumage, a=(0, .15, .3), b=(0, .32, .06), ra=.08, rb=.04)]
    for q in range(3):
        v.append(V('Serre.L', '#2a2420', a=(.08, -.04, .02), b=(.08 + (q - 1) * .04, -.12, .0), ra=.012, rb=.005, rel=0))
    # ailes : bras (épaule → poignet) et rémiges
    ep = Vector((.15, .04, .58)); pg = ep.lerp(Vector((.55, .1, .85)), ailes) + Vector((.0, .1, -.25)) * (1 - ailes) + Vector((0, 0, 0))
    bout = pg + Vector((.25 * ailes + .02, .22 - ailes * .1, .2 * ailes - .25 * (1 - ailes)))
    v.append(V('Aile.L', plumage, a=ep, b=pg, ra=.07, rb=.05))
    for q in range(5):
        t = q / 4; base = ep.lerp(pg, .5 + t * .5)
        v.append(V('Aile.L', (plumage, ventre)[q % 2 if chouette else 0], a=base, b=base.lerp(bout, .5 + t * .5) + Vector((0, .1 - t * .05, -.06 * (1 - ailes))),
                   ra=.045 - t * .01, rb=.012))
    return v
