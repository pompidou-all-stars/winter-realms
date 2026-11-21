"""Kit de créatures (2.40) : tous les monstres du bestiaire épique sont fabriqués par trois familles paramétrables.

  bipede(nom, p)     squelette BIPEDE : gobelins, orcs, ogres, trolls, géants, démons, liches (sans jambes : robe ou
                     traîne), cavaliers à pied, golems… ; tête au choix (orc, humain, rat, taureau, lézard, crâne, loup,
                     cyclope, crapaud, démon, tentacules, aucune).
  bete(nom, p)       squelette QUADRUPEDE : warg, sanglier, ours, mammouth, saurien, araignée (8 pattes), hydre (têtes
                     en plus), engins et chars (caisse rigide) ; cavalier assis possible.
  volant(nom, p)     squelette VOLANT : chauve-souris, griffon, vouivre, manticore, dragon, phénix, dracoliche.

Chaque monstre (art/monstres/<clé>.py) n'est qu'une fiche de réglages : proportions, couleurs, tête, pièces (casque,
armes, cornes, ailes…) et volumes en plus. La fabrication est commune (procédé validé sur la Brute orc et le Warg) :
corps fondu → sculpture détaillée cuite (peinture + relief) → squelette partagé → clips marche/vol, touche, mort.

Repère : modèle construit à la hauteur 1 (pieds en z = 0), regard vers -Y, côté gauche .L = +X. finir() met à la taille
du jeu : hauteur = 0,40 × z^1,8 (z de la table CR de sim.js, comme echelles.py)."""
import math
from mathutils import Vector
from .organique import (Volume as V, symetrique, miroir, squelette, corps, corps_haut, ajouter_pieces, colorier_et_lier,
                        boule, cone, corne, tore, plaque, profil, assembler, peindre_texture, lueur, finir)
from .squelettes import (BIPEDE, QUADRUPEDE, VOLANT, animer_bipede, animer_quadrupede, animer_volant, renommer_clip)

def hauteur_z(z): return .40 * z ** 1.8

# couleurs d'usage courant
FER, FER2, OR, OS_, CUIR, BOIS = '#6c7480', '#4a515c', '#e2b043', '#efe3c4', '#4a321f', '#6e4a2a'
ROUGE, NOIR, LAME = '#9a2a1e', '#22242a', '#c9d0d8'

RELIEF_PEAU = [('CLOUDS', .013, .05, None), ('CLOUDS', .005, .011, None)]
RELIEF_POIL = [('CLOUDS', .020, .020, (1.0, 11.0, 1.6)), ('CLOUDS', .006, .006, (1.0, 9.0, 1.0))]
RELIEF_PIERRE = [('VORONOI', .018, .06, None), ('CLOUDS', .006, .012, None)]
RELIEF_ECAILLE = [('VORONOI', .018, .085, None), ('CLOUDS', .003, .02, None)]   # 2.40 : écailles larges (avant : trop fines, effet de fourrure)
RELIEF_LISSE = [('CLOUDS', .004, .03, None)]
RELIEF_ROC = [('VORONOI', .03, .14, None), ('CLOUDS', .002, .015, None)]   # 2.40 : roche taillée en gros blocs fissurés (golems, titans)

def _centre(vols):
    """Les volumes hors du milieu rattachés à un os central (pectoral, oreille…) sont aussi recopiés à droite."""
    return vols + [miroir(x) for x in vols if '.L' not in x.os and x.kind == 'ellipse' and abs(x.c.x) > 1e-3
                   and not getattr(x, 'seul', False)]

def seul(v):
    """Volume qui ne doit pas être recopié de l'autre côté (cicatrice, trophée, bras unique…)."""
    v.seul = True; return v

class Kit:
    """Contexte passé aux pièces : articulations J, réglages p, et liste des lueurs (yeux, runes)."""
    def __init__(self, J, p):
        self.J, self.p, self.lueurs = {k: Vector(v) for k, v in J.items()}, p, []
    def j(self, n): return self.J[n]
    def oeil(self, nom, os_, pos, r, col=None):
        self.lueurs.append(boule(nom, col or self.p.get('oeil', '#ff5a2a'), os_, pos, r, seg=7))

def _fabriquer(nom, arm, vols, K, pieces, H, animer, p):
    vols = symetrique(_centre(vols))
    c = corps(nom, vols, voxel=p.get('voxel', .0095), lissage=5, triangles=p.get('tri', 1700))
    colorier_et_lier(c, vols, adoucir=p.get('adoucir', .025))
    haut = ajouter_pieces(corps_haut(nom, vols, voxel=p.get('voxel_haut', .0045), reliefs=p.get('relief', RELIEF_PEAU)), pieces)
    peau, lu = assembler(nom, arm, c, pieces, K.lueurs)
    peindre_texture(peau, taille=p.get('texture', 384), occl=.07, H=p.get('Hpeint', 1.0), source=haut, relief=1.0, taille_relief=p.get('texture_relief', 256),
                    taches=p.get('taches', .1), taille_taches=p.get('taille_taches', 8),
                    ecailles=p.get('ecailles', 9 if p.get('relief') is RELIEF_ECAILLE else 4 if p.get('relief') is RELIEF_ROC else 0),
                    grain=.03 if p.get('relief') in (RELIEF_ECAILLE, RELIEF_ROC) else .06)
    if lu: lueur(lu, p.get('oeil', '#ff5a2a'))
    finir(arm, H)
    animer(arm, H)
    return arm

# =================================================================== BIPÈDES
def joints_bipede(p):
    v = p.get('voute', .5); fj = p.get('jambes', .38); th = p.get('tete_h', .18); W = p.get('carrure', 1.0)
    Wh = p.get('hanches', 1.0); B = p.get('bras', 1.0)
    cou_z = 1 - th - .04; T = cou_z - fj
    ventre, poitrine = fj + .40 * T, fj + .80 * T
    ty = -.24 * v
    ep = (.22 * W, .02, poitrine + .05)
    coude = (ep[0] + .07 * W, .04, ep[2] - .19 * B)
    poignet = (coude[0] + .01, -.02, coude[2] - .17 * B)
    return {'bassin': (0, .02, fj + .02), 'ventre': (0, .03, ventre), 'poitrine': (0, .02, poitrine), 'cou': (0, ty * .55, cou_z),
            'tete': (0, ty, cou_z + .04), 'sommet': (0, ty - .02, 1.0),
            'clavicule.L': (.06 * W, .01, poitrine + .05), 'epaule.L': ep, 'coude.L': coude, 'poignet.L': poignet,
            'doigts.L': (poignet[0], poignet[1] - .02, poignet[2] - .08 * B),
            'hanche.L': (.10 * Wh, .02, fj), 'genou.L': (.12 * Wh, -.02, fj * .55), 'cheville.L': (.13 * Wh, .02, .06),
            'orteils.L': (.13 * Wh, -.09, .02)}

