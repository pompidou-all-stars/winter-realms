"""Reine-araignée des glaces (palier 2, spécial, invocation — capacité à venir) — kit 2.40 : araignée géante bleu nuit à huit pattes,
abdomen marqué d'un sigle de givre, crochets, grappe d'yeux bleus ; elle lâche des araignées rapides."""
from communs.creatures import *
INFOS = {'categorie': 'monstre', 'titre': "Reine-araignée des glaces"}
P = ('#2a3448', '#3a4a64', '#9fd8ff')

def vols(K):
    b, ga = K.j('bassin'), K.j('garrot'); v = [V('Hanches', P[0], c=(0, b.y + .12, b.z + .05), r=(.26, .3, .22)),
                                              V('Hanches', P[2], c=(0, b.y + .12, b.z + .27), r=(.1, .14, .02), prio=2, rel=0)]
    # 4 paires de pattes : deux suivent les pattes avant, deux les pattes arrière (elles bougent par paires)
    for k, (os_, y0, dy) in enumerate((('Avant', -.12, -.12), ('Avant', -.02, -.02), ('Arriere', .08, .1), ('Arriere', .16, .22))):
        hz = ga.z - .05
        v += [V(f'{os_}.L', P[0], a=(.1, y0, hz), b=(.36, y0 + dy, hz + .12), ra=.035, rb=.03),
              V(f'{os_}Bas.L', P[1], a=(.36, y0 + dy, hz + .12), b=(.48, y0 + dy * 1.5, .02), ra=.03, rb=.012)]
    return v

def pieces(K):
    nu = K.j('nuque')
    for k, (x, z) in enumerate(((-.03, .03), (.03, .03), (-.06, .0), (.06, .0), (0, .06))):
        K.oeil(f'OeilA{k}', 'Tete', (x, nu.y - .12, nu.z + z), .015)
    return [corne(f'Crochet.{n}', '#d8e8f0', 'Tete', (s * .04, nu.y - .14, nu.z - .06), .018, .07, .8, rot=(math.pi - .4, 0, 0), seg=5, n=3) for s, n in ((1, 'L'), (-1, 'R'))]

def construire(ctx):
    bete('reine_araignee', dict(z=1.15, poil=P, patte=P[1], crete=P[0], tete='aucune', queue=0, sans_pattes=True, epaisseur=.8, cou=.5,
                                longueur=.8, relief=RELIEF_ECAILLE, oeil='#5ab8ff', ech=1.1, duree=.35, foulee=.4,
                                volumes=lambda K: vols(K) + [V('Tete', P[0], c=(0, K.j('nuque').y - .06, K.j('nuque').z), r=(.1, .1, .08))],
                                pieces=pieces))
