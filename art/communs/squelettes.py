"""Squelettes partagés par famille de monstres (pilote 2.30) et leurs animations.

Un squelette = des noms d'os fixes. Chaque monstre place les articulations à sa façon (joints), mais
garde les mêmes os : les animations écrites ici servent donc à toute la famille.
  BIPEDE      : gobelin, sapeur, orc, troll, chaman, prêtresse, briseur, héros, cyclope, golem
  QUADRUPEDE  : warg (puis tortue)
Clips : « marche » (boucle), « touche » (coup reçu, court), « mort » (chute, finit au sol).
"""
import math
from .organique import clip

BIPEDE = [  # (os, articulation de tête, articulation de queue, parent)
    ('Hanches', 'bassin', 'ventre', None),
    ('Colonne', 'ventre', 'poitrine', 'Hanches'),
    ('Torse', 'poitrine', 'cou', 'Colonne'),
    ('Cou', 'cou', 'tete', 'Torse'),
    ('Tete', 'tete', 'sommet', 'Cou'),
    ('Epaule.L', 'clavicule.L', 'epaule.L', 'Torse'),
    ('Bras.L', 'epaule.L', 'coude.L', 'Epaule.L'),
    ('AvantBras.L', 'coude.L', 'poignet.L', 'Bras.L'),
    ('Main.L', 'poignet.L', 'doigts.L', 'AvantBras.L'),
    ('Cuisse.L', 'hanche.L', 'genou.L', 'Hanches'),
    ('Tibia.L', 'genou.L', 'cheville.L', 'Cuisse.L'),
    ('Pied.L', 'cheville.L', 'orteils.L', 'Tibia.L'),
]

QUADRUPEDE = [
    ('Hanches', 'bassin', 'reins', None),
    ('Dos', 'reins', 'garrot', 'Hanches'),
    ('Cou', 'garrot', 'nuque', 'Dos'),
    ('Tete', 'nuque', 'museau', 'Cou'),
    ('Machoire', 'machoire', 'menton', 'Tete'),
    ('Queue1', 'queue0', 'queue1', 'Hanches'),
    ('Queue2', 'queue1', 'queue2', 'Queue1'),
    ('Avant.L', 'epaule.L', 'coude.L', 'Dos'),
    ('AvantBas.L', 'coude.L', 'poignet.L', 'Avant.L'),
    ('PatteAvant.L', 'poignet.L', 'doigtsA.L', 'AvantBas.L'),
    ('Arriere.L', 'hanche.L', 'jarret.L', 'Hanches'),
    ('ArriereBas.L', 'jarret.L', 'cheville.L', 'Arriere.L'),
    ('PatteArriere.L', 'cheville.L', 'doigtsP.L', 'ArriereBas.L'),
]

S = lambda ph: math.sin(ph * 2 * math.pi)
C = lambda ph: math.cos(ph * 2 * math.pi)
def _douce(t):
    t = max(0.0, min(1.0, t)); return t * t * (3 - 2 * t)

# Axes (os créés avec roll 0, vérifié dans Blender) : rotation locale X positive
#  - os qui montent (Hanches, Colonne, Torse, Cou, Tete) : penche vers l'AVANT ;
#  - os qui descendent (bras, jambes) : la pointe part vers l'ARRIÈRE.
# Rotation locale Z positive d'un bras : vers -X monde (vers l'intérieur pour .L, l'extérieur pour .R).
# Hanches : axe local Y = vertical (rebond), axe local Z = vers l'avant.
HAUT, BAS = 1, -1          # signe d'une rotation « vers l'avant »