def _tete(K, hc, typ, c):
    """Volumes de la tête (centre hc) selon son type. c : couleurs (peau, peau2, peau3)."""
    P1, P2, P3 = c; x, y, z = hc; s = K.p.get('tete_r', 1.0); v = []
    E = lambda os_, col, cc, r, **k: v.append(V(os_, col, c=(x + cc[0] * s, y + cc[1] * s, z + cc[2] * s), r=tuple(q * s for q in r), **k))
    if typ in ('orc', 'humain', 'demon', 'cyclope'):
        big = {'orc': 1, 'humain': .88, 'demon': 1, 'cyclope': 1.15}[typ]
        E('Tete', P1, (0, 0, .02), (.098 * big, .095 * big, .098 * big))
        E('Tete', P2, (0, -.065, -.045), ((.095 if typ != 'humain' else .07), .075, .055), prio=1)           # mâchoire
        E('Tete', P3, (0, -.08, .04), (.088 * big, .037, .032), rot=(.15, 0, 0), prio=1)                      # arcade
        if typ != 'cyclope': E('Tete', P2, (0, -.105, .0), (.032, .036, .032), prio=2)                        # nez
        if typ in ('orc', 'demon'): E('Tete', P1, (.115, .025, .025), (.08, .015, .032), rot=(0, -.45, -.35))  # oreille pointue
        if typ == 'humain': E('Tete', P1, (.088, .0, .0), (.02, .03, .035))
        oy = -.092 * s
        if typ == 'cyclope': K.oeil('Oeil', 'Tete', (x, y + oy - .005, z + .025 * s), .034 * s)
        else:
            for sg, n in ((1, 'L'), (-1, 'R')): K.oeil(f'Oeil.{n}', 'Tete', (x + sg * .042 * s, y + oy, z + .017 * s), .019 * s)
    elif typ in ('rat', 'loup', 'lezard'):
        E('Tete', P1, (0, .01, .02), (.085, .09, .08))
        lg = {'rat': .14, 'loup': .15, 'lezard': .17}[typ]
        v.append(V('Tete', P2, a=(x, y - .05 * s, z), b=(x, y - lg * s, z - .03 * s), ra=.055 * s, rb=.03 * s, prio=1))
        E('Tete', NOIR if typ != 'lezard' else P3, (0, -lg - .005, -.025), (.022, .02, .02), prio=2)
        if typ == 'rat': E('Tete', P2, (.075, .03, .085), (.05, .012, .05), rot=(0, -.3, 0))                  # grandes oreilles rondes
        if typ == 'loup': E('Tete', P1, (.055, .03, .1), (.025, .02, .06), rot=(-.3, -.2, 0))
        for sg, n in ((1, 'L'), (-1, 'R')): K.oeil(f'Oeil.{n}', 'Tete', (x + sg * .05 * s, y - .06 * s, z + .04 * s), .016 * s)
    elif typ == 'taureau':
        E('Tete', P1, (0, 0, .02), (.1, .1, .095))
        v.append(V('Tete', P2, a=(x, y - .06 * s, z - .01 * s), b=(x, y - .13 * s, z - .05 * s), ra=.065 * s, rb=.058 * s, prio=1))
        E('Tete', NOIR, (0, -.18, -.045), (.04, .015, .025), prio=2)
        for sg, n in ((1, 'L'), (-1, 'R')): K.oeil(f'Oeil.{n}', 'Tete', (x + sg * .06 * s, y - .07 * s, z + .04 * s), .016 * s)
    elif typ == 'crane':
        E('Tete', OS_, (0, 0, .02), (.085, .09, .09))
        E('Tete', OS_, (0, -.06, -.05), (.06, .05, .035), prio=1)
        E('Tete', NOIR, (.035, -.08, .02), (.022, .012, .022), prio=3, rel=0)
        for sg, n in ((1, 'L'), (-1, 'R')): K.oeil(f'Oeil.{n}', 'Tete', (x + sg * .034 * s, y - .082 * s, z + .02 * s), .012 * s)
    elif typ == 'crapaud':
        E('Tete', P1, (0, -.02, 0), (.13, .11, .07))
        E('Tete', P2, (0, -.07, -.04), (.12, .07, .03), prio=1)
        for sg, n in ((1, 'L'), (-1, 'R')):
            E('Tete', P1, (sg * .07, -.03, .065), (.035, .035, .035))
            K.oeil(f'Oeil.{n}', 'Tete', (x + sg * .075 * s, y - .06 * s, z + .075 * s), .018 * s)
    elif typ == 'tentacules':
        E('Tete', P1, (0, .02, .05), (.1, .1, .12))
        E('Tete', P2, (0, -.05, -.03), (.07, .06, .06), prio=1)
        for sg, n in ((1, 'L'), (-1, 'R')): K.oeil(f'Oeil.{n}', 'Tete', (x + sg * .045 * s, y - .085 * s, z + .03 * s), .017 * s)
    return v

def bipede(nom, p):
    """p : z, couleurs (peau=(c1, c2, c3), bas, botte), proportions (voute, jambes, tete_h, carrure, hanches, bras, ventre,
    muscle), tete (type), bas_du_corps ('jambes' | 'robe' | 'traine'), queue (None | (couleur, longueur)),
    volumes (fonction K → volumes en plus), pieces (fonction K → pièces), vol (True : clip « vol » au lieu de « marche »)."""
    J = joints_bipede(p); K = Kit(J, p)
    P = p.get('peau', ('#4e9636', '#6cb04c', '#3d7a2b')); P1, P2, P3 = P
    bas, botte = p.get('bas', '#6b4a2e'), p.get('botte', '#33261a')
    W, Wh, B, m, ve = p.get('carrure', 1.0), p.get('hanches', 1.0), p.get('bras', 1.0), p.get('muscle', 1.0), p.get('ventre', 1.0)
    g = lambda n: J[n]
    fj, pz, vz, cz, tz = g('bassin')[2], g('poitrine')[2], g('ventre')[2], g('cou')[2], g('tete')[2]
    ty = g('tete')[1]
    v = [
        V('Hanches', bas, c=(0, .02, fj + .01), r=(.155 * Wh, .125, .10)),
        V('Colonne', P1, c=(0, -.005, vz), r=(.16 * max(W, Wh) * (.9 + .1 * ve), .13 * ve, .12)),
        V('Torse', P1, c=(0, .025, pz), r=(.215 * W, .16, .125)),
        V('Torse', P1, c=(.11 * W, .05, pz + .075), r=(.12 * W, .09, .07), rot=(0, -.35, 0)),            # trapèzes
        V('Torse', P1, c=(0, .07, pz + .06), r=(.15 * W, .11, .06 + .05 * p.get('voute', .5))),           # haut du dos
        V('Cou', P1, a=(0, ty * .4, cz - .02), b=(0, ty + .02, tz + .01), ra=.072 * W ** .5, rb=.065),
    ]
    if m > 0:
        v += [V('Torse', P1, c=(.085 * W, -.075, pz), r=(.095 * W * m, .06 * m, .07), rot=(0, .25, 0)),   # pectoraux
              V('Colonne', P2, c=(.037, -.13 * ve, vz + .055), r=(.036, .026, .03)),                      # abdominaux
              V('Colonne', P2, c=(.035, -.132 * ve, vz + .01), r=(.034, .025, .028)),
              V('Colonne', P1, c=(.125 * W, -.07, vz), r=(.05, .05, .075), rot=(0, 0, -.3))]
    ep, co, po = g('epaule.L'), g('coude.L'), g('poignet.L')
    v += [V('Bras.L', P1, c=ep, r=(.085 * W * max(m, .4) ** .5,) * 3),
          V('Bras.L', P1, a=ep, b=co, ra=.075 * W * max(m, .4) ** .5, rb=.058 * W ** .5),
          V('AvantBras.L', P1, a=co, b=po, ra=.066 * W ** .5, rb=.055 * W ** .5),
          V('Main.L', P2, c=(po[0], po[1] - .01, po[2] - .05 * B), r=(.06 * W ** .5, .066 * W ** .5, .062 * W ** .5))]
    corps_bas = p.get('bas_du_corps', 'jambes')
    if corps_bas == 'jambes':
        hi, ge, ch = g('hanche.L'), g('genou.L'), g('cheville.L')
        v += [V('Cuisse.L', bas, a=hi, b=ge, ra=.088 * Wh, rb=.07 * Wh),
              V('Tibia.L', botte, a=ge, b=ch, ra=.07 * Wh, rb=.06 * Wh),
              V('Pied.L', botte, c=(ch[0], -.03, .04), r=(.068 * Wh, .105, .045))]
    elif corps_bas == 'robe':     # robe jusqu'au sol (mages, prêtres)
        v += [V('Hanches', bas, a=(0, .02, fj), b=(0, .04, .06), ra=.16 * Wh, rb=.24 * Wh)]
    else:                         # traîne flottante (spectres, liches) : s'affine vers le bas sans toucher le sol
        v += [V('Hanches', bas, a=(0, .02, fj), b=(0, .12, .12), ra=.17 * Wh, rb=.05)]
    if p.get('queue'):
        qc, ql = p['queue']
        v += [V('Hanches', qc, a=(0, .12, fj), b=(0, .12 + .25 * ql, fj * .55), ra=.05, rb=.03),
              V('Hanches', qc, a=(0, .12 + .25 * ql, fj * .55), b=(0, .15 + .45 * ql, .04), ra=.03, rb=.012)]
    if p.get('masse'): v = []          # masse informe (gelées) : seuls les volumes de la fiche comptent
    v += _tete(K, (0, ty - .005, tz + .06), p.get('tete', 'orc'), P)
    if p.get('volumes'): v += p['volumes'](K)
    pieces = p['pieces'](K) if p.get('pieces') else []
    arm = squelette(nom, J, BIPEDE)
    H = p.get('H') or hauteur_z(p['z'])
    def anim(a, h):
        animer_bipede(a, h, lourd=p.get('lourd', 1.0))
        if p.get('vol'): renommer_clip(a, 'marche', 'vol')
    return _fabriquer(nom, arm, v, K, pieces, H, anim, p)

# =================================================================== BÊTES (quadrupèdes)
def joints_bete(p):
    L, h, cl = p.get('longueur', 1.0), p.get('pattes', 1.0), p.get('cou', 1.0)
    dz = (h - 1) * .30   # pattes plus longues : tout le corps monte
    tz = p.get('tete_z', 0)
    return {'bassin': (0, .40 * L, .55 + dz), 'reins': (0, .14 * L, .60 + dz), 'garrot': (0, -.18 * L, .66 + dz),
            'nuque': (0, -.18 * L - .18 * cl, .74 + dz + tz), 'museau': (0, -.18 * L - .52 * cl, .66 + dz + tz),
            'machoire': (0, -.18 * L - .26 * cl, .66 + dz + tz), 'menton': (0, -.18 * L - .48 * cl, .585 + dz + tz),
            'queue0': (0, .52 * L, .58 + dz), 'queue1': (0, .74 * L, .50 + dz), 'queue2': (0, .93 * L, .36 + dz),
            'epaule.L': (.13, -.20 * L, .55 + dz), 'coude.L': (.14, -.15 * L, .31 * h), 'poignet.L': (.13, -.21 * L, .10),
            'doigtsA.L': (.13, -.21 * L - .09, .02),
            'hanche.L': (.14, .40 * L, .50 + dz), 'jarret.L': (.15, .28 * L, .30 * h), 'cheville.L': (.15, .44 * L, .12),
            'doigtsP.L': (.15, .44 * L - .08, .02)}