def animer_bipede(arm, H, lourd=1.0):
    """Marche (plus lente et plus chaloupée si lourd > 1), coup reçu, mort."""
    d = .95 + .25 * (lourd - 1)
    jambe, genou, bras = .55, .8, .42
    av = lambda x: BAS * x      # membre vers l'avant
    pistes = {
        ('Cuisse.L', 'rot', 0): lambda ph: av(jambe * S(ph)),
        ('Cuisse.R', 'rot', 0): lambda ph: av(-jambe * S(ph)),
        # le genou plie (tibia vers l'arrière) quand la jambe revient vers l'avant
        ('Tibia.L', 'rot', 0): lambda ph: -av(genou * max(0.0, C(ph)) ** 1.5),
        ('Tibia.R', 'rot', 0): lambda ph: -av(genou * max(0.0, -C(ph)) ** 1.5),
        ('Pied.L', 'rot', 0): lambda ph: .25 * max(0.0, C(ph)) - .12 * S(ph),
        ('Pied.R', 'rot', 0): lambda ph: .25 * max(0.0, -C(ph)) + .12 * S(ph),
        ('Bras.L', 'rot', 0): lambda ph: av(-bras * S(ph)),
        ('Bras.R', 'rot', 0): lambda ph: av(bras * .6 * S(ph)),           # le bras armé balance moins
        ('AvantBras.L', 'rot', 0): lambda ph: av(.25 + .2 * max(0.0, -S(ph))),
        ('AvantBras.R', 'rot', 0): lambda ph: av(.35 + .12 * max(0.0, S(ph))),
        ('Hanches', 'loc', 1): lambda ph: H * .04 * abs(S(ph)) * lourd,  # rebond à chaque pas
        ('Hanches', 'rot', 2): lambda ph: .08 * S(ph) * lourd,            # roulis
        ('Hanches', 'rot', 1): lambda ph: .10 * S(ph),                    # torsion du bassin
        ('Colonne', 'rot', 1): lambda ph: -.08 * S(ph),
        ('Torse', 'rot', 1): lambda ph: -.06 * S(ph),
        ('Torse', 'rot', 0): lambda ph: HAUT * .05 * abs(S(ph)),
        ('Tete', 'rot', 0): lambda ph: -HAUT * .06 * abs(S(ph)),
    }
    clip(arm, 'marche', d, pistes, n=12)
    # coup reçu : le haut du corps part en arrière puis revient
    k = lambda ph: math.sin(ph * math.pi) * (1 - ph) ** .4
    clip(arm, 'touche', .35, {
        ('Colonne', 'rot', 0): lambda ph: -HAUT * .25 * k(ph),
        ('Torse', 'rot', 0): lambda ph: -HAUT * .2 * k(ph),
        ('Tete', 'rot', 0): lambda ph: -HAUT * .3 * k(ph),
        ('Bras.L', 'rot', 2): lambda ph: -.35 * k(ph),
        ('Bras.R', 'rot', 2): lambda ph: .35 * k(ph),
    }, boucle=False, n=8)
    # mort : les genoux cèdent, puis chute sur le dos (les jambes, enfants des hanches, finissent vers l'avant)
    t1 = lambda ph: _douce(ph / .4)
    t2 = lambda ph: _douce((ph - .2) / .55)
    clip(arm, 'mort', 1.1, {
        ('Hanches', 'loc', 1): lambda ph: -H * (.08 * t1(ph) + .22 * t2(ph)),
        ('Hanches', 'loc', 2): lambda ph: -H * .18 * t2(ph),
        ('Hanches', 'rot', 0): lambda ph: -HAUT * 1.4 * t2(ph),
        ('Cuisse.L', 'rot', 0): lambda ph: av(.7 * t1(ph) - .2 * t2(ph)),
        ('Cuisse.R', 'rot', 0): lambda ph: av(.5 * t1(ph)),
        ('Tibia.L', 'rot', 0): lambda ph: -av(1.1 * t1(ph) - .6 * t2(ph)),
        ('Tibia.R', 'rot', 0): lambda ph: -av(.9 * t1(ph) - .3 * t2(ph)),
        ('Colonne', 'rot', 0): lambda ph: -HAUT * .2 * t2(ph),
        ('Tete', 'rot', 0): lambda ph: -HAUT * .35 * t2(ph),
        ('Bras.L', 'rot', 2): lambda ph: -.55 * t2(ph),
        ('Bras.R', 'rot', 2): lambda ph: .55 * t2(ph),
        ('Bras.L', 'rot', 0): lambda ph: av(-.25 * t2(ph)),
        ('Bras.R', 'rot', 0): lambda ph: av(-.25 * t2(ph)),
    }, boucle=False, n=14)