def bete(nom, p):
    """p : z (ou H), poil=(c1, c2, ventre), patte, crete, longueur, pattes, cou, epaisseur, tete ('loup', 'sanglier',
    'ours', 'felin', 'lezard', 'taureau', 'mammouth', 'cheval', 'rat', 'araignee', 'aucune'), queue (longueur, 0 = aucune),
    volumes / pieces (fonctions K → listes), duree / foulee (trot)."""
    J = joints_bete(p); K = Kit(J, p)
    P1, P2, PV = p.get('poil', ('#69707a', '#8d959e', '#b3bac2')); PA, CR_ = p.get('patte', '#454a52'), p.get('crete', '#25292f')
    E = p.get('epaisseur', 1.0); g = lambda n: Vector(J[n])
    b0, re, ga, nu, mu = g('bassin'), g('reins'), g('garrot'), g('nuque'), g('museau')
    v = [V('Hanches', P1, c=(0, b0.y - .03, b0.z + .01), r=(.165 * E, .21, .16 * E)),
         V('Dos', P1, c=(0, re.y - .07, re.z - .02), r=(.18 * E, .30 * p.get('longueur', 1.0), .17 * E)),
         V('Dos', P1, c=(0, ga.y + .01, ga.z - .09), r=(.22 * E, .17, .21 * E)),
         V('Dos', PV, c=(0, (re.y + ga.y) / 2, re.z - .14 * E), r=(.12 * E, .26, .07), prio=1),
         V('Cou', P1, a=(0, ga.y - .02, ga.z + .02), b=(0, nu.y, nu.z), ra=.13 * E, rb=.11 * E ** .5)]
    for n, a, b, r1, r2 in () if p.get('sans_pattes') else (('Avant', 'epaule.L', 'coude.L', .1, .07), ('AvantBas', 'coude.L', 'poignet.L', .062, .048),
                            ('Arriere', 'hanche.L', 'jarret.L', .085, .062), ('ArriereBas', 'jarret.L', 'cheville.L', .058, .045)):
        v.append(V(n + '.L', P1 if n in ('Avant', 'Arriere') else PA, a=g(a), b=g(b), ra=r1 * E ** .6, rb=r2 * E ** .6))
    if not p.get('sans_pattes'): v += [V('Arriere.L', P1, c=(.135, b0.y - .03, b0.z - .1), r=(.10 * E, .15, .16 * E)),
          V('PatteAvant.L', PA, c=(g('poignet.L').x, g('poignet.L').y - .045, .035), r=(.06 * E ** .6, .08, .038)),
          V('PatteArriere.L', PA, c=(g('cheville.L').x, g('cheville.L').y - .04, .035), r=(.058 * E ** .6, .08, .038))]
    ql = p.get('queue', 1.0)
    if ql:
        v += [V('Queue1', P1, a=g('queue0'), b=g('queue1'), ra=.06 * ql ** .3, rb=.06 * ql ** .3),
              V('Queue2', CR_, a=g('queue1'), b=g('queue1') + (g('queue2') - g('queue1')) * ql, ra=.055 * ql ** .3, rb=.02)]
    t = p.get('tete', 'loup'); dm = mu - nu
    ct = nu + dm * .2
    if t != 'aucune':
        st = p.get('tete_r', 1.0)
        v.append(V('Tete', P1, c=(0, ct.y, ct.z + .02), r=(.125 * st, .13 * st, .11 * st)))
        if t in ('loup', 'rat', 'felin', 'lezard', 'cheval'):
            lg = {'loup': 1, 'rat': .9, 'felin': .6, 'lezard': 1.1, 'cheval': 1.05}[t]
            v.append(V('Tete', P2, a=(0, ct.y - .07, ct.z - .04), b=(0, ct.y - .07 - .17 * lg, ct.z - .08), ra=.075 * st, rb=.05 * st, prio=1))
            v.append(V('Machoire', P2, a=(0, ct.y - .03, ct.z - .095), b=(0, ct.y - .03 - .16 * lg, ct.z - .135), ra=.048 * st, rb=.032 * st, prio=1))
            v.append(V('Tete', NOIR, c=(0, ct.y - .25 * lg, ct.z - .07), r=(.03, .026, .024), prio=2, rel=0))
        elif t in ('sanglier', 'ours', 'taureau', 'mammouth'):
            lg = {'sanglier': .8, 'ours': .7, 'taureau': .65, 'mammouth': .5}[t]
            v.append(V('Tete', P2, a=(0, ct.y - .06, ct.z - .03), b=(0, ct.y - .06 - .15 * lg, ct.z - .07), ra=.085 * st, rb=.07 * st, prio=1))
            v.append(V('Tete', NOIR, c=(0, ct.y - .21 * lg - .04, ct.z - .07), r=(.045, .02, .035), prio=2, rel=0))
            if t in ('ours', 'taureau', 'mammouth'):
                v.append(V('Tete', P1, c=(.11 * st, ct.y + .02, ct.z + .07), r=(.04, .02, .04)))         # oreilles
        oy = ct.y - .07
        for sg, n in ((1, 'L'), (-1, 'R')): K.oeil(f'Oeil.{n}', 'Tete', (sg * .055 * st, oy, ct.z + .04), .018 * st)
    if p.get('volumes'): v += p['volumes'](K)
    pieces = p['pieces'](K) if p.get('pieces') else []
    arm = squelette(nom, J, QUADRUPEDE)
    H = p.get('H') or hauteur_z(p['z']) * p.get('ech', 1.3)
    return _fabriquer(nom, arm, v, K, pieces, H,
                      lambda a, h: animer_quadrupede(a, h, duree=p.get('duree', .45), foulee=p.get('foulee', .5)),
                      dict({'Hpeint': .85, 'relief': RELIEF_POIL, 'adoucir': .03, 'voxel': .0105}, **p))

# =================================================================== VOLANTS
def joints_volant(p):
    E = p.get('envergure', 1.0); L = p.get('longueur', 1.0); cl = p.get('cou', 1.0)
    return {'bassin': (0, .15 * L, .45), 'poitrine': (0, -.15 * L, .50), 'nuque': (0, -.15 * L - .17 * cl, .58),
            'museau': (0, -.15 * L - .40 * cl, .56), 'machoire': (0, -.15 * L - .22 * cl, .54), 'menton': (0, -.15 * L - .36 * cl, .51),
            'epaule.L': (.09, -.08 * L, .55), 'coude.L': (.09 + .36 * E, -.02 * L, .62), 'pointe.L': (.09 + .80 * E, .10 * L, .56),
            'hanche.L': (.07, .15 * L, .40), 'pied.L': (.08, .22 * L, .24),
            'queue0': (0, .22 * L, .44), 'queue1': (0, .22 * L + .3 * p.get('queue', 1.0), .42),
            'queue2': (0, .22 * L + .6 * p.get('queue', 1.0), .40)}

def aile(K, nom, col, col2, forme='membrane', plumes=None):
    """Aile en deux parties (bras, bout) liées aux os Aile / AileBout, des deux côtés.
    forme : 'membrane' (chauve-souris, dragon : doigts et voile) ou 'plumes' (griffon, phénix : rangées de plumes)."""
    out = []
    for sg, n in ((1, 'L'), (-1, 'R')):
        e, c, pt = K.j('epaule.L'), K.j('coude.L'), K.j('pointe.L')
        X = lambda q: (sg * q[0], q[1], q[2])
        if forme == 'membrane':
            pts1 = [(e.x, e.z), (c.x, c.z + .02), (c.x + .02, c.z - .30), (e.x + .05, e.z - .14)]
            out.append(profil(f'Voile{nom}A.{n}', col2, f'Aile.{n}', [(sg * x, z) for x, z in pts1] if sg > 0 else
                              [(sg * x, z) for x, z in reversed(pts1)], .012, pos=(0, (e.y + c.y) / 2 + .04, 0)))
            pts2 = [(c.x, c.z + .02), (pt.x, pt.z), (pt.x - .12, pt.z - .2), (c.x + .25, c.z - .32), (c.x + .02, c.z - .30)]
            out.append(profil(f'Voile{nom}B.{n}', col2, f'AileBout.{n}', [(sg * x, z) for x, z in pts2] if sg > 0 else
                              [(sg * x, z) for x, z in reversed(pts2)], .012, pos=(0, (c.y + pt.y) / 2 + .05, 0)))
            for k, (dx, dz) in enumerate(((-.12, -.2), (.05, -.3), (.2, -.28))):   # doigts de l'aile
                out.append(corne(f'Doigt{nom}{k}.{n}', col, f'AileBout.{n}', X((c.x, c.y + .02, c.z)), .014, .35, .2,
                                 rot=(0, sg * (1.2 + k * .45), 0), seg=5, n=3))
        else:
            # 2.40 : aile pleine et plate en trois couches de plumes festonnées (rémiges, plumes moyennes, couvertures),
            # couchée à l'horizontale derrière l'os : elle se lit comme une aile peinte, sans plumes éparses
            def couche(nm, os_, x0, x1, y0, z0, prof0, prof1, nb, col_c, dz):
                bord = [(x0, 0.0), (x1, 0.0)]
                for i in range(nb * 2 + 1):
                    t = 1 - i / (nb * 2); x = x0 + (x1 - x0) * t
                    pr = prof0 + (prof1 - prof0) * t
                    bord.append((x, pr + (.035 if i % 2 == 0 else 0.0)))
                pts = [(sg * x, z) for x, z in bord]
                if sg < 0: pts = list(reversed(pts))
                return profil(nm, col_c, os_, pts, .008, pos=(0, y0, z0 + dz), rot=(-math.pi / 2, 0, 0), biseau=.002)
            out.append(couche(f'Remiges{nom}.{n}', f'AileBout.{n}', c.x - .02, pt.x, (c.y + pt.y) / 2, (c.z + pt.z) / 2, .42, .18, 6, col2, 0))
            out.append(couche(f'Moyennes{nom}.{n}', f'Aile.{n}', e.x, c.x + .02, (e.y + c.y) / 2, (e.z + c.z) / 2, .34, .40, 5, col2, 0))
            out.append(couche(f'Couvertures{nom}.{n}', f'Aile.{n}', e.x, c.x + .02, (e.y + c.y) / 2, (e.z + c.z) / 2, .16, .19, 6, col, .012))
            out.append(couche(f'CouverturesB{nom}.{n}', f'AileBout.{n}', c.x - .02, pt.x - .1, (c.y + pt.y) / 2, (c.z + pt.z) / 2, .17, .09, 4, col, .012))
    return out

def volant(nom, p):
    """p : z (ou H), corps=(c1, c2, ventre), aile=(os, voile), forme ('membrane' | 'plumes'), tete ('chauve', 'bec',
    'dragon', 'felin', 'crane'), envergure, longueur, cou, queue, volumes / pieces (fonctions K → listes)."""
    J = joints_volant(p); K = Kit(J, p)
    P1, P2, PV = p.get('corps', ('#5a4a6a', '#7a6a8a', '#9a8aa8')); g = lambda n: Vector(J[n])
    b0, po, nu, mu = g('bassin'), g('poitrine'), g('nuque'), g('museau')
    ep, co = g('epaule.L'), g('coude.L')
    E = p.get('epaisseur', 1.0)
    v = [V('Hanches', P1, c=(0, b0.y, b0.z + .02), r=(.12 * E, .17, .11 * E)),
         V('Hanches', P1, c=(0, po.y + .03, po.z), r=(.14 * E, .14, .13 * E)),
         V('Hanches', PV, c=(0, (b0.y + po.y) / 2, b0.z - .06), r=(.09 * E, .18, .06), prio=1),
         V('Cou', P1, a=po, b=nu, ra=.08 * E, rb=.065),
         V('Aile.L', P1, c=ep, r=(.055, .055, .05)),
         V('Aile.L', P2, a=ep, b=co, ra=.03, rb=.018),
         V('AileBout.L', P2, a=co, b=g('pointe.L'), ra=.016, rb=.006),
         V('Patte.L', P2, a=g('hanche.L'), b=g('pied.L'), ra=.035, rb=.022)]
    if p.get('queue', 1.0):
        v += [V('Queue1', P1, a=g('queue0'), b=g('queue1'), ra=.05, rb=.035), V('Queue2', P2, a=g('queue1'), b=g('queue2'), ra=.035, rb=.008)]
    t = p.get('tete', 'dragon'); ct = nu + (mu - nu) * .25; st = p.get('tete_r', 1.0)
    v.append(V('Tete', P1, c=(0, ct.y, ct.z + .01), r=(.075 * st, .08 * st, .07 * st)))
    if t in ('dragon', 'felin', 'chauve'):
        lg = {'dragon': 1.0, 'felin': .5, 'chauve': .45}[t]
        v.append(V('Tete', P2, a=(0, ct.y - .04, ct.z - .01), b=(0, ct.y - .04 - .16 * lg, ct.z - .03), ra=.05 * st, rb=.032 * st, prio=1))
        v.append(V('Machoire', P2, a=(0, ct.y - .02, ct.z - .05), b=(0, ct.y - .02 - .15 * lg, ct.z - .07), ra=.032 * st, rb=.02 * st, prio=1))
        if t == 'chauve': v.append(V('Tete', P2, c=(.06 * st, ct.y + .02, ct.z + .08), r=(.035, .012, .06), rot=(0, -.3, 0)))
    elif t == 'bec':
        v.append(V('Tete', p.get('bec', OR), a=(0, ct.y - .05, ct.z), b=(0, ct.y - .13 * st, ct.z - .04), ra=.032 * st, rb=.008, prio=2, rel=0))
    elif t == 'crane':
        v.append(V('Tete', OS_, a=(0, ct.y - .04, ct.z), b=(0, ct.y - .2 * st, ct.z - .03), ra=.05 * st, rb=.03 * st, prio=2))
    for sg, n in ((1, 'L'), (-1, 'R')): K.oeil(f'Oeil.{n}', 'Tete', (sg * .045 * st, ct.y - .05 * st, ct.z + .03 * st), .014 * st)
    if p.get('volumes'): v += p['volumes'](K)
    col_aile, voile = p.get('aile', (P2, P1))
    pieces = aile(K, '', col_aile, voile, p.get('forme', 'membrane')) + (p['pieces'](K) if p.get('pieces') else [])
    arm = squelette(nom, J, VOLANT)
    H = p.get('H') or hauteur_z(p['z']) * p.get('ech', 1.0)
    return _fabriquer(nom, arm, v, K, pieces, H,
                      lambda a, h: animer_volant(a, h, chute=p.get('chute', .71)),   # 0,5 case de vol / échelle 0,7 des volants en jeu
                      dict({'Hpeint': .75, 'voxel': .009}, **p))