def animer_quadrupede(arm, H, duree=.45, foulee=.5):
    """Trot (pattes en diagonale), coup reçu, mort (bascule sur le flanc). Rotations dans les axes du monde :
    rotation X négative = la patte part vers l'avant ; X positive sur la mâchoire = la gueule s'ouvre."""
    M = lambda r=(0, 0, 0), d=(0, 0, 0): (r, d)
    sw = lambda ph: max(0.0, C(ph)) ** 1.4          # patte levée (elle revient vers l'avant)
    pistes = {}
    for cote, dec in (('L', 0.0), ('R', .5)):
        autre = 'R' if cote == 'L' else 'L'
        pistes[(f'Avant.{cote}', 'monde')] = lambda q, d=dec: M((-foulee * S(q + d), 0, 0))
        pistes[(f'AvantBas.{cote}', 'monde')] = lambda q, d=dec: M((1.0 * sw(q + d), 0, 0))
        pistes[(f'PatteAvant.{cote}', 'monde')] = lambda q, d=dec: M((.45 * sw(q + d), 0, 0))
        # patte arrière opposée dans la même phase (trot en diagonale)
        pistes[(f'Arriere.{autre}', 'monde')] = lambda q, d=dec: M((-foulee * .9 * S(q + d), 0, 0))
        pistes[(f'ArriereBas.{autre}', 'monde')] = lambda q, d=dec: M((-.7 * sw(q + d), 0, 0))
        pistes[(f'PatteArriere.{autre}', 'monde')] = lambda q, d=dec: M((.5 * sw(q + d), 0, 0))
    pistes[('Hanches', 'monde')] = lambda q: M((.03 * S(2 * q), .04 * S(q), 0), (0, 0, H * .03 * abs(S(q))))
    pistes[('Dos', 'monde')] = lambda q: M((-.03 * S(2 * q), -.03 * S(q), .03 * S(q)))
    pistes[('Cou', 'monde')] = lambda q: M((.06 * S(2 * q + .2), 0, 0))
    pistes[('Machoire', 'monde')] = lambda q: M((.16 + .06 * S(2 * q), 0, 0))
    pistes[('Queue1', 'monde')] = lambda q: M((0, 0, .25 * S(q)))
    pistes[('Queue2', 'monde')] = lambda q: M((0, 0, .35 * S(q - .12)))
    clip(arm, 'marche', duree, pistes, n=10)
    k = lambda ph: math.sin(ph * math.pi) * (1 - ph) ** .4
    clip(arm, 'touche', .35, {
        ('Cou', 'monde'): lambda q: M((-.4 * k(q), 0, 0)),
        ('Machoire', 'monde'): lambda q: M((.4 * k(q), 0, 0)),
        ('Hanches', 'monde'): lambda q: M((0, 0, 0), (0, H * .05 * k(q), -H * .02 * k(q))),
    }, boucle=False, n=8)
    t1 = lambda ph: _douce(ph / .35)
    t2 = lambda ph: _douce((ph - .15) / .55)
    clip(arm, 'mort', 1.0, {
        ('Hanches', 'monde'): lambda q: M((0, 1.5 * t2(q), 0), (H * .08 * t2(q), 0, -H * (.08 * t1(q) + .32 * t2(q)))),
        ('Avant.L', 'monde'): lambda q: M((.5 * t1(q) - .7 * t2(q), 0, 0)),
        ('Avant.R', 'monde'): lambda q: M((.6 * t1(q) - .5 * t2(q), 0, 0)),
        ('AvantBas.L', 'monde'): lambda q: M((.9 * t1(q) - .6 * t2(q), 0, 0)),
        ('AvantBas.R', 'monde'): lambda q: M((1.0 * t1(q) - .7 * t2(q), 0, 0)),
        ('Arriere.L', 'monde'): lambda q: M((.4 * t2(q), 0, 0)),
        ('Arriere.R', 'monde'): lambda q: M((.25 * t2(q), 0, 0)),
        ('Cou', 'monde'): lambda q: M((.25 * t1(q) - .1 * t2(q), 0, 0)),
        ('Machoire', 'monde'): lambda q: M((.3 * t2(q), 0, 0)),
        ('Queue1', 'monde'): lambda q: M((.4 * t2(q), 0, 0)),
    }, boucle=False, n=12)