# =================================================================== PIÈCES (bibliothèque)
def _cotes(): return ((1, 'L'), (-1, 'R'))

def epaulieres(K, col=FER, taille=1.0, pointes=3, col_pointe=OS_, bord=OR):
    out = []; e = K.j('epaule.L')
    for s, n in _cotes():
        out.append(boule(f'Epauliere.{n}', col, f'Bras.{n}', (s * (e.x + .015), e.y, e.z + .035), .118 * taille, ech=(1, 1, .72), demi=True, rot=(0, s * .5, 0)))
        if bord: out.append(tore(f'Bord.{n}', bord, f'Bras.{n}', (s * (e.x + .015), e.y, e.z + .032), .116 * taille, .01, rot=(0, s * .5, 0), seg=12, seg2=4))
        for k, (dy, h) in enumerate(((-.05, .095), (.025, .12), (.09, .08))[:pointes]):
            out.append(corne(f'Pointe{k}.{n}', col_pointe, f'Bras.{n}', (s * (e.x + .045), e.y + dy, e.z + .085), .022 * taille, h * taille, .5, rot=(0, s * .35, 0)))
    return out

def casque(K, typ='cornu', col=FER, col2=OS_):
    t = K.j('tete'); s = K.p.get('tete_r', 1.0); c = (0, t.y + .01, t.z + .1 * s); out = []
    if typ in ('cornu', 'pointe', 'heaume'):
        out.append(boule('Casque', col, 'Tete', c, .108 * s, ech=(1, 1.02, .85 if typ != 'heaume' else 1.15), demi=True, rot=(-.15, 0, 0)))
        out.append(tore('Bandeau', CUIR if typ != 'heaume' else col, 'Tete', c, .107 * s, .012, rot=(-.15, 0, 0)))
    if typ == 'cornu':
        for sg, n in _cotes(): out.append(corne(f'Corne.{n}', col2, 'Tete', (sg * .085 * s, c[1] + .005, c[2] + .045 * s), .034 * s, .16 * s, 1.4, rot=(-.4, sg * 1.2, 0)))
    elif typ == 'pointe':
        out.append(cone('Pique', col, 'Tete', (0, c[1], c[2] + .07 * s), .03 * s, .002, .12 * s, seg=6))
    elif typ == 'heaume':
        out.append(plaque('Visiere', NOIR, 'Tete', (0, c[1] - .1 * s, c[2] - .02 * s), .09 * s, .01, .016))
    elif typ == 'couronne':
        out.append(tore('Couronne', col, 'Tete', (c[0], c[1], c[2] + .03 * s), .085 * s, .014, seg=12, seg2=4))
        for k in range(6):
            a = k / 6 * 2 * math.pi
            out.append(cone(f'Fleuron{k}', col, 'Tete', (math.sin(a) * .085 * s, c[1] - math.cos(a) * .085 * s, c[2] + .035 * s), .02, .002, .06 * s, seg=4))
    elif typ == 'capuche':
        out.append(boule('Capuche', col, 'Tete', (c[0], c[1] + .025, c[2] - .03 * s), .125 * s, ech=(1, 1.1, 1.2), demi=True, rot=(-.4, 0, 0)))
    return out

def cornes(K, col=OS_, taille=1.0, forme='belier'):
    t = K.j('tete'); s = K.p.get('tete_r', 1.0) * taille; out = []
    for sg, n in _cotes():
        if forme == 'belier':
            out.append(corne(f'CorneB.{n}', col, 'Tete', (sg * .07 * s, t.y + .01, t.z + .14 * s), .035 * s, .2 * s, 2.6, rot=(-.6, sg * 1.5, 0), n=6))
        elif forme == 'taureau':
            out.append(corne(f'CorneT.{n}', col, 'Tete', (sg * .09 * s, t.y, t.z + .12 * s), .03 * s, .18 * s, 1.2, rot=(0, sg * 1.6, 0)))
        else:   # droites vers l'arrière (démons)
            out.append(corne(f'CorneD.{n}', col, 'Tete', (sg * .05 * s, t.y, t.z + .15 * s), .028 * s, .22 * s, .7, rot=(-.6, sg * .25, 0)))
    return out

def defenses(K, col=OS_, taille=1.0):
    t = K.j('tete'); s = K.p.get('tete_r', 1.0) * taille
    return [corne(f'Defense.{n}', col, 'Tete', (sg * .05 * s, t.y - .1 * s, t.z + .015), .02 * s, .075 * s, .9) for sg, n in _cotes()]

def arme(K, typ='hache', cote='R', taille=1.0, col=LAME, manche=BOIS):
    """Arme tenue dans la main (cote 'R' par défaut). Types : hache, epee, masse, lance, baton, faux, marteau, gourdin, fouet."""
    sg = 1 if cote == 'L' else -1; w = K.j('poignet.L'); m = (sg * w.x, w.y - .02, w.z - .05); os_ = f'Main.{cote}'; s = taille; out = []
    if typ in ('hache', 'marteau', 'masse', 'gourdin', 'lance', 'baton', 'faux'):
        L = {'lance': .62, 'baton': .55, 'faux': .58}.get(typ, .42) * s
        out.append(cone('Manche', manche, os_, (m[0], m[1], m[2] - .1 * s), .016 * s, .014 * s, L, rot=(.25, 0, 0)))
        haut = (m[0], m[1] - .25 * L * .25 / .42, m[2] + L - .19 * s)
        if typ == 'hache':
            out.append(profil('Lame', col, os_, [(0, .085), (.14, .155), (.165, 0), (.14, -.155), (0, -.085)], .018 * s,
                              pos=(m[0] - sg * .005, m[1] - .07, m[2] + .23 * s), rot=(.25, 0, math.pi if sg < 0 else 0)))
        elif typ == 'marteau':
            out.append(plaque('Tete_marteau', col, os_, (m[0], m[1] - .07 * s, m[2] + .26 * s), .2 * s, .09 * s, .1 * s, rot=(.25, 0, 0)))
        elif typ in ('masse', 'gourdin'):
            out.append(boule('Masse', col if typ == 'masse' else manche, os_, (m[0], m[1] - .07 * s, m[2] + .27 * s), .06 * s, ech=(1, 1, 1.4), rot=(.25, 0, 0), seg=10))
            if typ == 'masse':
                for k in range(4):
                    a = k * math.pi / 2
                    out.append(cone(f'Clou{k}', col, os_, (m[0] + math.cos(a) * .055 * s, m[1] - .07 * s + math.sin(a) * .055 * s, m[2] + .27 * s), .015 * s, .001, .04 * s, rot=(math.sin(a) * 1.5, -math.cos(a) * 1.5, 0), seg=4))
        elif typ == 'lance':
            out.append(cone('Fer', col, os_, (m[0], m[1] - .155 * s, m[2] + .58 * s), .03 * s, .001, .13 * s, rot=(.25, 0, 0), seg=5))
        elif typ == 'baton':
            K.lueurs.append(boule('Orbe', K.p.get('magie', '#7fd8ff'), os_, (m[0], m[1] - .14 * s, m[2] + .5 * s), .045 * s, seg=10))
            out.append(tore('Griffe_baton', col, os_, (m[0], m[1] - .14 * s, m[2] + .48 * s), .045 * s, .01, rot=(1.3, 0, 0), seg=10, seg2=3))
        elif typ == 'faux':
            out.append(profil('Faux', col, os_, [(0, 0), (.32, .05), (.3, .0), (.05, -.06)], .012 * s, pos=(m[0], m[1] - .14 * s, m[2] + .5 * s), rot=(.25, 0, math.pi if sg < 0 else 0)))
    elif typ == 'epee':
        out.append(cone('Poignee', CUIR, os_, (m[0], m[1], m[2] - .06 * s), .014 * s, .014 * s, .09 * s, rot=(.25, 0, 0)))
        out.append(plaque('Garde', OR, os_, (m[0], m[1] - .01, m[2] + .03 * s), .1 * s, .025 * s, .02 * s, rot=(.25, 0, 0)))
        out.append(profil('Lame_epee', col, os_, [(-.025, 0), (.025, 0), (.02, .38), (0, .43), (-.02, .38)], .012 * s,
                          pos=(m[0], m[1] - .02, m[2] + .04 * s), rot=(.25, 0, 0)))
    elif typ == 'fouet':
        for k in range(5):
            out.append(corne(f'Fouet{k}', col, os_, (m[0] + sg * .03 * k, m[1] - .06 * k, m[2] - .02 * k * k), .012 * s, .1 * s, .6, rot=(1.2 + .3 * k, 0, 0), seg=5, n=3))
    return out

def bouclier(K, col=BOIS, bord=FER, cote='L', taille=1.0, embleme=None):
    sg = 1 if cote == 'L' else -1; c = K.j('coude.L'); w = K.j('poignet.L')
    pos = (sg * (c.x + .06), (c.y + w.y) / 2 - .02, (c.z + w.z) / 2)
    out = [boule('Bouclier', col, f'AvantBras.{cote}', pos, .13 * taille, ech=(.28, 1, 1), rot=(0, 0, 0), seg=14),
           tore('Bord_bouclier', bord, f'AvantBras.{cote}', pos, .125 * taille, .012, rot=(0, math.pi / 2, 0), seg=14, seg2=4)]
    if embleme: out.append(boule('Umbo', embleme, f'AvantBras.{cote}', (pos[0] + sg * .035, pos[1], pos[2]), .035 * taille, seg=8))
    return out

def ceinture(K, col=CUIR, boucle=OR, pagne=ROUGE, crane=False):
    b = K.j('bassin'); Wh = K.p.get('hanches', 1.0); z = b.z + .045; out = [tore('Ceinture', col, 'Hanches', (0, .015, z), .16 * Wh, .022, ech=(1, .86, 1))]
    if boucle: out.append(plaque('Boucle', boucle, 'Hanches', (0, -.128, z), .065, .02, .052, biseau=.006))
    if pagne:
        out.append(profil('PagneAvant', pagne, 'Hanches', [(-.07, 0), (.07, 0), (.06, -.15), (0, -.17), (-.06, -.15)], .016, pos=(0, -.115, z - .025), rot=(-.12, 0, 0)))
        out.append(profil('PagneArriere', pagne, 'Hanches', [(-.09, 0), (.09, 0), (.08, -.15), (-.08, -.15)], .016, pos=(0, .14, z - .025), rot=(.15, 0, 0)))
    if crane:
        out.append(boule('Crane', OS_, 'Hanches', (.155 * Wh, -.07, z - .025), .036, ech=(.9, .9, 1), seg=9))
        out.append(plaque('CraneMachoire', OS_, 'Hanches', (.155 * Wh, -.096, z - .05), .045, .022, .016, biseau=.004))
    return out

def cape(K, col=ROUGE, longueur=1.0):
    t = K.j('poitrine'); W = K.p.get('carrure', 1.0)
    return [profil('Cape', col, 'Torse', [(-.17 * W, 0), (.17 * W, 0), (.22 * W, -.5 * longueur), (0, -.55 * longueur), (-.22 * W, -.5 * longueur)], .012,
                   pos=(0, .15, t.z + .08), rot=(.18, 0, 0))]

def brassards(K, col=CUIR, pointes=None):
    out = []; c, w = K.j('coude.L'), K.j('poignet.L')
    for s, n in _cotes():
        p = (s * (c.x + w.x) / 2, (c.y + w.y) / 2, (c.z + w.z) / 2 - .02)
        out.append(cone(f'Brassard.{n}', col, f'AvantBras.{n}', (p[0], p[1], p[2] - .035), .066 * K.p.get('carrure', 1.0) ** .5, .062 * K.p.get('carrure', 1.0) ** .5, .07, rot=(.33, 0, 0), seg=10))
        if pointes: out.append(corne(f'PointeBras.{n}', pointes, f'AvantBras.{n}', (s * (p[0] * s + .055), p[1], p[2]), .014, .05, .3, rot=(0, s * 1.5, 0), seg=5, n=3))
    return out

def genouilleres(K, col=FER):
    g = K.j('genou.L')
    return [boule(f'Genouillere.{n}', col, f'Tibia.{n}', (s * g.x, g.y - .05, g.z + .005), .05, ech=(1, .55, 1), demi=True, rot=(-1.45, 0, 0), seg=10) for s, n in _cotes()]