# 2.40 : volants (chauve-souris, griffon, vouivre, manticore, dragon, phénix, dracoliche)
VOLANT = [
    ('Hanches', 'bassin', 'poitrine', None),
    ('Cou', 'poitrine', 'nuque', 'Hanches'),
    ('Tete', 'nuque', 'museau', 'Cou'),
    ('Machoire', 'machoire', 'menton', 'Tete'),
    ('Aile.L', 'epaule.L', 'coude.L', 'Hanches'),
    ('AileBout.L', 'coude.L', 'pointe.L', 'Aile.L'),
    ('Patte.L', 'hanche.L', 'pied.L', 'Hanches'),
    ('Queue1', 'queue0', 'queue1', 'Hanches'),
    ('Queue2', 'queue1', 'queue2', 'Queue1'),
]

def animer_volant(arm, H, duree=.55, battement=.75, chute=.7):
    """Vol (battement d'ailes, corps qui monte quand les ailes descendent), coup reçu, mort (chute en vrille jusqu'au sol).
    Axes du monde : une rotation Y négative lève l'aile gauche (+X), positive lève l'aile droite.
    chute : hauteur de la chute, dans les unités du modèle (le jeu fait voler les volants à 0,5 case et les réduit)."""
    M = lambda r=(0, 0, 0), d=(0, 0, 0): (r, d)
    b = lambda q: battement * S(q)
    pistes = {('Aile.L', 'monde'): lambda q: M((0, -b(q), 0)), ('Aile.R', 'monde'): lambda q: M((0, b(q), 0)),
              ('AileBout.L', 'monde'): lambda q: M((0, -.55 * battement * S(q - .12), 0)),
              ('AileBout.R', 'monde'): lambda q: M((0, .55 * battement * S(q - .12), 0)),
              ('Hanches', 'monde'): lambda q: M((.05 * S(q + .25), 0, 0), (0, 0, -H * .06 * S(q))),
              ('Cou', 'monde'): lambda q: M((-.06 * S(q + .3), 0, 0)),
              ('Machoire', 'monde'): lambda q: M((.12 + .05 * S(2 * q), 0, 0)),
              ('Patte.L', 'monde'): lambda q: M((.5, 0, 0)), ('Patte.R', 'monde'): lambda q: M((.5, 0, 0)),
              ('Queue1', 'monde'): lambda q: M((.1 * S(q - .2), 0, .12 * S(q / 2 if False else q))),
              ('Queue2', 'monde'): lambda q: M((.15 * S(q - .35), 0, .2 * S(q - .2)))}
    clip(arm, 'vol', duree, pistes, n=12)
    k = lambda ph: math.sin(ph * math.pi) * (1 - ph) ** .4
    clip(arm, 'touche', .35, {
        ('Hanches', 'monde'): lambda q: M((-.35 * k(q), 0, 0), (0, H * .06 * k(q), H * .04 * k(q))),
        ('Cou', 'monde'): lambda q: M((-.3 * k(q), 0, 0)),
        ('Aile.L', 'monde'): lambda q: M((0, -.5 * k(q), 0)), ('Aile.R', 'monde'): lambda q: M((0, .5 * k(q), 0)),
    }, boucle=False, n=8)
    t1 = lambda ph: _douce(ph / .7)
    clip(arm, 'mort', 1.1, {
        ('Hanches', 'monde'): lambda q: M((.3 * t1(q), 0, 2.2 * t1(q)), (0, 0, -chute * t1(q) ** 1.6)),
        ('Aile.L', 'monde'): lambda q: M((0, .6 * t1(q), 0)), ('Aile.R', 'monde'): lambda q: M((0, -.6 * t1(q), 0)),
        ('AileBout.L', 'monde'): lambda q: M((0, .7 * t1(q), 0)), ('AileBout.R', 'monde'): lambda q: M((0, -.7 * t1(q), 0)),
        ('Cou', 'monde'): lambda q: M((.4 * t1(q), 0, 0)), ('Machoire', 'monde'): lambda q: M((.35 * t1(q), 0, 0)),
    }, boucle=False, n=12)

def renommer_clip(arm, ancien, nouveau):
    """Renomme une piste NLA (un bipède qui flotte dans les airs doit avoir un clip « vol », pas « marche »)."""
    for tr in arm.animation_data.nla_tracks:
        if tr.name == ancien:
            tr.name = nouveau
            for s in tr.strips: s.name = nouveau