def collier_crocs(K, col=OS_, cordon=CUIR, n=5):
    p = K.j('poitrine'); out = [tore('Cordon', cordon, 'Torse', (0, -.045, p.z + .045), .105, .007, rot=(.55, 0, 0), ech=(1, .9, 1), seg=12, seg2=3)]
    for k in range(n):
        a = (k - (n - 1) / 2) * .42
        out.append(corne(f'Croc{k}', col, 'Torse', (math.sin(a) * .1, -.045 - math.cos(a) * .088, p.z + .045 - math.cos(a) * .045), .011, .04, .4, rot=(math.pi - .5, 0, a), seg=5, n=3))
    return out

def ailes_dos(K, col, col2, envergure=1.0, forme='membrane'):
    """Ailes rigides dans le dos d'un bipède (démons, gargouilles) : elles suivent le torse."""
    p = K.j('poitrine'); out = []; E = envergure
    for sg, n in _cotes():
        out.append(corne(f'BrasAile.{n}', col, 'Torse', (sg * .08, .14, p.z + .06), .03, .38 * E, .5, rot=(-.3, sg * 1.0, 0), seg=6, n=4))
        pts = [(0, 0), (.42 * E, .3 * E), (.5 * E, -.05 * E), (.32 * E, -.25 * E), (.12 * E, -.2 * E)]
        out.append(profil(f'Voile.{n}', col2, 'Torse', [(sg * x, z) for x, z in (pts if sg > 0 else list(reversed(pts)))], .012,
                          pos=(sg * .08, .18, p.z + .02), rot=(.25, 0, 0)))
    return out

def meches_dos(K, col, os_=('Cou', 'Dos'), n=5, taille=1.0, rangs=True):
    """Crinière de mèches pointues le long du dos d'une bête."""
    out = []; ga, re = K.j('garrot'), K.j('reins')
    for k in range(n):
        t = k / max(1, n - 1); q = ga.lerp(re, t * 1.2); h = (.15 + .05 * math.sin(t * 3)) * taille
        o = os_[0] if t < .2 else os_[1]
        out.append(corne(f'Meche{k}', col, o, (0, q.y - .1, q.z + .14 - .02 * t), .05 * taille, h, .9, rot=(-.5, 0, 0)))
        if rangs and k < n - 1:
            for s, nn in _cotes():
                out.append(corne(f'MecheCote{k}.{nn}', col, o, (s * .075, q.y - .06, q.z + .1), .04 * taille, h * .75, .8, rot=(-.6, s * .55, 0)))
    return out

def plaques_dos(K, col, n=6, taille=1.0):
    """Plaques osseuses dressées sur le dos (stégosaure, dragon-tortue, ankylosaure)."""
    out = []; ga, b = K.j('garrot'), K.j('bassin')
    for k in range(n):
        t = k / max(1, n - 1); q = ga.lerp(b, t); h = (.12 + .1 * math.sin(t * math.pi)) * taille
        o = 'Dos' if t < .7 else 'Hanches'
        out.append(profil(f'Plaque{k}', col, o, [(-.06 * taille, 0), (.06 * taille, 0), (0, h)], .025, pos=(0, q.y, q.z + .13), rot=(0, 0, math.pi / 2)))
    return out

def griffes(K, col=OS_):
    out = []
    for s, n in _cotes():
        for pat, j in (('PatteAvant', 'poignet.L'), ('PatteArriere', 'cheville.L')):
            w = K.j(j)
            for d in (-.028, 0, .028):
                out.append(corne(f'Griffe{pat}{d}.{n}', col, f'{pat}.{n}', (s * w.x + d, w.y - .115, .03), .009, .03, -.6, rot=(-1.45, 0, 0), seg=4, n=2))
    return out

def cavalier(K, peau=('#7a9a3a', '#93b04c', '#5e7a2a'), tissu='#6b4a2e', taille=.55, tete='orc', y=None, pieces=None, z=None):
    """Cavalier assis sur le dos de la bête (volumes fondus dans le corps, rigides avec l'os Dos) et ses pièces.
    Renvoie (volumes, pièces). pieces(sx, base) → pièces supplémentaires (arme…), base = position du bassin du cavalier."""
    re = K.j('reins'); ga = K.j('garrot'); yb = y if y is not None else (re.y + ga.y) / 2
    s = taille; bz = z if z is not None else re.z + .17
    base = Vector((0, yb, bz)); P1, P2, P3 = peau
    v = [V('Dos', tissu, c=(0, yb, bz), r=(.12 * s, .1 * s, .08 * s)),
         V('Dos', P1, c=(0, yb - .01, bz + .16 * s), r=(.15 * s, .11 * s, .12 * s)),
         V('Dos', P1, c=(0, yb - .02, bz + .32 * s), r=(.1 * s, .1 * s, .1 * s)),
         V('Dos', P2, c=(0, yb - .08 * s, bz + .29 * s), r=(.07 * s, .06 * s, .05 * s), prio=1)]
    for sg in (1, -1):
        v += [V('Dos', tissu, a=(sg * .08 * s, yb, bz), b=(sg * .14 * s, yb - .1 * s, bz - .16 * s), ra=.055 * s, rb=.045 * s),
              V('Dos', P1, a=(sg * .15 * s, yb, bz + .22 * s), b=(sg * .2 * s, yb - .12 * s, bz + .12 * s), ra=.05 * s, rb=.04 * s)]
    for sg, n in _cotes(): K.oeil(f'OeilC.{n}', 'Dos', (sg * .035 * s, yb - .1 * s, bz + .33 * s), .015 * s)
    out = pieces(s, base) if pieces else []
    return v, out

def lance_cavalier(s, b, col=LAME, manche=BOIS, cote=-1, longueur=.6, bouclier=None):
    """Lance couchée vers l'avant, tenue par le cavalier (pièces liées à l'os Dos). s : taille du cavalier, b : son bassin."""
    a = 1.25; d = Vector((0, -math.sin(a), math.cos(a))); base = Vector((cote * .16 * s, b.y + .08, b.z + .12 * s))
    out = [cone('Lance', manche, 'Dos', tuple(base), .012, .01, longueur, rot=(a, 0, 0)),
           cone('FerLance', col, 'Dos', tuple(base + d * longueur), .022, .001, .09, rot=(a, 0, 0), seg=5)]
    if bouclier: out.append(boule('BouclierC', bouclier, 'Dos', (-cote * .2 * s, b.y, b.z + .17 * s), .08 * s / .55, ech=(.3, 1, 1), seg=10))
    return out
